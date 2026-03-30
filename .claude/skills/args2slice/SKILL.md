---
name: args2slice
description: Use when inspecting shell argument tokenization by printing argv as a Go-style `[]string` literal.
disable-model-invocation: true
user-invocable: true
---

# args2slice

## Quick Start

- **Command:** `args2slice [arguments...]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/args2slice`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Debug quoting, escaping, and whitespace handling before embedding arguments into shell wrappers or generated commands.
- Show exactly how the current shell split argv.
- Produce a copy-pastable Go-style `[]string{...}` literal for debugging or documentation.

## Common Patterns

```bash
# 1) Check how quoted and unquoted arguments were tokenized
/home/vimalinx/miniforge3/envs/bio/bin/args2slice \
  alpha \
  'two words' \
  --flag
```

```text
[]string{
    "alpha",
    "two words",
    "--flag",
}
```

```bash
# 2) Verify a complex command line before wrapping it elsewhere
/home/vimalinx/miniforge3/envs/bio/bin/args2slice \
  -db nucleotide \
  -query 'gene name with spaces' \
  'field=a,b,c'
```

## Recommended Workflow

1. Reproduce the exact command-line shape you are trying to debug.
2. Compare the emitted slice against the argv you expected.
3. Fix shell quoting in the original command rather than post-processing the emitted slice.
4. Re-run until spaces, commas, flags, and embedded quotes survive exactly as intended.

## Guardrails

- This tool inspects only argv; it does not read stdin or open files for you.
- Output is diagnostic Go-like text, not a structured interchange format.
- No help or version mode is implemented.
- It reflects the shell's tokenization after parsing, so it cannot explain quoting mistakes that prevented the command from starting at all.
