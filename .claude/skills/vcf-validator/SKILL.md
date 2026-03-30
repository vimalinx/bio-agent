---
name: vcf-validator
description: Use when you need to validate VCF files for format compliance and detect issues like duplicate positions.
disable-model-invocation: true
user-invocable: true
---

# vcf-validator

## Quick Start
- **Command:** `vcf-validator [OPTIONS] file.vcf.gz`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/vcf-validator`
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Check whether a VCF is structurally valid before indexing, merging, or handing it to stricter downstream software.
- Detect duplicate positions that may break assumptions in later tools.
- Collapse repeated warning types to a single message when triaging noisy files.

## Common Patterns

```bash
# 1) Basic validation
vcf-validator file.vcf.gz
```

```bash
# 2) Warn about duplicate positions too
vcf-validator -d file.vcf.gz
```

```bash
# 3) Show each message type only once
vcf-validator -u file.vcf.gz
```

## Recommended Workflow

1. Validate the VCF before compression/index regeneration, merging, or cohort comparison.
2. Re-run with `-d` if positional duplication is a concern in your workflow.
3. Use `-u` for noisy failure cases so you can see the distinct categories of problems quickly.
4. Fix the source VCF rather than normalizing around repeated validator failures downstream.

## Guardrails

- Use this as a structural sanity check, not as proof that the biological content is correct.
- Input is expected to be a VCF path in the style documented by the tool; compressed VCF is the common case in this workspace.
- `--version` is not supported in the usual way; use `-h` for interface help.
- Validation output can be noisy on badly malformed files, so `-u` is useful for triage but should not replace a full review.
