---
name: ghostwriter
description: Turn transcripts, notes, or research into authentic human-sounding drafts before exporting with dialexis-write. Use when source material is rough, rambling, or sounds robotic.
license: MIT
---

# Ghostwriter

Raw material in, human draft out. The draft then goes to `dialexis-write`
(`create_document`) for export — this skill covers words, not file formats.

## 1. Digest the source

- Extract: claims, decisions, anecdotes, numbers, names, direct quotes. Discard filler.
- Note what's MISSING: every gap becomes either a question for the user or a
  clearly-marked `[TODO]` — never invent facts, quotes, or statistics.
- If the source is a transcript: merge scattered repetitions of one point into
  a single statement; keep the speaker's best phrasing verbatim where it sings.

## 2. Match the voice

Pick one, or blend. If user samples exist, imitate their fingerprint instead:

- **Conversational:** short paragraphs, contractions, direct address ("you").
  Best for posts, newsletters, memos.
- **Analytical:** calm, precise, numbers-first, conclusions up front. Best for
  reports, proposals, decision docs.
- **Terse:** fragments allowed, no throat-clearing. Best for exec summaries,
  slide speaker notes, action items.

Voice fingerprint to copy from samples: sentence length rhythm, favorite
transitions, humor level, how they open (story? stat? blunt claim?) and close
(decision? question? call to action?).

## 3. Structure before sentences

- One idea per section; headings that carry meaning alone (`## Costs grew 3x
  after the migration`, not `## Costs`).
- Open with the point (BLUF) — background goes second, never first.
- End with a decision, next step, or question. Never end with a summary of the
  summary ("In conclusion, this document has shown...").

## 4. Humanize the draft

- **Vary rhythm:** alternate short punches with longer flowing sentences.
  Three same-length sentences in a row is the classic AI tell — break it up.
- **One concrete detail per section:** a name, number, place, or quoted phrase.
  Abstract claims without evidence sound generated.
- **Cut the tells:** robotic triads ("fast, reliable, and scalable"), "delve",
  "tapestry", "moreover/furthermore", em-dash chains, hedged non-conclusions
  ("it's important to note that..."), hype adjectives with no proof.
- **Prefer verbs over nouns:** "we decided" beats "a decision was made";
  active voice, named actors, no throat-clearing openers.
- **Keep the rough edges that earn trust:** a conceded drawback, a number that
  isn't round, an admission of uncertainty where it genuinely exists.

## 5. QA pass (read it aloud)

- If a sentence can't be spoken in one breath, split it.
- Check every number/name/quote against the source — no drift.
- Check headings alone tell the story.
- Confirm the ending asks for or states something.

## 6. Hand off

Output clean markdown (headings, bullets, `| tables |`) and pass it to
`dialexis-write`. Mention any `[TODO]` gaps so the user can fill them before
export. For house formatting rules, also load `dialexis-style`.
