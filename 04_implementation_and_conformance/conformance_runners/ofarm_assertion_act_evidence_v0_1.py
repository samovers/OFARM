#!/usr/bin/env python3
"""Opt-in assertion-act evidence conformance; no runtime admission."""
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[2]
def main():
    with tempfile.TemporaryDirectory(prefix="ofarm-assertion-act-") as output:
        return subprocess.run([sys.executable, "-B", str(ROOT / "04_implementation_and_conformance/conformance_runners/assertion_act_evidence/run_act_conformance.py"),
            "--package-root", str(ROOT / "03_machine_contracts/drafts_non_default/assertion_act_evidence"), "--fixture-root", str(ROOT / "04_implementation_and_conformance/examples_and_fixtures/fixtures/assertion_act_evidence"),
            "--output-dir", output], cwd=ROOT).returncode
if __name__ == "__main__":
    raise SystemExit(main())
