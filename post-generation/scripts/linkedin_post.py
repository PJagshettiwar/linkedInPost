#!/usr/bin/env python3
"""
LinkedIn posting script using OAuth 2.0.
First run: opens browser for auth, saves token.
Subsequent runs: uses saved token to post directly.

Usage:
  python linkedin_post.py "Your post text here"
  python linkedin_post.py "Your post text here" /path/to/image.jpg
  python linkedin_post.py  # prompts for text interactively
"""

import sys
import json
import os
import webbrowser
import urllib.parse
import http.server
import threading
import secrets
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# --- Config ---
CLIENT_ID = os.environ["LINKEDIN_CLIENT_ID"]
CLIENT_SECRET = os.environ["LINKEDIN_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:3000/callback"
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", ".linkedin_token.json")
SCOPE = "openid profile email w_member_social"

AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
POST_URL = "https://api.linkedin.com/v2/ugcPosts"
ASSETS_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"


def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return None


def save_token(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    print(f"Token saved to {TOKEN_FILE}")


def get_access_token_via_browser():
    """Run local OAuth flow: open browser, catch callback, exchange code."""
    state = secrets.token_urlsafe(16)
    auth_code_holder = {}
    server_ready = threading.Event()

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/callback":
                params = urllib.parse.parse_qs(parsed.query)
                auth_code_holder["code"] = params.get("code", [None])[0]
                auth_code_holder["state"] = params.get("state", [None])[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Auth complete! You can close this tab.</h1>")
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            pass  # suppress server logs

    server = http.server.HTTPServer(("localhost", 3000), CallbackHandler)

    def serve():
        server_ready.set()
        server.handle_request()  # handle one request then stop

    t = threading.Thread(target=serve, daemon=True)
    t.start()
    server_ready.wait()

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": SCOPE,
    }
    url = AUTH_URL + "?" + urllib.parse.urlencode(params)
    print(f"Opening browser for LinkedIn authorization...")
    webbrowser.open(url)

    t.join(timeout=120)

    code = auth_code_holder.get("code")
    if not code:
        raise RuntimeError("No auth code received. Did you authorize in the browser?")

    # Exchange code for token
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    resp.raise_for_status()
    token_data = resp.json()
    save_token(token_data)
    return token_data["access_token"]


def get_person_urn(access_token):
    resp = requests.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
    resp.raise_for_status()
    data = resp.json()
    return f"urn:li:person:{data['sub']}"


def upload_image(access_token, person_urn, image_path):
    """Register and upload an image asset. Returns the asset URN."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    # Step 1: Register the upload
    register_payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": person_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }
    resp = requests.post(ASSETS_URL, headers=headers, json=register_payload)
    resp.raise_for_status()
    data = resp.json()

    upload_url = data["value"]["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]
    asset_urn = data["value"]["asset"]

    # Step 2: Upload the binary
    ext = os.path.splitext(image_path)[1].lower()
    content_type = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
    with open(image_path, "rb") as f:
        upload_resp = requests.put(upload_url, data=f, headers={"Content-Type": content_type})
    upload_resp.raise_for_status()

    print(f"Image uploaded: {asset_urn}")
    return asset_urn


def post_to_linkedin(access_token, person_urn, text, image_path=None):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    if image_path:
        asset_urn = upload_image(access_token, person_urn, image_path)
        payload = {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset_urn,
                        }
                    ],
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }
    else:
        payload = {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }

    resp = requests.post(POST_URL, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.headers.get("x-restli-id") or resp.json()


def do_post(access_token, post_text, image_path):
    person_urn = get_person_urn(access_token)
    post_id = post_to_linkedin(access_token, person_urn, post_text, image_path)
    print(f"Posted successfully! Post ID: {post_id}")
    return post_id


def main():
    image_path = None

    if len(sys.argv) >= 3:
        post_text = sys.argv[1]
        image_path = sys.argv[2]
    elif len(sys.argv) == 2:
        post_text = sys.argv[1]
    else:
        print("Enter your LinkedIn post text (Ctrl+D when done):")
        lines = []
        try:
            for line in sys.stdin:
                lines.append(line)
        except EOFError:
            pass
        post_text = "".join(lines).strip()

    if not post_text:
        print("No text provided. Exiting.")
        sys.exit(1)

    if image_path and not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        sys.exit(1)

    token_data = load_token()
    if token_data:
        access_token = token_data["access_token"]
        print("Using saved token.")
    else:
        print("No saved token found. Starting OAuth flow...")
        access_token = get_access_token_via_browser()

    try:
        do_post(access_token, post_text, image_path)
    except requests.HTTPError as e:
        if e.response.status_code == 401:
            print("Token expired or invalid. Re-authenticating...")
            if os.path.exists(TOKEN_FILE):
                os.remove(TOKEN_FILE)
            access_token = get_access_token_via_browser()
            do_post(access_token, post_text, image_path)
        else:
            print(f"HTTP error: {e.response.status_code} — {e.response.text}")
            sys.exit(1)


if __name__ == "__main__":
    main()