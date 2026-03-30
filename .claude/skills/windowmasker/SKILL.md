---
name: windowmasker
description: Use when masking repetitive or low-complexity regions in genomic sequences before alignment or database searches
disable-model-invocation: true
user-invocable: true
---

# windowmasker

## Quick Start
- **Command:** `windowmasker`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/windowmasker`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Mask repetitive genomic sequence using WindowMasker's frequency-based approach.
- Build unit-count statistics for a genome or sequence collection, then apply those statistics back to mask the same kind of sequence.
- Generate interval, FASTA, or ASN.1/XML masking outputs for downstream BLAST-related workflows.
- Optionally combine repeat masking with DUST-style low-complexity filtering.

## Common Patterns

```bash
# 1) Stage 1: build unit-count statistics from FASTA
windowmasker \
  -mk_counts \
  -in genome.fa \
  -out genome.counts
```

```bash
# 2) Stage 2: apply those counts to produce interval masks
windowmasker \
  -ustat genome.counts \
  -in genome.fa \
  -out genome.mask.interval \
  -outfmt interval
```

```bash
# 3) Produce masked FASTA and combine with DUST
windowmasker \
  -ustat genome.counts \
  -in genome.fa \
  -out genome.masked.fa \
  -outfmt fasta \
  -dust true
```

## Recommended Workflow

1. Run `-mk_counts` first on representative input to generate unit-count statistics.
2. Reuse the resulting counts file with `-ustat` during the masking stage.
3. Choose `-outfmt` based on downstream expectations, keeping in mind the default is interval output.
4. Tune memory and threshold parameters only after seeing default behavior on real data.

## Guardrails

- `-mk_counts` and masking-stage options are separate modes; many arguments are mutually exclusive across them.
- `-convert` is for converting count-file formats, not for performing the normal masking stage.
- The default masking output format is `interval`, not FASTA.
- `-mem` applies to count generation, while `-smem` targets the size of the generated counts file.
- Repeat masking quality depends on representative counts; do not blindly reuse a counts file from a very different genome.
