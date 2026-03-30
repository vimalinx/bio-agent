---
name: hmmalign
description: Use when aligning sequences to a profile HMM to produce multiple sequence alignments.
disable-model-invocation: true
user-invocable: true
---

# hmmalign

## Quick Start
- **Command:** `hmmalign [options] <hmmfile> <seqfile>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hmmalign`
- **Version:** HMMER 3.4
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Add sequences to an existing HMM-guided alignment.
- Produce a multiple sequence alignment constrained by match states in a profile HMM.
- Recreate an alignment in Stockholm, Pfam, A2M, or PSIBLAST-compatible formats.
- Prefer `hmmbuild` when creating a model from an alignment instead of aligning new sequences to an existing one.

## Common Patterns

```bash
# 1) Align sequences to a profile HMM and write Stockholm output
hmmalign \
  -o aligned.sto \
  profile.hmm \
  sequences.fa
```

```bash
# 2) Preserve the original seed alignment columns when mapping new sequences
hmmalign \
  --mapali seed_alignment.sto \
  -o mapped.sto \
  profile.hmm \
  new_sequences.fa
```

```bash
# 3) Trim terminal unaligned tails and emit A2M output
hmmalign \
  --trim \
  --outformat A2M \
  -o aligned.a2m \
  profile.hmm \
  sequences.fa
```

## Recommended Workflow

1. Start from a trusted HMM built from a compatible alphabet and a sequence file in FASTA or another supported format.
2. Decide whether you need raw alignment output, mapped seed columns via `--mapali`, or trimmed termini via `--trim`.
3. Write the alignment explicitly with `-o` and set `--outformat` when downstream tools do not want Stockholm.
4. Review the aligned output before feeding it into phylogeny, consensus calling, or model rebuilding.

## Guardrails

- Positional argument order matters: HMM first, sequence file second.
- The default output format is Stockholm written to stdout unless `-o` is used.
- Use `-h` for help; `--help` and `--version` are not accepted here.
- If alphabet autodetection is ambiguous, force it with `--amino`, `--dna`, or `--rna`, and use `--informat` when sequence parsing is the problem.
