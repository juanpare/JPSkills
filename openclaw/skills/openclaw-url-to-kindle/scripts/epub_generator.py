"""EPUB generator adapted from smerchek/claude-epub-skill."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import List, Optional, cast

from ebooklib import epub

from markdown_processor import Chapter, EbookMetadata, MarkdownProcessor


DEFAULT_CSS = """
body { font-family: Georgia, serif; line-height: 1.5; margin: 0; padding: 1em; }
h1 { page-break-before: always; color: #1a1a1a; }
h2, h3, h4, h5, h6 { color: #2c3e50; }
p { margin: 0.75em 0; text-align: justify; }
a { color: #0b5fff; text-decoration: none; }
code { font-family: Courier New, monospace; background: #f5f5f5; padding: 0.1em 0.3em; }
blockquote { border-left: 3px solid #0b5fff; margin: 1em 0; padding-left: 1em; color: #555; }
ul { padding-left: 1.5em; }
"""


def render_book(markdown_content: str, output_path: str, title: Optional[str] = None, author: Optional[str] = None) -> str:
    processor = MarkdownProcessor()
    result = processor.process(markdown_content)
    metadata = cast(EbookMetadata, result["metadata"])
    if title:
        metadata.title = title
    if author:
        metadata.author = author

    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(metadata.title or "Untitled")
    book.set_language(metadata.language)
    book.add_author(metadata.author)

    style = epub.EpubItem(uid="style", file_name="style/main.css", media_type="text/css", content=DEFAULT_CSS)
    book.add_item(style)

    chapters = cast(List[Chapter], result["chapters"])
    html_items = []
    for index, chapter in enumerate(chapters, start=1):
        parts = [f'<h1 id="{chapter.anchor}">{chapter.title}</h1>']
        if chapter.content:
            parts.append(MarkdownProcessor.markdown_to_html(chapter.content))
        item = epub.EpubHtml(title=chapter.title, file_name=f"chap_{index:03d}.xhtml", lang=metadata.language)
        item.set_content("\n".join(parts))
        item.add_link(rel="stylesheet", href="style/main.css", type="text/css")
        book.add_item(item)
        html_items.append(item)

    book.toc = tuple(html_items)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", *html_items]

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(output), book, {})
    return str(output)
