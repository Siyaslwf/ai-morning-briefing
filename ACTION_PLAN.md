# The 90-Day Execution Plan
## From GitHub Repo → Audience → Income

**Owner:** Siyas Mohammed CK
**Project:** AI Morning Briefing
**Start date:** 2026-05-27
**Goal:** Convert a working AI project into a real audience, real skills proof, and real income within 90 days.

---

## How to Use This Document

- Each section has a **deadline** and a **success metric**
- Tick the boxes as you go
- If you fall behind on a date, push everything forward — don't skip steps
- The goal is not perfection. The goal is **shipping**.

---

# WEEKEND 1 — Foundation (May 30–31)

The goal of this weekend: prove the system runs, set up the platforms that will host your future audience and income.

## Saturday — Make It Bulletproof (4 hours)

### Block 1 — Validate the automation (1 hour)
- [ ] Trigger the GitHub Action manually: Repo → Actions → Daily AI Newsletter → Run workflow
- [ ] Confirm the email arrives in your inbox
- [ ] Forward it to 3 friends and ask: "Be honest — would you subscribe?"
- [ ] Note their feedback in a notebook

**Success metric:** At least 1 friend says "yes, I'd actually read this every day."

### Block 2 — Polish the newsletter content (1 hour)
- [ ] Run the newsletter with 3 different topics:
  - "AI agent frameworks in 2026"
  - "Open source LLMs this week"
  - "AI tools for productivity"
- [ ] Pick the best-looking one
- [ ] Take a high-quality screenshot in Gmail (laptop view, not mobile)
- [ ] Save it as `marketing/hero-screenshot.png`

**Success metric:** You have one screenshot you'd proudly show on LinkedIn.

### Block 3 — Set up a custom domain (1 hour)
- [ ] Buy `aimorningbriefing.com` or `morningbrief.ai` or similar on Namecheap (~$10/year)
- [ ] If those are taken, try: `dailyai.email`, `briefme.ai`, `aibrief.dev`
- [ ] Set up email forwarding so `hello@yourdomain.com` → your Gmail (free on Namecheap)

**Success metric:** You own a domain and have a professional-looking email address.

### Block 4 — Polish your GitHub presence (1 hour)
- [ ] On the repo: click ⚙️ next to "About" → add description, website URL, topics: `ai`, `newsletter`, `automation`, `gemini`, `github-actions`, `python`
- [ ] Pin the repo on your GitHub profile
- [ ] Update your GitHub bio to mention what you build
- [ ] Add the hero screenshot to the top of `README.md`

**Success metric:** Your GitHub profile tells a clear story in 5 seconds.

---

## Sunday — Set Up the Audience Platform (3 hours)

