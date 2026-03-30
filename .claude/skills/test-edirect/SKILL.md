---
name: test-edirect
description: Use when smoke-testing an Entrez Direct installation with the bundled long-form example suite or the focused `-test` trace mode.
disable-model-invocation: true
user-invocable: true
---

# test-edirect

Large shell-based demonstration and smoke-test script for Entrez Direct. With no arguments it runs a long sequence of real EDirect examples and prints titled sections such as `INFO HELP`, `FIELD EXAMPLE`, and `LINK EXAMPLE`. It also has a special `-test` mode that enables tracing around one targeted pipeline.

## Quick Start

- **Command:** `test-edirect`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/test-edirect`
- **Special modes:** `-timer`, `-timed`, `-test`

## When To Use This Tool

- Verifying that a local EDirect installation can execute a broad set of canonical example workflows
- Running a human-readable smoke suite instead of a one-endpoint connectivity probe
- Spot-checking whether `esearch`, `efetch`, `elink`, `xtract`, and related helpers all cooperate correctly
- Using the focused `-test` path when you want tracing around one smaller pipeline

## Common Patterns

```bash
# Run the full demonstration / smoke suite
test-edirect
```

```bash
# Add elapsed times between sections
test-edirect -timer
```

```bash
# Run the focused trace-enabled test path
test-edirect -test
```

## Recommended Workflow

1. Start with a plain `test-edirect` run when you want a broad installation smoke test.
2. Use `-timer` if you care about rough section timings.
3. Use `-test` when you want a much narrower traced pipeline instead of the whole suite.
4. Treat this tool as a diagnostic/demo harness, not as a stable machine-readable checker.

## Guardrails

- `-h` and `--version` are not help/version modes; locally both failed with `Unrecognized option`.
- The default no-arg path is long-running and network-dependent. In a bounded local run it began by printing `EDirect 24.0`, `Linux - x86_64`, then section headers like `INFO HELP`, `FIELD EXAMPLE`, and `LINK EXAMPLE`.
- Source inspection shows `-test` exports `EDIRECT_TRACE=true` and runs a specific `esearch | efilter | elink | xtract` pipeline before exiting.
- Because the script exercises many live EDirect examples, failures may reflect network issues, remote content drift, or one broken helper anywhere in the chain.
