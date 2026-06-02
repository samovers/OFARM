# OFARM Durable Relationship Semantics RFC v0.1

Date: 2026-04-21  
Status: accepted post-charter RFC  
Scope: close the durable legal-operational relationship seam for recurring multiparty farm-network realities without reopening OFARM’s constitutional authority model

---

## 1. Problem statement

The active baseline, authority companion policy, Authority Policy Model RFC, and Authority Source Record Closure RFC already get the explicit authority layer right.
That direction remains correct.
It should not be replaced.

What remains open is a narrower seam:

Today OFARM lacks a first-class machine-visible way to represent persistent legal-operational relationships such as:
- owner / tenant / operator
- beneficial owner / operational steward
- cooperative member / cooperative admin
- employer / worker / supervisor
- contractor / customer
- advisor-of-record
- pooled responsibility
- linkage from farm truth or outputs to an external contract or commitment

At present those semantics can only be inferred from:
- free-text role labels
- free-text purposes or conditions
- or external documents that the machine layer does not understand

That is too weak for implementation, conformance, and dispute handling.
It invites hidden business logic and makes revocation/accountability harder to trace.

This RFC closes that seam with the smallest controlled patch.
It does **not**:
- replace `RoleAssignment`
- replace `AuthorityGrant`
- replace `DelegationGrant`
- replace `SharingGrant`
- create a new permission system
- create ERP / CRM / HR / order-management semantics inside OFARM

---

## 2. Core stance

### 2.1 Relationship artifacts are basis/context, not permission

A durable relationship artifact may represent a persistent legal-operational relationship among parties and scopes.

It may be used as:
- evidence or justification for later grants
- an auditable contextual fact
- a conformance precondition
- a runtime policy-check input

It is **not** permission by itself.

### 2.2 Roles and grants remain separate

- `RoleAssignment` still answers **who this party is in context**.
- `AuthorityGrant` still answers **what this party or role may do**.
- `DelegationGrant` still answers **who may act on behalf of whom**.
- `SharingGrant` still answers **who may receive or view OFARM artifacts**.
- `RevocationDecision` still governs prospective narrowing of future power.

Nothing in this RFC allows a durable relationship to silently create any of those objects.

### 2.3 Small typed family set, not one generic relationship bucket

This RFC prefers a small typed set over one universal relationship blob.

The unresolved seam is not uniform.
Some relationships are primarily Party↔Party.
Some are Party↔Scope responsibility or control.
Some are references to external contracts or commitments.

A single generic bucket would push too much meaning into free-text or implementation conventions.
That would recreate the drift this RFC is intended to remove.

### 2.4 No constitutional rewrite in this wave

This RFC is intentionally narrow.
It is an extension-layer closure.

A tiny future constitutional guardrail sentence may still be justified later, but it is not required to make this seam executable now.

---

## 3. New contract families created by this RFC

This RFC creates these active machine-contract families in `03_machine_contracts/`:
- `OFARM_PartyRelationship_schema_v0_1.json`
- `OFARM_ScopeResponsibilityRelationship_schema_v0_1.json`
- `OFARM_ExternalCommitmentLink_schema_v0_1.json`

---

## 4. Contract minimums

### 4.1 PartyRelationship minimums

A `PartyRelationship` contract must be able to carry at least:
- stable relationship identifier
- relationship kind
- party A and party B references
- directionality posture
- validity interval
- relationship state
- optional anchor scope references
- optional basis and evidence references

It is intended for durable legal or organisational relationships between parties such as:
- cooperative membership
- cooperative admin office
- employment
- contracted service
- advisor retained-by / employed-by
- pooled-responsibility participation between parties

### 4.2 ScopeResponsibilityRelationship minimums

A `ScopeResponsibilityRelationship` contract must be able to carry at least:
- stable relationship identifier
- relationship kind
- party reference
- target scope
- validity interval
- relationship state
- optional counterparty reference
- optional responsibility classes
- optional basis and evidence references

It is intended for durable relationships between a party and an OFARM scope such as:
- tenancy / lease
- beneficial ownership
- operational stewardship
- advisor-of-record
- pooled responsibility in a field/lot/facility scope
- emergency operator designation

### 4.3 ExternalCommitmentLink minimums

An `ExternalCommitmentLink` contract must be able to carry at least:
- stable link identifier
- link kind
- external system reference
- external object type
- external object identifier
- one or more OFARM linked targets (party, scope, and/or output)
- validity interval
- reference posture
- optional evidence references

It is intended for read-only or evidence-linked references from OFARM parties/scopes/outputs to an external contract, filing, claim, agreement, or sister-platform commitment.

---

## 5. Controlled kinds in the first patch

### 5.1 PartyRelationship kinds

The first patch carries at least:
- `COOPERATIVE_MEMBERSHIP`
- `COOPERATIVE_ADMIN`
- `EMPLOYMENT`
- `CONTRACTED_SERVICE`
- `ADVISOR_RETAINED_BY`
- `POOLED_RESPONSIBILITY_PARTICIPANT`

### 5.2 ScopeResponsibilityRelationship kinds

The first patch carries at least:
- `TENANCY_LEASE`
- `BENEFICIAL_OWNERSHIP`
- `OPERATIONAL_STEWARDSHIP`
- `ADVISOR_OF_RECORD`
- `POOLED_RESPONSIBILITY`
- `EMERGENCY_OPERATOR_DESIGNATION`

### 5.3 ExternalCommitmentLink kinds

The first patch carries at least:
- `BUYER_CONTRACT_LINKAGE`
- `SERVICE_CONTRACT_LINKAGE`
- `LEASE_DOCUMENT_LINKAGE`
- `COOPERATIVE_AGREEMENT_LINKAGE`
- `EXTERNAL_FILING_LINKAGE`
- `EXTERNAL_CLAIM_LINKAGE`

---

## 6. Non-implication rule

A durable relationship artifact must **never** automatically create:
- a `RoleAssignment`
- an `AuthorityGrant`
- a `DelegationGrant`
- a `SharingGrant`
- a `RevocationDecision`
- a compliance fact
- an accepted executed consequence
- lot identity change
- title / payment / settlement truth
- cross-platform access

Relationship artifacts may only be used as:
- evidence or justification for grant issuance
- a condition checked by runtime policy
- a conformance-fixture precondition
- a filter or explanation input in audit traces

---

## 7. Compatibility rule

Existing authority envelopes remain valid.
This RFC adds relationship-basis objects behind them.

Nothing in this RFC widens the active authority families.
Instead, grants, sharing rules, reviews, and runtime checks may now point at explicit durable relationship records instead of relying on free-text inference.

---

## 8. Out of scope

This RFC does not:
- create a second policy engine
- make membership equal authority
- make tenancy equal filing or signatory power
- make beneficial ownership equal operational control
- create native labour-management or contract-management workflows
- promote payment, settlement, or order-management truth into OFARM

---

## 9. Outcome

After this RFC:
- OFARM gains a small typed durable-relationship layer
- recurring multiparty legal-operational context becomes machine-visible
- the authority layer remains explicit and separate
- exchange-boundary and hostile-fixture work can anchor to stable relationship-basis objects instead of prose alone
