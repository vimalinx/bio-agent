---
name: interpolate-sam-pl
description: Use when deriving interpolated per-base coverage counts from a sorted SAM file, especially across paired-end inserts.
disable-model-invocation: true
user-invocable: true
---

# interpolate-sam-pl

## Quick Start

- **Command:** `interpolate_sam.pl sorted.sam > interpolated.txt`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/interpolate_sam.pl`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Turn a sorted SAM file into an interpolated base-by-base coverage trace.
- Count bases spanned between paired ends rather than only piling up aligned read sequence.
- Generate simple per-position depth summaries from older MAQ-style SAM workflows.
- Produce a lightweight text coverage profile without launching a full coverage toolkit.

## Common Patterns

```bash
# 1) Generate interpolated per-base counts from a sorted SAM file
interpolate_sam.pl \
  alignments.sorted.sam > interpolated.txt
```

```bash
# 2) Save per-contig coverage blocks for downstream plotting
interpolate_sam.pl \
  alignments.sorted.sam > coverage.blocks.txt
```

```bash
# 3) Inspect the first region header and counts
interpolate_sam.pl \
  alignments.sorted.sam | head -n 40
```

## Recommended Workflow

1. Start from a SAM file that is already sorted in the order expected by the script.
2. Confirm the reference names and CIGAR strings match the assumptions documented in the source comments.
3. Generate the interpolated count output, then inspect the `#RNAME` block headers and early counts for sanity.
4. Use the output as a lightweight diagnostic or plotting input rather than as a drop-in replacement for modern pileup/depth tools.

## Guardrails

- This script expects a SAM filename as its first positional argument; `--help` and `--version` are treated as missing-file names and error out.
- The input SAM must be sorted.
- It expects simple CIGAR operations (`M`, `I`, and `D`) and a colon-delimited `RNAME` format such as `chromosome:NCBI36:18:1:76117153:1`.
- The source comments note an MAQ-specific assumption that flag `0x0010` marks the second read in paired-end data, so validate behavior before using it on arbitrary modern SAM files.
