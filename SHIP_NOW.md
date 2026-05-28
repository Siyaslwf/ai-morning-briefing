# 🚀 SHIP NOW — 7-Day Sprint

The fast plan. No weekends, no waiting. Ship → audience → income in one week.

**Today is Day 0.** Read this once, then start executing.

---

## ✅ What's Already Done (Claude has shipped these)

| Item | Status | File |
|------|--------|------|
| GitHub repo live + public | ✅ Done | github.com/Siyaslwf/ai-morning-briefing |
| Daily automation scheduled (11 AM EET) | ✅ Done | `.github/workflows/daily_newsletter.yml` |
| Beehiiv API integration code | ✅ Done | `tools/beehiiv_publish.py` |
| Landing page (Vercel-ready) | ✅ Done | `landing/index.html` |
| LinkedIn launch post (3 versions) | ✅ Done | `marketing/01_linkedin_launch.md` |
| Twitter launch thread (6 tweets) | ✅ Done | `marketing/02_twitter_thread.md` |
| Reddit posts (4 subreddits) | ✅ Done | `marketing/03_reddit_posts.md` |
| Hacker News submission | ✅ Done | `marketing/04_hackernews.md` |
| Cold email templates (5 industries) | ✅ Done | `marketing/05_cold_emails.md` |
| Target prospect list method | ✅ Done | `marketing/06_target_list_template.md` |
| Long-form blog post (Dev.to/Medium) | ✅ Done | `marketing/07_blog_post.md` |
| LinkedIn/GitHub/Twitter profile copy | ✅ Done | `marketing/08_profile_assets.md` |
| Professional README with badges | ✅ Done | `README.md` |
| MIT License | ✅ Done | `LICENSE` |
| Full GitHub user guide | ✅ Done | `GITHUB_GUIDE.md` |

**Translation:** All the "what do I write" thinking is done. You just execute.

---

## 🎯 What You Need to Do (Total: ~6 hours over 7 days)

Three categories of work — only YOU can do these because they require your accounts and your fingers.

### A. Account creation (60 min, Day 1)
- Beehiiv (free) — 10 min
- Vercel (free, Sign in with GitHub) — 5 min
- Stripe (free) — 15 min, includes ID verification
- Namecheap (€10/yr, optional but recommended) — 15 min
- Apollo.io (free, for cold email targeting) — 10 min

### B. Manual publishing (90 min, Day 2)
- LinkedIn launch post — 20 min
- Twitter thread — 15 min
- Reddit (r/SideProject only on Day 2) — 15 min
- Hacker News — 15 min
- Dev.to blog post — 25 min

### C. Outreach (3 hours total, Days 3–7)
- Build 20-prospect list — 90 min
- Send 5 cold emails per day (Days 3–6) — 30 min × 4 = 2 hrs
- Take 2-3 calls — 30 min each

That's it. Everything else is automated.

---

## 📅 The 7-Day Calendar

### **DAY 1 — TODAY (Setup, 2 hours)**

