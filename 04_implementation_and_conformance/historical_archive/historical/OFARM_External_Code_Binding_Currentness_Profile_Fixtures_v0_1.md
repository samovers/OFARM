# OFARM External Code-Binding Currentness Profile Fixtures v0.1

Date: 2026-05-14  
Status: active supporting implementation/conformance  
Amendment line: ONT-SEMINT v0.2 / Phase 4

## Purpose

These fixtures close the narrow Phase 4 currentness-profile work for Belgian crop-protection product authorisation identity.

The fixtures use the supporting research report:

`06_active_supporting_research/syntheses/OFARM_external_code_binding_currentness_profile_crop_protection_BE_research_report_v0_1.md`

## Fixtures added

- `OFARM_ExternalRegistryVerificationTrace_schema_v0_1.json`
- Belgium Phytoweb ReferenceSnapshot examples
- Belgium crop-protection authorisation currentness profile example
- Belgian product authorisation verified identity binding
- GTIN-only and EU-active-substance-only negative posture identity bindings
- ExternalRegistryVerificationTrace PASS / REVIEW_REQUIRED / REFUSE_OUTPUT examples

## Required behavior

A high-consequence current-compliance PassportView under this profile may pass only when:

1. the product identity binds to Belgian Phytoweb authorisation by authorisation number or equivalent official permit identifier;
2. a ReferenceSnapshot exists for the jurisdictional source;
3. ExternalRegistryVerificationTrace records the exact lookup surface, query inputs, candidate count, selected ID, observed status/date context, registry availability, discrepancies, and final outcome;
4. required label/certificate evidence is correlated when label-level output is claimed;
5. EU active-substance and GS1 commercial identifiers remain supporting context only.

## Negative posture

The runner must treat these as not eligible for high-consequence current-compliance PassportView pass:

- free-text product name only;
- GTIN only;
- EU active-substance-only evidence;
- stale or missing access date;
- wrong jurisdiction;
- missing ReferenceSnapshot;
- registry unavailable at output time;
- prescription/as-applied product identity mismatch.

## Non-claims

These fixtures are package-local conformance evidence. They do not claim live registry integration, legal advice, production readiness, or external-standard readiness.
