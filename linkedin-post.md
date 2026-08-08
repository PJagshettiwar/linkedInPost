---
name: linkedin-post
description: Write and publish a LinkedIn post with optional branded visual — structured workflow from topic to posted. Use when user wants to draft, write, or publish a LinkedIn post.
---

# LinkedIn Post Workflow

End-to-end: topic → draft → visual → review → publish.

---

## STEP 1 — Ask for Topic

Ask:

> "What topic would you like to create a LinkedIn post about?"

If user provides a file/doc with content, use that as source material. Wait for response before continuing.

---

## STEP 2 — Generate Post Text

Write a LinkedIn post in Pankaj's voice. Follow every rule below.

### Structure (in order)
1. **Hook** (1-2 sentences) — Bold, direct, sometimes provocative. Statement or question. Under 210 chars (what shows before "...see more").
2. **The problem** (2-3 sentences) — What's broken, what people get wrong. Make it relatable.
3. **The shift** (1-2 sentences) — What changed. Name the tool/method/insight.
4. **Examples** (3-4 lines each, 2-3 examples) — Specific. Each needs: what went wrong, what was tried, what worked. Use real numbers.
5. **Takeaway** (2-3 sentences) — The non-obvious lesson. Not "AI is great" but the specific insight.
6. **CTA** (1-2 sentences) — Question or invitation that sparks comments. Not salesy.
7. **Hashtags** — 3-5 specific ones. No generic tags like #innovation.

### Tone & Voice Rules
- First person. "I found" not "We discovered."
- Conversational and honest — sounds like a developer sharing real experience
- Short paragraphs (1-3 sentences each), separated by blank line
- Heavy use of "I" and "you" — personal, never corporate
- Enthusiastic but grounded — never hype-y
- Specific over general: "12,000-line PR" not "large PR", "4 minutes" not "quickly"
- 180-280 words total (~1500-2500 chars)
- Maximum 2 emojis in entire post — use sparingly, only for visual section markers
- Opinionated but backed by evidence

### Banned Words
Never use: synergy, leverage, utilize, revolutionize, game-changer, paradigm, cutting-edge, seamless, robust, innovative, unlock, journey

### What NOT to Do
- Don't start with "In today's fast-paced world..."
- Don't end with "What do you think? Let me know in the comments!" (too generic)
- Don't use emojis as bullet points
- Don't use more than 5 hashtags
- No bullet lists unless it's a "playbook" format post

---

## STEP 3 — Ensure Template is on GitHub

The Kie.ai API requires a **publicly accessible URL** for `image_input`. The template must be hosted in a public GitHub repo.

**Check if template is already pushed:**
```bash
curl -s -o /dev/null -w "%{http_code}" \
  "https://raw.githubusercontent.com/<GITHUB_USERNAME>/<PUBLIC_REPO>/main/linkedin-post-template.jpg"
```

If **200**, skip to URL assignment.

**If not 200 (first time only):** push template to GitHub:
```bash
cd /tmp && git clone https://github.com/<GITHUB_USERNAME>/<PUBLIC_REPO>.git 2>/dev/null || true
cp "nano-banana/template/linkedin-post-template.jpg" \
  /tmp/<PUBLIC_REPO>/
cd /tmp/<PUBLIC_REPO>
git add "linkedin-post-template.jpg"
git commit -m "Add LinkedIn post template"
git push origin main
```

**Set permanent raw URL:**
```
TEMPLATE_URL = https://raw.githubusercontent.com/<GITHUB_USERNAME>/<PUBLIC_REPO>/main/linkedin-post-template.jpg
```

---

## STEP 4 — Choose Visual Format

Read `nano-banana/prompts/brand_style.json` and pick best fit:

| Format | When to use |
|---|---|
| **A — Bold Text + Person** | Personal/inspirational posts. Large title text + photorealistic confident figure. |
| **B — Tech Infographic** | Framework, system, or multi-part concept posts. Connected nodes + accent lines. |
| **C — Split Layout** | Contrast/comparison posts. Two-column with central divider. |

Identify 3-5 key concepts that need to appear as labeled nodes or text in the visual.

**If user skips image generation**, jump to Step 7.

---

## STEP 5 — Build Image Prompt

Use Dense Narrative Format with `image_input`. The model receives template as structural reference and generates inner content inside it.

### How `image_input` changes the prompt
- Template provides: outer frame, rounded border, background gradient
- Prompt instructs model to **fill the empty inner content area**
- Explicitly tell model to **preserve** border, background, and any logo
- **Inner background must match template gradient** — not black, not grey

