#!/usr/bin/env python3
"""Opt-in selected authorization-output evidence checks; no effect permission."""
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[2]
def main():
    with tempfile.TemporaryDirectory(prefix="ofarm-canonical-path-") as output:
        return subprocess.run([sys.executable,"-B",str(ROOT/"04_implementation_and_conformance/conformance_runners/canonical_success_path/run_cases.py"),
            "--package-root",str(ROOT/"03_machine_contracts/drafts_non_default/authorization_decision_evidence/canonical_success_path"),"--fixtures-root",str(ROOT/"04_implementation_and_conformance/examples_and_fixtures/fixtures/canonical_success_path"),
            "--source-root",str(ROOT/"04_implementation_and_conformance/examples_and_fixtures/fixtures/canonical_success_path"),"--report",str(Path(output)/"conformance-report.json")],cwd=ROOT).returncode
if __name__=="__main__": raise SystemExit(main())
