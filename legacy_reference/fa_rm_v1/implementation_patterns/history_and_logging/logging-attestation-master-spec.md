# Logging and Attestation Master Spec

Version: 0.1 (draft)
Date: 2026-03-11
Applies to: hybrid logging and attestation rollout on OF Platform, with SI organic crops-only as the first fully worked compliance example.

## 0. Scope and Hard Constraints

1. This program covers the full handoff package: current-state baseline, capability matrix, contradictions ledger, normative target model, runtime contracts appendix, and unresolved decisions.
2. `docs/implementation/` is the canonical home for this package.
3. First-rollout commit semantics stay hybrid:
   - generic `Operation*` abstractions define the target architecture
   - current event-specific `/v1/field-ops/*` routes remain the authoritative v1 commit path
   - current `/v1/compliance/*` endpoints remain the authoritative v1 attestation-fact path
4. `Field` and `CropInstance` remain the semantic anchors for execution.
5. `ProductionUnitSeasonSlot` is an overlay for lightweight planning and logging coordination, not a replacement entity and not a new twin of `Field` or `CropInstance`.
6. Committed execution stays append-only.
7. `OperationDraft`, `OperationProposal`, review items, and `OperationComplianceAssessment` stay outside immutable `ExecutedOperation` records.
8. The first concrete example stays `SI + organic + crops-only + 2026`.
9. `complianceProfile` is modeled as `jurisdiction + scheme + scope + version`.

## 1. Semantic Anchors and Target Types

### Observed current state

- The base model already has `Field`, `CropInstance`, `PlannedOperation`, `ExecutedOperation`, and `EvidenceRecord` as first-class anchors. Evidence: `specs/v0.1/Farm-RM-v0.1-Specification.md:L79-L112`, `specs/v0.1/ontology/farm-rm-v1.ttl:L18-L30`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L99-L269`
- Current crop-context resolution reuses or creates `CropInstance` records instead of inventing a second execution anchor. Evidence: `specs/api/v1/server/fastapi/app/main.py:L21757-L21920`, `docs/implementation/crop-context-resolver-governed-fallback.md:L38-L63`
- The nearest existing planning-layer contract is the A.5 canonical source-plan entry, which is already explicitly modeled outside committed execution facts. Evidence: `docs/implementation/si-rb-a5-1-rotation-plan-structure-spec.md:L83-L145`, `specs/v0.8/archetypes/CLUSTER.rotation_plan_entry.v1.md:L1-L53`

### Evidence-backed inference

- The target logging model should wrap existing anchors rather than replace them, because commit, reporting, and crop-context flows already depend on `Field` and `CropInstance`.
- The planning overlay problem is already partially solved in repo evidence by A.5 source-plan semantics plus crop-context ensure, so the missing abstraction is a lightweight coordination layer, not a new source-of-truth entity.

### Recommended working assumption

- Treat `ExecutedOperation` as the immutable fact that starts once an operation is committed.
- Treat all pre-commit, proposal, assessment, and review state as additive surfaces around that fact.
- Treat `ProductionUnitSeasonSlot` as the lightweight bridge between logging intent, crop-context readiness, and incomplete plan coverage.

### Normative target

| Type | Purpose | Required anchors | Persistence rule |
| --- | --- | --- | --- |
| `OperationCatalog` | Governed registry of operation families, commit adapters, required anchors, and profile hooks. | `operationFamilyCode`, `commitRoute`, `requiredAnchors`, `supportedProfiles[]` | Additive registry or generated config; not a mutable user record. |
| `OperationProposal` | Ranked suggestion from OCR, operator prompt, template hint, or prior history. | `proposalUri`, `operationFamilyCode`, `sourceKind`, `score`, `payloadDraft`, `sourceEvidence[]` | Mutable or replaceable suggestion state; never a committed execution fact. |
| `OperationDraft` | Saveable mutable operation record before immutable commit. | `draftUri`, `operationFamilyCode`, `fieldUri`, optional `cropInstanceUri`, `seasonSlotUri`, `proposalUri`, `draftPayload`, `draftEvidence[]` | Stored outside `executed_operation`; updateable until commit or discard. |
| `OperationRequirementProfile` | Declares completeness rules for one operation family under one compliance profile. | `profileKey`, `operationFamilyCode`, `requirements[]`, `reportBindings[]` | Additive policy/config surface; versioned by profile. |
| `OperationComplianceAssessment` | Evaluates one committed operation against one `OperationRequirementProfile`. | `assessmentUri`, `executedOperationUri`, `profileKey`, `requirementResults[]`, `attestationState`, `reportReady` | Separate append-only or superseding assessment records; never mutate the execution fact. |
| `ProductionUnitSeasonSlot` | Lightweight overlay that binds one production unit, season window, and crop-context intent before or alongside full planning. | `seasonSlotUri`, `fieldUri`, `seasonCode`, optional `cropInstanceUri`, optional `cropTypeUri`, `productionStatus`, `basisCode` | Overlay/readiness surface only; not a replacement for `Field` or `CropInstance`. |

## 2. Lifecycle and State Model

### Observed current state

- Current field-op routes commit directly to immutable execution facts and auto-link payload evidence. Evidence: `specs/api/v1/server/fastapi/app/main.py:L25109-L25417`, `specs/api/v1/server/fastapi/app/main.py:L28495-L28787`, `specs/api/v1/server/fastapi/app/main.py:L28790-L28988`, `specs/api/v1/server/fastapi/app/persistence.py:L6172-L6326`, `specs/api/v1/server/fastapi/app/persistence.py:L7935-L8097`, `specs/api/v1/server/fastapi/app/persistence.py:L8099-L8261`
- Current compliance endpoints capture supporting facts separately from execution and reporting joins them later. Evidence: `specs/api/v1/server/fastapi/app/main.py:L42017-L42960`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1456-L1490`
- Current binder behavior exposes incompleteness through warnings, not a dedicated shared lifecycle state. Evidence: `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1547-L1574`, `specs/api/v1/server/fastapi/tests/test_reporting_control_pack.py:L1305-L1338`

