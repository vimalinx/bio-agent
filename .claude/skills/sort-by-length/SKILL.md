---
name: sort-by-length
description: Use when sorting plain text lines by character length, especially in shell pipelines where one logical item is stored per line.
disable-model-invocation: true
user-invocable: true
---

# sort-by-length

Tiny Bash wrapper around a one-line Perl sort. It reads stdin line by line and emits the same lines ordered by increasing string length.

## Quick Start

- **Command:** `... | sort-by-length`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/sort-by-length`
- **Implementation core:** `perl -e 'print sort { length($a) <=> length($b) } <>'`

## When To Use This Tool

- Sorting one-item-per-line text streams by line length
- Reordering small identifier or sequence-string lists before downstream filtering
- Applying a lightweight length-based sort inside an EDirect-style shell pipeline
- Avoiding a custom Perl one-liner when a reusable wrapper already exists

## Common Patterns

```bash
# Sort simple text lines by length
printf 'bbb\na\ncc\n' | sort-by-length
```

```bash
# Reorder a generated list before taking the shortest entries
some_generator | sort-by-length | head
```

```bash
# Save the sorted result
cat items.txt | sort-by-length > items.sorted.txt
```

## Recommended Workflow

1. Feed the tool a line-oriented text stream.
2. Use it only when each logical item already occupies exactly one line.
3. Capture or pipe the reordered output immediately into the next shell stage.
4. If ties matter, assume Perl's default sort behavior rather than relying on an explicit stable-sort contract.

## Guardrails

- This tool sorts lines, not multi-line FASTA/GenBank records, so it is unsafe for structured sequence files unless they have already been flattened to one record per line.
- There is no real `-h`, `--help`, or `--version` interface; invoking it with flags and no stdin simply produces no useful metadata output.
- In local testing, `printf 'bbb\na\ncc\n' | sort-by-length` produced `a`, `cc`, `bbb`, confirming ascending line-length order.
- The wrapper refuses to run only if `perl` is missing; otherwise it passes stdin straight into the Perl expression.
