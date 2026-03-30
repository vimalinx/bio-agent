---
name: test-pcre
description: Use when testing or benchmarking PCRE2 regular expressions with the local `test_pcre` / `pcre2test` executable.
disable-model-invocation: true
user-invocable: true
---

# test-pcre

PCRE2 test harness installed here as `test_pcre`. It is the standard `pcre2test`-style CLI for trying patterns against subjects, checking compile-time options, and timing compilation or matching.

## Quick Start

- **Command:** `test_pcre [options] [input [output]]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/test_pcre`
- **Reported tool identity:** `pcre2test`

## When To Use This Tool

- Trying a PCRE2 pattern against sample subjects before embedding it elsewhere
- Checking PCRE2 build capabilities such as JIT, Unicode, newline type, or enabled library widths
- Timing regex compilation or execution with `-t`, `-tm`, `-T`, or `-TM`
- Debugging pattern behavior with `-d`, `-i`, or other pcre2test modifiers

## Common Patterns

```bash
# Show usage
test_pcre -help
```

```bash
# Show version
test_pcre -version
```

```bash
# Minimal pattern/subject test via stdin
printf '/abc/\nabc\n\n' | test_pcre
```

## Recommended Workflow

1. Start with `test_pcre -help` or `test_pcre -C` to confirm available PCRE2 features.
2. Feed pattern/subject pairs through stdin or an input file in pcre2test format.
3. Add debug/info/timing flags only after the base match works.
4. Use the exact local command name `test_pcre`, not the skill folder name.

## Guardrails

- The real executable here is `test_pcre` with an underscore, not `test-pcre`.
- `test_pcre -help` works and prints standard `pcre2test` usage; `-version` reports `PCRE2 version 10.44 2024-06-07`.
- In live testing, `printf '/abc/\nabc\n\n' | test_pcre` produced a successful match with capture line `0: abc`.
- `-v|--version` is documented by the tool, so GNU-style `--version` should be treated as valid for the real executable even though the old skill text assumed otherwise.
