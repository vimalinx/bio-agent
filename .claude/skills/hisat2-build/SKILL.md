---
name: hisat2-build
description: Use when building HISAT2 index files from reference genomes for subsequent alignment with hisat2. Handles FASTA reference inputs and creates .ht2 index files.
disable-model-invocation: true
user-invocable: true
---

# hisat2-build

## Quick Start
- **Command:** `hisat2-build [options]* <reference_in> <ht2_index_base>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hisat2-build`
- **Version:** 2.2.2
- **Full reference:** See [references/help.md](references/help.md) for complete options and details

## When To Use This Tool

- Build a standard or graph-aware HISAT2 index from reference FASTA.
- Add splice sites, exons, SNPs, or haplotypes into the index when the workflow benefits from them.
- Rebuild the index when the reference or annotations change.
- Use before `hisat2` whenever the `.ht2` files do not already exist.

## Common Patterns

```bash
# 1) Basic HISAT2 index build
hisat2-build -p 8 reference.fa ref_index
```

```bash
# 2) Build with splice sites and exons
hisat2-build \
  -p 8 \
  --ss splicesites.txt \
  --exon exons.txt \
  reference.fa \
  ref_index
```

```bash
# 3) Force a large index
hisat2-build --large-index reference.fa ref_index
```

## Recommended Workflow

1. Start from the exact reference FASTA used across the RNA-seq project.
2. Add splice-site and exon files if you want a more annotation-aware index.
3. Keep the index basename stable for reproducible pipeline configuration.
4. Confirm all expected `.ht2` files exist before aligning.

## Guardrails
- Annotation sidecar files (`--ss`, `--exon`, `--snp`, `--haplotype`) must match the same reference build used in FASTA.
- `--large-index` is needed for very large references and changes the resulting index format.
- `-c` means sequence text is supplied on the command line, which is rarely appropriate for real genomes.
- Building graph-aware indexes adds complexity; use only the annotation inputs you actually trust.
