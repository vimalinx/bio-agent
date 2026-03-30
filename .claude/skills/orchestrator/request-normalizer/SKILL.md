---
name: request-normalizer
description: Use when turning a natural-language biology request into a structured request object before planning.
user-invocable: true
---

# request-normalizer

## Responsibility

Convert the user's natural-language goal into a structured request that captures inputs, outputs, constraints, and missing information.

## Inputs

- user request text
- optional file paths
- optional project context

## Outputs

- normalized request object
- list of missing fields
- initial request tags

## Workflow

1. Extract the scientific goal and expected deliverable.
2. Identify concrete inputs, references, and constraints already provided.
3. Tag the request with domain and task hints for routing.
4. Explicitly list any missing information needed before execution.

## Guardrails

- Do not generate execution steps here.
- Do not silently invent file paths or references.
- Prefer a partial structured request over a confident but wrong one.
