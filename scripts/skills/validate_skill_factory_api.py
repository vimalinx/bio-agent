#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_skill_from_help  # noqa: E402


def _models_url(base_url: str) -> str:
    trimmed = base_url.rstrip("/")
    if trimmed.endswith("/chat/completions"):
        trimmed = trimmed[: -len("/chat/completions")]
    return f"{trimmed}/models"


def _fetch_models(config: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        _models_url(str(config["base_url"])),
        headers={"Authorization": f"Bearer {config['api_key']}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=float(config["request_timeout_seconds"])) as response:
        body = response.read().decode("utf-8", errors="replace")
    payload = json.loads(body)
    models = [str(item.get("id", "")) for item in payload.get("data", []) if isinstance(item, dict)]
    return {"ok": True, "models": models}


def _sample_tool() -> dict[str, Any]:
    return {
        "name": "bedtools",
        "command": "bedtools",
        "summary": "genomic interval arithmetic, overlap, merge, coverage, and genome feature comparisons",
        "path": "/home/vimalinx/miniforge3/envs/bio/bin/bedtools",
        "version_text": "$ bedtools --version\nbedtools v2.31.1",
        "help_text": (
            "$ bedtools --help\n"
            "bedtools: a powerful toolset for genome arithmetic.\n"
            "Usage: bedtools <subcommand> [options]\n"
            "Available subcommands:\n"
            "  intersect  Find overlapping intervals\n"
            "  merge      Combine overlapping or adjacent intervals\n"
            "  coverage   Compute feature coverage\n"
        ),
        "man_text": "bedtools provides utilities for comparing, manipulating, and annotating genomic intervals.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the biology skill factory API configuration.")
    parser.add_argument(
        "--config-path",
        default=str(render_skill_from_help.DEFAULT_CONFIG_PATH),
        help="Path to skill factory config JSON.",
    )
    args = parser.parse_args()

    config_path = Path(args.config_path).resolve()
    config = render_skill_from_help.load_render_config(config_path=config_path)

    report: dict[str, Any] = {
        "config_path": str(config_path),
        "base_url": config.get("base_url"),
        "model": config.get("model"),
        "reasoning_effort": config.get("reasoning_effort"),
        "max_completion_tokens": config.get("max_completion_tokens"),
        "api_key_present": bool(config.get("api_key")),
    }

    if not render_skill_from_help._config_is_complete(config):
        report["ok"] = False
        report["error"] = "API configuration is incomplete."
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1

    try:
        report["models_probe"] = _fetch_models(config)
    except Exception as exc:
        report["models_probe"] = {"ok": False, "error": str(exc)}

    try:
        rendered = render_skill_from_help.render_skill_markdown(_sample_tool(), mode="online", config_path=config_path)
        report["render_probe"] = {
            "ok": True,
            "preview": rendered[:1200],
        }
        report["ok"] = True
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as exc:
        report["render_probe"] = {
            "ok": False,
            "error": str(exc),
        }
        report["ok"] = False

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
