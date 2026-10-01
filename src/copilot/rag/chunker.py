from __future__ import annotations

import re

from copilot.rag.types import Chunk, Document


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")

def _split_sections(text: str) -> list[tuple[str,str]]:
    """Return [(heading_path, section_text), ...] for a markdown document."""
    stack: list[tuple[int,str]] = [] 
    sections: list[tuple[str,list[str]]] = []
    current_lines: list[str] = []

    def flush():
        if current_lines:
            path = " > ".join(title for _, title in stack)
            sections.append((path, current_lines.copy()))
            current_lines.clear()

    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            flush()
            level = len(match.group(1))
            title = match.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
        else:
            current_lines.append(line)
    flush()

    return [(path, "\n".join(lines).strip()) for path, lines in sections if "\n".join(lines).strip()]

def _split_paragraphs(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    buf = ""

    for para in paragraphs:
        candidate = f"{buf}\n\n{para}".strip() if buf else para
        if len(candidate) <= max_chars:
            buf = candidate
            continue

        if buf:
            chunks.append(buf)
        if len(para) <= max_chars:
            buf = para
        else:
            # A single paragraph longer than max_chars: hard-split with overlap.
            start = 0
            while start < len(para):
                end = start + max_chars
                chunks.append(para[start:end])
                start = end - overlap_chars
            buf = ""

    if buf:
        chunks.append(buf)

    # Stitch small overlap between consecutive chunks for continuity.
    if overlap_chars > 0:
        stitched = []
        for i, c in enumerate(chunks):
            if i == 0:
                stitched.append(c)
            else:
                prev_tail = chunks[i - 1][-overlap_chars:]
                stitched.append(f"{prev_tail}\n{c}")
        return stitched
    return chunks


def chunk_document(doc: Document, max_chars: int = 1000, overlap_chars: int = 150) -> list[Chunk]:
    sections = _split_sections(doc.text) or [("", doc.text)]
    chunks: list[Chunk] = []
    position = 0

    for heading_path, section_text in sections:
        for piece in _split_paragraphs(section_text, max_chars, overlap_chars):
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.doc_id}-{position}",
                    doc_id=doc.doc_id,
                    source=doc.source,
                    title=doc.title,
                    heading_path=heading_path or doc.title,
                    text=piece,
                    position=position,
                )
            )
            position += 1

    return chunks


def chunk_documents(docs: list[Document], max_chars: int = 1000, overlap_chars: int = 150) -> list[Chunk]:
    result: list[Chunk] = []
    for doc in docs:
        result.extend(chunk_document(doc, max_chars=max_chars, overlap_chars=overlap_chars))
    return result
