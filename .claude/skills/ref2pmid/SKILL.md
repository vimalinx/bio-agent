---
name: ref2pmid
description: Use when converting reference citations or identifiers to PubMed IDs (PMIDs) using Entrez Direct utilities.
disable-model-invocation: true
user-invocable: true
---

# ref2pmid

Tiny EDirect wrapper around `transmute -r2p`. It maps citation-style XML or similar reference payloads to PMIDs, but it is only a stdin transformer and does not expose its own help text.

## Quick Start

- **Command:** `ref2pmid`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/ref2pmid`
- **Actual implementation:** a one-line shell wrapper calling `transmute -r2p "$@"`

## When To Use This Tool

- Converting bibliographic references to PubMed IDs
- Part of the Entrez Direct (EDirect) bioconda package for NCBI database queries
- Turning citation XML streams into PMID-enriched output for later EDirect steps

## Common Patterns

```bash
# 1) Convert a citation XML stream to PMIDs
cat citations.xml | ref2pmid
```

```bash
# 2) Source-comment example using explicit matching options
cat uniprot_citations.xml | ref2pmid -options remote,strict
```

```bash
# 3) Continue into downstream EDirect processing
cat citations.xml | ref2pmid | efetch -db pubmed -format xml
```

## Recommended Workflow

1. Start from a real citation-oriented XML stream rather than free-form text.
2. Pipe that stream into `ref2pmid`.
3. If you need stricter or remote matching behavior, pass options through to the underlying `transmute` layer.
4. Feed the resulting PMIDs into later EDirect commands or save them for audit.

## Guardrails

- `ref2pmid` has no standalone help/version implementation. In local tests, `-help` and `-version` both fell through to `transmute` and failed because no stdin was supplied.
- Because the wrapper is literally `transmute -r2p "$@"`, any extra flags are passed straight through to `transmute`.
- The tool expects input from stdin or a `transmute`-compatible file path; calling it empty is not a metadata-safe operation.
