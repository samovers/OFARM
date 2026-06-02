# OFARM Interoperability Mapping Coverage, Loss, and Runtime Surface RFC v0.1

Date: 2026-04-10  
Status: accepted RFC extension  
Scope: formalize mapping coverage/loss artifacts, formalize runtime surface contracts, and extend pack merge law for interoperability surfaces

---

## 1. Problem statement

RC2.1 and the Platform baseline already say that OFARM supports import/export mappings and interoperability tooling.
That is architecturally correct.
It is not yet explicit enough for safe standard-readiness work.

The remaining gap is:
- mappings exist as a named artifact family, but their coverage and loss posture is not formalized
- runtime API/event/query/discovery surfaces exist in practice, but there is no explicit artifact contract for them
- pack merge law covers many semantic/configuration surfaces, but not the interoperability surfaces most likely to proliferate during standard-readiness work
- ingest from external formats can easily drift into silent auto-promotion unless the promotion posture is attached to the mapping contract itself

This RFC closes that gap.

---

## 2. Core stance

### 2.1 Mappings are integration surfaces, not truth
Import/export mappings remain interoperability surfaces.
They are not canonical OFARM truth.
They must resolve back to the canonical substrate and its governed promotion path.

### 2.2 Every mapping needs coverage and loss disclosure
A mapping module alone is not enough.
Each governed mapping surface should publish:
- a `MappingCoverageStatement`
- a `LossMap`

That makes interoperability claims explicit and testable.

### 2.3 Default ingest posture remains conservative
External payload ingest should normally land as:
- draft material
- `operation claim`
- `observation assertion`
- `evidence record`

Stronger promotion requires separate governed policy.
External-format presence alone is not evidence of accepted OFARM truth.

### 2.4 Runtime surfaces are governed contracts
Partner-facing APIs, event surfaces, query façades, and discovery documents should be representable as `RuntimeSurfaceContract` artifacts.

This keeps the boundary explicit between:
- the constitutional model
- the runtime surface used for integration
- the service-description documents that describe that surface

### 2.5 Merge law must cover interoperability surfaces
This RFC introduces two additional surface families for pack merge law:
- `IMPORT_EXPORT_MAPPING`
- `RUNTIME_SURFACE_CONTRACT`

Without them, external-standard-readiness work would add a large ungoverned seam to pack activation.

---

## 3. Formal artifacts produced by this RFC

This RFC defines:
- **OFARM MappingCoverageStatement schema v0.1** (`ofarm.mappingcoveragestatement.v0.1`)
- **OFARM LossMap schema v0.1** (`ofarm.lossmap.v0.1`)
- **OFARM RuntimeSurfaceContract schema v0.1** (`ofarm.runtimesurfacecontract.v0.1`)
- matching examples for bridge/mapping/runtime-surface scenarios

---

## 4. MappingCoverageStatement schema decisions

### 4.1 Mandatory top-level fields
A valid `MappingCoverageStatement` should include at minimum:
- `schemaVersion`
- `statementId`
- `mappingModuleRef`
- `direction`
- `externalStandardRef`
- `coveredConstructs`
- `promotionPosture`
- `roundTripExpectation`
- `lossMapRef`

### 4.2 Covered, dropped, and approximated constructs
The statement should make four categories explicit:
- what external constructs are covered
- what external constructs are dropped
- what external constructs are approximated
- what OFARM concepts are required but have no source in the external payload

This is the minimum honesty required for real interoperability.

### 4.3 Promotion posture
The mapping statement should declare the default ingest/export promotion posture.

This is where OFARM says, in executable form, that an inbound payload usually creates claims/evidence first rather than accepted truth.

---

## 5. LossMap schema decisions

A `LossMap` records the known semantic and operational loss posture for a mapping surface.

Each loss item should identify at minimum:
- the affected external construct
- the loss class
- the impact level
- the downstream risk statement
- whether governance is required for high-consequence use

Loss disclosure is not a defect in itself.
Undisclosed loss is the defect.

---

## 6. RuntimeSurfaceContract schema decisions

A valid `RuntimeSurfaceContract` should identify at minimum:
- the surface kind
- the direction
- the protocol family
- the target standard or documentation basis
- the semantic-preservation posture

Optional references may include:
- mapping modules
- service-description documents
- discovery documents

This keeps runtime surface documentation attached to governed artifacts without turning OFARM into an API-first standard.

---

## 7. Surface-family merge semantics

### 7.1 IMPORT_EXPORT_MAPPING

#### Safe cases
Use **ADDITIVE_UNION** when:
- mappings target disjoint external standards, or
- mappings target disjoint construct subsets under the same standard and direction, and
- the runtime can keep coverage/loss trace distinct

Use **IDENTICAL_ONLY** when:
- two packs reference the same mapping surface and the effective mapping, coverage statement, and loss posture are materially identical

Use **ORDERED_COMPOSITION** only when:
- the mapping stages are explicitly governed
- stage order is semantically meaningful and preserved
- each stage publishes its own coverage/loss posture
- the composed result remains explainable end to end

#### Unsafe cases
Use **HARD_FAIL** when:
- the same external construct is mapped to incompatible OFARM targets for the same direction and scope
- two mappings imply incompatible promotion postures for the same ingest path
- loss posture is materially different but undeclared as a governed alternative
- the runtime cannot explain which mapping path actually governed the result

### 7.2 RUNTIME_SURFACE_CONTRACT

#### Safe cases
Use **ADDITIVE_UNION** when:
- surfaces are disjoint by endpoint/path/topic/resource/query façade namespace, or
- discovery entries are distinct and non-contradictory

Use **IDENTICAL_ONLY** when:
- two packs declare the same runtime surface and the contract is materially identical in the meaning-bearing parts

#### Unsafe cases
Use **HARD_FAIL** when:
- the same endpoint/topic/query façade is declared with conflicting meaning-bearing behavior
- the same discovery entry resolves to conflicting manifest/surface targets
- the same surface implies conflicting mapping or authority behavior
- the runtime cannot prove which surface contract is in force

---

## 8. Minimum conformance expectations

A deployment claiming mapping or runtime-surface support should be able to show at minimum:
- schema validation for `MappingCoverageStatement`, `LossMap`, and `RuntimeSurfaceContract`
- consistency between mapping module refs and the coverage/loss artifacts that reference them
- ingest-promotion-path tests for declared import surfaces
- conflict-handling tests for mapping/runtime-surface overlaps
- manifest-to-surface-reference consistency where those surfaces are advertised

---

## 9. Main patch consequences

If promoted, this RFC implies:
- a Constitution patch adding interoperability surface families
- a Pack Safety Policy patch adding those family names
- a Platform patch requiring coverage/loss/runtime-surface references where interoperability is declared
- no change to OFARM’s truth model

---

## 10. Hard stop question

Should OFARM claim support for a mapping or runtime surface if it cannot publish coverage, loss, and contract posture in governed artifacts?

This RFC’s answer is **no**.
