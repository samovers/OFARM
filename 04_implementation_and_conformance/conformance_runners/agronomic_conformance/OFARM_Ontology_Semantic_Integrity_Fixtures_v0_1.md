# OFARM Ontology Semantic Integrity Fixtures v0.1

Date: 2026-05-14  
Status: active supporting implementation/conformance  
Role: executable package-local checks for ONT-SEMINT v0.1

## Scope

The fixture set in `OFARM_ontology_semantic_integrity_fixtures_v0_1.json` checks the no-regret semantic-integrity amendments:

- package-local `ReferenceSnapshot` references resolve;
- agronomic carrier compatibility fields do not conflict with canonical agronomic fields;
- delayed-sync and execution carriers do not collapse all temporal semantics into one timestamp;
- high-consequence approved queries use version-pinned aliases;
- known negative cases fail for semantic reasons even when the base schema may allow them.

## Expected posture

The runner may report compatibility warnings. Warnings are acceptable when they identify old generic fields or unverified external registry posture. Unresolved package-local reference snapshots, conflicting carrier refs, and unpinned high-consequence aliases must not pass silently.
