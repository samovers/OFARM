# OFARM Ontology Semantic Integrity Amendment Summary v0.1

Date: 2026-05-14  
Status: active supporting implementation/conformance  
Amendment line: ONT-SEMINT v0.1

## Outcome

The package now includes a controlled semantic-integrity amendment line for the Ontology Steward review findings.

Added active substance:

- `01_companion_artifacts/OFARM_Concept_Boundary_Map_v0_1.md`
- `01_companion_artifacts/OFARM_Temporal_Field_Conformance_Matrix_v0_1.md`
- `02_accepted_rfcs/OFARM_Reference_Resolution_and_Semantic_Conformance_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Agronomic_Carrier_Field_Canonicalization_and_Temporal_Conformance_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_High_Consequence_Query_and_Output_Gate_Hardening_RFC_v0_1.md`
- `03_machine_contracts/schemas/runtime_surface/OFARM_ReferenceResolutionManifest_schema_v0_1.json`
- `03_machine_contracts/schemas/identity_lifecycle/OFARM_ReferenceResolutionFinding_schema_v0_1.json`
- `03_machine_contracts/schemas/identity_lifecycle/OFARM_ReferenceResolutionReport_schema_v0_1.json`
- `03_machine_contracts/schemas/core/OFARM_TemporalFieldConformanceMatrix_schema_v0_1.json`

Added supporting implementation/conformance:

- amendment ledger;
- authority-status lint runner and result;
- package-local reference-resolution runner and result;
- ontology semantic-integrity fixture set, runner, and result;
- refreshed machine-contract validation runner/results v0.21.

## Concrete closure

The amendment normalizes package-local crop-protection `ReferenceSnapshot` references from `reference-snapshot:si:crop-protection:2026-04-01` to `reference-snapshot:crop-protection:si:2026-04-01` and adds the missing example `ReferenceSnapshot` for crop-stage/weed-code references.

Package-local `ReferenceSnapshot` resolution now reports:

- 39 refs checked;
- 39 resolved package-local refs;
- 0 unresolved package-local refs;
- overall `PASS`.

Semantic integrity now reports:

- authority lint `PASS`;
- reference resolution `PASS`;
- carrier conflict checks `PASS_WITH_WARNINGS` because four existing examples still use compatibility fields;
- high-consequence unpinned alias negative case caught;
- timestamp-collapse negative case caught;
- overall `PASS_WITH_WARNINGS`.

## Warnings retained intentionally

Compatibility warnings remain for existing examples using `identityBindingRefs` / `codeBindingProfileRef` instead of canonical `agronomicIdentityBindingRefs` / `agronomicCodeBindingProfileRef`.

Those examples are not silently treated as failures because the RFC keeps compatibility fields during transition. New examples should prefer canonical agronomic fields.

## Deferred work

External live registry/currentness verification remains deferred. The Deep Research prompt is available at:

`05_project_handoff_and_prompts/prompts/OFARM_External_Code_Binding_Currentness_Deep_Research_Prompt_v0_1.md`

The active RC2.1 baseline has not yet been harmonized for ONT-SEMINT. Baseline harmonization should occur only after external-profile research and additional break-test depth are complete.

## ONT-SEMINT v0.2 Phase 4/5 continuation

The attached Deep Research report was ingested as active supporting research and used to close Phase 4 narrowly around a Belgium/Phytoweb crop-protection product authorisation currentness profile.

Added support:

- accepted RFC extension: `OFARM_External_Code_Binding_Currentness_and_Verification_RFC_v0_1.md`
- machine contract: `OFARM_ExternalRegistryVerificationTrace_schema_v0_1.json`
- Belgium ReferenceSnapshot examples
- Belgium AgronomicCodeBindingProfile example
- positive and negative-posture AgronomicIdentityBinding examples
- ExternalRegistryVerificationTrace PASS / REVIEW_REQUIRED / REFUSE_OUTPUT examples
- external currentness profile runner/results
- operational break-test suite runner/results

No active RC2.1 baseline files were amended. No live Phytoweb integration, legal advice, production readiness, or external-standard readiness is claimed.

## ONT-SEMINT v0.2 validation closure

Phase 4 is closed at package-local profile/conformance level. Phase 5 is closed for the five operational break-test scenarios in the suite.

Validation after v0.2 additions:

- external code-binding currentness runner: `PASS`
- operational break-test suite runner: `PASS`
- authority-status lint: `PASS`
- package-local reference resolution: `PASS`
- ontology semantic-integrity runner: `PASS`
- machine-contract validation runner v0.22: `PASS`

The earlier compatibility-field warnings have been cleared by adding canonical agronomic reference fields to the transition examples while retaining compatibility fields for backwards-readable examples.

At ONT-SEMINT v0.1 this was intentionally not started; ONT-SEMINT v0.3 has now completed Phase 6 baseline harmonisation.

