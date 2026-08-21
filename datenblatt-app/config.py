"""config.py - lädt/speichert config.json (API-Key etc.) lokal neben dem Programm.
Der Key wird NIE fest im Code hinterlegt, sondern nur lokal von dir selbst
eingetragen und bleibt auf deinem Rechner."""
import json
from pathlib import Path

DEFAULT_CONFIG = {"anthropic_api_key": "", "model": "claude-sonnet-5"}


def load_config(run_dir: Path) -> dict:
    path = run_dir / "config.json"
    if not path.exists():
        path.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
        return dict(DEFAULT_CONFIG)
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
        return {**DEFAULT_CONFIG, **cfg}
    except Exception:
        return dict(DEFAULT_CONFIG)


def save_config(run_dir: Path, cfg: dict):
    path = run_dir / "config.json"
    path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
