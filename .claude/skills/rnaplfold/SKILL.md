---
name: rnaplfold
description: Use when computing local RNA secondary structure pair probabilities, scanning large genomes for short stable RNA structures, or analyzing unpaired region probabilities across sliding windows.
disable-model-invocation: true
user-invocable: true
---

# rnaplfold

## Quick Start

- **Command**: `RNAplfold [OPTION]...`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAplfold`
- **Reference**: See `references/help.md` for full option details

## When To Use This Tool

- Use `RNAplfold` when you care about **local** secondary structure rather than a single global fold.
- It is a good fit for scanning long transcripts or genomic windows for short stable stem-loop regions with bounded base-pair span.
- Use it when you need averaged base-pair probabilities over a sliding window, not just one minimum-free-energy structure.
- Turn on `-u` when the downstream question is accessibility or unpaired-region probability for short motifs.

## Common Patterns

```bash
# Default local folding over stdin sequence(s)
printf '>seq\nGGGAAAUCC\n' | RNAplfold

# Tune window size and maximal base-pair span for compact local structures
printf '>seq\nGGGAAAUCC\n' | RNAplfold -W 120 -L 80

# Report unpaired probabilities for regions up to length 10
printf '>seq\nGGGAAAUCC\n' | RNAplfold -u 10

# Reduce output noise to stronger local pair probabilities only
printf '>seq\nGGGAAAUCC\n' | RNAplfold -c 0.05
```

## Recommended Workflow

1. Prepare input sequences in FASTA format (T is auto-converted to U unless `--noconv` is set).
2. Set window size (`-W`, default 70) and maximum span (`-L`) based on target structure size.
3. Run `RNAplfold` with optional `-u` for unpaired region probabilities up to specified length.
4. Review output dot plot files for pair probabilities and unpaired probability data.

## Guardrails

- Set `-L` (span) explicitly; it limits the maximal separation of base pairs and affects memory/CPU usage.
- Use `-c` cutoff to filter reported base pairs by minimum average probability (default 0.01).
- For very large sequences, enable `-o` (`--print_onthefly`) to save memory by outputting during computation.
