---
name: xml2json
description: Use when converting XML documents into pretty-printed JSON for downstream parsing, provided the legacy Perl XML::Simple dependency is available.
disable-model-invocation: true
user-invocable: true
---

# xml2json

## Quick Start
- Command: `cat record.xml | xml2json > record.json`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/xml2json`
- Full reference: [references/help.md](references/help.md)

## When To Use This Tool

- Convert XML payloads into pretty-printed JSON for downstream scripting.
- Bridge XML-producing NCBI / EDirect commands into JSON-oriented tools.
- Inspect XML structure in a friendlier key/value form when the legacy converter dependency is available.

## Common Patterns

```bash
# 1) Convert an XML document from stdin into JSON
cat record.xml | xml2json > record.json
```

```bash
# 2) Stream XML into JSON and inspect the first lines
cat record.xml | xml2json | sed -n '1,40p'
```

## Recommended Workflow
1. Confirm the XML input is the actual payload you want to convert, not a filename string or shell fragment.
2. Pipe the XML into `xml2json`; the script reads stdin wholesale.
3. Validate that the Perl dependencies load before trying a batch conversion.
4. Inspect the first JSON objects before handing them to downstream code.

## Guardrails
- This script is a Perl program that reads only from stdin and depends on `XML::Simple` plus `JSON::PP`.
- In the current environment it cannot start because `XML::Simple.pm` is missing, and `--help` / `--version` fail with the same dependency error.
- Because it uses `XML::Simple`, the output structure can collapse repeated XML elements into arrays/hashes in ways that differ from hand-written JSON schemas.
- Treat this as a legacy converter and validate its JSON shape on representative XML before building automation around it.
