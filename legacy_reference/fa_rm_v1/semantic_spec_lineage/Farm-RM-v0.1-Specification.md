# Farm-RM v1 Specification

## 1. Purpose and Audience

Farm-RM v1 defines a semantic data model for interoperable farm applications.

It is designed for:
- Farm management software (small and large farms)
- Field register apps
- Sensor and telematics APIs
- Compliance and subsidy workflows
- Analytics and AI-assisted planning

This specification is inspired by openEHR's architecture pattern (Reference Model + Archetypes + Templates), but simplified for practical agriculture.

## 2. Design Goals (Normative)

Farm-RM v1 MUST support:
1. End-to-end farm management and compliance.
2. Separation of intent and reality (`PlannedOperation` vs `ExecutedOperation`).
3. Append-only audit history.
4. URI-first, cross-system identity.
5. Organic-first compliance priority.
6. Multi-tenant permissions and offline-capable execution.
7. Interoperability with workflow, telematics, IoT, and traceability standards.

Farm-RM v1 SHOULD reduce the following operational pains:
- Compliance time burden
- Compliance penalty risk
- Manual re-entry
- Task assignment friction
- Reconciliation time across harvest/storage/delivery/invoice

## 3. Scope

### 3.1 In scope (v1)
- Crop operations planning and execution
- Compliance evidence and submission support
- Organic / in-transition / conventional production states
- Slovenia profile (normative)
- Serbia profile (draft)
- Finance-ready links (without full finance domain model)

### 3.2 Out of scope (v1)
- Full variable-rate zone model (planned v2)
- Full financial/accounting ontology (extension module)
- US regulatory profile (planned v3)

## 4. Architecture Pattern

Farm-RM v1 adopts five layers:

1. **Reference Model (RM)**
A stable core of classes, identifiers, relationships, and lifecycle rules.

2. **Archetypes**
Reusable, machine-validated operation definitions (e.g. pre-emergence spray).

3. **Templates**
Context bundles for use cases (e.g. "Slovenia organic cereal season").

4. **Profiles**
Jurisdiction and production-mode constraints (EU/SI/RS; organic/in-transition/conventional).

5. **Execution Bindings**
Links to external engines and standards (BPMN, SensorThings, ISO telematics, EPCIS).

## 5. Core Concepts (Reference Model)

### 5.1 Entity groups

**A. Organization and land**
- `Farm`
- `Field`
- `ParcelBlock`
- `GERK` (Slovenia profile)

**B. Crop lifecycle**
- `CropInstance`
- `ProductionStatus` (`organic_certified`, `in_conversion`, `conventional`)

**C. Plans and execution**
- `OperationTemplate`
- `PlannedOperation`
- `ExecutedOperation`
- `TimeWindow`
- `Constraint`

**D. Resources and traceability**
- `Resource` (with `Machine`, `Worker`, `InputMaterial` subtypes)
- `MaterialLot`
- `StorageLot`

**E. Observations and evidence**
- `Observation`
- `SensorObservation`
- `DerivedObservation`
- `EvidenceRecord` (mandatory for every executed operation)

**F. Compliance and control**
- `ComplianceSubmission`
- `InspectionCase`
- `CertificationScope`
- `ControlBody`
- `NonConformity`
- `CorrectiveAction`

**G. Governance and audit**
- `RuleSet`
- `RuleExecutionTrace` (optional/conditional)
- `EventRecord` (append-only event log)

### 5.2 Intent vs reality (mandatory pattern)

- Plans are represented by `PlannedOperation`.
- Real-world activity is represented by `ExecutedOperation`.
- If execution was ad-hoc, `ExecutedOperation` MAY omit a `realizesPlannedOperation` link.
- Every `ExecutedOperation` MUST have at least one `EvidenceRecord`.

### 5.3 URI-first identity (mandatory)

Every primary business object MUST have:
- Global URI (`uri`)
- Local system identifier (`localId`, optional)
- Jurisdiction code (`jurisdiction`, where relevant)

Canonical URI format (recommended):

`https://data.<org-domain>/farm-rm/v1/{type}/{jurisdiction}/{id}`

## 6. Lifecycle and Versioning

### 6.1 Append-only model (mandatory)

Business events are immutable once committed.
Corrections MUST be represented as new events linked with `supersedes`.
Physical delete of compliance-relevant records MUST NOT be used.

### 6.2 Rule validity windows (mandatory)

