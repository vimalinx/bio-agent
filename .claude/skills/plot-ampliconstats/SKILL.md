---
name: plot-ampliconstats
description: Use when visualizing amplicon sequencing statistics from samtools ampliconstats output, generating heatmaps and graphs for coverage and read analysis.
disable-model-invocation: true
user-invocable: true
---

# plot-ampliconstats

Perl plotting helper for `samtools ampliconstats`. It consumes an ampliconstats table and writes a prefix-based set of gnuplot scripts, PNG figures, and an `index.html` gallery.

## Quick Start

- **Command:** `plot-ampliconstats prefix [FILE]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/plot-ampliconstats`
- **Input contract:** reads `samtools ampliconstats`-style data from `FILE` or stdin if `FILE` is omitted

## When To Use This Tool

- Visualizing amplicon statistics from samtools ampliconstats output
- Generating heatmaps and graphs for amplicon coverage analysis
- Producing prefix-named PNG panels and an HTML gallery for multi-sample reports
- Adjusting plot sizing, paging, orientation, thumbnail generation, and read-depth scaling

## Common Patterns

```bash
# 1) Plot from an existing ampliconstats table
plot-ampliconstats run1 stats.txt
```

```bash
# 2) Stream directly from stdin
samtools ampliconstats ... | plot-ampliconstats run1
```

```bash
# 3) Tune layout and create thumbnails
plot-ampliconstats -orient v -page 48 -thumbnails -thumb-size 160 run1 stats.txt
```

## Recommended Workflow

1. Generate a valid ampliconstats table first, then choose a writable output prefix.
2. Decide whether you want horizontal or vertical layouts and whether large cohorts need `-page` limits.
3. Run the plotter and inspect both the `*.png` figures and the generated `index.html`.
4. Re-run with adjusted `-size`, `-size2`, `-size3`, or `-depth-max` if the default panels are cramped or clipped.

## Guardrails

- `plot-ampliconstats --help` works, but `--version` is not a real metadata flag: it prints `Unknown option: version` before the usage text.
- The script requires `gnuplot` 5.0 or later. In this environment a smoke test failed immediately with `gnuplot: No such file or directory`.
- Prefix controls many output names, not just one file. Source inspection shows outputs such as `prefix-combined-depth.png`, `prefix-heat-reads-*.png`, `prefix-*.gp`, and `index.html`.
- If `FILE` is omitted the script reads stdin. That makes it stream-friendly, but also easy to hang if the upstream producer never terminates.
- The script exposes an undocumented-but-real `--index-only` switch in `GetOptions`; do not rely on it without testing because it is not listed in the built-in usage text.
