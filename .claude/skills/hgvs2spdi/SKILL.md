---
name: hgvs2spdi
description: Use when converting EDirect HGVS XML records into NCBI SPDI XML, optionally with a precomputed accession-to-CDS-offset transform table.
disable-model-invocation: true
user-invocable: true
---

# hgvs2spdi

## Quick Start

- **Command:** `... | hgvs2spdi [transform.tsv]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hgvs2spdi`
- **Output:** formatted XML with `Id`, `Hgvs`, and `Spdi` fields

## When To Use This Tool

- Convert HGVS records produced inside an EDirect pipeline into SPDI coordinates.
- Resolve CDS-relative HGVS notations against transcript-specific coding-start offsets.
- Keep working in XML-based NCBI tooling instead of manually translating coordinates.
- Reuse a cached transform table when you want to avoid repeated live accession lookups.

## Common Patterns

```bash
# 1) Convert HGVS extracted from dbSNP docsum records
efetch -db snp -id 11549407 -format docsum |
xtract -rec HGVS -pattern DocumentSummary -wrp Id -element Id -rst -hgvs DOCSUM |
hgvs2spdi
```

```bash
# 2) Use a precomputed accession-to-offset transform file
xtract -rec HGVS -pattern DocumentSummary -wrp Id -element Id -rst -hgvs DOCSUM < input.xml |
hgvs2spdi cds_offsets.tsv
```

```bash
# 3) Inspect the resulting SPDI XML
... | hgvs2spdi | xtract -pattern Variant -element Accession,Position,Deleted,Inserted,Spdi
```

## Recommended Workflow

1. Feed the tool HGVS XML, not raw HGVS strings.
2. Decide whether to let the wrapper compute transcript offsets live or to pass an existing `accession<TAB>offset` table as the optional positional file argument.
3. Inspect the emitted `Hgvs` and `Spdi` fields together before downstream storage or querying.
4. Cache transform tables when converting many transcript-relative HGVS records from the same accession set.

## Guardrails

- `hgvs2spdi` reads its HGVS records from stdin; a positional file argument is only for the optional transform table.
- There is no real help path; `hgvs2spdi --help` with empty stdin exits silently.
- Without a transform file, the wrapper performs live `efetch` / `gbf2xml` lookups to derive CDS-start offsets for transcript accessions.
- The transform table is expected to contain `Accession<TAB>offset` rows suitable for `xtract -transform`.
- Output is XML, not a bare `accession:position:deleted:inserted` text line.
- The wrapper depends on sibling EDirect helpers such as `xtract`, `print-columns`, `gbf2xml`, and `transmute` being on `PATH`.