#### 🟦 Block 1 — Beehiiv (15 min)
1. Go to [beehiiv.com](https://beehiiv.com) → Start for free
2. Publication name: **The Morning Stack** (or your pick)
3. Subdomain: `morningstack` → URL becomes `morningstack.beehiiv.com`
4. Skip the "import subscribers" step
5. Go to **Settings → Integrations → API** → click **Create API Key**
6. Copy the API key (starts with `bh-`)
7. Find your Publication ID: **Settings → API** (a string starting with `pub_`)

#### 🟦 Block 2 — Add Beehiiv to GitHub Secrets (5 min)
1. Repo → Settings → Secrets and variables → Actions
2. Add three new secrets:
   - `BEEHIIV_API_KEY` = (your API key)
   - `BEEHIIV_PUBLICATION_ID` = (your pub_xxx ID)
   - `BEEHIIV_SEND_LIVE` = `false` (keep as draft for first week)

#### 🟦 Block 3 — Run a test newsletter (10 min)
1. Repo → Actions tab → Daily AI Newsletter → **Run workflow**
2. Wait ~2 minutes
3. Check your inbox AND your Beehiiv dashboard (Posts → Drafts)
4. If the Beehiiv draft looks right → set `BEEHIIV_SEND_LIVE` to `true` for tomorrow

#### 🟦 Block 4 — Deploy the landing page (20 min)
1. Sign in to [vercel.com/new](https://vercel.com/new) with GitHub
2. Import the `ai-morning-briefing` repo
3. **Root directory:** `landing`
4. **Framework preset:** Other
5. Click Deploy → wait 30 seconds → you have a live URL
6. Open `landing/index.html` and replace placeholders:
   - `REPLACE_WITH_BEEHIIV_SUBSCRIBE_URL` → from Beehiiv → Settings → Embed forms → copy the form action URL
   - For now leave Stripe placeholders alone (we'll do those Day 4)
7. Commit + push → Vercel auto-redeploys

#### 🟦 Block 5 — Buy a domain (15 min, optional)
1. Go to [namecheap.com](https://namecheap.com)
2. Search: `morningstack.ai`, `briefme.ai`, `dailystack.io` — pick what's free + under €15
3. Skip all the upsells (no WhoisGuard upgrade, no SSL — Vercel gives free SSL)
4. In Vercel project → Settings → Domains → Add your domain
5. Copy the 2 DNS records Vercel shows you
6. In Namecheap → Domain List → Manage → Advanced DNS → paste those 2 records
7. Wait 5 minutes — site goes live on your domain

#### 🟦 Block 6 — Capture your hero screenshot (10 min)
1. Open the test newsletter that arrived in your Gmail
2. Open it on your laptop (NOT phone)
3. Make the window full-screen
4. Take a clean screenshot showing the header + first insight card
5. Save it as `marketing/hero-screenshot.png`
6. Add it to the top of `README.md` (just push the image, then add `![](marketing/hero-screenshot.png)` near the top)

✅ **End of Day 1 success:** Beehiiv is wired in, landing page is live, you have a screenshot.

---

### **DAY 2 — LAUNCH (3 hours)**

**Pick the best time of day for your audience:**
- LinkedIn → Tuesday/Wednesday 8:30 AM Riga
- Twitter → 4–5 PM Riga (= US morning)
- Hacker News → 6 PM Riga (= 8 AM Pacific)

#### 🟩 Block 1 — LinkedIn (30 min)
1. Open `marketing/01_linkedin_launch.md`
2. Pick Version A (recommended) — copy the text
3. Post on LinkedIn with your hero screenshot attached
4. Within 30 seconds: comment on your own post with the GitHub link + Beehiiv subscribe link
5. **Critical:** reply to every comment in the first 60 minutes — even 1-word replies work
6. DM 10 friends/contacts: "Hey, just shipped this — would love your honest take. Comment if you have one."

#### 🟩 Block 2 — Twitter/X thread (20 min)
1. Open `marketing/02_twitter_thread.md`
2. Post tweet 1 with hero screenshot
3. Add tweets 2–6 as replies in the same thread (use the "+" button)
4. After last tweet, quote-tweet your own thread with the GitHub link

#### 🟩 Block 3 — Hacker News (15 min)
1. Open `marketing/04_hackernews.md`
2. Submit to news.ycombinator.com with the title + URL provided
3. **Within 30 seconds:** post the first comment from the file
4. Stay online for 2 hours and reply to every comment

#### 🟩 Block 4 — Reddit r/SideProject (15 min)
1. Open `marketing/03_reddit_posts.md` → r/SideProject section
2. Post with the title + body provided
3. Reply to commenters
4. **Don't** post to other subreddits today — space them out

#### 🟩 Block 5 — Dev.to blog post (40 min)
1. Sign up at [dev.to](https://dev.to) with GitHub
2. Click **Create Post**
3. Copy content from `marketing/07_blog_post.md`
4. Add tags: `#ai`, `#python`, `#tutorial`, `#opensource`
5. Add a cover image (the Pollinations.ai illustration from your test newsletter works great)
6. Publish

#### 🟩 Block 6 — Update profiles (20 min)
1. Open `marketing/08_profile_assets.md`
2. Update LinkedIn headline + About + Featured section
3. Update GitHub bio + create profile README repo
4. Update Twitter bio
5. Add the new email signature to Gmail

✅ **End of Day 2 success:** Posted on 4 platforms, all profiles updated, first wave of subscribers landing.

---

### **DAY 3 — CONSULTING OUTREACH BEGINS (2 hours)**

#### 🟧 Block 1 — Build the target list (90 min)
1. Open `marketing/06_target_list_template.md`
2. Create a Google Sheet called `outreach-tracker`
3. Find 20 prospects (5 real estate, 5 law firms, 4 marketing agencies, 3 e-commerce, 3 recruitment)
4. For each: company name, website, contact name from LinkedIn, email
5. Use Apollo.io free credits to verify the emails

#### 🟧 Block 2 — Send 5 cold emails (30 min)
1. Open `marketing/05_cold_emails.md`
2. Pick the template that matches each prospect's industry
3. Personalize the opening line with one specific thing from their website
4. Send 5 today (not more — start slow, monitor deliverability)
5. Log each in the spreadsheet

✅ **End of Day 3 success:** Target list complete, 5 emails sent.

---

### **DAY 4 — STRIPE + SEND 5 MORE (2 hours)**

#### 🟨 Block 1 — Stripe Payment Links (45 min)
1. Sign up at [stripe.com](https://stripe.com)
2. Complete identity verification (driver's license or passport)
3. Once verified, go to **Payment Links** → **New**
4. Create two products:
   - **Pro** — $5/month recurring → copy the payment link
   - **Team** — $15/month recurring → copy the payment link
5. Open `landing/index.html` → replace:
   - `REPLACE_WITH_STRIPE_LINK_PRO` with the Pro payment link
   - `REPLACE_WITH_STRIPE_LINK_TEAM` with the Team payment link
6. Commit + push — Vercel auto-redeploys

#### 🟨 Block 2 — Send 5 more cold emails (30 min)
Different industries this time. Track in the spreadsheet.

#### 🟨 Block 3 — Reddit round 2 (20 min)
Post to r/Python today (different community, no risk of cross-posting penalty).

#### 🟨 Block 4 — Engagement (25 min)
Reply to all LinkedIn comments from yesterday. DM anyone who showed strong interest.

✅ **End of Day 4 success:** Payment infrastructure live, 10 cold emails out, audience growing.

---

### **DAY 5 — FOLLOW-UPS + 5 MORE EMAILS (90 min)**

#### 🟪 Block 1 — Follow up Day 3 emails (15 min)
Use the follow-up template in `marketing/05_cold_emails.md` (one line).

#### 🟪 Block 2 — Send 5 more cold emails (30 min)

#### 🟪 Block 3 — Take any booked calls (variable)
- Spend the first 5 min listening to their pain
- Show the GitHub repo as proof
- Quote €500 with confidence
- Ask for 50% upfront via Stripe Payment Link
- After call, log notes in the spreadsheet

#### 🟪 Block 4 — Post a Day 5 milestone update on LinkedIn (15 min)
Template:
```
4 days ago I shipped The Morning Stack — a self-running AI newsletter.

Quick check-in:
→ X subscribers
→ Y GitHub stars
→ Z DMs asking how to build their own

If you've been on the fence — link in comments.
```

✅ **End of Day 5 success:** Day 3 emails followed up, 15 emails total sent, at least 1 call booked.

---

### **DAY 6 — REDDIT BLAST + 5 MORE EMAILS (90 min)**

#### 🟫 Block 1 — Reddit round 3 (20 min)
Post to r/learnmachinelearning or r/SaaS (whichever fits the day's mood).

#### 🟫 Block 2 — Send 5 more cold emails (30 min)
Total to date: 20.

#### 🟫 Block 3 — Follow up Day 4 emails (15 min)

#### 🟫 Block 4 — Submit to free directories (25 min)
- [Awesome AI Agents on GitHub](https://github.com/e2b-dev/awesome-ai-agents) — open a PR adding your project
- [BetaList](https://betalist.com) — submit
- [Indie Hackers Products](https://www.indiehackers.com) — add your product

✅ **End of Day 6 success:** Across 4 platforms + 3 directories, 20 cold emails out.

---

### **DAY 7 — RETROSPECTIVE + DOUBLE DOWN (60 min)**

#### 🟥 Block 1 — Measure everything (20 min)
Make a single document with these numbers:
- Beehiiv subscribers
- LinkedIn followers gained
- LinkedIn impressions on launch post
- GitHub stars
- Twitter followers gained
- Cold email reply rate (X/20)
- Calls booked
- Paying clients closed (€)

#### 🟥 Block 2 — Plan week 2 (20 min)
Based on data:
- **Best channel** → double down (post 3× next week)
- **Worst channel** → cut entirely
- **Worst cold email template** → rewrite or drop
- **Best industry** → focus next 20 emails there

#### 🟥 Block 3 — Celebrate something tangible (20 min)
- Print this plan
- Cross off what's done
- Buy yourself coffee with first €1 of revenue

✅ **End of Day 7 success:** You know what works, what to cut, what to scale.

---

## 📊 Realistic Day-7 Outcomes

If you executed everything:

| Metric | Realistic | Stretch | Best case |
|--------|-----------|---------|-----------|
| Beehiiv subscribers | 20–50 | 100 | 300+ (if HN front page) |
| GitHub stars | 5–15 | 30 | 100+ (if HN front page) |
| LinkedIn followers gained | 30–80 | 150 | 500+ |
| Cold email replies | 2–4 / 20 | 6 | 8 |
| Calls booked | 1–2 | 3 | 5 |
| Paying clients closed | 0–1 | 1 | 2 |
| Revenue | €0 | €500 | €1,500 |

**One client = success.** Even with €0 revenue, you have data + audience + proof to iterate on for week 2.

---

## ⚠️ When to Pull the Emergency Brake

Stop and rethink if any of these happen:

- **0 LinkedIn comments after Day 2** → your hook is wrong. DM 5 people, ask why it didn't land. Rewrite.
- **0 cold email replies after 20 sent** → your offer is unclear. Lower price to €300 and re-target.
- **0 Beehiiv subscribers after Day 3** → your subscribe page is broken or your call-to-action is buried. Test the signup flow yourself in incognito.
- **Gmail blocks you for "suspicious activity"** → you're sending too many cold emails too fast. Drop to 3/day and use longer gaps between sends.

---

## 🤖 What Claude (Me) Can Keep Doing for You

After Day 1, ping me back here and I'll:

- Write Beehiiv → Stripe webhook integration when you're ready to charge
- Rewrite any underperforming copy based on your stats
- Build the customer dashboard if you cross 10 paying users
- Draft the case study after your first paid client
- Generate week 2 / week 3 content from your day-7 data

You only need to be the publisher and the salesperson. I'll handle the engineering and the writing.

---

## 🎯 The One Thing That Matters

If you read nothing else: **publish on Day 2, even if it feels imperfect.**

Every hour you delay launching is an hour you're refining something nobody sees. The first edition of anything is the version that should ship.

Go.

— Last updated: 2026-05-28
