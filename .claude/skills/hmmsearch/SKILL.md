---
name: hmmsearch
description: Use when searching profile hidden Markov models against sequence databases to identify homologous sequences or protein family members
disable-model-invocation: true
user-invocable: true
---

# hmmsearch

## Quick Start
- **Command:** `hmmsearch [options] <hmmfile> <seqdb>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hmmsearch`
- **Version:** HMMER 3.4
- **Full reference:** See [references/help.md](references/help.md) for detailed options and usage

## When To Use This Tool

- Search one or more profile HMMs against a sequence database.
- Identify homologous proteins from a family or domain model.
- Prefer `hmmsearch` when the query is the model and the target is a sequence set.
- Prefer `hmmscan` when the query is the sequence set and the target is the HMM database.

## Common Patterns

```bash
# 1) Search one HMM against a protein FASTA database
hmmsearch \
  --tblout hits.tbl \
  --domtblout domains.tbl \
  --cpu 8 \
  kinase.hmm \
  proteome.fa
```

```bash
# 2) Use curated Pfam-style thresholds when the HMM provides them
hmmsearch \
  --cut_ga \
  --tblout hits.tbl \
  profile.hmm \
  targets.fa
```

```bash
# 3) Increase sensitivity by disabling heuristics
hmmsearch \
  --max \
  --domtblout domains.tbl \
  profile.hmm \
  targets.fa
```

## Recommended Workflow

1. Start from a trusted HMM built from a good alignment or downloaded from a curated source.
2. Save parseable output with `--tblout` and `--domtblout`; do not rely on plain-text reports alone.
3. Choose thresholding deliberately: generic E-values or curated `--cut_ga`, `--cut_tc`, or `--cut_nc`.
4. Review both per-sequence and per-domain significance before claiming family membership.

## Guardrails

- Positional argument order matters: `<hmmfile>` first, then `<seqdb>`.
- Use `-h` for help; `--help` and `--version` are not valid here.
- `--max` improves sensitivity but can slow searches down substantially.
- Save table outputs whenever results will be parsed or compared across runs.
