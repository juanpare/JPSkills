"""Dispatch an EPUB file to Kindle via email using the gog CLI."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


# Exit codes
EXIT_GOG_NOT_FOUND = 3
EXIT_EMAIL_MISSING = 4
EXIT_EPUB_NOT_FOUND = 1
EXIT_SEND_FAILED = 6


def check_gog_available() -> bool:
    """Check if gog CLI is installed and available in PATH."""
    return shutil.which("gog") is not None


def run_delivery(epub_path: Path, kindle_email: str, title: str) -> int:
    """Send EPUB to Kindle email using gog CLI.
    
    Args:
        epub_path: Path to the EPUB file
        kindle_email: The Kindle email address
        title: Article title (for logging)
    
    Returns:
        Exit code (0 = success)
    """
    # Validate gog is available
    if not check_gog_available():
        print(
            "ERROR: 'gog' CLI is not installed or not in PATH.\n"
            "This skill requires 'gog' to send emails to Kindle.\n"
            "Please install gog and ensure it's configured for email sending.",
            file=sys.stderr,
        )
        return EXIT_GOG_NOT_FOUND

    # Validate email is provided
    if not kindle_email:
        print(
            "ERROR: Kindle email address is required.\n"
            "Please provide your Kindle email with --kindle-email option.",
            file=sys.stderr,
        )
        return EXIT_EMAIL_MISSING

    # Validate EPUB exists
    if not epub_path.exists():
        print(f"ERROR: EPUB file not found: {epub_path}", file=sys.stderr)
        return EXIT_EPUB_NOT_FOUND

    # Build and execute gog command
    # gog gmail send --to email --attach file.epub
    command = ["gog"]
    account = os.environ.get("GOG_ACCOUNT")
    if account:
        command += ["-a", account]
    subject = f"Kindle: {title}" if title else "Kindle Delivery"
    body = "Sent by OpenClaw"
    command += [
        "gmail", "send",
        "--to", kindle_email,
        "--subject", subject,
        "--body", body,
        "--attach", str(epub_path),
    ]
    
    print(f"Sending '{title}' to {kindle_email}...", file=sys.stderr)
    
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        
        if completed.returncode != 0:
            print(f"ERROR: gog send failed with exit code {completed.returncode}", file=sys.stderr)
            if completed.stderr:
                print(f"gog stderr: {completed.stderr}", file=sys.stderr)
            return EXIT_SEND_FAILED
        
        print(f"Successfully sent to {kindle_email}", file=sys.stderr)
        if completed.stdout:
            print(completed.stdout)
        
        return 0
        
    except Exception as exc:
        print(f"ERROR: Failed to execute gog: {exc}", file=sys.stderr)
        return EXIT_SEND_FAILED


def main() -> int:
    parser = argparse.ArgumentParser(description="Send an EPUB to Kindle via email using gog")
    parser.add_argument("epub_path", help="Path to the EPUB file")
    parser.add_argument("--kindle-email", required=True, help="Kindle email address")
    parser.add_argument("--title", default="OpenClaw Article", help="Article title for logging")
    args = parser.parse_args()

    epub_path = Path(args.epub_path)
    return run_delivery(epub_path, args.kindle_email, args.title)


if __name__ == "__main__":
    raise SystemExit(main())
