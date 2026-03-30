---
name: find-in-gene
description: Use when filtering EDirect `GENE` XML records by strand and coordinate overlap to emit matching gene names.
disable-model-invocation: true
user-invocable: true
---

# find-in-gene

CLI tool from the bioconda package `entrez-direct` for filtering `GENE` XML on strand and interval overlap.

## Quick Start

- **Command:** `cat genes.xml | PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH /home/vimalinx/miniforge3/envs/bio/bin/find-in-gene plus 1200 1800`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/find-in-gene`
- **Reference:** See `references/help.md` for full usage details

## When To Use This Tool

- Select gene names whose `Min` / `Max` span overlaps a query interval in `GENE` XML.
- Restrict matches to a specific strand value such as `plus` or `minus`.
- Use as a tiny `xtract` wrapper in larger EDirect XML pipelines.

## Common Patterns

```bash
# 1) Find plus-strand genes overlapping a region
cat genes.xml | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/find-in-gene plus 1200 1800
```

```bash
# 2) Query minus-strand overlaps from an EDirect pipeline
upstream_gene_xml_command | \
  PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
  /home/vimalinx/miniforge3/envs/bio/bin/find-in-gene minus 50000 52000
```

## Recommended Workflow

1. Start from XML records that actually use the `GENE` pattern with `Name`, `Strand`, `Min`, and `Max` elements.
2. Pass strand first, then the lower and upper coordinate bounds.
3. Capture stdout as a simple list of matching gene names.
4. If the interval bounds are reversed, let the script swap them, but still verify the query window before automating it.

## Guardrails

- Despite the error text mentioning only start and stop positions, the script practically needs three arguments: `strand min max`. Supplying only two causes `xtract` to fail with empty numeric constraints.
- A fourth argument is accepted by the shell wrapper but is not used anywhere in the filter.
- This wrapper is stdin-driven and emits only `Name`; it does not fetch gene records on its own.
- Like other EDirect helpers, it requires companion binaries such as `xtract` to be on `PATH`; absolute-path invocation alone is not sufficient in a bare shell.
