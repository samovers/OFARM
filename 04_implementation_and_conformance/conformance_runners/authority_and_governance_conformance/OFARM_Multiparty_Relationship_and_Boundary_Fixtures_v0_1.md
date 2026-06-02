# OFARM Multiparty Relationship and Boundary Fixtures v0.1

Date: 2026-04-21  
Status: active supporting implementation artifact  
Scope: executed hostile fixture lanes for durable relationship semantics and starter sister-platform boundary artifacts

---

## 1. Purpose

This note now records the **executed** first and second hostile fixture packets for the typed relationship layer and starter exchange-boundary contracts.
It does not change active law.

These packets prove:
- durable relationship artifacts do not silently grant authority
- explicit grants and delegations still decide allowed actions
- recurring multiparty legal-operational context is machine-visible
- buyer contract linkage and cross-platform grant traceability can attach to stable OFARM references without mutating farm truth
- delayed sync, emergency handling, and dispute lineage re-enter explicit review/governance paths rather than silently promoting stale external state

Relationships remain **basis/context only**, and the boundary lane remains **reference/evidence only**. No commerce, settlement, payment, or advisory-social truth is promoted in this wave set.

## 2. Executed highest-priority fixture paths

### 2.1 Owner / tenant / operator disagreement

#### Relationship basis files
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/identity_lifecycle/OFARM_ScopeResponsibilityRelationship_example_tenancy_lease_field17_multiyear_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/identity_lifecycle/OFARM_ScopeResponsibilityRelationship_example_operational_stewardship_field17_greenacre_operating_co_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_ScopeResponsibilityRelationship_example_beneficial_ownership_field17_jana_kovac_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_RoleAssignment_example_field17_operator_greenacre_operating_co_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorityGrant_example_operator_file_submission_field17_2026_v0_1.json`

#### Allow path
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_tenant_operator_submission_allow_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_tenant_operator_submission_allow_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_tenant_operator_submission_allow_v0_1.json`

Expected outcome:
- **ALLOW** because the tenant/operator holds an explicit field-scoped filing grant for 2026
- tenancy and stewardship explain the context but do not create the power

#### Deny path after grant expiry
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_tenancy_submission_deny_after_grant_expiry_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_tenancy_submission_deny_after_grant_expiry_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_tenancy_submission_deny_after_grant_expiry_v0_1.json`

Expected outcome:
- **DENY** because the lease and operator context remain active into 2027 but the filing grant expired at the end of 2026
- proves tenancy does not imply filing/signatory power

#### Additional must-fail check
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_beneficial_owner_operational_deny_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_beneficial_owner_operational_deny_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_beneficial_owner_operational_deny_v0_1.json`

Expected outcome:
- **DENY** because beneficial ownership is visible but does not imply operational control or permission to mutate field truth

### 2.2 Advisor-of-record with delegated entry

#### Relationship basis files
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_PartyRelationship_example_advisor_retained_by_greenacre_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/identity_lifecycle/OFARM_ScopeResponsibilityRelationship_example_advisor_of_record_field17_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/core/OFARM_RoleAssignment_example_field17_advisor_agronomy_partners_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/drafts_non_default/authority/OFARM_DelegationGrant_example_advisor_draft_entry_field17_2026_v0_1.json`

#### Allow path for draft entry
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/drafts_non_default/authority/OFARM_AuthorizationDecisionRequest_example_advisor_draft_entry_allow_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/drafts_non_default/authority/OFARM_AuthorizationDecisionTrace_example_advisor_draft_entry_allow_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/drafts_non_default/authority/OFARM_AuthorizationDecisionResult_example_advisor_draft_entry_allow_v0_1.json`

Expected outcome:
- **ALLOW** for draft preparation only, because a narrow delegation exists
- proves advisor-of-record status itself does not do the permission work

