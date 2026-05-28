"""
Publish the rendered newsletter to a Beehiiv publication.

Beehiiv free tier: unlimited subscribers, web hosting, custom domain, paid subs.
Get an API key: https://app.beehiiv.com/settings/integrations/api
Get publication ID: https://app.beehiiv.com/settings (URL contains pub_xxx)

Env vars required:
  BEEHIIV_API_KEY        — API key from Beehiiv settings
  BEEHIIV_PUBLICATION_ID — your publication ID (starts with pub_)
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BEEHIIV_API_KEY = os.getenv("BEEHIIV_API_KEY", "")
BEEHIIV_PUBLICATION_ID = os.getenv("BEEHIIV_PUBLICATION_ID", "")
BEEHIIV_API_BASE = "https://api.beehiiv.com/v2"


def publish_to_beehiiv(
    html: str,
    content: dict,
    send: bool = True,
) -> dict:
    """
    Push the rendered newsletter to Beehiiv as a post.

    html:    Rendered HTML string
    content: Content dict (subject, preview, etc.)
    send:    If True, send to all subscribers immediately. If False, save as draft.

    Returns: {'success': bool, 'post_id': str|None, 'web_url': str|None, 'error': str|None}
    """
    if not BEEHIIV_API_KEY:
        return {"success": False, "post_id": None, "web_url": None,
                "error": "BEEHIIV_API_KEY not set in .env"}
    if not BEEHIIV_PUBLICATION_ID:
        return {"success": False, "post_id": None, "web_url": None,
                "error": "BEEHIIV_PUBLICATION_ID not set in .env"}

    subject = content.get("subject_line") or f"The AI Briefing — Issue #{content.get('issue_number')}"
    preview = content.get("preview_text") or content.get("hook", "")[:120]

    url = f"{BEEHIIV_API_BASE}/publications/{BEEHIIV_PUBLICATION_ID}/posts"
    headers = {
        "Authorization": f"Bearer {BEEHIIV_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "title": subject,
        "subtitle": preview,
        "body_content": html,
        "status": "confirmed" if send else "draft",
        "content_tags": ["ai", "newsletter", "daily-briefing"],
        "email_settings": {
            "email_subject_line": subject,
            "email_preview_text": preview,
        },
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code in (200, 201):
            data = resp.json().get("data", {})
            post_id = data.get("id")
            web_url = data.get("web_url") or data.get("url")
            print(f"[beehiiv] Published successfully — post_id={post_id}")
            if web_url:
                print(f"[beehiiv] Web URL: {web_url}")
            return {"success": True, "post_id": post_id, "web_url": web_url, "error": None}
        else:
            error = f"HTTP {resp.status_code}: {resp.text[:300]}"
            print(f"[beehiiv] ERROR: {error}")
            return {"success": False, "post_id": None, "web_url": None, "error": error}

    except requests.RequestException as exc:
        error = str(exc)
        print(f"[beehiiv] ERROR: {error}")
        return {"success": False, "post_id": None, "web_url": None, "error": error}


if __name__ == "__main__":
    sample_html = "<h1>Test</h1><p>Hello from the pipeline.</p>"
    sample_content = {
        "subject_line": "Test post from CLI",
        "preview_text": "This is a test draft.",
        "issue_number": 0,
        "hook": "Just a smoke test.",
    }
    result = publish_to_beehiiv(sample_html, sample_content, send=False)
    print(result)
