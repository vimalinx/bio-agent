# Bio Skill System V1 Design

**Date:** 2026-03-29

## Goal

Build a plan-first bioinformatics skill system for agents that converts natural-language requests into candidate plans, lets the user select or revise a plan, and then executes the approved plan in a half-automatic way using a local skill repository plus prompt-based orchestration.

## V1 Scope

The first version is not a full bioinformatics platform and does not try to perfect every domain workflow. Its job is to establish the control plane: request normalization, plan generation, plan selection, skill routing, stage-by-stage execution, pause/resume, and run review. Domain workflows can be added on top of this skeleton later.

## Core Objects

### Request

The `Request` object captures the user's natural-language intent and any concrete context that accompanies it, such as file paths, species, expected outputs, or time constraints. It is the system's normalized input.

### Plan

The `Plan` object is a candidate strategy generated from the request. It is the object the user reviews, compares, edits, and approves. Once approved, it becomes the execution contract rather than a loose explanation.

### Skill

The `Skill` object is the minimal executable capability unit. A skill may represent a single CLI tool, a validation routine, a workflow template, or a control-plane behavior such as routing or review.

### Workflow

The `Workflow` object composes multiple skills into a reusable sequence. Workflows should capture common analysis patterns without becoming rigid monoliths.

### Run

The `Run` object records one concrete execution of one approved plan. It stores stage status, artifacts, decisions, issues, and resume state.

## System Boundary

V1 should be defined as a half-automatic orchestration layer. It is not just a folder of skills and not just a freeform prompt. It sits between user intent and domain execution, stabilizing how requests are interpreted, how plans are compared, and how skills are invoked.

## Directory Structure

```text
bio-agent/
├── .claude/
│   ├── skills/
│   │   ├── atomic/
│   │   ├── workflow/
│   │   ├── orchestrator/
│   │   └── policy/
│   └── agents/
├── registry/
│   ├── skills.yaml
│   ├── workflows.yaml
│   └── routing_rules.yaml
├── schemas/
│   ├── request.schema.json
│   ├── plan.schema.json
│   └── run.schema.json
├── examples/
│   ├── requests/
│   ├── plans/
│   └── runs/
└── docs/
    ├── plans/
    └── system/
```

## End-to-End Flow

The orchestration flow for v1 is:

1. Normalize the user's natural-language request into a structured request.
2. Generate at least two candidate plans.
3. Present plans with clear trade-offs.
4. Let the user choose or modify a plan.
5. Expand the approved plan into an execution draft.
6. Route each stage to a candidate skill set.
7. Execute each stage in a half-automatic way.
8. Validate artifacts and store run state after each stage.
9. Pause when required by risk, missing prerequisites, or user checkpoints.
10. Resume from the stored run state.

## Current Runnable CLI Slice

The current repository now exposes a runnable control-plane chain that covers both planning and execution state:

- `propose`
- `review`
- `approve`
- `edit`
- `draft`
- `run-init`
- `run-next-stage`
- `run-pause`
- `run-resume`
- `run-status`
- `run-review`

The effective v1 path is:

1. `propose` candidate plans from a normalized request.
2. `review` and optionally `edit` the selected plan.
3. `approve` the plan and `draft` the stage-level skill mapping.
4. `run-init` to create the first `Run` object.
5. `run-next-stage` to advance one stage at a time.
6. `run-pause` or confirmation-gated pauses when execution should stop.
7. `run-resume` to continue from the recorded `resume_from` checkpoint.
8. `run-status` to summarize the current execution checkpoint for the user or another agent.
9. `run-review` to evaluate blockers, future risks, and whether the run is truly ready to continue.

## Browser Console Prototype

The current docs package now also includes a browser-viewable control console prototype:

- `docs/system/bio-skill-console.html`
- `docs/system/data/bio-skill-console-demo.json`

Its purpose is to make the control plane visible without waiting for a real frontend application. It shows:

- the normalized request
- candidate plan comparison
- the approved plan stages
- draft-time skill resolution state
- current run-state and next action
- run review verdict, blockers, and future issues

This prototype should remain static and inspectable. It is a design and review surface for the orchestration layer, not a production web app.

## Skill Taxonomy

### Atomic Skills

Atomic skills should wrap a single concrete capability. They must declare inputs, outputs, preconditions, side effects, and whether confirmation is required.

### Workflow Skills

Workflow skills should represent reusable multi-step patterns such as RNA-seq analysis or protein-structure analysis. They are execution templates, not universal controllers.

### Orchestrator Skills

Orchestrator skills define system behavior. They should cover request normalization, candidate plan generation, plan comparison, execution routing, stage review, and run resume.

### Policy Skills

Policy skills provide environment checks, input audit, execution guardrails, output validation, and review checkpoints.

## Plan Schema Principles

The `Plan` object should exist in two forms:

- A human-readable Markdown view for users.
- A structured machine view for routing and execution.

Each plan should minimally contain:

- `plan_id`
- `request_id`
- `title`
- `summary`
- `strategy_type`
- `assumptions`
- `prerequisites`
- `expected_outputs`
- `risks`
- `estimated_cost`
- `stages`
- `approval_state`

Each stage should minimally contain:

- `stage_id`
- `name`
- `goal`
- `candidate_skills`
- `requires_user_confirmation`
- `outputs`
- `validation`

## Run State Principles

The `Run` object should track:

- `run_id`
- `plan_id`
- `request_id`
- `status`
- `current_stage`
- `stage_status`
- `stage_order`
- `stage_context`
- `validation_results`
- `artifacts`
- `decisions`
- `issues`
- `resume_from`
- `last_update`

This lets the system pause safely, report clearly, and resume without rethinking the whole task. The new fields matter because the agent needs to know stage ordering, stage-local validation rules, and what has already been verified before it can continue reliably after a pause.

## Proposed Orchestrator Skills

The minimum orchestrator skill set for v1 should include:

- `request-normalizer`
- `candidate-plan-generator`
- `plan-comparator`
- `plan-editor`
- `skill-router`
- `execution-guard`
- `stage-reviewer`
- `run-resumer`

## Success Criteria

V1 is successful when:

- A natural-language request reliably becomes multiple candidate plans.
- The user can select or revise a plan before execution.
- Execution happens by approved stages, not freeform improvisation.
- The system records progress, artifacts, issues, and resume state.
- Adding a new skill means updating metadata and routing, not rewriting the whole system.

## Non-Goals

The following are explicitly out of scope for v1:

- Solving every domain-specific workflow in biology.
- Rebuilding all existing skills before the framework is usable.
- Introducing a heavy MCP-first runtime before the local orchestration model is stable.
- Turning the design page into a full web application.
