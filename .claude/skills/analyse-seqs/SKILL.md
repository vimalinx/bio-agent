---
name: analyse-seqs
description: Use when analyzing equal-length sequence sets with the legacy ViennaRNA statistical-geometry, clustering, or distance-matrix utility driven from stdin.
disable-model-invocation: true
user-invocable: true
---

# analyse-seqs

Legacy ViennaRNA sequence-set analysis tool for equal-length inputs. It reads sequence blocks from stdin, can build Hamming or edit-distance matrices, and can emit PostScript summaries for statistical geometry or tree reconstruction modes.

## Quick Start

- **Command:** `AnalyseSeqs`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/AnalyseSeqs`
- **Live help path:** `AnalyseSeqs -h`
- **Input contract:** reads sequence data from stdin until a separator line beginning with `@` or `%`

## When To Use This Tool

- Analyze a set of equal-length sequences with legacy ViennaRNA exploratory methods rather than modern aligners or phylogeny suites.
- Build Hamming, Needleman-Wunsch, or Gotoh distance matrices before neighbour-joining or Ward clustering.
- Generate statistical-geometry or clustering PostScript output from a small curated sequence panel.
- Work from stdin streams that may also include an optional taxa list and output filename prefix.

## Common Patterns

```bash
# 1) Neighbour-joining with Hamming distance and taxa labels
cat <<'EOF' | AnalyseSeqs -Xn -DH
* demo
1 : A
2 : B
3 : C
4 : D
*
AAAA
AAAT
AATT
TTTT
@
EOF
```

```bash
# 2) Statistical geometry (the default -Xb mode) with a PostScript sidecar
cat <<'EOF' | AnalyseSeqs -Xb -DH
* demo
1 : A
2 : B
3 : C
4 : D
*
AAAA
AAAT
AATT
TTTT
@
EOF
# writes demo_box.ps
```

```bash
# 3) Ward clustering with a generated PostScript tree
cat <<'EOF' | AnalyseSeqs -Xw -DH
* demo
1 : A
2 : B
3 : C
4 : D
*
AAAA
AAAT
AATT
TTTT
@
EOF
# writes demo_wards.ps
```

## Recommended Workflow

1. Prepare equal-length sequences and terminate the input block with `@` or `%`.
2. If you want labeled output files, prepend a taxa block starting with `* prefix`, followed by numbered `n : Taxon` lines and a closing `*`.
3. Choose the analysis family with `-X...` and the distance algorithm with `-D...`; use `-d...` only when you intentionally want a non-default edit-cost matrix.
4. Inspect both stdout summaries and any generated PostScript sidecars such as `*_box.ps`, `*_nj.ps`, or `*_wards.ps`.

## Guardrails

- The real binary name is capitalized: `AnalyseSeqs`, not `analyse-seqs`.
- `-h`, `--help`, and `--version` all fell through to the same usage text in live testing; no clean version banner was observed.
- The installed man page says the tool reads from stdin until it sees `@` or `%`, ignores unrelated non-sequence lines, and supports an optional taxa list beginning with `*`.
- A minimal two-sequence smoke test (`AAAA`, `AAAT`, `@`) exited `0` with no stdout or sidecar output, so do not expect every input size to yield a direct report.
- The man page explicitly warns that only Hamming distance is well tested; treat `-DA` and `-DG` as higher-risk legacy paths.
- Generated PostScript filenames derive from the taxa-list prefix and analysis mode, for example `demo_box.ps`, `demo_nj.ps`, and `demo_wards.ps`.
