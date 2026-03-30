---
name: hisat2-align-l
description: Use when aligning RNA-seq reads to a reference genome using a HISAT2 index, particularly for splice-aware alignment of transcriptomic data.
disable-model-invocation: true
user-invocable: true
---

# hisat2-align-l

## Quick Start

- **Command**: `hisat2-align-l -x <ht2-idx> {-1 <m1> -2 <m2> | -U <r>} [-S <sam>]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hisat2-align-l`
- **Full reference**: See [references/help.md](references/help.md) for complete options and usage details

## When To Use This Tool

- Use `hisat2-align-l` when aligning reads against a HISAT2 large index (`.ht2l`), typically for very large references or graph-aware indexes.
- It is especially appropriate for splice-aware RNA-seq alignment, including workflows that use known splice sites or downstream transcript assembly.
- Use it when you intentionally need the large-index binary rather than the generic `hisat2` wrapper.
- For DNA-style alignment, pair this with `--no-spliced-alignment`; otherwise spliced alignment behavior remains active by default.

## Common Patterns

```bash
# Splice-aware single-end alignment against a large index
hisat2-align-l -x genome_large -U reads.fq -S aln.sam

# Paired-end RNA-seq alignment with transcript-assembler friendly output
hisat2-align-l -x genome_large -1 reads_R1.fq -2 reads_R2.fq --dta -p 8 -S aln.sam

# Provide known splice sites to guide alignment
hisat2-align-l -x genome_large -U reads.fq --known-splicesite-infile splicesites.txt -S aln.sam

# DNA-style alignment with spliced alignment disabled
hisat2-align-l -x genome_large -U reads.fq --no-spliced-alignment -S aln.sam
```

## Recommended Workflow

1. Prepare a HISAT2 index using `hisat2-build` (produces `.ht2l` files referenced via prefix with `-x`)
2. Choose appropriate preset (`--fast`, `--sensitive`, or `--very-sensitive`) based on speed vs. sensitivity tradeoff
3. Run alignment specifying index prefix, input reads, and output SAM file: `hisat2-align-l -x genome -1 reads_1.fq -2 reads_2.fq -S output.sam`
4. Review alignment summary (printed to stderr or via `--summary-file`) for mapping statistics

## Guardrails

- Running `hisat2-align-l` directly is not recommended; prefer the `hisat2` wrapper script for typical use cases
- Large values for `-k` (max alignments per read) or `--max-seeds` can significantly slow alignment on repetitive genomes
- Thread count (`-p/--threads`) defaults to 1; increase for multi-core systems but match available resources
- Paired-end fragment bounds `-I/-X` are only valid with `--no-spliced-alignment`
