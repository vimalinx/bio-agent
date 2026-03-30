---
name: zoom2sam-pl
description: Use when converting legacy Zoom aligner output into SAM and the read length must be supplied explicitly.
disable-model-invocation: true
user-invocable: true
---

# zoom2sam-pl

## Quick Start

- **Command:** `zoom2sam.pl [-p] <readLen> alignments.zoom > alignments.sam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/zoom2sam.pl`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Convert legacy Zoom aligner output into SAM.
- Supply the read length explicitly because the Zoom format handled here does not carry full SAM-ready sequence context.
- Interpret mate relationships with `-p` when the Zoom output represents paired-end reads.
- Bridge older Illumina/Zoom alignment reports into downstream SAM/BAM tooling.

## Common Patterns

```bash
# 1) Convert single-end Zoom output with known read length
zoom2sam.pl \
  76 \
  alignments.zoom > alignments.sam
```

```bash
# 2) Convert paired-end Zoom output
zoom2sam.pl \
  -p \
  100 \
  paired.zoom > paired.sam
```

```bash
# 3) Convert and then inspect the SAM body
zoom2sam.pl \
  50 \
  alignments.zoom > alignments.sam
head alignments.sam
```

## Recommended Workflow

1. Confirm the input is the default Illumina-style Zoom output expected by the script.
2. Determine the true read length before conversion and pass it as the first positional argument.
3. Add `-p` only for paired-end layouts that still preserve mate adjacency.
4. Inspect a few converted records before downstream use, especially because sequence and quality fields are not recovered from the Zoom input.

## Guardrails

- The script requires `readLen` as a positional argument; there is no automatic inference from the input file.
- It explicitly warns that it only supports the default Illumina outputs for Zoom.
- Converted SAM records use `*` for sequence and quality fields, so this is not suitable when downstream tools require real `SEQ` and `QUAL` values.
- Help comes from Perl `Getopt::Std`, so `--help` works generically but `-help` is the wrong pattern for this script family.
