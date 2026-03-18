"""Fetch a public URL and store a markdown representation on disk."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional


USER_AGENT = "OpenClaw-URL-To-Kindle/1.0"


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        return f"https://{url}"
    return url


def build_reader_url(url: str) -> str:
    normalized = normalize_url(url)
    stripped = re.sub(r"^https?://", "", normalized, flags=re.IGNORECASE)
    return f"https://r.jina.ai/http://{stripped}"


def fetch_markdown(url: str, timeout: int = 30) -> str:
    reader_url = build_reader_url(url)
    request = urllib.request.Request(
        reader_url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/plain, text/markdown;q=0.9, */*;q=0.1"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read().decode("utf-8", errors="replace")
    return cleanup_markdown(payload, normalize_url(url))


def cleanup_markdown(markdown: str, source_url: str) -> str:
    text = markdown.replace("\r\n", "\n").strip()
    text = re.sub(r"\n{3,}", "\n\n", text)

    if not re.search(r"^#\s+", text, flags=re.MULTILINE):
        title = derive_title(text) or source_url
        text = f"# {title}\n\n{text}"

    if source_url not in text:
        text = f"> Source: {source_url}\n\n{text}"

    return text.rstrip() + "\n"


def derive_title(markdown: str) -> Optional[str]:
    for pattern in (r"^#\s+(.+)$", r"^Title:\s+(.+)$"):
        match = re.search(pattern, markdown, flags=re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9\s-]", "", value).strip().lower()
    value = re.sub(r"[\s_-]+", "-", value)
    return value or "article"


def write_output(markdown: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a URL as markdown")
    parser.add_argument("url")
    parser.add_argument("--output", help="Output markdown file path")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--print-metadata", action="store_true")
    args = parser.parse_args()

    try:
        markdown = fetch_markdown(args.url, timeout=args.timeout)
    except urllib.error.HTTPError as exc:
        print(f"HTTP error fetching URL: {exc.code} {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Network error fetching URL: {exc.reason}", file=sys.stderr)
        return 1

    title = derive_title(markdown) or normalize_url(args.url)
    slug = slugify(title)
    output_path = Path(args.output) if args.output else Path("output") / f"{slug}.md"
    write_output(markdown, output_path)

    if args.print_metadata:
        print(json.dumps({"title": title, "output": str(output_path)}, ensure_ascii=True))
    else:
        print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
