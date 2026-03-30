---
name: esl-selectn
description: Use when reservoir-sampling a fixed number of random lines from a large text file or stream without loading the whole file.
disable-model-invocation: true
user-invocable: true
---

# esl-selectn

## Quick Start

- **Command:** `esl-selectn [-options] <n> <file>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-selectn`
- **Extended help:** See `references/help.md`

## When To Use This Tool

- Use `esl-selectn` when the thing you want to sample is one physical line per record.
- It is useful for downsampling huge ID lists, score tables, one-record-per-line exports, or stdin streams in a single pass.
- Reach for `--seed` when you need the same sampled subset on repeated runs.

## Common Patterns

```bash
# Sample 100 random lines from a text file
esl-selectn 100 all-records.txt > sample.txt

# Reproducible sampling with a fixed seed
esl-selectn --seed 42 500 ids.txt > ids.sample.txt

# Sample directly from a stream
cat metrics.tsv | esl-selectn 1000 - > metrics.sample.tsv
```

## Recommended Workflow

1. Make sure each logical record you care about is represented by exactly one line.
2. Choose the sample size `n` and whether you need reproducibility.
3. Run `esl-selectn` on the file or stream, redirecting stdout to the sampled output.
4. Validate the sampled line count and spot-check that the input format survived intact.

## Guardrails

- This tool samples lines, not FASTA, FASTQ, or Stockholm records. Multi-line biological records must be flattened or sampled by another method first.
- The implementation is single-pass reservoir sampling, so memory scales with `n`, not with full file size.
- `-h` works; `--help` and `--version` are rejected by the local executable.
- `file` may be `-` to read from stdin.
