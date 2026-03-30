---
name: ref-cache
description: Use when managing local reference sequence caches for htslib-based tools. Invokes the ref-cache CLI to configure or interact with reference cache directories.
disable-model-invocation: true
user-invocable: true
---

# ref-cache

`ref-cache` is an HTSlib reference-caching proxy for CRAM workflows. It serves MD5-addressed reference sequence requests from a local cache, optionally fetching missing sequences from an upstream refget-like service.

## Quick Start

- **Command:** `ref-cache [options] -d <cache_dir>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/ref-cache`
- **Local help path:** `ref-cache -h`

## When To Use This Tool

- Managing local caches of reference sequences in htslib-based workflows
- Configuring cache directories for reference data access
- Running a local CRAM reference proxy instead of repeatedly hitting a remote server
- Wiring `REF_PATH` to a local cache plus HTTP fallback

## Common Patterns

```bash
# 1) Start a background cache using the EBI upstream service
mkdir -p cached_refs logs
ref-cache -b -d cached_refs -l logs -p 8080 -u https://www.ebi.ac.uk/ena/cram/md5/
```

```bash
# 2) Local-only mode with no upstream fetches
ref-cache -d cached_refs -U -p 8080
```

```bash
# 3) Point HTSlib/SAMtools at the cache
export REF_PATH='/abs/path/cached_refs/%2s/%2s/%s:http:://myhost::8080/%s'
```

## Recommended Workflow

1. Create the cache and log directories first.
2. Decide whether the service should run in the foreground, as a daemon (`-b`), or under systemd socket activation (`-s`).
3. Choose whether to allow upstream fetches (`-u`) or serve only local files (`-U`).
4. After startup, wire the service into CRAM tooling via `REF_PATH`.

## Guardrails

- `-d <dir>` is mandatory.
- This tool uses short options only in local testing. `-h` shows help, while `--help` / `--version` were not validated as safe paths.
- The man page says `-b` and `-s` are mutually exclusive.
- According to the man page, `ref-cache` exits silently if it detects another instance already listening on the chosen port.
- `-U` disables upstream fetches entirely; without it, the default upstream is `https://www.ebi.ac.uk/ena/cram/md5/`.
