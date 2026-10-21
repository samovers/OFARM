#!/usr/bin/env python3
"""Run the registered offline Event Ingress proof cases; no runtime admission."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "04_implementation_and_conformance/conformance_runners/event_ingress_classification_proof/run_conformance.py"
PACKAGE = ROOT / "03_machine_contracts/drafts_non_default/event_ingress_classification_proof"
FIXTURES = ROOT / "04_implementation_and_conformance/examples_and_fixtures/fixtures/event_ingress_classification_proof"


def main():
    with tempfile.TemporaryDirectory(prefix="ofarm-event-proof-") as output:
        return subprocess.run([
            sys.executable, "-B", str(CHECKER), "--package-root", str(PACKAGE),
            "--fixture-root", str(FIXTURES), "--source-root", str(FIXTURES), "--output-dir", output,
        ], cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
