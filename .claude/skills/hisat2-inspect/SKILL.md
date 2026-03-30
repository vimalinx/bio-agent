---
name: hisat2-inspect
description: Use when you need to inspect HISAT2 index files, extract reference sequences, view index summaries, or retrieve SNP/splice site/exon information from a .ht2 index.
disable-model-invocation: true
user-invocable: true
---

# hisat2-inspect

## Quick Start

- **Command:** `hisat2-inspect [options] <ht2_base>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hisat2-inspect`
- **Full reference:** See [`references/help.md`](references/help.md) for complete options and usage details

## When To Use This Tool

- Use `hisat2-inspect` when you need to audit what is stored inside a HISAT2 index basename before alignment or debugging.
- It is the generic entry point for recovering FASTA, listing reference names, printing summaries, or extracting embedded SNP/splice/exon annotations.
- Use `--large-index` when you need to force inspection of a large index even if a small one is also present.
- Reach for this wrapper before the `-s` and `-l` direct executables unless you specifically need to pin the index flavor.

## Common Patterns

```bash
# Summarize a HISAT2 index
hisat2-inspect -s genome

# List reference names only
hisat2-inspect -n genome

# Extract embedded splice sites and exons
hisat2-inspect --ss genome > splicesites.txt
hisat2-inspect --exon genome > exons.txt

# Reconstruct FASTA from the index
hisat2-inspect genome > genome_from_index.fa
```

## Recommended Workflow

1. Identify the `.ht2` index base name (filename minus trailing `.1.ht2`/`.2.ht2`)
2. Run `hisat2-inspect -s <ht2_base>` to view a summary of index contents and parameters
3. Use `-n` to list reference names only, or run without flags to output full FASTA sequences
4. Add `--snp`, `--ss`, or `--exon` flags as needed to extract specialized annotation data

## Guardrails

- Provide the index base name without the `.1.ht2`/`.2.ht2` suffix, not the full filename
- Extracting full FASTA with `-e/--ht2-ref` is slow; prefer default output unless color preservation is required
- Use `--large-index` flag only when forcing inspection of a large index variant
