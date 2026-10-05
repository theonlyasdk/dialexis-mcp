# dialexis-mcp

Write neat documents with AI: reports, memos, slides, spreadsheets, PDFs.
You write markdown, dialexis-mcp handles the formatting.

Supported formats: `md`, `docx`, `pptx`, `xlsx`, `pdf`, `html`.

## Quick start

```bash
git clone https://github.com/theonlyasdk/dialexis-mcp.git
cd dialexis-mcp
pip install -e ".[dev]"
```

Want a machine to set it all up? Hand it [`AUTOSETUP.md`](AUTOSETUP.md).

## Connect your AI tool

### Claude Code

Already configured via `.mcp.json`. Nothing to do.

### Antigravity

Already configured via `.agents/mcp_config.json`. Just restart the workspace.

### OpenCode

Add to `opencode.jsonc`:

```json
{ "mcp": { "dialexis-mcp": { "type": "local", "command": ["python", "-m", "dialexis_mcp"], "enabled": true } } }
```

### Codex CLI

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.dialexis-mcp]
command = "python"
args = ["-m", "dialexis_mcp"]
```

## How it works

1. Draft content as markdown (`# Title`, `## Sections`, lists, tables).
2. Ask for a document (for example: "turn this into a Word doc").
3. You get back a file path. Done.

Files land in `./exports` (override with `DIALEXIS_OUTPUT_DIR`). Headings,
tables, and lists are styled automatically. No manual formatting needed.

### Extras

- Convert between formats
- Small edits without rewriting the whole file
- Reusable templates: `report`, `memo`, `slides`, `meeting-notes`, `table-sheet`
- Validate files before sharing

## For contributors

```bash
pip install -e ".[dev]"
pytest -q
python scripts/sync_skills.py   # after editing anything in skills/
```

Skills live in `skills/` and are mirrored to `.agents/skills/`,
`.claude/skills/`, and `.opencode/skills/`, so every harness picks them up.
