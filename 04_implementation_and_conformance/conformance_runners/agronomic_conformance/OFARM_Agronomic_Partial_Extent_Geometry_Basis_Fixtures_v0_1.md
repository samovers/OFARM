
# OFARM agronomic partial extent and geometry-basis fixtures v0.1

Date: 2026-05-13  
Status: active supporting implementation artifact  
Scope: Phase AGR-P4 conformance fixtures for PartialExtent, geometry basis, partial treatment, failed pass, disputed geometry, and partial replant current-state invalidation

---

## 1. Authority boundary

These fixtures support the accepted `OFARM_Partial_Extent_and_Geometry_Basis_RFC_v0_1.md` and the active `OFARM_PartialExtent_schema_v0_1.json` contract.

They do not change the RC2.1 baseline. They also do not turn geometry evidence into truth by itself.

## 2. Fixture objectives

The fixture set proves these rules:

1. An observed patch may support advisory reasoning but must not become whole-field truth.
2. A prescription/treatment area remains intent until execution evidence and review exist.
3. A failed machine pass is retained as evidence and exception context, not accepted execution.
4. An accepted treated slice may drive materialization only for that sub-extent and declared purpose.
5. A disputed operator sketch remains parallel evidence and cannot overwrite accepted geometry without review.
6. A partial replant extent may support crop-cycle lineage while remaining event-bound geometry.
7. Prior whole-field materialization must be refused or recomputed after partial replant creates mixed crop-cycle or variety status.

## 3. Active contract family

- `03_machine_contracts/schemas/agronomic/OFARM_PartialExtent_schema_v0_1.json`

Positive examples:

- `OFARM_PartialExtent_example_field_17_west_edge_weed_patch_observed_v0_1.json`
- `OFARM_PartialExtent_example_field_17_spot_spray_treatment_area_v0_1.json`
- `OFARM_PartialExtent_example_field_17_failed_pass_machine_logged_v0_1.json`
- `OFARM_PartialExtent_example_field_17_accepted_treated_slice_v0_1.json`
- `OFARM_PartialExtent_example_field_17_operator_sketch_disputed_geometry_v0_1.json`
- `OFARM_PartialExtent_example_field_17_west_zone_replant_area_v0_1.json`

Bridge examples:

- observation context to PartialExtent
- prescription intent to PartialExtent
- machine failed-pass execution record to PartialExtent
- accepted execution record to PartialExtent
- identity lifecycle partial replant to PartialExtent
- materialization refusal after partial replant

## 4. Expected behavior

### 4.1 Observed patch

Expected: retained as observation-support geometry. It may support advisory planning. It must not create treatment truth or a durable management zone.

### 4.2 Treatment area

Expected: retained as intent-support geometry. It may constrain prescription/planning. It must not prove application.

### 4.3 Failed pass

Expected: retained as machine evidence. It may help split accepted and failed sub-extents. It must not become accepted execution by import alone.

### 4.4 Accepted treated slice

Expected: may support accepted execution for the reviewed sub-extent only. It must not overwrite the whole field.

### 4.5 Disputed geometry

Expected: retained as parallel dispute evidence. It must not collapse into a single exact area unless a review decision says so.

### 4.6 Partial replant

Expected: supports child crop-cycle lineage for the replant area. It does not automatically create a durable field or zone identity. It invalidates stale whole-field current-state reuse for high-consequence output.

## 5. Runner

Run:

```bash
python 04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_partial_extent_geometry_basis_runner_v0_1.py
```

Expected result: `PASS`.
