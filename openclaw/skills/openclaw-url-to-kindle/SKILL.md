---
name: openclaw-url-to-kindle
description: >
  Convert a public article URL into markdown, sync to Google Drive as Doc, build an EPUB, and send it to Kindle via email.
  Trigger: When the user wants to process a blog post, news article, or public X/article link into EPUB and deliver it to Kindle email.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "3.0"
---

## Prerequisites

- **`gog` CLI must be installed and configured** on the system. This skill uses `gog` for:
  - Google Drive operations (create folders, list folders)
  - Google Docs import (markdown → Google Doc)
  - Gmail sending (EPUB to Kindle email)
- If `gog` is not available, the skill will fail with a clear error message and will NOT attempt to configure it.

## When to Use

- User gives you a public URL and wants Kindle delivery via email
- User has `gog` installed and configured for Drive, Docs, and email sending
- Workflow is server-side and CLI-friendly
- User wants articles archived in Google Drive for later reference

## Critical Patterns

- Treat the workflow as 5 explicit stages: fetch, normalize, sync, generate, deliver
- Use `https://r.jina.ai/http://{url}` to obtain markdown-like article content from public pages
- Keep all intermediate artifacts on disk so the workflow is auditable on a VPS
- **Google Drive sync** creates/uses a `kindle` folder and imports markdown as Google Docs
- **Email delivery is MANDATORY** — the skill always sends to Kindle email, there is no "skip send" option
- The ONLY thing you need to ask the user is their Kindle email address

## Inputs

| Input | Required | Notes |
|------|----------|-------|
| `url` | Yes | Public article, blog, news, or readable public X URL |
| `kindle_email` | Yes | The Kindle email address (e.g., `user@kindle.com`) |
| `title` | No | Overrides detected title |
| `author` | No | Defaults to `OpenClaw` |
| `output_dir` | No | Defaults to `./output` |

## Workflow

1. Validate that `gog` is available on the system
2. Fetch markdown from the URL reader endpoint
3. Save the normalized markdown to disk
4. **Sync markdown to Google Drive**: create/reuse `kindle` folder, import as Google Doc
5. Convert markdown to EPUB with the bundled Python scripts
6. Send the EPUB to the Kindle email via `gog`

## Output JSON

On success, the script outputs:

```json
{
  "status": "success",
  "markdown_path": "./output/article-slug.md",
  "epub_path": "./output/article-slug.epub",
  "kindle_email": "user@kindle.com",
  "google_doc_synced": true,
  "google_doc_id": "1abc123xyz..."
}
```

## Commands

```bash
# Install dependencies
python3 -m pip install -r openclaw/skills/openclaw-url-to-kindle/requirements.txt

# Basic usage (only URL and Kindle email required)
python3 openclaw/skills/openclaw-url-to-kindle/scripts/url_to_kindle.py \
  "https://example.com/post" \
  --kindle-email "user@kindle.com"

# With custom title and author
python3 openclaw/skills/openclaw-url-to-kindle/scripts/url_to_kindle.py \
  "https://example.com/post" \
  --kindle-email "user@kindle.com" \
  --title "My Article" \
  --author "John Doe"
```

## Error Handling

| Exit Code | Error | Description |
|-----------|-------|-------------|
| 1 | URL fetch failed | Could not fetch or parse the URL |
| 3 | gog not found | `gog` CLI is not installed or not in PATH |
| 4 | Email missing | Kindle email address was not provided |
| 5 | EPUB generation failed | Could not generate EPUB from markdown |
| 6 | Send failed | `gog send` command failed |
| 7 | Drive error | General Google Drive operation error |
| 8 | Folder not found | Could not create or locate `kindle` folder |
| 9 | Doc import failed | Could not import markdown as Google Doc |

## gog CLI Assumptions

This skill assumes the following `gog` CLI syntax (based on documented capabilities):

```bash
# List folders
gog drive list --name "kindle" --type folder --max 1

# Create folder
gog drive mkdir --name "kindle"

# Import markdown as Google Doc
gog docs import --title "Article Title" --parent "folder_id" --format markdown file.md

# Send email with attachment
gog send --to user@kindle.com file.epub
```

If the actual `gog` CLI syntax differs, error messages will include the command that failed for easier debugging.

## Resources

- See `resources/sample-article.md` for a minimal markdown input example
- See `scripts/` for the reusable URL, Drive, EPUB, and delivery pipeline pieces
