---
name: filter-record
description: Use when filtering records from Entrez/NCBI data streams as part of entrez-direct workflows.
disable-model-invocation: true
user-invocable: true
---

# filter-record

## Quick Start

- **Command:** `filter-record < records.txt > filtered.txt`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/filter-record`
- **Full reference:** See `references/help.md` for detailed usage

## When To Use This Tool

- Apply EDirect's built-in record-filtering step to a record-oriented text stream.
- Clean or narrow structured NCBI/Entrez records before a downstream transformation stage.
- Keep record filtering inside the `transmute` toolchain instead of building ad hoc shell parsing.

## Common Patterns

```bash
# 1) Filter a saved record stream
filter-record < records.txt > filtered.txt
```

```bash
# 2) Filter an upstream EDirect stream before the next pipeline stage
some-upstream-command | filter-record | some-downstream-command
```

## Recommended Workflow

1. Start from a representative upstream record stream.
2. Run `filter-record` in a pipe or with stdin redirection.
3. Inspect a small sample of the output before scaling up.
4. Continue into downstream EDirect steps once the retained record structure looks right.

## Guardrails

- This wrapper is just `transmute -txf`, so `transmute` must be on `PATH`.
- `--help` and `--version` are not implemented here; both are reported as unrecognized arguments.
- Prefer stdin or pipes over undocumented positional-file behavior.
- The real filtering semantics live inside `transmute`, so validate behavior on a representative record stream before batching.
