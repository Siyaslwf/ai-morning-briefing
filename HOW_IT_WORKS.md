# How The AI Briefing Works

A plain-English walkthrough of what this project does, end to end.
Written so anyone — even someone who has never written Python — can follow along.

---

## The 30-second version

Every morning at 11:00 AM Riga time, a robot wakes up on a free server, asks an AI to research the latest AI news, asks another AI to turn that research into a polished newsletter, generates a picture for it, and emails it to you. You do nothing. It costs $0.

That's it. The rest of this document just explains *how* each of those steps actually works.

---

## The big picture

Think of the project like a tiny factory with five workstations on a conveyor belt:

```
[ 1. Research ] -> [ 2. Write ] -> [ 3. Illustrate ] -> [ 4. Format ] -> [ 5. Send ]
```

A "manager" script (called `run_newsletter.py`) walks down the conveyor, hands the work to each station in order, and yells if anything goes wrong.

Each workstation is a separate Python file in the `tools/` folder. They're separate on purpose — if one breaks, the others still work, and you can swap one out (e.g. replace the email-sender with a different one) without touching the rest.

---

## The cast of characters

Before we walk through the steps, here are the names you'll see:

| Name | What it is |
|---|---|
| **Python** | A programming language. It runs the scripts. |
| **OpenRouter** | A website that gives you access to dozens of different AI models through one API. We use only their *free* models. |
| **Pollinations.ai** | A free website that turns text descriptions into pictures. |
| **Gmail SMTP** | The plumbing behind Gmail that lets a script send email like a regular human. |
| **GitHub** | A website where code lives. It also has a feature called "Actions" that can run your code on a schedule, for free. |
| **GitHub Actions** | The "cron job in the cloud" that wakes up every morning and runs the project. You don't have to leave your laptop on. |
| **`.env` file** | A small text file holding passwords and API keys. Never goes on GitHub. |
| **HTML** | The language email and webpages are written in. |

If any of these are new, don't worry — you don't need to fully understand them. Just know they're tools, like a microwave or a stapler.

---

## Walking through one morning

Let's follow a single newsletter from "robot wakes up" to "email lands in your inbox."

### Step 0 — The alarm clock (GitHub Actions)

A file called `.github/workflows/daily_newsletter.yml` is GitHub's instruction sheet. It says:

> "Every day at 08:00 UTC, rent a fresh Ubuntu computer for 15 minutes, copy the project onto it, install Python, set up the secret passwords, and run `python run_newsletter.py`."

That's the whole job. 08:00 UTC is 11:00 in Riga because of the time-zone offset.

The "fresh Ubuntu computer" part is the magic. GitHub gives every project free use of a cloud server, but only for short bursts. We only need 5 minutes per day, well inside their free limit.

### Step 1 — Research the news

The first workstation is `tools/research_topic.py`.

It sends a long message to an AI model that says, in essence:

> "You're a senior AI journalist. Research the latest AI developments. Return your answer as a structured JSON object with these exact fields: a headline, a hook, five key insights, three deep-dive points, three ways to make money with this AI, three stats, four quick news bites, three recommended resources, and a prompt for an image generator. Use only real URLs from trusted domains."

The AI thinks for ~1-3 minutes and replies with a single big JSON document — basically a filled-in form. We save that file to `.tmp/research_*.json` so we can read it later if anything weird happens.

**Why JSON?** A newsletter has many sections. If we asked the AI for free-form text, we'd have to guess where each section ends. JSON gives every section a labeled box, so the next station can pick them up cleanly.

**Why free models?** Quality has caught up. The free model we use first (`nvidia/nemotron-3-super-120b`) is enormous, and free for everyone. The trade-off is that it's *shared* — sometimes thousands of people hit it at once and it returns a "rate-limited, try again" error. We handle that with a backup plan (see "What happens when something breaks?" below).

### Step 1.5 — Sanity-check the URLs

