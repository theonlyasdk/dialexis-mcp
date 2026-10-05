---
name: ghostwriter
description: Turn transcripts, notes, or research into authentic human-sounding drafts before exporting with dialexis-write. Use when source material is rough or sounds robotic.
license: MIT
---

# Ghostwriter (adapted for dialexis-mcp)

Inspired by `cdeistopened/skill-stack` ghostwriter skill (MIT). Rewritten to avoid verbatim copying.

## Workflow

1. **Understand source:** extract claims, anecdotes, numbers. Discard filler.
2. **Pick voice:** conversational / analytical / terse — match existing user samples if present.
3. **Draft from markdown:** short sentences, varied rhythm, one idea per paragraph.
4. **Humanize:** cut AI tells (triads, "moreover", em-dash chains, hedged conclusions). Add one concrete detail per section.
5. **QA:** read aloud test — if a sentence can't be spoken, rewrite it.
6. **Export:** hand the polished markdown to `dialexis-write` (`create_document`).

## Checklist

- [ ] No robotic triads or hype adjectives
- [ ] Numbers and names preserved from source
- [ ] Headings carry meaning without the body
- [ ] Ends with a decision or next step, not a summary of the summary
