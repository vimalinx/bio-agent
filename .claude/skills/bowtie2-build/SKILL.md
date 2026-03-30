---
name: bowtie2-build
description: Use when building Bowtie 2 index files from reference FASTA sequences for subsequent read alignment with bowtie2.
disable-model-invocation: true
user-invocable: true
---

# bowtie2-build

## Quick Start
- **Command:** `bowtie2-build [options]* <reference_in> <bt2_index_base>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-build`
- **Version:** 2.5.5
- **Full reference:** see `references/help.md`

## When To Use This Tool

- Build a Bowtie2 index from FASTA reference sequence(s).
- Create the `.bt2` files required by `bowtie2`.
- Rebuild the index when the reference assembly changes.
- Use before any Bowtie2 alignment job that lacks an existing index prefix.

## Common Patterns

```bash
# 1) Basic Bowtie2 index build
bowtie2-build reference.fa ref_index
```

```bash
# 2) Multi-threaded build
bowtie2-build --threads 8 reference.fa ref_index
```

```bash
# 3) Force a large index
bowtie2-build --large-index reference.fa ref_index
```

## Recommended Workflow

1. Build from the exact FASTA that the project will align against.
2. Choose a stable index basename and keep it consistent in pipeline configs.
3. Verify the `.bt2` outputs exist before launching alignment jobs.
4. Document whether `--large-index` was used if the reference is unusually large.

## Guardrails
- `reference_in` can be one FASTA or a comma-separated list of FASTA files.
- The index basename controls both directory and prefix; make sure the target path is writable.
- `-c` means reference sequences are on the command line, which is uncommon for real genomes.
- `--large-index` changes index format and should be used deliberately.
