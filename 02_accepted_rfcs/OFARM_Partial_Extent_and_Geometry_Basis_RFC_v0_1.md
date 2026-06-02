
# OFARM Partial Extent and Geometry Basis RFC v0.1

Date: 2026-05-13  
Status: accepted post-charter RFC  
Scope: close the smallest active carrier gap for sampled, treatment, failed-pass, replant, damage, and disputed sub-field extents without turning OFARM into a GIS topology engine or weakening identity/lifecycle law

---

## 1. Problem statement

OFARM now has active carriers for agronomic observation/measurement context and for quantity-bearing intervention/as-applied payloads. Those carriers can name partial areas, but they still need a first-class, evidence-bearing way to say **what spatial slice is meant, how it was derived, how good the geometry is, and whether it is only event-bound or a durable identity candidate**.

Real crop operations routinely produce sub-field extents:

- scouting patches
- sampled areas
- treatment areas
- failed passes
- re-treatment areas
- replant areas
- damage areas
- disputed operator and machine geometries

If OFARM treats those as whole-field facts, it creates false agronomic truth. If it turns every slice into a durable `Field` or `ManagementZone`, it creates identity sprawl. This RFC closes that middle seam.

## 2. Core stance

### 2.1 PartialExtent is a carrier, not a truth shortcut

`PartialExtent` records the geometry basis and quality of a spatial slice. It does not itself create accepted execution, compliance truth, or current state.

Promotion still depends on OFARM assertion/history, evidence sufficiency, review, authority, accepted-consequence, identity/lifecycle, and materialization law.

### 2.2 PartialExtent is not automatically a durable identity

A treatment area, sampled area, failed pass, damage polygon, or disputed sketch is usually **event-bound**.

It becomes a durable OFARM identity only when existing identity/lifecycle rules decide that the slice will be reused independently across later assertions, obligations, or documents.

### 2.3 Geometry precision must be explicit

Every `PartialExtent` must carry:

- parent scope
- temporal applicability
- geometry basis
- coordinate reference system or explicit non-spatial basis
- quality/precision statement
- evidence references
- durable-identity policy
- promotion boundary

A numeric polygon is not automatically exact. A machine path is not automatically accepted truth. An operator sketch is not automatically wrong. Disputed geometries remain reconstructable until review resolves or preserves the dispute.

### 2.4 External geometry and machinery formats stay exchange surfaces

GeoSPARQL, OWL-Time, O&M sampling concepts, ADAPT geometry surfaces, ISOXML task/timelog geometry, EFDI flows, controller paths, remote-sensing outputs, and GNSS tracks may inform or carry geometry evidence.

They do not become OFARM canonical truth stores.

---

## 3. New active contract family

This RFC creates:

- `03_machine_contracts/schemas/agronomic/OFARM_PartialExtent_schema_v0_1.json`

The contract supports these extent roles:

- `SAMPLED_AREA`
- `OBSERVED_PATCH`
- `TREATMENT_AREA`
- `FAILED_PASS`
- `RETREATMENT_AREA`
- `REPLANT_AREA`
- `DAMAGE_AREA`
- `DISPUTED_GEOMETRY`
- `OPERATIONAL_PASS`
- `OTHER`

## 4. Required semantics

A `PartialExtent` must identify:

- `partialExtentId`
- `extentRole`
- `extentState`
- `anchorScope`
- `parentScope`
- `temporalApplicability`
- `geometryBasis`
- `qualityStatement`
- `durableIdentityPolicy`
- `evidenceRefs`
- `promotionBoundary`

## 5. Durable identity rule

`durableIdentityPolicy.createsDurableIdentity` defaults by example to false for event-bound slices.

If `createsDurableIdentity` is true, the schema requires a `durableIdentityRef`.

If a partial replant or split creates a child crop-cycle or other durable relationship, that is represented by the existing identity/lifecycle machinery. The `PartialExtent` may reference the identity-lifecycle change, but the geometry record alone does not mint the identity.

## 6. Promotion and materialization behavior

A partial extent may support materialization only for its declared purpose and only when the surrounding accepted consequence, evidence sufficiency, and materialization rules permit it.

Default unsafe shortcuts remain blocked:

- partial extent as whole-field truth
- machine polygon as automatic accepted execution
- disputed sketch as exact reporting area
- treatment area as durable zone by default
- stale whole-field current state after partial replant
- PassportView hiding mixed or disputed spatial state

## 7. Bridge behavior

Existing active carriers should reference `PartialExtent` through existing reference fields where possible:

- `AgronomicObservationContext.spatialContext.partialExtentRef`
- `InterventionIntentPayload.targetExtentRef`
- `ExecutionRecordPayload.executionExtent.extentRef`
- `ExecutionRecordPayload.executionExtent.scopeExtentBasisRef`
- `IdentityLifecycleChange.evidenceRefs` or decision evidence where a partial extent supports lineage
- `MaterializationResult.problems.relatedRefs` when partial extent changes invalidate or stale prior current state

No baseline law is rewritten in this phase.

## 8. Conformance expectations

Phase AGR-P4 introduces fixtures and runner checks proving that:

- observed patches can support advice without becoming treatment truth
- treatment extents remain intent until execution evidence and review exist
- failed passes remain event-bound evidence
- accepted treatment consequences are limited to accepted sub-extents
- disputed geometries remain parallel and reconstructable
- partial replant invalidates unsafe whole-field current-state reuse

## 9. Non-goals

This RFC does not:

- define a full GIS topology model
- replace GeoSPARQL, ADAPT, ISOXML, or EFDI
- create a public OFARM geometry query language
- change Field, Zone, CropCycle, or Lot identity law
- let geometry imports bypass evidence or promotion gates
- require every partial extent to become a durable identity

## 10. Affected artifacts

New active artifacts:

- `03_machine_contracts/schemas/agronomic/OFARM_PartialExtent_schema_v0_1.json`
- PartialExtent examples in `03_machine_contracts/`

Supporting implementation artifacts:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Partial_Extent_Geometry_Basis_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_partial_extent_geometry_basis_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_partial_extent_geometry_basis_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_partial_extent_geometry_basis_results_v0_1.json`
