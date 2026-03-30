# Bio Skill System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Establish the first runnable skeleton of the Bio Skill System as a plan-first orchestration framework with registries, schemas, orchestrator skill definitions, and architecture documentation.

**Architecture:** Build the control plane before domain execution. Start by creating metadata contracts and directory structure, then add orchestrator skills, example request-plan-run artifacts, and a browser-viewable architecture page that acts as the system reference. Keep v1 static, inspectable, and easy to extend.

**Tech Stack:** Markdown, YAML/JSON schemas, static HTML/CSS, local `.claude/skills` conventions, lightweight shell verification

## Current Implemented Runtime Slice

The current repo now has a runnable CLI chain for the plan-first control plane:

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

The run-state portion adds:

- per-stage execution advancement
- confirmation-gated pauses
- explicit resume checkpoints
- recorded validation results
- artifact logging on each stage transition
- blocker and future-risk review for the current run

The current docs layer also ships a static browser console:

- `docs/system/bio-skill-console.html`
- `docs/system/data/bio-skill-console-demo.json`

This console is intentionally simple: it reads a checked-in demo bundle and renders the current plan, run-state story, and run-review verdict for inspection.

## Current Verification Commands

Run the following from the project root to verify the current slice:

- `python3 -m pytest tests/test_skill_registry_export.py tests/test_bio_skill_system_cli.py -q`
- `python3 scripts/bio_skill_system.py propose ...`
- `python3 scripts/bio_skill_system.py approve ...`
- `python3 scripts/bio_skill_system.py run-init ...`
- `python3 scripts/bio_skill_system.py run-next-stage ...`
- `python3 scripts/bio_skill_system.py run-pause ...`
- `python3 scripts/bio_skill_system.py run-resume ...`
- `python3 scripts/bio_skill_system.py run-status ...`
- `python3 scripts/bio_skill_system.py run-review ...`

---

### Task 1: Create the control-plane filesystem skeleton

**Files:**
- Create: `registry/skills.yaml`
- Create: `registry/workflows.yaml`
- Create: `registry/routing_rules.yaml`
- Create: `schemas/request.schema.json`
- Create: `schemas/plan.schema.json`
- Create: `schemas/run.schema.json`

**Step 1: Write the failing verification**

Check that the files do not exist yet.

Run: `test -f registry/skills.yaml`
Expected: non-zero exit status

**Step 2: Create minimal file skeletons**

Add placeholder metadata structures for skills, workflows, routing rules, and the three schemas.

**Step 3: Run a presence check**

Run: `for f in registry/skills.yaml registry/workflows.yaml registry/routing_rules.yaml schemas/request.schema.json schemas/plan.schema.json schemas/run.schema.json; do test -f "$f" || exit 1; done`
Expected: zero exit status

**Step 4: Commit**

```bash
git add registry schemas
git commit -m "feat: add bio skill system control-plane skeleton"
```

### Task 2: Reorganize skill inventory into layered categories

**Files:**
- Create: `.claude/skills/atomic/README.md`
- Create: `.claude/skills/workflow/README.md`
- Create: `.claude/skills/orchestrator/README.md`
- Create: `.claude/skills/policy/README.md`
- Modify: `docs/plans/2026-03-29-bio-skill-system-design.md`

**Step 1: Write the failing verification**

Run: `for d in .claude/skills/atomic .claude/skills/workflow .claude/skills/orchestrator .claude/skills/policy; do test -d "$d" || exit 1; done`
Expected: non-zero exit status

**Step 2: Create category directories and README files**

Describe the purpose and admissibility criteria for each layer.

**Step 3: Verify structure**

Run: `for d in .claude/skills/atomic .claude/skills/workflow .claude/skills/orchestrator .claude/skills/policy; do test -d "$d" || exit 1; done`
Expected: zero exit status

**Step 4: Commit**

```bash
git add .claude/skills docs/plans/2026-03-29-bio-skill-system-design.md
git commit -m "feat: define layered skill taxonomy"
```

