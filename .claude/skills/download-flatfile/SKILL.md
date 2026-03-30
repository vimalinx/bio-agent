---
name: download-flatfile
description: Use when mirroring consolidated NCBI GenBank flatfile divisions into the current directory or verifying existing downloaded flatfiles.
disable-model-invocation: true
user-invocable: true
---

# download-flatfile

## Quick Start
- **Command:** `download-flatfile [-ftp|-https] [-verify] division...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/download-flatfile`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Download one or more GenBank flatfile divisions as `.seq.gz` archives.
- Re-check previously downloaded GenBank flatfiles and remove corrupt or empty files with `-verify`.
- Build a local flatfile mirror for downstream XML conversion or archive indexing.

## Common Patterns

```bash
# 1) Download bacterial and viral GenBank flatfiles via the default FTP mode
download-flatfile BCT VRL
```

```bash
# 2) Use HTTPS explicitly if FTP routing is unreliable
download-flatfile -https PLN INV
```

```bash
# 3) Validate existing flatfiles and delete broken or empty downloads
download-flatfile -verify BCT VRL
```

## Recommended Workflow

1. Start in a dedicated download directory because all `.seq.gz` files are written to the current working directory.
2. Download the divisions you need, choosing `-https` if FTP is flaky in your environment.
3. Re-run with `-verify` before downstream processing when download integrity matters.
4. Convert or inspect the flatfiles only after the validation pass is clean.

## Guardrails

- `-verify` is destructive by design: it removes empty or invalid `.seq.gz` files so they can be re-downloaded.
- The local wrapper validates content by decompressing and checking parsed records, so verification can be expensive on large downloads.
- Output is written into the current directory, and large GenBank divisions consume substantial disk space.
- The wrapper retries failed downloads, but persistent network or content failures still leave you with deleted files that must be fetched again later.
