# OFARM PackActivation fixtures v0.1

Date: 2026-04-10  
Status: executable/conformance fixture note  
Scope: baseline activation-set and activation-outcome fixtures for the post-gap closure v0.5 runtime-governance pass

---

## Purpose

These fixtures make the activation seam more executable by covering the smallest high-value cases:
- declared-safe merge activation
- same-precedence hard fail
- governance-required overlap
- compatibility by scope separation

They do **not** claim full pack-conformance closure.
They provide a stable starter set for activation planning and activation-result tooling.

---

## Executable fixtures in this package

### Fixture 1 — orchard activation allowed by declared merge
- requested pack: `pack:orchard:v1`
- active packs: Slovenia + organic baseline
- relevant overlap: `EVIDENCE_POLICY`
- declared merge mode: `STRONGEST_REQUIREMENT`

Expected:
- activation allowed
- compatibility class = `COMPATIBLE_WITH_DECLARED_MERGE`

### Fixture 2 — same-precedence template conflict hard fail
- requested pack collides with an already-active same-precedence template pack
- no declared safe merge path exists

Expected:
- activation denied
- compatibility class = `EXCLUSIVE`
- stable reason code = `PACK_SAME_PRECEDENCE_CONFLICT`

### Fixture 3 — decision-rule overlap requires governance
- same-precedence decision-rule overlap exists
- no safe automatic arbitration is available

Expected:
- activation outcome = `GOVERNANCE_REQUIRED`
- compatibility class = `GOVERNANCE_REQUIRED`

### Fixture 4 — compatibility by scope separation
- a potentially conflicting pack is active elsewhere
- the evaluated PackActivationSet is for a non-colliding scope/time context

Expected:
- activation allowed
- compatibility class = `COMPATIBLE_BY_SCOPE_SEPARATION`

---

## Executable evidence

Executable fixture payloads live under:
- `04_implementation_and_conformance/examples_and_fixtures/ofarm_governance_runtime_fixtures_v0_1/`

Executable results are written to:
- `04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_governance_runtime_closure_results_v0_1.json`
