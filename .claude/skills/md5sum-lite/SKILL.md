---
name: md5sum-lite
description: Use when computing plain MD5 digests for files or stdin in lightweight HTSlib-based workflows without GNU md5sum features.
disable-model-invocation: true
user-invocable: true
---

# md5sum-lite

md5sum-lite is a minimal MD5 calculator backed by HTSlib routines. It behaves like a stripped-down `md5sum`: hash files or stdin, print the digest, and leave comparison logic to the caller.

## Quick Start

- **Command:** `md5sum-lite [FILE]...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/md5sum-lite`
- **Confirmed stdin path:** `printf 'abc\n' | md5sum-lite`

## When To Use This Tool

- Compute a plain MD5 for one or more files.
- Hash a byte stream from stdin when you do not need a temp file.
- Use a small checksum helper in pipelines that already depend on HTSlib / samtools packaging.

## Common Patterns

```bash
# 1) Hash a file
md5sum-lite sample.txt
```

```bash
# 2) Hash stdin
printf 'abc\n' | md5sum-lite
```

```bash
# 3) Hash several files in one call
md5sum-lite a.txt b.txt
```

## Recommended Workflow

1. Hash the target file or pipe directly into stdin.
2. Capture the reported digest and compare it externally against your expected value or manifest.
3. Repeat over all targets if you need a multi-file checksum table.
4. Use standard shell filtering or your own verification logic because no check-mode workflow was confirmed locally.

## Guardrails

- `md5sum-lite -h` is not help; it is treated as a filename and errors as `md5sum: -h: No such file or directory`.
- Error messages are prefixed with `md5sum:` even though the executable name is `md5sum-lite`.
- The confirmed output is the simple two-field form `digest  target`; stdin is labeled as `-`.
- No real help, version, or GNU-style verification mode was evidenced from local tests or binary strings.
- An empty file hashes to the standard empty MD5 `d41d8cd98f00b204e9800998ecf8427e`.
