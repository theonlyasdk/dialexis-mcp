# CLAUDE.md (Claude Code, OpenCode)

Write neat documents with dialexis-mcp. Markdown is the only authoring format.

- Skills: `.claude/skills/dialexis-write/SKILL.md`, `.claude/skills/dialexis-style/SKILL.md`, `.claude/skills/ghostwriter/SKILL.md`
- MCP stdio: `python -m dialexis_mcp` (project config in `.mcp.json`)
- Flow: draft markdown → `create_document` → path → `validate_document`
- Token rules: `read_document(summary)` first; `edit_document(find/replace)` for fixes; `fill_template` for repeats. Never paste file bytes.
