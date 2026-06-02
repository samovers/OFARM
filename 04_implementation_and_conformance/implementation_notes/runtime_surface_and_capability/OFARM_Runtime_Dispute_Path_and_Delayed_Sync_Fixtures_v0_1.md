# OFARM Runtime Dispute Path and Delayed Sync Fixtures v0.1

Date: 2026-04-18  
Status: active supporting implementation artifact  
Scope: bounded runtime-shaped fixtures for late-evidence correction/supersession and offline contractor sync after authority revocation

---

## 1. Purpose

These fixtures close two inspector-critical seams without changing OFARM law:

- a recommendation or plan becomes an execution claim, then an accepted consequence, then a frozen output, and later stronger evidence arrives
- a contractor performs work offline, synchronizes later, and authority has changed before the queued promotion step completes

The fixtures are designed to prove:
- no edit-in-place for frozen outputs or filed submissions
- original basis, actor lineage, and acceptance history are preserved
- late evidence creates successor output paths rather than historical erasure
- queued sync rechecks current authority before high-consequence promotion
- revoked contractor authority blocks auto-promotion but does not erase the historical local capture

---

## 2. Fixture families

### 2.1 Plan → claim → accepted consequence → frozen output → late evidence
1. a `PlannedIntervention` exists for row-selective pruning in field 17
2. the work is later reported through an execution claim
3. a governed `ReviewDecision` accepts the claim and mints an `AcceptedEventConsequence`
4. a frozen dossier and submission package are assembled on that basis
5. late evidence arrives after the output and after the filing
6. OFARM preserves the original dossier and the original filing basis
7. OFARM creates successor dossier/submission packages and successor review decisions instead of rewriting the originals

### 2.2 Offline contractor capture → delayed sync → revocation recheck
1. a contractor with delegated orchard authority captures work and evidence offline
2. the queued sync reaches the platform after the delegation was prospectively revoked
3. the historical contractor capture remains preserved
4. the queued promotion step re-checks active authority and returns review-required rather than auto-accept
5. a review decision is emitted to keep the dispute/audit trail explicit

---

## 3. Non-goals

This fixture family does not:
- add a new truth store
- claim deployment-collected delayed-sync telemetry or a full product-grade sync engine
- claim multi-hop delegation or full correction workflow product readiness

It only closes the package-internal runtime-shaped evidence seam for the two highest-value dispute paths named by review.


---

## 4. Relationship and boundary hardening addendum (2026-04-21)

The first hostile multiparty fixture wave adds explicit relationship/boundary context around the delayed-sync lane.

New supporting artifacts:
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartyRelationship_example_contracted_service_orchard_team_3_greenacre_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/interoperability/OFARM_ExternalCommitmentLink_example_service_contract_linkage_field17_spring_2026_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AssertionRecord_example_service_provider_field17_delayed_sync_execution_claim_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_ReviewDecision_example_service_provider_sync_review_requested_v0_1.json`

Interpretation:
- contracted service and service contract linkage are now machine-visible context
- they still do not create delegation, accepted execution, or dispute resolution by implication
- the delayed-sync path continues to re-enter explicit review after revocation
- settlement/payment remain outside OFARM truth and were not required to prove the late-sync governance seam
