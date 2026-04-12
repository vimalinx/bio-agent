from __future__ import annotations

import json
import re
import threading
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from lib.bio_skill_console_server import build_console_control_server
from lib.bio_skill_system import start_session


ROOT = Path(__file__).resolve().parents[1]


def _http_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
    headers: dict[str, str] | None = None,
    expect_status: int | None = None,
) -> dict:
    data = None
    merged_headers = dict(headers or {})
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        merged_headers["Content-Type"] = "application/json"

    request = Request(url, data=data, headers=merged_headers, method=method)
    try:
        with urlopen(request) as response:
            if expect_status is not None:
                assert response.status == expect_status
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if expect_status is None:
            raise
        assert exc.code == expect_status
        return json.loads(exc.read().decode("utf-8"))


def _start_server(session_dir: Path):
    server = build_console_control_server(
        session_dir=session_dir,
        docs_root=ROOT / "docs",
        sessions_root=session_dir.parent / "sessions-root",
        host="127.0.0.1",
        port=0,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def test_console_server_exposes_health_and_live_bundle(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    start_session(
        session_dir=session_dir,
        request_text="I have bulk RNA-seq FASTQ files for treated and control samples and want a differential expression result bundle.",
        goal="Generate candidate plans for RNA-seq differential expression analysis.",
    )

    server, thread = _start_server(session_dir)
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        health = _http_json(f"{base_url}/api/health")
        bundle = _http_json(f"{base_url}/api/session/bundle")

        assert health["ok"] is True
        assert health["default_session_dir"] == str(session_dir.resolve())
        assert health["sessions_endpoint"] == "/api/sessions"
        assert health["bundle_endpoint"] == "/api/session/bundle"
        assert health["plan_markdown_endpoint"] == "/api/session/plan-markdown"
        assert bundle["session"]["session_id"] == session_dir.name
        assert bundle["review"]["recommended_plan_id"].endswith("_conservative")
        assert bundle["candidate_plans"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_can_start_and_switch_to_new_session(tmp_path: Path) -> None:
    session_dir = tmp_path / "existing-session"
    start_session(
        session_dir=session_dir,
        request_text="Initial RNA-seq request kept only to seed the server.",
        goal="Seed session for start endpoint test.",
    )

    server, thread = _start_server(session_dir)
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        create_result = _http_json(
            f"{base_url}/api/session/start",
            method="POST",
            payload={
                "request_text": "I want a protein structure analysis workflow for a small enzyme panel.",
                "goal": "Generate candidate plans for enzyme structure analysis.",
                "session_name": "enzyme-structure-demo",
                "extra_tags": ["protein", "structure"],
            },
        )
        health = _http_json(f"{base_url}/api/health")
        live_bundle = _http_json(f"{base_url}/api/session/bundle")

        assert create_result["action"] == "start_session"
        assert Path(create_result["session_dir"]).name.startswith("enzyme-structure-demo-")
        assert create_result["bundle"]["session"]["session_id"] == Path(create_result["session_dir"]).name
        assert create_result["bundle"]["session"]["approved_plan_id"] is None
        assert health["default_session_dir"] == create_result["session_dir"]
        assert live_bundle["session"]["session_id"] == Path(create_result["session_dir"]).name
        assert live_bundle["request"]["request_text"] == "I want a protein structure analysis workflow for a small enzyme panel."
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_lists_known_sessions_and_marks_default(tmp_path: Path) -> None:
    session_a = tmp_path / "session-a"
    session_b = tmp_path / "sessions-root" / "session-b"
    start_session(
        session_dir=session_a,
        request_text="Initial session outside the shared sessions root.",
        goal="Seed default session.",
    )
    start_session(
        session_dir=session_b,
        request_text="Second session inside the sessions root.",
        goal="Seed switchable session.",
    )

    server = build_console_control_server(
        session_dir=session_a,
        docs_root=ROOT / "docs",
        sessions_root=session_b.parent,
        host="127.0.0.1",
        port=0,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        listing = _http_json(f"{base_url}/api/sessions")
        switched_bundle = _http_json(
            f"{base_url}/api/session/bundle?session_dir={quote(str(session_b.resolve()), safe='')}"
        )

        assert listing["default_session_dir"] == str(session_a.resolve())
        assert {item["session_id"] for item in listing["items"]} == {session_a.name, session_b.name}
        default_item = next(item for item in listing["items"] if item["session_id"] == session_a.name)
        assert default_item["is_default"] is True
        assert default_item["session_dir"] == str(session_a.resolve())
        assert switched_bundle["session"]["session_id"] == session_b.name
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_action_endpoint_approves_and_advances_session(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    start_session(
        session_dir=session_dir,
        request_text="I have bulk RNA-seq FASTQ files for treated and control samples and want a differential expression result bundle.",
        goal="Generate candidate plans for RNA-seq differential expression analysis.",
    )

    server, thread = _start_server(session_dir)
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        approve_result = _http_json(
            f"{base_url}/api/session/action",
            method="POST",
            payload={
                "action": "approve_recommended",
                "payload": {"reason": "Approved from server test."},
            },
        )
        advance_result = _http_json(
            f"{base_url}/api/session/action",
            method="POST",
            payload={
                "action": "next_stage",
                "payload": {},
            },
        )

        assert approve_result["bundle"]["session"]["approved_plan_id"].endswith("_conservative")
        assert approve_result["bundle"]["run_review"]["verdict"] == "ready_to_continue"
        assert advance_result["bundle"]["session"]["current_stage"] == "s2"
        assert advance_result["bundle"]["run_status"]["current_stage"] == "s2"
        assert advance_result["bundle"]["history"]["events"][-1]["type"] == "run_advanced"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_can_force_export_skill_from_completed_session(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    start_session(
        session_dir=session_dir,
        request_text="I have paired-end WES FASTQ files and need germline SNP and indel discovery.",
        goal="Generate a germline short variant discovery workflow.",
        workflow_family="germline-short-variant-discovery",
        strategy_profile="bwa-gatk-hardfilter",
    )

    from lib.bio_skill_system import approve_session_plan, advance_session_run
    review = json.loads((session_dir / "review.json").read_text(encoding="utf-8"))
    approve_session_plan(session_dir=session_dir, plan_id=review["recommended_plan_id"])
    advance_session_run(session_dir=session_dir, validation_updates=["input_paths_exist=passed", "reference_bundle_available=passed"])
    advance_session_run(session_dir=session_dir, confirm=True, validation_updates=["analysis_ready_bams_exist=passed", "recalibration_metrics_exist=passed"])
    advance_session_run(session_dir=session_dir, allow_missing_tools=True, validation_updates=["gvcf_bundle_exists=passed"])
    advance_session_run(session_dir=session_dir, allow_missing_tools=True, validation_updates=["joint_vcf_exists=passed"])
    advance_session_run(session_dir=session_dir, validation_updates=["filtered_vcf_exists=passed", "summary_exists=passed"])

    server, thread = _start_server(session_dir)
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        result = _http_json(
            f"{base_url}/api/session/action",
            method="POST",
            payload={
                "action": "export_skill",
                "payload": {
                    "skill_root": str((tmp_path / "skills").resolve()),
                    "force": True,
                },
            },
        )

        assert result["skill_export"]["files"]["skill_markdown"].endswith("SKILL.md")
        assert Path(result["skill_export"]["files"]["skill_markdown"]).exists()
        assert result["skill_export"]["eligibility"]["eligible"] is False
        assert result["bundle"]["skill_crystallization_candidate"]["eligible"] is False
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_can_round_trip_plan_markdown_edits(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    start_session(
        session_dir=session_dir,
        request_text="I have bulk RNA-seq FASTQ files for treated and control samples and want a differential expression result bundle.",
        goal="Generate candidate plans for RNA-seq differential expression analysis.",
    )

    server, thread = _start_server(session_dir)
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        approve_result = _http_json(
            f"{base_url}/api/session/action",
            method="POST",
            payload={
                "action": "approve_recommended",
                "payload": {"reason": "Approved before markdown edit."},
            },
        )
        assert approve_result["bundle"]["session"]["approved_plan_id"].endswith("_conservative")

        encoded_session_dir = quote(str(session_dir.resolve()), safe="")
        markdown_payload = _http_json(
            f"{base_url}/api/session/plan-markdown?session_dir={encoded_session_dir}&approved=true"
        )
        assert markdown_payload["approved"] is True
        assert markdown_payload["plan_id"].endswith("_conservative")
        assert markdown_payload["text"].startswith("# Bio Agent Plan Editor")

        updated_text = re.sub(
            r"^summary: .*$",
            "summary: User-edited plan summary from the console server test.",
            markdown_payload["text"],
            count=1,
            flags=re.MULTILINE,
        )
        apply_result = _http_json(
            f"{base_url}/api/session/action",
            method="POST",
            payload={
                "action": "approve_plan_document",
                "payload": {
                    "plan_text": updated_text,
                    "file_name": "editable-plan.md",
                    "reason": "Edited through the console server.",
                },
            },
        )

        assert apply_result["bundle"]["approved_plan"]["summary"] == "User-edited plan summary from the console server test."
        assert apply_result["bundle"]["session"]["latest_approval_reason"] == "Edited through the console server."
        assert apply_result["bundle"]["session"]["latest_plan_change_count"] > 0
        assert apply_result["bundle"]["history"]["events"][-1]["type"] == "plan_approved"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_start_endpoint_applies_family_strategy_tags(tmp_path: Path) -> None:
    session_dir = tmp_path / "seed-session"
    start_session(
        session_dir=session_dir,
        request_text="Seed existing session for family strategy start test.",
        goal="Seed server.",
    )

    server, thread = _start_server(session_dir)
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        result = _http_json(
            f"{base_url}/api/session/start",
            method="POST",
            payload={
                "request_text": "Plan a bulk RNA-seq differential expression workflow with explicit QC and DE testing. Use the Salmon + tximport strategy.",
                "goal": "Generate a staged bulk RNA-seq differential expression plan.",
                "session_name": "bulk-rnaseq-salmon-tximport",
                "extra_tags": ["rnaseq", "differential-expression", "strategy-salmon-tximport"],
            },
        )

        first_plan = result["bundle"]["candidate_plans"][0]
        assert result["bundle"]["request"]["request_tags"]
        assert first_plan["selected_strategy_profile"] == "salmon-tximport"
        assert first_plan["selected_strategy_label"] == "Salmon + tximport"
        assert "Salmon + tximport" in first_plan["summary"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_start_endpoint_accepts_workflow_family_defaults(tmp_path: Path) -> None:
    session_dir = tmp_path / "seed-session"
    start_session(
        session_dir=session_dir,
        request_text="Seed existing session for workflow family default test.",
        goal="Seed server.",
    )

    server, thread = _start_server(session_dir)
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        result = _http_json(
            f"{base_url}/api/session/start",
            method="POST",
            payload={
                "workflow_family": "germline-short-variant-discovery",
                "strategy_profile": "bwa-gatk-hardfilter",
            },
        )

        assert Path(result["session_dir"]).name.startswith("germline-short-variants-bwa-gatk-hardfilter-")
        assert result["bundle"]["candidate_plans"][0]["selected_strategy_profile"] == "bwa-gatk-hardfilter"
        assert "strategy-bwa-gatk-hardfilter" in result["bundle"]["request"]["request_tags"]
        assert result["bundle"]["request"]["request_text"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_rejects_disallowed_browser_origin(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    start_session(
        session_dir=session_dir,
        request_text="Seed session for CORS test.",
        goal="Seed server.",
    )

    server, thread = _start_server(session_dir)
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        payload = _http_json(
            f"{base_url}/api/health",
            headers={"Origin": "https://evil.example"},
            expect_status=403,
        )

        assert payload["ok"] is False
        assert payload["error_type"] == "OriginNotAllowed"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_rejects_session_dir_outside_allowed_roots(tmp_path: Path) -> None:
    default_session = tmp_path / "default-session"
    disallowed_session = tmp_path / "outside" / "other-session"
    start_session(
        session_dir=default_session,
        request_text="Seed default session.",
        goal="Seed server.",
    )
    start_session(
        session_dir=disallowed_session,
        request_text="Session outside the configured sessions root.",
        goal="Seed disallowed path.",
    )

    server = build_console_control_server(
        session_dir=default_session,
        docs_root=ROOT / "docs",
        sessions_root=tmp_path / "sessions-root",
        host="127.0.0.1",
        port=0,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        payload = _http_json(
            f"{base_url}/api/session/bundle?session_dir={quote(str(disallowed_session.resolve()), safe='')}",
            expect_status=400,
        )

        assert payload["ok"] is False
        assert "outside the allowed session roots" in payload["error"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_console_server_export_rejects_output_path_outside_session_dir(tmp_path: Path) -> None:
    session_dir = tmp_path / "session"
    start_session(
        session_dir=session_dir,
        request_text="Seed session for export path guard.",
        goal="Seed server.",
    )

    server, thread = _start_server(session_dir)
    try:
        base_url = f"http://127.0.0.1:{server.server_address[1]}"
        payload = _http_json(
            f"{base_url}/api/session/action",
            method="POST",
            payload={
                "action": "export_bundle_file",
                "payload": {
                    "output_path": str((tmp_path / "escape.json").resolve()),
                },
            },
            expect_status=400,
        )

        assert payload["ok"] is False
        assert "must stay inside the session directory" in payload["error"]
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
