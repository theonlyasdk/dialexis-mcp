"""dialexis-mcp MCP server (MCP Python SDK v2, stdio + Streamable HTTP)."""
from __future__ import annotations

import argparse
import asyncio
import re
import sys
from pathlib import Path
from typing import Annotated, Literal

from mcp.server import MCPServer
from pydantic import Field

from . import docs as D

server = MCPServer(name="dialexis-mcp")


def _ok(path: Path, extra: str = "") -> str:
    info = D.file_info(path)
    base = f"Saved: {info['path']} ({info['format']}, {info['bytes']} bytes)"
    return base + (f"\n{extra}" if extra else "")


@server.tool(description="Create a neat document from markdown. Returns a file path, not file bytes. Use for md/docx/pptx/xlsx/pdf/html.")
def create_document(
    markdown: Annotated[str, Field(description="Full markdown source. H1 = title; H2s split slides for pptx; |tables| supported. Max 400k chars.")],
    format: Annotated[Literal["md", "docx", "pptx", "xlsx", "pdf", "html"], Field(description="Output format")] = "docx",
    file_name: Annotated[str | None, Field(description="Optional base name, e.g. 'q3-report'. Safe slug auto-generated.")] = None,
) -> str:
    """Create a document from markdown."""
    try:
        path = D.create_from_markdown(markdown, format, file_name)
        return _ok(path, f"Title: {D.extract_title(markdown)}")
    except (ValueError, OSError) as e:
        return f"Error: {e}"


@server.tool(description="Save one document in several formats at once (e.g. docx+pdf+pptx). One call, one path per format. Ask the user which formats first.")
def create_bundle(
    markdown: Annotated[str, Field(description="Full markdown source. H1 = title. Max 400k chars.")],
    formats: Annotated[list[str], Field(description="Formats to save, e.g. [\"docx\", \"pdf\"]. Choices: md, docx, pptx, xlsx, pdf, html.")] = ["docx", "pdf"],  # noqa: B006
    file_name: Annotated[str | None, Field(description="Optional base name, e.g. 'q3-report'")] = None,
) -> str:
    """Save multiple formats at once."""
    try:
        paths = D.create_bundle(markdown, formats, file_name)
        lines = []
        for p in paths:
            info = D.file_info(p)
            lines.append(f"- {info['path']} ({info['format']}, {info['bytes']} bytes)")
        return "Saved bundle:\n" + "\n".join(lines)
    except (ValueError, OSError) as e:
        return f"Error: {e}"


@server.tool(description="Read a document back as markdown with pagination. Prefer detail_level summary/metadata_only first to save tokens.")
def read_document(
    path: Annotated[str, Field(description="Path returned by create_document, or any existing md/docx/pptx/xlsx/pdf/html/txt file.")],
    detail_level: Annotated[Literal["full", "summary", "metadata_only"], Field(description="summary=first 40 lines, metadata_only=size/shape only")] = "full",
    page: Annotated[int, Field(description="1-based page of lines")] = 1,
    page_size: Annotated[int, Field(description="Lines per page, max 2000")] = 200,
) -> str:
    """Read a document as markdown."""
    try:
        p = D.resolve_read_path(path)
    except FileNotFoundError as e:
        return f"Error: {e}"
    try:
        if detail_level == "metadata_only":
            return str(D.file_info(p))
        text, meta = D.read_as_markdown(p, detail_level, page, page_size)
        suffix = f"\n\n[{meta.get('page')}/{meta.get('pages')} · {meta.get('lines')} lines]" if meta.get("pages", 1) > 1 else ""
        return (text or "(empty document)") + suffix
    except (ValueError, OSError) as e:
        return f"Error: {e}"


@server.tool(description="Convert a document between formats via markdown IR. Returns new file path.")
def convert_document(
    path: Annotated[str, Field(description="Existing document path")],
    to_format: Annotated[Literal["md", "docx", "pptx", "xlsx", "pdf", "html"], Field(description="Target format")] = "docx",
    file_name: Annotated[str | None, Field(description="Optional output base name")] = None,
) -> str:
    """Convert formats."""
    try:
        src = D.resolve_read_path(path)
        md_full = D.extract_markdown(src)
        # full extraction: no pagination cap, convert preserves large docs
        if not md_full.strip():
            return "Error: source document is empty"
        out = D.create_from_markdown(md_full, to_format, file_name or f"{src.stem}-converted")
        return _ok(out, f"Converted from {src.name}")
    except (ValueError, OSError) as e:
        return f"Error: {e}"


