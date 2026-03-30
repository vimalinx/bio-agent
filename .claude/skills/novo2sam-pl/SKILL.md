---
name: novo2sam-pl
description: Use when converting legacy Novoalign text output into SAM, especially for unique alignments and optional paired-end interpretation.
disable-model-invocation: true
user-invocable: true
---

# novo2sam-pl

## Quick Start

- **Command:** `novo2sam.pl [-p] alignments.novo > alignments.sam`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/novo2sam.pl`
- **Reference:** See [references/help.md](references/help.md)

## When To Use This Tool

- Convert legacy Novoalign output into SAM.
- Interpret mate relationships with `-p` when the Novoalign output contains paired reads.
- Preserve read sequence and quality while translating older Novoalign text into a SAM-compatible form.
- Handle gapped Novoalign variation strings without rewriting the entire conversion logic yourself.

## Common Patterns

```bash
# 1) Convert single-end Novoalign output
novo2sam.pl \
  alignments.novo > alignments.sam
```

```bash
# 2) Convert paired-end Novoalign output
novo2sam.pl \
  -p \
  paired_alignments.novo > paired.sam
```

```bash
# 3) Stream a filtered Novoalign file through the converter
grep -v '^#' alignments.novo | novo2sam.pl > alignments.sam
```

## Recommended Workflow

1. Confirm the input is Novoalign's legacy text alignment format rather than already-formed SAM/BAM.
2. Enable `-p` only when the file contains paired reads in the expected alternating layout.
3. Convert to SAM, then inspect a few records for pairing flags, CIGAR strings, and sequence orientation.
4. If you need non-unique or QC-failed rows preserved, verify the converter's filtering behavior before trusting the output.

## Guardrails

- The script silently skips lines it considers QC/NM summary output and ignores alignments whose status field is not `U` (unique), so it is not a lossless converter for all Novoalign record types.
- `-p` changes mate interpretation only; it does not repair arbitrarily shuffled paired-end records.
- Help comes from Perl `Getopt::Std`, so `--help` works generically but `-help` is the wrong pattern for this script family.
- Output is plain SAM records without a SAM header.