#### Deny path for final submission
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_advisor_final_submission_deny_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_advisor_final_submission_deny_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_advisor_final_submission_deny_v0_1.json`

Expected outcome:
- **DENY** because advisor-of-record plus draft-entry delegation does not imply filing/signatory authority

### 2.3 Contract-linked buyer passport access

#### Boundary basis files
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/interoperability/OFARM_ExternalCommitmentLink_example_buyer_contract_linkage_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_ContractReference_example_buyer_passport_access_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_SharingGrant_example_lot_passport_buyer_7_2026_09_01_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_CrossPlatformGrantReceipt_example_buyer_passport_share_v0_1.json`

#### Allow path using explicit sharing
- request: existing `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_buyer_passport_read_v0_1.json`
- result: existing `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_buyer_passport_read_allow_v0_1.json`

Expected outcome:
- **ALLOW** because a separate SharingGrant exists
- contract linkage and grant receipt explain the cross-platform context but do not replace OFARM sharing law

#### Must-fail deny path without sharing
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_buyer_contract_read_without_sharing_deny_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_buyer_contract_read_without_sharing_deny_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_buyer_contract_read_without_sharing_deny_v0_1.json`

Expected outcome:
- **DENY** because contract linkage and buyer role do not create access without a SharingGrant

Important note:
`AuthorizationDecision*` artifacts continue to point at role/grant/delegation/sharing basis only. The contract/boundary files remain contextual and audit-relevant, not decision-basis permissions.

### 2.4 Delivery dispute / delayed sync / settlement reference posture

#### Relationship/boundary context files
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartyRelationship_example_contracted_service_orchard_team_3_greenacre_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/interoperability/OFARM_ExternalCommitmentLink_example_service_contract_linkage_field17_spring_2026_v0_1.json`

#### Must-fail contracted-service path without delegation
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_contracted_service_report_without_delegation_deny_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_contracted_service_report_without_delegation_deny_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_contracted_service_report_without_delegation_deny_v0_1.json`

Expected outcome:
- **DENY** because service relationship and service contract linkage remain context only; execution/report promotion still requires explicit delegation

#### Delayed-sync explicit review handoff
- assertion: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AssertionRecord_example_service_provider_field17_delayed_sync_execution_claim_v0_1.json`
- existing delayed-sync authorization result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_service_provider_sync_require_review_v0_1.json`
- existing delayed-sync authorization trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_service_provider_sync_require_review_v0_1.json`
- review handoff: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_ReviewDecision_example_service_provider_sync_review_requested_v0_1.json`

Expected outcome:
- historical contractor capture remains preserved
- queued promotion hits the revocation boundary and returns **REQUIRE_REVIEW**
- review remains explicit rather than silently accepting stale external state

Settlement/payment posture proven in this wave:
- no settlement or payment artifact was needed to validate the dispute path
- no standalone delivery or dispute top-level family was forced
- settlement/payment remain explanatory external references only at this stage

## 3. Executed second-priority fixture paths

### 3.1 Seasonal worker under supervision

#### Relationship and delegation basis files
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_PartyRelationship_example_employment_greenacre_luka_novak_harvest_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/core/OFARM_RoleAssignment_example_field17_seasonal_worker_luka_novak_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_DelegationGrant_example_greenacre_seasonal_worker_evidence_field17_harvest_2026_v0_1.json`

#### Allow path for evidence capture
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_seasonal_worker_evidence_allow_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_seasonal_worker_evidence_allow_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_seasonal_worker_evidence_allow_v0_1.json`

Expected outcome:
- **ALLOW** only for narrow evidence capture because an explicit supervised delegation exists
- employment and worker role remain context only

#### Must-fail deny path for submission
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_seasonal_worker_submission_deny_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_seasonal_worker_submission_deny_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_seasonal_worker_submission_deny_v0_1.json`

Expected outcome:
- **DENY** because employment and a seasonal-worker role do not imply filing or signatory power

### 3.2 Cooperative aggregation and branding

