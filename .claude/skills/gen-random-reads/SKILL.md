---
name: gen-random-reads
description: Use when simulating transcriptome reads from a transcript FASTA and TPM table with `genRandomReads`, or when summarizing transcript lengths before building that TPM table.
disable-model-invocation: true
user-invocable: true
---

# gen-random-reads

## Quick Start

- **Command:** `genRandomReads ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/genRandomReads`
- **Two main modes:** `--summarizeFasta` for transcript lengths, or read generation with `--transcriptFasta`, `--outputPrefix`, and `--expressionLevels`

## When To Use This Tool

- Simulate single-end or paired-end transcriptomic reads from a transcript FASTA.
- Build synthetic RNA-seq datasets from transcript-level TPM values for benchmarking.
- Summarize transcript names and lengths before constructing the TPM table.
- Encode ground-truth origins in read names when testing alignment or quantification pipelines.

## Common Patterns

```bash
# 1) Summarize transcript IDs and lengths from a FASTA file
genRandomReads \
  --summarizeFasta \
  --transcriptFasta transcripts.fa \
  --outputPrefix tx_summary
```

```bash
# 2) Generate single-end reads from a TPM table
genRandomReads \
  --transcriptFasta transcripts.fa \
  --outputPrefix sim_reads \
  --expressionLevels tpm.tsv \
  --totalReads 500000
```

```bash
# 3) Generate paired-end reads and preserve truth in read names
genRandomReads \
  --transcriptFasta transcripts.fa \
  --outputPrefix sim_pe \
  --expressionLevels tpm.tsv \
  --totalReads 200000 \
  --pairedEnd \
  --truthInReadNames
```

## Recommended Workflow

1. Run `--summarizeFasta` first so you know the available transcript IDs and lengths.
2. Build the required two-column tab-delimited expression file: `TranscriptID<TAB>TPM`.
3. Decide on read length, total reads, and whether you need paired-end simulation or truth labels in the read names.
4. Generate the dataset, then inspect the created files before feeding them into downstream aligners or quantifiers.

## Guardrails

- For read generation, `--transcriptFasta`, `--outputPrefix`, and `--expressionLevels` are required; omitting `--totalReads` triggers a warning and defaults to one million reads.
- `--help` is not a clean help path: it is reported as an unrecognized option before the usage block is printed.
- The expression file must be tab-delimited with transcript ID in column 1 and TPM in column 2.
- `--qualityRefFile` expects Phred+33 strings whose lengths match `--readLen`.
- `--simpleTranscriptId` truncates transcript names at the first `|` or space, which can change identifier matching if used carelessly.
- The transcript FASTA can be plain or gzipped (`FASTA/gz` in the usage text).
