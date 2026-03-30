---
name: starlong-sse4-1
description: Use when aligning long RNA-seq reads to a reference genome or generating genome indexes for spliced transcript alignment
disable-model-invocation: true
user-invocable: true
---

# starlong-sse4-1

## Quick Start

- **Command:** `STARlong-sse4.1`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/STARlong-sse4.1`
- **Full reference:** See `references/help.md` for complete parameter documentation

## When To Use This Tool

- Align long RNA-seq reads from PacBio or Nanopore with STARlong.
- Build or reuse STAR-compatible genome indices for long-read splice-aware mapping.
- Map full-length transcript reads while keeping STAR-style splice-junction outputs.
- Run a long-read-focused STAR wrapper using the SSE4.1-optimized binary.

## Common Patterns

```bash
# 1) Build a genome index for STARlong
STARlong-sse4.1 \
  --runMode genomeGenerate \
  --genomeDir starlong_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align long reads from FASTQ
STARlong-sse4.1 \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq \
  --runThreadN 16
```

```bash
# 3) Align gzipped long reads and emit sorted BAM
STARlong-sse4.1 \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. Generate a genome index: `STARlong-sse4.1 --runMode genomeGenerate --genomeDir /path/to/index --genomeFastaFiles ref.fa --sjdbGTFfile annotations.gtf`
2. Prepare long-read input files in FASTA/FASTQ format
3. Align reads: `STARlong-sse4.1 --genomeDir /path/to/index --readFilesIn reads.fq --runThreadN N`
4. Review output alignments (SAM/BAM) and splice junction files (SJ.out.tab)

## Guardrails

- Always generate or obtain a compatible genome index before running alignment
- Scale `--genomeSAindexNbases` down for small genomes (min(14, log2(GenomeLength)/2 - 1))
- Ensure input format matches `--readFilesType` (default Fastx for FASTA/FASTQ)
