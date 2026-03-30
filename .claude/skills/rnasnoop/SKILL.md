---
name: rnasnoop
description: Use when searching target RNAs for interactions with a query H/ACA snoRNA, especially when the search should respect H/ACA-specific structural constraints and optionally use accessibility profiles.
disable-model-invocation: true
user-invocable: true
---

# rnasnoop

## Quick Start

- **Command:** `RNAsnoop -s <query_file> -t <target_file>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/RNAsnoop`
- **Full reference:** See [references/help.md](references/help.md) for complete options and details

## When To Use This Tool

- Use `RNAsnoop` when the biological question is specifically about **H/ACA snoRNA target prediction**, not general RNA-RNA duplexing.
- It is tailored to snoRNA-target geometry and stem constraints, so it is more appropriate than generic ViennaRNA interaction tools for this niche case.
- Use `-P` or `-U` when accessibility profiles from `RNAplfold` or `RNAup` should be incorporated into target ranking.
- Reach for the duplex/stem-length filters when your snoRNA architecture differs from the defaults or you need to tighten candidate selection.

## Common Patterns

```bash
# Basic H/ACA snoRNA target search
RNAsnoop -s sno.fa -t target.fa

# Add accessibility profiles from RNAplfold
RNAsnoop -s sno.fa -t target.fa -P plfold_profiles/

# Add accessibility profiles from RNAup
RNAsnoop -s sno.fa -t target.fa -U rnaup_profiles/

# Tighten stem-length and energy filters for stricter candidate selection
RNAsnoop -s sno.fa -t target.fa -h 6 -i 80 -q -1200
```

## Recommended Workflow

1. Prepare query file containing the H/ACA snoRNA sequence and target file containing the RNA sequence to search
2. Run `RNAsnoop -s <query.fa> -t <target.fa>` to compute hybridization structures
3. Review output: dot-bracket structures with `<>` for snoRNA intramolecular interactions and `()` for intermolecular duplexes, including energy values in kcal/mol
4. Optionally provide accessibility profiles via `-P` (RNAplfold) or `-U` (RNAup) to improve target prediction accuracy

## Guardrails

- This tool is specialized for H/ACA snoRNA target prediction only; for general RNA-RNA interactions use RNAduplex, RNAup, RNAcofold, or RNAplex instead
- Energy threshold options expect values in decacal/mol (not kcal/mol); a threshold of -2.8 kcal/mol should be specified as -280
- Default parameter values assume typical H/ACA snoRNA stem lengths (5-120 nt) and duplex-box distances (11-16 nt); adjust `-h/-i` and `-j/-k` if your snoRNA differs significantly
- `RNAsnoop -h` does not show help; `-h` is the minimal stem length option, so use `--help` for usage text
