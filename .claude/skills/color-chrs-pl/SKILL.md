---
name: color-chrs-pl
description: Use when rendering `bcftools +color-chrs` `.dat` output into an SVG chromosome-coloring plot, optionally with custom haplotype colors.
disable-model-invocation: true
user-invocable: true
---

# color-chrs-pl

## Quick Start

- **Command:** `color-chrs.pl -p output-prefix output.dat`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/color-chrs.pl`
- **Help:** `perl /home/vimalinx/miniforge3/envs/bio/bin/color-chrs.pl -h`
- **Output:** writes `<prefix>.svg`

## When To Use This Tool

- Plot `.dat` files produced by `bcftools +color-chrs`.
- Build a chromosome-level SVG summary of haplotype assignments or painted regions.
- Apply a custom `chr hap color` palette instead of the built-in red / green / blue / yellow defaults.
- Combine multiple `.dat` files into one rendered figure when they belong in the same visualization.

## Common Patterns

```bash
# 1) Render a basic plot from one plugin output file
color-chrs.pl -p sample sample.dat
```

```bash
# 2) Override the default haplotype colors
color-chrs.pl -c colors.txt -p sample sample.dat
```

```bash
# 3) Merge multiple .dat inputs into one SVG
color-chrs.pl -p cohort cohort_a.dat cohort_b.dat
```

## Recommended Workflow

1. Generate one or more `.dat` files with `bcftools +color-chrs`.
2. Decide whether the default colors are acceptable or whether you need an explicit color map file.
3. Pick a unique `-p` prefix for the output figure before running the plotter.
4. Open the resulting `<prefix>.svg` and confirm the chromosome names and painted regions look sensible.

## Guardrails

- `-p` is mandatory; omitting it aborts with `Expected -p option`.
- Help is available with `-h`, `-?`, or `--help`; there is no `--version` path in this script.
- File arguments are detected by existence, so typos are treated as unknown options while real existing paths are consumed as input files wherever they appear on the command line.
- The colors file must be whitespace-delimited `chr hap color` rows.
- The plotter hard-codes chromosomes `1` through `22` plus `X`, so it is not a natural fit for arbitrary contig naming or non-human assemblies.
