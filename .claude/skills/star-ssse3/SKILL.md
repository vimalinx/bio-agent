---
name: star-ssse3
description: Use when aligning RNA-seq reads to a reference genome or generating splice-aware genome indices for transcript alignment.
disable-model-invocation: true
user-invocable: true
---

# star-ssse3

## Quick Start

- **Command**: `STAR-ssse3`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/STAR-ssse3`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Build STAR genome indices for RNA-seq alignment.
- Perform splice-aware alignment of short RNA-seq reads against a genome.
- Run STAR, BAM-input, or lift-over modes with the SSSE3-optimized STAR binary.
- Generate splice-junction-aware mappings for downstream counting, transcript assembly, or QC.

## Common Patterns

```bash
# 1) Build a STAR genome index
STAR-ssse3 \
  --runMode genomeGenerate \
  --genomeDir star_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align paired-end gzipped RNA-seq reads
STAR-ssse3 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --runThreadN 16
```

```bash
# 3) Align and emit coordinate-sorted BAM
STAR-ssse3 \
  --genomeDir star_index \
  --readFilesIn sample_R1.fastq.gz sample_R2.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. Generate genome index using `--runMode genomeGenerate` with `--genomeDir`, `--genomeFastaFiles`, and optional `--sjdbGTFfile`
2. Align reads using `--runMode alignReads` with `--genomeDir` pointing to the index and `--readFilesIn` specifying input files
3. Set `--runThreadN` to match available CPU cores for parallel processing
4. Review alignment outputs (BAM) and splice junction files (SJ.out.tab) in the output directory

## Guardrails

- Use genome indices generated with STAR version 2.7.4a or later; older indices are incompatible
- Provide uncompressed FASTA/FASTQ input files, or use `--readFilesCommand` (e.g., `zcat`) for compressed files
- Specify `--genomeLoad NoSharedMemory` unless you explicitly manage shared memory genome loading across runs
