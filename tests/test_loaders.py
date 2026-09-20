import pytest

from copilot.rag.loaders import load_documents


def test_markdown_title_comes_from_first_h1(tmp_path):
    # The "## Sub" line comes first on purpose: only a single "# " counts as the title.
    (tmp_path / "policy.md").write_text("## Sub\n\n# Leave Rules\nText", encoding="utf-8")
    docs = load_documents(tmp_path)
    assert docs[0].title == "Leave Rules"
    assert docs[0].source == "policy.md"


def test_title_falls_back_to_filename(tmp_path):
    (tmp_path / "my_notes.txt").write_text("just some text", encoding="utf-8")
    docs = load_documents(tmp_path)
    assert docs[0].title == "My Notes"


def test_finds_files_in_subfolders_with_relative_source(tmp_path):
    (tmp_path / "hr").mkdir()
    (tmp_path / "hr" / "leave.md").write_text("# Leave\nbody", encoding="utf-8")
    docs = load_documents(tmp_path)
    assert len(docs) == 1
    assert docs[0].source == "hr/leave.md"


def test_ignores_unsupported_file_types(tmp_path):
    (tmp_path / "keep.md").write_text("# Keep", encoding="utf-8")
    (tmp_path / "skip.png").write_bytes(b"\x89PNG")
    docs = load_documents(tmp_path)
    assert [d.source for d in docs] == ["keep.md"]


def test_doc_id_is_stable_across_base_directories(tmp_path):
    for folder in ("machine_a", "machine_b"):
        (tmp_path / folder).mkdir()
        (tmp_path / folder / "policy.md").write_text("# Policy", encoding="utf-8")
    id_a = load_documents(tmp_path / "machine_a")[0].doc_id
    id_b = load_documents(tmp_path / "machine_b")[0].doc_id
    assert isinstance(id_a, str) and len(id_a) == 12
    assert id_a == id_b


def test_missing_directory_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_documents(tmp_path / "does_not_exist")


def test_empty_directory_raises_value_error(tmp_path):
    with pytest.raises(ValueError):
        load_documents(tmp_path)
