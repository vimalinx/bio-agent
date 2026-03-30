---
name: plan-editor
description: Use when incorporating user changes into a selected plan while preserving execution structure and validation semantics.
user-invocable: true
---

# plan-editor

## Responsibility

Apply user edits to a selected plan and return a structurally coherent plan that is safe to approve.

## Inputs

- selected plan
- user edits or constraints

## Outputs

- updated plan
- change summary
- validation impact notes

## Workflow

1. Identify which plan fields the user changed.
2. Apply the change without breaking stage order or validation semantics.
3. Recompute affected risks, prerequisites, and candidate skills.
4. Return a revised plan plus the consequences of the edit.

## Guardrails

- Do not treat freeform user edits as executable commands.
- If a user edit breaks the plan, say so explicitly and propose repair options.
- Approval should be reset after substantial structural changes.
