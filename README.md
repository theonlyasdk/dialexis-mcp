# dialexis-mcp

Write neat documents with AI — reports, memos, slides, spreadsheets, PDFs.
You write markdown, dialexis-mcp handles the formatting.

Supports `md`, `docx`, `pptx`, `xlsx`, `pdf`, and `html`.

## Quick start

```bash
git clone https://github.com/theonlyasdk/dialexis-mcp.git
cd dialexis-mcp
pip install -e ".[dev]"
```

Just want a machine to set it all up? Hand it [`AUTOSETUP.md`](AUTOSETUP.md).

## Connect your AI tool

- **Claude Code** — already configured via `.mcp.json`. Nothing to do.
- **Antigravity** — already configured via `.agents/mcp_config.json`. Just restart the workspace.
- **OpenCode** — add to `opencode.jsonc`:
  ```json
  { "mcp": { "dialexis-mcp": { "type": "local", "command": ["python", "-m", "dialexis_mcp"], "enabled": true } } }
  ```
- **Codex CLI** — add to `~/.codex/config.toml`:
  ```toml
  [mcp_servers.dialexis-mcp]
  command = "python"
  args = ["-m", "dialexis_mcp"]
  ```

## How it works

1. Draft your content as markdown (`# Title`, `## Sections`, bullet lists, tables).
2. Ask for a document — e.g. *"turn this into a Word doc"*.
3. You get back a file path. That's it.

Files land in `./exports` (change with `DIALEXIS_OUTPUT_DIR`). Every heading
level, table, and list is styled automatically — no manual formatting.

Extras: convert between formats, make small edits without rewriting the whole
file, fill reusable templates (`report`, `memo`, `slides`, `meeting-notes`,
`table-sheet`), and validate files before sharing.

## For contributors

```bash
pip install -e ".[dev]"
pytest -q
python scripts/sync_skills.py   # after editing anything in skills/
```

Skills live in `skills/` and are mirrored to `.agents/skills/`,
`.claude/skills/`, and `.opencode/skills/` so every harness picks them up.
