---
name: segmasker
description: Use when identifying and masking low-complexity regions in protein sequences with the SEG algorithm before BLAST or other downstream analyses.
disable-model-invocation: true
user-invocable: true
---

# segmasker

## Quick Start
- **Command:** `segmasker`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/segmasker`
- **Version:** BLAST+ 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Mask low-complexity regions in protein sequences before `blastp`, `rpsblast`, or related protein-domain searches.
- Emit interval masks, masked FASTA, or ASN.1/XML mask metadata for downstream tooling.
- Prepare masking information from FASTA or an existing protein BLAST database.
- Prefer `dustmasker` for nucleotide low-complexity masking.

## Common Patterns

```bash
# 1) Produce interval-style SEG mask coordinates
segmasker \
  -in proteins.fa \
  -out proteins.seg.interval \
  -outfmt interval
```

```bash
# 2) Emit masked FASTA for downstream protein BLAST
segmasker \
  -in proteins.fa \
  -out proteins.masked.fa \
  -outfmt fasta
```

```bash
# 3) Tune SEG aggressiveness
segmasker \
  -in proteins.fa \
  -out proteins.masked.fa \
  -outfmt fasta \
  -window 12 \
  -locut 2.2 \
  -hicut 2.5
```

## Recommended Workflow

1. Decide whether downstream tools want coordinates, masked FASTA, or mask metadata.
2. Run with default SEG parameters first; tune `-window`, `-locut`, and `-hicut` only if masking is obviously too weak or too strong.
3. Inspect the masked output before pushing it into alignment or search workflows.
4. Keep the unmasked protein FASTA alongside the masked output for traceability.

## Guardrails

- `segmasker` is the protein low-complexity masker; use `dustmasker` for nucleotide data.
- The default output format is `interval`, not FASTA.
- There is no separate hard-masking switch here; choose the output format that your downstream tool expects.
- If FASTA identifiers matter downstream, consider `-parse_seqids`.
