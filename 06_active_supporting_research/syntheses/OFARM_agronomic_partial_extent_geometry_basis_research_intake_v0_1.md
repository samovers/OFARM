
# OFARM agronomic partial extent and geometry-basis research intake v0.1

Date: 2026-05-13  
Status: active supporting research intake  
Scope: intake summary for the user-supplied Deep Research report used to activate Phase AGR-P4 partial extent and geometry-basis closure

---

## 1. Source

This intake summarizes the user-supplied `deep-research-report-21.md` received for the agronomic amendment lane.

The report is supporting research. It informs this amendment but does not override the active baseline by itself.

## 2. Research conclusions used in Phase AGR-P4

The report recommends `PartialExtent` as one of the small OFARM-owned carrier shells needed for real crop operations.

For Phase AGR-P4, the actionable conclusions are:

- partial spatial slices must carry geometry basis and quality
- sampled areas, treatment areas, failed passes, re-treatment areas, replant areas, damage areas, and disputed geometries must be distinguishable
- event-bound extents should not automatically become durable `Field`, `Zone`, or `ManagementZone` identities
- geometry needs temporal applicability as well as coordinate or representation context
- machine polygons, operator sketches, GNSS tracks, remote-sensing extents, and ISOXML/EFDI/ADAPT geometry surfaces are evidence or exchange surfaces, not truth stores
- stale whole-field materialization must be refused or recomputed when partial replant creates mixed crop-cycle or variety status

## 3. Phase AGR-P4 application

Phase AGR-P4 applies the research by creating:

- `02_accepted_rfcs/OFARM_Partial_Extent_and_Geometry_Basis_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_PartialExtent_schema_v0_1.json`
- positive examples for observed patch, treatment area, failed pass, accepted treated slice, disputed geometry, and partial replant area
- bridge examples into observation, intervention intent, execution/as-applied, identity/lifecycle, and materialization records
- a dedicated Phase AGR-P4 runner and result record

No active baseline law text is changed in this phase.

## 4. Deferred research conclusions

The report also recommends work for:

- agronomic code-binding profile
- query/output reconstruction policy
- later baseline harmonisation

Those remain follow-on work under `IMP-307`, `IMP-309`, and `IMP-311`.
