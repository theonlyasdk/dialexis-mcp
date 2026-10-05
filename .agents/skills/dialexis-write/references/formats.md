# Format mapping (markdown → outputs)

## docx

- `#` → Title, `##` → Heading 1, `###+` → Heading 2/3
- `- item` → List Bullet, `1. item` → List Number
- `| a | b |` → Light Grid table (header + rows)
- ` ``` ` → Consolas 9pt paragraph
- `**bold**`, `*italic*`, `` `code` `` preserved via runs

## pptx

- `#` → deck title; each `##` starts a new slide (max 60)
- Bullets/numbered → bullet lines (max 12/slide, 220 chars each)
- Tables → flattened `a | b` lines (max 8 rows/slide)
- Long paragraphs truncated per slide — split source with more `##` for control

## pdf

- A4, Title + H1/H2/H3, bullets, grid tables, code in Courier 8pt

## xlsx

- `#` → sheet title cell (bold 14pt)
- Tables → real cells (row 1 bold headers)
- Other blocks → column A lines

## Token tips

- `read_document(summary)` = 40 lines; `metadata_only` = shape only.
- `edit_document(find/replace)` < full `create_document`.
- `fill_template` < free-form drafting for repeated docs.
