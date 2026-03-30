---
name: run-resumer
description: Use when resuming a paused or interrupted run from saved run state instead of regenerating the plan from scratch.
user-invocable: true
---

# run-resumer

## Responsibility

Recover execution context from a stored run object so the agent can continue from the right stage with the right artifacts and decisions in view.

## Inputs

- run state
- approved plan

## Outputs

- resume context
- next executable stage
- unresolved blockers

## Workflow

1. Read run status, current stage, and previous decisions.
2. Identify the last validated completed stage.
3. Rebuild the next-step context from plan plus run artifacts.
4. Resume from the saved point instead of re-planning the whole request.

## Guardrails

- Never discard prior user decisions without explicit reason.
- Resume should preserve artifact lineage and issue history.
- If run state is inconsistent, stop and request repair instead of guessing.
