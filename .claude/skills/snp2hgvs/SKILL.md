---
name: snp2hgvs
description: Use when converting NCBI dbSNP docsum XML into HGVS-oriented XML records for downstream variant normalization or annotation pipelines.
disable-model-invocation: true
user-invocable: true
---

# snp2hgvs

Small bash wrapper over `xtract` and `transmute`. It reads dbSNP `DocumentSummarySet` XML, selects matching `DocumentSummary` records, and emits structured HGVS XML with one or more `<Variant>` blocks per rsID.

## Quick Start

- **Command:** `efetch -db snp -id <rsid> -format docsum | snp2hgvs`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/snp2hgvs`
- **Expected input:** dbSNP docsum XML from Entrez Direct

## When To Use This Tool

- Converting dbSNP docsum XML into HGVS-centered XML for one or more rsIDs
- Bridging from `efetch -db snp -format docsum` into later HGVS/SPDI conversion steps
- Extracting multiple genomic, coding, or protein HGVS representations from the same SNP record
- Feeding rsID-derived HGVS records into `hgvs2spdi`, `spdi2prod`, or custom XML processing

## Common Patterns

```bash
# Convert one rsID into HGVS XML
efetch -db snp -id 104894914 -format docsum | snp2hgvs
```

```bash
# Convert multiple dbSNP docsum records, then continue into SPDI
efetch -db snp -id 104894914,104894915 -format docsum | snp2hgvs | hgvs2spdi
```

```bash
# Full chain hinted by the wrapper source
efetch -db snp -id 104894914 -format docsum | snp2hgvs | hgvs2spdi | spdi2prod
```

## Recommended Workflow

1. Fetch SNP records from Entrez Direct in `-format docsum`, not an unrelated XML flavor.
2. Pipe the docsum XML directly into `snp2hgvs`.
3. Inspect the resulting `<HGVS>` document if you care about class/type distinctions across genomic, coding, or protein variants.
4. Chain into `hgvs2spdi` or other downstream normalizers only after confirming the wrapper emitted the variant forms you need.

## Guardrails

- There is no safe standalone help/version path: both `-h` and `--version` fell through to `xtract` and failed with `No data supplied to xtract from stdin or file`.
- The wrapper depends on both `xtract` and `transmute` being available on `PATH`.
- Source inspection shows it expects `DocumentSummarySet` / `DocumentSummary` XML with `SNP_ID`; it is not a generic rsID-to-HGVS web client.
- In live testing on rs104894914, the wrapper emitted `<HGVS>` XML containing multiple `<Variant>` records, including genomic (`NC_000023.11:g.154191716T>C`) and coding (`NM_000513.2:c.607T>C`) forms.
