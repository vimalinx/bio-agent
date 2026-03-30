---
name: skill-router
description: Use when expanding an approved plan into stage-by-stage candidate skills drawn from the local skill registry.
user-invocable: true
---

# skill-router

## Responsibility

Map each approved plan stage to a candidate set of workflow, atomic, and policy skills using registry metadata instead of ad hoc selection.

## Inputs

- approved plan
- skill registry
- workflow registry
- routing rules

## Outputs

- execution draft
- stage-to-skill mapping
- routing rationale

## Workflow

1. Read the plan stages and required outputs.
2. Match stages to workflow or atomic skills using tags and registry contracts.
3. Attach policy skills for validation and guardrails.
4. Produce a stage execution draft with rationale.

## Guardrails

- Prefer registry-backed routing over intuition.
- More than one candidate skill is acceptable when selection remains deferred.
- Route policy skills explicitly; do not assume they will appear later.
