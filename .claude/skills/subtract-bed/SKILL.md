---
name: subtract-bed
description: Use when you need to remove overlapping portions of one interval set from another, such as subtracting blacklist, repeat, or annotation regions from BED, GFF, VCF, or BAM-like inputs.
disable-model-invocation: true
user-invocable: true
---

# subtract-bed

## Quick Start
- Command: `subtractBed -a <bed/gff/vcf> -b <bed/gff/vcf>`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/subtractBed`
- Full reference: [references/help.md](references/help.md)

## When To Use This Tool

- Remove blacklist, repeat, or exclusion intervals from a target interval set.
- Trim only the overlapping segments from A while keeping the remaining pieces.
- Drop entire A features on qualifying overlap with `-A` or `-N`.
- Apply strand-aware and fraction-aware subtraction rules before downstream counting or annotation.

## Common Patterns

```bash
# 1) Remove blacklist segments from peaks
subtractBed \
  -a peaks.bed \
  -b blacklist.bed \
  > peaks.clean.bed
```

```bash
# 2) Remove whole A features if at least half the feature overlaps B
subtractBed \
  -a exons.bed \
  -b repeats.bed \
  -A \
  -f 0.5 \
  > exons.filtered.bed
```

```bash
# 3) Subtract only same-strand overlaps, treating BED12/BAM splits separately
subtractBed \
  -a transcripts.bed12 \
  -b antisense-mask.bed \
  -s \
  -split \
  > transcripts.trimmed.bed
```

## Recommended Workflow

1. Decide whether you want partial trimming of A (default) or whole-record removal with `-A` / `-N`.
2. Add overlap thresholds and strand rules deliberately with `-f`, `-F`, `-r`, `-e`, `-s`, or `-S`.
3. For large datasets, coordinate-sort the inputs first and then use `-sorted` with `-g` when a stable chromosome order matters.
4. If you need to inspect why intervals were altered, rerun with `-wo` or `-wb` as a diagnostic pass rather than as the final cleaned output.

## Guardrails

- Default subtraction can split one A interval into multiple output fragments; that is expected behavior, not duplication.
- `-A` removes the whole A feature on qualifying overlap, while `-N` with `-f` uses the summed overlap across all B features.
- `-wo` and `-wb` change the output layout for overlap inspection; do not treat those outputs like plain trimmed BED intervals.
- `-sorted` requires truly coordinate-sorted inputs and may need `-nonamecheck` if naming conventions differ (`chr1` vs `chr01`).
- If you use BAM as input A, add `-bed` when the downstream consumer expects BED-style output rather than alignment output.
