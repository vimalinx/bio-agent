---
name: rnaparconv
description: Use when converting legacy ViennaRNA 1.8.4 energy parameter files to the 2.0+ format used by modern ViennaRNA tools.
disable-model-invocation: true
user-invocable: true
---

# rnaparconv

## Quick Start

- **Command**: `RNAparconv [options] [<input file>] [<output file>]`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/RNAparconv`
- **Full reference**: See [references/help.md](references/help.md) for complete options

## When To Use This Tool

- Use `RNAparconv` when you have a legacy ViennaRNA 1.8.4 parameter file that must be made compatible with ViennaRNA 2.x tools.
- It is appropriate for migration or reproducibility work where old parameter sets need to be preserved in a modern toolchain.
- Use `--dump` when you want the built-in ViennaRNA 1.8.4 defaults emitted directly in 2.x format without providing an input file.
- Use `--vanilla` or `--silent` when you want cleaner machine-readable output with minimal commentary.

## Common Patterns

```bash
# Convert an old parameter file to the modern format
RNAparconv -i old.par -o new.par

# Convert from stdin to stdout
cat old.par | RNAparconv

# Emit built-in ViennaRNA 1.8.4 defaults in 2.x format
RNAparconv --dump > vienna184.par

# Produce a minimal converted file
RNAparconv -i old.par -o new.par --vanilla
```

## Recommended Workflow

1. Confirm your input is a valid ViennaRNA 1.8.4 energy parameter file
2. Run `RNAparconv -i <input_file> -o <output_file>` to perform the conversion
3. Use `--vanilla` for minimal output or `--silent` to suppress non-parameter output
4. Verify the converted parameters work with your target ViennaRNA 2.0+ tool

## Guardrails

- Input must be a valid ViennaRNA 1.8.4 energy parameter file or parameters from stdin
- Output is in ViennaRNA 2.0+ format; converted files are not backward-compatible with 1.8.4
- Use `--dump` to output default 1.8.4 parameters in 2.0 format without any input file