The AI is good but not perfect — sometimes it makes up URLs that don't actually exist. So before we trust its research, `tools/validate_links.py` quietly checks every URL the AI gave us. If a link is broken, it gets replaced with just the homepage (e.g. `https://openai.com/blog/article-that-does-not-exist` becomes `https://openai.com`).

All URLs are checked at the same time in parallel — like one person doing 20 phone calls simultaneously instead of one after another. Saves ~3 minutes.

### Step 2 — Write the newsletter

The second workstation is `tools/generate_content.py`.

It takes the research JSON from Step 1, hands it to an AI again with a different prompt:

> "You're a newsletter writer. Using the research below, write the final newsletter copy: a punchy headline, a 2-sentence hook, five short numbered insights, a three-paragraph deep dive, three concrete money-making methods, a tool spotlight, four quick bites, three resources, a call-to-action, and a subject line under 55 characters. Tone: smart, direct, zero hype."

The AI takes another ~1-2 minutes and returns a *second* JSON — this one is the finished writing, ready to drop into an email template. We save it but it's used immediately.

### Step 3 — Make the picture

`tools/generate_infographic.py` does two things:

1. **An AI illustration.** It takes the "infographic_prompt" from Step 1 (something like *"a glowing network of AI agents collaborating, purple and indigo tones, cinematic"*) and sends it to Pollinations.ai. Pollinations replies with a real PNG image. We convert that PNG to a long text string called "base64" — that's the standard trick for embedding pictures directly inside an email so the reader doesn't have to download anything.

2. **A bar chart.** If the research has numeric stats (e.g. "Adoption: 40%", "Growth: 3x"), it uses matplotlib (a Python charting library) to draw a clean bar chart. Same base64 trick to embed it in the email.

If either of those fails — and they sometimes do, since Pollinations is a free service — the newsletter just goes out without the picture. The other steps don't care.

### Step 4 — Build the email

`tools/generate_html.py` takes a pre-made template (`templates/newsletter.html.j2`) — basically an HTML skeleton with `{{ placeholders }}` everywhere — and fills in the blanks from Step 2's writing and Step 3's pictures.

Then it runs a tool called **premailer** which copies all the styling rules from `<style>` blocks down into each individual element (`<p style="color: #fff">…`). This sounds boring but it matters: email clients like Outlook and Gmail strip out shared style blocks, so the only styling that survives is the kind glued directly onto each element. Premailer does that automatic gluing.

The result is one big HTML file, ~100KB, with pictures embedded. We save it to `.tmp/newsletter_*.html` so you can open it in a browser to preview before it goes out.

### Step 5 — Send the email

`tools/send_email.py` opens a connection to Gmail's SMTP server (`smtp.gmail.com:587`), logs in with the email address and an *App Password* (a special one-purpose password Google gives you for scripts), and hands the HTML over for delivery.

We also build a plain-text fallback version of the newsletter (just text, no styling) so that if the recipient's email client can't show HTML, they still see something readable.

If Gmail says "yes, sent," we're done. If it says "no" with a transient error (network blip, temporarily busy), we wait a few seconds and try up to 3 times. Real auth errors (wrong password) don't get retried because retrying won't help.

### Step 6 — Bookkeeping

Once the email is out the door:

- The current issue number (`NEWSLETTER_ISSUE_NUMBER` in `.env`) is bumped by 1, so tomorrow's newsletter is automatically "Issue #N+1."
- The HTML preview gets uploaded to GitHub as an "artifact" — a file you can download from the Actions page later for the next 7 days.

Total time, end to end: about 5 minutes.

---

## What happens when something breaks?

Robots fail. Free APIs go down. The internet has bad days. Here's how the project handles trouble:

### Problem: The AI model is too busy (rate limited)

OpenRouter's free models are shared across all OpenRouter users worldwide. Sometimes they return "429 — too many requests" errors.

