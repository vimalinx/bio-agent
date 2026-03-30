---
name: difference-uid-lists
description: Use when finding the symmetric difference between two Entrez or NCBI UID files.
disable-model-invocation: true
user-invocable: true
---

# difference-uid-lists

## Quick Start

- **Command**: `difference-uid-lists FILE1 FILE2`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/difference-uid-lists`
- **Full reference**: `references/help.md`

## When To Use This Tool

- Keep only IDs that appear in exactly one of two UID files.
- Compare an older and newer search result to see which IDs were added or dropped.
- Audit drift between two snapshots of the same Entrez query.
- Use this instead of `exclude-uid-lists` when you need both sides' uniques, not just FILE1 minus FILE2.

## Common Patterns

```bash
# 1) Find IDs that changed between two saved searches
difference-uid-lists old.ids new.ids > changed.ids
```

```bash
# 2) Count how many UIDs are unique to either cohort
difference-uid-lists case.ids control.ids | wc -l
```

```bash
# 3) Review the changed IDs before refetching records
difference-uid-lists baseline.ids rerun.ids | sed -n '1,20p'
```

## Recommended Workflow

1. Prepare exactly two one-UID-per-line files.
2. Run `difference-uid-lists` to compute the symmetric difference.
3. Inspect or count the output before feeding it into downstream fetch or QC steps.
4. Switch to `exclude-uid-lists` or `intersect-uid-lists` if you actually need a directional subtraction or shared set.

## Guardrails

- The real implementation is `comm -3 <(sort "$1") <(sort "$2") | tr -d '\t' | sort -n`, so it returns IDs unique to either file.
- The wrapper sorts inputs internally; original input order is discarded.
- This command expects exactly two files and has no real built-in help/version path.
- Passing `--help` or `--version` does not show clean custom docs; it leaks through to `sort` and can still emit `comm` / missing-file noise.
