---
name: jsonl2xml
description: Use when converting JSON Lines streams into XML fragments for downstream EDirect or XML-based processing.
disable-model-invocation: true
user-invocable: true
---

# jsonl2xml

## Quick Start

- **Command:** `jsonl2xml < records.jsonl > records.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/jsonl2xml`
- **Full reference:** See [references/help.md](references/help.md) for detailed usage and options.

## When To Use This Tool

- Convert one-JSON-object-per-line streams into XML fragments.
- Bridge JSONL-producing tooling into XML-side steps without writing a custom line loop.
- Inspect or transform line-oriented JSON exports with XML-aware tools.

## Common Patterns

```bash
# 1) Convert a JSONL stream into XML fragments
jsonl2xml < records.jsonl > records.xml
```

```bash
# 2) Convert and inspect the first converted records immediately
jsonl2xml < records.jsonl | sed -n '1,40p'
```

## Recommended Workflow

1. Make sure each input line is a complete JSON document.
2. Feed the JSONL stream to `jsonl2xml` through stdin.
3. Inspect a few converted records before batching a large stream.
4. If you need a single enclosing XML document, add that wrapper yourself after conversion.

## Guardrails

- The wrapper is just a `while read` loop that runs `transmute -j2x` once per line, so `transmute` must be on `PATH`.
- Each JSONL record becomes its own `<root>...</root>` fragment. The output is not automatically wrapped into one combined XML document.
- The installed wrapper has no real `--help` / `--version` response.
- Prefer stdin input; the wrapper is stream-oriented rather than filename-oriented.
