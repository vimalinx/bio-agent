---
name: convert2blastmask
description: Use when converting lower-case masked FASTA files to masking formats compatible with makeblastdb for BLAST database preparation.
disable-model-invocation: true
user-invocable: true
---

# convert2blastmask

## Quick Start
- **Command:** `convert2blastmask -in masked.fa -out mask.asn1 -masking_algorithm <name> -masking_options <text> [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/convert2blastmask`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Convert lower-case soft-masked FASTA into mask files that `makeblastdb` can consume.
- Preserve masking provenance by recording the masking program name and options used upstream.
- Emit interval or ASN.1/XML mask representations for BLAST database preparation.
- Carry sequence IDs through with `-parse_seqids` when the masking data must stay aligned to parsed FASTA identifiers.

## Common Patterns

```bash
# 1) Convert soft-masked FASTA to the default ASN.1 text format
convert2blastmask \
  -in masked.fa \
  -out masked.asn1.txt \
  -masking_algorithm windowmasker \
  -masking_options "-mk_counts true -ustat counts.obinary"
```

```bash
# 2) Emit interval output for inspection
convert2blastmask \
  -in masked.fa \
  -out masked.interval \
  -outfmt interval \
  -masking_algorithm dust \
  -masking_options "20 64 1"
```

```bash
# 3) Keep parsed FASTA identifiers aligned with downstream BLAST DB creation
convert2blastmask \
  -in masked.fa \
  -out masked.xml \
  -outfmt maskinfo_xml \
  -parse_seqids \
  -masking_algorithm other \
  -masking_options "custom repeat masking"
```

## Recommended Workflow

1. Start from a FASTA whose masked regions are represented in lower case.
2. Record the masking method faithfully with `-masking_algorithm` and `-masking_options`; treat those fields as provenance, not decoration.
3. Choose the output format that matches how `makeblastdb` or your downstream tooling expects mask data.
4. Build the BLAST database immediately afterward so the mask file and FASTA stay synchronized.

## Guardrails

- `-masking_algorithm` and `-masking_options` are required.
- The input is lower-case masked FASTA, not BED, GFF, or interval text.
- Use BLAST+ style flags such as `-help` and `-version`; the common `--help` pattern is wrong here.
- `-parse_seqids` only helps if the FASTA deflines are parseable and you will preserve those IDs consistently into `makeblastdb`.
- The default input and output are stdin and stdout, so explicit `-in` and `-out` are safer in batch workflows.
