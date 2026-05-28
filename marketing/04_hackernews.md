# Hacker News Submission

**When:** Tuesday or Wednesday, 8 AM Pacific Time (= 6 PM Riga time)
**Why that time:** Hits the front page before US workday peaks, giving max votes window
**Account:** Your HN account needs to exist for at least a week before posting Show HNs

---

## Title (under 80 chars)

**Use one of these:**

- `Show HN: AI newsletter that emails me every morning ($0/run)`
- `Show HN: A self-running AI newsletter using only free APIs`
- `Show HN: Daily AI newsletter automation in 5 Python steps`

**My pick:** Option 1 — the "$0/run" hooks attention. HN loves cost-zero achievements.

---

## URL field

`https://github.com/Siyaslwf/ai-morning-briefing`

---

## First comment (post within 30 seconds of submission)

```
Author here.

I built this because I couldn't keep up with AI news but didn't want
yet another paid newsletter cluttering my inbox.

A few architecture decisions that mattered:

- Splitting the pipeline into discrete tools instead of one big LLM call
  was the difference between 90% reliable and 99% reliable.
- Gemini's Google Search grounding turned out to matter more than model
  size — the free Flash model with grounding beats the bigger models
  without it for "what's happening now" questions.
- The whole thing runs free because every API used has a generous free
  tier: Gemini (1500 req/day), Pollinations.ai (unlimited), Gmail SMTP
  (500 emails/day), GitHub Actions (2000 min/month).

The repo includes the full pipeline plus a GitHub Actions workflow that
schedules it daily. Happy to answer questions about the architecture,
the prompts, or how I'd extend it.
```

---

## Engagement playbook

HN is harsh but fair. Two rules that matter:

1. **Reply substantively to every top-level comment in the first 2 hours.**
   Don't say "thanks!" — actually engage with their point. Even disagreement
   is fine if reasoned.

2. **Never argue defensively about criticism.** If someone says your prompt
   is sloppy, say "you're right, here's how I'd improve it" or "interesting,
   tell me more about your approach." Defending = downvotes.

---

## If you hit the front page

- Don't spam friends to upvote (HN detects this and flags it)
- DO post a follow-up tweet linking to the HN discussion
- Stay online and reply for the full first 4 hours
- Update your README with "Featured on Hacker News [date]" badge afterwards

---

## If it flops (most submissions do — don't take it personally)

- Wait 2 weeks
- Resubmit with a slightly different title and the same URL
- Different time of day
- HN explicitly allows respinning posts that didn't get traction
