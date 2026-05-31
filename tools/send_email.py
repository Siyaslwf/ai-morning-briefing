"""
Sends the newsletter HTML via Gmail SMTP.
Includes a plain-text fallback auto-derived from the content dict.
"""

import os
import smtplib
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")


def _build_plain_text(content: dict) -> str:
    lines = [
        f"THE AI BRIEFING — Issue #{content.get('issue_number')} — {content.get('date')}",
        f"Topic: {content.get('topic')}",
        "=" * 60,
        "",
        content.get("headline", ""),
        "",
        content.get("hook", ""),
        "",
        "KEY INSIGHTS",
        "-" * 40,
    ]
    for item in content.get("key_insights", []):
        lines.append(f"{item['number']}. {item['title']}: {item['body']}")
    lines += [
        "",
        "DEEP DIVE",
        "-" * 40,
    ]
    for para in content.get("deep_dive", []):
        lines.append(para)
        lines.append("")
    spotlight = content.get("tools_spotlight", {})
    lines += [
        "TOOL SPOTLIGHT",
        "-" * 40,
        f"{spotlight.get('name', '')} — {spotlight.get('tagline', '')}",
        spotlight.get("why_it_matters", ""),
        spotlight.get("url", ""),
        "",
        "QUICK BITES",
        "-" * 40,
    ]
    for bite in content.get("quick_bites", []):
        lines.append(f"[{bite['tag']}] {bite['title']}: {bite['summary']} {bite['url']}")
    lines += [
        "",
        "WORTH READING",
        "-" * 40,
    ]
    for r in content.get("resources", []):
        lines.append(f"• {r['title']}: {r['description']} {r['url']}")
    lines += [
        "",
        "-" * 60,
        content.get("cta", ""),
        "",
        "The AI Briefing",
        f"Reply to: {GMAIL_ADDRESS}",
    ]
    return "\n".join(lines)


def send_email(
    html: str,
    content: dict,
    recipients: list[str],
) -> dict:
    """
    html:       Rendered HTML string
    content:    Content dict (used for subject + plain text)
    recipients: List of email addresses
    Returns:    {'success': bool, 'sent_to': list, 'error': str|None}
    """
    if not GMAIL_ADDRESS:
        return {"success": False, "sent_to": [], "error": "GMAIL_ADDRESS not set in .env"}
    if not GMAIL_APP_PASSWORD:
        return {"success": False, "sent_to": [], "error": "GMAIL_APP_PASSWORD not set in .env"}
    if not recipients:
        return {"success": False, "sent_to": [], "error": "No recipients provided"}

    subject = content.get("subject_line", f"The AI Briefing — Issue #{content.get('issue_number')}")
    plain_text = _build_plain_text(content)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"The AI Briefing <{GMAIL_ADDRESS}>"
    msg["To"] = ", ".join(recipients)

    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    # Retry on transient SMTP errors (network blips, Gmail server flaps).
    # Auth errors are NOT retried — the credentials are wrong, retrying won't help.
    last_error: str | None = None
    for attempt in range(3):
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
                server.sendmail(GMAIL_ADDRESS, recipients, msg.as_string())

            print(f"[email] Sent to {len(recipients)} recipient(s): {', '.join(recipients)}")
            return {"success": True, "sent_to": recipients, "error": None}

        except smtplib.SMTPAuthenticationError:
            error = (
                "Gmail authentication failed. Make sure you're using an App Password "
                "(not your account password). Generate one at: "
                "myaccount.google.com/apppasswords"
            )
            print(f"[email] ERROR (no retry): {error}")
            return {"success": False, "sent_to": [], "error": error}

        except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError,
                smtplib.SMTPHeloError, TimeoutError, OSError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            wait = 5 * (attempt + 1)
            print(f"[email] Transient error (attempt {attempt+1}/3): {last_error} — retrying in {wait}s")
            time.sleep(wait)

        except Exception as exc:
            last_error = str(exc)
            print(f"[email] ERROR: {last_error}")
            return {"success": False, "sent_to": [], "error": last_error}

    return {"success": False, "sent_to": [], "error": f"SMTP failed after 3 attempts: {last_error}"}


if __name__ == "__main__":
    # Test: print the plain text version
    sample = {
        "issue_number": 1,
        "date": "May 24, 2026",
        "topic": "Agentic AI",
        "headline": "AI Agents Are Rewriting the Rules of Work",
        "hook": "Three months ago, agentic AI was a demo.",
        "key_insights": [{"number": 1, "title": "Adoption surge", "body": "Tripled in Q1."}],
        "deep_dive": ["Paragraph one.", "Paragraph two."],
        "tools_spotlight": {"name": "AutoGen 2.0", "tagline": "Multi-agent framework", "why_it_matters": "Best in class.", "url": "https://example.com"},
        "quick_bites": [{"tag": "Research", "title": "Test", "summary": "Summary.", "url": "https://example.com"}],
        "resources": [{"title": "Test", "description": "Why read.", "url": "https://example.com"}],
        "cta": "Hit reply with your thoughts.",
        "subject_line": "AI agents are in production. Now what?",
    }
    print(_build_plain_text(sample))
