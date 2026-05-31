"""
Generates newsletter infographics in two ways:
1. AI illustration via OpenRouter (google/gemini-3-pro-image-preview) — high quality
   Falls back to Pollinations.ai if OpenRouter fails or key is missing.
2. Data chart via matplotlib — when numeric stats are present in research JSON
Both are returned as base64-encoded PNG strings for inline HTML embedding.
"""

import base64
import io
import os
import sys
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# matplotlib is optional — only used if stats are present
try:
    import matplotlib
    matplotlib.use("Agg")  # non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Newsletter color palette
COLORS = {
    "dark": "#0f172a",
    "accent": "#6366f1",
    "accent_light": "#818cf8",
    "light": "#e2e8f0",
    "white": "#ffffff",
    "text": "#1e293b",
    "muted": "#64748b",
}


def _fetch_via_openrouter(prompt: str) -> str | None:
    """Uses google/gemini-2.5-flash-image on OpenRouter. Returns base64 PNG or None.
    OpenRouter puts the image in message.images (non-standard field), not message.content."""
    if not OPENROUTER_API_KEY:
        return None
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "google/gemini-2.5-flash-image",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 512,
            },
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        message = data.get("choices", [{}])[0].get("message", {})

        # OpenRouter puts images in message.images (non-standard)
        for img in message.get("images", []):
            raw_url = img.get("image_url", {}).get("url", "")
            if raw_url.startswith("data:image"):
                return raw_url.split(",", 1)[1]
            if raw_url:
                img_resp = requests.get(raw_url, timeout=60)
                img_resp.raise_for_status()
                return base64.b64encode(img_resp.content).decode("utf-8")

        # Also check standard multimodal content list
        content = message.get("content", [])
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    raw_url = part["image_url"]["url"]
                    if raw_url.startswith("data:image"):
                        return raw_url.split(",", 1)[1]

        print("[infographic] OpenRouter returned no image in response")
        return None
    except Exception as exc:
        print(f"[infographic] OpenRouter image generation failed: {exc}")
        return None


def _fetch_via_pollinations(prompt: str, width: int = 480, height: int = 220) -> str | None:
    """Fallback: Pollinations.ai free image gen. Returns base64 PNG or None."""
    encoded = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&model=flux&nologo=true"
    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        return base64.b64encode(resp.content).decode("utf-8")
    except Exception as exc:
        print(f"[infographic] Pollinations.ai failed: {exc}")
        return None


def _fetch_ai_illustration(prompt: str) -> str | None:
    """Try OpenRouter first (high quality), fall back to Pollinations.ai."""
    print("[infographic] Trying OpenRouter (gemini-2.5-flash-image)...")
    result = _fetch_via_openrouter(prompt)
    if result:
        print("[infographic] OpenRouter image generated successfully")
        return result
    print("[infographic] Falling back to Pollinations.ai...")
    return _fetch_via_pollinations(prompt)


def _build_stat_chart(stats: list[dict]) -> str | None:
    """Builds a horizontal bar chart from stats list. Returns base64 PNG."""
    if not MATPLOTLIB_AVAILABLE:
        print("[infographic] matplotlib not available, skipping chart")
        return None
    if not stats:
        return None

    # matplotlib mathtext treats $...$ specially; disable it (rcParam added in MPL 3.5)
    try:
        plt.rcParams["text.parse_math"] = False
    except KeyError:
        pass

    labels = [str(s.get("label", ""))[:30] for s in stats]
    contexts = [str(s.get("context", "")) for s in stats]
    raw_values = [str(s.get("value", "0")) for s in stats]

    # Try to parse numeric values; fall back to index-based sizing
    numeric = []
    for v in raw_values:
        cleaned = "".join(c for c in str(v) if c.isdigit() or c in ".,-")
        cleaned = cleaned.replace(",", "")
        try:
            numeric.append(float(cleaned.split("-")[-1]))
        except ValueError:
            numeric.append(0.0)

    if all(n == 0.0 for n in numeric):
        # Use equal sizing when all are non-numeric
        numeric = [1.0] * len(stats)

    fig, ax = plt.subplots(figsize=(6, max(2.5, len(stats) * 0.7)))
    fig.patch.set_facecolor(COLORS["white"])
    ax.set_facecolor(COLORS["white"])

    bar_colors = [COLORS["accent"] if i % 2 == 0 else COLORS["accent_light"] for i in range(len(labels))]
    bars = ax.barh(labels, numeric, color=bar_colors, height=0.55, edgecolor="none")

    # Annotate bars with value + context
    for bar, raw_val, ctx in zip(bars, raw_values, contexts):
        label_text = f"{raw_val}  {ctx}" if ctx else raw_val
        ax.text(
            bar.get_width() + max(numeric) * 0.02,
            bar.get_y() + bar.get_height() / 2,
            label_text,
            va="center",
            ha="left",
            fontsize=8,
            color=COLORS["text"],
        )

    ax.set_xlim(0, max(numeric) * 1.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_color(COLORS["light"])
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.tick_params(axis="y", labelsize=9, labelcolor=COLORS["text"])
    ax.yaxis.set_tick_params(length=0)

    plt.tight_layout(pad=0.5)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=COLORS["white"])
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def generate_infographic(research: dict) -> dict:
    """
    Returns dict with:
      illustration_b64: str | None  — AI-generated contextual image
      chart_b64:        str | None  — data chart (only when stats are available)
    """
    topic = research.get("topic", "AI technology")
    infographic_prompt = research.get(
        "infographic_prompt",
        f"A clean, modern tech illustration representing {topic}. "
        "Digital art style, dark background with purple and indigo accents, "
        "futuristic but professional, high detail, 4K quality.",
    )

    illustration_b64 = _fetch_ai_illustration(infographic_prompt)

    if not illustration_b64:
        print("[infographic] All image sources failed — newsletter will render without illustration")

    stats = research.get("stats", [])
    chart_b64 = None
    if stats:
        print(f"[infographic] Generating stat chart ({len(stats)} data points)...")
        try:
            chart_b64 = _build_stat_chart(stats)
            if chart_b64:
                print("[infographic] Stat chart generated successfully")
        except Exception as exc:
            print(f"[infographic] Stat chart failed (continuing): {type(exc).__name__}: {exc}")
            chart_b64 = None

    return {"illustration_b64": illustration_b64, "chart_b64": chart_b64}


if __name__ == "__main__":
    sample = {
        "topic": "Agentic AI Systems",
        "infographic_prompt": "A network of glowing AI agents collaborating across a digital landscape, purple and indigo tones, cinematic lighting, ultra-detailed",
        "stats": [
            {"label": "Enterprise adoption", "value": "40%", "context": "Fortune 500"},
            {"label": "YoY growth", "value": "3x", "context": "agent frameworks"},
            {"label": "Cost reduction", "value": "60%", "context": "workflow automation"},
        ],
    }
    result = generate_infographic(sample)
    print(f"illustration_b64 length: {len(result['illustration_b64']) if result['illustration_b64'] else 0}")
    print(f"chart_b64 length: {len(result['chart_b64']) if result['chart_b64'] else 0}")
