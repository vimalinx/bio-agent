---
name: starlong-sse3
description: Use when aligning long RNA-seq reads to a reference genome using STARlong with SSE3 optimization, or when generating genome indices for long-read splice-aware alignment.
disable-model-invocation: true
user-invocable: true
---

# starlong-sse3

## Quick Start

- **Command**: `STARlong-sse3`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/STARlong-sse3`
- **Version**: 2.7.11b
- **Full reference**: See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Align long RNA-seq reads from PacBio or Nanopore with STARlong.
- Build or reuse STAR-compatible genome indices for long-read splice-aware mapping.
- Map full-length transcript reads while keeping STAR-style splice-junction outputs.
- Run a long-read-focused STAR wrapper using the SSE3-optimized binary.

## Common Patterns

```bash
# 1) Build a genome index for STARlong
STARlong-sse3 \
  --runMode genomeGenerate \
  --genomeDir starlong_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# 2) Align long reads from FASTQ
STARlong-sse3 \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq \
  --runThreadN 16
```

```bash
# 3) Align gzipped long reads and emit sorted BAM
STARlong-sse3 \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. Prepare a genome directory and FASTA reference; optionally provide a GTF file with `--sjdbGTFfile` for splice junction annotation.
2. Generate the genome index with `--runMode genomeGenerate --genomeDir <dir> --genomeFastaFiles <fasta>`.
3. Align long reads with `--runMode alignReads --genomeDir <dir> --readFilesIn <reads.fq>`.
4. Verify output files (alignments and splice junctions) and review summary statistics before downstream analysis.

## Guardrails

- Always specify `--genomeDir` pointing to a valid STAR genome index directory.
- Use `--runThreadN` to match available CPU cores; avoid oversubscribing system resources.
- For long reads, ensure the genome index was built with appropriate `--genomeSAindexNbases` scaled to genome size.
