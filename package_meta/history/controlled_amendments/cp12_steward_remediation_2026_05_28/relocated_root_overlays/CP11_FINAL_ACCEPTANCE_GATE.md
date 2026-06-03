# CP11 Final Acceptance Gate

CP11 may be accepted only if all conditions below are true.

## Baseline and RFC

- [ ] CP11 RFC is accepted as `02_accepted_rfcs/OFARM_Sustainable_Autonomous_Farming_Charter_RFC_v0_1.md`.
- [ ] Baseline patch text is reviewed and applied only as controlled additions.
- [ ] Existing assertion/history, current-state, twin, pack, authority, output, and AI-agent laws are not reopened.

## Machine contracts

- [ ] CP11 schemas remain in `drafts_non_default/` until currentness is explicitly updated.
- [ ] `REPORT_ONLY_LIMIT` is removed from `SustainabilityConstraint.constraintStrength`.
- [ ] Approval-dependent states are conditionally enforced.
- [ ] Evidence source, quality/status, and freshness are distinct.
- [ ] Exceptions cannot be open-ended.
- [ ] Claim-ready, attestation-ready, and filed states require basis and authority.
- [ ] Output qualifications cannot permit contradictory use classes.
- [ ] Risk/regret budgets do not authorise experimentation or execution.
- [ ] CP11 contracts do not authorise robot/machine execution.

## Pack law

- [ ] CP11 sustainability pack surfaces are added to pack merge/currentness machinery.
- [ ] Conflicting sustainability pack surfaces hard-fail or require governance.

## Conformance

- [ ] P0/P1 executable fixtures pass.
- [ ] Aggregate conformance result is retained.
- [ ] Capability/readiness claims distinguish model-law support from runtime implementation support.

## Non-claims

- [ ] No claim of production readiness.
- [ ] No claim of autonomous compliance decisioning.
- [ ] No claim of robot/machine execution readiness.
- [ ] No claim of certification readiness.
- [ ] No claim of CP12, CP13, CP14, or CP15 readiness.


## Phase 7.1 additional acceptance checks

- [x] Draft/currentness identity fixed across CP11 schemas.
- [x] SustainabilityMetricProfile evidence fields remediated.
- [x] Draft pack schema patches added.
- [x] Positive and negative conformance fixtures included.
- [x] Conformance runner validates payloads against JSON Schema.
- [x] Output allowed/blocked use no-overlap guarded.
- [x] Grant/reference array minItems/uniqueItems guarded where required.
- [x] High-governance CharterApprovalGate actions require traceRequired true.
- [x] TradeoffPolicy rule-level ALLOW requires allowBasis.
- [x] PolicyEvaluationTrace result objects typed.
- [x] CP11 hook headings renamed to reduce scope creep.
- [x] RFC section numbering fixed.


## Phase 7.3 final boundary and claim-disposition checks

- [x] `CLAIM_READY` requires `outputDisposition = CLAIM_BEARING`.
- [x] `ATTESTATION_READY` requires `outputDisposition = ATTESTATION_CANDIDATE`.
- [x] `FILED` requires `outputDisposition = FILED_SUBMISSION`.
- [x] Failed hard `SustainabilityConstraint` results cannot allow `ALLOW` or `ALLOW_WITH_QUALIFICATION`, even when `blocking = false`.
- [x] Complete `ALLOW_WITH_QUALIFICATION` with empty typed results requires `noApplicableRulesBasis`.
- [x] Advisory-only outputs block public disclosure by default.
- [x] Positive and negative fixtures were added for the Phase 7.3 boundary cases.
- [x] Schema validation and schema-aware semantic conformance passed after Phase 7.3 hardening.
