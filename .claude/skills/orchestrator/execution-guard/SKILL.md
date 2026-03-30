---
name: execution-guard
description: Use when deciding whether a plan stage should continue automatically, pause for confirmation, or escalate because of risk.
user-invocable: true
---

# execution-guard

## Responsibility

Evaluate stage-level execution risk and decide whether the agent should continue, pause, or escalate before acting.

## Inputs

- stage definition
- current environment state
- risk metadata

## Outputs

- go
- pause-for-confirmation
- escalate-with-reason

## Workflow

1. Inspect the stage for external downloads, long-running jobs, destructive writes, and missing prerequisites.
2. Compare detected risks against routing rules.
3. Decide whether the stage can continue or should pause.
4. State the decision and the reason in run state.

## Guardrails

- High-cost or destructive actions should pause by default.
- Missing prerequisites should not be treated as soft warnings.
- The decision must be persisted to run state.
