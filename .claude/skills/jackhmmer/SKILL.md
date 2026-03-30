---
name: jackhmmer
description: Use when running iterative sequence-to-sequence HMMER searches to expand a protein family from one or a few seed sequences against a sequence database.
disable-model-invocation: true
user-invocable: true
---

# jackhmmer

## Quick Start
- **Command**: `jackhmmer`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/jackhmmer`
- **Version:** HMMER 3.4
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Start from one or a few representative protein sequences and iteratively expand the hit set across a sequence database.
- Detect more remote homologs than a one-pass `phmmer` search can usually recover.
- Build an evolving alignment of accepted hits over multiple rounds before downstream model curation.
- Prefer `hmmsearch` when you already have a profile HMM, and `hmmscan` when the target is an HMM database.

## Common Patterns

```bash
# 1) Iterative search with parseable hit tables
jackhmmer \
  --tblout hits.tbl \
  --domtblout domains.tbl \
  -N 5 \
  --cpu 8 \
  query.fa \
  targets.fa
```

```bash
# 2) Save the accepted-hit alignment from the search rounds
jackhmmer \
  -N 3 \
  -A accepted_hits.sto \
  query.fa \
  targets.fa
```

```bash
# 3) Tighten inclusion thresholds during iterative expansion
jackhmmer \
  -N 5 \
  --incE 1e-5 \
  --incdomE 1e-5 \
  query.fa \
  targets.fa
```

## Recommended Workflow

1. Start from a representative protein FASTA query and a rewindable target sequence database in FASTA or another supported sequence format.
2. Save `--tblout` and `--domtblout` outputs on the first run so iteration effects are inspectable.
3. Cap the number of rounds with `-N` and set explicit inclusion thresholds if family drift would be costly.
4. Review accepted hits and saved alignments before promoting the result into `hmmbuild` or downstream annotation.

## Guardrails

- In this workspace the binary currently fails to start because `libopenblas.so.0` is missing, so fix the runtime environment before expecting live execution.
- `jackhmmer` takes positional arguments in query-then-database order; the target `<seqdb>` cannot be a non-rewindable stdin stream.
- This is a sequence-vs-sequence iterative searcher, not a profile-vs-sequence tool.
- `jackhmmer` does not accept curated `--cut_ga`, `--cut_nc`, or `--cut_tc` threshold modes.
