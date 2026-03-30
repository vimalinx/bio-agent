---
name: esl-histplot
description: Use when turning one numeric value per line into Easel or xmgrace histogram or survival-plot data for score-distribution analysis.
disable-model-invocation: true
user-invocable: true
---

# esl-histplot

## Quick Start

- **Command:** `esl-histplot [-options] <datafile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/esl-histplot`
- **Full reference:** See `references/help.md` for `--help` failure behavior and `esl-histplot -h` output

## When To Use This Tool

- Use `esl-histplot` when you have one numeric value per line, or one numeric field per whitespace-delimited line, and you need an XY data file describing its distribution.
- It is useful for search-score distributions, simulation outputs, fit diagnostics, or any workflow where Easel-compatible histogram or survival data is easier to inspect than raw numbers.
- Reach for `--surv` when you want a survival curve instead of histogram bins.
- Use the ML fit options such as `--gumbel`, `--exptail`, `--gev`, or `--normal` when comparing empirical distributions to common score models.

## Common Patterns

```bash
# Histogram from the first field of a text file
esl-histplot scores.txt > scores.xy

# Read the second field from a tabular file
esl-histplot -f 2 metrics.tsv > field2.xy

# Emit a survival plot instead of histogram bins
esl-histplot --surv scores.txt > survival.xy

# Fit a Gumbel curve to the observed score distribution
esl-histplot --gumbel -t 0.01 scores.txt > gumbel-fit.xy
```

## Recommended Workflow

1. Prepare a text file with one relevant numeric value per line, or choose a field with `-f`.
2. Run the default mode first on a small sample so you know what the emitted XY file represents in your local environment.
3. Adjust output type and binning with `--surv`, `-w`, `--min`, and `--max`.
4. Add a fit option only after confirming the raw distribution looks sensible.
5. Plot the resulting XY file in xmgrace or another plotting tool that can read plain coordinate pairs.

## Guardrails

- `-h` works; `--help` and `--version` are rejected by the local executable.
- The installed man page says the default output is a survival plot, but the live local binary emits histogram-style XY output unless `--surv` is set. Verify default semantics on a small sample before automating around it.
- `datafile` may be `-` to read from stdin.
- Output is xmgrace-style XY data, not a rendered image file.
- With text input, `-f <n>` is 1-based field indexing.
