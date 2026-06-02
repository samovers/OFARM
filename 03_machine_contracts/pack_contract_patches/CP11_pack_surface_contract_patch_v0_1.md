# CP11 pack-contract surface patch v0.1 — boundary repair

Status: draft/non-default patch. This file is not active pack law until formally merged into the pack-contract currentness map.

Executable draft patch schemas are now included in:

```text
03_machine_contracts/drafts_non_default/pack_contract_patches/
  OFARM_CP11_PackSurfaceDeclaration_schema_v0_1.json
  OFARM_CP11_PackMergeResolutionTraceExtension_schema_v0_1.json
  OFARM_CP11_PackActivationSetSustainabilityExtension_schema_v0_1.json
```

The CP11 sustainability surface families are:

```text
SUSTAINABILITY_CONSTRAINT
SUSTAINABILITY_OBJECTIVE
SUSTAINABILITY_OBJECTIVE_PRIORITY
SUSTAINABILITY_TRADEOFF_POLICY
SUSTAINABILITY_EVIDENCE_POLICY
SUSTAINABILITY_METRIC_PROFILE
SUSTAINABILITY_CLAIM_RULE
CHARTER_EXCEPTION_POLICY
CHARTER_BREACH_POLICY
```

Boundary rules:

- CP11 sustainability pack surfaces may not weaken core meaning.
- CP11 sustainability pack surfaces may not create authority.
- Conflicting CP11 sustainability pack surfaces must `HARD_FAIL` or `REQUIRE_GOVERNANCE`.
- These schemas patch pack-surface declaration and merge trace shape only; they do not replace general pack law.
