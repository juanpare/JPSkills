"""Sync markdown to Google Drive as a Google Doc using the gog CLI.

This module creates/ensures a 'kindle' folder exists in Google Drive and
imports markdown files as Google Docs.

ASSUMPTIONS about gog CLI syntax (not yet verified on system):
- gog drive mkdir --name "folder" → creates folder, returns ID
- gog drive list --name "folder" → lists folders matching name
- gog docs import --title "Title" --parent "folder_id" file.md → creates Doc from markdown

If these assumptions are incorrect, the error messages will indicate the actual
gog output for easier debugging.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple


# Exit codes
EXIT_DRIVE_ERROR = 7
EXIT_FOLDER_NOT_FOUND = 8
EXIT_DOC_IMPORT_FAILED = 9

KINDLE_FOLDER_NAME = "kindle"


def run_gog_command(args: list[str], capture_output: bool = True) -> Tuple[int, str, str]:
    """Run a gog command and return (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["gog"] + args,
            capture_output=capture_output,
            text=True,
            timeout=60,
        )
        return result.returncode, result.stdout or "", result.stderr or ""
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out after 60 seconds"
    except FileNotFoundError:
        return -2, "", "gog CLI not found in PATH"
    except Exception as exc:
        return -3, "", str(exc)


def find_kindle_folder() -> Optional[str]:
    """Find the 'kindle' folder in Google Drive root.
    
    Returns:
        Folder ID if found, None otherwise.
    """
    # ASSUMPTION: gog drive list --name "folder" returns JSON with folder info
    exit_code, stdout, stderr = run_gog_command([
        "drive", "list",
        "--name", KINDLE_FOLDER_NAME,
        "--type", "folder",
        "--max", "1",
    ])
    
    if exit_code != 0:
        print(f"Warning: Could not list Drive folders: {stderr}", file=__import__("sys").stderr)
        return None
    
    # Try to parse folder ID from output
    # ASSUMPTION: Output is JSON with "id" field, or line with "id: xxx"
    try:
        # Try JSON first
        data = json.loads(stdout)
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("id")
        if isinstance(data, dict):
            return data.get("id")
    except json.JSONDecodeError:
        pass
    
    # Try line-based format: "id: xxx" or "ID: xxx"
    match = re.search(r"(?i)(?:id|folder[_-]?id)[:\s]+([a-zA-Z0-9_-]+)", stdout)
    if match:
        return match.group(1)
    
    return None


def create_kindle_folder() -> Optional[str]:
    """Create the 'kindle' folder in Google Drive root.
    
    Returns:
        Folder ID if created successfully, None otherwise.
    """
    # ASSUMPTION: gog drive mkdir --name "folder" creates folder and returns ID
    exit_code, stdout, stderr = run_gog_command([
        "drive", "mkdir",
        "--name", KINDLE_FOLDER_NAME,
    ])
    
    if exit_code != 0:
        print(f"ERROR: Failed to create '{KINDLE_FOLDER_NAME}' folder: {stderr}", file=__import__("sys").stderr)
        return None
    
    # Try to parse folder ID from output
    try:
        data = json.loads(stdout)
        if isinstance(data, dict):
            return data.get("id")
    except json.JSONDecodeError:
        pass
    
    # Try line-based format
    match = re.search(r"(?i)(?:id|folder[_-]?id)[:\s]+([a-zA-Z0-9_-]+)", stdout)
    if match:
        return match.group(1)
    
    # If we can't parse the ID but command succeeded, assume it worked
    # and return None (we'll try to find it next time)
    print(f"Warning: Could not parse folder ID from output: {stdout[:200]}", file=__import__("sys").stderr)
    return None


