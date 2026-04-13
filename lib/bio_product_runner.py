from __future__ import annotations

import hashlib
import os
import platform
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lib.bio_skill_system import (
    SESSION_FILES,
    analysis_flow_for_workflow,
    approve_session_plan,
    load_structured_file,
    save_json,
    session_status,
    start_session,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _canonical_artifact_paths(session_dir: Path) -> dict[str, str]:
    return {
        artifact_key: str((session_dir / file_name).resolve())
        for artifact_key, file_name in SESSION_FILES.items()
        if artifact_key in {"run", "run_status", "run_review", "approved_plan", "session", "history"}
    }


def _write_checksums(output_dir: Path, file_names: list[str]) -> Path:
    checksums_path = output_dir / "checksums.sha256"
    lines: list[str] = []
    for name in file_names:
        file_path = output_dir / name
        digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {name}")
    checksums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksums_path


def export_session_repro_bundle(
    session_dir: Path,
    output_dir: Path,
    *,
    invoked_command: str | None = None,
    runner_args: dict[str, Any] | None = None,
) -> dict[str, Any]:
    session_dir = session_dir.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    status_payload = session_status(session_dir)
    session_payload = dict(status_payload.get("session", {}))
    run_status = dict(status_payload.get("run_status", {}))
    run_review = dict(status_payload.get("run_review", {}))
    approved_plan = load_structured_file(session_dir / SESSION_FILES["approved_plan"])
    workflow_id = str(approved_plan.get("source_workflow_id") or "")
    strategy_profile = str(
        approved_plan.get("selected_strategy_profile")
        or approved_plan.get("strategy_type")
        or ""
    )
    analysis_flow = analysis_flow_for_workflow(workflow_id) or {}
    canonical_artifacts = _canonical_artifact_paths(session_dir)

    commands_path = output_dir / "commands.sh"
    environment_path = output_dir / "environment.json"
    provenance_path = output_dir / "provenance.json"
    delivery_bundle_path = output_dir / "delivery-bundle.json"

    hero_invocation = invoked_command or (
        " ".join(
            [
                shlex.quote(sys.executable),
                shlex.quote(str(REPO_ROOT / "scripts" / "bio_skill_system.py")),
                "hero-run",
                "--session-dir",
                shlex.quote(str(session_dir)),
                "--workflow-family",
                shlex.quote(workflow_id),
            ]
            + (
                ["--strategy-profile", shlex.quote(strategy_profile)]
                if strategy_profile
                else []
            )
        )
    )
    command_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        f"# workflow_family: {workflow_id}",
        f"# strategy_profile: {strategy_profile or '-'}",
        f"# session_dir: {session_dir}",
        "",
        "# product-facing command",
        hero_invocation,
        "",
        "# canonical control-plane truth",
        f"{shlex.quote(sys.executable)} {shlex.quote(str(REPO_ROOT / 'scripts' / 'bio_skill_system.py'))} session-status --session-dir {shlex.quote(str(session_dir))}",
        f"{shlex.quote(sys.executable)} {shlex.quote(str(REPO_ROOT / 'scripts' / 'bio_skill_system.py'))} session-export-repro-bundle --session-dir {shlex.quote(str(session_dir))} --output-dir {shlex.quote(str(output_dir))}",
    ]
    commands_path.write_text("\n".join(command_lines) + "\n", encoding="utf-8")
    try:
        os.chmod(commands_path, 0o755)
    except OSError:
        pass

    environment_payload = {
        "generated_at": _now_iso(),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "platform": platform.platform(),
        "cwd": str(REPO_ROOT),
        "path": os.environ.get("PATH", ""),
    }
    save_json(environment_payload, environment_path)

    delivery_bundle_payload = {
        "generated_at": _now_iso(),
        "session_id": session_payload.get("session_id"),
        "workflow_family": workflow_id,
        "strategy_profile": strategy_profile or None,
        "run_status": run_status.get("status"),
        "run_verdict": run_review.get("verdict"),
        "delivery_state": "planned" if run_status.get("status") != "completed" else "recorded",
        "items": [
            {
                "name": item,
                "status": "pending_execution" if run_status.get("status") != "completed" else "recorded",
            }
            for item in analysis_flow.get("delivery_bundle", [])
        ],
        "canonical_run_artifacts": canonical_artifacts,
    }
    save_json(delivery_bundle_payload, delivery_bundle_path)

    provenance_payload = {
        "generated_at": _now_iso(),
        "generator": "hero-run",
        "session_id": session_payload.get("session_id"),
        "session_dir": str(session_dir),
        "workflow_family": workflow_id,
        "strategy_profile": strategy_profile or None,
        "approved_plan_id": approved_plan.get("plan_id"),
        "request_id": approved_plan.get("request_id"),
        "run_status": run_status.get("status"),
        "run_verdict": run_review.get("verdict"),
        "canonical_run_artifacts": canonical_artifacts,
        "runner_args": runner_args or {},
    }
    save_json(provenance_payload, provenance_path)

    checksums_path = _write_checksums(
        output_dir,
        [
            commands_path.name,
            environment_path.name,
            provenance_path.name,
            delivery_bundle_path.name,
        ],
    )

    return {
        "path": str(output_dir),
        "files": {
            "commands": str(commands_path),
            "environment": str(environment_path),
            "provenance": str(provenance_path),
            "delivery_bundle": str(delivery_bundle_path),
            "checksums": str(checksums_path),
        },
        "canonical_artifacts": canonical_artifacts,
    }


def hero_run(
    *,
    session_dir: Path,
    workflow_family: str,
    strategy_profile: str | None = None,
    request_text: str | None = None,
    goal: str | None = None,
    extra_tags: list[str] | None = None,
    repro_dir: Path | None = None,
    invoked_command: str | None = None,
) -> dict[str, Any]:
    session_dir = session_dir.expanduser().resolve()
    start_session(
        session_dir=session_dir,
        request_text=request_text,
        goal=goal,
        extra_tags=extra_tags,
        workflow_family=workflow_family,
        strategy_profile=strategy_profile,
    )
    review_payload = load_structured_file(session_dir / SESSION_FILES["review"])
    recommended_plan_id = str(review_payload["recommended_plan_id"])
    approve_session_plan(
        session_dir=session_dir,
        plan_id=recommended_plan_id,
        reason="Approved by hero-run thin adapter.",
    )
    bundle = export_session_repro_bundle(
        session_dir,
        repro_dir or (session_dir / "repro"),
        invoked_command=invoked_command,
        runner_args={
            "workflow_family": workflow_family,
            "strategy_profile": strategy_profile,
        },
    )
    payload = session_status(session_dir)
    approved_plan = load_structured_file(session_dir / SESSION_FILES["approved_plan"])
    return {
        "session_dir": str(session_dir),
        "workflow_family": workflow_family,
        "strategy_profile": strategy_profile,
        "recommended_plan_id": recommended_plan_id,
        "approved_plan_id": approved_plan.get("plan_id"),
        "run_status": payload.get("run_status"),
        "run_review": payload.get("run_review"),
        "session": payload.get("session"),
        "repro_bundle": bundle,
    }
