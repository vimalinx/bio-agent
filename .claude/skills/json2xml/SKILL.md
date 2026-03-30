---
name: json2xml
description: Use when converting JSON documents into XML for downstream EDirect or XML-based processing.
disable-model-invocation: true
user-invocable: true
---

# json2xml

## Quick Start

- **Command**: `json2xml < data.json > data.xml`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/json2xml`
- **Reference**: See `references/help.md` for detailed usage and options.

## When To Use This Tool

- Convert structured JSON into XML so it can be inspected with `xtract` or merged into XML-side pipelines.
- Bridge JSON-speaking tooling into the XML-centric parts of an EDirect workflow.
- Normalize simple object trees before downstream XML extraction or archiving.

## Common Patterns

```bash
# 1) Convert a JSON document into XML
json2xml < data.json > data.xml
```

```bash
# 2) Convert and inspect the resulting XML immediately
json2xml < data.json | sed -n '1,40p'
```

## Recommended Workflow

1. Start with a representative JSON sample from the upstream source.
2. Feed it to `json2xml` through stdin redirection or a pipe.
3. Inspect the first emitted XML blocks before converting a full dataset.
4. Pass the XML to `xtract`, `xml2tbl`, or other downstream XML-side tools once the shape looks right.

## Guardrails

- This wrapper simply calls `transmute -j2x`, so the companion `transmute` binary must be on `PATH`.
- `--help` and `--version` are not real metadata switches here; in this build they are converted into literal XML tags like `<--help>`.
- Prefer stdin/pipes over positional filenames. In a smoke test, passing a filename argument caused the literal path string to be wrapped as XML content.
- The converter emits a `<root>` / `<opt>` style wrapper for a simple object, so check that downstream tools expect that structure.
