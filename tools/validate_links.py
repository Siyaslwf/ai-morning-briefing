"""
Validates all URLs in a research or content dict.
Broken URLs are replaced with the site's homepage (e.g. https://openai.com/blog/x → https://openai.com).
Non-blocking: any URL that can't be reached within 5 seconds is considered broken.
"""

import re
from urllib.parse import urlparse

import requests

TIMEOUT = 5
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; newsletter-bot/1.0)"}


def _homepage(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _is_reachable(url: str) -> bool:
    try:
        r = requests.head(url, timeout=TIMEOUT, headers=HEADERS, allow_redirects=True)
        return r.status_code < 400
    except Exception:
        try:
            r = requests.get(url, timeout=TIMEOUT, headers=HEADERS, stream=True)
            return r.status_code < 400
        except Exception:
            return False


def _fix_url(url: str) -> str:
    """Return url if reachable, else the site homepage."""
    if not url or not url.startswith("http"):
        return url
    if _is_reachable(url):
        return url
    home = _homepage(url)
    print(f"[links] Broken: {url} → using homepage: {home}")
    return home


def validate_links(data: dict) -> dict:
    """
    Walk the research/content dict and validate every 'url' or 'tool_url' field.
    Returns the same dict with broken URLs replaced by their site's homepage.
    """
    if isinstance(data, dict):
        return {k: (_fix_url(v) if k in ("url", "tool_url") and isinstance(v, str) else validate_links(v))
                for k, v in data.items()}
    if isinstance(data, list):
        return [validate_links(item) for item in data]
    return data


if __name__ == "__main__":
    test = {
        "tools_spotlight": {"url": "https://openai.com/blog/this-does-not-exist-12345"},
        "resources": [{"url": "https://github.com"}, {"url": "https://fake-domain-xyz-999.com/article"}],
    }
    result = validate_links(test)
    import json
    print(json.dumps(result, indent=2))
