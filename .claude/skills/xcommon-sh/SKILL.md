---
name: xcommon-sh
description: Use when reading or debugging the shared `xcommon.sh` shell library that supplies local-archive discovery, stdin parsing, and common helper functions to EDirect `x*` scripts.
disable-model-invocation: true
user-invocable: true
---

# xcommon-sh

Shared shell library for the newer local-archive `x*` EDirect scripts. It is not a meaningful standalone CLI; it defines common variables and functions such as `ParseStdin`, `GetUIDs`, `FindArchiveFolder`, `FindPostingsFolder`, `FindDataFolder`, `DisplayError`, and date-constraint normalization.

## Quick Start

- **File:** `/home/vimalinx/miniforge3/envs/bio/bin/xcommon.sh`
- **Typical use:** sourced by sibling tools such as `xfetch`, `xfilter`, and `xinfo`
- **Not a normal command:** direct execution provides no useful interface

## When To Use This Tool

- Understanding why `xfetch`, `xfilter`, or `xinfo` behave the way they do
- Debugging local archive/postings path discovery based on `EDIRECT_LOCAL_ARCHIVE`
- Inspecting shared stdin parsing and UID-normalization logic across the `x*` helpers
- Auditing common error/warning rendering or `EDIRECT_TRACE` behavior

## Common Patterns

```bash
# Read the shared helper source
sed -n '1,260p' /home/vimalinx/miniforge3/envs/bio/bin/xcommon.sh
```

```bash
# Grep the library for folder-discovery helpers
rg 'FindArchiveFolder|FindPostingsFolder|FindDataFolder' /home/vimalinx/miniforge3/envs/bio/bin/xcommon.sh
```

```bash
# Source it inside a debugging shell if needed
. /home/vimalinx/miniforge3/envs/bio/bin/xcommon.sh
```

## Recommended Workflow

1. Treat `xcommon.sh` as shared implementation, not as an end-user command.
2. Read it when a sibling `x*` wrapper emits path or stdin-source errors that seem opaque.
3. Focus first on `FindLocalArchiveFolder`, `GetUIDs`, `ParseStdin`, and the display helpers.
4. If tracing is needed, set `EDIRECT_TRACE=true` before running the higher-level wrapper that sources this file.

## Guardrails

- Direct execution is effectively meaningless here: `xcommon.sh -h` and `xcommon.sh --version` produced no useful output in local testing.
- Source inspection shows local path discovery ultimately calls `rchive -local <db> <Archive|Postings|Data|Source>`.
- If `EDIRECT_LOCAL_ARCHIVE` cannot be resolved, the shared helper emits `ERROR: Must supply path to local data by setting EDIRECT_LOCAL_ARCHIVE environment variable` and exits.
- `GetUIDs` normalizes IDs by splitting on non-alphanumeric/underscore/dot characters and sorting/uniquing the final stream.
