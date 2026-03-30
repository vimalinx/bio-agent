---
name: gene2range
description: Use when converting Entrez Gene `DocumentSummary` XML for one chromosome into sorted `GENE` interval XML.
disable-model-invocation: true
user-invocable: true
---

# gene2range

## Quick Start

- **Command:** `PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/gene2range chr1 < gene_summaries.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/gene2range`
- **Reference:** See `references/help.md` for detailed usage and examples

## When To Use This Tool

- Filter `DocumentSummary` XML down to one chromosome with normalized `Min` / `Max` coordinates.
- Convert Entrez Gene summaries into `GENE` XML blocks that downstream helpers such as `find-in-gene` can consume.
- Preserve strand direction by inferring `plus` or `minus` from `ChrStart` versus `ChrStop`.

## Common Patterns

```bash
# 1) Convert chr1 gene summaries into sorted GENE XML
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/gene2range chr1 \
  < gene_summaries.xml \
  > chr1_ranges.xml
```

```bash
# 2) Use directly in a larger Entrez XML pipeline
upstream_gene_summary_command | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/gene2range chr2
```

## Recommended Workflow

1. Start from `DocumentSummary` XML that still contains `GenomicInfoType` blocks.
2. Pass the target chromosome name as the sole positional argument.
3. Capture the emitted `GENE` XML and inspect a few records for `Strand`, `Min`, `Max`, `Id`, `Name`, and `Desc`.
4. Feed that XML into downstream interval helpers only after confirming the chromosome filter behaved as expected.

## Guardrails

- The only required positional argument is the chromosome name; the script reads gene summaries from stdin.
- This wrapper depends on sibling EDirect tools (`xtract`, `sort-table`, `tbl2xml`), so absolute-path invocation alone can still fail if the bio / EDirect bin directory is missing from `PATH`.
- Output is XML, not a plain TSV coordinate table.
- Strand is inferred by comparing `ChrStart` and `ChrStop`; reversed genomic coordinates are normalized into `Min` / `Max` with `Strand=minus`.
