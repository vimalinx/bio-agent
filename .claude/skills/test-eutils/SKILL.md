---
name: test-eutils
description: Use when probing NCBI E-utilities reachability or endpoint health with the bundled `-alive`, `-all`, or per-endpoint diagnostic checks.
disable-model-invocation: true
user-invocable: true
---

# test-eutils

POSIX shell diagnostic for E-utilities availability. It checks one or more remote endpoints and reports progress with dots for apparent success and `x` markers for failures, optionally with verbose details and repeats.

## Quick Start

- **Command:** `test-eutils [ -all | -alive | -esearch | -elink | -efetch | -esummary ]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/test-eutils`
- **Useful flags:** `-verbose`, `-repeats <n>`

## When To Use This Tool

- Checking whether E-utilities endpoints are reachable from the current machine
- Narrowing a connectivity problem to one endpoint such as `esearch`, `elink`, `efetch`, or `esummary`
- Repeating health checks to catch intermittent failures
- Performing a smaller network diagnostic than `test-edirect`

## Common Patterns

```bash
# Quick reachability probe
test-eutils -alive
```

```bash
# Run the broader endpoint suite
test-eutils -all
```

```bash
# Repeat one check and show detailed failure output
test-eutils -esummary -verbose -repeats 3
```

## Recommended Workflow

1. Start with `-alive` for a lightweight reachability probe.
2. Escalate to `-all` or a specific endpoint flag if you need to localize the failure.
3. Add `-verbose` when you want the underlying failing command and payload details.
4. Use `-repeats` for intermittent problems instead of rerunning manually.

## Guardrails

- `-h`, `-help`, and `--help` print real usage text, but `--version` is unrecognized.
- The source accepts a few additional modes such as `-preview` and `-einfo` that are broader than the abbreviated usage banner.
- This tool is network-dependent and can take time. In a local bounded run, `test-eutils -alive` printed `EDirect 24.0`, the mode name `alive`, then progress dots (`....`) before the external timeout ended the run.
- Progress-dot output is concise by design; use `-verbose` if you need actionable failure details rather than just success/failure markers.
