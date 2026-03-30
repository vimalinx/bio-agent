#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.workspace_env import build_subprocess_env


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import discover_bio_tools  # noqa: E402
import render_skill_from_help  # noqa: E402


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _run_command_capture(
    args: list[str],
    repo_root: Path,
    env: dict[str, str],
    timeout: int = 8,
) -> str:
    try:
        completed = subprocess.run(
            args,
            cwd=repo_root,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return ""

    output = "\n".join(part for part in [completed.stdout, completed.stderr] if part).strip()
    return output[:20000].strip()


def capture_command_reference(tool: dict[str, Any], repo_root: Path) -> dict[str, str]:
    commands = [str(tool.get("command") or tool["name"]).strip(), *[str(item).strip() for item in tool.get("aliases", [])]]
    commands = [item for item in commands if item]
    if not commands:
        return {"version_text": "", "help_text": "", "man_text": ""}

    env = build_subprocess_env()
    version_text = ""
    help_text = ""
    man_text = ""

    for command in commands:
        if not version_text:
            for args in ([command, "--version"], [command, "-version"], [command, "-V"]):
                output = _run_command_capture(list(args), repo_root, env, timeout=5)
                if output:
                    version_text = f"$ {' '.join(args)}\n{output}"
                    break

        if not help_text:
            for args in ([command, "--help"], [command, "-h"], [command, "-help"]):
                output = _run_command_capture(list(args), repo_root, env, timeout=8)
                if output:
                    help_text = f"$ {' '.join(args)}\n{output}"
                    break
            if not help_text:
                output = _run_command_capture([command], repo_root, env, timeout=5)
                if output and "usage" in output.lower():
                    help_text = f"$ {command}\n{output}"

        if not man_text:
            man_path = _run_command_capture(["man", "-w", command], repo_root, env, timeout=5)
            if man_path:
                shell_cmd = f"MANPAGER=cat man {shlex.quote(command)} | col -b"
                output = _run_command_capture(["sh", "-lc", shell_cmd], repo_root, env, timeout=8)
                if output:
                    man_text = output

        if version_text and help_text and man_text:
            break

    return {
        "version_text": version_text,
        "help_text": help_text,
        "man_text": man_text,
    }


def render_command_reference_markdown(tool: dict[str, Any]) -> str:
    lines = [
        f"# {tool['name']} Help Reference",
        "",
        f"- Command: `{tool.get('command') or tool['name']}`",
        f"- Sources: {', '.join(tool.get('sources', [])) or 'unknown'}",
    ]
    if tool.get("path"):
        lines.append(f"- Local executable: `{tool['path']}`")
    if tool.get("summary"):
        lines.append(f"- Summary: {tool['summary']}")
    if tool.get("package_names"):
        lines.append(f"- Package names: {', '.join(tool['package_names'])}")
    lines.extend(
        [
            "",
            "## Captured Version",
            "",
            "```text",
            str(tool.get("version_text", "")).strip() or "No version text captured.",
            "```",
            "",
            "## Captured Help",
            "",
            "```text",
            str(tool.get("help_text", "")).strip() or "No help text captured.",
            "```",
            "",
            "## Captured Man Page",
            "",
            "```text",
            str(tool.get("man_text", "")).strip() or "No man page captured.",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def _should_skip_existing(skill_dir: Path) -> bool:
    if not skill_dir.exists():
        return False
    generated_marker = skill_dir / "references" / "help.md"
    return not generated_marker.exists()


def generate_skill_for_tool(
    tool: dict[str, Any],
    output_root: Path,
    render_mode: str = "auto",
) -> dict[str, Path]:
    skill_dir = output_root / str(tool["name"])
    skill_path = skill_dir / "SKILL.md"
    help_path = skill_dir / "references" / "help.md"

    skill_markdown = render_skill_from_help.render_skill_markdown(tool, mode=render_mode)
    help_markdown = render_command_reference_markdown(tool)

    _write_text(skill_path, skill_markdown)
    _write_text(help_path, help_markdown)

    return {
        "skill_dir": skill_dir,
        "skill_path": skill_path,
        "help_path": help_path,
    }


def write_catalog_doc(
    catalog_path: Path,
    existing_domain_skills: Iterable[str],
    generated_tools: Iterable[dict[str, Any]],
) -> Path:
    existing = sorted(str(item) for item in existing_domain_skills)
    generated = sorted(generated_tools, key=lambda item: str(item["name"]))

    lines = [
        "# Biology Skill Catalog",
        "",
        "This catalog is refreshed by `scripts/skills/generate_bio_skills.py`.",
        "",
        "## Existing Domain Skills",
        "",
        "| Skill | Status |",
        "| --- | --- |",
    ]
    for skill_name in existing:
        lines.append(f"| {skill_name} | existing-domain |")

    lines.extend(
        [
            "",
            "## Generated Tool Skills",
            "",
            "| Skill | Status | Sources |",
            "| --- | --- | --- |",
        ]
    )
    for tool in generated:
        sources = ", ".join(tool.get("sources", [])) or "unknown"
        lines.append(f"| {tool['name']} | generated-tool | {sources} |")

    lines.append("")
    _write_text(catalog_path, "\n".join(lines))
    return catalog_path


def generate_skills(
    repo_root: Path,
    output_root: Path,
    render_mode: str = "auto",
    selected_tools: set[str] | None = None,
    dry_run: bool = False,
    discover_source: str = "combined",
    continue_on_error: bool = False,
    failures: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    discovered = discover_bio_tools.discover_tools(repo_root, source=discover_source)
    generated: list[dict[str, Any]] = []
    eligible_tools: list[dict[str, Any]] = []

    for tool in discovered:
        tool_names = {str(tool["name"]), str(tool.get("command", ""))}
        if selected_tools and tool_names.isdisjoint(selected_tools):
            continue
        skill_dir = output_root / str(tool["name"])
        if _should_skip_existing(skill_dir):
            continue
        eligible_tools.append(tool)

    total = len(eligible_tools)
    print(
        json.dumps(
            {
                "event": "generation_start",
                "total_tools": total,
                "render_mode": render_mode,
                "discover_source": discover_source,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )

    for index, tool in enumerate(eligible_tools, start=1):
        skill_dir = output_root / str(tool["name"])
        enriched_tool = dict(tool)
        if dry_run:
            generated.append(
                {
                    "name": enriched_tool["name"],
                    "sources": enriched_tool.get("sources", []),
                    "skill_dir": skill_dir,
                }
            )
            print(
                json.dumps(
                    {
                        "event": "tool_dry_run",
                        "index": index,
                        "total_tools": total,
                        "tool": enriched_tool["name"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
            continue

        print(
            json.dumps(
                {
                    "event": "tool_start",
                    "index": index,
                    "total_tools": total,
                    "tool": enriched_tool["name"],
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        try:
            references = capture_command_reference(enriched_tool, repo_root)
            enriched_tool.update(references)

            written = generate_skill_for_tool(enriched_tool, output_root=output_root, render_mode=render_mode)
            generated.append(
                {
                    "name": enriched_tool["name"],
                    "sources": enriched_tool.get("sources", []),
                    "skill_dir": written["skill_dir"],
                }
            )
            print(
                json.dumps(
                    {
                        "event": "tool_success",
                        "index": index,
                        "total_tools": total,
                        "tool": enriched_tool["name"],
                        "skill_dir": str(written["skill_dir"]),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
        except Exception as exc:
            failure = {
                "name": enriched_tool["name"],
                "sources": enriched_tool.get("sources", []),
                "error": str(exc),
            }
            if failures is not None:
                failures.append(failure)
            print(
                json.dumps(
                    {
                        "event": "tool_failure",
                        "index": index,
                        "total_tools": total,
                        "tool": enriched_tool["name"],
                        "error": str(exc),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
            if continue_on_error:
                continue
            raise

    return generated


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate project-local biology tool skills.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--output-root", default=".claude/skills", help="Skill output directory.")
    parser.add_argument(
        "--catalog-path",
        default="docs/skills/biology-skill-catalog.md",
        help="Catalog markdown output path.",
    )
    parser.add_argument(
        "--render-mode",
        choices=("auto", "offline", "online"),
        default="auto",
        help="Skill rendering mode.",
    )
    parser.add_argument(
        "--source",
        choices=("curated", "linux-all", "combined"),
        default="combined",
        help="Discovery source.",
    )
    parser.add_argument(
        "--tool",
        action="append",
        default=[],
        help="Restrict generation to one or more tool names or commands.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Compute outputs without writing skill files.")
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue generating later skills if one tool fails.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_root = (repo_root / args.output_root).resolve()
    catalog_path = (repo_root / args.catalog_path).resolve()
    selected_tools = {item.strip() for item in args.tool if item.strip()}

    failures: list[dict[str, Any]] = []
    generated = generate_skills(
        repo_root=repo_root,
        output_root=output_root,
        render_mode=args.render_mode,
        selected_tools=selected_tools or None,
        dry_run=args.dry_run,
        discover_source=args.source,
        continue_on_error=args.continue_on_error,
        failures=failures,
    )

    existing_domain_skills = discover_bio_tools.discover_existing_domain_skills(repo_root)
    write_catalog_doc(catalog_path, existing_domain_skills=existing_domain_skills, generated_tools=generated)

    print(
        json.dumps(
            {
                "generated_count": len(generated),
                "generated_tools": generated,
                "failure_count": len(failures),
                "failures": failures,
                "catalog_path": str(catalog_path),
            },
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
