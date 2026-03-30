---
name: esl-shuffle
description: Use when shuffling biological sequences, bootstrapping alignment columns, or generating de novo random RNA, DNA, or protein controls.
disable-model-invocation: true
user-invocable: true
---

# esl-shuffle

## Quick Start

- **Command:** `esl-shuffle [options] <seqfile>` (shuffle sequences)
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-shuffle`
- **Help:** See `references/help.md` for full options (access with `-h`)

## When To Use This Tool

- Use `esl-shuffle` when you need randomized controls derived from existing sequences or alignments.
- Default mode shuffles individual sequences; `-A` switches to multiple-alignment shuffling; `-G` generates de novo random sequences.
- Reach for `-d`, `-0`, `-1`, `-w`, or `-r` when you want a specific preservation model for sequence-based controls.
- Use `-b` or `-v` in `-A` mode for bootstrap-like or per-column randomized alignment controls.

## Common Patterns

```bash
# Shuffle each input sequence while preserving monoresidue composition
esl-shuffle sequences.fa > shuffled.fa

# Preserve diresidue composition exactly
esl-shuffle -d sequences.fa > diresidue.fa

# Bootstrap alignment columns with replacement
esl-shuffle -A -b alignment.sto > bootstrap.sto

# Generate 10 random RNA sequences of length 80
esl-shuffle -G --rna -N 10 -L 80 > random-rna.fa

# Reproducible amino-acid generation
esl-shuffle -G --amino --seed 17 -N 3 -L 50 > random-aa.fa
```

## Recommended Workflow

1. Pick the correct mode first: default sequence shuffling, `-A` for alignments, or `-G` for de novo generation.
2. Choose the randomization scheme that matches the null model you actually need.
3. Add `-N`, `-L`, and `--seed` if you need multiple samples, fixed lengths, or reproducibility.
4. Force `--informat <fmt>` when autodetection is ambiguous.
5. Validate a few outputs to ensure the preserved statistics match your intended control design.

## Guardrails

- `-h` works; `--help` and `--version` are rejected by the local executable.
- Local `-h` advertises `--rna` as the default alphabet in `-G` mode, but the installed man page says one of `--rna`, `--dna`, or `--amino` must be selected. Pass the alphabet explicitly to avoid ambiguity.
- Default mode and `-A` need an input file; `-G` does not.
- `-b` and `-v` only make sense in `-A` mode, while `-d`, `-0`, `-1`, `-r`, and `-w` are sequence-mode operations.
- `-L` truncates outputs as well as setting generated-sequence length, so do not enable it casually on aligned data.
