---
name: window-bed
description: Use when you need to find features in one file that fall within a configurable window around features in another file, including strand-aware upstream and downstream proximity searches.
disable-model-invocation: true
user-invocable: true
---

# window-bed

## Quick Start
- **Command**: `windowBed -a <bed/gff/vcf> -b <bed/gff/vcf> -w <bp>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/windowBed`
- **Full reference**: See `references/help.md`

## When To Use This Tool

- Find nearby features in B around each feature in A without requiring direct overlap.
- Build promoter, enhancer, or neighborhood-style proximity joins.
- Use asymmetric windows with different upstream and downstream distances.
- Count, flag, or exclude nearby hits instead of returning full paired records.

## Common Patterns

```bash
# 1) Find B features within 5 kb of each A feature
windowBed \
  -a genes.bed \
  -b peaks.bed \
  -w 5000
```

```bash
# 2) Query a strand-aware promoter window: 2 kb upstream, 500 bp downstream
windowBed \
  -a transcripts.bed \
  -b atac-peaks.bed \
  -l 2000 \
  -r 500 \
  -sw \
  -sm
```

```bash
# 3) Count nearby features instead of returning paired records
windowBed \
  -a genes.bed \
  -b enhancers.bed \
  -w 100000 \
  -c
```

## Recommended Workflow

1. Decide whether you need the default paired-output join, a presence/absence view (`-u`, `-v`), or counts (`-c`).
2. Choose a symmetric window with `-w` or an asymmetric design with `-l` and `-r`.
3. Add `-sw` only when upstream/downstream should be interpreted relative to strand, and add `-sm` or `-Sm` only when overlap partners must match or oppose strand.
4. If A is BAM, switch to `-abam` and choose whether output should stay BAM-like or be converted with `-bed`.

## Guardrails

- `-a` and `-b` are both required unless BAM input is supplied through `-abam`, which replaces `-a`.
- If you do not specify `-w`, `-l`, or `-r`, bedtools uses a default symmetric window of 1000 bp.
- Default output emits the full A and full B record for every hit; `-u`, `-c`, and `-v` change the row count and layout substantially.
- `-sw` changes how left/right windows are interpreted relative to feature strand; it is different from `-sm` / `-Sm`, which filter the strand relationship between A and B.
- Prefer `-h` for help; GNU-style `--help` and `--version` emit wrapper errors before usage text.