### Brand Rules (from brand_style.json)
- **Primary accent**: Warm orange (#e87435) — title glow, connecting lines
- **Secondary accent**: Cyan (#00c8d8) — icon fills, node borders
- **Text**: White labels (#ffffff), orange glow on main title
- **Connections**: Orange thin lines with glowing dot endpoints
- Update colors in `brand_style.json` to match your template

### JSON structure (flat format — routes to nano-banana-pro):
```json
{
  "prompt": "Keep the outer frame, rounded border, and background exactly as shown in the reference image — do not alter or remove them. Fill the empty inner content area with: <dense narrative of visual concept — layout, title text, node labels, connecting lines, brand colors>. Primary accent: warm orange (#e87435). Secondary accent: cyan (#00c8d8). White sans-serif labels.",
  "negative_prompt": "white background, light background, pastel colors, blurry text, low contrast, excessive clutter, purple tones, black background",
  "image_input": [
    "<TEMPLATE_URL>"
  ],
  "api_parameters": {
    "aspect_ratio": "4:5",
    "resolution": "1K",
    "output_format": "jpg"
  },
  "settings": {
    "style": "premium dark tech infographic, preserve reference template frame, neon accent visuals",
    "lighting": "ambient neon glow from warm orange and cyan accents, dark atmospheric",
    "quality": "high detail, sharp legible text, vibrant neon on dark background"
  }
}
```

**Note:** No `"model"` key, no `"input"` wrapper. Flat structure with `api_parameters` routes to nano-banana-pro.

---

## STEP 6 — Save Prompt and Generate Image

1. Create slug from topic (lowercase, hyphens, max 30 chars). E.g. "AI agents for sales" → `ai-agents-for-sales`

2. Save prompt JSON to:
   ```
   nano-banana/prompts/post_<slug>.json
   ```

3. Generate:
   ```bash
   cd nano-banana
   python3 scripts/generate_kie.py \
     "prompts/post_<slug>.json" \
     "images/posts/<slug>_final.jpg" \
     "4:5"
   ```

4. Read and display the generated image to user.

---

## STEP 7 — Save Draft

Save post text to `Topics/<topic-slug>.md`

If revising an existing file, save as `<topic-slug>_v<N>.md`

---

## STEP 8 — Present and Get Approval

Show in this order:
1. Full post text, formatted as it would appear on LinkedIn (ready to copy-paste)
2. Final visual (if generated) — display the image
3. Character count
4. File locations (post text + image + prompt)

Ask: **"Ready to post, or want changes?"**

**NEVER post without explicit approval.**

---

## STEP 9 — Post to LinkedIn

Once approved, post using `linkedin_post.py`:

**Text-only:**
```bash
python3 linkedin_post.py "FULL POST TEXT HERE"
```

**With image:**
```bash
python3 linkedin_post.py \
  "FULL POST TEXT HERE" \
  "nano-banana/images/posts/<slug>_final.jpg"
```

First-time auth opens browser for LinkedIn OAuth. Token saved to `.linkedin_token.json` and reused automatically.

On success, script prints post ID.

---

## Error Handling

| Error | Action |
|---|---|
| Template URL returns non-200 | Push template to GitHub using Step 3 commands |
| GitHub push fails (auth) | Run `gh auth login` and retry |
| `generate_kie.py` fails with auth error | Check `KIE_API_KEY` in `nano-banana/.env` |
| API returns 500 or task fails | Kie.ai overload — wait 30 seconds, retry |
| `generate_kie.py` times out (60 polls) | Report task ID, check Kie.ai dashboard |
| Output image looks off | Offer to regenerate, reinforce preservation language in prompt |
| Token expired (401) | Script auto-retries with fresh OAuth flow |

---

## First-Time Setup Checklist

- [ ] Create LinkedIn post template image (1200×1500 px) with your branding
- [ ] Save to `nano-banana/template/linkedin-post-template.jpg`
- [ ] Push template to public GitHub repo (Step 3)
- [ ] Update `<GITHUB_USERNAME>` and `<PUBLIC_REPO>` placeholders in this workflow
- [ ] Update brand colors in `nano-banana/prompts/brand_style.json` to match template
- [ ] Verify `KIE_API_KEY` in `nano-banana/.env`
- [ ] `pip install requests python-dotenv`
- [ ] LinkedIn OAuth credentials set in `linkedin_post.py` (lines 24-25)
