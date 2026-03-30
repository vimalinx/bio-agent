---
name: rchive-linux
description: Use when calling the Linux-specific compiled `rchive.Linux` binary directly to build, query, or manage local XML archives and postings indices.
disable-model-invocation: true
user-invocable: true
---

# rchive-linux

Linux platform binary for EDirect local archiving and postings management. It can archive XML records, build inverted indices, promote postings, and run word/phrase queries against a prepared local postings directory.

## Quick Start

- **Command:** `rchive.Linux [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/rchive.Linux`
- **Version seen locally:** `24.0`

## When To Use This Tool

- Running the compiled Linux backend for local EDirect archive/index operations
- Building Entrez-style archive and postings infrastructure from XML input
- Querying an already prepared postings directory with `-query`, `-count`, or `-counts`
- Debugging raw `rchive` backend behavior separately from the wrapper script

## Common Patterns

```bash
# Show direct binary help
rchive.Linux -help
```

```bash
# Build Entrez index XML from XML input
cat records.xml | rchive.Linux -strict -e2index
```

```bash
# Query an existing postings directory
rchive.Linux -path /path/to/Postings -query 'dna repair'
```

## Recommended Workflow

1. Use `rchive.Linux -help` to choose the right archive/index stage.
2. Separate build-stage operations (`-e2index`, `-e2invert`, `-merge`, `-promote`) from query-stage operations (`-query`, `-count`, `-counts`).
3. Only run query/count modes after a valid postings directory has been prepared and supplied.
4. Prefer the public `rchive` wrapper if you want the platform-dispatch layer instead of direct Linux binding.

## Guardrails

- `rchive.Linux -help` and `rchive.Linux -version` both work here and report version `24.0`.
- Query-like modes are not self-contained. In local testing, `rchive.Linux -count dna` against ad hoc stdin failed with `Unable to get folder Postings for database pubmed`.
- The built-in help shows `-archive`/`-fetch`/`-stream` for local record caches and `-e2index`/`-e2invert`/`-join`/`-fuse`/`-merge`/`-promote` for postings construction.
- Do not treat this as a generic XML transformer; it expects either archive/index workflows or an already prepared postings environment.
