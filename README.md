# LinkedIn Post CLI

Post to LinkedIn from terminal. Text-only or with image.

## Setup

1. Create a LinkedIn app at [linkedin.com/developers](https://www.linkedin.com/developers/)
   - Add OAuth 2.0 redirect URL: `http://localhost:3000/callback`
   - Request scopes: `openid`, `profile`, `email`, `w_member_social`
2. Set your credentials in `linkedin_post.py` (lines 24-25):
   ```python
   CLIENT_ID = "your_client_id"
   CLIENT_SECRET = "your_client_secret"
   ```
3. Install dependency:
   ```bash
   pip install requests
   ```

## Usage

```bash
# Text post
python linkedin_post.py "Your post text here"

# Post with image
python linkedin_post.py "Your post text here" /path/to/image.jpg

# Interactive (type text, Ctrl+D to send)
python linkedin_post.py
```

## Auth

First run opens browser for LinkedIn OAuth. Token saved to `.linkedin_token.json` and reused automatically. If token expires, re-auth happens automatically.
