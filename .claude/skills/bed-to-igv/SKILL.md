---
name: bed-to-igv
description: Use when you need to generate an IGV batch script for taking snapshots at loci defined in BED, GFF, or VCF files, especially for repeatable visual review of many regions.
disable-model-invocation: true
user-invocable: true
---

# bed-to-igv

## Quick Start
- **Command**: `bedToIgv -i loci.bed -path snapshots/ [options] > review.igv.batch`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/bedToIgv`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Generate repeatable IGV snapshot scripts for a BED / GFF / VCF locus list.
- Automate review of peaks, variants, breakpoints, or candidate loci across many regions.
- Preload an IGV session with `-sess` before snapshotting.
- Standardize snapshot naming, flanking context, read sorting, and collapse settings across a review batch.

## Common Patterns

```bash
# 1) Basic IGV batch script for a BED file
bedToIgv \
  -i loci.bed \
  -path snapshots \
  > loci.igv.batch
```

```bash
# 2) Load a saved IGV session and use the BED name field for filenames
bedToIgv \
  -i peaks.bed \
  -path snapshots \
  -sess tumor-review.xml \
  -name \
  -slop 250 \
  > peaks.igv.batch
```

```bash
# 3) Sort alignments and collapse reads before each image
bedToIgv \
  -i variants.vcf \
  -path snapshots \
  -sort position \
  -clps \
  -img svg \
  > variants.igv.batch
```

## Recommended Workflow

1. Prepare the BED / GFF / VCF interval list and decide whether an existing IGV session should be loaded with `-sess`.
2. Decide where IGV should save the snapshots via `-path`, whether filenames should come from column 4 via `-name`, and whether flanking context is needed with `-slop`.
3. Run `bedToIgv` and redirect stdout into a batch-script file.
4. Open IGV, load the appropriate genome and tracks (or let `-sess` do it), then execute the batch script from within IGV.

## Guardrails

- `-path` sets the snapshot directory used inside IGV; it does not choose where the batch script itself is written.
- The command writes the IGV batch script to stdout, so redirect it to a file explicitly.
- `-name` assumes column 4 is populated with safe, unique names; otherwise the default `chr:start-end.ext` naming is safer.
- The generated script must be run from within IGV, not from the shell.
- Without `-sess`, you must load the correct genome and tracks in IGV before running the script.
