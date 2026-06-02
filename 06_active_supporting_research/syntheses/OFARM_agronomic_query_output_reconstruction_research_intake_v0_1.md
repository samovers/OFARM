# OFARM Agronomic Query / Output Reconstruction Research Intake v0.1

Status: Active supporting research intake  
Date: 2026-05-13

## Source

This intake records the Phase AGR-P6 use of `deep-research-report-21.md`.

## Applied recommendations

The report recommended extending QuerySpecification rather than adding a new report ontology, with explicit reconstruction controls for effective-as-of time, knowledge cut, truth scope, promotion, evidence floor, freshness, geometry, late evidence, disputes, and code profile. Phase AGR-P6 implements this through `AgronomicReconstructionPolicy` and additive references from existing query/output contracts.

The report also recommended preserving PassportView as a live projection of accepted or profile-permitted facts and DocumentAssembly as the frozen, versioned output surface that can include annexes. Phase AGR-P6 implements that distinction through metadata examples and reconstruction traces.

## Non-applied recommendations

This phase does not import AIM, O&M JSON, ISOXML, EFDI, ADAPT, or vendor controller formats as normative OFARM truth stores. Those remain exchange or reference surfaces under the active external standards integration policy.