### Evidence-backed inference

- A single lifecycle axis is too coarse because commit, attestation, and reportability already happen on different surfaces.
- The system needs one explicit state model that keeps saveability, immutable commit, profile attestation, and report readiness distinct.

### Recommended working assumption

- Model lifecycle as layered state, not one overloaded status field.
- Keep the immutable execution fact binary: not committed vs committed.
- Keep attestation and report readiness profile-scoped and review-derived.

### Normative target

The canonical state model is:

| State | Meaning | Where it lives |
| --- | --- | --- |
| `saveable` | The payload is coherent enough to retain as draft, even if not yet ready for immutable commit. | `OperationDraft` |
| `committed` | Immutable execution fact has been written through the authoritative event-specific route. | `ExecutedOperation` plus event-specific row |
| `non_attested` | A committed operation has no approved profile-scoped assessment yet. | `OperationComplianceAssessment` |
| `partially_attested` | Some requirements for a profile have been reviewed or satisfied, but at least one required item remains unresolved. | `OperationComplianceAssessment` |
| `attested` | All required checks for a profile are satisfied and approved for that operation. | `OperationComplianceAssessment` |
| `report_ready` | The committed operation, related facts, and profile bindings are sufficient for the target report path. | Derived read model from assessment plus report bindings |

Normative clarifications:

1. `operator_attestation` is an evidence type, not a lifecycle state.
2. A record can be `committed` and still be `non_attested`.
3. A record can be `attested` but not `report_ready` if report-binding requirements remain unresolved.
4. `report_ready` is profile-scoped and report-path-scoped, not globally absolute.

## 3. Hybrid Runtime Architecture

### Observed current state

