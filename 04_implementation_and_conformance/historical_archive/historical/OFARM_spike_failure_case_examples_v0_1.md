# OFARM spike failure-case examples v0.1

Date: 2026-04-08  
Status: phase-8 artifact  
Scope: concrete examples of bad implementation paths the spike is designed to expose early

---

## 1. Identity failure
Bad implementation:
- every field boundary change creates a new field identity
- or no field boundary change ever creates a new identity

Why this is bad:
- lineage becomes either fragmented or falsely continuous

---

## 2. Lot failure
Bad implementation:
- shipment reference automatically creates a new lot
- or commingling never creates a new lot

Why this is bad:
- traceability becomes either artificially fragmented or falsely conflated

---

## 3. Query failure
Bad implementation:
- runtime accepts malformed QuerySpecification and silently “best-efforts” it
- alias resolution guesses when stale

Why this is bad:
- query meaning drifts into runtime magic

---

## 4. Pack failure
Bad implementation:
- packs touching same surface merge by ad hoc operator choice
- or merge policy is global rather than surface-specific

Why this is bad:
- behavior becomes irreproducible across deployments

---

## 5. Authority failure
Bad implementation:
- buyer read access implicitly grants write/update
- service provider is assumed to act for farmer without explicit delegation
- AI-prepared action silently becomes approved action

Why this is bad:
- governance collapses into convenience

---

## 6. Materialization failure
Bad implementation:
- current-state cache reused for compliance submission after context change without recomputation
- stale advisory state treated as hard compliance state

Why this is bad:
- governed current state stops being trustworthy

---

## 7. Capability manifest failure
Bad implementation:
- manifest claims a pack or query capability that is not present in the active artifact set
- tooling trusts the claim without consistency checking

Why this is bad:
- self-description turns into marketing instead of runtime contract
