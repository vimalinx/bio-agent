---
name: esl-seqstat
description: Use when you need to compute and report statistics on biological sequence files (e.g., count, length distribution, composition) as part of HMMER/Easel workflows.
disable-model-invocation: true
user-invocable: true
---

# esl-seqstat

## Quick Start

- **Command:** `esl-seqstat [options] <seqfile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-seqstat`
- **Full reference:** See [references/help.md](references/help.md) for detailed options (use `esl-seqstat -h`)

## When To Use This Tool

- Use `esl-seqstat` when you need a quick summary of a sequence file before downstream modeling, search, or translation.
- It is appropriate for counting records, checking length ranges, and optionally reporting residue composition.
- Use `-a` when you want per-sequence lines instead of just one summary block.
- Reach for `--dna`, `--rna`, or `--amino` when automatic alphabet detection is ambiguous.

## Common Patterns

```bash
# Basic summary statistics for a sequence file
esl-seqstat sequences.fa

# Report per-sequence information
esl-seqstat -a sequences.fa

# Include residue composition in the report
esl-seqstat -c sequences.fa

# Force RNA alphabet interpretation
esl-seqstat --rna transcripts.fa
```

## Recommended Workflow

1. Verify your sequence file format is supported by Easel/HMMER tools
2. Run `esl-seqstat <seqfile>` to obtain basic statistics
3. Review output for expected sequence count and length ranges
4. Proceed with downstream HMMER analyses if statistics look correct

## Guardrails

- Use `esl-seqstat -h` for help; `--help` and `--version` are not supported flags
- Ensure the input sequence file exists and is readable before running
- This tool only reports statistics; it does not modify or filter sequences
- `--comptbl` changes the output style to a composition table rather than the default human-readable summary
