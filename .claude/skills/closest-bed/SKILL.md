---
name: closest-bed
description: Use when you need to find the closest genomic feature in one file for each feature in another file, including distance calculations and strand-aware lookups.
disable-model-invocation: true
user-invocable: true
---

# closest-bed

## Quick Start
- **Command:** `closestBed -a <A> -b <B> [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/closestBed`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Find the nearest genomic feature in B for every feature in A.
- Report unsigned distance with `-d` or signed upstream/downstream distance with `-D`.
- Ignore overlaps and search only for nearby non-touching features with `-io`.
- Limit to same-strand or opposite-strand neighbors with `-s` / `-S`.
- Resolve ties or return multiple nearest hits with `-t`, `-k`, and `-mdb`.

## Common Patterns

```bash
# 1) Find the nearest gene for each peak with distance
closestBed \
  -a peaks.bed \
  -b genes.bed \
  -d
```

```bash
# 2) Report upstream/downstream signed distance relative to A strand
closestBed \
  -a peaks.bed \
  -b genes.bed \
  -D a \
  -io
```

```bash
# 3) Keep the two closest same-strand hits and break ties by file order
closestBed \
  -a exons.bed \
  -b transcripts.bed \
  -s \
  -k 2 \
  -t first
```

## Recommended Workflow

1. Decide whether overlapping features should count as closest; if not, add `-io`.
2. Choose `-d` for absolute distance or `-D ref|a|b` if signed orientation matters biologically.
3. Apply `-s` / `-S`, `-iu` / `-id`, or `-fu` / `-fd` only after you are sure the strand and orientation model is the one you want.
4. Inspect cases with `none` / `-1` output because they mean no candidate in B exists on the same chromosome.

## Guardrails

- `-iu`, `-id`, `-fu`, and `-fd` require `-D` and inherit its upstream/downstream orientation rules.
- Ties are reported by default; if you need one record only, set `-t first` or `-t last`.
- With multiple B files, `-mdb each` and `-mdb all` produce meaningfully different semantics.
- Chromosome naming mismatches can make valid neighbors disappear silently into `none` / `-1` results.
- Prefer `-h` for help; some `--help` / `--version` invocations on these wrappers produce extra errors.
