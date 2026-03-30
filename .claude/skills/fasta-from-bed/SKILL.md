---
name: fasta-from-bed
description: Use when extracting DNA or RNA sequences from a FASTA file using coordinate ranges from BED, GFF, or VCF files.
disable-model-invocation: true
user-invocable: true
---

# fasta-from-bed

## Quick Start
- **Command:** `fastaFromBed -fi reference.fa -bed intervals.bed [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/fastaFromBed`
- **Alias form:** `bedtools getfasta`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Extract sequence from a reference FASTA using interval coordinates.
- Retrieve exon, peak, promoter, or variant-adjacent sequences.
- Reverse-complement antisense features with `-s`.
- Concatenate BED12 blocks with `-split`.
- Emit FASTA, tabular, or BED-like sequence output depending on downstream needs.

## Common Patterns

```bash
# 1) Basic sequence extraction to FASTA
fastaFromBed \
  -fi reference.fa \
  -bed peaks.bed \
  -fo peaks.fa
```

```bash
# 2) Strand-aware transcript sequence extraction
fastaFromBed \
  -fi reference.fa \
  -bed transcripts.bed \
  -s \
  -fo transcripts.fa
```

```bash
# 3) Extract concatenated BED12 block sequence in tabular form
fastaFromBed \
  -fi reference.fa \
  -bed transcripts.bed12 \
  -split \
  -tab > transcripts.tsv
```

## Recommended Workflow

1. Make sure FASTA headers and interval chromosome names refer to the same assembly.
2. Choose the output mode deliberately: FASTA (`default`), `-tab`, or `-bedOut`.
3. Add `-s` for strand-aware extraction and `-rna` if the reference sequence alphabet is RNA.
4. Use `-split` only when BED12 block concatenation is the intended biology.

## Guardrails

- `-fi` and `-bed` are required.
- Without `-fo`, output goes to stdout.
- `-name+` is deprecated; prefer `-name` or `-nameOnly`.
- `-split` is for BED12 block extraction and changes the extracted sequence substantially.
- By default, strand is ignored; antisense features are only reverse-complemented when `-s` is set.
