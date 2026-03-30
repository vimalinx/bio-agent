---
name: cutadapt
description: Use when you need to remove adapter sequences from high-throughput sequencing reads, trim low-quality bases, or filter reads by length. Supports single-end and paired-end FASTQ/FASTA input with error-tolerant adapter matching.
disable-model-invocation: true
user-invocable: true
---

# cutadapt

## Quick Start
- **Command:** `cutadapt -a ADAPTER -o output.fastq input.fastq`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/cutadapt`
- **Version:** 5.2
- **Full reference:** See [references/help.md](references/help.md) for complete options and documentation

## When To Use This Tool

- Remove known adapter sequences with explicit 3', 5', or anywhere-end semantics.
- Paired-end trimming where read synchronization must be preserved exactly.
- Quality trimming and length filtering after or alongside adapter removal.
- Prefer `cutadapt` over `fastp` when the adapter model itself needs precise control.

## Common Patterns

```bash
# 1) Trim a known 3' adapter from single-end reads
cutadapt \
  -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCA \
  -o sample.trimmed.fastq.gz \
  sample.fastq.gz
```

```bash
# 2) Paired-end trimming with separate R1/R2 adapters
cutadapt \
  -a ADAPTER_R1 \
  -A ADAPTER_R2 \
  -o sample_R1.trimmed.fastq.gz \
  -p sample_R2.trimmed.fastq.gz \
  sample_R1.fastq.gz sample_R2.fastq.gz
```

```bash
# 3) Adapter trimming plus quality/length filtering
cutadapt \
  -a ADAPTER \
  -q 20 \
  -m 50 \
  --json sample.cutadapt.json \
  -o sample.trimmed.fastq.gz \
  sample.fastq.gz
```

## Recommended Workflow

1. Determine whether the adapter is expected at the 3' end, 5' end, or either end.
2. Encode that expectation with `-a`, `-g`, or `-b` rather than using a vague fallback.
3. Add quality and length filters after the adapter model is correct.
4. Review the cutadapt report or JSON output before sending reads downstream.

## Guardrails

- Without `-o`, reads go to stdout; that is fine for piping, but dangerous if you expected a file.
- For paired-end data, always provide both inputs and both outputs so mate synchronization is preserved.
- `-b/--anywhere` is powerful but easy to misuse; do not use it unless you really want 5' or 3' matching.
- Use `-j` to parallelize larger jobs; default execution is single-core.
