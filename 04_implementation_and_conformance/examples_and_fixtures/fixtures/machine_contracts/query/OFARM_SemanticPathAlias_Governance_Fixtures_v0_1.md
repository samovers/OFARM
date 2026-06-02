# OFARM SemanticPathAlias governance fixtures v0.1

Date: 2026-04-11  
Status: active machine-contract fixture note  
Scope: starter executable fixtures for alias governance and query reproducibility

---

## Included fixtures

### 1. Active version-pinned alias resolution
- Query: `OFARM_QuerySpecification_example_field_passport_v0_1.json`
- Catalog: `OFARM_SemanticPathAliasCatalog_example_core_profile_v0_1.json`
- Trace: `OFARM_SemanticPathAliasResolutionTrace_example_field_passport_active_v0_1.json`

Expected posture:
- direct resolution
- no warning
- canonical alias version preserved exactly

### 2. Deprecated alias rollover with explicit canonical successor
- Query: `OFARM_QuerySpecification_example_field_passport_legacy_alias_v0_1.json`
- Catalog: `OFARM_SemanticPathAliasCatalog_example_core_profile_v0_1.json`
- Trace: `OFARM_SemanticPathAliasResolutionTrace_example_field_passport_deprecated_rollover_v0_1.json`

Expected posture:
- deprecated alias accepted only through explicit trace
- warning retained
- canonical alias version visible

### 3. Ambiguity hard-fail for unpinned alias
- Query: `OFARM_QuerySpecification_example_field_passport_unpinned_alias_v0_1.json`
- Catalog: `OFARM_SemanticPathAliasCatalog_example_conflict_cropstage_v0_1.json`
- Trace: `OFARM_SemanticPathAliasResolutionTrace_example_field_passport_ambiguous_fail_v0_1.json`

Expected posture:
- no guessed resolution
- candidate alias versions enumerated
- high-consequence posture fails clearly

### 4. Cross-target QueryPlanIR equivalence starter case
- Plans:
  - `OFARM_QueryPlanIR_example_field_passport_v0_1.json`
  - `OFARM_QueryPlanIR_example_field_passport_search_target_v0_1.json`

Expected posture:
- same `sourceQuerySpecificationId`
- same normalized target
- same canonical resolved alias meaning
- different execution-target strategy allowed
