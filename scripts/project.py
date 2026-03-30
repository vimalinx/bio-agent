#!/usr/bin/env python3
"""
工作区级项目操作入口。
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from lib.create_project import create_project
from lib.workspace_env import build_subprocess_env, resolve_workspace_python


def project_dir(workspace_root: Path, project_name: str) -> Path:
    return workspace_root / "projects" / project_name


def project_scripts_dir(workspace_root: Path, project_name: str) -> Path:
    return project_dir(workspace_root, project_name) / "scripts"


def ensure_project_exists(workspace_root: Path, project_name: str) -> Path:
    project_root = project_dir(workspace_root, project_name)
    scripts_dir = project_scripts_dir(workspace_root, project_name)
    if not project_root.exists() or not scripts_dir.exists():
        raise FileNotFoundError(
            f"找不到项目 {project_name}: {project_root}"
        )
    return scripts_dir


def run_python_entrypoint(
    script_path: Path,
    extra_args: list[str] | None = None,
    extra_env: dict[str, str] | None = None,
) -> int:
    python_executable = resolve_workspace_python()
    args = [str(python_executable), script_path.name]
    if extra_args:
        args.extend(extra_args)
    env = build_subprocess_env(extra_env=extra_env)
    completed = subprocess.run(args, cwd=script_path.parent, env=env)
    return completed.returncode


def cmd_create(args: argparse.Namespace) -> int:
    workspace_root = args.workspace_root
    original_cwd = Path.cwd().resolve()
    try:
        os.chdir(workspace_root)
        create_project(args.project_name, args.type, args.description)
    finally:
        os.chdir(original_cwd)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    scripts_dir = ensure_project_exists(args.workspace_root, args.project_name)
    return run_python_entrypoint(scripts_dir / "validate_project.py")


def cmd_steps(args: argparse.Namespace) -> int:
    scripts_dir = ensure_project_exists(args.workspace_root, args.project_name)
    return run_python_entrypoint(scripts_dir / "pipeline.py", ["--steps"])


def cmd_run(args: argparse.Namespace) -> int:
    scripts_dir = ensure_project_exists(args.workspace_root, args.project_name)
    extra_env = {
        "BIO_STUDIO_WORKSPACE_CLI": "1",
        "BIO_STUDIO_WORKSPACE_ROOT": str(args.workspace_root),
        "BIO_STUDIO_WORKSPACE_CLI_PATH": str(args.workspace_root / "scripts" / "project.py"),
        "BIO_STUDIO_PROJECT_NAME": args.project_name,
    }
    return run_python_entrypoint(
        scripts_dir / "pipeline.py",
        list(args.pipeline_args),
        extra_env=extra_env,
    )


def cmd_workspace_validate(args: argparse.Namespace) -> int:
    script_path = (
        args.workspace_root
        / "projects"
        / "test_env_validation"
        / "scripts"
        / "run_validation.py"
    )
    if not script_path.exists():
        raise FileNotFoundError(f"找不到工作区验证脚本: {script_path}")
    return run_python_entrypoint(script_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bio Studio 工作区项目入口",
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path.cwd(),
        help="工作区根目录，默认使用当前目录",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="创建新项目")
    create_parser.add_argument("project_name", help="项目名称")
    create_parser.add_argument(
        "--type",
        "-t",
        default="generic",
        choices=["generic", "rnaseq", "variant", "phylogeny", "genome"],
        help="项目类型",
    )
    create_parser.add_argument("--description", "-d", default="", help="项目描述")
    create_parser.set_defaults(func=cmd_create)

    validate_parser = subparsers.add_parser("validate", help="运行项目级自检")
    validate_parser.add_argument("project_name", help="项目名称")
    validate_parser.set_defaults(func=cmd_validate)

    steps_parser = subparsers.add_parser("steps", help="列出项目可用步骤")
    steps_parser.add_argument("project_name", help="项目名称")
    steps_parser.set_defaults(func=cmd_steps)

    run_parser = subparsers.add_parser("run", help="从工作区根目录运行项目 pipeline")
    run_parser.add_argument("project_name", help="项目名称")
    run_parser.add_argument("pipeline_args", nargs=argparse.REMAINDER, help="透传给 pipeline.py 的参数")
    run_parser.set_defaults(func=cmd_run)

    workspace_validate_parser = subparsers.add_parser(
        "workspace-validate",
        help="运行 projects/test_env_validation 的工作区级 smoke test",
        description="运行 projects/test_env_validation/scripts/run_validation.py。",
    )
    workspace_validate_parser.set_defaults(func=cmd_workspace_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.workspace_root = args.workspace_root.resolve()

    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
