# OFARM Agronomic Carrier Field Canonicalization and Temporal Conformance RFC v0.1

Date: 2026-05-14  
Status: accepted RFC extension  
Change class: RFC extension + conformance implication  
Baseline impact: no direct RC2.1 baseline edit until later harmonisation

## 1. Purpose

AGR-P2 through AGR-P7 added strong agronomic carrier semantics. Some carriers still expose generic and agronomic-specific reference fields that can be confused in implementation. This RFC defines canonical field precedence and adds temporal conformance expectations.

## 2. Canonical agronomic reference fields

For agronomic carriers, the canonical fields are:

- `agronomicIdentityBindingRefs` for agronomic identity bindings;
- `agronomicCodeBindingProfileRef` for agronomic code-binding profile governance.

The generic fields remain compatibility fields:

- `identityBindingRefs`
- `codeBindingProfileRef`

## 3. Compatibility rule

If only compatibility fields are present, the record may remain schema-valid but semantic conformance should emit a compatibility warning for high-consequence agronomic use.

If both canonical and compatibility fields are present, their values must be equivalent. If they conflict, the record must require review or fail closed depending on consequence level.

New examples should prefer canonical agronomic fields.

## 4. Temporal conformance rule

High-consequence agronomic records must preserve distinct time meanings. In particular:

- observation/phenomenon time is not report time;
- intended time is not execution time;
- captured time is not accepted execution time;
- assertion time is not occurrence time;
- review/correction/dispute time is not original event time;
- materialization/output time is not canonical event time.

## 5. Conformance fixtures

The semantic integrity runner must include positive and negative fixtures for:

- canonical-only carrier refs;
- compatibility-only carrier refs with warning;
- conflicting carrier refs with expected fail/review;
- delayed sync preserving separate timestamps;
- collapsed timestamps failing semantic conformance.

## 6. Non-claims

This RFC does not remove compatibility fields, does not change the truth model, and does not make current-state projections canonical truth.

---

## Baseline harmonisation note — ONT-SEMINT v0.3

On 2026-05-14, this RFC's supported closure was harmonised into the active RC2.1 baseline by ONT-SEMINT v0.3. The harmonisation is narrow: it incorporates the RFC's semantic-integrity rule into baseline posture while preserving all RFC non-claims around production readiness, live external registry verification, legal advice, external-standard readiness, livestock scope, and any profile-specific limitations.
