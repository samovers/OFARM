# OFARM Concept Boundary Map v0.1

Date: 2026-05-14  
Status: active companion artifact; interpretive map, not replacement baseline law  
Role: reduce ontology drift by making core concept boundaries easy to inspect

## Purpose

This map gives implementers and reviewers a quick boundary guide for OFARM concepts that are commonly confused. It preserves the RC2.1 model/runtime split, assertion/history-first truth, explicit promotion law, and PassportView/DocumentAssembly output separation.

## Boundary table

| Concept | Means | Does not mean | Truth posture |
|---|---|---|---|
| Thing | Durable real-world subject such as a field, party, lot, facility, machine, crop cycle, or governed named scope. | A record about the thing, a current-state row, or an output view. | Identified by governed identity/lifecycle law. |
| Role | Time-bounded authority, responsibility, relationship, or participation posture of a party/system. | The party identity itself or an unrestricted permission. | Requires explicit role/authority/delegation basis. |
| Event | Something that happened, was claimed to have happened, or was accepted as having happened. | A durable resource or mutable status bucket. | Event-family and commit-class law controls promotion. |
| Record | A canonical assertion, review, evidence, authority, or consequence artifact. | A UI card or cache row. | Assertion/history-first truth carrier. |
| Observation | A reported or measured view of farm reality at a time and scope. | Recommendation, prescription, execution, or accepted consequence. | Supports decisions; does not become treatment truth by itself. |
| Measurement evidence | Method-bound evidence with result, source, provenance, calibration/uncertainty where relevant. | Final compliance fact or accepted state. | Evidence carrier; may support promotion after sufficiency/review. |
| Recommendation | Advisory suggestion or analysis output. | Prescription, work order, execution, or governance decision. | Advisory Twin unless explicitly converted through governed action. |
| Prescription / authorized intent | A governed instruction or intent to perform an intervention. | Proof that work happened. | Intent carrier; not execution truth. |
| Planned intervention | Operational plan/work-order state. | Executed work or accepted consequence. | Planning state; must not auto-promote. |
| Execution claim | A party/system claim that work happened. | Accepted execution or as-applied truth. | Historical claim requiring evidence/review for high consequence. |
| As-applied evidence | Machine log, operator record, product/quantity/extent evidence, or related source payload. | Accepted consequence by itself. | Evidence; may be degraded, disputed, corrected, or superseded. |
| Accepted consequence | Reviewed/promoted consequence of an event or operation. | Original claim, machine log, or current-state projection. | Compliance Twin truth result after promotion law. |
| Correction | Superseding or amending record that changes interpretation of a prior claim/result. | Deletion of historical record. | Must preserve lineage and supersession basis. |
| Dispute | Explicit challenge or disagreement over a claim, evidence, extent, quantity, identity, authority, or outcome. | Automatic invalidation or accepted truth. | Must remain reconstructable; output policy decides disclosure/refusal. |
| Evidence | Source, artifact, attestation, payload, snapshot, or measurement basis. | Governance decision. | Evaluated by evidence sufficiency and provenance policy. |
| Current-state materialization | Governed projection derived from canonical history. | Canonical truth store. | Derivative; freshness and basis must be traceable. |
| PassportView | Governed compiled view for passport-like disclosure. | A generic bucket for all outputs or a truth source. | Derivative output with policy, freshness, and trace basis. |
| DocumentAssembly | Compiled document/dossier/annex package. | PassportView or canonical truth. | Derivative output; can include annexed unresolved/disputed material without promotion. |
| External standard binding | Link to an external code, registry, vocabulary, exchange format, or runtime surface. | Imported OFARM law or proof of compliance by itself. | Anchor/binding/mapping only, subject to profile and verification policy. |

## Boundary stress rules

1. Observation can support a decision, but it does not become the decision.
2. Recommendation can become input to a prescription, but it does not become a prescription by label change.
3. Prescription can authorize intended work, but it does not prove work happened.
4. Execution claim can support review, but it is not accepted consequence.
5. Machine/as-applied evidence can support promotion, but it is not automatic truth.
6. Current state can support display/query, but stale or unsupported materialization cannot drive high-consequence output by default.
7. PassportView and DocumentAssembly must remain distinct compiled output classes.

## Status discipline

This companion artifact is an interpretive map. If it conflicts with `00_active_baseline/`, the baseline wins. If it reveals ambiguity, amend the accepted RFCs or baseline through controlled change rather than silently reinterpreting schemas or examples.
