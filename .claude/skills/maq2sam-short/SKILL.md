---
name: maq2sam-short
description: Use when converting legacy MAQ short-map files into SAM for downstream SAMtools-compatible processing.
disable-model-invocation: true
user-invocable: true
---

# maq2sam-short

## Quick Start

- **Command:** `maq2sam-short reads.map [readGroup] > reads.sam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/maq2sam-short`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Convert legacy MAQ `.map` alignment output into SAM.
- Preserve an older MAQ-based alignment result while moving it into current SAM/BAM tooling.
- Attach a simple trailing read-group label when you need to distinguish converted cohorts.
- Use this specific binary for the MAQ short-map flavor rather than the long-map variant.

## Common Patterns

```bash
# 1) Convert a MAQ short-map file to SAM
maq2sam-short \
  reads.map > reads.sam
```

```bash
# 2) Add a read-group label during conversion
maq2sam-short \
  reads.map RG1 > reads.rg.sam
```

```bash
# 3) Convert then hand off to samtools
maq2sam-short \
  reads.map > reads.sam
samtools view -bS reads.sam > reads.bam
```

## Recommended Workflow

1. Confirm the input really is the MAQ short-map flavor before choosing this binary.
2. Decide whether you want to attach the optional trailing read-group label during conversion.
3. Convert to SAM, then inspect a few records before turning the file into BAM or mixing it with other alignments.
4. Keep the original `.map` file because these legacy converters expose almost no self-describing metadata.

## Guardrails

- `maq2sam-short` does not implement real `--help` or `--version`; those strings are treated like filenames and trigger usage text only after a file-open failure.
- The optional second positional argument is just a trailing read-group label, not a full SAM `@RG` header definition.
- Use the short-map converter only for the matching MAQ map flavor; the usage text does not autodetect the correct variant for you.
- Output is plain SAM records and should be inspected before downstream compression or merging.
