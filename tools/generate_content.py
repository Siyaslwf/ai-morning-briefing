"""
Takes research JSON and produces polished newsletter copy via the shared
LLM client (free OpenRouter models with fallback chain).
"""

import json
from datetime import datetime

from tools.llm_client import chat_json


def generate_content(research: dict, issue_number: int, date: str | None = None) -> dict:
    if date is None:
        date = datetime.now().strftime("%B %d, %Y")

    topic = research.get("topic", "AI & Technology")

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

    content = chat_json(system_instruction, prompt, temperature=0.7)
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
