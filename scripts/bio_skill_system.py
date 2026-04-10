#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from lib.bio_skill_system import (
    advance_run_stage,
    advance_session_run,
    approve_plan,
    approve_session_plan,
    build_execution_draft,
    build_request,
    edit_plan,
    export_session_console_bundle,
    generate_candidate_plans,
    initialize_run,
    load_structured_file,
    pause_run,
    prepare_session_start_inputs,
    resume_run,
    review_plans,
    review_run,
    render_session_plan_markdown,
    resume_session_run,
    save_json,
    session_status,
    start_session,
    summarize_run,
    pause_session_run,
)
from lib.bio_skill_console_server import serve_console_control


def cmd_propose(args: argparse.Namespace) -> int:
    request = build_request(
        request_text=args.request_text,
        goal=args.goal,
        extra_tags=args.tag,
    )
    plans = generate_candidate_plans(request)
    payload = {"request": request, "plans": plans}
    text = save_json(payload, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    proposals = load_structured_file(Path(args.plans_file))
    approved = approve_plan(proposals, args.plan_id)
    text = save_json(approved, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_draft(args: argparse.Namespace) -> int:
    plan = load_structured_file(Path(args.plan_file))
    draft = build_execution_draft(plan)
    text = save_json(draft, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    proposals = load_structured_file(Path(args.plans_file))
    review = review_plans(proposals)
    text = save_json(review, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_edit(args: argparse.Namespace) -> int:
    plan = load_structured_file(Path(args.plan_file))
    edited = edit_plan(
        plan,
        set_summary=args.set_summary,
        set_strategy=args.set_strategy,
        add_risks=args.add_risk,
        require_confirmation_updates=args.require_confirmation,
    )
    text = save_json(edited, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_run_init(args: argparse.Namespace) -> int:
    plan = load_structured_file(Path(args.plan_file))
    run_state = initialize_run(plan)
    text = save_json(run_state, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_run_next_stage(args: argparse.Namespace) -> int:
    run_state = load_structured_file(Path(args.run_file))
    updated = advance_run_stage(
        run_state,
        confirm=bool(args.confirm),
        validation_updates=args.validation,
        artifacts=args.artifact,
    )
    text = save_json(updated, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_run_pause(args: argparse.Namespace) -> int:
    run_state = load_structured_file(Path(args.run_file))
    updated = pause_run(run_state, args.reason)
    text = save_json(updated, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_run_resume(args: argparse.Namespace) -> int:
    run_state = load_structured_file(Path(args.run_file))
    updated = resume_run(run_state)
    text = save_json(updated, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_run_status(args: argparse.Namespace) -> int:
    run_state = load_structured_file(Path(args.run_file))
    summary = summarize_run(run_state)
    text = save_json(summary, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_run_review(args: argparse.Namespace) -> int:
    run_state = load_structured_file(Path(args.run_file))
    execution_draft = load_structured_file(Path(args.draft_file)) if args.draft_file else None
    review = review_run(run_state, execution_draft=execution_draft)
    text = save_json(review, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_session_start(args: argparse.Namespace) -> int:
    manifest = start_session(
        session_dir=Path(args.session_dir),
        request_text=args.request_text,
        goal=args.goal,
        extra_tags=args.tag,
        workflow_family=args.workflow_family,
        strategy_profile=args.strategy_profile,
    )
    text = save_json(manifest, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_session_approve(args: argparse.Namespace) -> int:
    manifest = approve_session_plan(
        session_dir=Path(args.session_dir),
        plan_id=args.plan_id,
        plan_file=Path(args.plan_file) if args.plan_file else None,
        reason=args.reason,
    )
    text = save_json(manifest, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_session_next_stage(args: argparse.Namespace) -> int:
    manifest = advance_session_run(
        session_dir=Path(args.session_dir),
        confirm=bool(args.confirm),
        validation_updates=args.validation,
        artifacts=args.artifact,
        allow_missing_tools=bool(args.allow_missing_tools),
    )
    text = save_json(manifest, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_session_pause(args: argparse.Namespace) -> int:
    manifest = pause_session_run(
        session_dir=Path(args.session_dir),
        reason=args.reason,
    )
    text = save_json(manifest, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_session_resume(args: argparse.Namespace) -> int:
    manifest = resume_session_run(session_dir=Path(args.session_dir))
    text = save_json(manifest, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_session_status(args: argparse.Namespace) -> int:
    payload = session_status(Path(args.session_dir))
    text = save_json(payload, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_session_render_plan(args: argparse.Namespace) -> int:
    text = render_session_plan_markdown(
        session_dir=Path(args.session_dir),
        plan_id=args.plan_id,
        approved=bool(args.approved),
    )
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


def cmd_session_history(args: argparse.Namespace) -> int:
    payload = session_status(Path(args.session_dir)).get("history", {})
    text = save_json(payload, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_session_export_console(args: argparse.Namespace) -> int:
    payload = export_session_console_bundle(
        session_dir=Path(args.session_dir),
        scenario_name=args.scenario_name,
        scenario_note=args.scenario_note,
    )
    text = save_json(payload, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


def cmd_session_serve_console(args: argparse.Namespace) -> int:
    serve_console_control(
        session_dir=Path(args.session_dir) if args.session_dir else None,
        docs_root=Path(args.docs_root),
        sessions_root=Path(args.sessions_root) if args.sessions_root else None,
        host=args.host,
        port=args.port,
        allowed_origins=args.allow_origin or None,
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bio Skill System plan-first orchestration CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    propose_parser = subparsers.add_parser("propose", help="Generate a normalized request and candidate plans")
    propose_parser.add_argument("--request-text", required=True, help="Natural-language user request")
    propose_parser.add_argument("--goal", help="Optional explicit user goal")
    propose_parser.add_argument("--tag", action="append", default=[], help="Optional extra request tag")
    propose_parser.add_argument("--output", help="Optional JSON output file")
    propose_parser.set_defaults(func=cmd_propose)

    approve_parser = subparsers.add_parser("approve", help="Approve one candidate plan by id")
    approve_parser.add_argument("--plans-file", required=True, help="JSON file produced by `propose`")
    approve_parser.add_argument("--plan-id", required=True, help="Selected plan identifier")
    approve_parser.add_argument("--output", help="Optional JSON output file")
    approve_parser.set_defaults(func=cmd_approve)

    draft_parser = subparsers.add_parser("draft", help="Expand an approved plan into an execution draft")
    draft_parser.add_argument("--plan-file", required=True, help="Approved plan file in JSON or YAML")
    draft_parser.add_argument("--output", help="Optional JSON output file")
    draft_parser.set_defaults(func=cmd_draft)

    review_parser = subparsers.add_parser("review", help="Compare candidate plans and emit a recommendation")
    review_parser.add_argument("--plans-file", required=True, help="JSON file produced by `propose`")
    review_parser.add_argument("--output", help="Optional JSON output file")
    review_parser.set_defaults(func=cmd_review)

    edit_parser = subparsers.add_parser("edit", help="Apply simple editable updates to a plan")
    edit_parser.add_argument("--plan-file", required=True, help="Plan file in JSON or YAML")
    edit_parser.add_argument("--set-summary", help="Replace the plan summary")
    edit_parser.add_argument(
        "--set-strategy",
        choices=["conservative", "efficient", "exploratory"],
        help="Replace the strategy type",
    )
    edit_parser.add_argument("--add-risk", action="append", default=[], help="Append a new plan risk")
    edit_parser.add_argument(
        "--require-confirmation",
        action="append",
        default=[],
        help="Set per-stage confirmation state, e.g. s2=false",
    )
    edit_parser.add_argument("--output", help="Optional JSON output file")
    edit_parser.set_defaults(func=cmd_edit)

    run_init_parser = subparsers.add_parser("run-init", help="Initialize a run state from an approved plan")
    run_init_parser.add_argument("--plan-file", required=True, help="Approved plan file in JSON or YAML")
    run_init_parser.add_argument("--output", help="Optional JSON output file")
    run_init_parser.set_defaults(func=cmd_run_init)

    run_next_parser = subparsers.add_parser("run-next-stage", help="Advance the current run by one stage")
    run_next_parser.add_argument("--run-file", required=True, help="Run state file in JSON or YAML")
    run_next_parser.add_argument("--confirm", action="store_true", help="Confirm execution for confirmation-gated stages")
    run_next_parser.add_argument(
        "--validation",
        action="append",
        default=[],
        help="Validation result assignment, e.g. bam_files_exist=passed",
    )
    run_next_parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="Artifact spec, e.g. outputs/sample.bam:bam:Aligned BAM",
    )
    run_next_parser.add_argument("--output", help="Optional JSON output file")
    run_next_parser.set_defaults(func=cmd_run_next_stage)

    run_pause_parser = subparsers.add_parser("run-pause", help="Pause a run with a reason")
    run_pause_parser.add_argument("--run-file", required=True, help="Run state file in JSON or YAML")
    run_pause_parser.add_argument("--reason", required=True, help="Reason to record on pause")
    run_pause_parser.add_argument("--output", help="Optional JSON output file")
    run_pause_parser.set_defaults(func=cmd_run_pause)

    run_resume_parser = subparsers.add_parser("run-resume", help="Resume a paused run")
    run_resume_parser.add_argument("--run-file", required=True, help="Run state file in JSON or YAML")
    run_resume_parser.add_argument("--output", help="Optional JSON output file")
    run_resume_parser.set_defaults(func=cmd_run_resume)

    run_status_parser = subparsers.add_parser("run-status", help="Summarize the current run state for review")
    run_status_parser.add_argument("--run-file", required=True, help="Run state file in JSON or YAML")
    run_status_parser.add_argument("--output", help="Optional JSON output file")
    run_status_parser.set_defaults(func=cmd_run_status)

    run_review_parser = subparsers.add_parser("run-review", help="Review run blockers, gates, and readiness")
    run_review_parser.add_argument("--run-file", required=True, help="Run state file in JSON or YAML")
    run_review_parser.add_argument("--draft-file", help="Optional execution draft file in JSON or YAML")
    run_review_parser.add_argument("--output", help="Optional JSON output file")
    run_review_parser.set_defaults(func=cmd_run_review)

    session_start_parser = subparsers.add_parser(
        "session-start",
        help="Create a session directory with request, candidate plans, and review artifacts",
    )
    session_start_parser.add_argument("--session-dir", required=True, help="Target session directory")
    session_start_parser.add_argument("--request-text", help="Natural-language user request")
    session_start_parser.add_argument("--goal", help="Optional explicit user goal")
    session_start_parser.add_argument("--workflow-family", help="Workflow family id or registry workflow id")
    session_start_parser.add_argument("--strategy-profile", help="Optional strategy profile id within the selected workflow family")
    session_start_parser.add_argument("--tag", action="append", default=[], help="Optional extra request tag")
    session_start_parser.add_argument("--output", help="Optional JSON output file")
    session_start_parser.set_defaults(func=cmd_session_start)

    session_approve_parser = subparsers.add_parser(
        "session-approve",
        help="Approve a plan inside a session and initialize run artifacts",
    )
    session_approve_parser.add_argument("--session-dir", required=True, help="Existing session directory")
    session_approve_parser.add_argument("--plan-id", help="Plan id from plans.json")
    session_approve_parser.add_argument(
        "--plan-file",
        help="Edited plan file to approve instead of selecting by id",
    )
    session_approve_parser.add_argument("--reason", help="Optional approval rationale to record in session history")
    session_approve_parser.add_argument("--output", help="Optional JSON output file")
    session_approve_parser.set_defaults(func=cmd_session_approve)

    session_next_parser = subparsers.add_parser(
        "session-next-stage",
        help="Advance the session run and refresh run-status/run-review artifacts",
    )
    session_next_parser.add_argument("--session-dir", required=True, help="Existing session directory")
    session_next_parser.add_argument("--confirm", action="store_true", help="Confirm execution for gated stages")
    session_next_parser.add_argument(
        "--validation",
        action="append",
        default=[],
        help="Validation result assignment, e.g. bam_files_exist=passed",
    )
    session_next_parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="Artifact spec, e.g. outputs/sample.bam:bam:Aligned BAM",
    )
    session_next_parser.add_argument(
        "--allow-missing-tools",
        action="store_true",
        help="Manually advance even when the current stage depends on tools not available on this machine.",
    )
    session_next_parser.add_argument("--output", help="Optional JSON output file")
    session_next_parser.set_defaults(func=cmd_session_next_stage)

    session_pause_parser = subparsers.add_parser(
        "session-pause",
        help="Pause the active session run and refresh review artifacts",
    )
    session_pause_parser.add_argument("--session-dir", required=True, help="Existing session directory")
    session_pause_parser.add_argument("--reason", required=True, help="Reason to record on pause")
    session_pause_parser.add_argument("--output", help="Optional JSON output file")
    session_pause_parser.set_defaults(func=cmd_session_pause)

    session_resume_parser = subparsers.add_parser(
        "session-resume",
        help="Resume the active session run and refresh review artifacts",
    )
    session_resume_parser.add_argument("--session-dir", required=True, help="Existing session directory")
    session_resume_parser.add_argument("--output", help="Optional JSON output file")
    session_resume_parser.set_defaults(func=cmd_session_resume)

    session_status_parser = subparsers.add_parser(
        "session-status",
        help="Summarize the current session manifest, run status, and run review",
    )
    session_status_parser.add_argument("--session-dir", required=True, help="Existing session directory")
    session_status_parser.add_argument("--output", help="Optional JSON output file")
    session_status_parser.set_defaults(func=cmd_session_status)

    session_render_parser = subparsers.add_parser(
        "session-render-plan",
        help="Render a session plan as editable markdown with an embedded YAML payload",
    )
    session_render_parser.add_argument("--session-dir", required=True, help="Existing session directory")
    session_render_parser.add_argument("--plan-id", help="Candidate plan id from plans.json")
    session_render_parser.add_argument(
        "--approved",
        action="store_true",
        help="Render the approved plan instead of a candidate plan",
    )
    session_render_parser.add_argument("--output", help="Optional markdown output path")
    session_render_parser.set_defaults(func=cmd_session_render_plan)

    session_history_parser = subparsers.add_parser(
        "session-history",
        help="Show the persisted session history timeline",
    )
    session_history_parser.add_argument("--session-dir", required=True, help="Existing session directory")
    session_history_parser.add_argument("--output", help="Optional JSON output file")
    session_history_parser.set_defaults(func=cmd_session_history)

    session_export_parser = subparsers.add_parser(
        "session-export-console",
        help="Export a real session as a console bundle JSON for the web UI",
    )
    session_export_parser.add_argument("--session-dir", required=True, help="Existing session directory")
    session_export_parser.add_argument("--scenario-name", help="Optional scenario title override")
    session_export_parser.add_argument("--scenario-note", help="Optional scenario note override")
    session_export_parser.add_argument("--output", help="Optional JSON output file")
    session_export_parser.set_defaults(func=cmd_session_export_console)

    session_serve_parser = subparsers.add_parser(
        "session-serve-console",
        help="Serve the docs console plus a thin local control API for one session",
    )
    session_serve_parser.add_argument("--session-dir", help="Default session directory for live bundle and actions")
    session_serve_parser.add_argument(
        "--docs-root",
        default=str(REPO_ROOT / "docs"),
        help="Static docs directory to serve",
    )
    session_serve_parser.add_argument(
        "--sessions-root",
        default=str(REPO_ROOT / "sessions"),
        help="Root directory where new sessions created from the web console should be stored",
    )
    session_serve_parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    session_serve_parser.add_argument("--port", type=int, default=8040, help="Bind port")
    session_serve_parser.add_argument(
        "--allow-origin",
        action="append",
        default=[],
        help="Allowed browser Origin for the local control API. Defaults include localhost and the published project docs.",
    )
    session_serve_parser.set_defaults(func=cmd_session_serve_console)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
