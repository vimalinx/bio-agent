---
name: datatool
description: Use when working with NCBI ASN.1 module files, schema exports, or ASN.1/XML conversion tasks that require the `datatool` command.
disable-model-invocation: true
user-invocable: true
---

# datatool

## Quick Start

- **Command:** `datatool -m module.asn [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/datatool`
- **Version observed locally:** `2.24.0` (`blast 2.17.0` package build)
- **Detailed help:** `datatool -help`

## When To Use This Tool

- Work with NCBI ASN.1 module definitions and related XML / JSON schema exports.
- Validate or dry-run complex ASN.1 conversion jobs before executing them.
- Generate DTD, XMLSchema, JSONSchema, definition, or export-spec artifacts from module files.
- Stay within the NCBI `datatool` ecosystem instead of hand-rolling format metadata.

## Common Patterns

```bash
# 1) Show the detailed argument reference
datatool -help
```

```bash
# 2) Validate a planned run against a module file without executing it fully
datatool -m module.asn -dryrun
```

```bash
# 3) Ask for XML-oriented help text
datatool -xmlhelp
```

## Recommended Workflow

1. Start with `-help` or `-xmlhelp` because the option surface is large.
2. Identify the relevant ASN.1 module file and pass it with `-m`.
3. Use `-dryrun` before any real export or transformation step.
4. Add only the specific output-generation flags you actually need once the dry run looks correct.

## Guardrails

- Real work requires `-m moduleFile`; help and version flags are the exception.
- `datatool` uses NCBI-style single-dash long options such as `-help`, `-version`, `-version-full-xml`, not GNU `--help`.
- The CLI surface is broad enough that blindly copying flags is error-prone; verify intended modes with `-help` first.
- `-dryrun` is the safest way to check a complex invocation before generating files.
- This binary comes from the BLAST package build rather than a standalone `datatool` package, so version strings include both the tool and BLAST package context.
