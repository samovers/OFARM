# OFARM post-hardening hostile review v0.3

Date: 2026-04-19
Status: active supporting implementation artifact
Scope: adversarial review of the refreshed post-hardening package after delivery of the thin active-contract reference harness

Reviewed package:
- active RC2.1 baseline and accepted RFC set
- companion artifacts and policies
- active machine contracts and current draft lanes
- `OFARM_conformance_coverage_matrix_v0_1.md`
- `OFARM_machine_contract_validation_results_v0_18.json`
- `OFARM_Thin_Active_Contract_Reference_Harness_Fixtures_v0_1.md`
- `OFARM_thin_active_contract_reference_harness_results_v0_1.json`
- bridge-promotion readiness and live-evidence gate artifacts
- runtime-surface currentness/linkage/release/live-evidence boundary artifacts
- partner-output governance-boundary and submission-gateway boundary artifacts

---

## 1. Bottom line

**OFARM remains implementation-directed with bounded debt, and the package no longer has an obvious package-internal implementation-proof gap for the current scope.**

A hostile reviewer can still criticize the package, but the strongest remaining criticisms are now mostly about:
- missing real deployment evidence
- optional draft or candidate lanes being misread as active defaults
- promotion gates being bypassed in practice during future pilots

Those are materially smaller criticisms than the earlier package-internal contract and implementation-proof gaps.

---

## 2. Strongest positive findings

### 2.1 Package-internal closure is now both quantitatively legible and implementation-proved at one narrow path
The conformance matrix is still:
- 64 total rows
- 63 covered rows
- 1 partial row
- 0 not-started rows

The remaining partial is named, bounded, and evidence-gated.
The newly delivered thin active-contract reference harness removes the prior criticism that OFARM proved many seams only in isolation.

### 2.2 The thin active-contract reference harness is the right level of proof for this phase
The harness proves one narrow path from semantic event ingress through governed publication of a buyer-facing `PassportView` using only active contracts.
It is narrow on purpose.
That is the correct proof target for this phase.
A hostile reviewer can no longer credibly say that implementers must obviously invent hidden glue just to get one end-to-end path working.

### 2.3 The dangerous runtime seams remain substantially better governed than earlier checkpoints
The current package still has explicit closure or bounded governance posture for:
- event ingress and replay-safe promotion
- generic identity/lifecycle change handling
- advisory bridge handoff constraints
- runtime-surface currentness and release linkage
- live-evidence capture boundaries
- partner-output promotion boundaries
- submission-gateway promotion boundaries

These are still the seams most likely to drift into hidden local implementations if left vague.

---

## 3. Hardest remaining criticisms

### 3.1 Same-standard bridge promotion is still not deployment-proven
The package still does **not** have:
- live field-collected same-standard bridge telemetry
- deployment-produced trace-back linkage
- production approval records

A hostile reviewer is still right to reject any bridge-promotion claim until those three evidence classes exist.

### 3.2 The package can still be oversold if support-layer evidence is treated as live proof
The runtime-surface release lane now has better linkage, traceability, capture posture, and one narrow reference harness.
It still has zero qualifying live deployment evidence.
A hostile reviewer should continue to reject any claim that package-local telemetry, templates, or the thin harness are equivalent to production evidence.

### 3.3 Draft and candidate lanes remain easy to misread if currentness discipline slips
The package is still explicit about keeping these non-default:
- `RuntimeSurfaceContract v0.2`
- `Capability Manifest v0.2`
- partner-output channels beyond `NGSI_LD_PARTNER_EXPORT`
- the submission-gateway equivalent contract candidate

A hostile reviewer should still insist that these stay non-default until the named promotion thresholds are actually met.

---

## 4. Things that no longer look like serious blockers

These no longer look like credible blockers for the current package phase:
- event-family coverage and commit-promotion safety
- non-lot identity/lifecycle closure for the current priority families
- advisory-to-governed-action bridge discipline
- runtime-surface currentness and linkage boundaries
- partner-output governance-boundary clarity
- submission-gateway promotion-boundary clarity
- machine-contract validation depth
- the absence of one thin end-to-end active-contract path

---

## 5. Adversarial recommendation

A hostile but fair reviewer should now conclude:
- do not reopen OFARM architecture
- do not promote same-standard bridges, partner outputs, or filing-boundary candidates prematurely
- do keep using the thin active-contract harness as the minimum implementation reference path
- do collect real deployment evidence before promoting any currently gated lane
- do treat this package as a strong implementation-and-evidence checkpoint rather than as a finished external standard packet

That is the correct adversarial reading of the current bundle.
