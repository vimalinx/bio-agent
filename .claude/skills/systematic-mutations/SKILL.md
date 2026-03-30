---
name: systematic-mutations
description: Use when enumerating all single-position A/C/G/T substitutions for sequence strings inside an EDirect-style text pipeline.
disable-model-invocation: true
user-invocable: true
---

# systematic-mutations

Tiny bash filter over `transmute -replace`. It reads `sequence [pattern]` records from stdin, uppercases the sequence, substitutes `A`, `C`, `G`, and `T` at every position, optionally appends the second whitespace-delimited field after a colon, then case-insensitively sorts and deduplicates the emitted variants.

## Quick Start

- **Command:** `echo ATGAAACCCGGGTTTTAG | systematic-mutations`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/systematic-mutations`
- **Required dependency:** `transmute` on `PATH`

## When To Use This Tool

- Generating every single-base substitution of a short sequence
- Expanding disambiguated sequence sets into explicit A/C/G/T mutation catalogs
- Keeping an attached pattern/label while mutating the leading sequence token
- Building small exhaustive mutation sets in a shell pipeline without writing custom code

## Common Patterns

```bash
# Enumerate all single-position substitutions
echo ATGAAACCCGGGTTTTAG | systematic-mutations
```

```bash
# Preserve a second-column pattern label
echo 'ATG tag1' | systematic-mutations
```

```bash
# Expand ambiguous input first, then enumerate mutations
echo RCCGGY | disambiguate-nucleotides | systematic-mutations
```

## Recommended Workflow

1. Feed one sequence per line on stdin, optionally followed by one extra whitespace-delimited label/pattern.
2. Normalize ambiguous bases upstream if you need explicit A/C/G/T inputs before mutation expansion.
3. Pipe the output directly into downstream text filters, because this tool does not create files by itself.
4. Deduplicate or rank the resulting variant strings downstream only if you need more than the built-in case-insensitive uniqueness pass.

## Guardrails

- This script ignores command-line flags. Local testing showed `systematic-mutations -h` is silent with no stdin and behaves exactly like the normal mutator when stdin is present.
- Input is read from stdin only; the first whitespace-delimited token is the sequence and the second token, if present, is preserved as `:<pattern>`. Additional columns are ignored.
- The original sequence can reappear in the output because the substitution loop also tries the existing base at each position before the final `sort -f | uniq -i`.
- The script depends on `transmute -replace`; if `transmute` is missing from `PATH`, mutation generation fails.
