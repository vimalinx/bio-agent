---
name: prodigal
description: Use when predicting protein-coding genes in prokaryotic genomes or metagenomic sequences
disable-model-invocation: true
user-invocable: true
---

# prodigal

## Quick Start
- **Command:** `prodigal -i input.fna -o output.gff -a proteins.faa`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/prodigal`
- **Version:** Prodigal V2.6.3
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Predict protein-coding genes in bacterial or archaeal genomes.
- Annotate fragmented contigs or metagenomic assemblies with `-p meta`.
- Emit proteins, nucleotide CDS sequences, and GFF/GenBank/SCO annotations from the same run.
- Prefer `prodigal` for prokaryotic gene calling, not eukaryotic genome annotation.

## Common Patterns

```bash
# 1) Standard prokaryotic genome annotation with proteins and GFF
prodigal \
  -i assembly.fna \
  -o genes.gff \
  -f gff \
  -a proteins.faa
```

```bash
# 2) Metagenome mode for fragmented contigs
prodigal \
  -i contigs.fna \
  -p meta \
  -o genes.gff \
  -a proteins.faa \
  -d cds.fna
```

```bash
# 3) Save and reuse a training file
prodigal \
  -i genome.fna \
  -t prodigal.trn \
  -o genes.gbk
```

## Recommended Workflow

1. Start from a prokaryotic nucleotide assembly or contig set.
2. Choose `-p single` for a coherent isolate genome or `-p meta` for fragmented metagenomic data.
3. Always request proteins with `-a`, and often CDS sequences with `-d`, so downstream annotation has direct sequence inputs.
4. Review coordinates and translation outputs before chaining into functional annotation or comparative genomics.

## Guardrails

- This is a prokaryotic gene finder; it is not appropriate for eukaryotic intron-rich genomes.
- The default translation table is 11; set `-g` explicitly for unusual genetic codes.
- Use `-m` if runs of `N` should break genes rather than being spanned.
- `-v` prints the version; `--help` and `--version` are not the right interface here.
