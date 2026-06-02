# OFARM agronomic baseline harmonisation fixtures v0.1

Date: 2026-05-13  
Status: active supporting implementation/conformance artifact  
Scope: executable fixture expectations for AGR-P7 baseline harmonisation

---

## 1. Purpose

AGR-P7 verifies that the active baseline reflects the already-accepted agronomic RFC and machine-contract closures from AGR-P2 through AGR-P6 without creating a second truth model.

This fixture family is intentionally narrow. It checks baseline harmonisation, not production runtime execution.

## 2. Required fixture expectations

| Fixture | Expected result | Evidence target |
|---|---:|---|
| Active baseline has AGR-P7 phase marker | PASS | Constitution, Platform, Alignment Register |
| Crop-only release boundary is explicit | PASS | Constitution §1.2a |
| Carrier-shell law exists in baseline | PASS | Constitution §3.8 and related truth-boundary sections |
| All AGR-P2 through AGR-P6 carriers are named in model law | PASS | Constitution and Platform |
| All AGR-P2 through AGR-P6 carriers are alignment-registered | PASS | Alignment Register |
| Normative agronomic RFC references are present | PASS | Constitution normative support list |
| Preservation rules remain explicit | PASS | Constitution truth, no-shortcut, output, and materialization sections |
| Readiness posture is updated but bounded | PASS | readiness gate memo |
| Hostile review posture is updated but bounded | PASS | final hostile review |

## 3. Non-goals

This fixture family does not prove:

- full production runtime execution
- field-pilot readiness
- external-standard readiness
- live registry correctness
- wire-level ADAPT, ISOXML, EFDI, ISOBUS, or controller-file interoperability
- crop-specific or jurisdiction-specific pack sufficiency

Those remain implementation and conformance work after baseline harmonisation.

## 4. Boundary assertions

AGR-P7 must preserve:

- assertion/history-first canonical truth
- governed current-state materialization
- Advisory Twin versus Compliance Twin separation
- explicit authority, evidence, review, and promotion gates
- external standards as anchors, bindings, exchange mappings, runtime surfaces, or attestation wrappers rather than hidden OFARM law
- pack non-mutation of core meaning
- PassportView versus DocumentAssembly separation
