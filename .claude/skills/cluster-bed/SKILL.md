---
name: cluster-bed
description: Use when you need to cluster overlapping or nearby genomic intervals in BED, GFF, or VCF files into groups.
disable-model-invocation: true
user-invocable: true
---

# cluster-bed

## Quick Start
- **Command:** `clusterBed -i intervals.bed [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/clusterBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Assign intervals into overlap / proximity-based clusters while preserving each original record.
- Group peaks, exons, or other features by neighborhood without collapsing them into merged coordinates.
- Keep strand-specific cluster assignment with `-s`.
- Expand clusters to nearby but non-overlapping features with `-d`.

## Common Patterns

```bash
# 1) Cluster overlapping or book-ended intervals
clusterBed \
  -i peaks.bed
```

```bash
# 2) Cluster intervals within 1000 bp
clusterBed \
  -i peaks.bed \
  -d 1000
```

```bash
# 3) Cluster on the same strand only
clusterBed \
  -i transcripts.bed \
  -s
```

## Recommended Workflow

1. Use `clusterBed` when you need cluster IDs on original records, not merged coordinates.
2. Set `-d` deliberately based on the biological neighborhood you want to treat as one cluster.
3. Add `-s` only when strand is meaningful for the feature class.
4. Feed the appended cluster ID into downstream grouping, summarization, or visualization steps.

## Guardrails

- This tool appends a cluster ID; it does not merge records the way `mergeBed` does.
- The default `-d 0` clusters overlapping and book-ended intervals together.
- Cluster numbering depends on input order, so pre-sort input if you need stable IDs across reruns.
- `-s` prevents opposite-strand records from entering the same cluster.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.
