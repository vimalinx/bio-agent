---
name: subread-buildindex
description: Use when building an index from a reference sequence for Subread alignment tools.
disable-model-invocation: true
user-invocable: true
---

# subread-buildindex

## Quick Start

- **Command:** `subread-buildindex -o <basename> <reference.fa[.gz]>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/subread-buildindex`
- **Version:** 2.1.1
- **Full reference:** See `references/help.md` for detailed options and usage

## When To Use This Tool

- Build the reference index required by `subread-align` and `subjunc`.
- Tune index layout for memory or speed with `-F`, `-B`, and `-M`.
- Create the index once per reference build, then reuse it across samples.

## Common Patterns

```bash
# 1) Default index build
subread-buildindex -o ref_index genome.fa
```

```bash
# 2) Build from gzipped FASTA
subread-buildindex -o ref_index genome.fa.gz
```

```bash
# 3) Favor speed at the cost of larger memory/index size
subread-buildindex -o ref_index -F -B -M 16000 genome.fa
```

## Recommended Workflow

1. Choose a stable basename for the index; downstream aligners refer to that basename with `-i`.
2. Build from the exact FASTA used for the project assembly and annotation.
3. Decide whether you want the default compact index or a larger full index with `-F`.
4. Verify the expected index files exist before aligning any sample.

## Guardrails

- The required argument is `-o <basename>`; the reference FASTA comes after options as positional input.
- `-F` builds a full index that is larger on disk but can improve alignment behavior for some workloads.
- `-B` disables index splitting and can increase alignment memory use substantially.
- `-M` is the requested RAM budget in MB during index building; raise it explicitly for large genomes.
