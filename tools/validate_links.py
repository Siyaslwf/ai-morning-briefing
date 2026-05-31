"""
Validates all URLs in a research or content dict.
Broken URLs are replaced with the site's homepage (e.g. https://openai.com/blog/x -> https://openai.com).
Checks run in parallel with a per-URL timeout and a hard overall cap so a few
slow hosts can never sink the whole newsletter run.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests

PER_URL_TIMEOUT = 5     # seconds per request
MAX_TOTAL_WALL = 60     # seconds — give up validation entirely if exceeded
MAX_WORKERS = 12
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; newsletter-bot/1.0)"}


def _homepage(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _is_reachable(url: str) -> bool:
    try:
        r = requests.head(url, timeout=PER_URL_TIMEOUT, headers=HEADERS, allow_redirects=True)
        if r.status_code < 400:
            return True
    except Exception:
        pass
    try:
        r = requests.get(url, timeout=PER_URL_TIMEOUT, headers=HEADERS, stream=True)
        return r.status_code < 400
    except Exception:
        return False


def _collect_urls(data, out: list[str]) -> None:
    if isinstance(data, dict):
        for k, v in data.items():
            if k in ("url", "tool_url") and isinstance(v, str) and v.startswith("http"):
                out.append(v)
            else:
                _collect_urls(v, out)
    elif isinstance(data, list):
        for item in data:
            _collect_urls(item, out)


def _rewrite(data, mapping: dict):
    if isinstance(data, dict):
        return {
            k: (mapping.get(v, v) if k in ("url", "tool_url") and isinstance(v, str) else _rewrite(v, mapping))
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [_rewrite(item, mapping) for item in data]
    return data


def validate_links(data: dict) -> dict:
    """Validate every 'url' / 'tool_url' field in parallel; substitute homepage for broken links."""
    urls: list[str] = []
    _collect_urls(data, urls)
    unique = list(dict.fromkeys(urls))
    if not unique:
        return data

    mapping: dict[str, str] = {u: u for u in unique}
    print(f"[links] Checking {len(unique)} URL(s) in parallel...")

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            future_to_url = {pool.submit(_is_reachable, u): u for u in unique}
            for fut in as_completed(future_to_url, timeout=MAX_TOTAL_WALL):
                url = future_to_url[fut]
                try:
                    ok = fut.result()
                except Exception:
                    ok = False
                if not ok:
                    home = _homepage(url)
                    mapping[url] = home
                    print(f"[links] Broken: {url} -> using homepage: {home}")
    except Exception as exc:
        # TimeoutError or anything else: skip validation, keep URLs as-is.
        # Better to ship the newsletter than to block on a slow host.
        print(f"[links] Validation aborted ({type(exc).__name__}: {exc}); keeping URLs as-is.")
        return data

    return _rewrite(data, mapping)


if __name__ == "__main__":
    test = {
        "tools_spotlight": {"url": "https://openai.com/blog/this-does-not-exist-12345"},
        "resources": [{"url": "https://github.com"}, {"url": "https://fake-domain-xyz-999.com/article"}],
    }
    result = validate_links(test)
    import json
    print(json.dumps(result, indent=2))
