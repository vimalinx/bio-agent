---
name: soap2sam-pl
description: Use when converting legacy SOAP aligner text output into SAM, including paired-end interpretation with `-p`.
disable-model-invocation: true
user-invocable: true
---

# soap2sam-pl

## Quick Start

- **Command:** `soap2sam.pl [-p] alignments.soap > alignments.sam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/soap2sam.pl`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Convert legacy SOAP text alignment output into SAM.
- Interpret mate relationships with `-p` when the SOAP file contains paired-end alignments.
- Preserve sequence, quality, mismatch count, and simple mate fields while moving into SAM-aware tooling.
- Bridge old SOAP-based pipelines into modern BAM-centric downstream steps.

## Common Patterns

```bash
# 1) Convert single-end SOAP output
soap2sam.pl \
  alignments.soap > alignments.sam
```

```bash
# 2) Convert paired-end SOAP output
soap2sam.pl \
  -p \
  paired.soap > paired.sam
```

```bash
# 3) Convert then compress with samtools
soap2sam.pl \
  -p \
  paired.soap > paired.sam
samtools view -bS paired.sam > paired.bam
```

## Recommended Workflow

1. Confirm the input is SOAP text output and decide whether the file is paired-end before setting `-p`.
2. Convert to SAM, then inspect a few records for read names, orientation flags, and mismatch tags.
3. Validate that mate pairing still makes sense if the SOAP file was reordered upstream.
4. Compress or sort with `samtools` only after confirming the converted SAM looks structurally correct.

## Guardrails

- `-p` only toggles paired-end interpretation; it assumes mates arrive in the expected order and does not recover arbitrarily shuffled records.
- Help comes from Perl `Getopt::Std`, so `--help` works generically but `-help` is the wrong pattern for this script family.
- The script trims the quality string to sequence length if SOAP reports a longer quality field.
- Output is plain SAM records without a SAM header.
