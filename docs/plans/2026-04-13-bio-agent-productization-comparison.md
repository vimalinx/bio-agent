# Bio-Agent Productization Comparison — 2026-04-13

## Comparative Judgment

- **bio-agent** is strongest today at the **control-plane / truth-model** layer: plan generation, session lifecycle, benchmark-aware routing, and canonical `run.json` / `run-status.json` / `run-review.json` state.
- **ClawBio** is strongest at **packaged reproducible delivery**: a smaller finished product promise with explicit bundle-style outputs.
- **LabClaw** is strongest at **breadth and catalog coverage**: many discoverable capabilities, but not a single narrow first-party product surface.

## Recommended Direction

`bio-agent` should remain a **control-plane-first hybrid**, not a wet-lab/XR pivot and not a raw skill-count race.

The productization move is:

1. Keep the canonical control plane as the execution source of truth.
2. Productize a small set of **hero workflows** first.
3. Attach automatic reproducibility bundles to those hero lanes.
4. Publish an honest capability catalog that distinguishes:
   - `first_party_executable`
   - `bridge_executable`
   - `reference_only`

## Hero Lanes

The first two hero lanes are:

- `rnaseq-differential-expression`
- `germline-short-variant-discovery`

These lanes are now the benchmark-backed productization targets because they already have grounded workflow metadata, benchmark coverage, and canonical session/run convergence.

## Guardrails

- No second orchestrator.
- Canonical `run.json`, `run-status.json`, and `run-review.json` stay authoritative.
- Session-to-skill crystallization remains phase 2 and must stay gated behind hero-runner proof plus reproducibility-bundle completeness.

## Packaging Implications

- Product-facing hero commands must stay as **thin adapters** over the existing session machinery.
- Reproducibility is not optional marketing copy; it must emit inspectable artifacts.
- Capability breadth must never be presented as first-party runnable maturity unless the metadata proves it.
