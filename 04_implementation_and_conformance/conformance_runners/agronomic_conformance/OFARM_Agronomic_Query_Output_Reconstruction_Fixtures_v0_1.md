# OFARM Agronomic Query / Output Reconstruction Fixtures v0.1

Status: Active supporting implementation and conformance material  
Date: 2026-05-13  
Phase: AGR-P6

## Purpose

These fixtures prove that the agronomic carriers added in AGR-P2 through AGR-P5 can be reconstructed through existing OFARM query and output surfaces without creating a second current-state truth store or a new report ontology.

## Fixture scope

The fixture set covers all ten AGR-P1 scenario records:

1. latest scouting observation reconstruction;
2. treatment history by partial extent;
3. offline contractor late-sync reconstruction;
4. prescribed versus applied rate and failed extent;
5. mixed crop-cycle PassportView disclosure;
6. measurement sampling/method/evidence posture reconstruction;
7. unresolved product identity reconstruction;
8. wet grain/storage evidence placeholder through measurement evidence;
9. stale materialization pre-output refusal;
10. alias/code/evidence drift reconstruction.

## Expected behavior

- `QuerySpecification` declares the agronomic reconstruction target and pinned aliases.
- `QueryPlanIR` declares whether governed current-state reuse is allowed and whether trace-back is required.
- `QueryExecutionResult` refuses stale high-consequence materialization.
- `PassportViewMetadata` remains live and recomputable.
- `DocumentAssemblyMetadata` freezes a versioned basis and can include late/disputed material as an annex.
- `AgronomicReconstructionTrace` explains which checks passed or refused output.

## Non-goals

These fixtures do not define a public query syntax, a UI report model, or a runtime engine. They create machine-checkable reconstruction pressure for the active contracts.
