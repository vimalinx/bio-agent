---
name: download-sequence
description: Use when downloading NCBI ASN.1 biological sequence archive divisions such as BCT, PLN, or VRL into the current directory.
disable-model-invocation: true
user-invocable: true
---

# download-sequence

## Quick Start
- **Command:** `download-sequence division...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/download-sequence`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Mirror one or more NCBI biological sequence archive divisions into the current directory.
- Build a local batch archive of ASN.1 sequence files for offline processing.
- Use when you want division-wide dumps, not individual accession lookups.

## Common Patterns

```bash
# 1) Download bacterial and plant ASN.1 sequence batches
download-sequence BCT PLN
```

```bash
# 2) Download viral and mammalian divisions into the current working directory
download-sequence VRL MAM
```

## Recommended Workflow

1. Choose the archive division abbreviations you actually need.
2. Run the command from a dedicated download directory because files are written into the current working directory.
3. Re-run safely if needed; the script skips files that already exist.
4. Feed the downloaded ASN.1 archives into downstream EDirect or conversion utilities as needed.

## Guardrails

- Despite the name, this command does not fetch a single accession; it downloads division-wide `.aso.gz` archive batches.
- The local script lists files under NCBI's `ncbi-asn1` area and then downloads matching names, so network access is mandatory even for help-like exploration.
- Output lands in the current directory, so run it inside a clean target folder.
- Division filters are applied case-insensitively, but you still need valid archive abbreviations.
