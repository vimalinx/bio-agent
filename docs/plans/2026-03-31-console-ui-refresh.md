# Bio Agent Console UI Refresh Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rebuild the static console page into a darker, product-like bio-agent workspace inspired by the reference UI while preserving bio-agent-specific session, plan, runtime, and history concepts.

**Architecture:** Keep the page as a single static HTML document that reads the checked-in demo bundle, but reorganize the information hierarchy into a left navigation rail plus a central workspace. Adapt the existing session and runtime data into a lighter product shell instead of a documentation-style dashboard.

**Tech Stack:** Single-file HTML/CSS/vanilla JS, static JSON demo bundle, pytest doc checks

---

### Task 1: Redesign the console shell

**Files:**
- Modify: `docs/system/bio-skill-console.html`
- Test: `tests/test_system_docs.py`

**Step 1:** Replace the current documentation-style layout with a dark application shell:
- fixed left rail
- minimal top utility strip
- centered request composer
- lower workspace panels for session, plans, runtime, and history

**Step 2:** Keep the page single-file and preserve `fetch("data/bio-skill-console-demo.json")`.

**Step 3:** Update tests so they verify the new shell-level anchors rather than the old panel wording.

### Task 2: Expand the demo bundle for session UI

**Files:**
- Modify: `docs/system/data/bio-skill-console-demo.json`
- Test: `tests/test_system_docs.py`

**Step 1:** Add `session` and `history` objects that match the newer session workflow.

**Step 2:** Keep all currently asserted runtime fields intact so the console still demonstrates paused conservative execution.

### Task 3: Rewire rendering logic

**Files:**
- Modify: `docs/system/bio-skill-console.html`

**Step 1:** Replace old `renderSummary/renderPlans/renderStages/renderMetrics/renderRunReview` output with product-style renderers for:
- sidebar session inventory
- hero composer state
- session health
- plan comparison
- stage timeline
- history timeline
- raw JSON inspector

**Step 2:** Ensure responsive behavior keeps the left rail and main workspace readable on mobile.

### Task 4: Verify

**Files:**
- Modify: `tests/test_system_docs.py`

**Step 1:** Run:

```bash
python3 -m pytest tests/test_system_docs.py -q
```

**Step 2:** Run:

```bash
python3 -m pytest tests/test_skill_registry_export.py tests/test_bio_skill_system_cli.py tests/test_system_docs.py -q
```

**Step 3:** Keep the console page loadable from GitHub Pages and local static hosting.
