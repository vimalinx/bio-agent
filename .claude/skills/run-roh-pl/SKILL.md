---
name: run-roh-pl
description: Use when batch-running `bcftools roh` across a directory of VCF, VCF.GZ, or BCF files and merging the resulting ROH calls across samples.
disable-model-invocation: true
user-invocable: true
---

# run-roh-pl

Perl convenience wrapper around `bcftools roh`. It scans an input directory of variant files, normalizes chromosome names, optionally injects allele-frequency annotations, runs `bcftools roh` per sample file, appends genotype rows with `bcftools query`, and finally merges surviving ROH regions into one summary table.

## Quick Start

- **Command:** `run-roh.pl -i <indir> -o <outdir>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/run-roh.pl`
- **Downstream visualizer:** `plot-roh.py`

## When To Use This Tool

- Running the same ROH-calling workflow across many per-sample VCF, VCF.GZ, or BCF files in one directory
- Producing merged cross-sample ROH presence/absence summaries without hand-writing bcftools loops
- Applying consistent ROH length, marker-count, and quality filters before cross-sample merging
- Augmenting the batch run with allele-frequency annotations or IMPUTE2-style genetic maps

## Common Patterns

```bash
# Basic batch ROH run
run-roh.pl -i cohort-vcfs -o roh-out
```

```bash
# Add allele frequencies and a genetic map directory
run-roh.pl -i cohort-vcfs -o roh-out -a af-tags.bcf -m genetic-maps
```

```bash
# Forward extra options directly to bcftools roh
run-roh.pl -i cohort-vcfs -o roh-out --roh-args '--buffer-size 200000,200000'
```

## Recommended Workflow

1. Put only `.vcf`, `.vcf.gz`, or `.bcf` sample files in the input directory.
2. If using `-a`, make sure the annotation file exists alongside both its `.tbi` index and `.hdr` header sidecar.
3. Run the wrapper and inspect the output directory for per-sample `.bcf`, `.txt.gz`, and `.log` files plus the final `merged.txt`.
4. Use `plot-roh.py` or your own downstream logic on the generated `*.txt.gz` and `merged.txt` outputs.

## Guardrails

- `--help` prints real usage text, but `--version` is not implemented; locally it failed with `Unknown parameter "--version". Run -h for help.`
- `-i/--indir` and `-o/--outdir` are mandatory.
- The wrapper enforces extra sidecars for `-a/--af-annots`: it refuses to run unless `<file>`, `<file>.tbi`, and `<file>.hdr` all exist.
- Source inspection shows the output directory also gets `chr-names.txt`, and the merge phase writes `merged.txt` with one row per merged region and one indicator column per sample.
- Existing per-sample `.bcf` or `.txt.gz` outputs are skipped on rerun, so the wrapper is partially restart-friendly.
- The ROH phase always appends `bcftools query -f 'GT\t%CHROM\t%POS[\t%SAMPLE\t%GT]\n'` output to each `.txt.gz`, which is why `plot-roh.py` can later consume the files.
