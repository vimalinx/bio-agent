---
name: stage-reviewer
description: Use when checking whether a completed stage produced the artifacts and validation evidence required by the approved plan.
user-invocable: true
---

# stage-reviewer

## Responsibility

Review stage outputs against the plan's validation criteria and decide whether the stage is complete, failed, or incomplete.

## Inputs

- artifacts produced by the stage
- stage validation rules
- relevant logs or summaries

## Outputs

- stage verdict
- missing evidence list
- issues to attach to run state

## Workflow

1. Read the stage validation rules from the approved plan.
2. Check whether required artifacts and summaries exist.
3. Mark the stage as complete only when evidence is present.
4. Record issues or missing evidence in run state.

## Guardrails

- Artifact existence alone is not always enough; use validation rules.
- Do not mark a stage complete when evidence is ambiguous.
- Record uncertainty explicitly instead of smoothing it over.
