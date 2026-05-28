# Twitter/X Launch Thread

**Best time:** 9–10 AM US Eastern Time (= 4–5 PM Riga)
**Format:** 6-tweet thread, post the first one with a screenshot
**Tag at end of final tweet:** @levelsio @marc_louvion @GoogleDeepMind

---

## Tweet 1 (hook + screenshot)

```
I built an AI that emails me the latest AI news every morning.

It costs $0 to run.

Here's how the entire system works 👇
```
**Attach:** Screenshot of the newsletter rendered in Gmail (laptop view)

---

## Tweet 2 (architecture)

```
Every morning at 11 AM, a GitHub Actions runner spins up a free
Linux container and executes a 5-step pipeline.

Total runtime: ~90 seconds.
Total cost per edition: $0.00
```

---

## Tweet 3 (steps 1-3)

```
1️⃣ Research
Gemini 2.0 Flash + Google Search grounding fetches today's AI news.
Free: 1,500 requests/day.

2️⃣ Writing
Same model writes the full newsletter in a defined tone.

3️⃣ Illustration
Pollinations.ai generates a custom image. Free. Unlimited.
```

---

## Tweet 4 (steps 4-5)

```
4️⃣ HTML rendering
Jinja2 + premailer for inline CSS that survives Outlook.

5️⃣ Delivery
Gmail SMTP. Free up to 500 emails/day.

That's it. No paid APIs. No servers. No subscriptions.
```

---

## Tweet 5 (architecture insight)

```
The pattern that makes this work: WAT — Workflows, Agents, Tools.

→ Markdown SOPs describe the goal
→ Claude/Gemini handles reasoning
→ Python scripts handle execution

If each step were AI-only, 5 steps × 90% accuracy = 59% success rate.
Deterministic execution keeps it reliable.
```

---

## Tweet 6 (CTA)

```
Open-sourced the entire codebase under MIT.

Fork it, modify the topics, run your own version for free:
🔗 github.com/Siyaslwf/ai-morning-briefing

Or subscribe to mine here:
🔗 [your-beehiiv-url]

Built in Riga 🇱🇻
```

---

## After posting

- Quote-tweet your own thread with a follow-up insight 24 hrs later
- Reply to comments within 1 hour
- DM 3 builders you admire and share the thread with them personally
