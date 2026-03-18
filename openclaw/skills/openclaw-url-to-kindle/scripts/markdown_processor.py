"""Minimal markdown processor adapted for local EPUB generation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Section:
    title: str
    level: int
    content: str
    anchor: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.anchor:
            self.anchor = slugify(self.title)


@dataclass
class Chapter:
    title: str
    content: str
    sections: List[Section]
    anchor: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.anchor:
            self.anchor = slugify(self.title)


@dataclass
class EbookMetadata:
    title: Optional[str] = None
    author: str = "OpenClaw"
    language: str = "en"


def slugify(value: str) -> str:
    value = re.sub(r"[^\w\s-]", "", value.lower())
    value = re.sub(r"[-\s]+", "-", value).strip("-")
    return value or "section"


class MarkdownProcessor:
    def __init__(self) -> None:
        self.metadata = EbookMetadata()

    def process(self, markdown_content: str) -> Dict[str, object]:
        self._extract_metadata(markdown_content)
        chapters = self._parse_chapters(markdown_content)
        return {"chapters": chapters, "metadata": self.metadata}

    def _extract_metadata(self, content: str) -> None:
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            self.metadata.title = match.group(1).strip()

    def _parse_chapters(self, content: str) -> List[Chapter]:
        matches = list(re.finditer(r"^#\s+(.+)$", content, re.MULTILINE))
        if not matches:
            return [Chapter(title=self.metadata.title or "Untitled", content=content.strip(), sections=[])]

        chapters: List[Chapter] = []
        for index, match in enumerate(matches):
            title = match.group(1).strip()
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            body = content[start:end].strip()
            chapters.append(Chapter(title=title, content=body, sections=self._parse_sections(body)))
        return chapters

    def _parse_sections(self, content: str) -> List[Section]:
        matches = list(re.finditer(r"^(#{2,6})\s+(.+)$", content, re.MULTILINE))
        sections: List[Section] = []
        for index, match in enumerate(matches):
            level = len(match.group(1))
            title = match.group(2).strip()
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
            sections.append(Section(title=title, level=level, content=content[start:end].strip()))
        return sections

    @staticmethod
    def markdown_to_html(markdown_text: str) -> str:
        if not markdown_text.strip():
            return "<p></p>"

        lines = markdown_text.splitlines()
        html_parts: List[str] = []
        in_list = False
        paragraph: List[str] = []

        def flush_paragraph() -> None:
            nonlocal paragraph
            if paragraph:
                joined = " ".join(paragraph).strip()
                if joined:
                    html_parts.append(f"<p>{MarkdownProcessor.render_inline(joined)}</p>")
                paragraph = []

        def close_list() -> None:
            nonlocal in_list
            if in_list:
                html_parts.append("</ul>")
                in_list = False

        for line in lines:
            stripped = line.strip()
            if not stripped:
                flush_paragraph()
                close_list()
                continue

            if stripped.startswith("#"):
                flush_paragraph()
                close_list()
                level = len(stripped) - len(stripped.lstrip("#"))
                text = stripped[level:].strip()
                html_parts.append(f"<h{min(level, 6)}>{MarkdownProcessor.render_inline(text)}</h{min(level, 6)}>")
                continue

            if stripped.startswith(("- ", "* ")):
                flush_paragraph()
                if not in_list:
                    html_parts.append("<ul>")
                    in_list = True
                html_parts.append(f"<li>{MarkdownProcessor.render_inline(stripped[2:].strip())}</li>")
                continue

            close_list()
            paragraph.append(stripped)

        flush_paragraph()
        close_list()
        return "\n".join(html_parts)

    @staticmethod
    def render_inline(text: str) -> str:
        text = (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
        text = re.sub(r"\[(.+?)\]\((.+?)\)", r"<a href=\"\2\">\1</a>", text)
        return text
