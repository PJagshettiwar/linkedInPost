# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal utility for creating and publishing LinkedIn posts with branded visuals. Two Python scripts handle image generation and posting via LinkedIn's OAuth API.

## Dependencies

No `requirements.txt`. Install manually:

```
pip install requests python-dotenv Pillow
```

## Scripts

- `post-generation/scripts/linkedin_post.py` — Posts text/image to LinkedIn via OAuth2
- `post-generation/scripts/create_post_image.py` — Renders text onto template image using Pillow

## Environment

LinkedIn OAuth credentials live in `.env` at repo root:

```
LINKEDIN_CLIENT_ID=...
LINKEDIN_CLIENT_SECRET=...
```

Cached token stored in `.linkedin_token.json` (gitignored).

## Workflow

Use the `/linkedin-post` skill for the full brainstorm-to-publish flow. It handles topic selection, drafting, image generation, and posting.
