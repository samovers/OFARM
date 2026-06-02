# OFARM supplemental construct-family round-trip and live-field evidence fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded Wave 15 same-standard bridge supplemental-family reversible proof plus explicit live-field evidence gate

---

## Purpose

This wave closes the remaining reversible-proof gap that Wave 14 left open for the **supported supplemental construct families** under the ADAPT and ISOXML draft same-standard bridge pairs.

It does **not** fabricate or imply live field-collected production telemetry.

Instead, it does two narrower things:

1. proves reversible round-trip behavior for the currently supported supplemental construct families inside the bounded draft bridge scope
2. adds an explicit gate showing that live field-collected same-standard bridge telemetry is still absent from the package

---

## Success fixtures

### ADAPT supported supplemental families
- quantified input application subset
- equipment configuration reference subset

### ISOXML supported supplemental families
- worker allocation reference subset
- operational summary quantity subset

For each success fixture, the expected path is:

1. import through the existing draft candidate pair
2. normalize into canonical OFARM material
3. export through the draft same-standard bridge surface
4. re-import and verify bounded supplemental-scope equivalence

The expected outcome is:
- reversible for the supported supplemental family
- still limited to draft-surface scope
- still honest about disclosed divergence

---

## Blocked conflict fixtures

### ADAPT blocked supplemental family
- nested vendor-private quantified-input extension blocks

### ISOXML blocked supplemental family
- timezone-ambiguous worker-summary aggregates

The expected outcome is:
- reversible claim denied
- raw evidence retained or review forced
- blocked family remains outside declared reversible scope

---

## Live-field evidence gate

The package now also evaluates an explicit live-field evidence gate for both bridge pairs.

Expected outcome:
- no live field-collected same-standard bridge telemetry artifact is found in the package-local search scope
- promotion readiness stays blocked for that reason, even after supplemental-family round-trip proof is added

This gate is intentionally conservative:
- executor telemetry does not count as live field telemetry
- partner sample replay does not count as live field telemetry
- redacted deployment-intake samples do not count as live field telemetry

---

## Expected package effect

After this wave, the bridge promotion blocker should narrow from:

- no supplemental-family round-trip proof
- no live field telemetry
- no production promotion approval

to:

- no live field telemetry
- no production promotion approval

Both bridge surfaces still remain `DRAFT`.
