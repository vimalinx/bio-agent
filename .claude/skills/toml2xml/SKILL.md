---
name: toml2xml
description: Use when converting TOML configuration or metadata files into XML for downstream EDirect or XML-based processing.
disable-model-invocation: true
user-invocable: true
---

# toml2xml

## Quick Start

- **Command:** `toml2xml < config.toml > config.xml`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/toml2xml`
- **Full reference:** See `references/help.md` for detailed usage

## When To Use This Tool

- Convert TOML configuration or metadata into XML.
- Bridge TOML-speaking tooling into XML-oriented EDirect workflows.
- Normalize simple structured config data before XML-side extraction or archiving.

## Common Patterns

```bash
# 1) Convert a TOML file into XML
toml2xml < config.toml > config.xml
```

```bash
# 2) Convert and inspect the emitted XML quickly
toml2xml < config.toml | sed -n '1,40p'
```

## Recommended Workflow

1. Validate the TOML syntax on a small representative file.
2. Run `toml2xml` through stdin redirection or a pipe.
3. Confirm the emitted XML matches the expected config hierarchy.
4. Pass the XML to downstream inspection or reporting tools after that quick check.

## Guardrails

- This wrapper simply runs `transmute -m2x`, so `transmute` must be on `PATH`.
- The installed wrapper does not expose a real `--help` / `--version` surface.
- Prefer stdin or pipes over undocumented positional-file behavior.
- In practice the converter emits a `<ConfigFile>` root, so confirm that downstream tools expect that top-level tag.