All rule sets and profile constraints MUST support:
- `effectiveFrom`
- `effectiveTo` (optional)
- `jurisdiction`
- `legalReference`

### 6.3 Plan revisions

Replanning MUST create explicit revision links:
- `PlanRevision` relationships from old plan to replacement plan
- `changeReason` (e.g. weather, labor, machine failure)

## 7. Compliance by Design

### 7.1 Minimum compliance-complete season record (v1)

A season is considered compliance-complete when at least the following exist:

1. Farm/operator identity and role assignments.
2. Field/parcel identifiers and area.
3. Crop instances with production status.
4. Planned and executed operations.
5. Input product references and lot/batch links.
6. Observations used for decisions (raw and/or derived).
7. Evidence for every executed operation.
8. Compliance submissions and inspection links (if applicable).
9. Append-only event log with timestamps and actor metadata.

### 7.2 Organic-first precedence (mandatory)

When multiple rules apply, engines MUST apply this order:
1. Organic rules
2. In-transition rules
3. Conventional rules

### 7.3 Manual-first claims, then validation (mandatory)

User-entered compliance claims are allowed.
Systems MUST validate these claims against available events, evidence, and rule sets.

## 8. Rule Model

### 8.1 Constraint expression

Every machine-checkable constraint MUST include:
- `constraintType`
- `expressionLanguage` (e.g. JSONLogic, FEEL, SHACL-SPARQL)
- `expression`
- `severity` (`hard`, `soft`)

### 8.2 Rule execution trace

`RuleExecutionTrace` is optional overall but REQUIRED when:
- A hard rule fails.
- A compliance decision is disputed.
- An inspector/auditor requests proof.

Trace SHOULD include:
- `ruleUri`
- `inputSnapshotRef`
- `result`
- `explanation`
- `timestamp`
- `engineVersion`

## 9. Profiles

### 9.1 Production mode profiles
- `OrganicPrimaryProfile` (default strict profile)
- `InTransitionProfile`
- `ConventionalProfile`

### 9.2 Jurisdiction profiles
- `SloveniaV1Profile` (normative)
- `SerbiaV1DraftProfile` (draft)

### 9.3 Mixed farm support

A farm MAY operate mixed statuses in one season, but segregation and traceability rules MUST be met for claims.

## 10. Interoperability Bindings

Farm-RM v1 SHOULD expose mapping adapters for:
- ISO 11783 and AEMP telematics events -> `ExecutedOperation`, `Resource`, `Observation`
- OGC SensorThings -> `SensorObservation`
- GS1 EPCIS -> `MaterialLot`, `StorageLot`, traceability events
- BPMN task instances -> `PlannedOperation` / `ExecutedOperation`

## 11. Security, Tenancy, and Offline

### 11.1 Multi-tenant

Model MUST support:
- Farm-scoped ownership
- Contractor-limited access
- Role-based permissions with validity intervals

### 11.2 Offline-first

Systems SHOULD support local capture with delayed sync.
Conflicts MUST resolve via append-only merge semantics and provenance.

## 12. Finance-Ready Core

Core model is not a full finance model but MUST support stable linking fields:
- `commercialReference` on operations/lots
- `deliveryReference`
- `invoiceReference`
- `paymentReference`

Finance extension module MAY define full entities later without breaking core URIs.

## 13. Conformance

### 13.1 Conformance levels

- **L1 Core**: RM entities + URI-first + append-only.
- **L2 Compliance**: Evidence-per-execution + profile validation.
- **L3 Interop**: At least two external mapping adapters.
- **L4 Auditable AI**: AI-assisted rule generation with traceable validations.

### 13.2 Mandatory v1 checks

A v1-conformant implementation MUST pass:
1. SHACL core shape validation.
2. Executed-operation evidence cardinality check.
3. Production profile precedence test.
4. Immutable history test (no destructive changes).

## 14. Non-Technical Reading Guide

For non-technical stakeholders, Farm-RM v1 means:
1. Work is planned once, executed once, and reused everywhere.
2. Compliance documents come from normal work records, not extra typing.
3. Organic farms get strict defaults automatically.
4. Inspectors can trace what happened, who did it, and why.
5. Different apps can exchange farm data with less manual re-entry.

## 15. Roadmap

- **v1**: Serbia + Slovenia + EU baseline, organic-first, core compliance.
- **v2**: Full EU profile coverage, sub-field zones, variable rate.
- **v3**: US profile, FSMA-aligned traceability profile, extended commerce mappings.
