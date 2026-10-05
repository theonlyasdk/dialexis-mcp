"""Mirror skills/ to .agents/skills, .claude/skills, .opencode/skills (Windows-safe copy)."""
from __future__ import annotations
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "skills"
DESTS = [ROOT / ".agents" / "skills", ROOT / ".claude" / "skills", ROOT / ".opencode" / "skills"]

def main() -> None:
    names = [p.name for p in SRC.iterdir() if p.is_dir()]
    for dest in DESTS:
        for n in names:
            shutil.copytree(SRC / n, dest / n, dirs_exist_ok=True)
            print(f"synced {dest.parent.name}/{dest.name}/{n}")

if __name__ == "__main__":
    main()
