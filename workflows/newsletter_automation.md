# Workflow: Newsletter Automation

## Objective
Produce and deliver a fully-researched, beautifully designed AI/tech newsletter edition from a single topic input.

## Inputs Required
| Input | Where | Notes |
|-------|-------|-------|
| `--topic` | CLI arg | Required. The theme for this issue. |
| `GEMINI_API_KEY` | `.env` | Google Gemini API key (free at aistudio.google.com) |
| `GMAIL_ADDRESS` | `.env` | Sender email (siyasmohammedd@gmail.com) |
| `GMAIL_APP_PASSWORD` | `.env` | Gmail App Password (not your account password) |
| `NEWSLETTER_RECIPIENTS` | `.env` | Comma-separated recipient emails |
| `NEWSLETTER_ISSUE_NUMBER` | `.env` | Auto-increments after each successful send |

## How to Run

### Standard send
```bash
python run_newsletter.py --topic "OpenAI o3 and reasoning models"
```

### Preview only (no email sent)
```bash
python run_newsletter.py --topic "OpenAI o3 and reasoning models" --dry-run
```

### Send to specific recipients (overrides .env)
```bash
python run_newsletter.py --topic "AI agents in enterprise" --recipients "you@example.com,editor@example.com"
```

### Override issue number
```bash
python run_newsletter.py --topic "Google Gemini 2.5" --issue 12
```

## Pipeline Steps

```
Step 1: research_topic.py      → Gemini 2.0 Flash + Google Search grounding (real-time web)
Step 2: generate_content.py    → Gemini 2.0 Flash (newsletter copywriting)
Step 3: generate_infographic.py → Pollinations.ai (free AI image) + matplotlib (stat chart)
Step 4: generate_html.py        → Jinja2 + premailer CSS inlining
Step 5: send_email.py           → Gmail SMTP with HTML + plain text
```

Each step saves intermediate output to `.tmp/` for inspection.

## Template Tags Reference

These placeholders are filled automatically each run:

| Tag | Source | Description |
|-----|--------|-------------|
| `issue_number` | `.env` counter | Edition number, auto-incremented |
| `date` | System | Today's date, formatted |
| `topic` | CLI arg | Newsletter theme |
| `headline` | Claude | Punchy main headline (max 12 words) |
| `hook` | Claude | 2–3 sentence opener |
| `key_insights` | Claude | 5 numbered insight cards |
| `deep_dive` | Claude | 3 analysis paragraphs |
| `tools_spotlight` | Research + Claude | Featured tool of the week |
| `quick_bites` | Research + Claude | 4 short news items with tags |
| `resources` | Research + Claude | 3 curated links |
| `cta` | Claude | Call to action |
| `subject_line` | Claude | Email subject (max 55 chars) |
| `preview_text` | Claude | Email preview (max 90 chars) |
| `illustration_b64` | Pollinations.ai | Inline AI-generated image |
| `chart_b64` | matplotlib | Inline stat chart (if stats exist) |

## Topic Selection Guidelines

**Good topics (specific, timely):**
- "OpenAI's o3 reasoning model and what it means for benchmarks"
- "Anthropic's computer use feature in production"
- "The state of open-source LLMs in 2026"
- "AI agent frameworks: AutoGen vs LangGraph vs CrewAI"
- "Multimodal AI: where vision models are heading"

**Avoid (too broad):**
- "AI" (too vague — Perplexity won't return focused results)
- "Technology" (no angle)

**Format tip:** Add a year or quarter for more current results:
- "AI coding assistants Q2 2026"
- "LLM inference optimization 2026"

## Customizing the Newsletter

### Add or remove sections
Edit `templates/newsletter.html.j2`. Sections are clearly commented. Add a new section between any two existing ones using the same table-based pattern.

### Change the color scheme
Edit the color variables at the top of `templates/newsletter.html.j2`:
```
#0f172a  → dark background (header)
#6366f1  → accent (indigo/purple)
#f8fafc  → body background
#ffffff  → card background
#1e293b  → body text
```

### Change the AI illustration style
In `tools/generate_infographic.py`, the `infographic_prompt` from research is passed to Pollinations.ai. To force a specific style, edit the fallback prompt in `generate_infographic()`.

### Change the Claude writing tone
Edit the `system` prompt in `tools/generate_content.py`. Current tone: smart, direct, human — not hype-y. Change `"never hype-y, never corporate"` to whatever fits your brand.

## Error Recovery

### "GEMINI_API_KEY not set"
→ Add your Gemini API key to `.env`. Get one free at aistudio.google.com/apikey

### "Gmail authentication failed"
→ You need an App Password, not your Gmail account password.
→ Go to: myaccount.google.com/apppasswords
→ Create a new app password for "Mail"
→ Paste it as `GMAIL_APP_PASSWORD` in `.env`
→ Make sure 2-factor authentication is enabled on your Gmail account

### "Pollinations.ai failed"
→ The AI illustration step is non-blocking. If it fails, the newsletter renders without the image.
→ Check internet connectivity. Pollinations.ai has no API key and should always be free.

### "premailer failed"
→ Install it: `pip install premailer`
→ If still failing, the HTML will render without CSS inlining (looks fine in modern email clients, may degrade in Outlook)

### Research returns generic or outdated information
→ Make your topic more specific and add a date/year
→ Check your Perplexity API key has credits: perplexity.ai/settings/api

## Rate Limits & Costs

| Service | Free Limit | Cost |
|---------|-----------|------|
| Gemini 2.0 Flash | 1,500 req/day, 15 RPM | **Free** |
| Pollinations.ai | Unlimited | **Free** |
| Gmail SMTP | 500 emails/day | **Free** |

**Estimated cost per newsletter edition: $0.00** — the entire pipeline is free.

## Improving the System

When you find better methods, update this workflow. Key areas for improvement:
1. **Topic curation** — Add an RSS feed scanner to auto-suggest weekly topics
2. **Subscriber management** — Add a CSV/Google Sheets subscriber list
3. **Analytics** — Add open-tracking pixel and click tracking
4. **Scheduling** — Use a cron job or Windows Task Scheduler to auto-run weekly
5. **A/B testing** — Generate two subject lines and track which performs better
