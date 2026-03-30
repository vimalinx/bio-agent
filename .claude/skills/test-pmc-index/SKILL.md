---
name: test-pmc-index
description: Use when validating a local PMC archive/index configured through `EDIRECT_LOCAL_ARCHIVE` by round-tripping random PMC records through `xfetch` and `xsearch`.
disable-model-invocation: true
user-invocable: true
---

# test-pmc-index

EDirect shell smoke test for a local PMC archive. It generates random PMC-style IDs, fetches records from the local archive with `xfetch -db pmc`, extracts titles, then uses `xsearch -db pmc -title` to see whether the same records are findable through the local index.

## Quick Start

- **Command:** `test-pmc-index`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/test-pmc-index`
- **Critical environment:** `EDIRECT_LOCAL_ARCHIVE`

## When To Use This Tool

- Checking whether a local PMC archive/index is wired up well enough for title-based lookup
- Validating `xfetch` and `xsearch` behavior against a prepared PMC local archive
- Troubleshooting an `EDIRECT_LOCAL_ARCHIVE` PMC installation rather than the public PMC service
- Running a quick title-roundtrip consistency test on archived PMC records

## Common Patterns

```bash
# Run against the configured local archive
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
test-pmc-index
```

```bash
# Capture the diagnostic output
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
test-pmc-index > pmc-index-check.txt
```

```bash
# Time the run externally if needed
export EDIRECT_LOCAL_ARCHIVE=/path/to/local/archive
time test-pmc-index
```

## Recommended Workflow

1. Set `EDIRECT_LOCAL_ARCHIVE` to a real local archive root before running the test.
2. Run `test-pmc-index` with no arguments.
3. Inspect `OKAY`, `MULT`, `NONE`, `TRIM`, `SKIP`, or `FAIL` lines to understand how well title-based lookup matches fetched records.
4. Fix the local archive/index configuration first if the script emits path or `rchive` errors before the record checks start.

## Guardrails

- `-h` and `--version` are not safe metadata paths. They were treated like normal execution in this environment and immediately fell into configuration/runtime errors.
- Without `EDIRECT_LOCAL_ARCHIVE`, the script printed `ERROR: Must supply path to local data by setting EDIRECT_LOCAL_ARCHIVE environment variable` and then still emitted an `Insufficient command-line arguments supplied to rchive` error before ending.
- The source shows no argument parsing at all; it always runs the same random-ID roundtrip test.
- This test depends on a working local PMC archive/index, not just network access.
