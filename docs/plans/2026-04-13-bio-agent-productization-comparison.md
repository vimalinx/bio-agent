# Bio-Agent Productization Comparison and Roadmap

_Date: 2026-04-13_

This is the canonical comparison-and-roadmap artifact for the current productization push. It replaces `reference/COMPARATIVE_ANALYSIS_REPORT.md` as the decision document that future work should cite.

## Decision Summary

`bio-agent` should be productized as a **control-plane-first hybrid**, not as:

- a ClawBio clone,
- a LabClaw-style skill-library breadth race, or
- a wet-lab / XR / robotics pivot.

The recommended move is to keep the current session / run / benchmark control plane as the source of truth, then layer a small number of exemplar product lanes on top of it.

## Comparative Positioning

| System | Current strength | What to borrow | What not to copy |
| --- | --- | --- | --- |
| `bio-agent` | plan-first orchestration, session truth, benchmark-aware control plane | keep as the canonical backbone | do not dilute it with a second orchestrator |
| ClawBio | packaged local-first delivery and reproducibility bundles | automatic `commands.sh` / environment / checksum style outputs | do not narrow the whole repo to only one-command local execution |
| LabClaw | breadth and capability browsing | honest capability catalog / connector surfacing | do not pivot toward wet-lab / XR breadth as the primary product story |

## Product Direction

The near-term product story is:

1. **Preserve canonical runtime truth** — `run.json`, `run-status.json`, and `run-review.json` remain the execution source of truth.
2. **Ship 2 hero workflow families first** — start with:
   - `rnaseq-differential-expression`
   - `germline-short-variant-discovery`
3. **Make reproducibility a default output** for hero runs, not a manual benchmark-only export path.
4. **Publish an evidence-derived capability catalog** that separates:
   - `first_party_executable`
   - `bridge_executable`
   - `reference_only`
5. **Keep crystallization gated to phase 2** until hero lanes, reproducibility, and stable review/status outputs are proven.

## Execution Lanes

### Lane A — Hero runner surface
- Add a thin product-facing runner on top of the existing session lifecycle.
- It must adapt inputs and output locations only.
- It must not become a second orchestrator or bypass canonical session/run artifacts.

### Lane B — Reproducibility bundle system
- Emit `commands.sh`, environment snapshot, `checksums.sha256`, `provenance.json`, and `delivery-bundle.json` for hero runs.
- Bundle generation should be automatic for product-facing runs.

### Lane C — Capability catalog from evidence
- Derive surfaced capability metadata from registries, exports, and proof-bearing artifacts.
- Every capability should declare execution tier, runtime mode, verification level, reproducibility level, and source kind.

### Lane D — Verification / CI / smoke proof
- Keep the stable control-plane regression lane green.
- Add separable hero-runner smoke checks.
- Keep heavyweight bio-tool integration lanes optional and honest about environment requirements.

### Lane E — Comparison / docs packaging
- Publish the comparison, roadmap, and guardrails in the docs surface.
- Make the control-plane-first hybrid story explicit in README, docs index, and architecture comparison pages.

## Guardrails

- No second orchestrator.
- No marketing claim that collapses `defined`, `bridge-runnable`, and `first-party runnable` into one bucket.
- No wet-lab / XR repositioning.
- No crystallization-by-default before hero-runner proof exists.
- No product runner that diverges from canonical `run.json` / `run-status.json` / `run-review.json` truth.

## Verification Shape

The roadmap should be considered implemented only when the following are true:

- stable local regression tests stay green,
- the benchmark contract lane remains green,
- both hero families have smoke coverage,
- reproducibility bundle contents are emitted automatically for hero runs,
- docs explain the capability tiers and product boundaries truthfully.

## Canonical References

- `README.md`
- `.omx/plans/prd-2026-04-13-bio-agent-productization-roadmap.md`
- `.omx/plans/test-spec-2026-04-13-bio-agent-productization-roadmap.md`
- `docs/system/architecture-comparison-roadmap.html`
- `reference/COMPARATIVE_ANALYSIS_REPORT.md` (historical raw snapshot only)
