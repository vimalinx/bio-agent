---
name: plot-roh-py
description: Use when plotting runs of homozygosity from `run-roh.pl` style output directories into PNG tracks, optionally filtered by region, sample list, or group contrast.
disable-model-invocation: true
user-invocable: true
---

# plot-roh-py

Python plotting script for ROH visualization. It scans a directory of `*.txt.gz` files, reads both `GT` and `RG` records, and renders per-sample ROH tracks to `plot.png` or a user-specified output file.

## Quick Start

- **Command:** `plot-roh.py <dir>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/plot-roh.py`
- **Default output:** `plot.png`

## When To Use This Tool

- Visualizing ROH calls that have already been converted into the `GT`/`RG` text format expected by the script
- Rendering static PNG ROH track plots without writing custom matplotlib code
- Filtering ROH calls by minimum length, marker count, quality, or genomic region
- Comparing grouped samples with `--highlight +group1,-group2`

## Common Patterns

```bash
# Basic non-interactive plot
plot-roh.py roh_dir -o roh.png
```

```bash
# Restrict plotted calls by region and quality/length filters
plot-roh.py roh_dir -r chr1:1-5000000 -l 100000 -n 20 -q 30 -o chr1.png
```

```bash
# Use a sample/group file and highlight calls enriched in one group
plot-roh.py roh_dir -s samples.tsv -H +cases,-controls -o grouped.png
```

## Recommended Workflow

1. Feed the script a directory containing gzipped text files with both `GT` genotype rows and `RG` region rows.
2. Use `-o` for batch output or `-i` for interactive plotting, but not both.
3. Add `-s` when you need renaming or grouping, then layer `-H` on top for between-group highlighting.
4. Tighten `-l`, `-n`, `-q`, and `-r` before plotting large cohorts so the rendered track view stays readable.

## Guardrails

- The script does not accept raw `bcftools roh` output by itself; the source explicitly says it expects extra `GT` lines such as those produced by `run-roh.pl`.
- A directory with only `RG` rows failed in live testing with `IndexError: list index out of range` because `RG` rows must include at least eight columns, including quality.
- A minimal gzipped file containing two `GT` rows plus one `RG` row successfully produced a PNG (`3000 x 150`) in local testing.
- `--version` is not a real metadata path; running it without a valid data directory falls through to `No data files found in "--version"`.
- `-i/--interactive` and `-o/--outfile` are mutually exclusive, and the script will exit with a usage error if both are provided.
