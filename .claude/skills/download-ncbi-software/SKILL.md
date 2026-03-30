---
name: download-ncbi-software
description: Use when fetching a small set of NCBI command-line binaries (`magic-blast`, `datasets`, or `sra-toolkit`) with the bundled EDirect downloader.
disable-model-invocation: true
user-invocable: true
---

# download-ncbi-software

## Quick Start

- **Command:** `download-ncbi-software [ magic-blast | datasets | sra-toolkit ]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/download-ncbi-software`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Download `magic-blast`, `datasets` / `dataformat`, or `sra-toolkit` directly from NCBI-hosted distribution locations.
- Grab platform-specific binaries without manually browsing the FTP / HTTPS directories.
- Bootstrap a local tool directory in shell-heavy EDirect workflows.

## Common Patterns

```bash
# 1) Download magic-blast for the current platform
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/download-ncbi-software magic-blast
```

```bash
# 2) Download the current datasets + dataformat pair
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/download-ncbi-software datasets
```

```bash
# 3) Show the tiny built-in usage banner
/home/vimalinx/miniforge3/envs/bio/bin/download-ncbi-software --help
```

## Recommended Workflow

1. Decide whether you need `magic-blast`, `datasets`, or `sra-toolkit`.
2. Run the downloader from the directory where you want the files to land.
3. Verify that the expected executable or unpacked directory actually appeared.
4. Add execute permissions or move the downloaded binaries into your normal tool path if needed.

## Guardrails

- This script only knows three package families: `magic-blast`, `datasets` / `dataformat`, and `sra-toolkit`.
- It depends on the EDirect helper `nquire`; keep the bio / EDirect bin directory on `PATH`.
- Platform support is uneven. In the current Linux x86_64 source logic, `magic-blast` and `datasets` are handled, but `sra-toolkit` falls through with an empty suffix and effectively does nothing while still exiting successfully.
- The downloads unpack into the current working directory; this is an operational script, not a dry-run metadata query.
