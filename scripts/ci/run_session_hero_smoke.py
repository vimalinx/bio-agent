#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CLI_SCRIPT = ROOT / "scripts" / "bio_skill_system.py"
CANONICAL_ARTIFACTS = ("run.json", "run-status.json", "run-review.json")


class SmokeFailure(RuntimeError):
    pass


def run_cli(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        check=True,
        capture_output=True,
        text=True,
        env=merged_env,
    )


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require_canonical_artifacts(session_dir: Path) -> None:
    missing = [name for name in CANONICAL_ARTIFACTS if not (session_dir / name).exists()]
    if missing:
        raise SmokeFailure(f"Missing canonical session artifacts: {', '.join(missing)}")


def run_lane(
    *,
    workflow_family: str,
    expected_block_type: str,
    expected_skill: str,
    strategy_profile: str | None = None,
) -> dict[str, Any]:
    temp_root = Path(tempfile.mkdtemp(prefix="hero-smoke-"))
    session_dir = temp_root / workflow_family
    restricted_env = {"PATH": ""}
    attempts: list[dict[str, Any]] = []

    try:
        args = ["session-start", "--session-dir", str(session_dir), "--workflow-family", workflow_family]
        if strategy_profile:
            args.extend(["--strategy-profile", strategy_profile])
        run_cli(*args, env=restricted_env)

        review = load_json(session_dir / "review.json")
        run_cli(
            "session-approve",
            "--session-dir",
            str(session_dir),
            "--plan-id",
            str(review["recommended_plan_id"]),
            env=restricted_env,
        )
        require_canonical_artifacts(session_dir)

        for _ in range(8):
            status_payload = json.loads(
                run_cli("session-status", "--session-dir", str(session_dir), env=restricted_env).stdout
            )
            run_status = dict(status_payload.get("run_status", {}))
            run_review = dict(status_payload.get("run_review", {}))
            attempts.append(
                {
                    "current_stage": run_status.get("current_stage"),
                    "status": run_status.get("status"),
                    "verdict": run_review.get("verdict"),
                    "next_action": run_review.get("next_action"),
                }
            )

            verdict = str(run_review.get("verdict") or "")
            if verdict == "blocked":
                blocking_issues = list(run_review.get("blocking_issues", []))
                matching_issue = next(
                    (item for item in blocking_issues if item.get("type") == expected_block_type),
                    None,
                )
                if matching_issue is None:
                    raise SmokeFailure(
                        f"{workflow_family} blocked, but expected issue type {expected_block_type!r} was absent: {blocking_issues!r}"
                    )
                skills = [str(item) for item in matching_issue.get("skills", [])]
                if expected_skill not in skills:
                    raise SmokeFailure(
                        f"{workflow_family} blocked on {matching_issue.get('type')!r}, but {expected_skill!r} was absent from {skills!r}"
                    )
                require_canonical_artifacts(session_dir)
                return {
                    "workflow_family": workflow_family,
                    "session_dir": str(session_dir),
                    "result": "blocked-as-expected",
                    "current_stage": run_status.get("current_stage"),
                    "status": run_status.get("status"),
                    "verdict": verdict,
                    "blocking_issue": matching_issue,
                    "attempts": attempts,
                }

            if str(run_status.get("status") or "") == "completed":
                require_canonical_artifacts(session_dir)
                return {
                    "workflow_family": workflow_family,
                    "session_dir": str(session_dir),
                    "result": "completed",
                    "current_stage": run_status.get("current_stage"),
                    "status": run_status.get("status"),
                    "verdict": verdict,
                    "attempts": attempts,
                }

            next_args = ["session-next-stage", "--session-dir", str(session_dir)]
            if verdict == "awaiting_confirmation":
                next_args.append("--confirm")
            run_cli(*next_args, env=restricted_env)

        raise SmokeFailure(f"{workflow_family} did not reach a stable completed/blocked state within 8 transitions")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    results = [
        run_lane(
            workflow_family="rnaseq-differential-expression",
            expected_block_type="unresolved_current_stage_skills",
            expected_skill="pydeseq2",
        ),
        run_lane(
            workflow_family="germline-short-variant-discovery",
            strategy_profile="bwa-gatk-hardfilter",
            expected_block_type="missing_local_tools",
            expected_skill="gatk-haplotypecaller",
        ),
    ]
    sys.stdout.write(json.dumps({"lanes": results}, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
