# How I Built a Self-Running AI Newsletter for Free

**Cross-post to:** Dev.to, Hashnode, Medium, your own Beehiiv as a special edition
**Reading time:** ~6 minutes
**Cover image:** Use the AI illustration from one of your newsletter editions

---

I haven't read an AI newsletter myself in three weeks.

I built one to do it for me. Every morning at 11 AM Riga time, a GitHub Actions runner spins up, researches the day's most important AI developments, writes a fully-formatted briefing, generates a custom illustration, and emails it to my inbox.

The whole thing costs $0.00 to run.

This is a walkthrough of what I built, why I built it that way, and what I learned along the way. The full code is open-source: [github.com/Siyaslwf/ai-morning-briefing](https://github.com/Siyaslwf/ai-morning-briefing)

---

## The problem

The AI space moves faster than any human can track. Every newsletter I subscribed to was either:
- Too dense (a 30-minute read I never finished)
- Too hype-y (every announcement framed as "the future of work")
- Or just abandoned after their initial enthusiasm wore off

I wanted something opinionated, current, and short. So I built it.

---

## The architecture: WAT (Workflows, Agents, Tools)

The biggest mistake I made on my first attempt: I tried to do everything with one giant LLM call. "Hey Gemini, research today's AI news AND write a newsletter AND format it AND send it." The output was inconsistent across runs, and when something broke, I had no idea where.

The fix was splitting the system into three layers:

```
Layer 1 — Workflows (markdown)
    Plain-language SOPs describing the goal of each step.

Layer 2 — Agents (the AI)
    Reads the workflow, decides what to do, coordinates the tools.

Layer 3 — Tools (Python scripts)
    Deterministic execution. Each script does ONE thing predictably.
```

This pattern matters because **end-to-end AI is fragile**. If each step is 90% accurate, you're at 59% reliability after just 5 steps. Wrapping the AI's decisions in deterministic Python execution drops the error rate dramatically.

---

## The pipeline

The orchestrator (`run_newsletter.py`) sequences five tools:

### 1. Research (`research_topic.py`)
Calls Gemini 2.0 Flash with Google Search grounding enabled. The model fetches today's actual news, not its training data. Returns a structured JSON with insights, tools to spotlight, statistics, and source URLs.

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=research_prompt,
    config={"tools": [{"google_search": {}}]}
)
```

Free tier: 1,500 requests/day. I use ~30/month.

### 2. Writing (`generate_content.py`)
Takes the research output and writes the newsletter copy. A separate prompt with a strict system message defining tone: "smart, direct, human. Never hype-y. Never corporate."

Output is structured JSON: headline, hook, five insight cards, three deep-dive paragraphs, a tools spotlight, four quick bites, three resources, and email metadata (subject line, preview text).

### 3. Illustration (`generate_infographic.py`)
Calls Pollinations.ai with a prompt derived from the day's topic. No API key needed, no rate limits.

```python
url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
image_bytes = requests.get(url).content
```

The image is base64-encoded and embedded inline in the email so it works in every email client.

### 4. HTML rendering (`generate_html.py`)
Jinja2 templates rendered, then run through `premailer` to inline all CSS. This is the difference between an email that looks great in Gmail and one that breaks in Outlook 2016.

### 5. Delivery (`send_email.py`)
Standard `smtplib` against Gmail SMTP. Free up to 500 emails/day, which is generous for any newsletter under a few thousand subscribers.

---

## What surprised me

### Free tier APIs are extraordinarily capable now
The free tier of Gemini 2.0 Flash, paired with Google Search grounding, beats most paid models without grounding for "what's happening right now" questions. I tried this with GPT-4 (no grounding) and Claude (no grounding) — neither came close on freshness.

### Pollinations.ai changed how I think about image generation
No API key. No rate limits. No payment. The images aren't DALL-E quality, but for a newsletter cover image, they're more than enough — and the price (free, unlimited) is unbeatable.

### GitHub Actions is the most underrated infrastructure
2,000 free minutes per month. Cron scheduling. Built-in secrets management. Automatic logs. For any project that needs to "run X every Y" — start here before you spin up an EC2 instance.

### The Mom Test was right
After two weeks of running this for myself, I sent it to three friends to ask "would you subscribe?" The first one said "yes definitely!" That meant nothing. The second forwarded it to a colleague — that meant everything.

---

## What I'd do differently

1. **I'd add topic curation.** Right now I pass the topic as an argument. The next version should auto-suggest topics by scanning RSS feeds and trending GitHub repos.

2. **I'd add archive search.** A subscriber asking "what did you say about agents last month?" can't find it. A simple Beehiiv-hosted archive solves this.

3. **I'd ship faster.** I spent 3 days polishing the HTML template before showing anyone. The first version of anything you build is the version that should ship.

---

## What's next

I'm open-sourcing this so anyone can fork it and run their own version — daily competitor monitoring, industry-specific briefings, custom team digests. The full code is at:

🔗 [github.com/Siyaslwf/ai-morning-briefing](https://github.com/Siyaslwf/ai-morning-briefing)

If you want to subscribe to mine instead of running your own:
🔗 [your-beehiiv-url]

And if you're a company that wants a custom version (internal team digest, competitive intelligence, market intel), I build those for a flat fee — reply to this post or DM me.

---

## TL;DR

- AI newsletter that writes itself, running on free APIs
- Architecture: deterministic Python + AI reasoning, not end-to-end AI
- Cost: $0.00 per edition
- Time to build: ~3 days
- Repo: github.com/Siyaslwf/ai-morning-briefing (MIT licensed)

Hit reply with questions, criticisms, or ideas for what to automate next.

— Siyas
