#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
import textwrap
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Mapping


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = SCRIPT_DIR / "config.local.json"
DEFAULT_MAX_COMPLETION_TOKENS = 100000
DEFAULT_REQUEST_RETRIES = 3
DEFAULT_REQUEST_TIMEOUT_SECONDS = 120


def _clean_summary(summary: str) -> str:
    text = " ".join(summary.strip().split())
    if not text:
        return "bioinformatics command-line analysis"
    return text.rstrip(".")


def _build_description(tool: Mapping[str, Any]) -> str:
    name = str(tool.get("name", "tool")).strip()
    summary = _clean_summary(str(tool.get("summary", "")))
    return f"Use when you need {name} for {summary.lower()} in this workspace."


def load_render_config(
    config_path: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    config: dict[str, Any] = {}
    config_path = config_path or DEFAULT_CONFIG_PATH
    if config_path.exists():
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
        for key, value in loaded.items():
            if value is not None:
                config[str(key)] = value

    env_map = dict(os.environ if env is None else env)

    api_key_env = config.get("api_key_env", "BIO_SKILL_FACTORY_API_KEY")
    if api_key_env and env_map.get(api_key_env):
        config["api_key"] = env_map[api_key_env]

    for key, env_names in {
        "api_key": ["BIO_SKILL_FACTORY_API_KEY", "OPENAI_API_KEY"],
        "base_url": ["BIO_SKILL_FACTORY_BASE_URL", "OPENAI_BASE_URL"],
        "model": ["BIO_SKILL_FACTORY_MODEL"],
        "reasoning_effort": ["BIO_SKILL_FACTORY_REASONING_EFFORT"],
        "max_completion_tokens": ["BIO_SKILL_FACTORY_MAX_COMPLETION_TOKENS"],
        "request_retries": ["BIO_SKILL_FACTORY_REQUEST_RETRIES"],
        "request_timeout_seconds": ["BIO_SKILL_FACTORY_REQUEST_TIMEOUT_SECONDS"],
    }.items():
        for env_name in env_names:
            value = env_map.get(env_name, "").strip()
            if value:
                config[key] = value
                break

    for key, default_value in {
        "max_completion_tokens": DEFAULT_MAX_COMPLETION_TOKENS,
        "request_retries": DEFAULT_REQUEST_RETRIES,
        "request_timeout_seconds": DEFAULT_REQUEST_TIMEOUT_SECONDS,
    }.items():
        config[key] = _coerce_positive_int(config.get(key), default_value)

    return config


def _coerce_positive_int(value: Any, default: int) -> int:
    try:
        coerced = int(str(value).strip())
    except (AttributeError, TypeError, ValueError):
        return default
    return coerced if coerced > 0 else default


def _config_is_complete(config: Mapping[str, Any]) -> bool:
    return bool(config.get("api_key") and config.get("base_url") and config.get("model"))


def _build_offline_markdown(tool: Mapping[str, Any]) -> str:
    name = str(tool.get("name", "tool")).strip()
    command = str(tool.get("command") or name).strip()
    summary = _clean_summary(str(tool.get("summary", "")))
    path = str(tool.get("path", "")).strip()
    help_reference = "references/help.md"

    path_line = f"- Local executable: `{path}`" if path else "- Local executable: resolve with `which {command}` before running"

    body = f"""---
name: {name}
description: {_build_description(tool)}
disable-model-invocation: true
user-invocable: true
---

# {name}

Use this skill when `{command}` is the right local tool for the task and you want a concise workflow anchored to this repository.

## Quick Start

- Command: `{command}`
{path_line}
- Raw local help snapshot: [{help_reference}]({help_reference})

## What This Tool Is Good For

- {summary}
- Fast inspection of the tool's supported flags before writing a longer workflow
- Converting the user's biology request into a concrete local CLI run

## Recommended Workflow

1. Read `references/help.md` to confirm the exact subcommand or flag set.
2. Check that input paths, reference files, and output locations are explicit.
3. Run the smallest command that answers the current question before scaling up.
4. Validate the output format and summary statistics before chaining more tools.

## Guardrails

- Prefer reproducible commands with explicit inputs and outputs.
- Record version or path details when the result depends on a specific local binary.
- Do not assume a pipeline wrapper when the help text only documents a single CLI tool.
"""
    return textwrap.dedent(body).strip() + "\n"


def _compose_chat_completions_url(base_url: str) -> str:
    trimmed = base_url.rstrip("/")
    if trimmed.endswith("/chat/completions"):
        return trimmed
    return f"{trimmed}/chat/completions"


def _extract_content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text") or item.get("content") or ""))
        return "".join(parts)
    return ""


def _extract_choice_text(choice: Mapping[str, Any]) -> str:
    message = choice.get("message")
    if isinstance(message, Mapping):
        return _extract_content_text(message.get("content", ""))

    delta = choice.get("delta")
    if isinstance(delta, Mapping):
        return _extract_content_text(delta.get("content", ""))

    return ""


def _extract_message_text(payload: Mapping[str, Any]) -> str:
    choices = payload.get("choices", [])
    if not choices:
        return ""
    return "".join(_extract_choice_text(choice) for choice in choices if isinstance(choice, Mapping)).strip()


def _extract_response_text(body: str) -> str:
    stripped = body.strip()
    if not stripped:
        return ""

    if stripped.startswith("{"):
        return _extract_message_text(json.loads(stripped)).strip()

    if "data:" not in stripped:
        return ""

    parts: list[str] = []
    for raw_line in stripped.splitlines():
        line = raw_line.strip()
        if not line.startswith("data:"):
            continue
        payload_text = line[5:].strip()
        if not payload_text or payload_text == "[DONE]":
            continue
        try:
            event = json.loads(payload_text)
        except json.JSONDecodeError:
            continue
        text = _extract_message_text(event)
        if text:
            parts.append(text)
    return "".join(parts).strip()


def _normalize_skill_markdown(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    return stripped


def _build_online_prompt(tool: Mapping[str, Any]) -> str:
    name = str(tool.get("name", "tool")).strip()
    command = str(tool.get("command") or name).strip()
    summary = _clean_summary(str(tool.get("summary", "")))
    path = str(tool.get("path", "")).strip()
    version_text = str(tool.get("version_text", "")).strip()[:2000]
    help_text = str(tool.get("help_text", "")).strip()[:12000]
    man_text = str(tool.get("man_text", "")).strip()[:6000]

    prompt = f"""
    Generate ONLY the final markdown contents of `SKILL.md` for a Claude Code skill describing the local bioinformatics command `{name}`.

    Hard requirements:
    - Return only markdown, with no surrounding code fences
    - Include YAML frontmatter
    - `name` must be `{name}`
    - `description` must begin with `Use when`
    - Include `disable-model-invocation: true`
    - Include `user-invocable: true`
    - Mention `references/help.md` instead of copying the full reference material
    - Ground every claim in the provided summary, version, help, or man text
    - Keep the result concise, operational, and standardized
    - Use exactly these top-level sections in this order:
      1. `# {name}`
      2. `## Quick Start`
      3. `## What This Tool Is Good For`
      4. `## Recommended Workflow`
      5. `## Guardrails`
    - `## Quick Start` must include bullets for command, local executable when available, and the `references/help.md` link
    - `## Recommended Workflow` must be a 4-step numbered list
    - `## Guardrails` must contain 3 concise bullets
    - Do not invent unsupported subcommands, file formats, or pipeline wrappers

    Tool metadata:
    - Name: {name}
    - Command: {command}
    - Summary: {summary}
    - Local executable: {path or "not provided"}

    Captured version text:
    {version_text or "(none captured)"}

    Captured help text:
    {help_text or "(none captured)"}

    Captured man page excerpt:
    {man_text or "(none captured)"}
    """
    return textwrap.dedent(prompt).strip()


def _skill_markdown_is_valid(text: str, tool_name: str) -> bool:
    required_fragments = [
        f"name: {tool_name}",
        "description: Use when",
        "disable-model-invocation: true",
        "user-invocable: true",
        "## Quick Start",
        "## What This Tool Is Good For",
        "## Recommended Workflow",
        "## Guardrails",
        "references/help.md",
    ]
    return text.startswith("---") and all(fragment in text for fragment in required_fragments)


def _candidate_reasoning_efforts(config: Mapping[str, Any]) -> list[str]:
    configured = str(config.get("reasoning_effort", "") or "").strip().lower()
    if not configured:
        return [""]

    order = ["xhigh", "high", "medium", "low", ""]
    if configured not in order:
        return [configured, ""]

    start_index = order.index(configured)
    return order[start_index:]


def _request_chat_completion(payload: Mapping[str, Any], config: Mapping[str, Any]) -> str:
    request = urllib.request.Request(
        _compose_chat_completions_url(str(config["base_url"])),
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=float(config["request_timeout_seconds"])) as response:
        return response.read().decode("utf-8", errors="replace")


def _render_online(tool: Mapping[str, Any], config: Mapping[str, Any]) -> str:
    prompt = _build_online_prompt(tool)
    attempts = max(int(config["request_retries"]), 1)
    errors: list[str] = []

    for reasoning_effort in _candidate_reasoning_efforts(config):
        payload: dict[str, Any] = {
            "model": str(config["model"]),
            "messages": [
                {
                    "role": "system",
                    "content": "You write concise Claude Code skills for local command-line tools.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "max_completion_tokens": int(config["max_completion_tokens"]),
            "stream": False,
        }
        if reasoning_effort:
            payload["reasoning_effort"] = reasoning_effort

        for attempt in range(1, attempts + 1):
            try:
                body = _request_chat_completion(payload, config)
            except urllib.error.HTTPError as error:
                error_body = error.read().decode("utf-8", errors="replace").strip()
                errors.append(
                    f"HTTP {error.code} on attempt {attempt} with reasoning={reasoning_effort or 'none'}: {error_body[:240]}"
                )
                if attempt < attempts:
                    time.sleep(0.5 * attempt)
                continue
            except urllib.error.URLError as error:
                errors.append(f"URL error on attempt {attempt} with reasoning={reasoning_effort or 'none'}: {error}")
                if attempt < attempts:
                    time.sleep(0.5 * attempt)
                continue
            except TimeoutError as error:
                errors.append(
                    f"Timeout on attempt {attempt} with reasoning={reasoning_effort or 'none'}: {error}"
                )
                if attempt < attempts:
                    time.sleep(0.5 * attempt)
                continue

            text = _normalize_skill_markdown(_extract_response_text(body))
            if _skill_markdown_is_valid(text, str(tool.get("name", ""))):
                return text + ("\n" if not text.endswith("\n") else "")

            errors.append(
                f"Malformed or empty response on attempt {attempt} with reasoning={reasoning_effort or 'none'}: {body[:240]}"
            )
            if attempt < attempts:
                time.sleep(0.5 * attempt)

    raise ValueError("Online renderer returned no valid SKILL.md content. " + " | ".join(errors[-6:]))


def render_skill_markdown(
    tool: Mapping[str, Any],
    mode: str = "auto",
    config_path: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> str:
    selected_mode = mode.strip().lower()
    if selected_mode not in {"auto", "offline", "online"}:
        raise ValueError(f"Unsupported render mode: {mode}")

    config = load_render_config(config_path=config_path, env=env)
    can_render_online = _config_is_complete(config)

    if selected_mode == "offline":
        return _build_offline_markdown(tool)

    if selected_mode == "online":
        if not can_render_online:
            raise ValueError("Online rendering requested but API configuration is incomplete.")
        return _render_online(tool, config)

    if can_render_online:
        try:
            return _render_online(tool, config)
        except (urllib.error.URLError, TimeoutError, ValueError):
            return _build_offline_markdown(tool)

    return _build_offline_markdown(tool)
