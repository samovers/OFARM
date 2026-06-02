
# OFARM External Standard Readiness Fixtures v0.1

Date: 2026-04-10  
Status: example/conformance fixture set  
Scope: fixture relationships for the horizontal external-standard-readiness contracts promoted after the research review

---

## Fixture family 1 — semantic substrate grounding

Artifacts:
- `OFARM_SemanticSubstrateBundle_schema_v0_1.json`
- `OFARM_SemanticSubstrateBundle_example_core_profile_v0_1.json`

Expected:
- bundle validates
- semantic anchors are version-pinned
- validation backbones are explicit
- exchange bindings remain separate from semantic anchors

---

## Fixture family 2 — mapping coverage and loss disclosure

Artifacts:
- `OFARM_MappingCoverageStatement_example_adapt_import_v0_1.json`
- `OFARM_MappingCoverageStatement_example_isoxml_import_v0_1.json`
- `OFARM_MappingCoverageStatement_example_ngsi_ld_export_v0_1.json`
- matching `OFARM_LossMap_example_*.json`

Expected:
- every mapping coverage statement has a matching `LossMap`
- every `LossMap` points back to the matching mapping coverage statement
- ingest promotion posture stays conservative by default

---

## Fixture family 3 — runtime surface contracts

Artifacts:
- `OFARM_RuntimeSurfaceContract_example_ngsi_ld_export_v0_1.json`
- `OFARM_RuntimeSurfaceContract_example_capability_discovery_v0_1.json`
- `OFARM_RuntimeSurfaceContract_example_cql2_query_facade_v0_1.json`

Expected:
- runtime surfaces validate as governed contracts
- surface references declared by mappings or manifests resolve to a known contract where required
- discovery and query façades remain boundary surfaces rather than constitutional law

---

## Fixture family 4 — claim-set and manifest-by-reference grounding

Artifacts:
- `OFARM_ConformanceClaimSet_example_core_deployment_v0_1.json`
- `OFARM_ConformanceClaimSet_example_partner_deployment_v0_1.json`
- `OFARM_Capability_Manifest_schema_v0_2_draft.json`
- `OFARM_Capability_Manifest_example_core_deployment_v0_2_draft.json`

Expected:
- the v0.2 draft manifest stays narrow by reference
- manifest references to substrate bundle, claim set, mapping coverage, loss maps, and runtime surfaces resolve consistently
- conformance claims remain traceable to active artifact state and named evidence/test suites