def get_or_create_kindle_folder() -> Tuple[int, Optional[str]]:
    """Ensure the 'kindle' folder exists in Google Drive.
    
    Returns:
        (exit_code, folder_id) - exit_code 0 on success, folder_id may be None
        if we created but couldn't parse the ID.
    """
    # Try to find existing folder first
    folder_id = find_kindle_folder()
    if folder_id:
        print(f"Found existing '{KINDLE_FOLDER_NAME}' folder: {folder_id}", file=__import__("sys").stderr)
        return 0, folder_id
    
    # Create new folder
    print(f"Creating '{KINDLE_FOLDER_NAME}' folder in Google Drive...", file=__import__("sys").stderr)
    folder_id = create_kindle_folder()
    
    if folder_id:
        print(f"Created '{KINDLE_FOLDER_NAME}' folder: {folder_id}", file=__import__("sys").stderr)
        return 0, folder_id
    
    # Folder was created but we couldn't parse ID - try to find it again
    folder_id = find_kindle_folder()
    if folder_id:
        print(f"Found newly created '{KINDLE_FOLDER_NAME}' folder: {folder_id}", file=__import__("sys").stderr)
        return 0, folder_id
    
    # Complete failure
    print(f"ERROR: Could not create or locate '{KINDLE_FOLDER_NAME}' folder", file=__import__("sys").stderr)
    return EXIT_FOLDER_NOT_FOUND, None


def import_markdown_as_doc(
    markdown_path: Path,
    title: str,
    folder_id: Optional[str] = None,
) -> Tuple[int, Optional[str]]:
    """Import a markdown file as a Google Doc.
    
    Args:
        markdown_path: Path to the markdown file
        title: Title for the Google Doc
        folder_id: Optional parent folder ID (if None, creates in root)
    
    Returns:
        (exit_code, doc_id) - exit_code 0 on success
    """
    if not markdown_path.exists():
        print(f"ERROR: Markdown file not found: {markdown_path}", file=__import__("sys").stderr)
        return EXIT_DOC_IMPORT_FAILED, None
    
    # Build command
    # ASSUMPTION: gog docs import --title "Title" [--parent "folder_id"] file.md
    args = [
        "docs", "import",
        "--title", title,
        "--format", "markdown",
    ]
    
    if folder_id:
        args.extend(["--parent", folder_id])
    
    args.append(str(markdown_path))
    
    print(f"Importing '{title}' as Google Doc...", file=__import__("sys").stderr)
    exit_code, stdout, stderr = run_gog_command(args)
    
    if exit_code != 0:
        print(f"ERROR: Failed to import markdown as Google Doc: {stderr}", file=__import__("sys").stderr)
        print(f"gog command: gog {' '.join(args)}", file=__import__("sys").stderr)
        return EXIT_DOC_IMPORT_FAILED, None
    
    # Try to parse doc ID from output
    doc_id = None
    try:
        data = json.loads(stdout)
        if isinstance(data, dict):
            doc_id = data.get("id") or data.get("docId")
    except json.JSONDecodeError:
        pass
    
    if not doc_id:
        match = re.search(r"(?i)(?:id|doc[_-]?id)[:\s]+([a-zA-Z0-9_-]+)", stdout)
        if match:
            doc_id = match.group(1)
    
    if doc_id:
        print(f"Created Google Doc: {doc_id}", file=__import__("sys").stderr)
    else:
        print(f"Warning: Could not parse Doc ID from output: {stdout[:200]}", file=__import__("sys").stderr)
    
    return 0, doc_id


def sync_to_drive(markdown_path: Path, title: str) -> Tuple[int, Optional[str]]:
    """Full sync: ensure folder exists, import markdown as Doc.
    
    Args:
        markdown_path: Path to the markdown file
        title: Title for the Google Doc
    
    Returns:
        (exit_code, doc_id) - exit_code 0 on success, doc_id may be None
        even on success if we couldn't parse it from output
    """
    # Ensure kindle folder exists
    folder_result, folder_id = get_or_create_kindle_folder()
    if folder_result != 0:
        return folder_result, None
    
    # Import markdown as Doc
    doc_result, doc_id = import_markdown_as_doc(markdown_path, title, folder_id)
    
    return doc_result, doc_id


if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Sync markdown to Google Drive as Google Doc")
    parser.add_argument("markdown_path", help="Path to markdown file")
    parser.add_argument("--title", help="Title for the Google Doc (default: derived from filename)")
    args = parser.parse_args()
    
    path = Path(args.markdown_path)
    title = args.title or path.stem
    
    exit_code, doc_id = sync_to_drive(path, title)
    if exit_code == 0 and doc_id:
        print(json.dumps({"status": "success", "doc_id": doc_id}))
    elif exit_code == 0:
        print(json.dumps({"status": "success", "doc_id": None, "warning": "Doc created but ID could not be parsed"}))
    else:
        print(json.dumps({"status": "error", "exit_code": exit_code}))
    raise SystemExit(exit_code)
