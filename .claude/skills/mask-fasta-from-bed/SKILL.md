---
name: mask-fasta-from-bed
description: Use when you need to hard-mask or soft-mask regions in a FASTA file using BED, GFF, or VCF coordinates, such as repetitive elements, blacklist regions, or loci to exclude from sequence analysis.
disable-model-invocation: true
user-invocable: true
---

# mask-fasta-from-bed

## Quick Start
- **Command**: `maskFastaFromBed -fi <input.fasta> -bed <intervals.bed> -fo <output.fasta>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/maskFastaFromBed`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Hard-mask repetitive, blacklisted, or excluded regions in a FASTA with `N` or another replacement character.
- Soft-mask regions by lowercasing the existing sequence with `-soft`.
- Apply interval masks from BED, GFF, or VCF files to a reference or contig FASTA.
- Produce a derived masked FASTA without changing the original source file.

## Common Patterns

```bash
# 1) Hard-mask listed regions with Ns
maskFastaFromBed \
  -fi genome.fa \
  -bed blacklist.bed \
  -fo genome.masked.fa
```

```bash
# 2) Soft-mask repeats by converting bases to lowercase
maskFastaFromBed \
  -fi genome.fa \
  -bed repeats.bed \
  -fo genome.softmasked.fa \
  -soft
```

```bash
# 3) Hard-mask with a custom replacement character and full FASTA headers
maskFastaFromBed \
  -fi contigs.fa \
  -bed mask-regions.bed \
  -fo contigs.masked.fa \
  -mc X \
  -fullHeader
```

## Recommended Workflow

1. Confirm the interval file uses the same sequence naming convention as the FASTA headers.
2. Choose hard masking (default), soft masking with `-soft`, or an alternate hard-mask character with `-mc`.
3. Write the result to a new FASTA via `-fo` and preserve the original FASTA as the unmasked source.
4. Spot-check a few loci to confirm the intended regions were masked and the header matching behaved as expected.

## Guardrails

- `-fo` is required; this tool does not modify the input FASTA in place.
- Default behavior replaces masked sequence with uppercase `N`; `-soft` instead lowercases the original bases.
- `-mc` changes the hard-mask character; it is not a substitute for `-soft`.
- By default bedtools matches only the first token of a FASTA header; use `-fullHeader` when interval names must match the entire header line.
- Prefer `-h` for help; GNU-style `--help` and `--version` emit wrapper errors before usage text.
