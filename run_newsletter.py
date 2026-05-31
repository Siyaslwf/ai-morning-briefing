"""
Newsletter automation orchestrator.

Usage:
  python run_newsletter.py --topic "Agentic AI in 2026"
  python run_newsletter.py --topic "LLM fine-tuning" --recipients "you@example.com,friend@example.com"
  python run_newsletter.py --topic "OpenAI GPT-5" --dry-run

Options:
  --topic       Topic/theme for this newsletter edition (required)
  --recipients  Comma-separated email addresses (overrides .env NEWSLETTER_RECIPIENTS)
  --dry-run     Generate and save HTML but do NOT send the email
  --issue       Override the issue number (defaults to NEWSLETTER_ISSUE_NUMBER in .env)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv, set_key

load_dotenv()

# ── Tool imports ──────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from tools.research_topic import research_topic
from tools.validate_links import validate_links
from tools.generate_content import generate_content
from tools.generate_infographic import generate_infographic
from tools.generate_html import generate_html
from tools.send_email import send_email
from tools.beehiiv_publish import publish_to_beehiiv

ENV_PATH = Path(__file__).parent / ".env"
TMP_DIR  = Path(__file__).parent / ".tmp"


def log(step: str, msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{step.upper()}] {msg}", flush=True)


REQUIRED_SECRETS = ("OPENROUTER_API_KEY", "GMAIL_ADDRESS", "GMAIL_APP_PASSWORD")


def _preflight(dry_run: bool, recipients: list[str]) -> None:
    """Fail fast with a clear message if anything required is missing."""
    missing = [k for k in REQUIRED_SECRETS if not os.getenv(k)]
    if not dry_run and not recipients:
        missing.append("NEWSLETTER_RECIPIENTS (or --recipients)")
    if missing:
        print("ERROR: Missing required configuration:", file=sys.stderr)
        for k in missing:
            print(f"  - {k}", file=sys.stderr)
        print(
            "\nFor GitHub Actions: set these as repository secrets at "
            "Settings -> Secrets and variables -> Actions.",
            file=sys.stderr,
        )
        sys.exit(2)


def run(topic: str, recipients: list[str], dry_run: bool, issue_number: int) -> None:
    _preflight(dry_run, recipients)
    date = datetime.now().strftime("%B %d, %Y")
    print()
    print("=" * 60)
    print(f"  THE AI BRIEFING — Issue #{issue_number}")
    print(f"  Topic: {topic}")
    print(f"  Date:  {date}")
    print(f"  Mode:  {'DRY RUN (no email)' if dry_run else 'LIVE SEND'}")
    print(f"  To:    {', '.join(recipients) if recipients else '(none — dry run)'}")
    print("=" * 60)
    print()

    # ── Step 1: Research ──────────────────────────────────────────────────────
    log("1/5", "Researching topic via OpenRouter free models...")
    t0 = time.time()
    try:
        research = research_topic(topic)
    except Exception as exc:
        import traceback
        log("ERROR", f"Research failed: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        sys.exit(1)
    log("1/5", f"Research complete ({time.time()-t0:.1f}s)")
    log("1/5", "Validating URLs in research...")
    research = validate_links(research)

    # ── Step 2: Generate content ──────────────────────────────────────────────
    log("2/5", "Writing newsletter copy via OpenRouter free models...")
    t0 = time.time()
    try:
        content = generate_content(research, issue_number=issue_number, date=date)
    except Exception as exc:
        import traceback
        log("ERROR", f"Content generation failed: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        # Save the research so we can debug from the artifact
        TMP_DIR.mkdir(exist_ok=True)
        (TMP_DIR / f"newsletter_FAILED_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html").write_text(
            f"<pre>Content generation failed.\nResearch was:\n{json.dumps(research, indent=2)}</pre>",
            encoding="utf-8",
        )
        sys.exit(1)
    log("2/5", f"Content written ({time.time()-t0:.1f}s) — headline: \"{content.get('headline')}\"")

    # ── Step 3: Generate infographic ──────────────────────────────────────────
    log("3/5", "Generating infographics (AI illustration + stat chart)...")
    t0 = time.time()
    try:
        images = generate_infographic(research)
    except Exception as exc:
        log("WARN", f"Infographic generation failed (continuing without images): {exc}")
        images = {"illustration_b64": None, "chart_b64": None}
    img_note = []
    if images.get("illustration_b64"):
        img_note.append("AI illustration")
    if images.get("chart_b64"):
        img_note.append("stat chart")
    log("3/5", f"Infographics done ({time.time()-t0:.1f}s) — {', '.join(img_note) or 'none generated'}")

    # ── Step 4: Render HTML ───────────────────────────────────────────────────
    log("4/5", "Rendering HTML email template...")
    t0 = time.time()
    try:
        html = generate_html(content, images)
    except Exception as exc:
        log("ERROR", f"HTML rendering failed: {exc}")
        sys.exit(1)
    log("4/5", f"HTML rendered ({time.time()-t0:.1f}s) — {len(html):,} chars")

    # ── Save preview file ─────────────────────────────────────────────────────
    TMP_DIR.mkdir(exist_ok=True)
    preview_path = TMP_DIR / f"newsletter_issue{issue_number}_{datetime.now().strftime('%Y%m%d')}.html"
    preview_path.write_text(html, encoding="utf-8")
    print()
    print(f"  Preview saved: .tmp/{preview_path.name}")
    print(f"  Open in browser to review before sending.")
    print()

    # ── Step 5: Send ──────────────────────────────────────────────────────────
    if dry_run:
        log("5/5", "DRY RUN — email NOT sent. Remove --dry-run to send.")
        print()
        print("Done.")
        return

    if not recipients:
        log("ERROR", "No recipients specified. Use --recipients or set NEWSLETTER_RECIPIENTS in .env")
        sys.exit(1)

    log("5/5", f"Sending via Gmail SMTP to {len(recipients)} recipient(s)...")
    t0 = time.time()
    result = send_email(html, content, recipients)

    if result["success"]:
        log("5/5", f"Email sent ({time.time()-t0:.1f}s)")

        # Auto-increment issue number in .env
        next_issue = issue_number + 1
        set_key(str(ENV_PATH), "NEWSLETTER_ISSUE_NUMBER", str(next_issue))
        print()
        print(f"  Issue #{issue_number} sent successfully.")
        print(f"  Next issue number: #{next_issue} (updated in .env)")
    else:
        log("ERROR", f"Send failed: {result['error']}")
        sys.exit(1)

    # ── Step 6 (optional): Publish to Beehiiv ─────────────────────────────────
    if os.getenv("BEEHIIV_API_KEY") and os.getenv("BEEHIIV_PUBLICATION_ID"):
        log("6/6", "Publishing to Beehiiv public newsletter...")
        t0 = time.time()
        bh_send = os.getenv("BEEHIIV_SEND_LIVE", "false").lower() == "true"
        bh = publish_to_beehiiv(html, content, send=bh_send)
        if bh["success"]:
            mode = "SENT to subscribers" if bh_send else "saved as DRAFT"
            log("6/6", f"Beehiiv {mode} ({time.time()-t0:.1f}s)")
            if bh.get("web_url"):
                print(f"  Public URL: {bh['web_url']}")
        else:
            log("WARN", f"Beehiiv publish failed (non-blocking): {bh['error']}")
    else:
        log("6/6", "Beehiiv not configured (set BEEHIIV_API_KEY + BEEHIIV_PUBLICATION_ID to enable)")

    print()
    print("Done.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the newsletter automation pipeline")
    parser.add_argument("--topic",      required=True, help="Newsletter topic/theme")
    parser.add_argument("--recipients", default="",    help="Comma-separated recipient emails")
    parser.add_argument("--dry-run",    action="store_true", help="Generate but don't send")
    parser.add_argument("--issue",      type=int, default=None, help="Override issue number")
    args = parser.parse_args()

    # Resolve recipients
    recipients_raw = args.recipients or os.getenv("NEWSLETTER_RECIPIENTS", "")
    recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]

    # Resolve issue number
    if args.issue is not None:
        issue_number = args.issue
    else:
        try:
            issue_number = int(os.getenv("NEWSLETTER_ISSUE_NUMBER", "1"))
        except ValueError:
            issue_number = 1

    run(
        topic=args.topic,
        recipients=recipients,
        dry_run=args.dry_run,
        issue_number=issue_number,
    )


if __name__ == "__main__":
    main()
