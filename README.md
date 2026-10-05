# dialexis-mcp
Tools for writing authentic documents with AI. Token-efficient MCP + Agent Skills for `md/docx/pptx/xlsx/pdf/html`.

## Install

```bash
pip install dialexis-mcp
# or from source:
pip install -e .
```

Run: `python -m dialexis_mcp` (stdio) or `python -m dialexis_mcp --http --port 8000`.

`DIALEXIS_OUTPUT_DIR` (default `./exports`) controls where files are written.

## Connect

**Claude Code** — project `.mcp.json` already commits stdio config. Or manual:

```bash
claude mcp add --scope project dialexis-mcp -- python -m dialexis_mcp
```

**Antigravity** — workspace config in `.agents/mcp_config.json` (same stdio command).

**OpenCode** — `opencode.jsonc`:

```json
{ "mcp": { "dialexis-mcp": { "type": "local", "command": ["python", "-m", "dialexis_mcp"], "enabled": true } } }
```

**Codex CLI** — `~/.codex/config.toml`:

```toml
[mcp_servers.dialexis-mcp]
command = "python"
args = ["-m", "dialexis_mcp"]
```

Skills live in `skills/` (canonical), mirrored to `.agents/skills/`, `.claude/skills/`, `.opencode/skills/`. Re-sync after edits:

```bash
python scripts/sync_skills.py
```

## Tools (7, all return paths — never bytes)

| Tool | Purpose |
|---|---|
| `create_document(markdown, format, file_name?)` | md/docx/pptx/xlsx/pdf/html from markdown |
| `read_document(path, detail_level, page, page_size)` | back to markdown, paginated; `summary` first |
| `convert_document(path, to_format)` | via markdown IR |
| `edit_document(path, append_markdown, find, replace)` | surgical fix, no rewrite |
| `list_templates` / `fill_template(template, variables, format)` | `{{var}}` docs |
| `validate_document(path)` | opens OK + shape (slides/pages/sheets) |

## Token rules

1. Draft markdown only. `##` splits slides; `| tables |` feed xlsx.
2. `read(summary)` → page only if needed. `edit(find/replace)` beats rewrite.
3. `fill_template` beats free-form for repeats.
4. `validate_document` before handing files to users.

## Dev

```bash
pip install -e ".[dev]"
pytest -q
```
