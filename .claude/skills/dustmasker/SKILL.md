---
name: dustmasker
description: Use when masking low-complexity regions in nucleotide sequences using the Symmetric DUST algorithm before BLAST searches or other sequence analyses.
disable-model-invocation: true
user-invocable: true
---

# dustmasker

## Quick Start
- **Command:** `dustmasker -in input.fasta -out masked.out -outfmt fasta`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/dustmasker`
- **Version:** BLAST+ 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Mask low-complexity nucleotide regions before running BLAST or related seed-based searches.
- Produce interval masks, mask ASN.1/XML, or masked FASTA depending on downstream needs.
- Prepare masking information from FASTA or an existing nucleotide BLAST database.
- Prefer `segmasker` for protein low-complexity masking, not `dustmasker`.

## Common Patterns

```bash
# 1) Emit interval-style mask coordinates
dustmasker \
  -in genome.fa \
  -out genome.mask.interval \
  -outfmt interval
```

```bash
# 2) Produce soft-masked FASTA for downstream nucleotide BLAST
dustmasker \
  -in genome.fa \
  -out genome.softmasked.fa \
  -outfmt fasta
```

```bash
# 3) Produce hard-masked FASTA with Ns in masked regions
dustmasker \
  -in genome.fa \
  -out genome.hardmasked.fa \
  -outfmt fasta \
  -hard_masking
```

## Recommended Workflow

1. Decide whether downstream tools want interval masks, FASTA output, or mask metadata in ASN.1/XML.
2. Run with default DUST parameters first; only tune `-window`, `-level`, or `-linker` when the default masking is clearly too weak or too aggressive.
3. Use soft-masked FASTA for most BLAST workflows unless your pipeline explicitly requires hard masking.
4. Inspect the masked fraction before assuming the preprocessing improved search specificity.

## Guardrails

- This tool is for nucleotide input only.
- The default output format is `interval`, not FASTA.
- `-hard_masking` only matters when you request FASTA output.
- If FASTA identifiers matter downstream, consider `-parse_seqids` so sequence IDs are interpreted correctly.
