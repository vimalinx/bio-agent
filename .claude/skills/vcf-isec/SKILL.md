---
name: vcf-isec
description: Use when you need to compute intersections, unions, or complements between bgzipped and tabix-indexed VCF or tab-delimited files.
disable-model-invocation: true
user-invocable: true
---

# vcf-isec

## Quick Start
- **Command:** `vcf-isec [OPTIONS] file1.vcf file2.vcf ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-isec`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Compute intersections, unions, complements, or Venn-style set outputs across multiple indexed VCFs.
- Compare concordance or exclusivity between callsets.
- Work on either VCFs or other tab-delimited region files when positions are indexable.
- Use it when set logic matters more than multi-sample merging.

## Common Patterns

```bash
# 1) Keep positions present in at least two files
vcf-isec \
  -n +2 \
  a.vcf.gz b.vcf.gz c.vcf.gz \
  > shared.vcf
```

```bash
# 2) Output positions unique to the first file
vcf-isec \
  -c \
  a.vcf.gz b.vcf.gz c.vcf.gz \
  > a_only.vcf
```

```bash
# 3) Create Venn-style output files
vcf-isec \
  -p isec_out \
  a.vcf.gz b.vcf.gz c.vcf.gz
```

## Recommended Workflow

1. Bgzip and index all inputs first.
2. Decide whether you want count-based set logic (`-n`), complement (`-c`), or multi-output decomposition (`-p`).
3. Add `-a` if you want to ignore non-PASS records during comparison.
4. Review outputs carefully because records from different files can intermix in surprising ways.

## Guardrails

- Inputs must be bgzipped and tabix-indexed unless you are using the tab-delimited mode explicitly with `-t`.
- `-f` forces past differing columns or VCF versions; only do that when you understand the compatibility risk.
- `-o` prints only entries from the left-most file even when set logic uses all files.
- Nearby indels may be normalized differently across callers, so `-w` can materially change what is considered shared.
