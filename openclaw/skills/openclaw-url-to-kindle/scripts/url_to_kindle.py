"""End-to-end URL -> markdown -> Google Doc -> EPUB -> Kindle email delivery pipeline.

This script ALWAYS sends the EPUB to Kindle email. There is no "skip send" option.
The only user input required is the Kindle email address.

Pipeline stages:
1. Fetch markdown from URL
2. Save markdown locally
3. Sync markdown to Google Drive as Google Doc (in 'kindle' folder)
4. Generate EPUB from markdown
5. Send EPUB to Kindle email via gog
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from drive_sync import sync_to_drive, EXIT_FOLDER_NOT_FOUND, EXIT_DOC_IMPORT_FAILED
from epub_generator import render_book
from send_to_kindle import (
    EXIT_GOG_NOT_FOUND,
    EXIT_EMAIL_MISSING,
    check_gog_available,
    run_delivery,
)
from url_to_markdown import derive_title, fetch_markdown, derive_title_from_body


# Exit codes (extending send_to_kindle and drive_sync)
EXIT_URL_FETCH_FAILED = 1
EXIT_EPUB_GENERATION_FAILED = 5


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9\s-]", "", value).strip().lower()
    value = re.sub(r"[\s_-]+", "-", value)
    return value or "article"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a URL to EPUB and send it to Kindle email",
        epilog="Requires 'gog' CLI to be installed for email sending."
    )
    parser.add_argument("url", help="Public article URL to convert")
    parser.add_argument(
        "--kindle-email",
        required=True,
        help="Kindle email address (e.g., user@kindle.com)"
    )
    parser.add_argument("--title", help="Override detected title")
    parser.add_argument("--author", default="OpenClaw", help="Author name (default: OpenClaw)")
    parser.add_argument("--output-dir", default="output", help="Output directory (default: ./output)")
    parser.add_argument("--timeout", type=int, default=30, help="URL fetch timeout in seconds")
    args = parser.parse_args()

    # Validate gog is available BEFORE doing any work
    if not check_gog_available():
        print(
            "ERROR: 'gog' CLI is not installed or not in PATH.\n"
            "This skill requires 'gog' to send emails to Kindle.\n"
            "Please install gog and ensure it's configured for email sending.",
            file=sys.stderr,
        )
        return EXIT_GOG_NOT_FOUND

    # Validate email is provided
    if not args.kindle_email:
        print(
            "ERROR: Kindle email address is required.\n"
            "Use --kindle-email to provide your Kindle email.",
            file=sys.stderr,
        )
        return EXIT_EMAIL_MISSING

    # Fetch markdown from URL
    try:
        markdown = fetch_markdown(args.url, timeout=args.timeout)
    except Exception as exc:
        print(f"ERROR: Failed to fetch URL: {exc}", file=sys.stderr)
        return EXIT_URL_FETCH_FAILED

    # Derive title and prepare output paths
    title = args.title or derive_title(markdown) or ""
    generic_titles = {"x", "twitter", "untitled", "article"}
    if (not title) or (title.strip().lower() in generic_titles):
        fallback = derive_title_from_body(markdown)
        if fallback:
            title = fallback
    if not title:
        title = args.url
    slug = slugify(title)
    output_dir = Path(args.output_dir)
    markdown_path = output_dir / f"{slug}.md"
    epub_path = output_dir / f"{slug}.epub"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save markdown
    markdown_path.write_text(markdown, encoding="utf-8")
    print(f"Saved markdown: {markdown_path}", file=sys.stderr)

    # Sync to Google Drive as Google Doc (in 'kindle' folder)
    drive_result, doc_id = sync_to_drive(markdown_path, title)
    drive_synced = drive_result == 0
    if not drive_synced:
        print(json.dumps({
            "status": "partial",
            "error": "drive_sync_failed",
            "markdown_path": str(markdown_path),
            "drive_exit_code": drive_result,
            "message": "Markdown saved locally but Google Drive sync failed. Continuing with EPUB generation.",
        }, ensure_ascii=True), file=sys.stderr)
        # Continue with EPUB generation even if Drive sync fails
        # The local markdown is still available

    # Generate EPUB
    try:
        render_book(markdown, str(epub_path), title=title, author=args.author)
        print(f"Generated EPUB: {epub_path}", file=sys.stderr)
    except Exception as exc:
        print(f"ERROR: Failed to generate EPUB: {exc}", file=sys.stderr)
        return EXIT_EPUB_GENERATION_FAILED

    # Send to Kindle email (ALWAYS, not optional)
    send_result = run_delivery(epub_path, args.kindle_email, title)
    
    if send_result != 0:
        print(json.dumps({
            "status": "partial",
            "error": "delivery_failed",
            "markdown_path": str(markdown_path),
            "epub_path": str(epub_path),
            "send_exit_code": send_result,
        }, ensure_ascii=True))
        return send_result

    print(json.dumps({
        "status": "success",
        "markdown_path": str(markdown_path),
        "epub_path": str(epub_path),
        "kindle_email": args.kindle_email,
        "google_doc_synced": drive_synced,
        "google_doc_id": doc_id,
    }, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Pipeline failed: {exc}", file=sys.stderr)
        raise
