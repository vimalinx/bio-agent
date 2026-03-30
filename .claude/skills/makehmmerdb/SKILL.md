---
name: makehmmerdb
description: Use when building HMMER binary-formatted sequence databases from plain sequence files, especially for hmmpgmd-style serving or specialized accelerated workflows.
disable-model-invocation: true
user-invocable: true
---

# makehmmerdb

## Quick Start
- **Command**: `makehmmerdb [options] <seqfile> <binaryfile>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/makehmmerdb`
- **Version:** HMMER 3.4
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Convert a plain sequence file into HMMER's binary database format.
- Prepare sequence databases for `hmmpgmd`-style server workflows or other binary HMMER database use cases.
- Tune binary DB layout parameters such as suffix-array sampling and block size when serving large collections.
- Do not confuse this with `hmmpress`, which prepares HMM profile databases rather than sequence databases.

## Common Patterns

```bash
# 1) Build a binary HMMER database from a FASTA sequence file
makehmmerdb proteins.fa proteins.hmmerdb
```

```bash
# 2) Declare the input format explicitly
makehmmerdb \
  --informat fasta \
  proteins.fa \
  proteins.hmmerdb
```

```bash
# 3) Tune layout parameters for a large database
makehmmerdb \
  --bin_length 512 \
  --sa_freq 8 \
  --block_size 100 \
  proteins.fa \
  proteins.hmmerdb
```

## Recommended Workflow

1. Start from a stable sequence file in FASTA or another explicitly declared format.
2. Build the binary database into a dedicated output path rather than mixing it into an ordinary FASTA directory.
3. Keep the original sequence file because most other HMMER tools still operate directly on plain sequence or HMM inputs.
4. Use the binary DB only in the workflows that explicitly expect it.

## Guardrails

- This builds a binary sequence database, not a pressed HMM profile database.
- It expects exactly two positional arguments: input sequence file then output binary database path.
- Use `-h` for help; `--help` and `--version` are not valid here.
- The binary strings in this local build point to `hmmpgmd`, so treat this as infrastructure-oriented tooling rather than a mandatory step for ordinary `hmmsearch` or `hmmscan`.
