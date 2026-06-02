# OFARM submission-gateway promotion and equivalent contract fixtures v0.1

Date: 2026-04-19  
Status: active supporting implementation artifact  
Scope: bounded fixture lane for future governed filing-boundary promotion without promoting `PARTNER_SUBMISSION_XML` in the current package

---

## Purpose

This wave closes the next narrow seam after the partner-output governance boundary.
It answers the question:

- what would have to become true before OFARM promotes a submission adapter into a governed filing boundary

It does this without adding a new active machine-contract family.

## Included artifacts

- `OFARM_submission_gateway_promotion_decision_matrix_v0_1.json`
- `OFARM_submission_gateway_contract_candidate_v0_1.json`
- `service_descriptions/submission_gateway_candidate_v0_1/README.md`
- `service_descriptions/submission_gateway_candidate_v0_1/organic_certifier_submission_gateway_descriptor_v0_1.json`
- `ofarm_submission_gateway_promotion_boundary_runner_v0_1.py`
- `OFARM_submission_gateway_promotion_boundary_results_v0_1.json`

## What this wave does

- keeps the current `PARTNER_SUBMISSION_XML` lane implementation-local and explicit
- converts the earlier “future-promotion candidate” posture into a concrete promotion threshold
- defines a fixture-only candidate contract shape for a later governed filing-boundary lane
- ties that candidate shape back to existing active filing artifacts such as `SubmissionAssembly`, publication request/result boundaries, evidence-sufficiency cases, and authorization traces
- proves that the candidate lane is **not** silently entering the current manifest/release/runtime-surface lane

## What this wave does not do

- it does **not** promote `PARTNER_SUBMISSION_XML` into `RuntimeSurfaceContract`
- it does **not** create a new active machine-contract family in `03_machine_contracts/`
- it does **not** claim live partner filing receipts or deployment-collected gateway evidence
- it does **not** change the current filing-path truth model or no-edit-in-place correction posture

## Current bounded truth

Within the current package:

- successful submission filing is already traceable through publication request/result, evidence sufficiency, and authorization trace artifacts
- blocked submission publication already demonstrates a schema-mismatch refusal path
- partner-output telemetry keeps `PARTNER_SUBMISSION_XML` explicit while still retaining it outside the governed runtime-surface lane
- the new candidate gateway contract is fixture-only and intentionally absent from the current manifest and release bundle

## Conversion rule

Do not move the candidate gateway contract into `03_machine_contracts/` unless a later accepted OFARM governance step explicitly promotes it.

Do not add the candidate gateway identity into the Capability Manifest or runtime-surface release bundle until the submission gateway threshold is actually satisfied.

## Qualification rule for future promotion

Promotion work should start only when a real partner filing lane provides all of the following:

- stable external boundary identity
- published schema/service-description artifacts that matter operationally
- receipt/rejection semantics that matter operationally
- duplicate/retry/correlation semantics beyond local adapter behavior
- explicit correction/amendment semantics at the filing lane itself
- deployment/release traceability that names the lane directly

Until then, the fixture-only candidate lane is sufficient.
