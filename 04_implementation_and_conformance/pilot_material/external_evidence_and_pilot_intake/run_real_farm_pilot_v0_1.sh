#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python "$SCRIPT_DIR/ofarm_economic_intelligence_real_farm_pilot_cli_v0_1.py" "$@"
