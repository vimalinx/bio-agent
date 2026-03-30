---
name: esl-mixdchlet
description: Use when fitting, scoring, generating, or sampling mixture Dirichlet priors for count-vector data used in HMMER or Infernal-style models.
disable-model-invocation: true
user-invocable: true
---

# esl-mixdchlet

## Quick Start

- **Command:** `esl-mixdchlet`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-mixdchlet`
- **Version:** 0.49
- **Reference:** See [references/help.md](references/help.md) for detailed options and usage

## When To Use This Tool

- Use `esl-mixdchlet` when you need to train or inspect mixture Dirichlet priors from count vectors, such as emission or transition counts from profile-model training sets.
- Use `fit` to estimate a new prior, `score` to evaluate count data against an existing prior, `gen` to synthesize count vectors, and `sample` to create random priors for testing.
- It is most relevant in HMMER or Infernal-style modeling pipelines where count vectors are already available and you need reusable prior files.

## Common Patterns

```bash
# Fit a 9-component amino-acid prior from count vectors of length 20
esl-mixdchlet fit 9 20 counts.tsv aa.mixdchlet

# Score observed counts against an existing prior
esl-mixdchlet score aa.mixdchlet counts.tsv

# Generate 500 synthetic count vectors with 50 counts each
esl-mixdchlet gen -N 500 -M 50 aa.mixdchlet > synthetic.counts

# Sample a random 4-component nucleotide prior for testing
esl-mixdchlet sample -K 4 -Q 4 > random.mixdchlet
```

## Recommended Workflow

1. Decide which subcommand matches the task: `fit`, `score`, `gen`, or `sample`.
2. For `fit`, prepare one count vector per line with exactly `K` numeric fields; weighted real-valued counts are allowed.
3. Use `-s <seed>` whenever you need reproducible fitting, sampling, or data generation.
4. Validate the resulting prior by scoring held-out counts or by generating synthetic data for sanity checks.
5. Feed the saved mixture Dirichlet file into downstream model-building code only after the component count `Q` and alphabet size `K` look sensible.

## Guardrails

- Top-level and subcommand help both use `-h`; `--help` is rejected locally.
- `--version` works at the top level, which is unusual for this Easel family.
- `fit` takes arguments as `Q K in_countfile out_mixdchlet`, but the written prior file begins with `K Q` on its first line; do not mix those orders up.
- `sample` writes the sampled prior to stdout unless redirected.
- `score` only evaluates data; it does not refit parameters.
