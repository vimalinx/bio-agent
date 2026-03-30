---
name: transmute
description: Use when invoking the public `transmute` wrapper for format conversion, sequence editing, or shell-level helper modes that may be intercepted before dispatch to the platform binary.
disable-model-invocation: true
user-invocable: true
---

# transmute

Public wrapper script for the NCBI `transmute` toolkit. Some modes are handled directly in shell, Perl, Python, or `xmllint` helpers, while the remaining arguments are passed through to the compiled platform-specific executable such as `transmute.Linux`.

## Quick Start

- **Command:** `transmute [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/transmute`
- **Platform backend here:** `transmute.Linux`

## When To Use This Tool

- Using the preferred public `transmute` entry point instead of calling the platform binary directly
- Running format-conversion or sequence-processing modes described in `transmute -help`
- Accessing shell-intercepted convenience modes such as `-j2p`, `-x2p`, `-sort-by-length`, or XML encode/decode helpers
- Building pipelines that should stay portable across platforms because the wrapper selects the correct compiled backend

## Common Patterns

```bash
# Convert JSON to XML through the public wrapper
printf '{"a":1}\n' | transmute -j2x -set Set -rec Rec
```

```bash
# Pretty-print JSON using the wrapper's python helper path
printf '{"a":1}\n' | transmute -j2p
```

```bash
# Wrapper-level line-length sort helper
printf 'bbb\na\ncc\n' | transmute -sort-by-length
```

## Recommended Workflow

1. Start with `transmute -help` to choose the right mode.
2. Prefer the wrapper over `transmute.Linux` when you want portability or wrapper-only helper modes.
3. Feed data through stdin unless the selected mode explicitly documents file-based arguments.
4. If a mode behaves oddly, check whether it is one of the shell-intercepted paths before blaming the compiled backend.

## Guardrails

- `transmute -help` and `transmute -version` both work here and report version `24.0`.
- The wrapper intercepts several modes itself, including `-encodeXML`, `-decodeXML`, `-plainXML`, `-x2p`, `-j2p`, `-x2j`, `-word-pairs`, `-sort-by-length`, and multiple newline-conversion helpers.
- Some intercepted modes have extra runtime dependencies: for example `-x2p` needs `xmllint`, `-j2p` needs `python3`, and several helpers require `perl`.
- In local testing, `printf '{"a":1}\n' | transmute -j2x -set Set -rec Rec` produced a wrapped XML document with `<Set><Rec><a>1</a></Rec></Set>`.
- If the compiled backend is missing, the wrapper prints explicit download instructions for `transmute.<platform>.gz` rather than failing silently.
