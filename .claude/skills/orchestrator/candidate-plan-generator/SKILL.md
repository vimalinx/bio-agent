---
name: candidate-plan-generator
description: Use when generating multiple candidate plans from a normalized request before the user approves execution.
user-invocable: true
---

# candidate-plan-generator

## Responsibility

Produce at least two viable plans from the same request so the user can choose a strategy instead of inheriting a single hidden assumption set.

## Inputs

- normalized request object
- routing hints
- available workflow options

## Outputs

- conservative plan
- efficient plan
- optional exploratory plan

## Workflow

1. Build a baseline conservative plan with explicit prerequisites.
2. Build a faster or leaner efficient plan with clear trade-offs.
3. Add an exploratory plan only when uncertainty is materially high.
4. Make risks, outputs, and validation criteria explicit per plan.

## Guardrails

- Never return only one plan unless the task is truly degenerate.
- Separate strategy differences from formatting differences.
- Plans should describe stages and validations, not raw shell transcripts.
