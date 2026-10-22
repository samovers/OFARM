#!/usr/bin/env python3
"""Opt-in occupancy evidence checks; no runtime writes or source admission."""
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[2]
def main():
    with tempfile.TemporaryDirectory(prefix="ofarm-occupancy-") as output:
        return subprocess.run([sys.executable,"-B",str(ROOT/"04_implementation_and_conformance/conformance_runners/material_occupancy_evidence/run_conformance.py"),
            "--package-root",str(ROOT/"03_machine_contracts/drafts_non_default/material_occupancy_evidence"),"--fixture-root",str(ROOT/"04_implementation_and_conformance/examples_and_fixtures/fixtures/material_occupancy_evidence"),
            "--out",str(Path(output)/"conformance-report.json")],cwd=ROOT).returncode
if __name__=="__main__": raise SystemExit(main())
