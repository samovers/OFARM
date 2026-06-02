# OFARM Agronomic Code Binding Profile Research Intake v0.1

Status: Active supporting research intake. Research informs further development but does not override active baseline law.
Date: 2026-05-13
Source: `deep-research-report-21.md`, uploaded 2026-05-12.
Phase: AGR-P5

## Intake decision

The user-supplied Deep Research report is accepted as supporting context for the Phase AGR-P5 code-binding and standards-profile closure. It is not promoted into baseline law.

## Research findings used

The report recommends a small OFARM carrier approach: small carrier, external code binding, governed promotion. It identifies `AgronomicIdentityBinding` as the shell for binding local OFARM subjects to external schemes and registries without importing whole ontologies.

The report also recommends a role map for external standards: semantic anchors, code bindings, exchange mappings, runtime surfaces, attestation wrappers, and not-recommended dependencies.

Phase AGR-P5 converts those recommendations into the accepted RFC, two machine contracts, examples, and a conformance runner.

## Standards and registries treated as bindings or surfaces

- EPPO Codes: crop, pest, weed, disease, and target-organism code binding where available.
- BBCH: crop-stage code binding.
- QUDT: quantity-kind semantic anchor.
- UCUM: unit-code binding.
- SKOS: concept-scheme and mapping-discipline anchor.
- AGROVOC and Crop Ontology: optional crosswalk/method/trait code-binding support.
- UPOV/PLUTO and CPVO: variety registry lookup surfaces.
- GS1: commercial product and batch/lot code binding.
- EU/national PPP registries: runtime lookup surfaces for product authorisation.
- OECD seed schemes: seed-lot attestation wrapper.

## Constraints carried forward

- External standards do not become OFARM law.
- Free-text labels remain evidence until scheme-bound.
- GTIN alone is not sufficient crop-protection regulatory identity.
- Fertilizer blend, seed lot, PPP product, and irrigation water source identity semantics remain distinct.
- Packs constrain bindings and mappings; they do not mutate core meaning.
- Query/output reconstruction remains pending for Phase AGR-P6.
