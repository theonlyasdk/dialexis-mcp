---
name: dialexis-write
description: Write neat md, docx, pptx, xlsx, pdf, html documents via dialexis-mcp tools. Use when the user asks for a report, memo, slides, spreadsheet, handout, or any document export.
license: MIT
---

# dialexis-write

Markdown is the only authoring format. Never emit OOXML or base64.
Every file is styled automatically: Instrument Serif headings, Times New
Roman body, research-paper look. Keep documents simple.

## Workflow

1. Draft concise markdown: `# Title`, `## Sections`, `- bullets`,
   `| tables |`, fenced code.
2. For slides (`pptx`): each `##` = one slide, max ~6 bullets per slide.
3. For spreadsheets (`xlsx`): put data in `| tables |`; first row = headers.
4. Before saving, ask the user which formats they want using the harness
   question tool (suggest `docx` + `pdf`). Never guess. Multi-format is the
   default expectation, but the user confirms.
5. Call `create_bundle(markdown, formats, file_name)` once for all confirmed
   formats, or `create_document` for a single format. Report every path.
6. To inspect cheaply: `read_document(path, detail_level="summary")` first,
   then `page=2...` only if needed.
7. Small fixes: `edit_document(path, append_markdown=...)` or `find/replace`.
   Full rewrites are wasteful.
8. Format switches: `convert_document(path, to_format=...)`.
9. Repeated structure: `list_templates()` then
   `fill_template(template, variables, format)`.
10. Finish: `validate_document(path)` for anything user-facing.

## Rules

- `create_*` returns paths, never file bytes. Never paste file bytes in chat.
- Keep markdown under ~400k chars; split longer docs.
- Filenames: short slugs (`q3-report`); the server makes them unique.
- See `references/formats.md` for per-format mapping.