**The fix:** `tools/llm_client.py` doesn't just call one model — it tries a *chain* of free models. If model A says "busy," it instantly moves on to model B, then C, then D. Each fallback is a different vendor (NVIDIA, OpenAI's open-source models, DeepSeek), so it's very unlikely they're all rate-limited at the same time. Only after all of them fail does the script wait and retry.

### Problem: The AI returns malformed JSON

Sometimes models add a stray comma or wrap their output in code fences (` ``` `). The client strips fences and removes trailing commas before parsing. If parsing still fails, it moves to the next model.

### Problem: A URL the AI mentioned is dead

Already handled in Step 1.5 — broken URLs are replaced with the site's homepage.

### Problem: The image generator is down

The newsletter ships without the illustration. Text-only is still a complete newsletter.

### Problem: Gmail is temporarily unreachable

Up to 3 retries with a few seconds between each.

### Problem: A required password is missing from `.env`

The script checks all secrets are present *before* doing any slow work, and exits in under a second with a clear message listing exactly what's missing. No more "3-minute crash with a cryptic error."

### Problem: One URL takes forever to load

The link-validation step has a hard 60-second total cap. If it can't finish in time, it gives up gracefully and ships URLs as the AI provided them, instead of blocking the whole newsletter.

### Problem: Something else nobody anticipated

The "Run newsletter" step in the workflow has stack traces enabled, and the partial HTML/research files get uploaded as artifacts even on failure. So whoever debugs it the next morning can see exactly where things went wrong.

---

## The folder map

Here's what every file and folder in the project is for. Skim this when you're trying to figure out "where does X live?"

```
.
├── .github/workflows/
│   └── daily_newsletter.yml   The morning alarm clock (GitHub Actions schedule)
│
├── tools/                     Each file = one workstation on the factory line
│   ├── llm_client.py            Shared helper: try AI model A, then B, then C
│   ├── research_topic.py        Step 1: ask AI for structured research
│   ├── validate_links.py        Step 1.5: check every URL is alive
│   ├── generate_content.py      Step 2: ask AI to write the newsletter
│   ├── generate_infographic.py  Step 3: AI picture + stat chart
│   ├── generate_html.py         Step 4: fill in the HTML template
│   ├── send_email.py            Step 5: send via Gmail
│   └── beehiiv_publish.py       Optional Step 6: also publish to Beehiiv
│
├── workflows/                 Plain-English "how to do X" docs (SOPs)
│   └── newsletter_automation.md
│
├── templates/
│   └── newsletter.html.j2     The email skeleton with {{ placeholders }}
│
├── .tmp/                      Scratch space — research JSONs, HTML previews.
│                              Regenerated every run. Safe to delete.
│
├── landing/                   The public marketing page (optional, for subscribers)
├── marketing/                 Pre-written launch posts, cold emails, etc.
│
├── run_newsletter.py          The manager script. Runs steps 1-5 in order.
├── requirements.txt           List of Python libraries this project needs
├── .env                       Your passwords. NEVER goes on GitHub.
├── CLAUDE.md                  Instructions for the AI agent that helps maintain this
├── README.md                  Short overview for visitors landing on the repo
└── HOW_IT_WORKS.md            (you are here)
```

---

## How to change things

You don't need to be a Python expert. Most useful changes are one-line edits.

| What you want to change | File to open | What to look for |
|---|---|---|
| **The daily topic** | `.github/workflows/daily_newsletter.yml` | Line that says `--topic "..."` |
| **The send time** | same file | `cron: '0 8 * * *'` (the `8` is hours UTC) |
| **The recipient email** | GitHub Settings -> Secrets | Edit `NEWSLETTER_RECIPIENTS` |
| **The writing tone** | `tools/generate_content.py` | Look for `system_instruction = (...)` |
| **The picture style** | `tools/generate_infographic.py` | The fallback prompt at the bottom |
| **The newsletter colors** | `templates/newsletter.html.j2` | Top of the file, `:root` CSS variables |
| **Add or remove a section** | `templates/newsletter.html.j2` | Each section is clearly commented |

---

## Why the project is structured the way it is

You'll see lots of folders and files. There's a reason for the layout. It's called the **WAT framework** (Workflows, Agents, Tools):

- **Workflows** are plain-English instructions, like a recipe card. They live in `workflows/` and `.github/workflows/`.
- **Agents** are the smart parts that read the workflow and decide what to do. The orchestrator `run_newsletter.py` is one; the AI models are another.
- **Tools** are the deterministic doers. Each `tools/*.py` file does one job and only one job. If anything goes wrong, you know exactly which file to look at.

The reason matters: when AI tries to do *everything* itself, accuracy drops fast. By offloading the predictable parts (sending email, checking URLs, formatting HTML) to plain Python code, the AI only has to handle the parts that genuinely need judgment (researching, writing). Five 90%-reliable AI steps in a row gives you a ~59% chance of success. Two AI steps wrapped in deterministic Python gives you ~98%.

---

## Costs

Truly nothing. Here's the breakdown:

| What | Provider | Free limit | What we use |
|---|---|---|---|
| AI research + writing | OpenRouter (free models) | Unlimited if you tolerate rate limits | ~2 calls/day |
| AI illustration | Pollinations.ai | Unlimited | ~1 image/day |
| Email delivery | Gmail SMTP | 500 emails/day | ~1-50 emails/day |
| Scheduled compute | GitHub Actions | 2,000 minutes/month for private repos, **unlimited for public** | ~5 min/day = ~150 min/month |

You will not get a bill. The biggest "cost" is the 5 minutes of cloud server time per day, which is free on a public repo.

---

## Glossary (in case you hit jargon)

- **API**: A way for two pieces of software to talk to each other. When we "call the OpenRouter API," we're sending OpenRouter a request and getting an answer back.
- **API key**: A long password that proves a script has permission to use an API. Lives in `.env`. Treat it like a credit card.
- **JSON**: A way to write structured data in plain text. Like a filled-in form. The format AI models return when we tell them to.
- **HTML**: The language webpages and emails are written in. `<p>Hello</p>` is HTML for "a paragraph that says Hello."
- **SMTP**: The protocol email uses behind the scenes to actually move from sender to recipient.
- **App Password**: A separate password Google gives you specifically for letting scripts send mail through your Gmail account. Different from your normal login password — and revocable any time.
- **Rate limit**: "You've asked too many times — slow down." Returned by APIs that are being overwhelmed.
- **Fallback**: A backup plan. "If A fails, try B. If B fails, try C."
- **`.env` file**: A small text file holding secret passwords. Never gets uploaded to GitHub.
- **Commit / push**: To save a snapshot of your code (commit) and upload that snapshot to GitHub (push).
- **GitHub Actions**: GitHub's built-in way to run code on a schedule, like a cron job in the cloud.
- **Cron schedule**: A 5-number code that says "when to run." `0 8 * * *` = "at minute 0 of hour 8, every day."
- **base64**: A way to turn a picture (or any binary file) into a long string of letters and numbers, so it can be embedded directly inside an email or webpage.
- **Premailer**: A small Python library that "bakes in" CSS styling so email clients can't strip it.

---

## TL;DR for someone who learns by reading code

1. `python run_newsletter.py --topic "..."` is the entry point.
2. It calls 5 functions in order: `research_topic`, `validate_links`, `generate_content`, `generate_infographic`, `generate_html`, then `send_email`.
3. Each function returns a Python dictionary (or raises). The next function uses the previous output as input.
4. Failures at any step print a clear error and exit, so GitHub Actions shows red and you know to look.
5. Everything that talks to a free API has a fallback, a retry, or a timeout — so transient internet weather can't permanently sink the morning send.

That's the whole project. No magic, no hidden services, no monthly bills.
