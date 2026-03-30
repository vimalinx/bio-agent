---
name: between-two-genes
description: Use when extracting the inclusive tabular block between two gene-name rows from a first-column gene list or interval table.
disable-model-invocation: true
user-invocable: true
---

# between-two-genes

CLI tool from the bioconda package `entrez-direct` for working with genomic regions between two genes.

## Quick Start

- **Command:** `printf 'geneA\t1\ngeneB\t2\ngeneC\t3\ngeneD\t4\n' | /home/vimalinx/miniforge3/envs/bio/bin/between-two-genes geneB geneC`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/between-two-genes`
- **Full reference:** See [references/help.md](references/help.md) for complete options and usage

## When To Use This Tool

- Slice a tab-delimited stream down to the block spanning two gene-name markers in column 1.
- Keep the boundary rows themselves in the emitted block.
- Use as a fast text filter when you already have a gene-ordered table on stdin.

## Common Patterns

```bash
# 1) Print the inclusive block from geneB through geneC
printf 'geneA\t1\ngeneB\t2\ngeneC\t3\ngeneD\t4\n' | \
  /home/vimalinx/miniforge3/envs/bio/bin/between-two-genes geneB geneC
```

```text
geneB  2
geneC  3
```

```bash
# 2) Extract the block between two markers from a larger table
cat ordered_genes.tsv | \
  /home/vimalinx/miniforge3/envs/bio/bin/between-two-genes BRCA1 BRCA2
```

## Recommended Workflow

1. Ensure the first column contains the gene labels you want to use as boundaries.
2. Pass the two boundary patterns as positional arguments.
3. Inspect the emitted block to confirm the boundary order in the file matched your intent.
4. Only then feed the sliced block into downstream range or XML converters.

## Guardrails

- This is a local `awk` filter; it does not contact NCBI or perform identifier lookup.
- The two arguments are interpolated into awk regexes, not treated as escaped literal strings.
- Output begins at whichever boundary row appears first in the stream and stops after the second boundary row, so file order matters more than argument order.
- If only one boundary is encountered, the script prints from that row to EOF; there is no clean missing-boundary error.
