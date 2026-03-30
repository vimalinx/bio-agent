---
name: bowtie2-build-s
description: Use when building Bowtie 2 index files from reference sequences for short-read alignment.
disable-model-invocation: true
user-invocable: true
---

# bowtie2-build-s

## Quick Start

- **Command**: `bowtie2-build-s [options] <reference_in> <bt2_index_base>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-build-s`
- **Reference**: [references/help.md](references/help.md)

## When To Use This Tool

- Use `bowtie2-build-s` when building a standard Bowtie 2 small index (`.bt2`) for ordinary reference sizes.
- It is appropriate for FASTA input files or literal reference sequences supplied with `-c`.
- Use it when you specifically want to force the small-index builder rather than let the generic wrapper decide.
- In most routine workflows, `bowtie2-build` is still the preferred entry point unless you need direct control over the binary choice.

## Common Patterns

```bash
# Build a standard Bowtie 2 index from one FASTA
bowtie2-build-s ref.fa ref

# Build from multiple FASTA files
bowtie2-build-s ref1.fa,ref2.fa ref

# Parallelize index construction
bowtie2-build-s --threads 8 ref.fa ref

# Build from literal sequence strings
bowtie2-build-s -c ACGTACGT,GGGTTTAA ref
```

## Recommended Workflow

1. Prepare reference sequences in FASTA format
2. Run `bowtie2-build-s <reference.fasta> <output_basename>` to build the index
3. Verify index files were created with the specified basename
4. Use the generated index with `bowtie2 -x <basename>` for read alignment

## Guardrails

- The tool recommends using the `bowtie2-build` wrapper script instead of this direct executable
- Use `--threads <int>` to parallelize index construction on multi-core systems
- Generated indexes are compatible with Bowtie v1.2.3 and later
- The basename passed to downstream aligners should omit any `.bt2` suffix
