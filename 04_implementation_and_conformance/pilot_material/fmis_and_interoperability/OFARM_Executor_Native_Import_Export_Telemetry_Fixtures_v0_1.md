# OFARM executor-native import/export telemetry fixtures v0.1

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: scenario fixtures for runner-produced import/export telemetry that is generated from execution logic rather than replayed gate declarations

---

## 1. Purpose

These fixtures push OFARM one step past the Wave 9 replay-shaped import/export path logs.

They do **not** add new law or new machine-contract substance.
They add a package-local execution runner that:
- binds declared import/export scenarios to existing machine-contract examples
- validates the referenced machine-contract artifacts
- emits telemetry records from executor logic rather than from prewritten gate-log fixtures
- links those emitted telemetry runs back to declared round-trip records and output trace-back records where the package already has them

This wave therefore improves proof depth in `04_implementation_and_conformance/` without changing the active baseline or accepted RFC layer.

---

## 2. Scenario families

### 2.1 Import executor scenarios
- `adapt_import_executor_native.json`
- `isoxml_import_executor_native.json`

These prove that inbound standard payloads can be executed through a normalization runner that:
- resolves mapping coverage and loss posture
- emits claim/evidence-first commit posture
- routes accepted consequences through review rather than auto-promotion

### 2.2 Live export surface scenario
- `ngsi_ld_live_passport_export_executor_native.json`

This proves that the NGSI-LD surface can be executed as:
- a live projection-only export path
- a passport-family output boundary
- a traceable outward route linked to existing mapping and trace-back artifacts

### 2.3 Frozen output adapter scenarios
- `field_dossier_package_executor_native.json`
- `submission_filing_executor_native.json`
- `submission_invalid_materialization_executor_native.json`

These prove that output-family adapters can emit or refuse file/package actions based on:
- document-family metadata
- evidence sufficiency posture
- materialization state and freshness
- the existing passport-vs-document boundary rules

---

## 3. What this wave is and is not

This wave **is**:
- stronger than replaying a pre-authored gate sequence
- package-executable
- linked to existing machine-contract examples and Wave 9 mapping/trace-back artifacts

This wave is **not yet**:
- deployment-collected telemetry from a running OFARM runtime
- proof of same-standard reversible bridge-pack round trips
- proof of broad partner-specific export families beyond the current starter paths

---

## 4. Expected outcomes

The runner should emit executor-side telemetry showing that:
- ADAPT and ISOXML ingest remain draft/claim/evidence-first
- NGSI-LD export remains projection-only and passport-family
- dossier packaging remains frozen document-family only
- submission filing succeeds only when evidence, authority, and fresh current-state posture line up
- submission filing stops when materialization is invalid under the active context
