---
name: filter-genbank
description: Use when filtering or processing GenBank-format sequence records retrieved via NCBI Entrez Direct tools
disable-model-invocation: true
user-invocable: true
---

# filter-genbank

## Quick Start

- **Command:** `filter-genbank < records.gbf > filtered.gbf`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/filter-genbank`
- **Reference:** See `references/help.md` for detailed usage information

## When To Use This Tool

- Apply EDirect's built-in GenBank flatfile filtering/normalization step to a GenBank stream.
- Clean or reshape GenBank-format records before a downstream transmutation or extraction stage.
- Keep GenBank filtering inside the EDirect toolchain instead of writing a custom parser.

## Common Patterns

```bash
# 1) Filter a saved GenBank flatfile stream
filter-genbank < records.gbf > filtered.gbf
```

```bash
# 2) Filter GenBank output directly from an Entrez pipeline
efetch -db nuccore -id ABC123.1 -format gbwithparts | filter-genbank
```

## Recommended Workflow

1. Start from real GenBank flatfile content, typically from `efetch`.
2. Pipe it through `filter-genbank` rather than relying on positional filenames.
3. Inspect the first filtered records before running a large batch.
4. Pass the result to the next EDirect or archival step once the output looks right.

## Guardrails

- This is a thin wrapper around `transmute -gbf`, so `transmute` must be on `PATH`.
- `--help` and `--version` are not implemented here; both are reported as unrecognized arguments.
- Prefer stdin or pipes over undocumented positional-file behavior.
- Because the actual filtering rules live inside `transmute`, validate on a representative GenBank sample before batching.
