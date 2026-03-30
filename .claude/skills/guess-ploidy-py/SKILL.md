---
name: guess-ploidy-py
description: Use when plotting `bcftools +guess-ploidy -v` output into a PNG summary of haploid, diploid, score, and site-count signals across samples.
disable-model-invocation: true
user-invocable: true
---

# guess-ploidy-py

## Quick Start

- **Command:** `guess-ploidy.py guess-ploidy.out image-prefix`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/guess-ploidy.py`
- **Output:** writes `image-prefix.png`

## When To Use This Tool

- Visualize the verbose output of `bcftools +guess-ploidy -v`.
- Compare haploid vs diploid likelihood signals across samples.
- Inspect the total score and number-of-sites track before deciding whether ploidy calls look plausible.
- Produce a static PNG summary without opening an interactive plotting session.

## Common Patterns

```bash
# 1) Plot the verbose plugin output
guess-ploidy.py guess-ploidy.out ploidy_summary
```

```bash
# 2) End-to-end from bcftools output to PNG
bcftools +guess-ploidy -v input.vcf.gz > guess-ploidy.out
guess-ploidy.py guess-ploidy.out cohort_x_ploidy
```

```bash
# 3) Inspect the generated artifact
file cohort_x_ploidy.png
```

## Recommended Workflow

1. Run `bcftools +guess-ploidy -v` and keep the verbose text output file.
2. Pass that file plus an output prefix to `guess-ploidy.py`.
3. Open the generated PNG and inspect the male/female score separation together with the log-scaled site-count axis.
4. Re-run the upstream ploidy call if the plotted sample ordering or score separation looks suspicious.

## Guardrails

- The script requires exactly two positional arguments; even `--help` just falls through to the generic usage message.
- It expects the verbose `guess-ploidy` text format and only uses rows beginning with `SEX`.
- Output is a static PNG only; there is no PDF / SVG option in this wrapper.
- The plot logic explicitly splits samples by sex labels `M` and `F`, so unusual or missing labels will not be grouped as intended.
- The script uses the non-interactive Matplotlib `Agg` backend and does not display a GUI window.
