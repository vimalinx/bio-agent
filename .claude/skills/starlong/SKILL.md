---
name: starlong
description: Use when aligning long RNA-seq reads with STARlong through the CPU-dispatch wrapper installed in this environment.
disable-model-invocation: true
user-invocable: true
---

# starlong

Shell wrapper around multiple `STARlong-*` binaries. It chooses the best SIMD build available for the current CPU (`avx2`, `avx`, `sse4.1`, `ssse3`, `sse3`, `sse2`, `sse`) and otherwise falls back to `STARlong-plain`, while exposing the normal STARlong command-line interface.

## Quick Start

- **Command:** `STARlong --genomeDir /path/to/index --readFilesIn reads.fastq`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/STARlong`
- **Observed version:** `2.7.11b`

## When To Use This Tool

- Aligning PacBio or Nanopore-style long RNA-seq reads with STARlong
- Using the wrapper that auto-selects a CPU-specific STARlong binary on this machine
- Building or reusing STAR-compatible genome indices for long-read splice-aware alignment
- Producing standard STAR outputs such as SAM/BAM, `SJ.out.tab`, and log files

## Common Patterns

```bash
# Build a genome index
STARlong \
  --runMode genomeGenerate \
  --genomeDir starlong_index \
  --genomeFastaFiles genome.fa \
  --sjdbGTFfile genes.gtf \
  --runThreadN 16
```

```bash
# Align long reads
STARlong \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq \
  --runThreadN 16
```

```bash
# Align gzipped reads and emit coordinate-sorted BAM
STARlong \
  --genomeDir starlong_index \
  --readFilesIn longreads.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --runThreadN 16
```

## Recommended Workflow

1. Generate a compatible STAR genome index, optionally with `--sjdbGTFfile` for splice annotations.
2. Run the `STARlong` wrapper rather than hard-coding one SIMD binary unless you specifically need a fixed backend.
3. Add `--readFilesCommand zcat` or a similar decompressor for compressed inputs.
4. Review the standard STAR outputs along with long-read-specific alignment quality and splice-junction summaries.

## Guardrails

- `STARlong` is a wrapper script, not the aligner binary itself. `bash -x STARlong --version` on this host showed it selecting `STARlong-avx2`.
- `--help` shows the generic STAR usage banner (`Usage: STAR ...`) because the wrapper forwards directly to the selected backend.
- `--version` works and returned `2.7.11b` locally.
- Help text declares `versionGenome 2.7.4a` as the earliest compatible genome index version for this release.
- Genome FASTA files for `--runMode genomeGenerate` must be plain text and cannot be zipped.
- Default output is SAM (`outSAMtype SAM`), so request BAM explicitly when needed.
- Help text exposes STARlong-specific window coverage controls such as `winReadCoverageRelativeMin` and `winReadCoverageBasesMin`; adjust them only if you intentionally tune long-read sensitivity.
