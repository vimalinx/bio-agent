---
name: hmmconvert
description: Use when converting profile HMM files between HMMER3 ASCII or binary, legacy HMMER2, or specific 3.x text revisions.
disable-model-invocation: true
user-invocable: true
---

# hmmconvert

## Quick Start

- **Command:** `hmmconvert [-options] <hmmfile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hmmconvert`
- **Full reference:** See `references/help.md` for `--help` failure behavior and `hmmconvert -h` output

## When To Use This Tool

- Use `hmmconvert` when downstream tools or archival constraints require a different HMMER profile-file format than the one you currently have.
- It is useful for converting between current HMMER3 ASCII, HMMER3 binary, legacy HMMER2 ASCII, or older named HMMER3 text revisions such as `3/a` through `3/f`.
- Reach for it when comparing historical model files, shrinking storage with binary output, or preparing data for older compatibility experiments.

## Common Patterns

```bash
# Rewrite a profile file in the current HMMER3 ASCII format
hmmconvert profiles.hmm > profiles.3f.hmm
```

```bash
# Convert to HMMER3 binary format
hmmconvert -b profiles.hmm > profiles.h3m
```

```bash
# Convert to legacy HMMER2-style ASCII for comparison work
hmmconvert -2 profiles.hmm > profiles.hmmer2
```

```bash
# Read from stdin and pin an older HMMER3 text revision explicitly
cat profiles.hmm | hmmconvert --outfmt 3/b - > profiles.3b.hmm
```

## Recommended Workflow

1. Decide what exact target format the next consumer needs before converting anything.
2. Preserve the original profile file so you can diff or fall back after conversion.
3. Run `hmmconvert` and redirect stdout to an explicitly named output file.
4. Validate the converted file with `hmmstat`, `hmmfetch`, or the downstream HMMER tool you actually care about.

## Guardrails

- `-h` works; `--help` and `--version` are rejected by the local executable.
- Output goes to stdout, so forgetting redirection will dump the converted profile into the terminal session.
- Input `hmmfile` may be `-` to read from stdin.
- `-2` produces an approximate backward-compatible HMMER2 ASCII form, not a perfect round-trip of every HMMER3 feature.
- `--outfmt` applies only to named HMMER3 ASCII revisions, not binary or HMMER2 output.
