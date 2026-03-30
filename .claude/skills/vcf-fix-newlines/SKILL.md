---
name: vcf-fix-newlines
description: Use when VCF files have inconsistent or non-native newline characters and need normalization before downstream processing.
disable-model-invocation: true
user-invocable: true
---

# vcf-fix-newlines

## Quick Start
- **Command:** `vcf-fix-newlines [OPTIONS] [file.vcf|file.vcf.gz] > out.vcf`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/vcf-fix-newlines`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Normalize a VCF transferred from Windows or legacy systems before downstream parsing.
- Detect whether a file's newline style matches the current platform with `-i`.
- Clean a plain VCF or `.vcf.gz` before feeding it into stricter tooling.
- Repair line-ending issues without changing the variant content itself.

## Common Patterns

```bash
# 1) Report the source newline style only
vcf-fix-newlines -i file.vcf
```

```bash
# 2) Normalize a gzipped VCF into a plain-text output VCF
vcf-fix-newlines file.vcf.gz > fixed.vcf
```

```bash
# 3) Normalize a streamed VCF
cat file.vcf | vcf-fix-newlines > fixed.vcf
```

## Recommended Workflow

1. Probe first with `-i` if you are not sure whether newline normalization is actually needed.
2. Convert into a new output file instead of trying to overwrite the source.
3. Recompress and reindex afterward if the downstream pipeline expects `.vcf.gz` plus tabix.
4. Validate the resulting VCF with a parser once the line endings are fixed.

## Guardrails

- On this Linux machine, if the input already uses `\n`, the tool prints `No conversion needed.` and exits without echoing the file to stdout; do not use it as a transparent pass-through stage.
- `.vcf.gz` input relies on `gunzip -c` being available.
- `-i` only reports the detected platform / newline style; it does not emit the converted file.
- This script determines newline style from an initial sample of the file and errors if the format is too inconsistent to classify cleanly.
- The tool writes normalized content to stdout, so always redirect it to a new file.
