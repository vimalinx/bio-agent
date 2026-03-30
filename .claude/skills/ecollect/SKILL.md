---
name: ecollect
description: Use when collecting sorted UID lists from EDirect query sources such as PubMed queries, explicit IDs, WebEnv history state, or input files.
disable-model-invocation: true
user-invocable: true
---

# ecollect

EDirect query-source normalizer and PubMed SOLR workaround wrapper. It can count matching PubMed records, return a limited `eSearchResult` subset, or emit a deduplicated UID list from query, history, inline IDs, raw rest data, or input files.

## Quick Start

- **Command:** `ecollect`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/ecollect`
- **Prerequisite:** network access to NCBI EUtils for query and history-based modes

## When To Use This Tool

- Turn `-query`, `-id`, `-input`, `-rest`, or history-server state (`-web` / `-key`) into a normalized UID list.
- Use PubMed-specific `-count` or `-subset` helper modes when working around large-result SOLR behavior.
- Deduplicate identifiers before sending them to downstream `efetch`, `esummary`, or other EDirect stages.
- Preserve an EDirect shell workflow instead of writing your own UID-expansion logic around EUtils.

## Common Patterns

```bash
# 1) Ask PubMed for just the count of matching records
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
ecollect -db pubmed -count 'BRCA1[Title]'
```

```bash
# 2) Retrieve a small eSearchResult XML subset for inspection
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
ecollect -db pubmed -subset 'BRCA1[Title]' -retmax 3
```

```bash
# 3) Normalize explicit IDs into a deduplicated UID list
PATH=/home/vimalinx/miniforge3/envs/bio/bin:$PATH \
ecollect -db pubmed -id 7 3 7 1
```

## Recommended Workflow

1. Decide which source mode you are using: PubMed query, explicit IDs, input file, raw rest payload, or history-server coordinates.
2. Always set `-db` first so the wrapper knows which downstream semantics to apply.
3. Use `-count` or `-subset` only when you specifically want PubMed query introspection; use the normal path when you want a final UID list.
4. Inspect a small sample before bulk fetches, especially if you also apply date filters or rely on history-server state.

## Guardrails

- `-db` is mandatory. Bare invocation or incomplete argument sets fail with `ERROR: Missing -db argument`.
- `-help` is not a real help switch. The live result is `ERROR:  Unrecognized argument -help` followed by the missing `-db` complaint.
- The wrapper appends its own bin directory to `PATH` and sources `ecommon.sh`, so behavior here is broader than a single network call.
- `-count` and `-subset` are specialized PubMed SOLR workaround modes, not generic options for every Entrez database.
- Final UID output is deduplicated through `sort -n | uniq`, so original order is not preserved.
- `-tranquil` suppresses the usual `No items found` warning/retry handling. That is useful for expected-empty searches but easy to misuse if you need loud failures.
