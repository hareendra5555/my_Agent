from copilot.rag.chunker import chunk_document, chunk_documents
from copilot.rag.types import Document

SAMPLE_MD = """# Employee Handbook

## Leave Policy

### Parental Leave

Full-time employees are entitled to 16 weeks of paid parental leave after
one year of continuous employment.

### Sick Leave

Employees accrue 1 day of sick leave per month, up to 12 days per year.

## Expense Policy

All expenses over $75 require a manager's approval and a submitted receipt
within 30 days of purchase.
"""


def make_doc(text: str = SAMPLE_MD, doc_id: str = "doc1", source: str = "handbook.md") -> Document:
    return Document(doc_id=doc_id, source=source, title="Employee Handbook", text=text)


def test_chunks_carry_heading_path():
    chunks = chunk_document(make_doc(), max_chars=1000, overlap_chars=0)
    paths = {c.heading_path for c in chunks}
    assert "Employee Handbook > Leave Policy > Parental Leave" in paths
    assert "Employee Handbook > Leave Policy > Sick Leave" in paths
    assert "Employee Handbook > Expense Policy" in paths


def test_parental_leave_fact_survives_in_one_chunk():
    chunks = chunk_document(make_doc(), max_chars=1000, overlap_chars=0)
    matches = [c for c in chunks if "16 weeks" in c.text]
    assert len(matches) == 1
    assert "Parental Leave" in matches[0].heading_path


def test_long_paragraph_is_split_with_overlap():
    long_para = "word " * 500  # ~2500 chars, forces a hard split
    doc = make_doc(f"# Doc\n\n{long_para}")
    chunks = chunk_document(doc, max_chars=500, overlap_chars=50)
    assert len(chunks) > 1
    # consecutive chunks should share the overlap text
    assert chunks[0].text[-50:] in chunks[1].text


def test_chunk_ids_are_stable_and_ordered():
    chunks = chunk_document(make_doc(), max_chars=1000, overlap_chars=0)
    positions = [c.position for c in chunks]
    assert positions == sorted(positions)
    assert len(set(c.chunk_id for c in chunks)) == len(chunks)


def test_document_without_headings_uses_title_as_heading_path():
    chunks = chunk_document(make_doc("Just a plain paragraph."), max_chars=1000, overlap_chars=0)
    assert len(chunks) == 1
    assert chunks[0].heading_path == "Employee Handbook"


def test_short_paragraphs_in_one_section_are_packed_together():
    chunks = chunk_document(make_doc("# Doc\n\nFirst para.\n\nSecond para."), max_chars=1000, overlap_chars=0)
    assert len(chunks) == 1
    assert "First para." in chunks[0].text and "Second para." in chunks[0].text


def test_paragraphs_are_split_when_they_exceed_max_chars():
    text = "# Doc\n\n" + "a" * 600 + "\n\n" + "b" * 600
    chunks = chunk_document(make_doc(text), max_chars=1000, overlap_chars=0)
    assert len(chunks) == 2
    assert chunks[0].text == "a" * 600
    assert chunks[1].text == "b" * 600


def test_chunk_documents_combines_all_documents():
    docs = [
        make_doc(doc_id="d1", source="a.md"),
        make_doc(doc_id="d2", source="b.md"),
    ]
    chunks = chunk_documents(docs, max_chars=1000, overlap_chars=0)
    assert {c.source for c in chunks} == {"a.md", "b.md"}
    assert len({c.chunk_id for c in chunks}) == len(chunks)
