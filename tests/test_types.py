from copilot.rag.types import Chunk, Citation, RAGAnswer, RetrievedChunk

def test_chunk_holds_citation_info():
    c = Chunk(
        chunk_id="hb#0", doc_id="hb", source="handbook.md",
        title="Handbook", heading_path="Leave > Parental",
        text="16 weeks", position=0,
    )
    assert c.heading_path == "Leave > Parental"

def test_rag_answer_lists_are_not_shared():
    a = RAGAnswer(query="q", answer="a")
    b = RAGAnswer(query="q", answer="a")
    a.citations.append(
        Citation(source="handbook.md", title="Handbook", heading_path="Leave", chunk_id="hb#0")
    )
    assert b.citations == []


def test_retrieved_chunk_score_defaults():
    c = Chunk(
        chunk_id="hb#0", doc_id="hb", source="handbook.md",
        title="Handbook", heading_path="Leave", text="16 weeks", position=0,
    )
    r = RetrievedChunk(chunk=c, score=0.5)
    assert r.bm25_score == 0.0
