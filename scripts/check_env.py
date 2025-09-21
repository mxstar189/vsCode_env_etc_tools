"""Check environment helper

Compares variables present in the repo `.env` with the current process environment.
Also shows VS Code workspace settings if present.
"""
from __future__ import annotations

import sys
import json
import os
from pathlib import Path
from typing import Dict, Any

# If script is executed directly (python scripts/check_env.py) the package
# root may not be on sys.path. Add repo root so `from scripts.env_load_util import env`
# works both when run as a module and when run as a script.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.env_load_util import env


def compare_envs() -> Dict[str, Dict[str, Any]]:
    env.load()
    file_vals = env.as_dict()
    out: Dict[str, Dict[str, Any]] = {}
    for k, v in file_vals.items():
        out[k] = {
            "file": v,
            "process": os.environ.get(k, "<missing>"),
            "match": os.environ.get(k) == v,
        }
    return out


def show_vscode_settings() -> Dict[str, object]:
    # attempt to read .vscode/settings.json
    root = Path(env.root)
    vs = root / ".vscode" / "settings.json"
    if not vs.exists():
        return {}
    try:
        return json.loads(vs.read_text(encoding="utf-8"))
    except Exception:
        return {"error": "failed to parse"}


def main() -> None:
    comp = compare_envs()
    print("Comparison of .env -> process environment (showing mismatches):")
    for k, info in comp.items():
        if not info["match"]:
            print(f"{k}: file='{info['file']}' process='{info['process']}'")
    print()
    vs = show_vscode_settings()
    if vs:
        print("Found .vscode/settings.json entries:")
        print(json.dumps(vs, indent=2))
    else:
        print("No .vscode/settings.json found or empty.")


if __name__ == "__main__":
    main()
