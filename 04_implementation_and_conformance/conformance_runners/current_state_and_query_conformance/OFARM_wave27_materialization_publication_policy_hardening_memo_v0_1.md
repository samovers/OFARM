# OFARM wave 27 materialization/publication policy hardening memo v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact

## 1. Why this wave exists

Wave 26 closed the authority action-class and sharing-boundary seam.
The next still-partial central cluster in the conformance matrix was:

- invalidation-trigger breadth
- high-consequence recomputation versus refusal
- Compliance-versus-Advisory materialization policy
- runtime-produced evidence sufficiency and attestation/publication decisions
- compiled-output taxonomy conformance
- passport-versus-document separation

This wave stays inside `04_implementation_and_conformance/`.
It does not amend baseline law, accepted RFCs, companion policy, or machine-contract substance.

## 2. What this wave adds

This wave adds one bounded runtime-shaped evidence slice spanning materialization and publication:

- `OFARM_runtime_materialization_publication_pipeline_records_v0_1.json`
- `OFARM_runtime_materialization_publication_invalidation_records_v0_1.json`
- `OFARM_runtime_twin_materialization_policy_records_v0_1.json`
- `OFARM_runtime_evidence_attestation_publication_decision_records_v0_1.json`
- `OFARM_runtime_compiled_output_taxonomy_records_v0_1.json`
- `OFARM_runtime_publication_trace_back_records_v0_2.json`
- `OFARM_runtime_materialization_publication_telemetry_v0_1.json`
- `OFARM_runtime_materialization_publication_results_v0_1.json`

The runner emits runtime-shaped evidence for:

- advisory stale reuse with warning for low-consequence live and frozen outputs
- compliance recompute on context drift, evidence update, output-profile change, and submission-binding change
- refusal on explicit invalidation and high-consequence filing attempts
- attestation allow, review, and refuse outcomes
- signatory-scope failure denial
- live `PassportView` serving as distinct from frozen `DocumentAssembly` and `SubmissionAssembly` flows
- trace-back linkage from publication outcomes back to basis, snapshot, context, and evidence decisions

## 3. Bounded scope

This wave is intentionally bounded:

- no deployment-collected telemetry
- no new schema families
- no new output adapter families
- no bridge-pack promotion work

The goal is to close the central runtime policy seam, not to widen external-surface breadth.

## 4. Expected conformance effect

This wave is intended to move the following rows from `PARTIAL` to `COVERED`:

- invalidation-trigger tests
- high-consequence recomputation/refusal tests
- Compliance-versus-Advisory materialization-policy tests
- evidence-sufficiency case and attestation-policy tests
- compiled-output taxonomy conformance tests
- passport-vs-document separation tests

It should also strengthen, but not fully close, these rows:

- enforcement-gate sequencing tests
- projection trace-back tests

## 5. Guardrail

This is implementation/conformance hardening only.
If future work needs live deployment evidence or partner-specific publication adapters, that should be added as a later bounded conformance wave rather than smearing new law back into RC2.1.
