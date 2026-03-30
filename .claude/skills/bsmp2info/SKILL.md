---
name: bsmp2info
description: Use when converting BioSample `DocumentSummary` XML into a compact `BioSampleInfo` XML summary with accession, title, links, and harmonized attributes.
disable-model-invocation: true
user-invocable: true
---

# bsmp2info

## Quick Start

- **Command:** `... | bsmp2info`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/bsmp2info`
- **Output:** formatted `BioSampleInfo` XML

## When To Use This Tool

- Extract a compact XML summary from BioSample docsum records.
- Preserve accession, title, link IDs, and harmonized BioSample attributes in a simpler structure.
- Normalize attribute tag names to lowercase before downstream parsing.
- Keep BioSample extraction inside an EDirect XML pipeline.

## Common Patterns

```bash
# 1) Convert a local BioSample DocumentSummary XML snippet
cat biosample_docsum.xml | bsmp2info
```

```bash
# 2) End-to-end after obtaining BioSample docsum XML
esearch -db biosample -query 'SAMN38051082[ACCN]' |
efetch -format docsum |
bsmp2info
```

```bash
# 3) Pull selected fields from the simplified XML
... | bsmp2info | xtract -pattern BioSampleInfo -element Accession,organism,tissue
```

## Recommended Workflow

1. Start from BioSample `DocumentSummary` XML, whether from a local file or an EDirect fetch.
2. Pipe that XML into `bsmp2info` to collapse it to the key fields you actually need.
3. Inspect the emitted XML and confirm that expected harmonized attributes are present.
4. Continue with `xtract` or another XML-aware consumer instead of reparsing the original larger docsum structure.

## Guardrails

- The wrapper expects BioSample `DocumentSummary` XML on stdin; it does not accept a bare accession or identifier list.
- Only attributes carrying `harmonized_name` are emitted, and their tag names are lowercased.
- Multiple `Links/Link` values are collapsed into one pipe-delimited `Link` element such as `123|456`.
- There is no real help or version interface.
- Live BioSample EDirect requests may hit NCBI rate limits, so local fixture-based validation can be more reliable than repeated network probing.
