# OFARM Agronomic Query and Output Reconstruction RFC v0.1

Status: Accepted RFC extension; active substance unless overridden by the active baseline or a later accepted RFC.  
Date: 2026-05-13  
Phase: AGR-P6 agronomic query and output reconstruction closure  
Change class: RFC extension, machine-contract patch, and conformance expansion

## 1. Purpose

This RFC closes the agronomic reconstruction gap at query/output level. Earlier agronomic phases added carrier shells for observation and measurement context, intervention/as-applied payload, partial extent, and code binding. This phase makes those carriers reconstructable through OFARM's existing `QuerySpecification`, `QueryPlanIR`, `QueryExecutionRequest`, `QueryExecutionResult`, `PassportViewMetadata`, and `DocumentAssemblyMetadata` surfaces.

The closure is intentionally narrow. OFARM does not add a new report ontology or a second agronomic current-state model. It adds reusable reconstruction policy and trace shells plus additive references from existing query/output contracts.

## 2. Authority and non-goals

This RFC is active only as an accepted RFC extension. It does not edit `00_active_baseline/` text in this phase. Baseline harmonisation remains a later phase after the agronomic amendment line is stable.

This RFC must not be read to:

- let projections, saved query results, PassportView output, or current-state materialisations become canonical truth;
- let advisory outputs or AI-generated recommendations become compliance truth;
- let stale current state drive high-consequence agronomic output;
- merge recommendation, prescription, plan, claim, as-applied evidence, accepted consequence, correction, and dispute into a single CRUD row;
- create a new report-object family for agronomic output;
- allow unresolved product, unit, geometry, threshold, or evidence bindings to appear as accepted compliance facts.

## 3. Reconstruction policy controls

High-consequence agronomic queries and outputs must declare or inherit a reconstruction policy that covers at least:

- effective-as-of semantics;
- knowledge-cut semantics;
- promotion policy;
- truth scope;
- evidence floor;
- freshness and materialization policy;
- geometry policy;
- late-evidence policy;
- dispute policy;
- code-binding profile;
- output disclosure policy.

The policy is represented by `AgronomicReconstructionPolicy`.

## 4. Reconstruction trace controls

High-consequence agronomic query results and compiled-output inputs should produce an `AgronomicReconstructionTrace`. The trace records which checks passed, required review, or refused output. The trace is an explanation and audit reconstruction surface. It is not canonical truth.

## 5. Query rules

`QuerySpecification` and `QueryPlanIR` may reference `reconstructionPolicyRef`.

For high-consequence agronomic use:

- aliases must be version-pinned;
- current-state reuse must satisfy freshness policy or fail closed;
- the code profile must be explicit;
- geometry basis and quality must be available when a partial extent affects the answer;
- unresolved disputes must stay queryable in history, but not silently enter PassportView truth;
- late evidence must support dual reconstruction or successor output rather than edit-in-place.

## 6. Output rules

`PassportViewMetadata` and `DocumentAssemblyMetadata` may reference reconstruction policy and trace artifacts.

PassportView remains live and recomputable. By default, agronomic PassportView output uses accepted consequences only and must refuse high-consequence output when materialization, evidence, code binding, or geometry policy is not satisfied.

DocumentAssembly remains frozen, versioned, and basis-bearing. It may include unresolved mappings, disputed geometries, raw source payloads, late evidence, and advisory reasoning as annexes when the reconstruction policy permits them. Inclusion in a document annex does not make an item accepted truth.

## 7. Machine contracts introduced or patched

This RFC introduces:

- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicReconstructionPolicy_schema_v0_1.json`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicReconstructionTrace_schema_v0_1.json`

This RFC additively patches these active schemas with optional reconstruction references:

- `OFARM_QuerySpecification_schema_v0_1.json`
- `OFARM_QueryPlanIR_schema_v0_1.json`
- `OFARM_QueryExecutionRequest_schema_v0_1.json`
- `OFARM_QueryExecutionResult_schema_v0_1.json`
- `OFARM_PassportViewMetadata_schema_v0_1.json`
- `OFARM_DocumentAssemblyMetadata_schema_v0_1.json`

The optional fields do not weaken existing required fields.

## 8. Conformance expectations

Phase AGR-P6 fixtures must prove:

- agronomic query aliases are pinned and governed;
- treatment history can reconstruct accepted product, rate, extent, and evidence posture;
- observation-to-decision reconstruction preserves observation, threshold, and advisory/compliance separation;
- measurement reconstruction exposes sampling/method/evidence posture;
- stale materialization refuses high-consequence PassportView input;
- PassportView remains live and accepted-only by default;
- DocumentAssembly can freeze a dual reconstruction with annexed disputed or late evidence;
- query results retain projection traceback readiness.

## 9. Relationship to earlier agronomic phases

This RFC depends on:

- `OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md`
- `OFARM_Quantity_Bearing_Intervention_and_As_Applied_RFC_v0_1.md`
- `OFARM_Partial_Extent_and_Geometry_Basis_RFC_v0_1.md`
- `OFARM_Agronomic_Code_Binding_and_Standards_Profile_RFC_v0_1.md`

It prepares the later baseline-harmonisation phase. It does not itself change the baseline text.
