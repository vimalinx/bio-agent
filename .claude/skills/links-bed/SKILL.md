---
name: links-bed
description: Use when you need to generate HTML links to UCSC Genome Browser from BED, GFF, or VCF feature files.
disable-model-invocation: true
user-invocable: true
---

# links-bed

## Quick Start
- **Command:** `linksBed -i intervals.bed [options] > links.html`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/linksBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Generate clickable UCSC Genome Browser links for an interval file.
- Create lightweight HTML for manual browsing of genomic coordinates.
- Point links at a local UCSC mirror instead of the public site.
- Override organism and assembly when the defaults are wrong for your dataset.

## Common Patterns

```bash
# 1) Create UCSC links with defaults
linksBed \
  -i peaks.bed > peaks.links.html
```

```bash
# 2) Target a different organism / assembly
linksBed \
  -i peaks.bed \
  -org mouse \
  -db mm10 > peaks.mm10.links.html
```

```bash
# 3) Point links at a local UCSC mirror
linksBed \
  -i peaks.bed \
  -base http://mymirror.example.org \
  -org human \
  -db hg38 > peaks.local.links.html
```

## Recommended Workflow

1. Confirm the interval file uses coordinates compatible with the intended UCSC assembly.
2. Override `-org` and `-db` explicitly for modern datasets instead of accepting the defaults.
3. Open the generated HTML and spot-check a few links before sharing it.
4. Treat this as a browsing convenience tool, not a primary data export format.

## Guardrails

- The defaults are `human` and `hg18`, which are usually wrong for current work.
- `-base` only changes the browser hostname; it does not validate that your mirror has the chosen assembly.
- Output is HTML written to stdout, so redirect it to a file.
- Input should be BED / GFF / VCF-like coordinates that UCSC can interpret sensibly.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.