- Commit authority lives in event-specific `/v1/field-ops/*` routes. Evidence: `specs/api/v1/server/fastapi/app/main.py:L25109-L28988`
- Compliance fact authority lives in `/v1/compliance/*` routes. Evidence: `specs/api/v1/server/fastapi/app/main.py:L42017-L42960`
- Reporting authority for SI organic crops-only lives in `build_si_org_control_pack_payload()` plus reporting fetch helpers. Evidence: `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1326-L1715`, `specs/api/v1/server/fastapi/app/persistence.py:L16550-L17280`

### Evidence-backed inference

- The safest v1 architecture is not "replace routes with a generic operation API". It is "add generic proposal/draft/assessment/workbench layers that adapt back into existing commit and compliance surfaces".
- This approach preserves the only commit/reporting paths already proven by tests and current implementation docs.

### Recommended working assumption

- Generic logging abstractions are orchestration surfaces.
- Event-specific routes stay the commit adapters.
- Compliance routes stay fact adapters.
- Reporting keeps reading committed facts plus compliance records, not draft state.

### Normative target

The hybrid pipeline is:

1. `OperationCatalog` defines which event-specific commit adapter is authoritative for each operation family.
2. `OperationProposal` provides ranked candidate payloads from OCR, prompts, or explicit user selection.
3. `OperationDraft` stores mutable saveable payload plus evidence and crop/planning context.
4. `POST draft -> commit` invokes the mapped event-specific `/v1/field-ops/*` route, producing immutable `ExecutedOperation`.
5. `OperationComplianceAssessment` evaluates the committed fact against one `OperationRequirementProfile`.
6. Review and attestation actions update assessment state, not the committed operation.
7. Report-ready read models are derived from committed execution, compliance records, and assessment results.

## 4. Crop Context and Lightweight Planning Overlay

### Observed current state

- Current crop-bound commits require `fieldUri` plus `cropInstanceUri` on representative routes. Evidence: `specs/api/v1/server/fastapi/app/main.py:L25121-L25149`, `specs/api/v1/server/fastapi/app/main.py:L28519-L28528`, `specs/api/v1/server/fastapi/app/main.py:L28835-L28863`
- Crop-context ensure exists precisely to resolve valid crop context before those commits. Evidence: `specs/api/v1/server/fastapi/app/main.py:L21752-L21920`, `specs/api/v1/server/fastapi/tests/test_crop_context_ensure.py:L115-L376`
- A.5 rotation planning already models five-year field planning outside immutable execution facts, with explicit provenance and unresolved-status handling. Evidence: `docs/implementation/si-rb-a5-1-rotation-plan-structure-spec.md:L83-L145`, `specs/v0.8/templates/template-si-recordbook-a5-rotation-plan-crops-only-v0_8.md:L8-L27`

### Evidence-backed inference

- The system already knows how to work with incomplete planning context through controlled overlays and explicit provenance.
- A lightweight season-slot overlay can align with this pattern without displacing the current field/crop anchors.

### Recommended working assumption

- Use `ProductionUnitSeasonSlot` only when the user can identify a field and a season but not yet a durable `cropInstanceUri` or full `PlannedOperation`.
- Allow a slot to carry `cropTypeUri` or crop-label intent, `productionStatus`, and provenance basis until crop-context ensure resolves a `cropInstanceUri`.

### Normative target

`ProductionUnitSeasonSlot` MUST:

1. Reference one `fieldUri` and one `seasonCode`.
2. Carry one `basisCode` from:
   - `crop_instance_bound`
   - `crop_context_resolved`
   - `explicit_plan_overlay`
   - `rotation_reconstructed`
   - `operator_declared_pending_resolution`
3. Optionally carry:
   - `cropInstanceUri`
   - `cropTypeUri`
   - `productionStatus`
   - `certificationScopeUri`
   - `proposalUri`
4. Never replace the committed operation anchor.
5. Be discardable or supersedable without mutating `ExecutedOperation`.

## 5. Compliance Profiles and Assessments

### Observed current state

