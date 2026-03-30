---
name: run-with-lock
description: Use when wrapping a command in NCBI-style file locking so only one worker for a given lock base runs at a time.
disable-model-invocation: true
user-invocable: true
---

# run-with-lock

Compiled NCBI helper for serializing a command behind a named lock. Binary strings and official NCBI source both confirm option names such as `-base`, `-getter`, `-log`, `-map`, and `-reviewer`, but this local installation is incomplete because the default `get_lock` helper is missing from `PATH`.

## Quick Start

- **Command:** `run_with_lock -base <lock-name> command [args...]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/run_with_lock`
- **Observed dependency:** external `get_lock` helper

## When To Use This Tool

- Preventing two jobs with the same logical lock name from running concurrently
- Serializing fragile build, indexing, or cache-population steps
- Capturing a log file for a locked command run
- Reusing NCBI build-system locking conventions in custom workflows

## Common Patterns

```bash
# Run one command behind a named lock
run_with_lock -base make_taxdb make taxdb
```

```bash
# Keep a lock-scoped log file
run_with_lock -base make_taxdb -log make_taxdb.log make taxdb
```

```bash
# Ignore the wrapped command's exit status after the lock is acquired
run_with_lock -base make_taxdb ! make taxdb
```

## Recommended Workflow

1. Choose a stable lock base for the shared resource you are protecting.
2. Wrap the real command after any `run_with_lock` options.
3. Add `-log` when you want captured output, and only use `!` when failure of the wrapped command should not propagate.
4. Verify that the supporting lock helper programs are actually installed before depending on this in production.

## Guardrails

- `--help` and `--version` are not implemented as help/version paths here; local testing returned `Unsupported option --help` and `Unsupported option --version`.
- Bare invocation failed immediately with `run_with_lock: Unable to exec get_lock: No such file or directory.`, so this environment is missing the default lock-getter helper.
- Binary strings plus official NCBI source confirm these parsed options: `-base`, `-getter`, `-log`, `-map`, `-reviewer`, plus a standalone `!` marker that suppresses nonzero exit propagation from the wrapped command.
- If `-base` is omitted, the source derives it from the basename of the wrapped command and then forms `<base>.lock`.
- The source only applies `-map` remapping when the lock base begins with `make_`.
