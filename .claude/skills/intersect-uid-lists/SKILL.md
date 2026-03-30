---
name: intersect-uid-lists
description: Use when keeping only the Entrez or NCBI UIDs present in both of two UID files.
disable-model-invocation: true
user-invocable: true
---

# intersect-uid-lists

## Quick Start
- Command: `intersect-uid-lists FILE1 FILE2`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/intersect-uid-lists`
- Reference: `references/help.md`

## When To Use This Tool

- Keep only IDs shared by two independent Entrez result sets.
- Build overlap cohorts, for example records matching both a disease query and a species query.
- Confirm which previously processed IDs are still present in a refreshed search.
- Use this instead of `exclude-uid-lists` or `difference-uid-lists` when you want the shared core set.

## Common Patterns

```bash
# 1) Keep only UIDs that appear in both searches
intersect-uid-lists disease.ids species.ids > overlap.ids
```

```bash
# 2) Count the shared UID set between two snapshots
intersect-uid-lists old.ids new.ids | wc -l
```

```bash
# 3) Preview the first overlapping IDs before refetching
intersect-uid-lists query_a.ids query_b.ids | sed -n '1,20p'
```

## Recommended Workflow

1. Save the two UID sets you want to compare as one-UID-per-line files.
2. Run `intersect-uid-lists` to compute the shared set.
3. Inspect or count the overlap before feeding it into expensive downstream steps.
4. Use the resulting list with `efetch`, `xtract`, or other local archive utilities.

## Guardrails

- The real implementation is `comm -12 <(sort "$1") <(sort "$2") | sort -n`, so it returns only the shared IDs.
- The wrapper sorts inputs internally, so output order reflects numeric sorting rather than input order.
- This command expects exactly two files and has no real built-in help/version interface.
- Passing `--help` or `--version` can still produce `sort` / `comm` noise instead of clean documentation output.
