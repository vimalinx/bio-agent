---
name: vrfs-variances
description: Use when summarizing `bcftools +vrfs`/`vrfs` `SITE` output into selected sites or variance vectors from a subset of loci.
disable-model-invocation: true
user-invocable: true
---

# vrfs-variances

Perl parser for `bcftools/vrfs` `SITE` lines. It sorts candidate loci by their trailing distribution vector, keeps either a fraction or an absolute number of sites, and then emits one of three things: a default mixed summary, a site list, or a pure variance vector suitable for feeding back into `bcftools +vrfs -r`.

## Quick Start

- **Command:** `bcftools +vrfs ... | vrfs-variances -n 0.2`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vrfs-variances`
- **Input contract:** reads `SITE\t...` lines from stdin

## When To Use This Tool

- Selecting a subset of `bcftools +vrfs` sites by fraction or absolute count
- Computing the `VAR2` vector expected by downstream `bcftools +vrfs -r` workflows
- Listing which `SITE` lines survived the ranking step
- Adding reproducible random perturbation to the site distributions before variance calculation

## Common Patterns

```bash
# Default summary from 20% of sites
bcftools +vrfs ... | vrfs-variances -n 0.2
```

```bash
# Emit only the variance vector for bcftools +vrfs -r
bcftools +vrfs ... | vrfs-variances -n 100 -v > var2.txt
```

```bash
# List the selected sites instead of summary numbers
bcftools +vrfs ... | vrfs-variances -n 100 -s > selected_sites.txt
```

## Recommended Workflow

1. Feed genuine `SITE` records from `bcftools +vrfs` into stdin.
2. Decide whether `-n` should be a fraction (`<=1`) or an absolute count (`>1`).
3. Use the default mode for quick diagnostics, `-s` for site inspection, or `-v` for downstream machine-readable variance values.
4. Add `-r <seed>` only when you deliberately want stochastic perturbation and reproducibility.

## Guardrails

- This tool is stdin-driven. If stdin is a TTY and you give no arguments, it prints the help message and exits.
- Only lines beginning with `SITE` are parsed; everything else is ignored.
- `-n <= 1` is treated as a fraction of the sorted sites, while `-n > 1` is treated as an absolute count.
- Default mode writes `MEAN` and `VAR2` summaries to stderr but also prints the final selected `SITE` line to stdout, so capture streams intentionally.
- Local testing showed `-s` can duplicate the final selected site because the current code prints it once from the list-sites path and once again when the selection limit is reached.
- `-v` prints only the numeric variance vector, one value per line.
