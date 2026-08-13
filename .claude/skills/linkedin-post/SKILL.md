---
name: linkedin-post
description: Write and publish a LinkedIn post with branded visual — from brainstorm to posted. Use when user wants to brainstorm topics, draft, write, or publish a LinkedIn post.
---

# LinkedIn Post Workflow

Two paths: **Brainstorm** (need a topic) or **Post** (have content). If user provides content, skip to Step 2.

---

## STEP 1 — Brainstorm (skip if user has content)

### 1A — Persona & Voice

Pankaj is a Backend Architect at Autodesk, Platform Engineering. His voice:
- Senior IC who's seen production break at 3am
- Shares real war stories, not theory
- Specific numbers always ("12,000-line PR", "4 minutes", "41-point epic")
- Opinionated but evidence-backed
- First person, conversational, never corporate

**Target audience:** Senior/Staff engineers, engineering managers, developers evaluating AI tools.

### 1B — Topic Research

Ask: **"What topic would you like to create a LinkedIn post about?"**

If user needs ideas, research by:
1. Check `topics/` directory for existing drafts and past posts
2. Check what's trending in user's domain (platform engineering, AI-assisted dev, backend architecture)
3. Propose 3 topic angles with one-line hooks for each
4. Wait for user to pick or provide their own

### 1C — Thought Process & Structure

Before writing, plan the post structure:
1. **What's the pivot?** Two contrasting actions for the hook. "I stopped X. I started Y."
2. **What's the reframe?** What do people assume wrong? What's the real issue? (2 short lines)
3. **What's the method?** One bold rule + 3-5 framework questions that define it.
4. **What are the results?** 3-5 single-sentence outcomes with specific numbers.
5. **What's the counterintuitive insight?** Small investment → big payoff. "20 minutes saved hours."
6. **What's the punchline?** Contrasting pair. "X is temporary. Y becomes Z."

Present this plan to user in 6 lines. Get thumbs up before drafting.

### 1D — Draft Post

**Before writing, read `references/golden-example.md` for the exact structural blueprint and pattern rules.** Follow that line-by-line structure. The golden example is the quality bar — match it.

Write the post following the structure and rules below. **Critical formatting checklist before presenting draft:**

- [ ] Every sentence is on its own line (no multi-sentence paragraphs)
- [ ] Key phrases use Unicode bold (𝗯𝗼𝗹𝗱), not markdown `**bold**`
- [ ] Hook is two contrasting actions in one line ("I stopped X. I started Y.")
- [ ] Problem is a reframe in two lines (assumption + real issue)
- [ ] Method stated as bold rule + grouped framework questions (no blank lines between questions)
- [ ] Results are stacked single-sentence outcomes (one per line)
- [ ] Includes a surprise pivot ("The surprising part?") before counterintuitive insight
- [ ] Takeaway is a contrasting pair ("X is temporary. Y becomes Z.")
- [ ] CTA is soft intro + ONE strong question (not multiple weak ones)
- [ ] Link/promo is separate from CTA, casual tone
- [ ] Unicode bold on: key numbers, tool names, core method phrase, key term only — selective, not everywhere
- [ ] Post reads well when each line is scanned independently (mobile test)

Then go to Step 2.

---

## Post Structure Rules

### Format (in order — follow `references/golden-example.md` blueprint)
1. **Hook** — Two contrasting actions, same line. "I stopped X. I started Y." Under 210 chars. NOT a question, NOT a claim — a pivot.
2. **Reframe** (2 lines) — Line 1: what people assume. Line 2: the real issue. Short. Separated by blank line.
3. **Method** — Transition sentence ("We introduced..."), then bold rule in Unicode bold, then 3-5 grouped framework questions (no blank lines between questions).
4. **Tool intro** — One sentence naming the tool/method with Unicode bold on the name.
5. **Results** — One result per line, separated by blank lines. First result uses Unicode italic for one contrast word. Last can be slightly longer. Bold the numbers.
6. **Surprise pivot** — "The surprising part?" then counterintuitive insight with bold numbers (small investment → big payoff).
7. **Broader context** — One sentence zooming out to the trend, with bold key term.
8. **Punchline** — Two short sentences that mirror each other. Contrasting pair. "X is temporary. Y becomes Z."
9. **CTA** — Soft intro ("Curious to hear:") + ONE strong question. Not three weak ones.
10. **Link** — Separate section, casual. "If you're curious about X, check out\nY: link"
11. **Hashtags** — 3-5 specific ones.

