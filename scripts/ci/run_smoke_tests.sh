#!/usr/bin/env bash
set -euo pipefail

python3 -m pytest -q -m smoke tests/test_productization_roadmap.py "$@"
