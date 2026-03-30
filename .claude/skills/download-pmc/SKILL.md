---
name: download-pmc
description: Use when bulk-downloading PubMed Central OA tarballs across the standard PMC sections with the EDirect helper script.
disable-model-invocation: true
user-invocable: true
---

# download-pmc

## Quick Start

- **Command**: `PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/download-pmc [-ftp|-https]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/download-pmc`
- **Full reference**: See [references/help.md](references/help.md)

## When To Use This Tool

- Mirror the PMC OA bulk XML archives in batch.
- Pull baseline and incremental tarballs from `oa_comm`, `oa_noncomm`, and `oa_other`.
- Retry failed downloads and verify tarball contents before keeping them.

## Common Patterns

```bash
# 1) Use the default FTP-backed download mode
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/download-pmc
```

```bash
# 2) Force HTTPS retrieval instead of FTP-style listing
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/download-pmc -https
```

## Recommended Workflow

1. Run it from a directory where bulk PMC tarballs are supposed to accumulate.
2. Pick `-ftp` or `-https` deliberately; FTP-style mode is the default.
3. Let the script finish its full pass over `baseline` and `incr` tarballs in all three OA sections.
4. Review stderr for retries or invalid-content deletions before treating the mirror as complete.

## Guardrails

- This is a bulk operational downloader, not a one-file fetcher and not a safe probe.
- The script iterates all of `oa_comm`, `oa_noncomm`, and `oa_other` for both `baseline` and `incr`; there is no fine-grained selector for one archive family.
- It depends on `nquire`, `xtract`, and `skip-if-file-exists` being available on `PATH`.
- Files that download empty or fail XML verification are deleted and retried; a missing file after the run can reflect repeated validation failure, not just an interrupted transfer.
