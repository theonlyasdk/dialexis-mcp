# AUTOSETUP.md — drop this file into ANY agentic AI (no repo needed) and it sets up dialexis-mcp by itself

> You are an AI setup agent. The user has handed you this file with NO repo
> installed. Bootstrap everything from scratch: download, install, verify,
> connect. Work autonomously — do not ask questions unless a step truly fails.
> If a step fails, fix it or report exactly what broke.

## 0. Bootstrap — get the repo (run this FIRST, always)

You may be starting in an empty folder. Do this:

1. Check tools exist: `git --version` and `python --version` (need Python >= 3.10).
   If `git` is missing, install it (or report to the user and stop).
2. If the current directory does NOT contain `pyproject.toml` AND
   `src/dialexis_mcp/server.py`, you don't have the repo. Get it:
   ```bash
   # if a dialexis-mcp folder already exists here, update it instead of cloning:
   git -C dialexis-mcp pull 2>/dev/null || git clone https://github.com/theonlyasdk/dialexis-mcp.git
   cd dialexis-mcp
   ```
   (PowerShell equivalent: `if (Test-Path dialexis-mcp) { git -C dialexis-mcp pull } else { git clone https://github.com/theonlyasdk/dialexis-mcp.git }; cd dialexis-mcp`)
3. Confirm you're on branch `main` and at the repo root:
   `git rev-parse --show-toplevel` should print your current directory, and
   `pyproject.toml` must exist. If not, stop and report.

## 1. Install

```bash
pip install -e ".[dev]"
```

Expected: `Successfully installed dialexis-mcp-0.1.0`. If `pip` is missing,
use `python -m pip install -e ".[dev]"`. If the Python is older than 3.10,
stop and tell the user to upgrade.

## 2. Sync skills (canonical `skills/` → all harnesses)

```bash
python scripts/sync_skills.py
```

Expected: 9 `synced ...` lines covering `.agents/skills/`, `.claude/skills/`,
`.opencode/skills/` for `dialexis-write`, `dialexis-style`, `ghostwriter`.

## 3. Verify (must ALL pass — fix source, never weaken tests)

```bash
pytest -q
python scripts/e2e_stdio.py
```

Expected: `pytest` all passed (13+ tests); E2E lists exactly 7 tools
(`create_document`, `read_document`, `convert_document`, `edit_document`,
`list_templates`, `fill_template`, `validate_document`) and ends with `E2E OK`.
If anything fails: read the traceback, fix files under `src/`, re-run.

## 4. Connect ONE harness (auto-detect, else ask)

Detect which agent you are running in and configure it; if unsure, do ALL
file-based ones (they're just committed files, harmless):

- **Claude Code:** project config `.mcp.json` is already committed — nothing to
  do. Optional: `claude mcp add --scope project dialexis-mcp -- python -m dialexis_mcp`.
- **Antigravity:** workspace config `.agents/mcp_config.json` is already
  committed. Tell the user to restart the workspace so it loads.
- **OpenCode:** add to `opencode.jsonc`:
  `{"mcp":{"dialexis-mcp":{"type":"local","command":["python","-m","dialexis_mcp"],"enabled":true}}}`.
- **Codex CLI:** add to `~/.codex/config.toml`:
  `[mcp_servers.dialexis-mcp]` + `command="python"` + `args=["-m","dialexis_mcp"]`.

Skills resolve automatically: Claude reads `.claude/skills/`, the other three
read `.agents/skills/` (OpenCode also reads `.opencode/skills/`).

## 5. Smoke-test document creation

Call `create_document` with markdown `# Setup OK` in format `docx`, then
`validate_document` on the returned path. Expected: `Saved: ... .docx` then
`Valid: ...`. Set `DIALEXIS_OUTPUT_DIR` if the user wants files elsewhere
(default `./exports`).

## 6. Done — report

Reply with: repo path / install OK / tests passed (count) / E2E OK / harness
connected / example document path. List anything you changed.
