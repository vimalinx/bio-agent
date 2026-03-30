---
name: esl-translate
description: Use when translating nucleotide sequences to amino acid sequences using Easel's translation utility from the HMMER suite.
disable-model-invocation: true
user-invocable: true
---

# esl-translate

## Quick Start

- **Command:** `esl-translate [-options] <seqfile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-translate`
- **Full reference:** See `references/help.md` for detailed options (run `esl-translate -h`)

## When To Use This Tool

- Use `esl-translate` when you need quick ORF-oriented translation of nucleotide sequences into amino acid sequences.
- It is appropriate for six-frame translation scans, ORF extraction, or testing alternative genetic codes before downstream protein-domain analysis.
- Use `--watson` or `--crick` when you only want one strand instead of both.
- Reach for `-l`, `-m`, or `-M` when you need to constrain the ORFs that are reported.

## Common Patterns

```bash
# Default six-frame translation of nucleotide sequences
esl-translate transcripts.fa > orfs.fa

# Require longer ORFs
esl-translate -l 50 transcripts.fa > long_orfs.fa

# Restrict to Watson strand only
esl-translate --watson transcripts.fa > watson_orfs.fa

# Use bacterial genetic code and only AUG starts
esl-translate -c 11 -m transcripts.fa > bacterial_orfs.fa
```

## Recommended Workflow

1. Prepare your nucleotide sequence file in a supported format
2. Run `esl-translate -h` to review available options
3. Execute `esl-translate [-options] <seqfile>` with desired options
4. Verify the translated output sequences are correct

## Guardrails

- Use `-h` for help (not `--help` or `--version` which are unsupported)
- Input must be a valid sequence file `<seqfile>`
- Ensure input sequences are nucleotide (not already amino acid)
- `-m` and `-M` are stricter start-codon filters and can substantially reduce the number of reported ORFs