### LinkedIn-Native Formatting Rules
- **One sentence per line.** This is the #1 rule. LinkedIn is read on mobile. Walls of text kill engagement. Every sentence gets a blank line before and after it.
- **Unicode bold** (𝗧𝗵𝗶𝘀 𝘀𝘁𝘆𝗹𝗲) for key phrases, numbers, and tool names. LinkedIn does NOT render markdown. Use Unicode Mathematical Bold (U+1D5D4–U+1D607) for bold emphasis. Apply to: key numbers, tool/framework names, the core insight phrase, and the takeaway punchline.
- **Unicode italic** (𝘵𝘩𝘪𝘴 𝘴𝘵𝘺𝘭𝘦) sparingly for contrast words. Use Unicode Mathematical Italic (U+1D608–U+1D63B).
- **Stack statements, don't nest them.** Wrong: "PR reviews shifted from debating what to build to checking implementation, and design discussions moved out of pull requests." Right: "PR reviews stopped debating 𝘸𝘩𝘢𝘵 we were building.\n\nThey focused on whether the implementation matched the spec."
- **Questions as standalone lines.** Each question gets its own line, not embedded in a paragraph.

### Tone Rules
- First person always. "I found" not "We discovered"
- One sentence per paragraph, separated by blank lines (wall of text = scroll past)
- Specific over general: numbers, tool names, exact outcomes
- 180-280 words (~1500-2500 chars) — but airy with whitespace, not dense
- Maximum 2 emojis in entire post, only as section markers
- Opinionated but backed by evidence
- Write for mobile scrolling: each line should make sense if read in isolation

### Banned Words
synergy, leverage, utilize, revolutionize, game-changer, paradigm, cutting-edge, seamless, robust, innovative, unlock, journey

### Never Do
- Start with "In today's fast-paced world..."
- End with "What do you think? Let me know in the comments!"
- Use emojis as bullet points
- Use more than 5 hashtags
- Write multi-sentence paragraphs (split into single-sentence lines)
- Use humble-brag framing ("I'm humbled to announce...")
- Use markdown bold (`**text**`) — LinkedIn renders it literally. Always use Unicode bold.
- Write essay-style narrative paragraphs — stack punchy statements instead
- Embed questions inside paragraphs — each question gets its own line

---

## STEP 2 — Generate Image

Create slug from topic (lowercase, hyphens, max 30 chars).

### File structure

All files for a topic live under `topics/<slug>/`:
```
topics/<slug>/
├── <slug>-v1.md              # Post draft(s)
├── <slug>-for-image.md       # Image text (plain text + **bold** markers)
└── images/
    └── <slug>_final.png      # Generated image
```

### 2A — Prepare image content

Decide what text goes on the image. This is the **hook or summary** — not the full post. Usually 2-5 short sentences that capture the core message. Think tweet-screenshot style.

Save image text to `topics/<slug>/<slug>-for-image.md`. Use `**bold**` markers for emphasis — the script renders them as actual bold text. No markdown headers, no hashtags.

### 2B — Generate image

```bash
python3 post-generation/scripts/create_post_image.py \
  topics/<slug>/<slug>-for-image.md \
  topics/<slug>/images/<slug>_final.png
```

Script auto-scales font (28-80px) to fill template. Supports `**bold**` markers.

### 2C — Show image to user

Read and display the generated image. If user wants changes, edit image text file and regenerate.

---

## STEP 3 — Review & Approve

Show in this order:
1. Full post text (formatted as it would appear on LinkedIn — ready to copy-paste)
2. Generated image
3. Character count
4. File locations

Ask: **"Ready to post, or want changes?"**

If changes requested, loop back to relevant step.

**NEVER post without explicit approval.**

---

## STEP 4 — Post to LinkedIn

Once approved:

**With image:**
```bash
python3 post-generation/scripts/linkedin_post.py \
  "FULL POST TEXT HERE" \
  "topics/<slug>/images/<slug>_final.png"
```

**Text-only:**
```bash
python3 post-generation/scripts/linkedin_post.py "FULL POST TEXT HERE"
```

First-time auth opens browser for LinkedIn OAuth. Token saved to `.linkedin_token.json`.

Save final post text to `topics/<slug>/<slug>.md` (inside the topic folder, not at topics root).

---

## Error Handling

| Error | Fix |
|---|---|
| `create_post_image.py` fails | Check template exists at `post-generation/template/linkedin-black-template.png` |
| Pillow not installed | `pip install Pillow` |
| Token expired (401) | Script auto-retries OAuth flow |
| `linkedin_post.py` fails | Check `.env` has `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET` |

---

## Algorithm Tips (reference: `references/linkedin-2026-best-practices.md`)

- **Saves** are top signal — write frameworks/checklists people revisit
- **Dwell time** matters — tension + specifics + scannable formatting
- **Substantive comments** > reaction counts
- Best posting: Tue-Thu, 8-10am local
