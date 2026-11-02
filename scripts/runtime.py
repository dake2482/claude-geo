#!/usr/bin/env python3
"""claude-geo runtime: isolated venv bootstrap + command dispatch.

Commands:
  run <script.py> [args...]   ensure venv, then exec script with venv python
  setup                        create/refresh the venv
  doctor                       report runtime readiness
"""
import json
import os
import subprocess
import sys
import sysconfig
import venv
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REQUIREMENTS = SKILL_DIR / "requirements.txt"
MIN_PY = (3, 11)


def _data_dir() -> Path:
    override = os.environ.get("CLAUDE_GEO_DATA_DIR")
    if override:
        return Path(override).expanduser()
    if (SKILL_DIR / ".claude-plugin" / "plugin.json").is_file():
        if sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        elif sys.platform == "win32":
            base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        else:
            base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        return (base / "claude-geo").resolve()
    return SKILL_DIR


DATA_DIR = _data_dir()
VENV_DIR = DATA_DIR / ".venv"


def venv_python() -> Path:
    return VENV_DIR / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def have_deps() -> bool:
    try:
        out = subprocess.run(
            [str(venv_python()), "-c", "import requests, bs4; print('ok')"],
            capture_output=True, text=True, timeout=30,
        )
        return out.returncode == 0 and "ok" in out.stdout
    except Exception:
        return False


def setup() -> int:
    if sys.version_info[:2] < MIN_PY:
        print(f"claude-geo needs Python >={MIN_PY[0]}.{MIN_PY[1]}")
        return 1
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not venv_python().exists():
        print("Creating isolated claude-geo venv...")
        venv.create(str(VENV_DIR), with_pip=True)
    req = str(REQUIREMENTS) if REQUIREMENTS.exists() else "requests\nbeautifulsoup4\n"
    print("Installing dependencies...")
    r = subprocess.run(
        [str(venv_python()), "-m", "pip", "install", "-q", "-r", req],
    )
    if r.returncode != 0:
        print("Dependency installation failed.")
        return 1
    print("claude-geo runtime is ready.")
    return 0


def doctor() -> int:
    status = {
        "runtime": "ready" if (venv_python().exists() and have_deps()) else "not-ready",
        "python": "%d.%d" % sys.version_info[:2],
        "venv": str(VENV_DIR),
        "data_dir": str(DATA_DIR),
        "setup_hint": "claude-geo setup" if venv_python().exists() is False or not have_deps() else None,
    }
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    if cmd == "setup":
        return setup()
    if cmd == "doctor":
        return doctor()
    if cmd == "run":
        if len(sys.argv) < 3:
            print("usage: claude-geo run <script.py> [args...]")
            return 2
        if not venv_python().exists() or not have_deps():
            rc = setup()
            if rc != 0:
                return rc
        script = sys.argv[2]
        target = Path(script)
        if not target.is_absolute():
            target = SKILL_DIR / "scripts" / script
        os.execv(str(venv_python()), [str(venv_python()), str(target)] + sys.argv[3:])
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
