"""
Researches a newsletter topic via OpenRouter using perplexity/sonar-pro,
which has built-in real-time web search grounding.
Returns structured JSON with insights, stats, sources, and tool mentions.
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TMP_DIR = Path(__file__).parent.parent / ".tmp"
MAX_RETRIES_PER_MODEL = int(os.getenv("OPENROUTER_MAX_RETRIES_PER_MODEL", "3"))
BASE_RATE_LIMIT_WAIT_SECONDS = int(os.getenv("OPENROUTER_RATE_LIMIT_WAIT_SECONDS", "30"))


def _research_models() -> list[str]:
    configured = os.getenv(
        "OPENROUTER_RESEARCH_MODELS",
        "deepseek/deepseek-v4-flash:free,openrouter/auto,google/gemini-2.5-flash",
    )
    return [m.strip() for m in configured.split(",") if m.strip()]


def research_topic(topic: str) -> dict:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in .env")

    TMP_DIR.mkdir(exist_ok=True)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    system_instruction = (
        "You are a senior AI journalist and practical-income researcher. "
        "Your readers are curious professionals who want to stay ahead of AI news AND earn money or save time with it. "
        "Every URL you provide must be a real, working homepage or well-known article — use only trusted domains "
        "(openai.com, anthropic.com, github.com, arxiv.org, techcrunch.com, theverge.com, wired.com, "
        "huggingface.co, youtube.com, reddit.com/r/MachineLearning). "
        "When unsure of a specific article URL, use the site's homepage instead. NEVER invent URLs. "
        "Return your response as valid JSON only — no markdown fences, no preamble, no trailing text."
    )

    user_prompt = f"""Research the latest AI developments for this newsletter topic and focus on THREE angles:
1. What's NEW and notable this week in AI
2. How readers can MAKE MONEY or SAVE TIME with this AI development
3. How to IMPLEMENT it in real work (concrete steps, not theory)

TOPIC: {topic}
TODAY'S DATE: {datetime.now().strftime('%B %d, %Y')}

Return a JSON object with exactly these keys:
{{
  "topic": "{topic}",
  "headline_suggestion": "A punchy 10-word headline for this topic",
  "hook": "2 sentences — lead with a surprising number or bold claim. Make it feel urgent.",
  "key_insights": [
    {{"insight": "...", "why_it_matters": "..."}},
    {{"insight": "...", "why_it_matters": "..."}},
    {{"insight": "...", "why_it_matters": "..."}},
    {{"insight": "...", "why_it_matters": "..."}},
    {{"insight": "...", "why_it_matters": "..."}}
  ],
  "deep_dive_points": [
    "What is happening and why it matters right now (2-3 sentences with specifics)",
    "The mechanics — how this actually works (2-3 sentences)",
    "Forward-looking: who wins, who loses, what to watch (2-3 sentences)"
  ],
  "money_with_ai": [
    {{"method": "Specific way to earn or save money", "how": "Exactly how to do it in 1-2 sentences", "effort": "Low/Medium/High", "earning_potential": "e.g. $50-500/month or save 5h/week"}},
    {{"method": "Another method", "how": "How to do it", "effort": "Low/Medium/High", "earning_potential": "..."}},
    {{"method": "Third method", "how": "How to do it", "effort": "Low/Medium/High", "earning_potential": "..."}}
  ],
  "implement_today": {{
    "action": "One specific thing the reader can do TODAY (not 'learn about X' — an actual task)",
    "time_needed": "e.g. 10 minutes",
    "tool": "Exact tool or service name",
    "tool_url": "https://real-homepage-url.com",
    "outcome": "What you will have or be able to do when done"
  }},
  "stats": [
    {{"label": "Stat label", "value": "numeric or short value", "context": "brief context"}},
    {{"label": "Stat label", "value": "numeric or short value", "context": "brief context"}},
    {{"label": "Stat label", "value": "numeric or short value", "context": "brief context"}}
  ],
  "tools_spotlight": {{
    "name": "Tool name (real tool relevant to this topic)",
    "tagline": "One sentence — what it does",
    "why_it_matters": "2 sentences on practical value for readers",
    "url": "https://real-homepage.com"
  }},
  "quick_bites": [
    {{"title": "...", "summary": "One sentence.", "url": "https://real-domain.com", "tag": "News"}},
    {{"title": "...", "summary": "One sentence.", "url": "https://real-domain.com", "tag": "Tool"}},
    {{"title": "...", "summary": "One sentence.", "url": "https://real-domain.com", "tag": "Opportunity"}},
    {{"title": "...", "summary": "One sentence.", "url": "https://real-domain.com", "tag": "Research"}}
  ],
  "resources": [
    {{"title": "...", "url": "https://real-domain.com", "description": "One sentence on why to read/watch/try this"}},
    {{"title": "...", "url": "https://real-domain.com", "description": "One sentence on why to read/watch/try this"}},
    {{"title": "...", "url": "https://real-domain.com", "description": "One sentence on why to read/watch/try this"}}
  ],
  "infographic_prompt": "Detailed prompt for an AI image generator — describe the scene, style (cinematic, 4K, digital art), colors (dark background, purple/indigo accents), and mood",
  "cta": "Ask readers to reply with how they are using this AI in their work or business"
}}"""

    models = _research_models()
    raw = None
    last_error = None
    for model in models:
        model_succeeded = False
        for attempt in range(MAX_RETRIES_PER_MODEL):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.2,
                )
                print(f"[research] Model used: {model}")
                raw = response.choices[0].message.content.strip()
                model_succeeded = True
                break
            except RateLimitError as exc:
                last_error = exc
                if attempt == MAX_RETRIES_PER_MODEL - 1:
                    print(f"[research] Exhausted retries for {model} — moving to next model...")
                    break
                wait = BASE_RATE_LIMIT_WAIT_SECONDS * (attempt + 1)
                print(f"[research] Rate limited on {model} — retrying in {wait}s (attempt {attempt + 1}/{MAX_RETRIES_PER_MODEL})...")
                time.sleep(wait)
            except Exception as exc:
                last_error = exc
                print(f"[research] Model failed: {model} — {exc} — trying fallback model...")
                break
        if model_succeeded:
            break
    else:
        raise RuntimeError(f"All research models failed: {models}. Last error: {last_error}") from last_error

    # Strip markdown code fences if model adds them despite instructions
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    if raw.endswith("```"):
        raw = raw[: raw.rfind("```")].strip()

    # Remove trailing commas before ] or } (common model output mistake)
    raw = re.sub(r",\s*([}\]])", r"\1", raw)

    research = json.loads(raw)

    output_path = TMP_DIR / f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path.write_text(json.dumps(research, indent=2), encoding="utf-8")
    print(f"[research] Saved to .tmp/{output_path.name}")

    return research


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "Agentic AI systems in 2026"
    result = research_topic(topic)
    print(json.dumps(result, indent=2))
