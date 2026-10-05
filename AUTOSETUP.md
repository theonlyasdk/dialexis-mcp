# AUTOSETUP.md — feed this file to any AI agent to set up dialexis-mcp automatically

> You are an AI setup agent. Follow every step below in order. Do not skip
> verification. Stop and report if any step fails.

## 0. Facts

- Repo: `https://github.com/theonlyasdk/dialexis-mcp.git`, branch `main`.
- Stack: Python >= 3.10, MCP server `dialexis-mcp` (stdio + HTTP), skills in
  `skills/` mirrored to `.agents/skills/`, `.claude/skills/`, `.opencode/skills/`.
- Success = `pytest` green + MCP stdio E2E prints `E2E OK`.

## 1. Clone and install

```bash
git clone https://github.com/theonlyasdk/dialexis-mcp.git
cd dialexis-mcp
pip install -e ".[dev]"
```

Expected: `Successfully installed dialexis-mcp-0.1.0`.

## 2. Sync skills (canonical `skills/` → all harnesses)

```bash
python scripts/sync_skills.py
```

Expected: 9 lines, `synced .agents/skills/...`, `.claude/skills/...`,
`.opencode/skills/...` for `dialexis-write`, `dialexis-style`, `ghostwriter`.

## 3. Verify (must all pass)

```bash
pytest -q
python scripts/e2e_stdio.py
```

Expected: `pytest` reports all passed (13+ tests); E2E lists exactly 7 tools
(`create_document`, `read_document`, `convert_document`, `edit_document`,
`list_templates`, `fill_template`, `validate_document`) and ends with `E2E OK`.

If `pytest` fails: read the traceback, fix source under `src/`, re-run. Never
edit tests to make them pass.

## 4. Connect ONE harness (pick the user's)

- **Claude Code:** project config `.mcp.json` is already committed. Or run
  `claude mcp add --scope project dialexis-mcp -- python -m dialexis_mcp`.
- **Antigravity:** workspace config `.agents/mcp_config.json` is already
  committed. Restart the workspace so it loads.
- **OpenCode:** add to `opencode.jsonc`:
  `{"mcp":{"dialexis-mcp":{"type":"local","command":["python","-m","dialexis_mcp"],"enabled":true}}}`.
- **Codex CLI:** add to `~/.codex/config.toml`:
  `[mcp_servers.dialexis-mcp]` + `command="python"` + `args=["-m","dialexis_mcp"]`.

Skills resolve automatically: Claude reads `.claude/skills/`, the other three
read `.agents/skills/` (OpenCode also reads `.opencode/skills/`).

## 5. Smoke-test document creation

Call `create_document` with markdown `# Setup OK` in format `docx`, then
`validate_document` on the returned path. Expected: `Saved: ... .docx` then
`Valid: ...`. Report the file path to the user. Set `DIALEXIS_OUTPUT_DIR` if
they want files elsewhere (default `./exports`).

## 6. Done — report

Reply with: install OK / tests passed (count) / E2E OK / harness connected /
example document path. List anything you changed.
