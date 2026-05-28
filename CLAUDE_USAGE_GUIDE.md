# How to Use Claude Code Pro Without Hitting Limits

Practical guide to using your Claude Code subscription efficiently. Written for you specifically — based on how we've been working.

---

## How Claude Pro Limits Actually Work

Claude Pro uses **rolling 5-hour usage windows**, not a fixed daily/weekly cap. Each message you send adds to that window. When you hit the cap, you wait until the oldest messages "age out" of the 5-hour window.

The cap is measured in **tokens, not messages**. A short question costs a fraction of a long-context conversation. So one massive 50-back-and-forth session can hit the limit faster than 200 short questions across the day.

**Three drivers of how fast you burn through the limit:**
1. **Conversation length** — every message includes the full chat history. A 30-message thread costs ~30× the tokens of message 1.
2. **Model choice** — Opus 4.7 costs ~5× more per token than Sonnet 4.6, which costs ~5× more than Haiku 4.5.
3. **What's loaded in context** — files you've Read, tool outputs, system instructions, MCP servers, memory files.

---

## The Top 10 Rules (Ordered by Impact)

### 1. ⭐ Use `/clear` between unrelated tasks
This is the **single biggest** efficiency win. Every message you send replays the entire conversation. If you've finished one project and want to start something else, type `/clear` first — it resets the context window to zero.

**Example:** After we finished setting up the GitHub repo, you should have used `/clear` before asking about the action plan. The conversation cost would have dropped by ~70%.

**Rule of thumb:** New unrelated task = new conversation. Same task / follow-up = keep going.

---

### 2. ⭐ Switch models based on task complexity
Use `/model <name>` to switch on the fly. Default to the cheapest model that can do the job:

| Task | Best model | Why |
|------|-----------|-----|
| Quick edits, file renames, simple commits | `haiku` (4.5) | 25× cheaper than Opus, still smart enough |
| Routine coding, debugging, refactors | `sonnet` (4.6) | The workhorse — handles 90% of work |
| Hard architectural decisions, complex multi-file work, novel design | `opus` (4.7) | Use sparingly |

**My recommendation for you:** Default to `sonnet`. Only use Opus when you're explicitly designing something hard. You've been on Opus by default — switching to Sonnet for most work would multiply your effective usage by ~5×.

```
/model sonnet     ← do this at the start of most sessions
/model opus       ← only when you're stuck on something hard
/model haiku      ← when running quick one-shot tasks
```

---

### 3. ⭐ Be specific in your requests
Vague requests force me to explore the codebase, which costs tokens. Specific requests are direct.

**Bad (costs more):**
> "Look at my code and fix the issues."

**Good (costs less):**
> "In `tools/send_email.py`, the Gmail authentication fails when the password has spaces. Fix it."

When you know the file path, paste it. When you know the exact line, paste it. The less I have to search, the less it costs.

---

### 4. Use the `/compact` command on long conversations
When a conversation runs long (50+ messages), type `/compact`. It summarizes earlier messages, keeping the gist but dropping detail. Future messages cost less because they replay the summary, not the raw history.

Use `/compact` when:
- The same conversation has gone on for hours
- You want to keep context but the messages are stacking up
- You don't want to start over with `/clear`

---

### 5. Don't paste huge files or logs — point to them
**Bad:** Pasting a 500-line file into chat.
**Good:** "Read `tools/research_topic.py` and fix the error on line 42."

I can read files with the Read tool — costs much less than pasting because I only load what I need. Same for logs: save them to a file, then tell me to read that file.

---

### 6. Use sub-agents for big research tasks
If you ask me to "find all the places X is used in this codebase," I'd normally load lots of files into context. Instead, ask me to launch an Explore or general-purpose agent. Those agents have their own context window and return a short summary — saves a lot of your main context.

You don't have to know this technically — just say:
> "Use a subagent to search the codebase for X."

I'll handle the rest.

---

### 7. Close unused IDE files
When you have a file open in VS Code, it's auto-included in my context every turn. Close files you don't need. Look at the bottom of your editor — if you see `.env` open and we're talking about marketing copy, close `.env`.

This was happening throughout our last few conversations — your `.env` kept getting auto-attached. Each time it adds tokens for content I don't need.

---

### 8. Use Plan Mode for design discussions
Press `Shift + Tab` twice to enter Plan Mode. In this mode, I think and propose without making changes — cheaper than full execution mode for "let's discuss what we should do" conversations.

When you're ready to actually do the work, exit Plan Mode and I execute.

---

### 9. Batch your asks
**Bad:** 10 messages, each asking for one small thing.
**Good:** 1 message that lists all 10 things.