@server.tool(description="Append markdown or replace text in an existing md/docx/html document. Cheaper than full rewrite.")
def edit_document(
    path: Annotated[str, Field(description="Document path (md/docx/html/txt; docx rebuilt neatly)")],
    append_markdown: Annotated[str | None, Field(description="Markdown to append at end")] = None,
    find: Annotated[str | None, Field(description="Literal text to find (first occurrence)")] = None,
    replace: Annotated[str | None, Field(description="Replacement for find")] = None,
) -> str:
    """Surgical edit without rewriting the whole file."""
    try:
        src = D.resolve_read_path(path)
    except FileNotFoundError as e:
        return f"Error: {e}"
    ext = src.suffix.lower().lstrip(".")
    if ext not in ("md", "markdown", "txt", "html", "docx"):
        return f"Error: edit supports md/docx/html/txt, got .{ext}; use convert_document instead"
    try:
        if ext == "docx":
            md_full = D.extract_markdown(src)
        else:
            md_full = src.read_text(encoding="utf-8", errors="replace")
        updated = md_full
        if find is not None:
            if find not in updated:
                return "Error: 'find' text not found"
            updated = updated.replace(find, replace or "", 1)
        if append_markdown:
            updated = updated.rstrip() + "\n\n" + append_markdown.strip() + "\n"
        if updated == md_full:
            return "Error: nothing to change — provide append_markdown and/or find+replace"
        if ext == "docx":
            out = D.create_from_markdown(updated, "docx", src.stem)
        else:
            out = src
            out.write_text(updated, encoding="utf-8")
        return _ok(out, "Edit applied")
    except (ValueError, OSError) as e:
        return f"Error: {e}"


@server.tool(description="List built-in markdown templates (report, memo, slides, meeting-notes, table-sheet).")
def list_templates() -> str:
    """List templates."""
    base = Path(__file__).resolve().parent / "templates"
    items = sorted(p.stem for p in base.glob("*.md")) if base.exists() else []
    if not items:
        return "Templates: report, memo, slides, meeting-notes, table-sheet (built-in fallback)"
    return "Templates:\n" + "\n".join(f"- {n}" for n in items)


@server.tool(description="Fill a template's {{variables}} with values and create a document. Token-cheap vs free-form drafting.")
def fill_template(
    template: Annotated[str, Field(description="Template name from list_templates, or raw markdown containing {{var}} placeholders")],
    variables: Annotated[dict[str, str] | None, Field(description='Placeholder values, e.g. {"title": "Q3 Review"}')] = None,
    format: Annotated[Literal["md", "docx", "pptx", "xlsx", "pdf", "html"], Field(description="Output format")] = "docx",
    file_name: Annotated[str | None, Field(description="Optional output base name")] = None,
) -> str:
    """Fill {{var}} template."""
    base = Path(__file__).resolve().parent / "templates"
    src = template
    candidate = base / f"{template}.md"
    if candidate.exists() and "\n" not in template and "{{" not in template:
        src = candidate.read_text(encoding="utf-8")
    for k, v in (variables or {}).items():
        src = src.replace("{{" + str(k) + "}}", str(v))
        src = src.replace("{{ " + str(k) + " }}", str(v))
    missing = sorted(set(re.findall(r"\{\{\s*([\w-]+)\s*\}\}", src)))
    if missing:
        return f"Error: missing variables: {', '.join(missing)}"
    try:
        path = D.create_from_markdown(src, format, file_name or D.extract_title(src))
        return _ok(path, "Template filled")
    except (ValueError, OSError) as e:
        return f"Error: {e}"


@server.tool(description="Validate a document opens correctly and report size/shape (slides/pages/paragraphs/sheets).")
def validate_document(
    path: Annotated[str, Field(description="Document path to validate")],
) -> str:
    """Validate + describe."""
    try:
        p = D.resolve_read_path(path)
    except FileNotFoundError as e:
        return f"Error: {e}"
    info = D.file_info(p)
    if info["bytes"] == 0:
        return f"Error: file is empty: {p}"
    parts = [f"{k}={v}" for k, v in info.items() if k != "path"]
    return f"Valid: {p}\n" + "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser(prog="dialexis-mcp", description="Token-efficient document MCP server")
    ap.add_argument("--http", action="store_true", help="Run Streamable HTTP instead of stdio")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    if args.http:
        asyncio.run(server.run_streamable_http_async(host=args.host, port=args.port))
    else:
        asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()
