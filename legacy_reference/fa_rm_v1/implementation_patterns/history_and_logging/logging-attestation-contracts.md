# Logging and Attestation Contracts Appendix

- Date: 2026-03-11
- Scope: additive runtime contracts for the hybrid logging-and-attestation rollout.

## 1. Contract Principles

1. Existing strict event-specific commit routes remain authoritative in v1.
2. Existing `/v1/compliance/*` fact routes remain authoritative in v1.
3. New proposal/draft/assessment/workbench contracts are additive.
4. New contracts must not mutate committed `ExecutedOperation` rows.
5. Report-binding reads continue to consume committed execution facts plus compliance records and linked evidence.

## 2. Existing Authoritative Commit Adapters

| Operation family | Authoritative v1 commit route | Observed evidence |
| --- | --- | --- |
| `planting` | `POST /v1/field-ops/planting-events` | `specs/api/v1/server/fastapi/app/main.py:L25109-L25417`, `specs/api/v1/server/fastapi/app/persistence.py:L6172-L6326` |
| `mechanical_weeding` | `POST /v1/field-ops/mechanical-weeding-events` | `specs/api/v1/server/fastapi/app/main.py:L25420-L25420`, `specs/api/v1/server/fastapi/app/persistence.py:L6328-L6485` |
| `cover_crop_management` | `POST /v1/field-ops/cover-crop-management-events` | `specs/api/v1/server/fastapi/app/main.py:L25732-L25732`, `specs/api/v1/server/fastapi/app/persistence.py:L6487-L6676` |
| `tillage` | `POST /v1/field-ops/tillage-events` | `specs/api/v1/server/fastapi/app/main.py:L26170-L26170`, `specs/api/v1/server/fastapi/app/persistence.py:L6677-L7203` |
| `plant_protection_application` | `POST /v1/field-ops/plant-protection-application-events` | `specs/api/v1/server/fastapi/app/main.py:L27149-L27149`, `specs/api/v1/server/fastapi/app/persistence.py:L7204-L7389` |
| `pesticide_application` | `POST /v1/field-ops/pesticide-application-events` | `specs/api/v1/server/fastapi/app/main.py:L27513-L27513`, `specs/api/v1/server/fastapi/app/persistence.py:L7391-L7525` |
| `irrigation` | `POST /v1/field-ops/irrigation-events` | `specs/api/v1/server/fastapi/app/main.py:L28495-L28787`, `specs/api/v1/server/fastapi/app/persistence.py:L7935-L8097` |
| `harvest` | `POST /v1/field-ops/harvest-events` | `specs/api/v1/server/fastapi/app/main.py:L28790-L28988`, `specs/api/v1/server/fastapi/app/persistence.py:L8099-L8261` |

## 3. Existing Authoritative Compliance Fact Adapters

| Fact surface | Authoritative v1 route | Observed evidence |
| --- | --- | --- |
| Jurisdiction fact attestation | `POST /v1/compliance/jurisdiction-facts` | `specs/api/v1/server/fastapi/app/main.py:L42017-L42257`, `specs/api/v1/server/fastapi/app/persistence.py:L14217-L14405` |
| Conversion timeline | `POST /v1/compliance/conversion-timelines` | `specs/api/v1/server/fastapi/app/main.py:L42260-L42489`, `specs/api/v1/server/fastapi/app/persistence.py:L14407-L14627` |
| Parallel-production control | `POST /v1/compliance/parallel-production-controls` | `specs/api/v1/server/fastapi/app/main.py:L42492-L42766`, `specs/api/v1/server/fastapi/app/persistence.py:L14629-L14832` |
| Seed-sourcing exception | `POST /v1/compliance/seed-sourcing-exceptions` | `specs/api/v1/server/fastapi/app/main.py:L42769-L42960`, `specs/api/v1/server/fastapi/app/persistence.py:L14834-L15106` |

## 4. Implemented Additive API Surfaces

### 4.1 Capability flags

`GET /v1/capabilities` keeps the current `cropContextEnsure` flag and now exposes the additive operation-workbench feature lines proven in runtime, static OpenAPI, and tests:

| Feature flag | Meaning | Status |
| --- | --- | --- |
| `cropContextEnsure` | Explicit crop-context pre-resolution before strict commits. | `implemented` |
| `operationCatalog` | Generic operation-family catalog and adapter metadata for the five covered runtime families: `cover_crop_management`, `harvest`, `mechanical_weeding`, `planting`, and `tillage`. | `implemented` |
| `operationProposals` | Proposal ranking and retrieval surface. | `implemented` |
| `operationDrafts` | Saveable mutable operation drafts. | `implemented` |
| `operationAssessments` | Profile-scoped per-operation assessment reads and refreshes. | `implemented` |
| `operationAttestation` | Client-facing alias for the current attestation and review-workbench slice. | `implemented` |
| `controlCenterReviewQueue` | Client-facing alias for the current review-queue slice. | `implemented` |
| `controlCenterAttestationWorkbench` | Review queue/detail/actions for attestation and report readiness. | `implemented` |

