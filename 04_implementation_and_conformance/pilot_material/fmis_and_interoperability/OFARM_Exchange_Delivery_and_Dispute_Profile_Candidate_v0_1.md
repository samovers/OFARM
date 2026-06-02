# OFARM Exchange Delivery and Dispute Profile Candidate v0.1

Date: 2026-04-21  
Status: active supporting implementation artifact  
Scope: profile-first recommendation for delivery evidence and dispute boundary handling after the executed hostile multiparty fixture waves

---

## 1. Why this note exists

The targeted design pass recommended a narrow delivery/dispute lane and explicitly warned against creating a new top-level commerce truth family too early.
The executed hostile fixture waves have now exercised:
- contract-linked buyer access
- contracted-service no-delegation denial
- delayed sync after revocation
- explicit review handoff after delayed sync
- neighbour-help emergency review gating

This note records the outcome:
**the current fixtures still do not force a standalone `DeliveryEvidenceBundle` schema or a top-level `DisputeEvent` family.**

---

## 2. Current recommendation

### 2.1 Delivery evidence

Prefer a typed/profiled use of existing evidence-bearing structures over a new top-level family.
Minimum profile fields still worth carrying in implementation discussions are:
- delivery evidence bundle identifier
- linked contract reference
- linked lot refs and/or scope refs
- delivery event or delivery window reference
- sender and receiver party refs
- location/read-point reference
- evidence refs
- capture provenance
- bundle state

But the executed waves did not require a machine-enforced standalone schema to prove the boundary.

### 2.2 Dispute handling

Treat dispute open/update/close as an explicit `GovernanceEvent` / review-profile lane, not as a new top-level family.
In the current package the explicit review handoffs already prove the important runtime behavior:
- stale or revoked external context does not silently mutate OFARM truth
- the system produces explicit review/governance lineage instead of hidden mutation
- emergency-exception paths can remain review-gated without inventing new commerce truth families

### 2.3 Settlement and payment

Settlement and payment remain out of core OFARM truth.
No standalone `SettlementReceipt` or `PaymentReceipt` artifact is promoted in these waves.
If later needed, they should stay read-only reference/evidence carriers only.

---

## 3. Evidence from the hostile fixture waves

Relevant fixtures:
- `04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_Multiparty_Relationship_and_Boundary_Fixtures_v0_1.md`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/interoperability/OFARM_ExternalCommitmentLink_example_service_contract_linkage_field17_spring_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_contracted_service_report_without_delegation_deny_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_service_provider_sync_require_review_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_ReviewDecision_example_service_provider_sync_review_requested_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_neighbour_helper_emergency_require_review_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/pack_merge/OFARM_ReviewDecision_example_neighbour_help_emergency_review_requested_v0_1.json`

Observed result:
- context/reference artifacts and explicit review remain enough for the current hostile paths
- no standalone delivery/dispute schema was required to express or validate refusal and review posture

---

## 4. Consequence for tasking

`IMP-107` remains satisfied for the current wave set at the **profile-decision** level:
- keep delivery evidence profile-first
- keep dispute as a governance/review profile
- reopen only if later fixtures or pilot traffic prove real schema insufficiency
