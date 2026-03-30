---
name: nhance-sh
description: Use when trying the `nhance.sh` shortcut wrapper around `nquire` for pathway, gene-to-pathway, LitVar, or citation-match lookups against NCBI-related endpoints.
disable-model-invocation: true
user-invocable: true
---

# nhance-sh

## Quick Start

- **Command:** `nhance.sh <shortcut> <query>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/nhance.sh`
- **Supported shortcuts from the local source:** `-pathway`, `-gene-to-pathway`, `-litvar`, `-citmatch`

## When To Use This Tool

- Try the packaged shortcut wrapper for a few common `nquire`-based lookups.
- Resolve a Reactome pathway, gene-to-pathway mapping, LitVar entity, or heuristic citation match without building the raw `nquire` call yourself.
- Prototype an EDirect-side lookup quickly before deciding whether a lower-level `nquire` command is more reliable.
- Not for general-purpose EDirect requests; this wrapper only special-cases four shortcut modes.

## Common Patterns

```bash
# 1) Pathway lookup shortcut
nhance.sh -pathway Reactome:R-HSA-70171
```

```bash
# 2) Gene-to-pathway lookup shortcut
nhance.sh -gene-to-pathway 1956
```

```bash
# 3) Citation matching shortcut
nhance.sh -citmatch "nucleotide sequences required for tn3 transposition immunity"
```

## Recommended Workflow

1. Decide whether your request really matches one of the four hard-coded shortcut modes.
2. Pass exactly one query argument after the shortcut flag.
3. Inspect the returned XML or PMID-style result and fall back to raw `nquire` if you need tighter control.
4. Treat this wrapper as a convenience layer, not as the authoritative interface for complex EDirect querying.

## Guardrails

- The wrapper has no real built-in help or version path; `nhance.sh --help` exits silently with no useful output.
- Only `-pathway`, `-gene-to-pathway`, `-litvar`, and `-citmatch` are recognized as active shortcut modes.
- Missing shortcut payloads fail explicitly, for example `ERROR: Missing -pathway argument`.
- In the current local environment, active shortcut calls fail early with `Escape: command not found`, so the wrapper is not presently reliable without that missing shell helper.
- Plain `nhance.sh` or unrecognized leading arguments can exit successfully with no output at all, which makes silent failure easy to miss.
- Successful use also depends on `nquire`, `transmute`, and `xtract` being on `PATH`, plus live network access to the underlying NCBI / PubChem endpoints.
