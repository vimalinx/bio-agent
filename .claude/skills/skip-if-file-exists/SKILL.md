---
name: skip-if-file-exists
description: Use when filtering a newline-delimited list of file paths so only paths without an existing regular file continue downstream.
disable-model-invocation: true
user-invocable: true
---

# skip-if-file-exists

Tiny POSIX shell filter from EDirect. It reads file paths from stdin one line at a time and echoes only those paths for which `test -f` is false.

## Quick Start

- **Command:** `... | skip-if-file-exists`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/skip-if-file-exists`
- **Input contract:** newline-delimited file paths on stdin

## When To Use This Tool

- Skipping already materialized output files in shell pipelines
- Filtering a list of target paths before download, fetch, or conversion steps
- Building idempotent “only process missing outputs” loops around EDirect-style file lists
- Removing existing files from a queue without writing a custom `while read` shell block

## Common Patterns

```bash
# Keep only missing paths
printf '/tmp/a\n/etc/hosts\n/tmp/b\n' | skip-if-file-exists
```

```bash
# Generate only missing downloads
printf '%s\n' *.xml | skip-if-file-exists | xargs -r -n 1 download-step
```

```bash
# Use inside a while-read workflow
some_path_generator | skip-if-file-exists | while read -r path; do
  touch "$path"
done
```

## Recommended Workflow

1. Generate a newline-delimited stream of candidate file paths.
2. Pipe that stream through `skip-if-file-exists`.
3. Feed the surviving missing paths into `xargs`, `while read`, or another downstream executor.
4. Re-run the same pipeline safely; once files exist, they will be filtered out automatically.

## Guardrails

- This tool does not execute commands. It is only a stdin-to-stdout path filter.
- It has no real `-h`, `--help`, or `--version` interface; invoking it with flags and no stdin simply produces no output.
- The implementation uses `[ ! -f "$fl" ]`, so directories and other non-regular paths are treated as “missing” and will pass through.
- In local testing, `/etc/hosts` was correctly suppressed while nonexistent temp paths were echoed unchanged.
