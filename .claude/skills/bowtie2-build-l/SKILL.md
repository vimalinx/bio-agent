---
name: bowtie2-build-l
description: Use when building large Bowtie 2 index files from reference sequences for alignment of reads to large genomes (>4 billion bases).
disable-model-invocation: true
user-invocable: true
---

# bowtie2-build-l

Builds large-format Bowtie 2 index files (`.bt2l` extension) from FASTA reference sequences for use with `bowtie2-align-l`.

## Quick Start

- **Command:** `bowtie2-build-l [options] <reference_in> <bt2_index_base>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-build-l`
- **Full reference:** See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Use `bowtie2-build-l` when the reference is large enough that you need Bowtie 2 large-index output (`.bt2l`).
- It is appropriate when preparing references for `bowtie2-align-l` or a wrapper that resolves to the large-index path.
- Use it for one or more FASTA files, or with `-c` when sequences are provided directly on the command line.
- Most users should call `bowtie2-build` unless they intentionally need to force the large-index builder.

## Common Patterns

```bash
# Build a large Bowtie 2 index from one FASTA
bowtie2-build-l ref.fa ref_large

# Build from multiple FASTA files
bowtie2-build-l ref1.fa,ref2.fa ref_large

# Use multiple threads during index construction
bowtie2-build-l --threads 8 ref.fa ref_large

# Build from literal reference sequence text
bowtie2-build-l -c ACGTACGT,GGGTTTAA ref_large
```

## Recommended Workflow

1. Prepare your reference sequences in FASTA format (single or multiple files)
2. Run `bowtie2-build-l <reference.fasta> <index_basename>` to generate index files
3. Verify that six `.bt2l` files were created with the specified basename
4. Use the index basename with `bowtie2 -x <index_basename>` for alignment

## Guardrails

- Consider using the `bowtie2-build` wrapper instead, as recommended by the tool warning
- Ensure sufficient memory/disk space; large references require significant resources during indexing
- Use `--threads` to parallelize builds on multi-core systems for faster processing
- The output basename should be passed later via `-x` without adding `.bt2l` suffixes manually
