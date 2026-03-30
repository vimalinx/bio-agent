---
name: yaml2xml
description: Use when converting YAML documents into XML for downstream EDirect or XML-based processing.
disable-model-invocation: true
user-invocable: true
---

# yaml2xml

## Quick Start

- **Command:** `yaml2xml < data.yaml > data.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/yaml2xml`
- **Full reference:** See `references/help.md` for detailed usage and options

## When To Use This Tool

- Convert YAML metadata or configuration into XML.
- Bridge YAML-speaking tooling into XML-side EDirect workflows.
- Normalize structured YAML before XML-based extraction or reporting.

## Common Patterns

```bash
# 1) Convert a YAML document into XML
yaml2xml < data.yaml > data.xml
```

```bash
# 2) Convert and inspect the emitted XML quickly
yaml2xml < data.yaml | sed -n '1,40p'
```

## Recommended Workflow

1. Validate the YAML syntax on a small representative input.
2. Run `yaml2xml` via stdin redirection or a pipe.
3. Inspect the emitted XML hierarchy before converting a larger batch.
4. Feed the XML into downstream `xtract` or reporting steps once the shape looks right.

## Guardrails

- This wrapper simply runs `transmute -y2x`, so `transmute` must be on `PATH`.
- The installed wrapper does not expose a meaningful `--help` / `--version` response.
- Prefer stdin/pipes over undocumented positional-file behavior.
- In practice the converter emits a `<ConfigFile>` root for simple mappings, so check downstream expectations if you need a different document root.