Each message pays the full "replay the conversation" cost. Batching cuts that overhead.

```
"Three things:
1. Add Beehiiv to GitHub Secrets
2. Update the workflow file
3. Push to GitHub"
```

…costs much less than three separate messages.

---

### 10. Skip explaining — let me figure it out
If you say "do X" and I do it, that's one message. If you say "do X and explain to me what you did and why," that's a much longer response, costing more.

Only ask for explanations when you actually want to learn. For routine work, just let me ship.

---

## Specific Things We Did That Cost a Lot (Last Few Conversations)

Looking at our recent history, here's where tokens piled up unnecessarily — fixing these alone would have stretched your limit ~3×:

1. **`.env` was open in VS Code** for most of the session — meaning every turn re-loaded your API keys into context. ~~Lots~~ of tokens lost.

2. **We made lots of small commits** instead of batching. Each `git status` + `git commit` pair costs more than running them in one combined command.

3. **I was running on Opus 4.7** the whole time. For 80% of the work (creating files, copy-paste tasks, simple edits), Sonnet would have been fine.

4. **Long screenshots/conversations**: When you sent multiple screenshots back-to-back without `/clear`, each turn carried all previous screenshots in context.

5. **Asking me to "continue from where you left off"** when I had no specific direction caused exploration work that re-loaded the conversation.

---

## A Smart Working Pattern (Daily Routine)

This is the workflow I'd recommend you adopt going forward:

```
Morning task: "Help me add subscriber analytics to my newsletter."

1. /model sonnet         ← switch off Opus
2. /clear                ← reset context from yesterday
3. Be specific:          ← tell me the file paths up front
   "In tools/send_email.py, after a successful send,
    write the subscriber count to a JSON file
    at .tmp/stats.json."
4. Let me execute        ← don't interrupt
5. /clear when done      ← so the next ask starts fresh
```

vs. what we've been doing:

```
1. (stays on Opus)
2. (continues yesterday's context)
3. "Hey can you check the newsletter and maybe add stats?"
4. (lots of exploration, back-and-forth)
5. (continues into next task without clearing)
```

The first pattern uses ~10× less of your limit per task.

---

## Useful Commands You Should Know

| Command | What it does |
|---------|--------------|
| `/clear` | Reset conversation. Use between unrelated tasks. |
| `/compact` | Summarize long conversations to save context. |
| `/model sonnet` | Switch to Sonnet (cheaper, fast). |
| `/model opus` | Switch to Opus (smart, expensive). |
| `/model haiku` | Switch to Haiku (cheapest, fast). |
| `/fast` | Toggle fast mode on Opus (faster outputs, same model). |
| `/help` | List all available commands. |
| `/cost` | Check your current usage. |
| `Shift + Tab × 2` | Enter Plan Mode. |
| `Ctrl + C` | Cancel a running response (saves tokens if you realize mid-stream you asked the wrong thing). |

---

## If You Hit the Limit

You'll see a message like "You've reached your usage limit." When that happens:

1. **Don't panic.** Wait — the oldest messages age out of the 5-hour window automatically.
2. **Check the message** for the exact reset time. Often it's 1–3 hours away, not the full 5.
3. **Use the wait time productively** — do the manual stuff that doesn't need me (post on LinkedIn, send cold emails, do customer calls).
4. **When you're back**, start with `/clear` and `/model sonnet` to stretch the next window.

If you hit limits regularly, your Pro plan may not be enough — Claude has higher tiers ($100/mo, $200/mo). But before upgrading, try the rules above. Most people use 3× more tokens than necessary; cutting waste extends your existing plan a lot.

---

## When to Trust Memory vs. Re-Read Files

I store information about you in a memory file (`MEMORY.md` and linked files). Future conversations load this automatically — you don't have to re-explain things like:
- Your name, role, RTU student status
- Your project structure and goals
- The free resources/student tools you have access to
- Past preferences

**You don't need to re-paste:**
- Your student resources doc — saved as `student_resources.md`
- Your tech stack preferences — I default to your free options
- Your project context — saved in `project_newsletter_automation.md`

**You DO need to mention** (because memory ages):
- New project goals
- Today's specific deadline / urgency
- Anything that changed since our last conversation

---

## Bottom Line

To stretch your Claude Pro limit:
1. **`/clear` between tasks** (single biggest win)
2. **`/model sonnet` by default** (5× cheaper than Opus for most work)
3. **Be specific** (paste paths, line numbers, exact errors)
4. **Close unused files** in VS Code
5. **Batch your asks** (1 message > 5 messages)

Doing all five will multiply your effective usage by ~10× without changing what you ask for.

— Last updated: 2026-05-28
