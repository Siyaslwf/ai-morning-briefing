<div align="center">

# AI Morning Briefing

**A self-running AI newsletter that lands in your inbox every morning.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![GitHub Actions](https://img.shields.io/badge/Automated-GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/Siyaslwf/ai-morning-briefing/actions)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Cost](https://img.shields.io/badge/Cost-$0.00-brightgreen?style=flat-square)](#costs)

*Researches, writes, illustrates, and delivers a full AI newsletter — automatically, every day, for free.*

</div>

---

## What It Does

Every morning at **11:00 AM (Riga / EET)**, this project:

1. Searches the web for the latest AI developments using **Gemini 2.0 Flash + Google Search grounding**
2. Writes a full newsletter with insights, deep dives, tool spotlights, and quick bites
3. Generates a unique AI illustration for each edition
4. Renders a polished HTML email
5. Delivers it straight to your inbox

No manual work. No subscriptions. No cost.

---

## Pipeline

```
research_topic.py      →  Real-time web research via Gemini + Google Search
generate_content.py    →  Newsletter copywriting (smart, direct, human tone)
generate_infographic.py →  AI illustration via Pollinations.ai (free, unlimited)
generate_html.py        →  HTML email rendering via Jinja2 + CSS inlining
send_email.py           →  Delivery via Gmail SMTP
```

Each step saves output to `.tmp/` for local inspection.

---

## Stack

| Layer | Technology | Cost |
|-------|-----------|------|
| Research | Gemini 2.0 Flash + Google Search grounding | Free (1,500 req/day) |
| Writing | Gemini 2.0 Flash | Free |
| Illustration | Pollinations.ai | Free, unlimited |
| Email delivery | Gmail SMTP | Free (500/day) |
| Automation | GitHub Actions | Free |

**Total cost per edition: $0.00**

---

## Architecture — WAT Framework

This project follows the **WAT pattern** (Workflows → Agents → Tools):

```
workflows/        ← Plain-language SOPs: what to do and how
tools/            ← Python scripts: deterministic execution
.github/workflows ← GitHub Actions: scheduled automation
```

The AI handles reasoning and orchestration. Python scripts handle execution. The separation keeps the system reliable — if one step fails, it fails loudly and predictably.

---

## Quick Start

### Prerequisites
- Python 3.11+
- A Gmail account with [App Password enabled](https://myaccount.google.com/apppasswords)
- A free [Gemini API key](https://aistudio.google.com/apikey)

### Install

```bash
git clone https://github.com/Siyaslwf/ai-morning-briefing.git
cd ai-morning-briefing
pip install -r requirements.txt
```

### Configure

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_gemini_or_openrouter_key
GMAIL_ADDRESS=you@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
NEWSLETTER_RECIPIENTS=you@gmail.com
NEWSLETTER_ISSUE_NUMBER=1
OPENROUTER_RESEARCH_MODELS=deepseek/deepseek-v4-flash:free,openrouter/auto,google/gemini-2.5-flash
OPENROUTER_CONTENT_MODELS=deepseek/deepseek-v4-flash:free,openrouter/auto,google/gemini-2.5-flash
```

### Run

```bash
# Send today's newsletter
python run_newsletter.py --topic "AI agents and autonomous systems 2026"

# Preview without sending email
python run_newsletter.py --topic "OpenAI o3 reasoning models" --dry-run
```

---

## Automated Daily Delivery (GitHub Actions)

Fork this repo and add your keys as [GitHub Secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions):

| Secret | Description |
|--------|-------------|
| `OPENROUTER_API_KEY` | Gemini / OpenRouter API key |
| `GMAIL_ADDRESS` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Gmail App Password (not your account password) |
| `NEWSLETTER_RECIPIENTS` | Comma-separated recipient emails |
| `NEWSLETTER_ISSUE_NUMBER` | Starting issue number |
| `OPENROUTER_RESEARCH_MODELS` | Optional comma-separated model fallbacks for research step |
| `OPENROUTER_CONTENT_MODELS` | Optional comma-separated model fallbacks for content step |

Once set, the newsletter runs automatically every day. To trigger manually: **Actions → Daily AI Newsletter → Run workflow**.

To change the daily topic, edit line 37 of [`.github/workflows/daily_newsletter.yml`](.github/workflows/daily_newsletter.yml).

---

## Customization

**Change the visual design** — edit color variables at the top of [`templates/newsletter.html.j2`](templates/newsletter.html.j2)

**Change the writing tone** — edit the system prompt in [`tools/generate_content.py`](tools/generate_content.py)

**Change the illustration style** — edit the fallback prompt in [`tools/generate_infographic.py`](tools/generate_infographic.py)

**Add or remove newsletter sections** — sections in the Jinja2 template are clearly commented

---

## Project Structure

```
.
├── .github/workflows/
│   └── daily_newsletter.yml   # Runs every day at 11:00 AM Riga time
├── tools/
│   ├── research_topic.py      # Step 1 — web research
│   ├── generate_content.py    # Step 2 — copywriting
│   ├── generate_infographic.py # Step 3 — AI illustration
│   ├── generate_html.py       # Step 4 — HTML rendering
│   └── send_email.py          # Step 5 — email delivery
├── workflows/
│   └── newsletter_automation.md  # Agent instructions (WAT SOP)
├── templates/
│   └── newsletter.html.j2    # Email template
├── run_newsletter.py          # Entry point
└── requirements.txt
```

---

## License

MIT — use it, fork it, build on it.
