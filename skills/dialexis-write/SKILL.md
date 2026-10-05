---
name: dialexis-write
description: Write neat md, docx, pptx, xlsx, pdf, html documents via dialexis-mcp tools. Use when the user asks for a report, memo, slides, spreadsheet, handout, or any document export.
license: MIT
---

# dialexis-write

Markdown is the only authoring format. Never emit OOXML or base64.

## Workflow

1. Draft concise markdown: `# Title`, `## Sections`, `- bullets`, `| tables |`, fenced code.
2. For slides (`pptx`): each `##` = one slide, max ~6 bullets per slide, 60 slides max.
3. For spreadsheets (`xlsx`): put data in `| tables |`; first row = headers.
4. Call `create_document(markdown, format, file_name)` → returns a disk path. Report the path.
5. To inspect cheaply: `read_document(path, detail_level="summary")` first, then `page=2...` only if needed.
6. Small fixes: `edit_document(path, append_markdown=...)` or `find/replace`. Full rewrites are wasteful.
7. Format switches: `convert_document(path, to_format=...)`.
8. Repeated structure: `list_templates()` → `fill_template(template, variables, format)`.
9. Finish: `validate_document(path)` for anything user-facing.

## Rules

- `create_*` returns a path — never paste file bytes into chat.
- Keep markdown under ~400k chars; split longer docs.
- Filenames: short slugs (`q3-report`), server makes them unique.
- See `references/formats.md` for per-format mapping.
