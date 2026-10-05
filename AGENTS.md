# AGENTS.md (Codex, Antigravity, OpenCode)

Write neat documents with dialexis-mcp. Markdown is the only authoring format.

- Skills (canonical `skills/`, mirrored): `.agents/skills/dialexis-write/SKILL.md`, `.agents/skills/dialexis-style/SKILL.md`, `.agents/skills/ghostwriter/SKILL.md`
- MCP stdio: `python -m dialexis_mcp` (see `.mcp.json`, `.agents/mcp_config.json`)
- Flow: draft markdown → `create_document` → path → `validate_document`
- Token rules: `read_document(summary)` first; `edit_document(find/replace)` for fixes; `fill_template` for repeats. Never paste file bytes.
