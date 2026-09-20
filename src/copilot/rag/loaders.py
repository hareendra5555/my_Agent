"""Load source documents (markdown/text/pdf) from a directory into Document objects."""

from __future__ import annotations

import hashlib
from pathlib import Path

from copilot.rag.types import Document


SUPPORTED_SUFFIXES = {".md", ".txt", ".pdf"}

def _doc_id(source: str) -> str:
    return hashlib.sha1(source.encode("utf-8")).hexdigest()[:12]

def _title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.lstrip("# ").strip()
    return fallback

def _load_pdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)

def load_document(path: Path, base_dir: Path) -> Document:
    if path.suffix == ".pdf":
        text = _load_pdf(path)
    else:
        text = path.read_text(encoding="utf-8")
    fallback_title = path.stem.replace("_", " ").replace("-", " ").title()
    title = _title_from_markdown(text, fallback_title) if path.suffix == ".md" else fallback_title
    source = path.relative_to(base_dir).as_posix()

    return Document(
        doc_id=_doc_id(source),
        source=source,
        title=title,
        text=text,
    )

def load_documents(directory: Path) -> list[Document]:
    # Recursively load every file in "directory" and output a list of Document objects
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Docs directory not found: {directory}")

    paths = sorted(p for p in directory.rglob("*") if p.is_file() and p.suffix in SUPPORTED_SUFFIXES)

    if not paths:
        raise ValueError(f"No supported documents ({SUPPORTED_SUFFIXES}) found under {directory}")

    return [load_document(p, directory) for p in paths]
