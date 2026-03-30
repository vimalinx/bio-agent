---
name: download-pubmed
description: Use when you need to bulk-download PubMed baseline or update files from NCBI's FTP server for local offline analysis.
disable-model-invocation: true
user-invocable: true
---

# download-pubmed

## Quick Start
- **Command:** `download-pubmed [-ftp|-https] [section...]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/download-pubmed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Mirror PubMed XML baselines and daily update files into local storage.
- Seed a local PubMed archive before running `archive-pubmed`, `fetch-pubmed`, or custom text-mining pipelines.
- Refresh a PubMed mirror incrementally by targeting `updatefiles` after an initial baseline sync.

## Common Patterns

```bash
# 1) Download the default PubMed mirror set: baseline + updatefiles
download-pubmed
```

```bash
# 2) Use HTTPS explicitly
download-pubmed -https
```

```bash
# 3) Download only one section
download-pubmed baseline
download-pubmed updatefiles
```

## Recommended Workflow

1. Run this from a clean target directory because all downloaded `.xml.gz` files land in the current working directory.
2. Use the no-argument form once to fetch both `baseline` and `updatefiles`, or target sections explicitly when refreshing an existing mirror.
3. Let the wrapper finish its retry and validation cycle before deciding a file is broken.
4. Feed the validated archive into local indexing or parsing workflows instead of repeatedly querying PubMed live.

## Guardrails

- With no arguments, this command downloads both `baseline` and `updatefiles`, which is large.
- The local wrapper validates XML payloads and deletes bad downloads before retrying, so interrupted runs can leave partial work that must be retried.
- Output is written into the current directory; keep PubMed mirrors isolated from unrelated files.
- This script does not expose a normal `--help` mode in practice, so rely on the captured reference rather than probing it with arbitrary flags.
