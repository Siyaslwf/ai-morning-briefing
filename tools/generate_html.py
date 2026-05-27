"""
Renders the Jinja2 newsletter template with content + infographic data,
inlines all CSS via premailer for email-client compatibility,
and saves the output to .tmp/.
"""

import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
TMP_DIR = Path(__file__).parent.parent / ".tmp"


def generate_html(content: dict, images: dict) -> str:
    """
    content: dict from generate_content.py
    images:  dict from generate_infographic.py  {illustration_b64, chart_b64}
    Returns: final HTML string (CSS inlined)
    """
    TMP_DIR.mkdir(exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )
    template = env.get_template("newsletter.html.j2")

    gmail_address = os.getenv("GMAIL_ADDRESS", "")

    html_raw = template.render(
        content=content,
        images=images,
        gmail_address=gmail_address,
    )

    # Inline CSS for email-client compatibility
    try:
        import premailer
        html_final = premailer.transform(html_raw, remove_classes=False, strip_important=False)
        print("[html] CSS inlined via premailer")
    except Exception as exc:
        print(f"[html] premailer failed ({exc}), using raw HTML")
        html_final = html_raw

    # Save to .tmp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_path = TMP_DIR / f"newsletter_{timestamp}.html"
    output_path.write_text(html_final, encoding="utf-8")
    print(f"[html] Saved to .tmp/{output_path.name}")

    return html_final


if __name__ == "__main__":
    # Quick test with dummy data
    sample_content = {
        "issue_number": 1,
        "date": "May 24, 2026",
        "topic": "Agentic AI Systems",
        "headline": "AI Agents Are Rewriting the Rules of Work",
        "hook": "Three months ago, agentic AI was a research demo. Today it's in production at half the Fortune 500. The shift happened faster than anyone predicted.",
        "key_insights": [
            {"number": 1, "title": "Adoption hit an inflection point", "body": "Enterprise agentic AI deployments tripled in Q1 2026. The tooling finally caught up with the ambition."},
            {"number": 2, "title": "Multi-agent beats single-agent", "body": "Benchmark after benchmark shows that networks of specialized agents outperform single large models on complex tasks."},
            {"number": 3, "title": "Memory is the moat", "body": "The companies winning in agents are the ones solving long-term memory — not just the ones with the biggest models."},
            {"number": 4, "title": "Orchestration is the new DevOps", "body": "A new role is emerging: the AI orchestration engineer. Demand is outpacing supply 10-to-1."},
            {"number": 5, "title": "Costs are collapsing", "body": "Running a capable agent 24/7 now costs less than a monthly streaming subscription. Cost is no longer the barrier."},
        ],
        "deep_dive": [
            "The shift toward agentic AI isn't just a technical upgrade — it's a fundamental rethinking of how software gets built. For decades, applications followed a simple model: user inputs, system outputs. Agents break that contract. They plan, take actions, observe results, and adapt — all without human intervention on each step.",
            "What's driving the acceleration is a confluence of factors: faster inference, cheaper compute, and a new generation of tool-calling frameworks that let agents interact with real systems. The gap between 'demo that works sometimes' and 'system you'd trust in production' has closed dramatically in the last six months.",
            "The forward-looking question isn't whether agents will be everywhere — it's which layer of the stack captures the value. Right now, the bet is on orchestration and memory. The model layer is commoditizing fast. The companies that win will be the ones that figure out how to make agents reliable, auditable, and recoverable when they fail.",
        ],
        "tools_spotlight": {
            "name": "AutoGen 2.0",
            "emoji": "🤖",
            "tagline": "Microsoft's open-source multi-agent conversation framework",
            "why_it_matters": "AutoGen 2.0 ships with a new async-first architecture and built-in human-in-the-loop controls. It's the most production-ready open-source agent framework right now.",
            "url": "https://microsoft.github.io/autogen/",
        },
        "quick_bites": [
            {"tag": "Research", "title": "OpenAI releases agent eval benchmark", "summary": "A new standardized benchmark for measuring real-world agent performance across 47 task categories.", "url": "https://openai.com"},
            {"tag": "Product", "title": "Cursor adds multi-file agent mode", "summary": "The AI code editor can now autonomously plan and execute changes across entire codebases.", "url": "https://cursor.sh"},
            {"tag": "Funding", "title": "Cognition AI raises $175M Series B", "summary": "The team behind Devin, the AI software engineer, just closed a major round at $2B valuation.", "url": "https://cognition.ai"},
            {"tag": "Open Source", "title": "LangGraph 0.3 ships with persistence", "summary": "The graph-based agent framework now has first-class state persistence and human approval steps.", "url": "https://github.com/langchain-ai/langgraph"},
        ],
        "resources": [
            {"title": "The Anatomy of an AI Agent", "url": "https://example.com/1", "description": "Best breakdown of how planning, memory, and tool-use fit together — required reading if you're building."},
            {"title": "Agent Reliability Patterns", "url": "https://example.com/2", "description": "Practical patterns for making agents fail gracefully in production — covers retries, fallbacks, and audit logs."},
            {"title": "The Coming Agent Economy", "url": "https://example.com/3", "description": "A16Z's latest on how agentic workflows will reshape white-collar work over the next 18 months."},
        ],
        "cta": "What's the most interesting agent use case you've seen or built this month? Hit reply — I feature the best ones in the next issue.",
        "subject_line": "AI agents are in production. Now what?",
        "preview_text": "The shift happened faster than anyone predicted. Here's what it means.",
    }

    sample_images = {"illustration_b64": None, "chart_b64": None}

    html = generate_html(sample_content, sample_images)
    print(f"[html] Generated {len(html):,} chars")