### 4.2 Generic proposal and draft routes

| Route | Purpose | Contract notes |
| --- | --- | --- |
| `GET /v1/operations/catalog` | List governed `OperationCatalog` items. | Read-only registry; current runtime items include `operationFamilyCode`, `label`, `commitRoute`, `supportedProfiles[]`, and `supportedStates[]` for the five implemented generic families only. |
| `POST /v1/operations/proposals` | Create or rank `OperationProposal` items from OCR, operator prompt, or explicit structured input. | Accepts only `operationFamilyCode = cover_crop_management | harvest | mechanical_weeding | planting | tillage` and `sourceKind = ocr | operator_prompt | manual`. Returns ranked proposals. |
| `GET /v1/operations/proposals/{proposalUri}` | Fetch one proposal. | Read-only. |
| `POST /v1/operations/drafts` | Create `OperationDraft`. | Accepts only `operationFamilyCode = cover_crop_management | harvest | mechanical_weeding | planting | tillage`, plus `fieldUri`, optional `cropInstanceUri`, optional `proposalUri`, optional `cropContext`, `draftPayload`, and `draftEvidence[]`. |
| `GET /v1/operations/drafts` | List drafts by `state`, `operationFamilyCode`, or `profileKey`. | Read-only list; returned items still carry fields such as `fieldUri` and `reviewState`. |
| `GET /v1/operations/drafts/{operationDraftUri}` | Fetch one draft. | Read-only item lookup with linked proposal and evidence summary when present. |
| `PATCH /v1/operations/drafts/{operationDraftUri}` | Update mutable draft content before commit. | Incrementally merges `cropContext`, `draftPayload`, and `draftEvidence`, updates `note`, and rejects any patch after commit with `409 draft_already_committed`. |
| `POST /v1/operations/drafts/{operationDraftUri}/commit` | Commit a draft by invoking the mapped event-specific route. | Returns the committed event response, the committed `executedOperationUri`, and the refreshed additive assessment snapshot. |

### 4.3 Assessment routes

| Route | Purpose | Contract notes |
| --- | --- | --- |
| `GET /v1/operations/{executedOperationUri}/assessments` | List profile-scoped assessments for one committed operation. | Supports `profileKey` filter. |
| `POST /v1/operations/{executedOperationUri}/assessments:refresh` | Recompute one or more `OperationComplianceAssessment` records. | Response returns the refreshed assessment plus persistence and report-binding refresh details. |
| `POST /v1/operations/{executedOperationUri}/attestations` | Record an attestation action against an assessment. | Actions currently include `mark_partially_attested`, `mark_attested`, and `reopen`. |

### 4.4 Control Center workbench routes

| Route | Purpose | Contract notes |
| --- | --- | --- |
| `GET /v1/control-center/review-queue` | Queue/list view for review work. | Filters: `profileKey`, `attestationState`, `reportReady`, `operationFamilyCode`, `fieldUri`, `farmUri`. |
| `GET /v1/control-center/review-items/{reviewItemUri}` | Detail view for one review item. | Includes committed operation summary, linked draft/proposal provenance, requirement results, evidence summary, and related compliance record links. |
| `POST /v1/control-center/review-items/{reviewItemUri}/actions` | Execute review actions. | Supports `refresh_assessment`, `attach_operator_attestation`, `mark_partially_attested`, `mark_attested`, `reopen`, `request_evidence`, and `escalate_to_compliance_fact`. |

## 5. Current v1 Draft-Commit Mapping Rules

The currently implemented additive catalog MUST map to existing routes deterministically for the five covered generic families:

| `operationFamilyCode` | Required mapping |
| --- | --- |
| `planting` | Call `POST /v1/field-ops/planting-events` |
| `mechanical_weeding` | Call `POST /v1/field-ops/mechanical-weeding-events` |
| `cover_crop_management` | Call `POST /v1/field-ops/cover-crop-management-events` |
| `tillage` | Call `POST /v1/field-ops/tillage-events` |
| `harvest` | Call `POST /v1/field-ops/harvest-events` |

Additional rules:

