# OFARM Runtime Authority Depth and Review Fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded authority-depth hardening after the post-amendment drift check, focused on lineage-derived scope inheritance, revocation races, grant supersession, read/write sharing boundaries, and explicit non-human / review decision outcomes

---

## 1. Purpose

These fixtures deepen the authority proof layer without changing OFARM law.

They stay entirely inside `04_implementation_and_conformance/` and exercise central plan-linked seams that remained partial after the earlier runtime-boundary closure:
- `DERIVED_LINEAGE_SCOPES` inheritance
- revocation-race rechecks at final gate time
- delegated-scope narrowing and grant supersession
- read-only sharing that still denies write/assert actions
- explicit machine-allowed low-consequence paths
- explicit review outcomes for AI-assisted and sign/attest attempts

---

## 2. Fixture families

### 2.1 Derived-lineage inheritance
1. parent lot read grant with `DERIVED_LINEAGE_SCOPES` allows a child lot passport read after split/transform continuity
2. the same lineage-derived read grant does **not** silently allow compliance assertion on the child lot

### 2.2 Delegation, narrowing, and revocation
3. an older delegated descendant-scope reporting grant is superseded by a later exact-only narrowed grant
4. a provisional submission allow is rechecked at promotion time and denied after revocation

### 2.3 Sharing boundaries
5. a dossier-scoped advisory sharing grant allows read but denies write/update on the same dossier
6. a revoked dossier sharing grant denies later read even though earlier read was allowed

### 2.4 Non-human and review outcomes
7. a software agent is explicitly allowed to perform a low-consequence live-passport export because governance permits that action class for a machine principal
8. an AI-assisted compliance assertion finalization returns `REQUIRE_HUMAN_APPROVAL`
9. a delegated attestation-sign attempt returns `REQUIRE_REVIEW` because the actor lacks the required signatory authority class

---

## 3. What this wave is trying to prove

This wave is intentionally narrow.

It is trying to move the package from:
- starter allow/deny authority examples
- starter AI-human-approval and software-agent deny examples

toward:
- all scope inheritance modes represented at package level
- explicit grant supersession and revocation-race evidence
- explicit read-only sharing and post-revocation denial on non-passport artifacts
- explicit non-human allow-path evidence where governance really permits it
- explicit review outcomes beyond simple deny/allow binaries

---

## 4. Guardrails

This wave does **not**:
- change the baseline authority model
- change accepted RFCs or machine contracts
- claim deployment-collected authorization telemetry
- claim multi-hop delegation or every action class is now production-proven

It only hardens the runtime-shaped support layer.

---

## 5. Expected conformance effect

The intended package-level effect is:
- `scope-inheritance-mode tests` can close because `DERIVED_LINEAGE_SCOPES` is now represented alongside the earlier `DESCENDANT_SCOPES`, `EXACT_ONLY`, and `NO_INHERIT` cases
- `delegation and revocation tests` become materially stronger through revocation-race and supersession coverage
- `non-human / AI-assisted action tests` can close because the package now contains allow, deny, and require-human-approval families
- `authority action-class decision tests` and `sharing-boundary and no-implicit-access tests` become stronger but may still remain partial
