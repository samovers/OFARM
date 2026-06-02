# OFARM Authority Source Record Closure RFC v0.1

Date: 2026-04-17  
Status: accepted post-charter RFC  
Scope: close the machine-contract seam for authority-source records already required by RC2.1 and the Authority Policy Model RFC

---

## 1. Problem statement

RC2.1, the authority companion policy, and the Authority Policy Model RFC already depend on:
- `RoleAssignment`
- `AuthorityGrant`
- `DelegationGrant`
- `SharingGrant`
- `RevocationDecision`

That is directionally correct.
It is not yet machine-closed inside the active contract set.

Today:
- `AuthorizationDecisionTrace` records role/grant/delegation/sharing basis as identifiers
- revocation outcome is recorded, but source-object closure is weak
- current examples rely on these objects
- the active machine layer does not yet define them as first-class contract families

This RFC closes that seam with the smallest controlled patch.

---

## 2. Core stance

### 2.1 Boundary envelopes stay narrow
`AuthorizationDecisionRequest`, `AuthorizationDecisionResult`, and `AuthorizationDecisionTrace` remain the boundary envelopes.
This RFC only closes the source-object references behind them.

### 2.2 Source authority remains explicit and separate
Role, authority, delegation, sharing, and revocation remain distinct.
Nothing in this RFC allows sharing to silently become write/review/sign authority.

### 2.3 Minimum fields only
The contracts created here must carry only the minimum machine-verifiable fields needed for:
- who held or granted authority
- what action/scope/time envelope was covered
- inheritance mode
- purpose/conditions where relevant
- prospective revocation lineage

This RFC does **not** create a giant role matrix or policy engine inside the contracts.

---

## 3. New contract families created by this RFC

This RFC creates these active machine-contract families in `03_machine_contracts/`:
- `OFARM_RoleAssignment_schema_v0_1.json`
- `OFARM_AuthorityGrant_schema_v0_1.json`
- `OFARM_DelegationGrant_schema_v0_1.json`
- `OFARM_SharingGrant_schema_v0_1.json`
- `OFARM_RevocationDecision_schema_v0_1.json`

---

## 4. Contract minimums

### 4.1 RoleAssignment minimums
A `RoleAssignment` contract must be able to carry at least:
- stable assignment identifier
- party reference
- role type
- anchor scope
- validity interval

### 4.2 AuthorityGrant minimums
An `AuthorityGrant` contract must be able to carry at least:
- stable grant identifier
- grantor and grant-target references
- governed action classes and/or authority families
- target scope
- validity interval
- inheritance mode
- optional purpose, conditions, or limits
- grant state

### 4.3 DelegationGrant minimums
A `DelegationGrant` contract must be able to carry at least:
- stable delegation identifier
- delegating and delegate party references
- governed action classes and/or authority families
- target scope
- validity interval
- inheritance mode
- optional purpose, conditions, required evidence, or limits
- delegation state

### 4.4 SharingGrant minimums
A `SharingGrant` contract must be able to carry at least:
- stable sharing identifier
- grantor and grantee references
- shared artifact family/reference
- target scope
- validity interval
- permitted delivery/use posture
- optional purpose or limits
- sharing state

### 4.5 RevocationDecision minimums
A `RevocationDecision` contract must be able to carry at least:
- stable revocation identifier
- target artifact family/reference being ended or narrowed
- deciding party
- decision/effective time
- revocation mode
- affected scope and action classes where relevant

---

## 5. Compatibility rule

Existing authorization boundary envelopes remain valid.
This RFC only requires that package-local examples may now point to governed authority-source objects rather than leaving those identifiers unresolved.

`AuthorizationDecisionTrace` may carry optional `revocationDecisionRefs` to strengthen traceability without breaking older examples.

---

## 6. Out of scope

This RFC does not:
- replace the Authority Action Matrix
- create tenant-specific policy code
- make delegation broader than source authority
- relax human-only defaults for high-governance actions

---

## 7. Outcome

After this RFC:
- authorization traces can land on governed role/grant/delegation/sharing/revocation records
- contractor and revocation disputes can cross the authority-source seam without bare identifier dependence
- revocation remains prospective and traceable rather than implicit
