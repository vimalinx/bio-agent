---
name: vcf-phased-join
description: Use when joining multiple overlapping pre-phased VCF chunks into a single phased VCF using heterozygous calls from overlaps to determine correct phase.
disable-model-invocation: true
user-invocable: true
---

# vcf-phased-join

## Quick Start
- **Command:** `vcf-phased-join -o merged.vcf chunk1.vcf chunk2.vcf ...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-phased-join`
- **Fallback launcher in this workspace:** `/home/vimalinx/miniforge3/envs/bio/bin/perl /home/vimalinx/miniforge3/envs/bio/bin/vcf-phased-join`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Merge overlapping pre-phased VCF chunks into one phased VCF.
- Use overlap heterozygous calls to decide whether phase blocks need swapping across chunk boundaries.
- Break blocks when `PQ` falls below a threshold with `-q`.
- Provide a file list with `-l` when the chunk set is large or generated programmatically.

## Common Patterns

```bash
# 1) Join three overlapping phased chunks
/home/vimalinx/miniforge3/envs/bio/bin/perl \
  /home/vimalinx/miniforge3/envs/bio/bin/vcf-phased-join \
  -o merged.vcf \
  chr1.part1.vcf chr1.part2.vcf chr1.part3.vcf
```

```bash
# 2) Join from a manifest file
/home/vimalinx/miniforge3/envs/bio/bin/perl \
  /home/vimalinx/miniforge3/envs/bio/bin/vcf-phased-join \
  -l chunks.txt \
  -o merged.vcf
```

```bash
# 3) Tighten the join criteria
/home/vimalinx/miniforge3/envs/bio/bin/perl \
  /home/vimalinx/miniforge3/envs/bio/bin/vcf-phased-join \
  -j 20 \
  -q 0.9 \
  -o merged.vcf \
  chr1.part1.vcf chr1.part2.vcf
```

## Recommended Workflow

1. Confirm that all chunks are position-sorted, overlapping, and represent the same samples in the same column set.
2. Start with the default `-j 10` and `-q 0.6` thresholds unless you have a benchmarked reason to tighten them.
3. Write to a real output file with `-o` so you also capture the sidecar phase log (`.plog`).
4. Inspect the merged VCF and `.plog`, then validate sample ordering and phase continuity before downstream use.

## Guardrails

- In this shell, direct invocation may fail with `Can't locate Vcf.pm`; activate the bio environment first or call the script through `/home/vimalinx/miniforge3/envs/bio/bin/perl`.
- The inputs must already be phased and overlapping; this tool does not infer phase from unphased calls.
- The script warns when column names differ across files; use `vcf-shuffle-cols` first if sample order is inconsistent.
- Output `-o merged.vcf` also creates `merged.plog` with phase-join diagnostics.
- There are hidden `--split-*` modes in the script source, but the stable documented interface is the join workflow above.
