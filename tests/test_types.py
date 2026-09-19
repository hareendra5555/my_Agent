from copilot.rag.types import Chunk, RAGAnswer, RetrievedChunk

def test_chunk_holds_citation_info():
    c = Chunk(
        chunk_id="hb#0", doc_id="hb", source="handbook.md",
        title="Handbook", heading_path="Leave > Parental",
        text="16 weeks", position=0,
    )
    assert c.heading_path == "Leave > Parental"