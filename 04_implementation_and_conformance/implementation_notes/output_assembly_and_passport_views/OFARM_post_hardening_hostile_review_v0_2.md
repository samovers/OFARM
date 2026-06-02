# OFARM post-hardening hostile review v0.2

Date: 2026-04-19
Status: active supporting implementation artifact
Scope: adversarial review of the refreshed post-hardening package after the hostile-integrator continuation and runtime-surface governance-boundary waves through v0.18 validation

Reviewed package:
- active RC2.1 baseline and accepted RFC set
- companion artifacts and policies
- active machine contracts and current draft lanes
- `OFARM_conformance_coverage_matrix_v0_1.md`
- `OFARM_machine_contract_validation_results_v0_18.json`
- bridge-promotion readiness and live-evidence gate artifacts
- runtime-surface currentness/linkage/release/live-evidence boundary artifacts
- partner-output governance-boundary and submission-gateway boundary artifacts

---

## 1. Bottom line

**OFARM remains implementation-directed with bounded debt, and the package no longer has an obvious package-internal semantic seam that justifies architecture reopening.**

A hostile reviewer can still criticize the package, but the strongest remaining criticisms are now mostly about:
- missing real deployment evidence
- optional draft or candidate lanes being misread as active defaults
- the absence of one thin end-to-end reference harness built only from active contracts

Those are materially smaller criticisms than the earlier “law exists but no executable object exists” gaps.

---

## 2. Strongest positive findings

### 2.1 Package-internal closure is now quantitatively legible and nearly complete
The conformance matrix is now:
- 64 total rows
- 63 covered rows
- 1 partial row
- 0 not-started rows

That matters.
The remaining partial is named, bounded, and evidence-gated.
There is no longer a vague backlog of hidden closure debt.

### 2.2 The current checkpoint is much stronger than the older post-hardening packet
The current validation suite is `PASS` at:
- 60 schema validations
- 204 positive example validations
- 60 negative mutation checks
- 385 package-local reference checks
- 20 injected broken-reference failures

A hostile reviewer can still ask for deployment proof, but it is no longer credible to say the package is only prose-coherent.

### 2.3 The dangerous runtime seams are now substantially better governed
The refreshed package now has explicit closure or bounded governance posture for:
- event ingress and replay-safe promotion
- generic identity/lifecycle change handling
- advisory bridge handoff constraints
- runtime-surface currentness and release linkage
- live-evidence capture boundaries
- partner-output promotion boundaries
- submission-gateway promotion boundaries

These are precisely the seams most likely to drift into hidden local implementations if left vague.

---

## 3. Hardest remaining criticisms

### 3.1 Same-standard bridge promotion is still not deployment-proven
The package has good internal proof and a disciplined evidence gate.
It still does **not** have:
- live field-collected same-standard bridge telemetry
- deployment-produced trace-back linkage
- production approval records

A hostile reviewer is right to reject any promotion claim until those three evidence classes exist.

### 3.2 The package can still be oversold if support-layer evidence is treated as live proof
The runtime-surface release lane now has better linkage, traceability, and capture posture.
It still has zero qualifying live deployment evidence.
A hostile reviewer should continue to reject any claim that package-local telemetry or templates are equivalent to production evidence.

### 3.3 Draft and candidate lanes remain easy to misread if currentness discipline slips
The package is now explicit about keeping these non-default:
- `RuntimeSurfaceContract v0.2`
- `Capability Manifest v0.2`
- partner-output channels beyond `NGSI_LD_PARTNER_EXPORT`
- the submission-gateway equivalent contract candidate

A hostile reviewer should insist that these stay non-default until the named promotion thresholds are actually met.

### 3.4 The package still proves many seams separately rather than through one thin reference harness
This is no longer a semantic-law blocker.
It is now an implementation-proof gap.
A hostile reviewer can still ask for one narrow end-to-end active-contract flow to show that implementers will not need hidden glue logic.

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

---

## 5. Adversarial recommendation

A hostile but fair reviewer should now conclude:
- do not reopen OFARM architecture
- do not promote same-standard bridges, partner outputs, or filing-boundary candidates prematurely
- do build one thin active-contract reference harness
- do collect real deployment evidence before promoting any currently gated lane
- do treat this package as a strong implementation-and-evidence checkpoint rather than as a finished external standard packet

That is the correct adversarial reading of the current bundle.
