---
name: xtract-linux
description: Use when calling the Linux-specific compiled `xtract.Linux` binary directly to extract tabular or XML output from structured XML records.
disable-model-invocation: true
user-invocable: true
---

# xtract-linux

Linux platform binary for the EDirect `xtract` engine. It converts structured XML into tabular or generated XML output using record patterns, nested exploration scopes, conditional filters, and rich formatting controls.

## Quick Start

- **Command:** `xtract.Linux -pattern <record> -element <field>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/xtract.Linux`
- **Version seen locally:** `24.0`

## When To Use This Tool

- Extracting table rows directly from XML on Linux via the compiled `xtract` backend
- Debugging raw `xtract` behavior separately from the public wrapper
- Exploring XML structure before writing a larger Entrez Direct pipeline
- Using built-in compiled help as the canonical reference for `xtract` arguments

## Common Patterns

```bash
# Basic extraction from a tiny XML sample
printf '<Root><Rec><Val>A</Val></Rec><Rec><Val>B</Val></Rec></Root>\n' | \
  xtract.Linux -pattern Rec -element Val
```

```bash
# Show direct binary help
xtract.Linux -help
```

```bash
# Read XML from a file instead of stdin
xtract.Linux -input records.xml -pattern Rec -element Val
```

## Recommended Workflow

1. Start with `xtract.Linux -help` if you need the complete compiled argument taxonomy.
2. Identify the record boundary with `-pattern`.
3. Add `-group`, `-block`, `-subset`, or conditional operators only after the basic extraction works.
4. Prefer the public `xtract` wrapper if you need its front-end shortcuts into `transmute` or `rchive`.

## Guardrails

- `xtract.Linux -help` and `xtract.Linux -version` both work here and report version `24.0`.
- This is the compiled backend only; the public `xtract` wrapper intercepts some flags such as `-format`, `-outline`, `-j2x`, and `-e2index` before dispatch.
- In local testing, a minimal XML sample piped to `xtract.Linux -pattern Rec -element Val` emitted two lines: `A` and `B`.
- If you run it with no stdin and no `-input`, it expects XML input and will fail rather than acting like a metadata-only tool.
