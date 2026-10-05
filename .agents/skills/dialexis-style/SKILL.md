---
name: dialexis-style
description: House style for neat documents — typography, structure, and tone. Use together with dialexis-write when polishing user-facing docs.
license: MIT
---

# dialexis-style

## Structure

- One `# Title`, then `##` sections. Front-load the conclusion (BLUF).
- Paragraphs ≤ 4 lines. Prefer bullets and tables over walls of text.
- Every table gets a header row. Every slide gets a takeaway title, not "Slide 3".

## Tone

- Plain, active voice. No filler ("delve", "leverage", "in today's fast-paced").
- Numbers with units. Dates as `2026-10-05`.

## Formatting

- `docx/pdf`: 11pt body, real headings (not bold paragraphs), `Light Grid` tables.
- `pptx`: ≤ 6 bullets/slide, ≤ 220 chars per bullet.
- `xlsx`: headers bold, one table per sheet region, column A width 100.
