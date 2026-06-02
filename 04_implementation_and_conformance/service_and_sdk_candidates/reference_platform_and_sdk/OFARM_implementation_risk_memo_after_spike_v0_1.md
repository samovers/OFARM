# OFARM implementation risk memo after spike design v0.1

Date: 2026-04-08  
Status: phase-8 baseline artifact  
Scope: risks exposed or sharpened by the reference spike design and harness

---

## 1. Main risk judgment

The spike confirms that the architecture is now concrete enough to exercise.

It also confirms that a few risks remain sharper than others.

These are not “architecture failure” risks anymore.
They are **implementation divergence** risks.

---

## 2. Highest risks

### 2.1 Lot semantics
Still the most dangerous object family.

Why:
- traceability cohort identity
- commercial/shipment references
- transformation and commingling
- claim/certification continuity

Risk:
- implementations drift toward either over-splitting or false continuity

### 2.2 Alias stability
Still a real risk.

Why:
- path aliasing sits between archetype/template evolution and semantic query behavior
- schema fields help, but do not by themselves guarantee stable meaning

Risk:
- queries pass validation but drift semantically over time

### 2.3 Template merge safety
Still high risk.

Why:
- cardinality, typing, terminology bindings, and conditional constraints can interact in subtle ways

Risk:
- “safe merge” is declared too early and runtime behavior diverges

### 2.4 Materialization freshness policy
Still under-formalized.

Why:
- FRESH / STALE / INVALID are now real
- use-class and trigger policy still needs richer operational tuning

Risk:
- teams overuse stale state in high-consequence flows or recompute too aggressively without a governed policy

### 2.5 Capability honesty
Still partly external to schema.

Why:
- a manifest can be valid JSON and still misleading if not checked against active artifact state

Risk:
- partner compatibility based on self-description alone becomes brittle

---

## 3. Medium risks

### 3.1 Action-class growth
The action catalog will likely expand.

Risk:
- uncontrolled growth or inconsistent naming makes policy harder to maintain

### 3.2 Decision-rule merge behavior
The current stance is intentionally conservative.

Risk:
- teams push for shortcuts before decision-module schemas are strong enough

### 3.3 Trace object formalization debt
PackMergeResolutionTrace and AuthorizationDecisionTrace are conceptually required but not yet fully schematized.

Risk:
- trace shape diverges across implementations before formal contracts arrive

---

## 4. What the spike reduces

The spike materially reduces uncertainty in these areas:

- the architecture is no longer only prose
- core schemas validate
- seed fixtures can already drive deterministic outcomes
- the main seams can be exercised together in one vertical slice

That is meaningful progress.

---

## 5. Recommended next move after this phase

Run the final hostile review after gap closure against:
- RC2.1
- the accepted RFC set
- the spike package

Do not do another broad design rewrite first.

---

## 6. Update in v0.4

The v0.4 closure pass partially reduces the earlier trace-object formalization debt by adding machine contracts and validated examples for PackMergeResolutionTrace, AuthorizationDecisionTrace, MaterializationBasis, and MaterializationSnapshot. The larger governance-object, pack-activation, and runtime-boundary contract debt remains open.


---

## 7. Update in v0.5

The v0.5 closure pass partially reduces two of the sharpest remaining implementation-divergence risks:
- **capability honesty** is reduced because manifests can now be checked against a minimal active-artifact-state contract
- **pack-activation formalization debt** is reduced because `PackActivationSet` and pack-activation request/result envelopes now exist as machine contracts with starter executable fixtures

The broader runtime-boundary debt remains open for authority, materialization, query entry, and publication/export seams.
