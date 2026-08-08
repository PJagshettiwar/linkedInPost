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
1. **What's the one insight?** Every post has exactly one non-obvious takeaway.
2. **What's the tension?** What do people get wrong? What's the counterintuitive truth?
3. **What's the proof?** Real story, real numbers, real outcome.
4. **What's the hook?** First 210 chars must create enough tension to click "see more."

Present this plan to user in 4 lines. Get thumbs up before drafting.

### 1D — Draft Post

Write the post following the structure and rules below, then go to Step 2.

---

## Post Structure Rules

### Format (in order)
1. **Hook** (1-2 sentences) — Bold, direct, sometimes provocative. Under 210 chars.
2. **Problem/Setup** (2-3 sentences) — What's broken, what people get wrong. Relatable.
3. **The shift** (1-2 sentences) — What changed. Name the tool/method/insight.
4. **Evidence** (2-3 examples with specifics) — Each needs: what happened, what was tried, what worked. Real numbers.
5. **Takeaway** (1-2 sentences) — The non-obvious lesson. Standalone bold statement.
6. **CTA** (1 sentence) — Question that sparks real comments. Not generic.
7. **Hashtags** — 3-5 specific ones at the end.

### Tone Rules
- First person always. "I found" not "We discovered"
- Short paragraphs (1-3 sentences), separated by blank lines
- Specific over general: numbers, tool names, exact outcomes
- 180-280 words (~1500-2500 chars)
- Maximum 2 emojis in entire post, only as section markers
- Opinionated but backed by evidence

### Banned Words
synergy, leverage, utilize, revolutionize, game-changer, paradigm, cutting-edge, seamless, robust, innovative, unlock, journey

### Never Do
- Start with "In today's fast-paced world..."
- End with "What do you think? Let me know in the comments!"
- Use emojis as bullet points
- Use more than 5 hashtags
- Write bullet lists unless it's a "playbook" format post
- Use humble-brag framing ("I'm humbled to announce...")

---

## STEP 2 — Generate Image

Create slug from topic (lowercase, hyphens, max 30 chars).

### 2A — Prepare image content

Decide what text goes on the image. This is the **hook or summary** — not the full post. Usually 2-5 short sentences that capture the core message. Think tweet-screenshot style.

Save image text to `topics/<slug>-image.md` (no markdown headers, no hashtags — plain text only).

### 2B — Generate image

```bash
python3 post-generation/scripts/create_post_image.py \
  topics/<slug>-image.md \
  topics/<slug>/images/<slug>_final.png
```

Script auto-scales font (28-80px) to fill template. No manual tuning needed.

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

Save final post text to `topics/<slug>.md`.

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
