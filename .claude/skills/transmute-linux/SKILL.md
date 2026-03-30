---
name: transmute-linux
description: Use when calling the Linux-specific compiled `transmute.Linux` binary directly for NCBI format conversion, sequence processing, or variation-processing workflows.
disable-model-invocation: true
user-invocable: true
---

# transmute-linux

Linux platform binary for the `transmute` tool family. Unlike the public wrapper, this ELF executable goes straight into the compiled implementation and exposes the full built-in help/version text directly.

## Quick Start

- **Command:** `transmute.Linux [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/transmute.Linux`
- **Version seen locally:** `24.0`

## When To Use This Tool

- Calling the Linux backend directly instead of going through the `transmute` wrapper
- Working in environments where you specifically want the compiled binary and not wrapper-level intercepts
- Using the built-in help text as the authoritative reference for available compiled modes
- Debugging whether a behavior comes from the wrapper script or from the underlying executable itself

## Common Patterns

```bash
# Direct Linux-binary JSON to XML conversion
printf '{"a":1}\n' | transmute.Linux -j2x -set Set -rec Rec
```

```bash
# Show direct binary help
transmute.Linux -help
```

```bash
# Show direct binary version
transmute.Linux -version
```

## Recommended Workflow

1. Use `transmute.Linux -help` when you want the binary's own option inventory.
2. Call the platform binary directly only if you intentionally want to bypass wrapper-level helper logic.
3. Feed structured input through stdin for the selected mode.
4. If a mode seems to work in `transmute` but not here, check whether the wrapper was intercepting it in shell or Python.

## Guardrails

- `transmute.Linux -help` and `transmute.Linux -version` both work here and report version `24.0`.
- This binary does not provide the wrapper-only interception layer, so shell conveniences such as `-sort-by-length` belong conceptually to `transmute`, not necessarily to the native binary contract.
- The built-in help spans many categories, including pretty-printing, data conversion, text filtering, sequence editing, sequence processing, and variation processing.
- If you do not need direct binary behavior, prefer the public `transmute` wrapper for better portability and dependency handling.
