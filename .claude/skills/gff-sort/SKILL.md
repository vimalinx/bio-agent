---
name: gff-sort
description: Use when you need to reorder GFF3 records so parent features stay ahead of children in EDirect-style annotation pipelines.
disable-model-invocation: true
user-invocable: true
---

# gff-sort

## Quick Start

- **Command:** `PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/gff-sort < input.gff3 > sorted.gff3`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gff-sort`
- **Full reference:** See [references/help.md](references/help.md) for complete usage details

## When To Use This Tool

- Sort unsorted GFF3 feature streams while keeping `gene` / `pseudogene` before transcripts, then `CDS`, then `exon` / `intron`.
- Clean up record order after concatenating annotations or generating GFF programmatically.
- Use inside EDirect pipelines when you already have companion helpers such as `tbl2xml`, `xtract`, `transmute`, and `sort-table`.

## Common Patterns

```bash
# 1) Sort an unsorted GFF3 body in EDirect's expected feature order
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/gff-sort \
  < unsorted.gff3 \
  > sorted.gff3
```

```bash
# 2) Re-sort merged annotation fragments before downstream use
cat part1.gff3 part2.gff3 part3.gff3 | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/gff-sort \
  > merged.sorted.gff3
```

## Recommended Workflow

1. Put the EDirect bin directory on `PATH`; this wrapper depends on sibling tools and cannot run standalone by absolute path alone.
2. Feed it a valid tab-delimited GFF3 stream on stdin.
3. Spot-check that parent-child ordering is now `gene` -> transcript/RNA -> `CDS` -> `exon` / `intron`.
4. Reattach header or directive lines separately if downstream tools require them.

## Guardrails

- This script has no real built-in help or version mode; with missing companion tools it can still exit after printing `command not found` errors.
- It strips comment and directive lines such as `##gff-version 3`, so preserve headers separately if you need them later.
- Feature precedence is hard-coded: `gene` / `pseudogene` first, RNA-like features second, `CDS` third, `exon` / `intron` fourth, everything else last.
- Sorting relies on sibling EDirect tools (`tbl2xml`, `xtract`, `transmute`, `sort-table`) being discoverable on `PATH`.
