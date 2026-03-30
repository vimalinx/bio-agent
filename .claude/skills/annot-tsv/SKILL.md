---
name: annot-tsv
description: Use when you need to annotate regions in a target TSV/BED file with information from overlapping regions in a source file, transfer columns between files based on genomic overlap, or filter/drop overlapping records.
disable-model-invocation: true
user-invocable: true
---

# annot-tsv

CLI tool from htslib (1.22.1) that annotates regions in a target file using overlapping regions from a source file. Supports column transfer, conditional matching, special annotations (count, fraction, base pairs), and grep-like filtering. Coordinates are 1-based and inclusive by default.

## Quick Start

- **Command**: `annot-tsv -s source.txt -t target.txt -c chr,beg,end -f info:INFO > output.txt`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/annot-tsv`
- **Full reference**: See `references/help.md` for complete options and examples

## When To Use This Tool

- Transferring annotation columns from a source file to overlapping regions in a target file
- Filtering records by overlap (print matching lines or drop overlapping regions with `-x`)
- Adding overlap statistics: count of overlapping regions (`cnt`), fraction overlapped (`frac`), or base pairs overlapped (`nbp`)
- Conditional annotation transfer requiring matching values in specified columns (`-m`)

## Common Patterns

```bash
# 1) Transfer INFO from overlapping source regions into the target table
annot-tsv \
  -s source.txt \
  -t target.txt \
  -c chr,beg,end \
  -f info:INFO \
  > output.txt
```

```bash
# 2) Require matching type/sample columns before annotation transfer
annot-tsv \
  -s src.txt.gz \
  -t tgt.txt.gz \
  -c chr,beg,end \
  -m type,sample \
  -f info
```

```bash
# 3) Use grep-like overlap filtering instead of column transfer
annot-tsv \
  -s source.txt \
  -t target.txt \
  -c chr,beg,end \
  -x
```

## Recommended Workflow

1. Identify the chromosome, start, and end column names/indices in both source and target files
2. Determine which columns to transfer (`-f`) and any required match conditions (`-m`)
3. Run a test annotation with a subset to verify column mapping and output format
4. Execute the full annotation, redirecting stdout to output file or using `-o`

## Guardrails

- Coordinates are 1-based and inclusive by default; use `-C` to specify different conventions (e.g., BED is 0-based start)
- Either source or target can be streamed from stdin, but not both simultaneously
- The `-x` (drop overlaps) option is incompatible with `-f` (column transfer)
- Use `--help`, not `-h`, for usage output. Here `-h` is the header-row option and requires an argument.
