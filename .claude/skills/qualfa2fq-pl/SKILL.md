---
name: qualfa2fq-pl
description: Use when merging a legacy FASTA file and matching QUAL file into FASTQ, including `.gz` inputs, before downstream alignment or QC steps.
disable-model-invocation: true
user-invocable: true
---

# qualfa2fq-pl

## Quick Start

- **Command:** `qualfa2fq.pl reads.fa reads.qual > reads.fastq`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/qualfa2fq.pl`
- **Inputs:** exactly two files, FASTA first and QUAL second; `.gz` suffixes are supported

## When To Use This Tool

- Convert paired FASTA + QUAL inputs into FASTQ.
- Rescue older sequencing datasets that still store bases and qualities in separate files.
- Stay in a tiny shell / Perl workflow instead of writing a custom converter.
- Prepare legacy reads for aligners or QC tools that expect FASTQ.

## Common Patterns

```bash
# 1) Basic conversion
qualfa2fq.pl reads.fa reads.qual > reads.fastq
```

```bash
# 2) Gzipped inputs are handled automatically by filename suffix
qualfa2fq.pl reads.fa.gz reads.qual.gz > reads.fastq
```

```bash
# 3) Validate the first record after conversion
qualfa2fq.pl reads.fa reads.qual | sed -n '1,8p'
```

## Recommended Workflow

1. Confirm that the FASTA and QUAL files contain the same records in the same order.
2. Run the converter and redirect stdout to a FASTQ file or immediate downstream consumer.
3. Spot-check the first few records to confirm sequence lengths and quality lengths still match.
4. Run a normal FASTQ-aware validator or QC tool before using the output in a larger pipeline.

## Guardrails

- The script requires exactly two positional arguments and has no real `--help` or `--version` interface beyond the usage error path.
- FASTA and QUAL records are consumed in lockstep, but the script does not verify matching record IDs; mismatched order silently corrupts the output.
- Quality integers are converted with `chr(score + 33)` and are not range-checked.
- The converter writes to stdout.
- `.gz` handling is suffix-based; compressed files without a `.gz` name will not be auto-decompressed.
- Sequence formatting is preserved from the FASTA record, while qualities are wrapped at 60 characters, so pre-wrapped FASTA input can produce non-canonical multi-line FASTQ records.
