#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from lib.bio_skill_system import (
    advance_run_stage,
    approve_plan,
    build_execution_draft,
    build_request,
    edit_plan,
    generate_candidate_plans,
    initialize_run,
    load_structured_file,
    pause_run,
    resume_run,
    review_plans,
    review_run,
    save_json,
    summarize_run,
)


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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
