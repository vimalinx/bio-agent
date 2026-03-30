---
name: pair-to-pair
description: Use when comparing two paired-end BEDPE files to find overlapping pairs. Requires -a and -b BEDPE input files.
disable-model-invocation: true
user-invocable: true
---

# pair-to-pair

## Quick Start
- **Command:** `pairToPair -a A.bedpe -b B.bedpe [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/pairToPair`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Compare one BEDPE pair set against another BEDPE pair set.
- Require overlap on both ends, either end, neither end, or not-both.
- Add positional tolerance to each pair footprint with `-slop`.
- Enforce or ignore strand agreement depending on the assay design.

## Common Patterns

```bash
# 1) Require both ends of A to overlap B
pairToPair \
  -a loops_A.bedpe \
  -b loops_B.bedpe \
  -type both
```

```bash
# 2) Allow either end to match with 500 bp slop
pairToPair \
  -a loops_A.bedpe \
  -b loops_B.bedpe \
  -type either \
  -slop 500
```

```bash
# 3) Ignore strand and avoid self-matches by name
pairToPair \
  -a pairs.bedpe \
  -b pairs.bedpe \
  -is \
  -rdn
```

## Recommended Workflow

1. Confirm both files are valid BEDPE and represent the same conceptual pair geometry.
2. Choose `-type` based on whether one-end hits are sufficient or both anchors must agree.
3. Add `-slop` only when you intentionally want fuzzy anchor matching.
4. Use `-rdn` when self-hits or same-name artifacts would pollute the comparison.

## Guardrails

- `-a` and `-b` are both required.
- Strands are enforced by default; add `-is` to ignore them.
- `-slop` expands each footprint of A before matching, which can materially change reported overlap rates.
- `-type both` is the default and is stricter than many users expect.
- Prefer `-h` for help; GNU-style `--help` / `--version` calls on these wrappers are noisy.
