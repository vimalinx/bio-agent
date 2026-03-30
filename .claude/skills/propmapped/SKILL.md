---
name: propmapped
description: Use when you need to calculate the proportion of mapped reads or fragments from SAM/BAM alignment files to assess mapping quality and success rates.
disable-model-invocation: true
user-invocable: true
---

# propmapped

`propmapped` is a compact alignment-summary binary that reports mapped fractions for reads or fragments. In local tests it wrote results only when `-o` was provided, using a simple comma-separated summary line.

## Quick Start

- **Command:** `propmapped -i <input.sam|input.bam> [-o <out.csv>] [-f] [-p]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/propmapped`
- **Scope:** reports mapping proportion only; does not modify alignments

## When To Use This Tool

Calculating the proportion of mapped reads or fragments from alignment files in SAM or BAM format. Supports both single-end and paired-end reads, with options to count fragments as pairs or filter for properly paired reads only.

## Common Patterns

```bash
# 1) Single-end mapping fraction
propmapped -i aln.sam -o aln.mappability.csv
```

```bash
# 2) Count paired-end fragments instead of reads
propmapped -i pairs.sam -f -o pairs.fragments.csv
```

```bash
# 3) Restrict paired-end counting to properly paired fragments
propmapped -i pairs.sam -f -p -o pairs.proper.csv
```

## Recommended Workflow

1. Start from a finished SAM/BAM file, not a stream that is still being written.
2. Decide whether your unit of interest is reads or fragments before adding `-f`.
3. Use `-p` only when proper-pair status is meaningful for your dataset.
4. Save the result with `-o` and parse the emitted CSV line downstream.

## Guardrails

- Input file must be in SAM or BAM format (required `-i` argument)
- The `-f` and `-p` options are only applicable for paired-end reads
- `-h`, `--help`, and `--version` are all unrecognized options, but the binary still prints its usage banner and embedded version string (`propMapped v2.1.1`).
- The usage text contains a typo: it advertises `./prommapped`, while the actual executable is `propmapped`.
- In local tests, `propmapped -i file.sam` wrote nothing to stdout; the useful output appeared only after adding `-o`.
- A single-end smoke test produced `/path/min.sam,2,1,0.500000`, indicating the output fields are `path,total,mapped,fraction`.
- A paired-end `-f -p` test on one proper pair produced `/path/pairs.sam,1,1,1.000000`, confirming that `-f` collapses to fragment counts.
