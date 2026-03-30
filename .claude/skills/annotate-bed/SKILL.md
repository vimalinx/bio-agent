---
name: annotate-bed
description: Use when you need to annotate BED/GFF/VCF intervals with coverage depth and breadth from multiple feature files.
disable-model-invocation: true
user-invocable: true
---

# annotate-bed

## Quick Start
- **Command:** `annotateBed -i intervals.bed -files file1.bed file2.bed ... [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/annotateBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Annotate each interval in a primary file with coverage or overlap counts from multiple feature files.
- Summarize fraction covered, counts, or both across many annotation tracks at once.
- Compare how one set of intervals intersects promoters, exons, enhancers, blacklist regions, or similar catalogs.
- Restrict overlap accounting by strand with `-s` or `-S`.

## Common Patterns

```bash
# 1) Annotate intervals by fractional coverage from two tracks
annotateBed \
  -i peaks.bed \
  -files promoters.bed enhancers.bed
```

```bash
# 2) Report counts instead of fraction covered
annotateBed \
  -i peaks.bed \
  -files promoters.bed enhancers.bed \
  -counts
```

```bash
# 3) Emit both counts and coverage with readable column names
annotateBed \
  -i peaks.bed \
  -files promoters.bed enhancers.bed \
  -names promoters enhancers \
  -both
```

## Recommended Workflow

1. Pick a primary interval file whose row order you want to preserve in the output.
2. Decide whether the output should represent breadth (`default`), hit count (`-counts`), or both (`-both`).
3. Use `-names` so the header is interpretable when many annotation tracks are involved.
4. Validate a few intervals manually if the distinction between coverage fraction and feature count matters downstream.

## Guardrails

- `-i` and `-files` are both required.
- `-names` should have one label per annotation file if you want a correct header.
- `-counts` and `-both` change the meaning and number of appended columns, so downstream parsers must know which mode you used.
- `-s` and `-S` are mutually exclusive.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers produce noisy errors.
