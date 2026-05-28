"""
Takes research JSON and uses google/gemini-2.5-pro via OpenRouter to produce
polished newsletter copy for every text tag in the template.
"""

import json
import os
import re
import sys
import time
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def _content_models() -> list[str]:
    configured = os.getenv(
        "OPENROUTER_CONTENT_MODELS",
        "deepseek/deepseek-v4-flash:free,openrouter/auto,google/gemini-2.5-flash",
    )
    return [m.strip() for m in configured.split(",") if m.strip()]


def generate_content(research: dict, issue_number: int, date: str | None = None) -> dict:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in .env")

    if date is None:
        date = datetime.now().strftime("%B %d, %Y")

    topic = research.get("topic", "AI & Technology")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    system_instruction = (
        "You are a newsletter writer for a practical AI publication. "
        "Your readers want two things: stay informed on AI news, and actually use AI to earn money or save time. "
        "Tone: smart, direct, zero hype. Write like a knowledgeable friend texting you what matters. "
        "Return valid JSON only — no markdown fences, no preamble, no trailing text."
    )

    prompt = f"""Using the research below, write the final newsletter copy for Issue #{issue_number}.

RESEARCH:
{json.dumps(research, indent=2)}

DATE: {date}
ISSUE NUMBER: {issue_number}

Return a JSON object with EXACTLY these keys:

{{
  "issue_number": {issue_number},
  "date": "{date}",
  "topic": "{topic}",
  "headline": "Punchy headline (max 12 words). Specific, no clickbait.",
  "hook": "2-3 sentences. Lead with a number or bold claim from the research. Urgent, not hype-y.",
  "key_insights": [
    {{"number": 1, "title": "5 words max", "body": "2 sentences."}},
    {{"number": 2, "title": "5 words max", "body": "2 sentences."}},
    {{"number": 3, "title": "5 words max", "body": "2 sentences."}},
    {{"number": 4, "title": "5 words max", "body": "2 sentences."}},
    {{"number": 5, "title": "5 words max", "body": "2 sentences."}}
  ],
  "deep_dive": [
    "What is happening and why now — 3-4 sentences with specifics",
    "How it works / what is driving it — 3-4 sentences",
    "What this means for you: who benefits, what to do, what to watch — 3-4 sentences"
  ],
  "money_with_ai": [
    {{"method": "Short name for this income method", "how": "Exactly how to do this — 1-2 concrete sentences, no vague advice", "effort": "Low", "earning_potential": "e.g. $200-800/month or save 4h/week"}},
    {{"method": "Second method", "how": "How to do it", "effort": "Medium", "earning_potential": "..."}},
    {{"method": "Third method", "how": "How to do it", "effort": "Low", "earning_potential": "..."}}
  ],
  "implement_today": {{
    "action": "One specific task the reader can complete today — concrete, not vague",
    "time_needed": "e.g. 15 minutes",
    "tool": "Exact tool or service name",
    "tool_url": "URL from research — must be a real homepage",
    "outcome": "What you will have built or be able to do when this is done"
  }},
  "tools_spotlight": {{
    "name": "Tool name from research",
    "emoji": "Single relevant emoji",
    "tagline": "One sentence — what it does",
    "why_it_matters": "2 sentences on practical value for readers",
    "url": "URL from research"
  }},
  "quick_bites": [
    {{"tag": "News", "title": "Short title", "summary": "One punchy sentence.", "url": "..."}},
    {{"tag": "Tool", "title": "Short title", "summary": "One punchy sentence.", "url": "..."}},
    {{"tag": "Opportunity", "title": "Short title", "summary": "One punchy sentence.", "url": "..."}},
    {{"tag": "Research", "title": "Short title", "summary": "One punchy sentence.", "url": "..."}}
  ],
  "resources": [
    {{"title": "...", "url": "...", "description": "One sentence on why to read/try this"}},
    {{"title": "...", "url": "...", "description": "One sentence on why to read/try this"}},
    {{"title": "...", "url": "...", "description": "One sentence on why to read/try this"}}
  ],
  "cta": "Ask readers to reply with how they are using this in their work or side income.",
  "subject_line": "Email subject (max 55 chars) — specific, no clickbait",
  "preview_text": "Preview text (max 90 chars) — complements the subject"
}}"""

    raw = None
    last_error = None
    for model in _content_models():
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                )
                print(f"[content] Model used: {model}")
                raw = response.choices[0].message.content.strip()
                break
            except RateLimitError as exc:
                last_error = exc
                if attempt == 2:
                    print(f"[content] Model rate-limited after retries: {model} — trying fallback model...")
                    continue
                wait = 15 * (attempt + 1)
                print(f"[content] Rate limited on {model} — retrying in {wait}s (attempt {attempt+1}/3)...")
                time.sleep(wait)
            except Exception as exc:
                last_error = exc
                print(f"[content] Model failed: {model} — {exc} — trying fallback model...")
                break
        else:
            continue
        if raw is not None:
            break
    else:
        raise RuntimeError(f"All content models failed: {_content_models()}") from last_error

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    if raw.endswith("```"):
        raw = raw[: raw.rfind("```")].strip()

    # Remove trailing commas before ] or } (common model output mistake)
    raw = re.sub(r",\s*([}\]])", r"\1", raw)

    content = json.loads(raw)
    print(f"[content] Generated newsletter copy for issue #{issue_number}")
    return content


if __name__ == "__main__":
    sample_research = {
        "topic": "Agentic AI systems",
        "headline_suggestion": "AI Agents Are Taking Over the Workflow Stack",
        "hook": "Three months ago, agentic AI was a demo. Now it's in production at 40% of Fortune 500 companies.",
        "key_insights": [
            {"insight": "Multi-agent frameworks doubled in adoption", "why_it_matters": "Signals enterprise readiness"},
        ],
        "deep_dive_points": ["Point 1", "Point 2", "Point 3"],
        "stats": [{"label": "Adoption rate", "value": "40%", "context": "Fortune 500"}],
        "tools_spotlight": {"name": "AutoGen 2.0", "tagline": "Multi-agent framework", "why_it_matters": "...", "url": "https://microsoft.github.io/autogen/"},
        "quick_bites": [],
        "resources": [],
        "infographic_prompt": "A futuristic network of AI agents collaborating",
        "cta": "Reply with how you're using AI agents in your workflow.",
    }
    result = generate_content(sample_research, issue_number=1)
    print(json.dumps(result, indent=2))
