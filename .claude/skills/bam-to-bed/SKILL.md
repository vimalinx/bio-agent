---
name: bam-to-bed
description: Use when converting BAM alignment files to BED6, BED12, or BEDPE format for downstream analysis or visualization.
disable-model-invocation: true
user-invocable: true
---

# bam-to-bed

## Quick Start
- **Command:** `bamToBed -i input.bam [options] > output.bed`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bamToBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Convert alignments from BAM into BED6, BED12, or BEDPE for downstream interval analysis.
- Represent split or spliced alignments as separate blocks with `-split`, `-splitD`, or `-bed12`.
- Export paired-end geometry with `-bedpe`.
- Preserve extra alignment context such as edit distance or CIGAR when BED output alone is too lossy.

## Common Patterns

```bash
# 1) Basic BAM to BED6
bamToBed \
  -i alignments.bam > alignments.bed
```

```bash
# 2) BED12 output for split alignments
bamToBed \
  -i alignments.bam \
  -bed12 > alignments.bed12
```

```bash
# 3) BEDPE for paired-end reads
bamToBed \
  -i alignments.qname.bam \
  -bedpe > alignments.bedpe
```

## Recommended Workflow

1. Choose the target representation first: BED6 for simple intervals, BED12 for blocked alignments, or BEDPE for read pairs.
2. Query-name sort or group the BAM before using `-bedpe`.
3. Add `-split` / `-splitD` when the CIGAR structure matters for exon-aware or gapped alignments.
4. Redirect stdout to a file and sanity-check coordinates and column count before feeding the result into downstream tools.

## Guardrails

- `-bedpe` requires BAM records to be grouped or sorted by query.
- `-bed12` forces `-split`.
- `-splitD` also forces `-split` and breaks on both `N` and `D` CIGAR operators.
- `-tag` must reference a numeric BAM tag and cannot be combined with BEDPE output.
- Default BED score is mapping quality; `-ed` changes that semantics, especially for BEDPE where the mate edit distances are combined.
