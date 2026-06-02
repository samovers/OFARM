# AAI-CP1 AI-facing release qualification gate v0.1

Generated: 2026-05-16T13:00:00+02:00

Status: ACTIVE BASELINE PATCH + SUPPORTING IMPLEMENTATION / CONFORMANCE CONTROL MATERIAL.

Authority effect: CP1 edits the active baseline files in `00_active_baseline/`. This folder records the controlled-promotion evidence, examples, claim limits, and validation for that baseline patch. It does not itself promote any RFC, companion artifact, or machine-contract schema.

## Purpose

AAI-CP1 implements the synthesis finding that OFARM must strengthen “no hidden truth / no hidden governance” into an executable release gate. AI-facing, public-operation, state-affecting, and high-consequence surfaces must not ship results whose material limitations are hidden or only implied.

## What CP1 promotes

CP1 promotes only a narrow baseline-law clarification:

- a release surface must be able to produce machine-readable material qualification for state-affecting or high-consequence use;
- material qualification must be faithfully surfaced to users or downstream systems;
- missing material qualification must lead to review, refusal, or a policy-declared successor disposition;
- free-text explanation alone is not sufficient for operational or compliance-ready reliance.

## What CP1 does not promote

CP1 does not promote:

- `ResultQualificationEnvelope`;
- `TraceRetrievalResult`;
- `PublicOperationDescriptor`;
- `PreflightRequest` or `PreflightResult`;
- agent actorship, run trace, handoff, tool-manifest, world-model, EvidenceNeed, or ObservationRequest contracts;
- runtime readiness, two-agent compatibility, autonomous compliance decisioning, production readiness, or external-standard readiness.

## Outputs

- `disposition_memo.md`
- `affected_active_artifacts.md`
- `draft_patch/OFARM_AAI_CP1_baseline_release_qualification_gate_patch_v0_1.md`
- `draft_patch/OFARM_AAI_CP1_unified_diff.patch`
- `promotion_register.json`
- `claim_limits.json`
- `no_schema_promotion_manifest.json`
- `examples/positive/OFARM_AAI_CP1_positive_daily_brief_qualified_v0_1.json`
- `examples/negative/OFARM_AAI_CP1_negative_hidden_stale_basis_v0_1.json`
- `conformance/fixtures/OFARM_AAI_CP1_release_gate_fixture_plan_v0_1.json`
- `conformance/expected_traces/OFARM_AAI_CP1_expected_trace_qualification_block_v0_1.json`
- `conformance/validation_report.json`
- `CP1_file_manifest.json`

## Next phase

Proceed to CP2: public surfaces, preflight/dry-run, trace retrieval, and concrete result-qualification contracts.