#### Relationship and sharing basis files
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_PartyRelationship_example_cooperative_membership_greenacre_northvalley_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_PartyRelationship_example_cooperative_admin_matej_zupan_northvalley_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/core/OFARM_RoleAssignment_example_lot17_cooperative_admin_matej_zupan_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_SharingGrant_example_cooperative_branding_passport_northvalley_2026_09_12_v0_1.json`

#### Allow path for branding review
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_cooperative_branding_read_allow_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_cooperative_branding_read_allow_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_cooperative_branding_read_allow_v0_1.json`

Expected outcome:
- **ALLOW** because explicit sharing exists for the lot passport used in cooperative branding review
- membership, admin status, and branding participation do not replace sharing law

#### Must-fail deny path without sharing
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_cooperative_branding_read_without_sharing_deny_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_cooperative_branding_read_without_sharing_deny_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_cooperative_branding_read_without_sharing_deny_v0_1.json`

Expected outcome:
- **DENY** because cooperative membership/admin context remains basis only and does not create member-lot access

### 3.3 Shared machinery / pooled responsibility

#### Relationship and delegation basis files
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartyRelationship_example_pooled_responsibility_participant_ana_borut_shared_sprayer_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ScopeResponsibilityRelationship_example_pooled_responsibility_shared_sprayer_ana_kovac_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ScopeResponsibilityRelationship_example_pooled_responsibility_shared_sprayer_borut_hribar_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_RoleAssignment_example_field17_shared_machinery_operator_borut_hribar_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_DelegationGrant_example_ana_kovac_shared_operator_borut_field17_spring_2026_v0_1.json`

#### Allow path for shared machinery reporting in the delegated field
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_pooled_operator_field17_allow_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_pooled_operator_field17_allow_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_pooled_operator_field17_allow_v0_1.json`

Expected outcome:
- **ALLOW** because an explicit field-17 delegation exists
- pooled responsibility remains context only

#### Must-fail deny path outside the delegated field
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_pooled_operator_field18_without_delegation_deny_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_pooled_operator_field18_without_delegation_deny_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_pooled_operator_field18_without_delegation_deny_v0_1.json`

Expected outcome:
- **DENY** because pooled participation and a field-17 shared-machinery role do not imply field-18 operate/report authority

### 3.4 Neighbour-help emergency handling

#### Relationship, delegation, and review basis files
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_ScopeResponsibilityRelationship_example_emergency_operator_designation_field19_marko_horvat_2026_07_02_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/core/OFARM_RoleAssignment_example_field19_neighbour_helper_marko_horvat_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_DelegationGrant_example_greenacre_neighbour_helper_field19_storm_2026_07_02_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/pack_merge/OFARM_AssertionRecord_example_neighbour_help_emergency_field19_claim_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/pack_merge/OFARM_ReviewDecision_example_neighbour_help_emergency_review_requested_v0_1.json`

#### Explicit review-gated emergency path
- request: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionRequest_example_neighbour_helper_emergency_require_review_v0_1.json`
- trace: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionTrace_example_neighbour_helper_emergency_require_review_v0_1.json`
- result: `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AuthorizationDecisionResult_example_neighbour_helper_emergency_require_review_v0_1.json`

Expected outcome:
- **REQUIRE_REVIEW** because the temporary emergency designation and narrow delegation preserve the historical claim but do not permit silent acceptance
- explicit review remains mandatory before OFARM accepts or contests the emergency operation claim

## 4. Promotion consequence of these waves

These waves show stable reuse of:
- `PartyRelationship`
- `ScopeResponsibilityRelationship`
- `ExternalCommitmentLink`
- `ContractReference`
- `CrossPlatformGrantReceipt`

They also continue to show that:
- relationship objects behave as basis/context only
- exchange-boundary objects behave as reference/receipt only
- delivery/dispute pressure still does **not** force a standalone delivery or dispute schema family
- seasonal labour, cooperative branding, pooled responsibility, and emergency helper paths can all be represented without widening the core authority objects

## 5. Remaining queued lane

Still queued after this execution:
1. advisory/community signal import boundary
