# Reddit Posts

Reddit allergic to self-promo. The rule: give value first, link last.
Each post below is structured to start with the story/learning, end with the link.

---

## r/SideProject

**Title:** I built a daily AI newsletter that writes itself ($0 to run)

**Body:**
```
I kept feeling overwhelmed trying to keep up with AI news. Every newsletter
I subscribed to was either too dense, too hype-y, or just stopped updating.

So I built one that writes itself. Every morning at 11 AM, a GitHub Actions
runner fires off a 5-step Python pipeline:

1. Research — Gemini 2.0 Flash + Google Search grounding pulls today's
   most relevant AI developments.
2. Writing — same model writes the newsletter in a defined tone (smart,
   direct, no marketing fluff).
3. Illustration — Pollinations.ai generates a unique cover image.
4. HTML rendering — Jinja2 + premailer for emails that look good in
   every client including Outlook.
5. Delivery — Gmail SMTP to my subscriber list.

The whole thing runs on free tiers. Estimated cost per edition: $0.00.

Most interesting thing I learned building this: if you let AI handle
every step end-to-end, accuracy compounds downward. 5 steps × 90% =
59% reliable. The trick was splitting reasoning (AI) from execution
(Python) — what I'm calling the WAT pattern (Workflows, Agents, Tools).

Open-sourced under MIT:
https://github.com/Siyaslwf/ai-morning-briefing

Happy to answer questions about the architecture, the free APIs I used,
or anything else.
```

---

## r/Python

**Title:** Built a $0/run daily AI newsletter — 5-step Python pipeline with free APIs

**Body:**
```
Sharing a project I built this week. It's a Python pipeline that runs
daily via GitHub Actions and produces a fully-written AI newsletter
with no manual input.

Stack:
- google-genai (Gemini 2.0 Flash — research + writing, free tier)
- requests (Pollinations.ai for images, no API key needed)
- jinja2 + premailer (HTML email rendering with inline CSS)
- smtplib (Gmail SMTP delivery)
- python-dotenv for config

The architecture: workflows/ holds markdown SOPs that describe what to do.
tools/ holds the deterministic Python scripts. A single orchestrator
(run_newsletter.py) sequences them. Each step writes intermediate output
to .tmp/ so you can debug specific stages.

What surprised me most: structuring it as orchestration + deterministic
tools (rather than letting Gemini handle every step end-to-end) made it
dramatically more reliable. The Python scripts validate, retry, and fail
loudly. The AI just reasons.

Code: https://github.com/Siyaslwf/ai-morning-briefing

Specifically interested in feedback on the prompt engineering in
tools/generate_content.py.
```

---

## r/SaaS

**Title:** Validated a $0-cost AI newsletter pipeline — looking for honest feedback before launch

**Body:**
```
Built and ran an AI-generated daily newsletter for 2 weeks. Stack uses
only free APIs (Gemini, Pollinations, Gmail SMTP, GitHub Actions).
Operational cost per edition: $0.00.

Now considering whether to launch it as a hosted product:
- Free tier: 1 topic, 3x/week
- Pro: $5/mo, daily, custom topics
- Team: $15/mo, multi-recipient

Open source so others can self-host: github.com/Siyaslwf/ai-morning-briefing

Would love feedback from this community:
1. Is "AI does AI news" too meta to be marketable?
2. At $5/mo, what would you expect that the free tier doesn't deliver?
3. Worth building a hosted version, or is open source enough?

Genuinely undecided. Not promoting yet.
```

---

## r/learnmachinelearning

**Title:** What I learned building a 5-step AI pipeline that runs daily

**Body:**
```
Built a self-running AI newsletter system this week. Wanted to share
the architectural lessons that surprised me as someone newer to building
production AI pipelines.

1. End-to-end AI is fragile. I started with a single prompt that did
   research → writing → formatting. Output was inconsistent across runs.
   Splitting it into discrete steps with deterministic glue code fixed it.

2. Grounding with Google Search > training data. Gemini's search
   grounding made the "research" step actually current. Without it,
   the model hallucinated AI tools from 2023.

3. Prompt isolation matters. Each step has its own system prompt with
   one job. Easier to debug, easier to improve incrementally.

4. The cheap models are good enough. Gemini 2.0 Flash (free tier) handled
   research and writing better than I expected. Didn't need Opus or GPT-4.

5. Save every intermediate output. .tmp/ folder with each step's JSON
   means I can debug step 4 without re-running step 1.

Full code if anyone wants to dig in:
https://github.com/Siyaslwf/ai-morning-briefing
```

---

## When to post

- **r/SideProject:** Sunday evening (peak builder traffic)
- **r/Python:** Tuesday 9 AM ET
- **r/SaaS:** Wednesday 10 AM ET
- **r/learnmachinelearning:** Saturday morning (less moderation pressure)

**DO NOT cross-post the same day.** Space them across 4 days minimum.
