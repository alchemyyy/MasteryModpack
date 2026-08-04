#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python_cmd="${PYTHON:-python}"

"$python_cmd" "$script_dir/compile_mrpack.py" "$@"
