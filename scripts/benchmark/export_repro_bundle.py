#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.bio_skill_system import export_benchmark_repro_bundle, load_structured_file, save_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a benchmark reproducibility bundle from a benchmark-run JSON payload.")
    parser.add_argument("--benchmark-run-file", required=True, help="Benchmark-run JSON/YAML file")
    parser.add_argument("--output-dir", required=True, help="Target reproducibility bundle directory")
    parser.add_argument("--invoked-command", help="Optional benchmark-run command string to record in commands.sh")
    parser.add_argument("--output", help="Optional JSON output file")
    args = parser.parse_args()

    payload = load_structured_file(Path(args.benchmark_run_file))
    result = export_benchmark_repro_bundle(
        payload,
        Path(args.output_dir),
        invoked_command=args.invoked_command,
    )
    text = save_json(result, Path(args.output) if args.output else None)
    if not args.output:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
