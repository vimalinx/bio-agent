#!/usr/bin/env python3
"""
LiteFold 工作区桥接 CLI。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from lib.litefold_bridge import (
    build_selfhosted_command,
    build_start_plan,
    build_launch_env,
    collect_preflight,
    collect_status,
    probe_health,
)


def _print_json(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_status(args: argparse.Namespace) -> int:
    status = collect_status(workspace_root=args.workspace_root, base_url=args.url)
    if args.json:
        _print_json(status)
        return 0

    print(f"LiteFold source: {status['source_dir']}")
    print(f"Self-hosted dir: {status['selfhosted_dir']}")
    print(f"Source README: {'yes' if status['source_readme_exists'] else 'no'}")
    print(f"Self-hosted script: {'yes' if status['selfhosted_script_exists'] else 'no'}")
    print(f"Self-hosted Dockerfile: {'yes' if status['selfhosted_dockerfile_exists'] else 'no'}")
    print(f"Docker available: {'yes' if status['docker_available'] else 'no'}")
    print(f"Recommended mode: {status['recommended_launch_mode'] or 'n/a'}")
    if status["recommended_launch_command"]:
        print(f"Recommended command: {status['recommended_launch_command']}")
    if status["warnings"]:
        for warning in status["warnings"]:
            print(f"Warning: {warning}")
    if status["health"] is not None:
        print(f"Health ok: {status['health']['ok']}")
    return 0


def cmd_health(args: argparse.Namespace) -> int:
    health = probe_health(args.url)
    if args.json:
        _print_json(health)
    else:
        print(f"Health url: {health['url']}")
        print(f"Health ok: {health['ok']}")
        if "status_code" in health:
            print(f"Status code: {health['status_code']}")
        if "payload" in health:
            print(f"Payload: {health['payload']}")
        if "error" in health:
            print(f"Error: {health['error']}")
    return 0 if health["ok"] else 1


def cmd_print_selfhosted_command(args: argparse.Namespace) -> int:
    print(
        build_selfhosted_command(
            workspace_root=args.workspace_root,
            python_executable=args.python_executable,
        )
    )
    return 0


def cmd_preflight(args: argparse.Namespace) -> int:
    payload = collect_preflight(
        workspace_root=args.workspace_root,
        python_executable=args.python_executable,
    )
    if args.json:
        _print_json(payload)
        return 0

    print(f"Launch cwd: {payload['launch_context']['cwd']}")
    print(f"Launch script: {payload['launch_context']['script_path']}")
    print(f"Python executable: {payload['launch_context']['python_executable']}")
    print("PYTHONPATH entries:")
    for entry in payload["launch_context"]["pythonpath_entries"]:
        print(f"- {entry}")
    print("External modules:")
    for name in payload["external_python_modules"]:
        print(f"- {name}")
    print(f"Missing modules: {payload['module_probe']['missing_modules']}")
    if payload["requirements_candidates"]:
        print("Requirement candidates:")
        for candidate in payload["requirements_candidates"]:
            print(f"- {candidate['path']}")
    print(f"Workspace requirements: {payload['workspace_installation']['requirements_file']}")
    print(f"Workspace setup script: {payload['workspace_installation']['setup_script']}")
    print(f"Install command: {payload['workspace_installation']['install_command']}")
    for warning in payload["warnings"]:
        print(f"Warning: {warning}")
    return 0


def cmd_start_selfhosted(args: argparse.Namespace) -> int:
    plan = build_start_plan(
        workspace_root=args.workspace_root,
        python_executable=args.python_executable,
    )
    payload = {
        "dry_run": bool(args.dry_run),
        "launch_context": plan["launch_context"],
        "command": plan["command"],
    }

    if args.json or args.dry_run:
        if args.json:
            _print_json(payload)
        else:
            print(f"Launch cwd: {payload['launch_context']['cwd']}")
            print(f"Command: {' '.join(payload['command'])}")
        if args.dry_run:
            return 0

    env = build_launch_env(workspace_root=args.workspace_root)
    completed = subprocess.run(
        plan["command"],
        cwd=plan["launch_context"]["cwd"],
        env=env,
        check=False,
    )
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bio Studio LiteFold bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="查看 LiteFold 挂载状态")
    status_parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path.cwd(),
        help="工作区根目录，默认使用当前目录",
    )
    status_parser.add_argument("--url", help="可选：附带探测 LiteFold /health")
    status_parser.add_argument("--json", action="store_true", help="输出 JSON")
    status_parser.set_defaults(func=cmd_status)

    preflight_parser = subparsers.add_parser("preflight", help="检查 LiteFold 启动前上下文和依赖")
    preflight_parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path.cwd(),
        help="工作区根目录，默认使用当前目录",
    )
    preflight_parser.add_argument(
        "--python-executable",
        default="python",
        help="用于探测模块和启动 selfhosted.py 的 python 命令",
    )
    preflight_parser.add_argument("--json", action="store_true", help="输出 JSON")
    preflight_parser.set_defaults(func=cmd_preflight)

    health_parser = subparsers.add_parser("health", help="探测 LiteFold /health")
    health_parser.add_argument(
        "--url",
        required=True,
        help="LiteFold 服务地址，例如 http://localhost:7114",
    )
    health_parser.add_argument("--json", action="store_true", help="输出 JSON")
    health_parser.set_defaults(func=cmd_health)

    command_parser = subparsers.add_parser(
        "print-selfhosted-command",
        help="打印 LiteFold self-hosted 推荐启动命令",
    )
    command_parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path.cwd(),
        help="工作区根目录，默认使用当前目录",
    )
    command_parser.add_argument(
        "--python-executable",
        default="python",
        help="用于启动 selfhosted.py 的 python 命令",
    )
    command_parser.set_defaults(func=cmd_print_selfhosted_command)

    start_parser = subparsers.add_parser(
        "start-selfhosted",
        help="用桥接层推导出的上下文启动 LiteFold self-hosted 服务",
    )
    start_parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path.cwd(),
        help="工作区根目录，默认使用当前目录",
    )
    start_parser.add_argument(
        "--python-executable",
        default="python",
        help="用于启动 selfhosted.py 的 python 命令",
    )
    start_parser.add_argument("--dry-run", action="store_true", help="只打印启动计划，不实际执行")
    start_parser.add_argument("--json", action="store_true", help="输出 JSON")
    start_parser.set_defaults(func=cmd_start_selfhosted)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
