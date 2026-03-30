---
name: plan-comparator
description: Use when comparing candidate plans and explaining trade-offs so the user can select or modify a plan.
user-invocable: true
---

# plan-comparator

## Responsibility

Turn multiple candidate plans into a clear user-facing comparison that highlights differences in assumptions, cost, risk, and outputs.

## Inputs

- candidate plans
- request summary

## Outputs

- comparison table
- recommendation
- explicit open questions

## Workflow

1. Compare plans on goal fit, assumptions, cost, and risk.
2. State where plans differ structurally, not just cosmetically.
3. Recommend one plan and explain why.
4. Call out fields the user can edit without destabilizing execution.

## Guardrails

- Do not hide trade-offs behind vague summaries.
- Recommendation is required, but user choice remains primary.
- Keep the comparison tied to execution consequences.
