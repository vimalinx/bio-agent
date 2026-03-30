---
name: pmc2bioc
description: Use when converting PubMed Central article XML into BioC collection XML for downstream text-mining or annotation pipelines.
disable-model-invocation: true
user-invocable: true
---

# pmc2bioc

EDirect shell pipeline that converts PMC `<article>` XML into BioC-style `collection` / `document` / `passage` XML. It lifts front-matter metadata into the first passage, then emits abstract, title, and body passages for downstream text-mining workflows.

## Quick Start

- **Command:** `pmc2bioc`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/pmc2bioc`
- **Environment prerequisite:** add `/home/vimalinx/miniforge3/envs/bio/bin` to `PATH` so `xtract`, `transmute`, and related EDirect helpers are available

## When To Use This Tool

- Convert PMC full-text XML into BioC collection XML.
- Feed PMC articles into BioC-oriented NLP, annotation, or corpus-building pipelines.
- Preserve article metadata, title, abstract, and body passages in a text-mining-friendly structure.
- Use this on PMC article XML, not on PubMed citation XML or summary XML.

## Common Patterns

```bash
# 1) Convert a live PMC article fetch into BioC XML
export PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH

efetch -db pmc -id 6260607 -format xml | pmc2bioc > article.bioc.xml
```

```bash
# 2) Convert XML streamed from a PMC OA tarball
export PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH

tar -xOzf oa_bundle.tar.gz --to-stdout | pmc2bioc > batch.bioc.xml
```

```bash
# 3) Inspect the first BioC passages before batch processing
export PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH

efetch -db pmc -id 6260607 -format xml | pmc2bioc | sed -n '1,40p'
```

## Recommended Workflow

1. Fetch or extract PMC article XML first, because this wrapper does not retrieve articles on its own.
2. Activate the bio environment or export the EDirect bin directory into `PATH` so sibling utilities resolve.
3. Convert one representative article and inspect the first `passage` blocks to confirm the BioC shape your downstream tool expects.
4. Only then batch-convert larger PMC corpora or OA archive payloads.

## Guardrails

- The source itself labels this converter as `WORK IN PROGRESS`, so treat the emitted BioC schema as practical but not deeply stabilized.
- There is no true help path. With dependencies available, `pmc2bioc -help` still runs the conversion pipeline and only errors because no XML input was supplied.
- Without the bio bin directory on `PATH`, the live failure is `xtract: command not found` plus `transmute: command not found`.
- With dependencies available but no XML input, the live failure is `No data supplied to xtract from stdin or file`.
- This script expects PMC `<article>` XML and emits BioC XML; it is not a generic PMC metadata lister or PubMed citation converter.
