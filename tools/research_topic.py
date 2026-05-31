"""
Researches a newsletter topic via OpenRouter free models with fallback chain.
Returns structured JSON with insights, stats, sources, and tool mentions.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from tools.llm_client import chat_json

TMP_DIR = Path(__file__).parent.parent / ".tmp"


def research_topic(topic: str) -> dict:
    TMP_DIR.mkdir(exist_ok=True)

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

    research = chat_json(system_instruction, user_prompt, temperature=0.2)

    output_path = TMP_DIR / f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path.write_text(json.dumps(research, indent=2), encoding="utf-8")
    print(f"[research] Saved to .tmp/{output_path.name}")

    return research


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "Agentic AI systems in 2026"
    result = research_topic(topic)
    print(json.dumps(result, indent=2))
