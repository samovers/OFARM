# OFARM Advisory Signal Boundary Candidate v0.1

Date: 2026-04-21  
Status: active supporting implementation artifact  
Scope: placeholder candidate note for an external advisory signal carrier, kept below active-law promotion

---

## 1. Current posture

This lane remains queued.
The executed hostile multiparty fixture waves did not require an `AdvisorySignal` contract to prove the relationship or exchange-boundary seams.

## 2. Why it remains deferred

Current active OFARM law already closes the key safety rule:
- advisory/community/social-origin signals must not silently mutate compliance truth
- any consequential next step must re-enter governed review or a human-gated bridge path

What remains open is only a reusable external signal carrier.
That should stay candidate-only until at least two real integrations converge on the same minimal fields.

## 3. Minimal future field set

If activated later, the candidate should likely carry:
- signal id
- signal kind
- source platform ref
- source actor ref optional
- target scope refs
- observedAt
- recordedAt
- payload ref or compact payload summary
- provenance ref
- confidence posture
- verification status
- moderation status optional
- `nonAuthoritative = true`
- linked investigation refs optional
- notes

## 4. Stop rule

Do not promote this lane while relationship and exchange-boundary execution can still be completed with the current bridge/review law.
