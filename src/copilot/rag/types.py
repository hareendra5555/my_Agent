from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class Document:
    doc_id: str
    source: str
    title: str
    text: str

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    source: str
    title: str
    heading_path: str
    text: str
    position: int

@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float
    vector_score: float = 0.0
    bm25_score: float = 0.0

@dataclass
class Citation:
    source: str
    title: str
    heading_path: str
    chunk_id: str

@dataclass
class RAGAnswer:
    query: str
    answer: str
    citations: list[Citation] = field(default_factory=list)
    retrieved: list[RetrievedChunk] = field(default_factory=list)
    provider: str = ""
    model: str = ""