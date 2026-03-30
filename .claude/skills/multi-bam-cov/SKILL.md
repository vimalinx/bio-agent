---
name: multi-bam-cov
description: Use when you need to count read coverage from multiple BAM files across specific genomic regions defined in a BED, GFF, or VCF file.
disable-model-invocation: true
user-invocable: true
---

# multi-bam-cov

## Quick Start
- **Command:** `multiBamCov -bams sample1.bam sample2.bam ... -bed regions.bed [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/multiBamCov`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Count alignments from multiple BAMs over the same target interval set in one pass.
- Build per-region sample-by-sample count matrices from BED / GFF / VCF targets.
- Apply mapping-quality, pairing, duplication, and strand filters consistently across many BAMs.
- Compare sample support over defined loci without computing a genome-wide depth profile.

## Common Patterns

```bash
# 1) Basic multi-sample locus counts
multiBamCov \
  -bams tumor.bam normal.bam \
  -bed targets.bed
```

```bash
# 2) Count only proper pairs with MAPQ >= 20
multiBamCov \
  -bams sample1.bam sample2.bam sample3.bam \
  -bed exons.bed \
  -q 20 \
  -p
```

```bash
# 3) Count split alignments on the same strand
multiBamCov \
  -bams rna1.bam rna2.bam \
  -bed exons.bed \
  -split \
  -s
```

## Recommended Workflow

1. Prepare the region file that defines the reporting frame, because output is one row per input interval.
2. Decide whether the counts should exclude duplicates and failed-QC reads (`default`) or include them (`-D`, `-F`).
3. Set `-q`, `-p`, `-s` / `-S`, and `-split` deliberately so all BAMs are counted under the same policy.
4. Import the appended per-BAM count columns into downstream statistical or visualization tooling.

## Guardrails

- `-bams` and `-bed` are both required.
- This tool reports counts per interval per BAM, not per-base depth tracks like `genomeCoverageBed`.
- `-D` and `-F` widen the reads included in counting; the default excludes duplicates and failed-QC reads.
- `-q` defaults to `0`, so low-quality alignments are included unless you raise the threshold.
- Prefer indexed, queryable BAMs for practical performance on large region sets.