- Rulepacks and report packs are already profile-shaped by jurisdiction and scope. Evidence: `specs/v0.4/regulatory/rulepacks/organic-eu-2026.json:L1-L86`, `specs/v0.4/regulatory/rulepacks/organic-si-2026.json:L1-L78`, `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L1-L81`
- Current compliance routes capture facts that later feed reporting and inspector-note views, but do not evaluate one operation into one profile-scoped assessment. Evidence: `specs/api/v1/server/fastapi/app/main.py:L42017-L42960`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1456-L1490`

### Evidence-backed inference

- The repo already contains enough profile-specific structure to justify a first-class `OperationRequirementProfile`.
- Because fact capture is append-only and separate, assessment should remain a derived or additive layer rather than a mutation of those facts.

### Recommended working assumption

- Define `profileKey = jurisdiction + scheme + scope + version`.
- Resolve requirements by `profileKey + operationFamilyCode`.
- Evaluate assessments over committed operations plus linked evidence and related compliance facts.

### Normative target

`OperationRequirementProfile` MUST define:

1. `profileKey`
2. `operationFamilyCode`
3. `saveRequirements[]`
4. `attestationRequirements[]`
5. `reportBindingRequirements[]`
6. `relatedComplianceFacts[]`

`OperationComplianceAssessment` MUST define:

1. `assessmentUri`
2. `executedOperationUri`
3. `profileKey`
4. `operationFamilyCode`
5. `attestationState`
6. `reportReady`
7. `requirementResults[]`
8. `derivedFromEvidenceUris[]`
9. `derivedFromComplianceRecordUris[]`
10. `reviewedAt`

Each `requirementResults[]` item MUST include:

1. `requirementCode`
2. `status` from `met | missing | waived | not_applicable | conflicting`
3. `message`
4. `linkedEvidenceUris[]`
5. `linkedRecordUris[]`

## 6. Control Center Workbench Target

### Observed current state

- Control Center today is a local operational plane with health checks, payload inspection, request capture, service actions, reporting-governance inventory, and proxied review queue/detail/action plus report-binding backfill surfaces for the additive workbench layer. Evidence: `apps/control-center/README.md:L3-L12`, `apps/control-center/README.md:L141-L200`, `apps/control-center/server.py:L2269-L2468`, `apps/control-center/server.py:L3191-L3370`, `apps/control-center/tests/test_operation_review_workbench.py:L47-L181`

### Evidence-backed inference

- Control Center is already the repo-backed operational front door for diagnostics and governance checks, and it is now also the current local proxy/workbench entry point for the additive review surfaces.
- The remaining gap is not route existence or basic local operator documentation, but broader hosting and rollout clarity.

### Recommended working assumption

- Treat Control Center as the current local proxy/workbench entry point and the primary near-term home for review and attestation surfaces.
- Keep operator documentation explicit about the current proxy-first and still-partial rollout reality.

### Normative target

The Control Center workbench MUST expose:

1. Queue/list view:
   - missing requirements
   - stale drafts
   - committed but non-attested operations
   - attested but not report-ready operations
2. Detail view:
   - committed execution fact summary
   - linked proposal and draft provenance
   - linked evidence and compliance records
   - assessment-by-requirement results
3. Actions:
   - refresh assessment
   - request evidence
   - attach `operator_attestation`
   - mark `partially_attested`
   - mark `attested`
   - escalate to related compliance fact flows
4. Reporting surface:
   - target report path
   - report-readiness reasons
   - unresolved binding warnings

## 7. Reporting and Report-Ready Semantics

### Observed current state

- The SI binder already joins executed operations, conversion timelines, parallel-production controls, seed-sourcing exceptions, and A.5 source plans. Evidence: `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1326-L1715`
- Reporting fetch for executed operations already includes operation-type derivation and linked evidence URIs. Evidence: `specs/api/v1/server/fastapi/app/persistence.py:L17173-L17280`, `specs/api/v1/server/fastapi/tests/test_persistence.py:L8282-L8373`
- A.5 tests prove the reporting layer preserves explicit unknown and unsupported states instead of fabricating certainty. Evidence: `specs/api/v1/server/fastapi/tests/test_reporting_control_pack.py:L1267-L1338`

### Evidence-backed inference

- Report readiness should be derived from committed facts plus profile bindings, not from draft state and not from implicit binder heuristics alone.
- The current binder warning behavior is a suitable precursor for a first-class report-readiness explanation model.

### Recommended working assumption

- Keep reporting reads attached to committed operations and compliance records.
- Let assessments contribute status and reasons, but do not let reports read mutable draft state directly.

### Normative target

An operation is `report_ready` for a given `profileKey` and report path only when:

1. it is `committed`
2. its `OperationComplianceAssessment.attestationState` is `attested`
3. all `reportBindingRequirements[]` are `met`, `waived`, or `not_applicable`
4. all required linked compliance facts are present
5. the report path has no unresolved blocking warning derived from that operation

The report-ready explanation MUST include:

1. `blockingRequirementCodes[]`
2. `missingEvidenceUris[]`
3. `missingComplianceFactCodes[]`
4. `bindingWarningCodes[]`
5. `nextActionCode`

## 8. Worked Scenario: SI Organic Crops-Only

### Observed current state

- OCR parse already returns structured proposals and persistence targets. Evidence: `specs/api/v1/server/fastapi/app/main.py:L1716-L1793`, `specs/api/v1/server/fastapi/app/main.py:L9129-L9299`
- Crop-context ensure already supports resolving `cropInstanceUri` before commit. Evidence: `specs/api/v1/server/fastapi/app/main.py:L21752-L21920`
- Planting commit, compliance fact capture, and control-pack reporting all exist as separate proven surfaces. Evidence: `specs/api/v1/server/fastapi/app/main.py:L25109-L25417`, `specs/api/v1/server/fastapi/app/main.py:L42017-L42960`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1326-L1715`

