# Explainable Current-State Evidence Conformance

Status: implementation/conformance support.

This lane supports `02_accepted_rfcs/OFARM_Performance_and_Explainable_Current_State_Evidence_RFC_v0_1.md` with deterministic fixture metadata and a runner skeleton. It does not override accepted RFC authority, active baseline law, or current/default machine-contract selection.

The runner validates that the fixture pack names the expected behavior, trace tier, pass/fail criteria, and benchmark-only metrics for the RFC fixture family. It does not execute a runtime benchmark and does not claim production, fleet-scale, or workload-envelope readiness.

Benchmark outputs remain conformance evidence only. They do not become canonical farm truth, do not change materialization results, and do not override active OFARM authority.

Production or fleet readiness requires separately declared workload-envelope evidence, benchmark runs, storage-amplification evidence, cold rebuild evidence, and capability-claim disclosure.

Files:

- `fixtures_explainable_current_state_evidence_v0_1.json`
- `ofarm_explainable_current_state_evidence_conformance_runner_v0_1.py`
- `OFARM_explainable_current_state_evidence_conformance_summary_v0_1.json`
- `OFARM_explainable_current_state_evidence_conformance_summary_v0_1.md`
