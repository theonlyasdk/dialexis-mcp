---
name: ghostwriter
description: Turn transcripts, notes, or research into authentic human-sounding drafts before exporting with dialexis-write. Use when source material is rough, rambling, or sounds robotic.
license: MIT
---

# Ghostwriter

Raw material in, human draft out. This skill covers words only. File export
is handled by `dialexis-write` (`create_document`).

## When to use

Rough transcripts, scattered notes, research dumps, or any draft that sounds
robotic. If the content is already clean, skip straight to `dialexis-write`.

## Stage 1. Digest the source

- Extract claims, decisions, anecdotes, numbers, names, and direct quotes.
  Discard filler.
- Mark every gap as a question for the user or a `[TODO]`. Never invent
  facts, quotes, or statistics.
- Transcripts: merge repetitions of one point into a single statement. Keep
  the speaker's best phrasing verbatim where it sings.

## Stage 2. Match the voice

Pick one mode, or blend. If user writing samples exist, imitate them instead
(see Fingerprint below).

| Mode | Style | Best for |
| --- | --- | --- |
| Conversational | Short paragraphs, contractions, direct "you" | Posts, newsletters, memos |
| Analytical | Calm, precise, numbers first, conclusion up front | Reports, proposals, decisions |
| Terse | Fragments allowed, zero throat clearing | Summaries, slide notes, actions |

Fingerprint (from samples): sentence length rhythm, favorite transitions,
humor level, how pieces open (story, stat, blunt claim) and close (decision,
question, call to action).

## Stage 3. Structure first

1. One idea per section.
2. Headings that stand alone (`## Costs tripled after the migration`, not
   `## Costs`).
3. Open with the point. Background goes second, never first.
4. End with a decision, next step, or question. Never a summary of the summary.

## Stage 4. Humanize

- **Vary rhythm.** Alternate short punches with longer sentences. Three
  same-length sentences in a row is the classic AI tell.
- **One concrete detail per section.** A name, number, place, or quoted
  phrase. Abstract claims without evidence sound generated.
- **Cut the tells.** Robotic triads, "delve", "tapestry", "moreover",
  hedged non-conclusions ("it is important to note that"), hype adjectives
  with no proof, chains of parenthetical asides.
- **Verbs over nouns.** "We decided" beats "a decision was made". Active
  voice, named actors.
- **Keep honest rough edges.** A conceded drawback, an unrounded number, a
  genuine uncertainty. Perfection reads as synthetic.

## Stage 5. QA (read it aloud)

- [ ] Every sentence speakable in one breath (else split it)
- [ ] Every number, name, and quote matches the source
- [ ] Headings alone tell the story
- [ ] The ending states or asks for something

## Stage 6. Hand off

Emit clean markdown (headings, bullets, `| tables |`) and pass it to
`dialexis-write`. Flag any `[TODO]` gaps first. For formatting rules, also
load `dialexis-style`.
