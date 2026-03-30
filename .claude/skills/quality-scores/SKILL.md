---
name: quality-scores
description: Use when sampling per-base Phred quality values from FASTQ, gzipped FASTQ, BAM, or SAM files via the Subread `qualityScores` utility.
disable-model-invocation: true
user-invocable: true
---

# quality-scores

## Quick Start

- **Command:** `qualityScores -i input.fastq -o output.txt`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/qualityScores`
- **Version observed locally:** `2.1.1`
- **Output shape:** one comma-separated quality vector per sampled read

## When To Use This Tool

- Extract raw per-base Phred values from sequencing files for lightweight QC or downstream summaries.
- Sample qualities from plain FASTQ, gzipped FASTQ, BAM, or SAM input.
- Restrict quality extraction to first-end or second-end reads from paired BAM / SAM files.
- Keep using Subread's small helper instead of writing a one-off parser.

## Common Patterns

```bash
# 1) Plain FASTQ input
qualityScores -i reads.fastq -o qualities.txt
```

```bash
# 2) Gzipped FASTQ input
qualityScores --gzFASTQinput -i reads.fastq.gz -o qualities.txt
```

```bash
# 3) BAM input, first mates only, with a smaller sample
qualityScores \
  --BAMinput \
  --first-end \
  --counted-reads 2000 \
  -i alignments.bam \
  -o qualities.txt
```

## Recommended Workflow

1. Pick the correct input-mode flag: none for plain FASTQ, `--gzFASTQinput`, `--BAMinput`, or `--SAMinput` as needed.
2. Set `--counted-reads` deliberately if the default sample of `10000` reads is too large or too small.
3. Run the command and inspect the output text file to confirm the expected per-read comma-separated quality values.
4. If using BAM or SAM, apply `--first-end` or `--second-end` only when you really want one mate subset.

## Guardrails

- The skill folder is `quality-scores`, but the real executable is `qualityScores`.
- Both `-i` and `-o` are required.
- The tool does not implement clean help switches: `--help` and `-h` print an unrecognized-option message and then fall through to usage text.
- Default input interpretation is plain FASTQ; BAM and SAM require explicit mode flags.
- `--first-end` and `--second-end` are only meaningful for paired BAM / SAM input.
- FASTQ Phred encoding can be adjusted with `--phred-offset 33|64`; for SAM / BAM data, scores are usually already Phred+33.
