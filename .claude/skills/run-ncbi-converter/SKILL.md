---
name: run-ncbi-converter
description: Use when launching an NCBI converter binary through the `run-ncbi-converter` wrapper that downloads and caches the platform-specific executable on demand.
disable-model-invocation: true
user-invocable: true
---

# run-ncbi-converter

Perl bootstrap wrapper from Entrez Direct. It does not perform the conversion itself; instead it infers the current platform, downloads a named converter binary from NCBI FTP into a cache directory, unpacks it, and then `exec`s that converter with the remaining arguments.

## Quick Start

- **Command:** `run-ncbi-converter <converter-name> [converter-args...]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/run-ncbi-converter`
- **Default cache directory:** `~/.cache/ncbi-converters`

## When To Use This Tool

- Bootstrapping one of the NCBI converter binaries without manually downloading it first
- Reusing cached platform-specific converter executables across repeated runs
- Redirecting converter downloads into a controlled cache directory via `NCBI_CONVERTER_DIR`
- Debugging why an Entrez Direct converter wrapper is failing before the actual converter starts

## Common Patterns

```bash
# Run a named converter through the bootstrap wrapper
run-ncbi-converter <converter-name> [converter-args...]
```

```bash
# Keep downloaded converters in a project-local cache
export NCBI_CONVERTER_DIR="$PWD/.ncbi-converters"
run-ncbi-converter <converter-name> [converter-args...]
```

```bash
# Inspect or clean the cache between runs
ls ~/.cache/ncbi-converters
```

## Recommended Workflow

1. Decide which converter binary you actually need; the first positional argument becomes the remote archive basename.
2. Optionally point `NCBI_CONVERTER_DIR` at a writable cache location.
3. Run the wrapper only when FTP access to `ftp.ncbi.nlm.nih.gov` is available.
4. If the bootstrap succeeds, treat everything after the first argument as arguments for the downloaded converter, not for the wrapper itself.

## Guardrails

- There is no local `--help` or `--version` path: passing `-h` or `--version` is interpreted as a converter name and immediately triggers FTP access.
- In this workspace, invoking the wrapper failed before any conversion with `Unable to connect to FTP server: Bad file descriptor`.
- The source hardcodes `ftp.ncbi.nlm.nih.gov` and a per-platform directory under `/toolbox/ncbi_tools/converters/by_platform/`.
- On Unix-like systems the wrapper downloads `<converter>.<platform>.gz`, runs `gunzip -n`, renames the unpacked file to the bare converter name, marks it executable, and then `exec`s it.
- If you do not provide a first positional argument, the wrapper still constructs an archive name from `$ARGV[0]`, so empty or malformed invocations are not gracefully handled.