### Block 1 — Create the public newsletter (1.5 hours)
- [ ] Sign up for [Beehiiv](https://beehiiv.com) (free up to 2,500 subscribers)
- [ ] Name it: `The Morning Stack` or `AI Before Coffee` or your own pick
- [ ] Customize colors to match your GitHub README
- [ ] Connect your custom domain
- [ ] Write the welcome email — short, personal:
  > "Hey, I'm Siyas. Every morning I'll send you the most important AI news of the day. I built the system that writes this — it's open source. Reply to this email any time."

**Success metric:** You have a live subscribe page you can share.

### Block 2 — Connect your code to Beehiiv (1 hour)
- [ ] Read [Beehiiv's API docs](https://developers.beehiiv.com/docs/v2/)
- [ ] In `tools/send_email.py`, add a function `publish_to_beehiiv()` that posts your HTML to Beehiiv via their API
- [ ] Add `BEEHIIV_API_KEY` and `BEEHIIV_PUBLICATION_ID` to your `.env` and to GitHub Secrets
- [ ] Test that one edition publishes correctly

**Success metric:** A test edition appears on your public Beehiiv page.

### Block 3 — Get your first 10 subscribers (30 min)
- [ ] Send the signup link to 10 specific friends — one personal message each
- [ ] DO NOT mass-broadcast yet — you want feedback first
- [ ] Ask each one: "Tell me one thing that would make you forward this to someone else"

**Success metric:** 10 subscribers, 5+ pieces of honest feedback.

---

# WEEKEND 2 — Public Launch (June 6–7)

The goal of this weekend: maximum visibility across LinkedIn, Twitter, Reddit, and Hacker News. Build initial credibility and audience.

## Saturday — The LinkedIn Launch (3 hours)

### Block 1 — Write your launch post (1 hour)

Use this template, edit for your voice:

```
I built an AI that emails me the latest AI news every morning.
It costs $0 to run.

For the past few weeks I've been overwhelmed trying to keep up
with AI developments. So I built a system that does it for me.

Every morning at 11 AM, it:
→ Researches the latest AI news (Gemini + Google Search)
→ Writes a full newsletter with insights and analysis
→ Generates a custom AI illustration
→ Delivers it to my inbox

The whole thing runs on free tiers:
• Gemini 2.0 Flash (1,500 free requests/day)
• Pollinations.ai (free unlimited images)
• Gmail SMTP (free 500 emails/day)
• GitHub Actions (free automation)

I built it using the WAT framework — Workflows, Agents, Tools.
The AI handles reasoning; Python handles execution. That separation
is what keeps it reliable.

Open-sourced it so anyone can fork and run their own.
Link in comments.

What would you automate next?

#AI #Automation #OpenSource #Python #GeminiAPI #BuildInPublic
```

- [ ] Post on **Tuesday or Wednesday at 8:30 AM Riga time** for maximum reach
- [ ] First comment from your own account: GitHub link + Beehiiv signup link
- [ ] Reply to every single comment in the first hour (algorithm boost)

### Block 2 — Twitter/X thread (1 hour)

Same content, different format — a 6-tweet thread:

```
1/ I built an AI that emails me the latest AI news every morning.
It costs $0 to run.

Here's how it works 👇

2/ Every morning at 11 AM, GitHub Actions starts a free Linux runner
that executes a 5-step pipeline.

Total runtime: ~90 seconds.
Total cost: $0.

3/ Step 1 — Research
Gemini 2.0 Flash + Google Search grounding fetches the latest AI news.
Free: 1,500 requests/day.

4/ Step 2 — Writing
Same model writes the full newsletter in a defined tone.
Step 3 — Illustration
Pollinations.ai generates a custom image. Free, unlimited.

5/ Step 4 — HTML rendering
Jinja2 + premailer for inline CSS.
Step 5 — Delivery
Gmail SMTP. Free up to 500 emails/day.

6/ Open sourced the whole thing.
Fork it, run your own, modify it.
👉 github.com/Siyaslwf/ai-morning-briefing
```

### Block 3 — Reddit posts (1 hour)
Post to these subreddits (read each one's rules first):
- [ ] `r/SideProject` — title: "I built a free AI that emails me daily AI news"
- [ ] `r/Python` — title: "Built a $0/run daily AI newsletter — 5-step Python pipeline"
- [ ] `r/MachineLearning` — only the "Project" or weekly thread
- [ ] `r/learnmachinelearning` — focus on what you learned

**Reddit etiquette:** Don't just drop the link. Write 3-4 paragraphs explaining what you built, what was hard, what you learned. Link at the bottom.

---

## Sunday — Hacker News + Product Hunt (2 hours)

### Block 1 — Hacker News (30 min)
- [ ] Submit at **8 AM Pacific Time** (best HN time, = 6 PM Riga)
- [ ] Title: `Show HN: AI newsletter that emails me every morning ($0/run)`
- [ ] First comment from your own account: short story of why you built it
- [ ] If you get on the front page → reply to EVERY comment within an hour

### Block 2 — Product Hunt prep (30 min)
- [ ] Create a Product Hunt account if you don't have one
- [ ] Build hype: post on Twitter "Launching on PH next Tuesday — would love your support"
- [ ] Get 5 friends to commit to "hunting" / upvoting on launch day
- [ ] Prepare assets: logo, 3 screenshots, GIF demo, tagline

### Block 3 — Dev.to / Hashnode blog post (1 hour)
Write a long-form tutorial: **"How I built a self-running AI newsletter for free"**

Structure:
1. The problem (overwhelmed by AI news)
2. The solution architecture (WAT framework)
3. Step-by-step build (code snippets)
4. Lessons learned
5. The repo link

Cross-post to:
- [ ] Dev.to
- [ ] Hashnode
- [ ] Medium
- [ ] Your own Beehiiv (as a special edition)

---

# WEEK 3 — First Income (June 8–14)

The goal of this week: secure your first paid consulting client.

## Cold Email Campaign for Consulting

### Day 1 — Build your target list (1 hour)
Find 20 Latvian/Baltic companies who would benefit from AI automation:
- [ ] Real estate agencies (need market reports)
- [ ] Law firms (need legal news digests)
- [ ] Marketing agencies (need competitor monitoring)
- [ ] E-commerce stores (need trend tracking)
- [ ] Recruitment agencies (need talent market summaries)

**Tools:** LinkedIn Sales Navigator (free 30-day trial), Apollo.io (free 50 credits), Google Maps + their websites.

Build a spreadsheet:
| Company | Contact Name | Email | LinkedIn | Status |

### Day 2 — Send 10 cold emails (1 hour)

**Template:**
```
Subject: A daily AI briefing for [Company Name] — built in a weekend

Hi [Name],

I noticed [specific thing about their business — read their About page].

I recently built an AI system that researches a topic each morning,
writes a polished briefing, and emails it to a team. It runs $0/month.

I'd like to offer to build a custom version for [Company Name]:
- "Daily competitor watch" — what your top 5 competitors did yesterday
- "Industry pulse" — top 5 news stories in [their industry] each morning
- "Market intel" — daily summary of [their market]

15-min call this week to see if it fits?

Best,
Siyas
Student at RTU, building AI automation
github.com/Siyaslwf/ai-morning-briefing
```

**Pricing structure:**
- €500 — One custom newsletter, fully set up, runs on their infrastructure
- €1,500 — Three newsletters + their team trained on how to modify
- €3,000/year — Monthly maintenance retainer + 4 newsletters

### Day 3-5 — Follow up + take calls (2 hours/day)
- [ ] Follow up after 3 days if no reply (1 line: "bumping this in case it got buried")
- [ ] Take every call seriously, even if they say "not now"
- [ ] After each call, ask: "Do you know anyone else who could use this?"

**Success metric:** 1 paid client by end of week 3.

---

# WEEK 4 — Build the Hosted Version (June 15–21)

The goal: a landing page where strangers can sign up and pay for the service without you doing any manual work.

## Monday-Wednesday — Landing Page (3 evenings)

### Tech stack
- [ ] Vercel for hosting (free)
- [ ] Next.js or just plain HTML/CSS (your choice)
- [ ] Supabase for the subscriber database (free up to 500MB)
- [ ] Stripe for payments (no monthly fee, 1.4% + 25¢ per transaction)

### Pages to build
1. **Landing page** — hero + screenshot + pricing + signup form
2. **Pricing page** — Free / $5/mo / $15/mo tiers
3. **Dashboard** — let users pick their daily topic
4. **Login/signup** — Supabase auth (Google login)

### Pricing tiers
| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 1 topic, 3x/week |
| Pro | $5/mo | Daily, 3 topics, custom delivery time |
| Team | $15/mo | Daily, unlimited topics, team distribution |

## Thursday-Friday — Connect Backend (2 evenings)
- [ ] Modify `run_newsletter.py` to iterate through all paying subscribers
- [ ] Add subscriber email + topic preference to GitHub Actions inputs
- [ ] Test that 3 test subscribers all get their personalized newsletter

## Saturday — Soft Launch (2 hours)
- [ ] Email everyone who showed interest in week 2
- [ ] Post in Indie Hackers "Show IH"
- [ ] Update your LinkedIn with: "🚀 Just shipped the hosted version"

**Success metric:** 5 paying users by end of week 4 ($25/mo recurring).

---

# MONTH 2 — Audience Growth (June 22 – July 22)

## Weekly publishing rhythm

| Day | Activity | Time |
|-----|----------|------|
| Monday | Send daily newsletter | 0 min (automated) |
| Tuesday | LinkedIn post about a feature you built | 30 min |
| Wednesday | Reply to comments, engage with others' posts | 30 min |
| Thursday | Twitter thread on something AI-related | 30 min |
| Friday | Reach out to 10 new prospects (cold email) | 1 hr |
| Saturday | Write a long-form blog post | 2 hrs |
| Sunday | Plan next week's content | 30 min |

## Content ideas (one per week)

- [ ] "I just hit 100 subscribers — here's what I learned"
- [ ] "The 5 prompts I use to make my AI newsletter not suck"
- [ ] "Cost breakdown: running a daily AI service for $0"
- [ ] "How I added [feature] to my AI newsletter in 2 hours"
- [ ] "I asked AI to write a newsletter about itself — here's what happened"

## Submissions & directories

- [ ] [Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents) — submit PR
- [ ] [Awesome Newsletters](https://github.com/Stigjb/awesome-newsletters) — submit PR
- [ ] [AlternativeTo](https://alternativeto.net) — add as alternative to Morning Brew
- [ ] [BetaList](https://betalist.com) — list your product
- [ ] [Indie Hackers Products](https://www.indiehackers.com/products) — add yours

**Success metric by end of Month 2:** 100 newsletter subscribers, 10 paying users ($50/mo), 1,000 LinkedIn followers.

---

# MONTH 3 — Compound Growth (July 23 – Aug 22)

## Career leverage activities

### Update your professional presence
- [ ] LinkedIn headline: "Computer Engineering Student @ RTU | Building AI Automation Tools | Creator of Morning Stack"
- [ ] Featured section: pin the GitHub repo + Beehiiv newsletter
- [ ] About section: tell the story of building this
- [ ] Add project to LinkedIn projects with metrics ("X subscribers, Y paying users")

### CV updates
- [ ] Add to top of CV under "Projects":
  ```
  AI Morning Briefing — Self-running AI newsletter system
  • Built end-to-end automation: research → writing → image generation → delivery
  • Runs daily at $0 operational cost using free-tier APIs and GitHub Actions
  • [X] active subscribers, [X] paying customers, [X] GitHub stars
  • Stack: Python, Gemini API, Jinja2, SMTP, GitHub Actions
  ```

### Apply to opportunities
- [ ] Apply for a paid internship at: Anthropic, OpenRouter, Pollinations, Mintos, Printify, Lokalise
- [ ] Apply for Y Combinator Startup School (free, online)
- [ ] Apply for European AI/ML grants and competitions
- [ ] Apply for RTU's startup incubator if they have one

## Scaling activities

### Add monetization features
- [ ] Newsletter sponsorships — once you hit 500 subscribers, charge €100-300/issue
- [ ] Affiliate links — recommend AI tools, earn commission
- [ ] Premium tier — exclusive deep-dives for $20/mo

### Build a small team (optional, only if growing fast)
- [ ] Hire a part-time student to handle customer support (€5/hr from your revenue)
- [ ] Find a co-founder if you want to go full-time on this

**Success metric by end of Month 3:** 500 subscribers, 30 paying users ($150/mo recurring), 1+ paid consulting client at €500-1500.

---

# Tools & Resources

## Free tools you'll use
| Purpose | Tool | Cost |
|---------|------|------|
| Code hosting | GitHub | Free |
| Automation | GitHub Actions | Free (2,000 min/mo) |
| AI research | Gemini API | Free (1,500 req/day) |
| AI images | Pollinations.ai | Free, unlimited |
| Email sending | Gmail SMTP | Free (500/day) |
| Newsletter platform | Beehiiv | Free up to 2,500 subs |
| Web hosting | Vercel | Free |
| Database | Supabase | Free up to 500MB |
| Payments | Stripe | Free + 1.4% per txn |
| Cold email finder | Apollo.io | Free 50 credits/mo |
| Design assets | Canva | Free |
| Analytics | Plausible (cheap) or Vercel Analytics (free) | $9/mo or free |
| Domain | Namecheap | ~$10/year |

## Books to read (in this order)
1. **"The Mom Test"** by Rob Fitzpatrick — how to validate without lying to yourself
2. **"Show Your Work"** by Austin Kleon — how to build an audience by being open
3. **"The Lean Startup"** by Eric Ries — ship fast, learn faster
4. **"Make"** by Pieter Levels — solo indie hacker playbook

## People to follow / learn from
- [Pieter Levels](https://twitter.com/levelsio) — solo founder, $200k/mo with no team
- [Marc Lou](https://twitter.com/marc_louvion) — ships products fast
- [Tony Dinh](https://twitter.com/tdinh_me) — indie maker
- [Daniel Vassallo](https://twitter.com/dvassallo) — portfolio of small bets

---

# Common Pitfalls (Avoid These)

1. **❌ Spending 3 weeks improving the code before launching**
   The current version is good enough. Ship it.

2. **❌ Building features no one asked for**
   Talk to users first. Build second.

3. **❌ Trying to do everything at once**
   Pick one channel (LinkedIn or Twitter or Reddit) and go deep before adding more.

4. **❌ Underpricing**
   If a real estate agency wants this, €500 is cheap for them. Don't charge €50.

5. **❌ Going silent for 2 weeks then posting one update**
   Consistency > intensity. 1 post every Tuesday > 10 posts in one day then nothing.

6. **❌ Comparing yourself to people 5 years ahead of you**
   You're 1 week into this. Compare yourself to where you were last month.

---

# Daily Check-In Template

Use this 5-minute end-of-day journal:

```
Date: __________

Today I shipped: __________
Today I learned: __________
One thing I'm proud of: __________
Tomorrow's #1 priority: __________
Blocker (if any): __________
```

Saving these gives you content for "what I learned" posts later.

---

# Emergency Contacts / When Stuck

| Problem | Where to go |
|---------|-------------|
| Code bug | GitHub Issues / Stack Overflow / Claude |
| API limit hit | Switch to paid tier ($5-20/mo solves most) |
| No subscribers | Post in 3 more communities, ask 5 more friends |
| No paying users | Lower price, increase value, or pivot offer |
| Burnout | Take 1 weekend off completely. Then come back. |

---

# The Real Goal

Don't measure success by:
- ❌ GitHub stars
- ❌ LinkedIn likes
- ❌ Twitter followers

Measure success by:
- ✅ Paying users (even 1 = proof)
- ✅ A real audience that opens your emails (>40% open rate)
- ✅ Concrete skills you can demonstrate in any job interview
- ✅ The momentum to ship the next thing faster

---

**You've already done the hardest part — you built the system.**
**Everything from here is just distribution and iteration.**

Print this. Stick it on your wall. Cross things off.

The next 90 days will compound for the next 10 years.

— Start now. —