### Task 3: Define orchestrator skills

**Files:**
- Create: `.claude/skills/orchestrator/request-normalizer/SKILL.md`
- Create: `.claude/skills/orchestrator/candidate-plan-generator/SKILL.md`
- Create: `.claude/skills/orchestrator/plan-comparator/SKILL.md`
- Create: `.claude/skills/orchestrator/skill-router/SKILL.md`
- Create: `.claude/skills/orchestrator/execution-guard/SKILL.md`
- Create: `.claude/skills/orchestrator/run-resumer/SKILL.md`

**Step 1: Write the failing verification**

Run: `find .claude/skills/orchestrator -mindepth 2 -name SKILL.md | wc -l`
Expected: `0` or missing directories

**Step 2: Write the first six orchestrator skills**

Each skill should describe:
- responsibility
- inputs and outputs
- when to use it
- guardrails
- handoff conditions

**Step 3: Verify count**

Run: `test "$(find .claude/skills/orchestrator -mindepth 2 -name SKILL.md | wc -l | tr -d " ")" -ge 6`
Expected: zero exit status

**Step 4: Commit**

```bash
git add .claude/skills/orchestrator
git commit -m "feat: add orchestrator skill set for plan-first execution"
```

### Task 4: Add example artifacts for request, plan, and run

**Files:**
- Create: `examples/requests/rnaseq-differential-expression.request.json`
- Create: `examples/plans/rnaseq-differential-expression.plan.yaml`
- Create: `examples/runs/rnaseq-differential-expression.run.yaml`

**Step 1: Write the failing verification**

Run: `for f in examples/requests/rnaseq-differential-expression.request.json examples/plans/rnaseq-differential-expression.plan.yaml examples/runs/rnaseq-differential-expression.run.yaml; do test -f "$f" || exit 1; done`
Expected: non-zero exit status

**Step 2: Create the example trio**

Use one coherent example that shows how a request becomes a plan and then a run state.

**Step 3: Verify the files exist**

Run: `for f in examples/requests/rnaseq-differential-expression.request.json examples/plans/rnaseq-differential-expression.plan.yaml examples/runs/rnaseq-differential-expression.run.yaml; do test -f "$f" || exit 1; done`
Expected: zero exit status

**Step 4: Commit**

```bash
git add examples
git commit -m "feat: add example request plan and run artifacts"
```

### Task 5: Publish the architecture page

**Files:**
- Create: `docs/system/bio-skill-system.html`
- Modify: `docs/plans/2026-03-29-bio-skill-system-design.md`
- Modify: `progress.md`

**Step 1: Write the failing verification**

Run: `test -f docs/system/bio-skill-system.html`
Expected: non-zero exit status

**Step 2: Build the page**

The page should include:
- system boundary
- core objects
- layered architecture
- request lifecycle
- skill taxonomy
- plan vs run comparison
- half-automatic execution loop
- target directory structure

**Step 3: Serve and verify**

Run: `python3 -m http.server 8765 --directory docs/system`
Expected: local server starts

Run: `curl http://127.0.0.1:8765/bio-skill-system.html`
Expected: HTML containing the architecture title

**Step 4: Commit**

```bash
git add docs/system docs/plans progress.md
git commit -m "docs: publish bio skill system architecture page"
```

### Task 6: Add minimal registry backfill tooling

**Files:**
- Create: `scripts/skills/export_skill_registry.py`
- Create: `tests/test_skill_registry_export.py`

**Step 1: Write the failing test**

Create a test that expects layered skill metadata export from `.claude/skills`.

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_skill_registry_export.py -q`
Expected: FAIL

**Step 3: Write minimal implementation**

Implement a script that walks the layered skill directories and emits a registry snapshot.

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_skill_registry_export.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/skills/export_skill_registry.py tests/test_skill_registry_export.py
git commit -m "feat: add skill registry export script"
```
