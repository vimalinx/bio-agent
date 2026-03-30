---
name: esl-seqrange
description: Use when splitting an SSI-indexed sequence file into per-process sequence-index ranges for embarrassingly parallel Easel or HMMER jobs.
disable-model-invocation: true
user-invocable: true
---

# esl-seqrange

## Quick Start

- **Command:** `esl-seqrange [options] <sqfile> <procidx> <nproc>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-seqrange`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Use `esl-seqrange` when multiple workers need non-overlapping chunks of the same sequence database.
- It is designed for simple count-balanced partitioning of an SSI-indexed sequence file, returning a `start-end` sequence-index range for one worker.
- Reach for it when you already have worker IDs and want a quick deterministic split without writing custom indexing code.

## Common Patterns

```bash
# Build the required SSI index once
esl-sfetch --index sequences.fa

# Get the slice for worker 3 out of 8 total workers
esl-seqrange sequences.fa 3 8

# Force the input format if autodetection is ambiguous
esl-seqrange --informat fasta sequences.fa 1 16
```

## Recommended Workflow

1. Build an SSI index with `esl-sfetch --index <sqfile>` before trying to partition work.
2. Decide on the total worker count `nproc` and assign each worker a 1-based `procidx`.
3. Run `esl-seqrange` once per worker and capture the returned `start-end` range.
4. Feed those sequence-index ranges into the downstream worker logic.
5. Aggregate results knowing the split is balanced by number of sequences, not sequence length.

## Guardrails

- An SSI index is mandatory even though the short live help does not spell that out clearly; the local man page does.
- Runtime testing shows `procidx` is 1-based. `procidx=0` fails with “minimum allowed value for <procidx> is 1”.
- Partitioning is based on sequence counts only, so workloads can still be imbalanced if some sequences are much longer than others.
- `-h` works; `--help` and `--version` are rejected by the local executable.
