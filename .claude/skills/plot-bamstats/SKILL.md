---
name: plot-bamstats
description: Use when visualizing `samtools stats` output as BAM QC plots, including merged reports and reference-GC-aware summaries.
disable-model-invocation: true
user-invocable: true
---

# plot-bamstats

Perl-based visualization tool bundled with samtools for plotting BAM alignment statistics.

## Quick Start

- **Command:** `plot-bamstats [options] file.bam.bc`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/plot-bamstats`
- **Expected input:** `samtools stats` output, historically called `bamcheck`

## When To Use This Tool

- Visualizing output from `samtools stats` as graphical plots
- Generating publication-quality alignment statistic figures
- Merging multiple bamstats files into one stream before plotting
- Incorporating reference GC expectations through `-s` / `-r`

## Common Patterns

```bash
# 1) Basic BAM QC plotting
samtools stats aln.bam > aln.bam.bc
plot-bamstats -p outdir/ aln.bam.bc
```

```bash
# 2) Merge multiple bamstats files to stdout
plot-bamstats -m sample1.bc sample2.bc > merged.bc
```

```bash
# 3) Prepare reference GC statistics for later plotting
plot-bamstats -s ref.fa
plot-bamstats -p outdir/ -r ref.fa.gc aln.bam.bc
```

## Recommended Workflow

1. Produce a clean `samtools stats` file first and keep it alongside the source BAM.
2. Decide whether you want a fresh plot directory (`-p outdir/`) or a simple prefixed file set.
3. If GC bias matters, precompute reference stats with `-s` and pass the resulting `.gc` file back with `-r`.
4. Inspect the generated PNG/HTML outputs for insert size, coverage, GC, mismatch, and length-shape anomalies.

## Guardrails

- Local runtime is currently blocked before normal help or plotting because Perl cannot load `URI::Escape.pm`.
- The built-in source help says this parser expects `samtools stats` output, not raw BAM files and not `samtools flagstat`.
- The script also relies on `gnuplot` for figure generation; plan for both Perl-module and plotting-tool dependencies.
- `--help` could not be exercised cleanly here because the missing Perl module aborts compilation first; the available option surface was recovered from the script's own `error()` usage block.
- `-m` is a merge-to-stdout mode, so do not expect plots when that switch is present.
