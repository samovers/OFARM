# OFARM ReferenceSnapshot Closure RFC v0.1

Date: 2026-04-17  
Status: accepted post-charter RFC  
Scope: close the machine-contract seam for reference snapshots already required by RC2.1 and the ContextSnapshot closure

---

## 1. Problem statement

RC2.1 and the ContextSnapshot closure already require current interpretation to be explainable against relevant:
- rule/evidence-policy revisions
- reference snapshot versions
- identity revisions

That is directionally correct.
It is not yet machine-closed for reference snapshots inside the active contract set.

Today:
- `ContextSnapshot` records `referenceSnapshotRefs`
- current examples rely on those identifiers
- the active machine layer does not yet define a governed `ReferenceSnapshot` object

This RFC closes that seam with the smallest controlled patch.

---

## 2. Core stance

### 2.1 Thin reference-basis closure
This RFC does not create a full registry subsystem or universal code-list warehouse.
It only creates a first-class contract for the minimum reference basis that materially affects interpretation.

### 2.2 Context remains governed
`ContextSnapshot` remains the governed resolved interpretation posture.
`ReferenceSnapshot` only closes one source-basis family that `ContextSnapshot` may reference.

---

## 3. New contract family created by this RFC

This RFC creates:
- `OFARM_ReferenceSnapshot_schema_v0_1.json`

---

## 4. Contract minimums

A `ReferenceSnapshot` contract must be able to carry at least:
- stable snapshot identifier
- reference class/domain
- issuing authority and jurisdiction where relevant
- canonical version label
- effective interval
- source artifact references
- optional code-binding references

---

## 5. Compatibility rule

Existing `ContextSnapshot` contracts remain valid.
This RFC only requires that package-local `referenceSnapshotRefs` may now land on governed package-local reference snapshots rather than unresolved identifiers.

---

## 6. Out of scope

This RFC does not:
- force every reference system into one registry
- define jurisdiction-specific code content by itself
- redesign pack merge or context governance

---

## 7. Outcome

After this RFC:
- `ContextSnapshot` reference-basis identifiers can land on governed objects
- current-state interpretation is easier to reconstruct across deployments and later audit
