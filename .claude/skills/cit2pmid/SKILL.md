---
name: cit2pmid
description: Use when resolving structured citation fields or citation XML into candidate PubMed IDs with EDirect matching modes.
disable-model-invocation: true
user-invocable: true
---

# cit2pmid

## Quick Start

- **Command**: `cit2pmid -title "nucleotide sequences required for tn3 transposition immunity" -author "Kans JA" -author "Casadaban MJ" -journal "J Bacteriol" -year 1989 -volume 171 -issue 4 -page 1904-14`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/cit2pmid`
- **Reference**: See [references/help.md](references/help.md) for detailed usage

## When To Use This Tool

- Resolve structured citation fields to candidate PMIDs.
- Switch between remote, local, exact, verification, or E-utilities matching modes depending on available infrastructure.
- Consume either explicit `-title` / `-author` / `-journal` fields or compact citation payloads via `-asn` or `-cit`.

## Common Patterns

```bash
# 1) Query by explicit citation fields (default mode = remote)
/home/vimalinx/miniforge3/envs/bio/bin/cit2pmid \
  -title "nucleotide sequences required for tn3 transposition immunity" \
  -author "Kans JA" \
  -author "Casadaban MJ" \
  -journal "J Bacteriol" \
  -year 1989 \
  -volume 171 \
  -issue 4 \
  -page 1904-14
```

```bash
# 2) Read compact citation XML from stdin
cat citation.xml | \
  /home/vimalinx/miniforge3/envs/bio/bin/cit2pmid -cit -
```

```bash
# 3) Use a local archive-backed matching mode when configured
/home/vimalinx/miniforge3/envs/bio/bin/cit2pmid \
  -local \
  -title "Example title" \
  -author "Smith JA"
```

## Recommended Workflow

1. Decide whether you want the default remote matcher, `-eutils`, `-local`, `-exact`, or `-verify`.
2. Supply citation content either as explicit field/value pairs or via `-asn -` / `-cit -` on stdin.
3. Start with the most specific fields you have, especially title, authors, journal, year, volume, issue, and first page.
4. Validate any returned PMIDs with downstream PubMed queries before trusting them in automation.

## Guardrails

- `-help` and `-version` are not metadata flags here; the parser treats them as field names and errors with "Missing -help argument" or "Missing -version argument".
- Default mode is `remote`; `-local` and `-exact` require local archive infrastructure, while `-verify` chains local and remote logic.
- Repeated `-author` arguments are interpreted as first author then last author.
- Page ranges are truncated to the first page internally before matching.
