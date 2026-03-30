---
name: remove-dup
description: Use when removing duplicate alignments from SAM or BAM files with the Subread `removeDup` CLI and a location-count cutoff.
disable-model-invocation: true
user-invocable: true
---

# remove-dup

Subread binary for duplicate-read removal. It reads SAM or BAM, groups reads by mapped location, and drops every read at locations whose depth meets or exceeds the configured duplication threshold.

## Quick Start

- **Command:** `removeDup -i <input.sam|bam> -o <output.bam>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/removeDup`
- **Default duplication cutoff:** `10`

## When To Use This Tool

- Removing dense duplicate alignments from mapped read files before downstream counting or QC
- Applying a simple location-based duplication filter to SAM or BAM without marking duplicates first
- Forcing SAM output with `-S` when a downstream step cannot read BAM
- Running a quick Subread-native duplicate purge rather than a more feature-rich deduplication workflow

## Common Patterns

```bash
# Write BAM output with the default cutoff
removeDup -i alignments.bam -o dedup.bam
```

```bash
# Tighten the removal threshold
removeDup -i alignments.sam -o dedup.bam -r 2
```

```bash
# Emit SAM instead of BAM
removeDup -i alignments.bam -o dedup.sam -S
```

## Recommended Workflow

1. Start from a valid SAM or BAM alignment file.
2. Decide whether the default cutoff of `10` is acceptable; lower it only if you intentionally want aggressive pruning.
3. Write BAM by default, or add `-S` only when plain-text SAM is required downstream.
4. Inspect the summary banner or view the output with `samtools view` to confirm how many reads actually survived.

## Guardrails

- `-h` and `--version` are not true metadata/help switches; both are treated as invalid options, then the binary prints its usage banner and continues to complain about missing or invalid input.
- In live testing, three reads at the same locus with `-r 2` caused all three reads to be removed, confirming this tool drops the entire location bucket once the cutoff is reached.
- The usage text says output is BAM unless `-S` is specified, even though the `-o` description loosely says “output SAM file.”
- The tool requires `-i` and `-o`; invoking it without a real SAM/BAM input ends in `ERROR: The input file is neither a BAM file nor a SAM file.`
- This is a blunt duplicate filter, not a marker: it does not preserve one representative read at over-threshold loci.