### Evidence-backed inference

- A full end-to-end workflow can be specified immediately by chaining already-proven runtime surfaces with additive draft and assessment layers.

### Recommended working assumption

- Use planting as the first explicit operation-family example.
- Use SI organic crops-only as the first `profileKey`.

### Normative target

The canonical end-to-end scenario is:

1. Suggestion intake:
   - OCR or operator prompt creates one or more `OperationProposal` records for `operationFamilyCode = planting`.
   - Each proposal stores ranked payload candidates and the originating evidence or prompt.
2. Draft creation:
   - the operator accepts or edits a proposal into `OperationDraft`
   - the draft enters `saveable`
   - if no `cropInstanceUri` is available, the draft may bind to `ProductionUnitSeasonSlot`
3. Minimal save with operator declaration:
   - the operator may attach `operator_attestation` as draft evidence
   - this does not imply profile-scoped `attested`
4. Crop-context resolution:
   - before commit, the backend resolves crop context through crop-context ensure if required
5. Immutable commit:
   - `POST /v1/operation-drafts/{draftId}/commit` maps to `POST /v1/field-ops/planting-events`
   - successful commit writes immutable `ExecutedOperation` plus payload evidence
   - the draft becomes read-only and links to the committed operation
6. Profile assessment:
   - the system resolves `profileKey = si + organic + crops_only + 2026`
   - it evaluates save, attestation, and report-binding requirements into `OperationComplianceAssessment`
   - the new assessment starts as `non_attested` or `partially_attested`
7. Control Center review:
   - the operation appears in Control Center review queue with missing requirements
   - reviewer sees linked execution, evidence, and related compliance facts
8. Attestation progression:
   - reviewer resolves missing items, potentially via current `/v1/compliance/*` routes for conversion, parallel-production, or seed-sourcing records
   - reviewer advances assessment to `attested`
9. Report-ready outcome:
   - once report-binding requirements are also satisfied, the operation becomes `report_ready`
   - the SI control-pack binder can consume the committed fact and linked evidence without reading mutable draft state

## 9. Non-Goals

1. Replace current `/v1/field-ops/*` routes in v1.
2. Replace current `/v1/compliance/*` routes in v1.
3. Introduce a new twin entity that competes with `Field` or `CropInstance`.
4. Broaden the first fully worked compliance example beyond SI organic crops-only.
