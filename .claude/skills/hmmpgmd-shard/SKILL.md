---
name: hmmpgmd-shard
description: Use when running the sharded `hmmpgmd_shard` daemon so large protein sequence databases are split across HMMER worker nodes.
disable-model-invocation: true
user-invocable: true
---

# hmmpgmd-shard

## Quick Start

- **Command:** `hmmpgmd_shard [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hmmpgmd_shard`
- **Full reference:** See `references/help.md` for the current startup failure; daemon behavior below is grounded in the local man page

## When To Use This Tool

- Use `hmmpgmd_shard` when `hmmpgmd` would waste too much RAM by loading the full protein sequence database into every worker.
- This sharded variant divides protein sequence databases across worker nodes while keeping HMM databases unsharded.
- Reach for it when you already want an `hmmpgmd` master-worker deployment but need predictable RAM savings on very large sequence databases.

## Common Patterns

```bash
# Start a sharded master that expects 4 worker shards
hmmpgmd_shard --master --num_shards 4 --seqdb seqdb.hmmpgmd --hmmdb models.hmm
```

```bash
# Start a worker that connects to the sharded master
hmmpgmd_shard --worker 10.0.0.5 --seqdb seqdb.hmmpgmd --hmmdb models.hmm --cpu 8
```

## Recommended Workflow

1. Prepare the same kinds of inputs as `hmmpgmd`: hmmpgmd-formatted protein sequence databases and optionally HMM databases.
2. Decide the exact worker count first, because the master must be started with `--num_shards` equal to that number.
3. Start the master, then start exactly the required number of workers so each shard has a corresponding worker.
4. Submit client jobs only after all required workers are connected.
5. Monitor memory and worker registration closely, because sharding only helps if the deployment size matches the shard plan.

## Guardrails

- The actual executable name uses an underscore: `hmmpgmd_shard`, not `hmmpgmd-shard`.
- The local executable currently fails to start because `libopenblas.so.0` is missing, so live `-h` validation is unavailable in this environment.
- `--num_shards <n>` is only valid on the master and must equal the number of worker nodes that will connect.
- The daemon errors out if more than `num_shards` workers connect, or if a search is attempted before all required workers are connected.
- Only sequence databases are sharded; HMM databases are still loaded in full on every worker.
