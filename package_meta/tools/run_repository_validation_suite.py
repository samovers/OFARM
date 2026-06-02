#!/usr/bin/env python3
from __future__ import annotations
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
COMMANDS = [
    ['python3', 'package_meta/tools/validate_repo_hygiene.py'],
    ['python3', 'package_meta/tools/check_generated_currentness.py'],
    ['python3', 'package_meta/tools/check_repository_cross_references.py'],
    ['python3', 'package_meta/tools/check_repository_steward_guardrails.py'],
    ['python3', '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP10_final_readiness_claim_limits_v0_1/conformance/ofarm_cp10_final_readiness_runner_v0_1.py'],
    ['python3', '04_implementation_and_conformance/conformance_runners/cyber_physical_mission_conformance/ofarm_cp12_phase7_2_conformance_runner.py'],
    ['python3', '04_implementation_and_conformance/conformance_runners/learning_experimentation_farm_memory_conformance/ofarm_cp13_phase7_2_conformance_runner.py'],
    ['python3', '04_implementation_and_conformance/conformance_runners/farm_to_farm_intelligence_boundary_conformance/ofarm_cp14_phase7_2_conformance_runner.py'],
    ['python3', '04_implementation_and_conformance/conformance_runners/agentic_software_delivery_model_deployment_conformance/ofarm_cp15_phase7_2_conformance_runner.py'],
]

def main() -> int:
    for cmd in COMMANDS:
        print('$ ' + ' '.join(cmd))
        result = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
        if result.returncode != 0:
            if result.stdout:
                print(result.stdout[-4000:])
            if result.stderr:
                print(result.stderr[-4000:])
            return result.returncode
        # Print compact success marker; full runner JSON is kept in its own output files.
        print('PASS')
    print('Repository validation suite: OK')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
