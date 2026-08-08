# LinkedIn Post Toolkit

Write, design, and publish LinkedIn posts from terminal. Draft content in markdown, generate branded post images from templates, and publish directly via LinkedIn API — all without leaving the command line.

## Project Structure

```
linkedInPost/
├── topics/                          # Post content organized by topic
│   └── superpowers/                 # Each topic gets its own folder
│       ├── superpower_v2.md
│       ├── superpowers-skills-final.md
│       └── images/                  # Generated images for this topic
│           └── superpowers-skills_final.png
├── post-generation/
│   ├── scripts/
│   │   ├── linkedin_post.py        # Publish posts to LinkedIn (text or image)
│   │   └── create_post_image.py    # Render post text onto branded templates
│   └── template/
│       └── linkedin-black-template.png  # Dark-themed LinkedIn post template
├── .env                            # LinkedIn API credentials (git-ignored)
└── .claude/skills/linkedin-post/   # Claude Code skill for AI-assisted drafting
```

## Quick Start

### 1. LinkedIn App Setup

Create an app at [linkedin.com/developers](https://www.linkedin.com/developers/):
- OAuth 2.0 redirect URL: `http://localhost:3000/callback`
- Scopes: `openid`, `profile`, `email`, `w_member_social`

### 2. Configure Credentials

```bash
cp .env.example .env
# Edit .env with your credentials:
# LINKEDIN_CLIENT_ID=your_client_id
# LINKEDIN_CLIENT_SECRET=your_client_secret
```

### 3. Install Dependencies

```bash
pip install requests python-dotenv Pillow
```

## Usage

### Publish a Post

```bash
# Text-only post
python post-generation/scripts/linkedin_post.py "Your post text here"

# Post with image
python post-generation/scripts/linkedin_post.py "Your post text here" path/to/image.png

# Interactive mode (type text, Ctrl+D to send)
python post-generation/scripts/linkedin_post.py
```

First run opens browser for LinkedIn OAuth. Token is saved and reused automatically.

### Generate a Post Image

Render markdown content onto a branded template:

```bash
python post-generation/scripts/create_post_image.py topics/superpowers/superpowers-skills-final.md topics/superpowers/images/output.png
```

Use a custom template:

```bash
python post-generation/scripts/create_post_image.py content.md output.png --template post-generation/template/linkedin-black-template.png
```

Font size auto-scales to fill available space without truncation.

### Full Workflow: Draft to Published

```bash
# 1. Write your post in markdown
#    topics/<your-topic>/post-title.md

# 2. Generate the post image
python post-generation/scripts/create_post_image.py topics/superpowers/post.md topics/superpowers/images/post.png

# 3. Publish with image
python post-generation/scripts/linkedin_post.py "Post text here" topics/superpowers/images/post.png
```

## Adding New Topics

1. Create folder: `topics/<topic-name>/`
2. Write posts as `.md` files inside it
3. Generated images go to: `topics/<topic-name>/images/`

## Adding New Templates

Drop template images into `post-generation/template/`. Use `--template` flag to select.

## AI-Powered Workflow with Claude Code

This project includes a **Claude Code skill** (`linkedin-post`) that automates the entire post lifecycle — brainstorming topics, drafting posts, generating images, and publishing — all through conversation.

### Setup (for new clones)

```bash
# 1. Install Claude Code if you haven't
npm install -g @anthropic-ai/claude-code

# 2. Navigate to this project
cd linkedInPost

# 3. That's it — the skill lives in .claude/skills/ and loads automatically
```

### Using the Skill

From Claude Code, just say what you need:

```
> /linkedin-post
```

### What the Skill Does

| Step | What happens |
|------|-------------|
| **Brainstorm** | Researches trending angles, proposes 3 topic hooks, helps pick one |
| **Draft** | Writes post using proven structure — hook, tension, evidence, takeaway |
| **Image** | Generates branded post image from your content using templates |
| **Review** | Shows full post + image + char count for approval |
| **Publish** | Posts to LinkedIn via API after explicit approval |

The skill enforces best practices: 180-280 word range, max 2 emojis, specific numbers over vague claims, no corporate buzzwords. Posts are optimized for saves and dwell time — the top LinkedIn algorithm signals in 2026.