1. The adapter MUST preserve current strict route requirements.
2. The adapter MAY call crop-context ensure before commit if the catalog item requires crop-bound context and the draft does not yet contain a usable `cropInstanceUri`.
3. The adapter MUST never write directly to `executed_operation` bypassing the authoritative route.
4. A failed authoritative route commit leaves the draft mutable and uncommitted.
5. Other event-specific families such as `plant_protection_application`, `pesticide_application`, and `irrigation` remain authoritative direct routes today; they are not yet proven generic draft/proposal/assessment families.

## 6. Proposed Persistence Additions

The additive persistence layer SHOULD introduce the following surfaces outside immutable execution facts:

| Surface | Purpose | Write rule |
| --- | --- | --- |
| `operation_draft` | Mutable pre-commit operation content. | Updateable until commit/discard. |
| `operation_draft_evidence_link` | Links draft evidence, including `operator_attestation`. | Updateable until commit/discard. |
| `operation_proposal` | Ranked suggestion records. | Replaceable or supersedable. |
| `operation_compliance_assessment` | Profile-scoped assessment summary per committed operation. | Append-only or supersedable; never mutate execution fact. |
| `operation_compliance_requirement_result` | Requirement-level detail for one assessment. | Same lifecycle as parent assessment. |
| `production_unit_season_slot` | Lightweight planning/logging overlay before full planning or crop-context finalization. | Supersedable overlay only. |
| `control_center_review_item` | Queue/detail read-model backing surface. | Derived or regenerated from assessments and bindings. |

The existing immutable persistence boundary remains:

1. `executed_operation`
2. `executed_operation_evidence`
3. family-specific event tables
4. `jurisdiction_fact_attestation`
5. `conversion_timeline_record`
6. `parallel_production_control_record`
7. `seed_sourcing_exception_record`

## 7. Read-Model Contracts

### 7.1 `ReviewQueueItem`

```json
{
  "reviewItemUri": "urn:review-item:...",
  "farmUri": "urn:farm:...",
  "fieldUri": "urn:field:...",
  "operationFamilyCode": "planting",
  "executedOperationUri": "urn:executed-operation:...",
  "profileKey": "si:organic:crops_only:2026",
  "attestationState": "partially_attested",
  "reportReady": false,
  "missingRequirementCodes": ["seed_exception_or_authorized_seed", "operator_attestation"],
  "linkedEvidenceUris": ["urn:evidence:..."],
  "linkedComplianceRecordUris": ["urn:seed-sourcing-exception:..."],
  "nextActionCode": "request_evidence"
}
```

### 7.2 `ReviewItemDetail`

```json
{
  "reviewItemUri": "urn:review-item:...",
  "proposal": {"proposalUri": "urn:proposal:..."},
  "draft": {"draftUri": "urn:draft:...", "state": "committed"},
  "committedOperation": {"executedOperationUri": "urn:executed-operation:..."},
  "assessment": {"assessmentUri": "urn:assessment:...", "attestationState": "partially_attested"},
  "requirementResults": [],
  "reportBindings": [],
  "auditTrail": []
}
```

## 8. Report-Binding Implications

1. The SI control-pack binder remains committed-fact-first.
2. `OperationComplianceAssessment` adds explanation and readiness state; it does not replace current binder fetches for executed operations, conversion timelines, parallel-production controls, or seed-sourcing exceptions.
3. `report_ready` SHOULD be derivable without mutating binder payload shape.
4. A.5 source-plan semantics remain explicit:
   - `known`
   - `intentional_blank`
   - `fallow`
   - `unsupported`
   - `unknown`
5. Draft or proposal state MUST NOT be read directly by official report renderers.

## 9. Deterministic v1 Flow Mapping

| Generic target flow | Deterministic v1 mapping |
| --- | --- |
| Proposal intake from OCR | `POST /v1/operations/proposals` consumes OCR parse output from `/v1/ai/ocr/parse` |
| Draft save | `POST /v1/operations/drafts` persists mutable content only |
| Missing crop-context fixup | Optional call to `POST /v1/field-ops/crop-contexts/ensure` before commit |
| Immutable commit | `POST /v1/operations/drafts/{draftUri}/commit` calls the mapped `/v1/field-ops/*` route |
| Compliance fact capture | Existing `/v1/compliance/*` routes stay authoritative |
| Assessment refresh | `POST /v1/operations/{executedOperationUri}/assessments:refresh` derives results from committed operation + compliance facts + evidence |
| Review queue | `GET /v1/control-center/review-queue` reads derived assessment and binding state |
| Reporting | Existing binder reads committed operations and compliance records; new assessment state only explains readiness |
