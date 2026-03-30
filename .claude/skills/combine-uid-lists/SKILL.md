---
name: combine-uid-lists
description: Use when unioning multiple Entrez or NCBI UID files into one deduplicated numeric-sorted list.
disable-model-invocation: true
user-invocable: true
---

# combine-uid-lists

## Quick Start

- **Command**: `combine-uid-lists FILE1 FILE2 ...`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/combine-uid-lists`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Merge several one-UID-per-line files into a single union list.
- Deduplicate repeated PubMed, PMC, taxonomy, or other Entrez IDs before downstream fetches.
- Normalize multiple EDirect search results into one numerically sorted file.
- Use this when you want a quick set-union step without writing a custom `sort | uniq` command.

## Common Patterns

```bash
# 1) Combine two Entrez UID lists into one unique union
combine-uid-lists cohort_a.ids cohort_b.ids > union.ids
```

```bash
# 2) Merge several partial search results before efetch
combine-uid-lists day1.ids day2.ids day3.ids > merged.ids
```

```bash
# 3) Check how many unique IDs remain after the merge
combine-uid-lists a.ids b.ids c.ids | wc -l
```

## Recommended Workflow

1. Save each upstream UID set as one ID per line.
2. Run `combine-uid-lists` on all source files you want to union.
3. Redirect the result to a new file or pipe it directly into a downstream EDirect step.
4. Check the merged count before using the result in expensive downstream fetches.

## Guardrails

- The real implementation is a tiny wrapper around `sort -nu "$@"`; it always numeric-sorts and deduplicates.
- `--help` and `--version` come from GNU `sort`, not from custom EDirect documentation.
- This command expects file arguments, not two streams on stdin.
- Locale can affect sorting behavior in general `sort` usage; use `LC_ALL=C` if you need fully reproducible collation.
