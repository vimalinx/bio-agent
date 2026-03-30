---
name: esl-sfetch
description: Use when you need to extract specific sequences by name from a sequence file, or index a sequence file for faster lookup.
disable-model-invocation: true
user-invocable: true
---

# esl-sfetch

## Quick Start

- **Command**: `esl-sfetch [options] <sqfile> <name>` (single sequence) or `esl-sfetch [options] -f <sqfile> <namefile>` (multiple sequences) or `esl-sfetch [options] --index <sqfile>` (index file)
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/esl-sfetch`
- **Full reference**: See [references/help.md](references/help.md) for complete options and usage details

## When To Use This Tool

- Use `esl-sfetch` when you need random access to one or more named sequences from a sequence file.
- It is especially useful after creating an SSI index on a large FASTA or other Easel-supported sequence file.
- Use `-f` for batch extraction from a list of identifiers, and `-c/-C` when you need subsequences rather than whole records.
- Reach for it when plain `grep` is too brittle and you want indexed, format-aware retrieval.

## Common Patterns

```bash
# Index a sequence file for fast lookup
esl-sfetch --index sequences.fa

# Fetch one sequence by name
esl-sfetch sequences.fa seq123

# Fetch many sequences listed one-per-line in a file
esl-sfetch -f sequences.fa ids.txt > subset.fa

# Fetch a subsequence range from one record
esl-sfetch -c 23..100 sequences.fa seq123 > subseq.fa
```

## Recommended Workflow

1. Index the sequence file first: `esl-sfetch --index <sqfile>`
2. Identify the sequence name(s) to extract
3. Fetch sequence(s) using either single name or `-f` with a name file
4. Verify output matches expected sequences

## Guardrails

- Sequence file must exist and be readable before indexing or fetching
- Use `-h` (not `--help`) to view available options
- Run `--index` on large files before fetching to enable fast lookups
- `-C` changes the expected format of the name file: each line must carry subsequence coordinates, not just an identifier
