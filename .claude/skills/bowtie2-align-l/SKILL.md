---
name: bowtie2-align-l
description: Use when aligning sequencing reads to a reference using Bowtie 2's large-index alignment engine.
disable-model-invocation: true
user-invocable: true
---

# bowtie2-align-l

## Quick Start

- **Command**: `bowtie2-align-l`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/bowtie2-align-l`
- **Full reference**: See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Use `bowtie2-align-l` when your reference was indexed in Bowtie 2 large-index format (`.bt2l`), typically for very large references.
- It is appropriate for aligning single-end, paired-end, interleaved, or name-sorted unaligned BAM reads against that large index.
- Use it when you specifically need the large-index binary, not the generic `bowtie2` wrapper.
- Most routine workflows should still prefer the `bowtie2` wrapper unless you need to force the large-index executable directly.

## Common Patterns

```bash
# Align unpaired reads against a large Bowtie 2 index
bowtie2-align-l -x ref_large -U reads.fq -S aln.sam

# Align paired-end reads with multiple threads
bowtie2-align-l -x ref_large -1 reads_R1.fq -2 reads_R2.fq -p 8 -S aln.sam

# Use local alignment with a more sensitive preset
bowtie2-align-l -x ref_large -U reads.fq --very-sensitive-local -S aln.sam

# Report up to 5 alignments per read
bowtie2-align-l -x ref_large -U reads.fq -k 5 -S aln.sam
```

## Recommended Workflow

1. **Prepare index**: Ensure a Bowtie 2 large index (`.bt2l` files) exists for your reference genome
2. **Specify input**: Provide reads via `-1`/`-2` (paired), `-U` (unpaired), `--interleaved`, or `-b` (BAM)
3. **Configure alignment**: Select mode (`--end-to-end` or `--local`) and optionally a preset (e.g., `--sensitive-local`)
4. **Execute and output**: Run with `-x <index>`, input files, and `-S <output.sam>` (defaults to stdout)

## Guardrails

- Use Bowtie 2 indexes only (`.bt2l`); Bowtie 1 indexes are not compatible
- Prefer sensitivity presets over manual parameter tuning unless profiling requires it
- Consider the `bowtie2` wrapper script instead of direct invocation as recommended by the tool warning
- MAPQ is not meaningful in `-k` or `-a` multi-hit reporting modes
