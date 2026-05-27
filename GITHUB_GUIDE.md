# GitHub Guide — AI Workflow (WAT Framework)

Everything you need to know to use this project on GitHub, from setup to daily automation.

---

## What This Project Does

This is a **WAT Framework** project that sends you a daily AI newsletter every morning. It:
- Researches the latest AI news automatically using Gemini AI
- Writes a fully formatted newsletter with insights, tools, and quick bites
- Generates an AI illustration for each edition
- Emails it to you (and anyone else you add) every day at **11:00 AM Riga time**

Once it's on GitHub, **you never have to run anything manually** — GitHub runs it for you in the cloud, for free.

---

## Part 1: GitHub Basics

### What is GitHub?
GitHub stores your code online and lets you:
- **Back up** your project safely in the cloud
- **Run automated tasks** on a schedule (called GitHub Actions)
- **Track changes** over time so you can always go back
- **Share** your project or keep it private

### Key terms you'll use
| Term | What it means |
|------|---------------|
| **Repository (repo)** | Your project's home on GitHub — like a folder in the cloud |
| **Commit** | A saved snapshot of your code at a point in time |
| **Push** | Uploading your local commits to GitHub |
| **Pull** | Downloading changes from GitHub to your computer |
| **Branch** | A separate version of your code (you'll mostly use `main`) |
| **GitHub Actions** | Automated workflows that GitHub runs for you — this is what sends your daily newsletter |
| **Secrets** | Encrypted variables GitHub uses to store your API keys safely |
| **Workflow** | A `.yml` file in `.github/workflows/` that defines what GitHub Actions does |

---

## Part 2: First-Time Setup on GitHub

### Step 1 — Create the repository

1. Go to [github.com](https://github.com) and sign in as **Siyaslwf**
2. Click the **+** button (top right) → **New repository**
3. Fill in:
   - **Repository name:** `ai-morning-briefing`
   - **Description:** `Daily AI newsletter automation using the WAT framework`
   - **Visibility:** Private (recommended — keeps your API keys workflow private)
   - **Do NOT** check "Add a README" or any other files (your local project already has everything)
4. Click **Create repository**
5. GitHub will show you a page with setup commands — copy the repo URL, it looks like:
   ```
   https://github.com/Siyaslwf/ai-morning-briefing.git
   ```

### Step 2 — Push your local project to GitHub

Open a terminal (PowerShell or Command Prompt) in your project folder and run:

```powershell
# Navigate to the project folder
cd "C:\Users\moham\OneDrive - Rīgas Tehniskā Universitāte\Desktop\AI Workflow start"

# Connect your local project to GitHub
git remote add origin https://github.com/Siyaslwf/ai-morning-briefing.git

# Push everything to GitHub
git push -u origin main
```

GitHub will ask for your username and password. For the password, use a **Personal Access Token** (not your GitHub password):
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Name it `ai-workflow`, check `repo` scope, click **Generate token**
4. Copy the token and use it as your password when prompted

### Step 3 — Add your secrets (API keys)

GitHub Actions needs your API keys to run the newsletter. These are stored as encrypted **Secrets** — GitHub never shows them in plain text.

1. Go to your repo: `https://github.com/Siyaslwf/ai-morning-briefing`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of these:

| Secret Name | Where to get it | Example value |
|-------------|----------------|---------------|
| `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | `AIza...` |
| `GMAIL_ADDRESS` | Your Gmail address | `siyasmohammedd@gmail.com` |
| `GMAIL_APP_PASSWORD` | [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) | `xxxx xxxx xxxx xxxx` |
| `NEWSLETTER_RECIPIENTS` | Who receives the newsletter | `siyasmohammedd@gmail.com` |
| `NEWSLETTER_ISSUE_NUMBER` | Starting issue number | `1` |

> **Note on Gmail App Password:** Go to your Google Account → Security → 2-Step Verification must be ON → then go to App Passwords, create one for "Mail". Use that 16-character code, not your Gmail password.

---

## Part 3: How the Daily Automation Works

The file [.github/workflows/daily_newsletter.yml](.github/workflows/daily_newsletter.yml) tells GitHub what to do automatically.

### Schedule
```
Every day at 08:00 UTC = 11:00 AM Riga time (EET/EEST)
```

### What happens automatically each morning:
1. GitHub starts a virtual Linux computer (free, takes ~30 seconds)
2. It downloads your project code
3. Installs Python and all dependencies
4. Builds your `.env` file from your Secrets
5. Runs `python run_newsletter.py --topic "Latest AI developments and tools this week"`
6. Sends the newsletter to your email
7. Saves the HTML preview as a downloadable artifact for 7 days

### To change the daily topic
Edit [.github/workflows/daily_newsletter.yml](.github/workflows/daily_newsletter.yml), line 37:
```yaml
run: python run_newsletter.py --topic "YOUR NEW TOPIC HERE"
```
Then commit and push the change.

### To trigger it manually (without waiting for 11 AM)
1. Go to your repo on GitHub
2. Click **Actions** tab
3. Click **Daily AI Newsletter** on the left
4. Click **Run workflow** → **Run workflow**
5. Check your email in ~2 minutes

### To view past newsletter runs
1. Go to **Actions** tab in your repo
2. Click any past run
3. Scroll to **Artifacts** at the bottom
4. Download `newsletter-preview` to see the HTML

---

## Part 4: Day-to-Day Usage

### Checking if today's newsletter ran
- Go to **Actions** tab → green checkmark = success, red X = something failed

### If the newsletter fails
1. Click the failed run in **Actions**
2. Click **send-newsletter** job
3. Read the error log — it usually says exactly what went wrong
4. Common fixes:
   - `GEMINI_API_KEY not set` → re-add the secret in Settings
   - `Gmail authentication failed` → re-generate your App Password
   - `Rate limit` → Gemini API hit daily limit, runs fine tomorrow

### Changing who receives the newsletter
Update the `NEWSLETTER_RECIPIENTS` secret in **Settings → Secrets**. Separate multiple emails with commas:
```
siyasmohammedd@gmail.com,friend@example.com
```

### Updating the code (adding a new feature, fixing something)
```powershell
# After making changes locally:
git add .
git commit -m "describe what you changed"
git push
```
GitHub automatically uses your updated code in the next run.

### Pulling changes (if you edit on GitHub's website)
```powershell
git pull
```

---

## Part 5: Project File Structure

```
ai-morning-briefing/
│
├── .github/
│   └── workflows/
│       └── daily_newsletter.yml   ← GitHub Actions schedule (runs daily)
│
├── tools/                         ← Python scripts that do the actual work
│   ├── research_topic.py          ← Step 1: Fetches AI news via Gemini + Google Search
│   ├── generate_content.py        ← Step 2: Writes the newsletter copy
│   ├── generate_infographic.py    ← Step 3: Creates AI illustration
│   ├── generate_html.py           ← Step 4: Builds the HTML email
│   └── send_email.py              ← Step 5: Sends via Gmail SMTP
│
├── workflows/
│   └── newsletter_automation.md   ← Instructions for the AI agent (Claude)
│
├── templates/
│   └── newsletter.html.j2         ← Newsletter visual design (edit colors here)
│
├── CLAUDE.md                      ← Instructions for Claude Code AI assistant
├── GITHUB_GUIDE.md                ← This file
├── run_newsletter.py              ← Main entry point
├── requirements.txt               ← Python packages needed
├── .gitignore                     ← Files NOT uploaded to GitHub (secrets, temp files)
└── .env                           ← Your API keys (NEVER uploaded — gitignored)
```

---

## Part 6: Keeping Your Secrets Safe

The `.gitignore` file ensures these **never** get uploaded to GitHub:
- `.env` (your API keys)
- `credentials.json` / `token.json` (Google OAuth)
- `.tmp/` (temporary newsletter files)

**Never** paste API keys directly into `.yml` files or Python files. Always use GitHub Secrets (Settings → Secrets) for anything that runs in GitHub Actions, and `.env` for local runs.

---

## Part 7: Quick Reference Commands

```powershell
# See what files changed locally
git status

# Save your changes with a message
git add .
git commit -m "your message here"

# Upload to GitHub
git push

# Download latest from GitHub
git pull

# See history of all changes
git log --oneline

# Run the newsletter right now (locally)
python run_newsletter.py --topic "AI agents update May 2026"

# Preview without sending email
python run_newsletter.py --topic "AI agents update" --dry-run
```

---

## Part 8: Changing the Newsletter Topic Over Time

The current GitHub Actions workflow sends the same generic topic every day. To make it smarter, you can edit the workflow to rotate topics. For example:

```yaml
# In daily_newsletter.yml, replace the static topic with a dynamic one:
- name: Run newsletter
  run: |
    TOPICS=("AI agent frameworks 2026" "OpenAI vs Anthropic latest" "LLM inference optimization" "Multimodal AI June 2026" "AI coding tools roundup" "Open source LLMs June 2026" "AI safety and alignment news")
    DAY=$(date +%u)  # 1=Monday through 7=Sunday
    TOPIC=${TOPICS[$((DAY - 1))]}
    python run_newsletter.py --topic "$TOPIC"
```

---

## Summary: What to Do Right Now

1. ✅ Create the repo on GitHub (see Part 2, Step 1)
2. ✅ Push this code (see Part 2, Step 2)
3. ✅ Add your 5 secrets (see Part 2, Step 3)
4. ✅ Trigger a manual run to test it (see Part 3)
5. ✅ After that — do nothing. It runs itself every morning at 11 AM.
