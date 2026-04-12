from __future__ import annotations

import json
import re
import tempfile
from datetime import datetime
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from lib.bio_skill_system import (
    advance_session_run,
    approve_session_plan,
    export_session_as_skill,
    export_session_console_bundle,
    pause_session_run,
    prepare_session_start_inputs,
    render_session_plan_markdown,
    resume_session_run,
    save_json,
    start_session,
)


DEFAULT_ALLOWED_ORIGIN_RULES = (
    "http://127.0.0.1",
    "http://localhost",
    "https://vimalinx.xyz",
    "https://www.vimalinx.xyz",
)


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _default_export_path_for_session(session_dir: Path) -> Path:
    return session_dir.resolve() / "session-export.json"


def _truthy_query(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _slugify_session_name(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return value[:48] or "bio-session"


def _allocate_session_dir(sessions_root: Path, session_name: str | None, request_text: str) -> Path:
    sessions_root = sessions_root.resolve()
    sessions_root.mkdir(parents=True, exist_ok=True)

    preferred = _slugify_session_name(session_name or request_text)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    candidate = sessions_root / f"{preferred}-{timestamp}"
    counter = 2
    while candidate.exists():
        candidate = sessions_root / f"{preferred}-{timestamp}-{counter}"
        counter += 1
    return candidate


def _path_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _origin_allowed(origin: str | None, allowed_rules: tuple[str, ...]) -> bool:
    if not origin:
        return True

    parsed_origin = urlparse(origin)
    if parsed_origin.scheme not in {"http", "https"} or not parsed_origin.hostname:
        return False

    for rule in allowed_rules:
        parsed_rule = urlparse(rule)
        if parsed_origin.scheme != parsed_rule.scheme:
            continue
        if (parsed_origin.hostname or "").lower() != (parsed_rule.hostname or "").lower():
            continue
        if parsed_rule.port is not None and parsed_origin.port != parsed_rule.port:
            continue
        return True

    return False


def _safe_export_output_path(session_dir: Path, raw_output: str | None) -> Path:
    output_path = Path(raw_output).resolve() if raw_output else _default_export_path_for_session(session_dir)
    if output_path.suffix.lower() != ".json":
        raise ValueError("Console export output_path must end with `.json`.")
    if not _path_within(output_path, session_dir.resolve()):
        raise ValueError("Console export output_path must stay inside the session directory.")
    return output_path


def _plan_markdown_payload(
    session_dir: Path,
    *,
    plan_id: str | None = None,
    approved: bool = False,
) -> dict[str, Any]:
    session_dir = session_dir.resolve()
    bundle = export_session_console_bundle(session_dir)
    session = bundle.get("session", {})
    selected_plan_id = plan_id or (
        session.get("approved_plan_id") if approved else session.get("recommended_plan_id")
    )
    return {
        "session_dir": str(session_dir),
        "plan_id": selected_plan_id,
        "approved": approved,
        "file_name": "editable-plan.md",
        "text": render_session_plan_markdown(
            session_dir=session_dir,
            plan_id=plan_id,
            approved=approved,
        ),
    }


def _session_summary(session_dir: Path, *, is_default: bool = False) -> dict[str, Any]:
    session_file = session_dir.resolve() / "session.json"
    if not session_file.exists():
        raise FileNotFoundError(f"Session manifest is missing: {session_file}")
    payload = json.loads(session_file.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid session manifest payload: {session_file}")

    return {
        "session_id": payload.get("session_id") or session_dir.name,
        "session_dir": str(session_dir.resolve()),
        "status": payload.get("status"),
        "current_stage": payload.get("current_stage"),
        "run_status": payload.get("run_status"),
        "run_verdict": payload.get("run_verdict"),
        "next_action": payload.get("next_action"),
        "recommended_plan_id": payload.get("recommended_plan_id"),
        "approved_plan_id": payload.get("approved_plan_id"),
        "history_event_count": payload.get("history_event_count", 0),
        "latest_event_timestamp": payload.get("latest_event_timestamp"),
        "updated_at": payload.get("updated_at"),
        "is_default": is_default,
    }


def _list_sessions(
    sessions_root: Path,
    default_session_dir: Path | None,
    known_session_dirs: set[Path] | None = None,
) -> list[dict[str, Any]]:
    candidates: dict[str, Path] = {}
    if sessions_root.exists():
        for child in sessions_root.iterdir():
            if child.is_dir() and (child / "session.json").exists():
                candidates[str(child.resolve())] = child.resolve()

    for session_dir in known_session_dirs or set():
        session_dir = session_dir.resolve()
        if (session_dir / "session.json").exists():
            candidates[str(session_dir)] = session_dir

    if default_session_dir and (default_session_dir / "session.json").exists():
        candidates[str(default_session_dir.resolve())] = default_session_dir.resolve()

    items = [
        _session_summary(session_dir, is_default=default_session_dir is not None and session_dir.resolve() == default_session_dir.resolve())
        for session_dir in candidates.values()
    ]
    items.sort(
        key=lambda item: (
            str(item.get("updated_at") or item.get("latest_event_timestamp") or ""),
            str(item.get("session_id") or ""),
        ),
        reverse=True,
    )
    return items


def execute_console_action(
    session_dir: Path,
    action: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    session_dir = session_dir.resolve()
    payload = dict(payload or {})

    result: dict[str, Any] = {
        "action": action,
        "session_dir": str(session_dir),
    }

    if action == "approve_recommended":
        review = export_session_console_bundle(session_dir).get("review", {})
        plan_id = payload.get("plan_id") or review.get("recommended_plan_id")
        if not plan_id:
            raise ValueError("No recommended plan_id is available for approval.")
        manifest = approve_session_plan(
            session_dir=session_dir,
            plan_id=str(plan_id),
            reason=payload.get("reason"),
        )
        result["session"] = manifest
    elif action == "approve_plan":
        plan_id = payload.get("plan_id")
        if not plan_id:
            raise ValueError("`approve_plan` requires `plan_id`.")
        manifest = approve_session_plan(
            session_dir=session_dir,
            plan_id=str(plan_id),
            reason=payload.get("reason"),
        )
        result["session"] = manifest
    elif action == "next_stage":
        manifest = advance_session_run(
            session_dir=session_dir,
            confirm=bool(payload.get("confirm")),
            validation_updates=list(payload.get("validation", [])),
            artifacts=list(payload.get("artifact", [])),
            allow_missing_tools=bool(payload.get("allow_missing_tools")),
        )
        result["session"] = manifest
    elif action == "pause_run":
        manifest = pause_session_run(
            session_dir=session_dir,
            reason=str(payload.get("reason") or "Manual checkpoint from console control."),
        )
        result["session"] = manifest
    elif action == "resume_run":
        manifest = resume_session_run(session_dir=session_dir)
        result["session"] = manifest
    elif action == "export_bundle_file":
        raw_output = payload.get("output_path")
        output_path = _safe_export_output_path(
            session_dir,
            str(raw_output).strip() if raw_output else None,
        )
        bundle = export_session_console_bundle(session_dir)
        save_json(bundle, output_path)
        result["output_path"] = str(output_path)
    elif action == "approve_plan_document":
        plan_text = str(payload.get("plan_text") or "")
        if not plan_text.strip():
            raise ValueError("`approve_plan_document` requires non-empty `plan_text`.")
        file_name = str(payload.get("file_name") or "editable-plan.md")
        suffix = Path(file_name).suffix or ".md"
        with tempfile.TemporaryDirectory(prefix="bio-agent-plan-") as temp_dir:
            temp_path = Path(temp_dir) / f"edited-plan{suffix}"
            temp_path.write_text(plan_text, encoding="utf-8")
            manifest = approve_session_plan(
                session_dir=session_dir,
                plan_file=temp_path,
                reason=payload.get("reason"),
            )
        result["session"] = manifest
    elif action == "export_skill":
        raw_skill_root = str(payload.get("skill_root") or "").strip()
        skill_root = Path(raw_skill_root).resolve() if raw_skill_root else (session_dir.parent.parent / ".claude" / "skills").resolve()
        result["skill_export"] = export_session_as_skill(
            session_dir=session_dir,
            skill_root=skill_root,
            skill_name=str(payload.get("skill_name") or "").strip() or None,
            overwrite=bool(payload.get("overwrite")),
            force=bool(payload.get("force")),
        )
    else:
        raise ValueError(f"Unsupported console action: {action}")

    result["bundle"] = export_session_console_bundle(session_dir)
    return result


class BioSkillConsoleHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        server_address: tuple[str, int],
        handler_cls: type[SimpleHTTPRequestHandler],
        *,
        docs_root: Path,
        default_session_dir: Path | None,
        sessions_root: Path,
        allowed_origin_rules: tuple[str, ...],
    ) -> None:
        super().__init__(server_address, handler_cls)
        self.docs_root = docs_root.resolve()
        self.default_session_dir = default_session_dir.resolve() if default_session_dir else None
        self.sessions_root = sessions_root.resolve()
        self.known_session_dirs = {self.default_session_dir} if self.default_session_dir else set()
        self.allowed_origin_rules = allowed_origin_rules


class BioSkillConsoleRequestHandler(SimpleHTTPRequestHandler):
    server: BioSkillConsoleHTTPServer

    def end_headers(self) -> None:
        self._write_cors_headers()
        super().end_headers()

    def do_OPTIONS(self) -> None:
        if self.path.startswith("/api/") and self._reject_disallowed_origin():
            return
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/") and self._reject_disallowed_origin():
            return
        if parsed.path == "/api/health":
            self._send_json(
                {
                    "ok": True,
                    "default_session_dir": str(self.server.default_session_dir) if self.server.default_session_dir else None,
                    "sessions_root": str(self.server.sessions_root),
                    "docs_root": str(self.server.docs_root),
                    "start_endpoint": "/api/session/start",
                    "sessions_endpoint": "/api/sessions",
                    "bundle_endpoint": "/api/session/bundle",
                    "action_endpoint": "/api/session/action",
                    "plan_markdown_endpoint": "/api/session/plan-markdown",
                    "allowed_origins": list(self.server.allowed_origin_rules),
                }
            )
            return

        if parsed.path == "/api/sessions":
            try:
                items = _list_sessions(
                    self.server.sessions_root,
                    self.server.default_session_dir,
                    self.server.known_session_dirs,
                )
            except Exception as exc:  # pragma: no cover - handled by tests via response body
                self._send_error_json(exc)
                return
            self._send_json(
                {
                    "items": items,
                    "default_session_dir": str(self.server.default_session_dir) if self.server.default_session_dir else None,
                    "sessions_root": str(self.server.sessions_root),
                }
            )
            return

        if parsed.path == "/api/session/bundle":
            try:
                session_dir = self._resolve_session_dir(parse_qs(parsed.query))
                bundle = export_session_console_bundle(session_dir)
                self.server.known_session_dirs.add(session_dir.resolve())
            except Exception as exc:  # pragma: no cover - handled by tests via response body
                self._send_error_json(exc)
                return
            self._send_json(bundle)
            return

        if parsed.path == "/api/session/plan-markdown":
            try:
                query = parse_qs(parsed.query)
                session_dir = self._resolve_session_dir(query)
                approved = _truthy_query((query.get("approved") or [None])[0])
                plan_id = (query.get("plan_id") or [None])[0]
                payload = _plan_markdown_payload(
                    session_dir,
                    plan_id=plan_id,
                    approved=approved,
                )
            except Exception as exc:  # pragma: no cover - handled by tests via response body
                self._send_error_json(exc)
                return
            self._send_json(payload)
            return

        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/") and self._reject_disallowed_origin():
            return
        if parsed.path == "/api/session/start":
            try:
                body = self._read_json_body()
                raw_tags = body.get("extra_tags") or []
                if raw_tags is None:
                    raw_tags = []
                if not isinstance(raw_tags, list):
                    raise ValueError("`extra_tags` must be an array when provided.")
                resolved = prepare_session_start_inputs(
                    request_text=str(body.get("request_text") or "").strip() or None,
                    goal=str(body.get("goal") or "").strip() or None,
                    extra_tags=[str(item).strip() for item in raw_tags if str(item).strip()],
                    workflow_family=str(body.get("workflow_family") or "").strip() or None,
                    strategy_profile=str(body.get("strategy_profile") or "").strip() or None,
                    session_name=str(body.get("session_name") or "").strip() or None,
                )
                session_dir = _allocate_session_dir(
                    self.server.sessions_root,
                    session_name=resolved.get("session_name"),
                    request_text=resolved["request_text"],
                )
                manifest = start_session(
                    session_dir=session_dir,
                    request_text=resolved["request_text"],
                    goal=resolved.get("goal"),
                    extra_tags=resolved.get("extra_tags"),
                    workflow_family=resolved.get("workflow_family"),
                    strategy_profile=resolved.get("strategy_profile"),
                )
                self.server.default_session_dir = session_dir.resolve()
                self.server.known_session_dirs.add(session_dir.resolve())
                result = {
                    "action": "start_session",
                    "session_dir": str(session_dir.resolve()),
                    "session": manifest,
                    "bundle": export_session_console_bundle(session_dir),
                }
            except Exception as exc:  # pragma: no cover - handled by tests via response body
                self._send_error_json(exc)
                return

            self._send_json(result)
            return

        if parsed.path != "/api/session/action":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown API endpoint")
            return

        try:
            body = self._read_json_body()
            session_dir = self._resolve_session_dir(body)
            action = str(body.get("action") or "")
            payload = body.get("payload")
            if payload is not None and not isinstance(payload, dict):
                raise ValueError("`payload` must be a JSON object when provided.")
            result = execute_console_action(session_dir, action=action, payload=payload)
        except Exception as exc:  # pragma: no cover - handled by tests via response body
            self._send_error_json(exc)
            return

        self._send_json(result)

    def _read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        payload = json.loads(raw_body.decode("utf-8") or "{}")
        if not isinstance(payload, dict):
            raise ValueError("Expected a JSON object request body.")
        return payload

    def _resolve_session_dir(self, payload: dict[str, Any]) -> Path:
        raw = payload.get("session_dir")
        if isinstance(raw, list):
            raw = raw[0] if raw else None
        if raw:
            session_dir = Path(str(raw)).resolve()
            if self.server.default_session_dir is not None and session_dir == self.server.default_session_dir:
                return session_dir
            if session_dir in self.server.known_session_dirs:
                return session_dir
            if _path_within(session_dir, self.server.sessions_root):
                return session_dir
            raise ValueError("Requested session_dir is outside the allowed session roots.")
        if self.server.default_session_dir is not None:
            return self.server.default_session_dir
        raise ValueError("No session_dir provided and no default session is configured.")

    def _reject_disallowed_origin(self) -> bool:
        origin = self.headers.get("Origin")
        if _origin_allowed(origin, self.server.allowed_origin_rules):
            return False
        self._send_json(
            {
                "ok": False,
                "error_type": "OriginNotAllowed",
                "error": "Origin is not allowed to access the local console API.",
            },
            status=HTTPStatus.FORBIDDEN,
        )
        return True

    def _write_cors_headers(self) -> None:
        if not self.path.startswith("/api/"):
            return
        origin = self.headers.get("Origin")
        if not origin or not _origin_allowed(origin, self.server.allowed_origin_rules):
            return
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Vary", "Origin")

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = _json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, exc: Exception) -> None:
        status = HTTPStatus.BAD_REQUEST if isinstance(exc, ValueError | FileNotFoundError) else HTTPStatus.INTERNAL_SERVER_ERROR
        self._send_json(
            {
                "ok": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
            },
            status=status,
        )


def build_console_control_server(
    *,
    session_dir: Path | None,
    docs_root: Path,
    sessions_root: Path | None,
    host: str,
    port: int,
    allowed_origins: list[str] | None = None,
) -> BioSkillConsoleHTTPServer:
    docs_root = docs_root.resolve()
    default_sessions_root = sessions_root.resolve() if sessions_root else docs_root.parent / "sessions"
    handler_cls = partial(BioSkillConsoleRequestHandler, directory=str(docs_root))
    return BioSkillConsoleHTTPServer(
        (host, port),
        handler_cls,
        docs_root=docs_root,
        default_session_dir=session_dir,
        sessions_root=default_sessions_root,
        allowed_origin_rules=tuple(allowed_origins or DEFAULT_ALLOWED_ORIGIN_RULES),
    )


def serve_console_control(
    *,
    session_dir: Path | None,
    docs_root: Path,
    sessions_root: Path | None,
    host: str,
    port: int,
    allowed_origins: list[str] | None = None,
) -> None:
    server = build_console_control_server(
        session_dir=session_dir,
        docs_root=docs_root,
        sessions_root=sessions_root,
        host=host,
        port=port,
        allowed_origins=allowed_origins,
    )
    print(
        f"Bio Skill Console server listening on http://{host}:{server.server_address[1]} "
        f"for session {server.default_session_dir or '<none>'}"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping Bio Skill Console server.")
    finally:
        server.server_close()
