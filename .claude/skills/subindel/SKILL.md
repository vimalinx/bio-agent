---
name: subindel
description: Use when calling short or long indels from read alignments with the Subread `subindel` tool.
disable-model-invocation: true
user-invocable: true
---

# subindel

Compiled Subread indel caller. The live binary advertises a simple interface centered on `-i`, `-g`, `-o`, optional fragment distance `-d`, maximum indel length `-I`, and `--paired-end`, then writes VCF-style results for downstream variant analysis.

## Quick Start

- **Command:** `subindel -i alignments.sam -g subread_index -o sample`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/subindel`
- **Observed usage source:** live banner from bare invocation / invalid option path

## When To Use This Tool

- Calling indels from alignments that are already mapped to a Subread index
- Running a Subread-native indel caller after alignment rather than using a separate variant caller stack
- Handling paired-end libraries where fragment distance matters
- Adjusting the maximum indel length threshold for broader searches

## Common Patterns

```bash
# Basic indel calling
subindel -i sample.sam -g genome_index -o sample
```

```bash
# Paired-end calling with expected fragment distance
subindel -i sample.sam -g genome_index -o sample -d 300 --paired-end
```

```bash
# Increase maximum indel length
subindel -i sample.sam -g genome_index -o sample -I 200
```

## Recommended Workflow

1. Align reads first and keep the resulting alignment file in the format expected by the live CLI banner.
2. Make sure the matching Subread index is available through `-g`.
3. Start with the default indel length limit, then raise `-I` only when your assay genuinely needs longer events.
4. Add fragment-distance settings only for paired-end libraries.

## Guardrails

- `-h` is not a real help flag; local testing returned `subindel: invalid option -- 'h'` and then printed the usage banner. `--version` is likewise unrecognized.
- The visible CLI contract advertises `-i <SAM file> -g <subread index> -o <output>` plus optional `-d`, `-I`, and `--paired-end`. Follow that documented interface instead of guessing hidden flags.
- Usage text says “output VCF”, but the built-in example uses `-o my_result`, and binary strings contain `%s.indel.vcf`; treat `-o` as an output base/prefix rather than assuming an exact final filename.
- Binary strings include an internal warning that suggests `-p`, but the public usage banner documents `--paired-end`; prefer the documented long flag.
- Additional binary strings indicate very-long-indel detection can reject multi-block indexes and ask for `-I <= 16`, so extra-long-indel modes may have index constraints.
