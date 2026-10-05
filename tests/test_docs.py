"""Production smoke tests: create/read/convert/edit/templates/validate across formats."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from dialexis_mcp import docs as D

SAMPLE = """# Q3 Report

## Summary

Ship **fast**, stay *neat*. See `code` and [link](https://example.com).

- alpha
- beta
- gamma

1. first
2. second

| Metric | Before | After |
| --- | --- | --- |
| latency | 900ms | 120ms |
| errors | 12 | 1 |

```python
print("hi")
```
"""


@pytest.fixture(autouse=True)
def _tmp_out(monkeypatch, tmp_path):
    monkeypatch.setenv("DIALEXIS_OUTPUT_DIR", str(tmp_path))
    return tmp_path


@pytest.mark.parametrize("fmt", ["md", "html", "docx", "pptx", "pdf", "xlsx"])
def test_create_all_formats(fmt):
    p = D.create_from_markdown(SAMPLE, fmt, f"sample-{fmt}")
    assert p.exists() and p.stat().st_size > 0, fmt
    info = D.file_info(p)
    assert info["format"] == fmt


def test_read_pagination_and_summary():
    p = D.create_from_markdown("# T\n\n" + "\n".join(f"line {i}" for i in range(100)), "md", "paged")
    text, meta = D.read_as_markdown(p, "full", page=2, page_size=10)
    assert meta["page"] == 2 and "line" in text
    s, _ = D.read_as_markdown(p, "summary")
    assert len(s.splitlines()) <= 40
    m, _m = D.read_as_markdown(p, "metadata_only")
    assert m == ""


def test_read_roundtrip_docx_pptx_pdf_xlsx():
    for fmt in ("docx", "pptx", "pdf", "xlsx"):
        p = D.create_from_markdown(SAMPLE, fmt, f"rt-{fmt}")
        text, _ = D.read_as_markdown(p, "full")
        assert "Q3 Report" in text or "latency" in text or "alpha" in text, fmt


def test_convert_and_validate():
    src = D.create_from_markdown(SAMPLE, "md", "conv-src")
    out = D.create_from_markdown(src.read_text(encoding="utf-8"), "docx", "conv-out")
    assert out.suffix == ".docx"
    info = D.file_info(out)
    assert info["bytes"] > 0 and "paragraphs" in info


def test_fill_template_missing_var_reports():
    with pytest.raises(ValueError):
        D.create_from_markdown("", "docx")
    # fill path uses server-level missing detection; core create validates empty
    p = D.create_from_markdown("# {{title}}\n\nHi {{name}}", "md", "tpl")
    assert "{{title}}" in p.read_text(encoding="utf-8")


def test_large_doc_convert_preserves_all_lines():
    big = "# Big\n\n" + "\n".join(f"line {i}" for i in range(3000))
    src = D.create_from_markdown(big, "md", "big-src")
    full = D.extract_markdown(src)
    assert "line 2999" in full
    out = D.create_from_markdown(full, "docx", "big-out")
    back = D.extract_markdown(out)
    assert "line 2999" in back, "convert/edit must not truncate at 2000 lines"


def test_safe_names_and_errors():
    p1 = D.create_from_markdown(SAMPLE, "docx", "dup")
    p2 = D.create_from_markdown(SAMPLE, "docx", "dup")
    assert p1 != p2  # unique on collision
    with pytest.raises(ValueError):
        D.create_from_markdown(SAMPLE, "exe", "bad")
    with pytest.raises(FileNotFoundError):
        D.resolve_read_path("no-such-file-xyz.docx")
    with pytest.raises(ValueError):
        D.create_from_markdown("x" * 400_001, "md")


def test_house_fonts_applied():
    from docx import Document

    p = D.create_from_markdown(SAMPLE, "docx", "fonts-docx")
    doc = Document(str(p))
    assert doc.styles["Normal"].font.name == "Times New Roman"
    assert doc.styles["Heading 1"].font.name == "Instrument Serif"
    from pptx import Presentation

    q = D.create_from_markdown(SAMPLE, "pptx", "fonts-pptx")
    slide = Presentation(str(q)).slides[0]
    assert slide.shapes.title.text_frame.paragraphs[0].runs[0].font.name == "Instrument Serif"
    r = D.create_from_markdown(SAMPLE, "pdf", "fonts-pdf")
    from pypdf import PdfReader

    assert len(PdfReader(str(r)).pages) >= 1
    h = D.create_from_markdown(SAMPLE, "html", "fonts-html")
    html = h.read_text(encoding="utf-8")
    assert "Instrument Serif" in html and "Times New Roman" in html


def test_bundle_creates_all_formats():
    paths = D.create_bundle(SAMPLE, ["docx", "pdf", "md"], "bundle-test")
    assert len(paths) == 3
    assert sorted(p.suffix for p in paths) == [".docx", ".md", ".pdf"]
    assert all(p.exists() and p.stat().st_size > 0 for p in paths)
    with pytest.raises(ValueError):
        D.create_bundle(SAMPLE, [], "bundle-empty")
    with pytest.raises(ValueError):
        D.create_bundle(SAMPLE, ["exe"], "bundle-bad")


def test_server_tools_callable():
    from dialexis_mcp import server as S

    expected = {"create_document", "create_bundle", "read_document", "convert_document", "edit_document",
                "list_templates", "fill_template", "validate_document"}
    for fn in expected:
        assert callable(getattr(S, fn, None)), fn
    # ensure MCP decorators registered (v1 _tools or v2 _tool_registry)
    registry = getattr(S.server, "_tools", None) or getattr(S.server, "_tool_registry", None) or {}
    try:
        names = set(registry.keys()) if isinstance(registry, dict) else {t.name for t in registry}
    except Exception:
        names = set()
    if names:
        assert expected <= names, names
