import asyncio

from routers import sentences


def test_txt_list_uses_natural_order(tmp_path, monkeypatch):
    (tmp_path / "S10-20.txt").write_text("ten", encoding="utf-8")
    (tmp_path / "S1-2.txt").write_text("one", encoding="utf-8")
    (tmp_path / "ignore.md").write_text("ignore", encoding="utf-8")
    monkeypatch.setattr(sentences, "DATA_SENTENCE_DIR", str(tmp_path))

    result = asyncio.run(sentences.api_txt_list())

    assert result == {"files": ["S1-2.txt", "S10-20.txt"]}
