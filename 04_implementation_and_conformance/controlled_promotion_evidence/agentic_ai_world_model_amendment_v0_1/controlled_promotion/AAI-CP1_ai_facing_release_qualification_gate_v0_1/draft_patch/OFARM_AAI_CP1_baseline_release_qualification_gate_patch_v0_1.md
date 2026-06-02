# OFARM AAI-CP1 baseline release-qualification gate patch v0.1

Generated: 2026-05-16T13:00:00+02:00

## Summary

This patch strengthens the existing AAI-P1 baseline-safety clarification by adding an AI-facing release-qualification gate.

## Baseline-law effect

A release surface that is AI-facing, public-operation-oriented, state-affecting, or high-consequence must be able to produce machine-readable qualification for material limitations. Missing or suppressed qualification is a gate failure.

## Non-promotion rule

This patch does not promote `ResultQualificationEnvelope`, `TraceRetrievalResult`, public-operation, preflight, or agentic/world-model draft schemas. Those remain CP2+ work.

## Changed active files

- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
- `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
- `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`
