# OFARM Authority, Delegation, and Data Sovereignty Policy v0.2

Date: 2026-04-08  
Status: updated by RFC-4 authority action matrix and policy model  
Scope: normative constitutional policy for authority, delegation, sharing, revocation, and farm-scoped data sovereignty in OFARM 2.0

---

## 1. Purpose

OFARM needs explicit law for:
- who may assert or submit
- who may perform or report work
- who may review or decide
- who may attest or sign
- who may install or activate context
- who may see or receive data and compiled outputs
- how delegation works
- how sharing differs from truth authority
- how revocation works without breaking audit history

This policy defines those principles without turning the Constitution into a giant permission spreadsheet.

---

## 2. Core principle

RoleAssignment identifies **who someone is in a context**.

RoleAssignment does **not** automatically imply unlimited power.

Authority in OFARM must be:
- explicit
- scoped
- time-bounded
- traceable
- revocable where governance allows
- distinct by authority family

---

## 3. Authority families

OFARM recognizes at least these baseline authority families:

### 3.1 observe/report authority
Authority to submit observations, measurements, scouting reports, evidence links, and related records.

### 3.2 assert/submit authority
Authority to create typed assertions or submissions in a scope.

### 3.3 operate/intervene authority
Authority to plan, execute, or report interventions and related operational acts in a scope.

### 3.4 review authority
Authority to review, validate, contest, or request correction of records or consequences.

### 3.5 govern/decide authority
Authority to accept, reject, approve, supersede, mandate, or otherwise create governance decisions with effect.

### 3.6 attest/sign authority
Authority to attest, sign, or issue governed compiled outputs or evidentiary statements.

### 3.7 context-governance authority
Authority to install, activate, deactivate, or govern packs, profiles, and other context-bearing artifacts in a scope.

### 3.8 share/revoke authority
Authority to grant, narrow, or revoke access/sharing rights for specific scopes, artifacts, or outputs.

### 3.9 receive/use authority
Authority to access, inspect, or use specific OFARM truth, evidence, views, or Document Assemblies for a stated purpose.

---

## 4. AuthorityGrant

An **AuthorityGrant** binds:
- one Party or RoleAssignment
- to one or more authority families
- in a scope
- for a time interval
- optionally for a stated purpose
- optionally with conditions or limits

AuthorityGrant is the baseline constitutional bridge between:
- identity/role
- scope/time
- permitted kinds of action

---

## 5. DelegationGrant

A **DelegationGrant** is an explicit governed grant through which one Party permits another Party to act within a bounded authority family/scope/time.

Delegation rules:
- delegation must be explicit where governance requires it
- delegation may not exceed the delegator’s valid authority
- delegation must remain traceable
- delegation may carry limits, conditions, or required evidence
- delegation does not erase who actually performed the work
- delegation does not transfer ownership of prior truth history

Delegation is especially important for:
- service providers
- contractor work
- advisor-assisted submission
- delegated pack/context administration
- delegated document preparation or filing

---

## 6. SharingGrant

A **SharingGrant** gives another Party the right to see, retrieve, or receive specific OFARM data, views, evidence, or compiled outputs.

SharingGrant is not the same as:
- authority to assert
- authority to review
- authority to decide
- authority to sign

Sharing rules:
- sharing should be explicit unless law or governing contract/certification says otherwise
- sharing should be scope-bounded
- sharing should be purpose-bounded where relevant
- sharing may be time-bounded
- sharing of a compiled output does not imply write authority over underlying truth

---

## 7. Data sovereignty principle

### 7.1 Farm-scoped default
Farm-scoped operational truth and evidence are governed by the responsible farm-side authority unless a stronger legal, contractual, certification, or public-authority rule applies.

### 7.2 No implicit cross-farm sharing
OFARM must not silently share farm-scoped truth across farms, buyers, certifiers, or advisors merely because integration is convenient.

### 7.3 Separation of sharing and authorship
Sharing access does not change:
- authorship
- provenance
- review lineage
- truth authority

### 7.4 Regional intelligence boundary
Cross-farm or regional intelligence belongs in the Advisory Twin by default.

Recommended posture:
- opt-in where appropriate
- aggregation/pseudonymization where possible
- no direct creation of farm-level compliance facts from regional signals alone

---

## 8. RevocationDecision

A **RevocationDecision** may end or narrow:
- an AuthorityGrant
- a DelegationGrant
- a SharingGrant
- future visibility or use rights

Revocation rules:
- revocation is prospective unless stronger governance says otherwise
- revocation does not erase historical truth
- revocation does not silently void already-issued attested history
- revocation may still terminate future access or future use rights

---

## 9. Separation-of-authority principle

The following must remain separable:

- authority to observe/report
- authority to assert/submit
- authority to operate/intervene
- authority to review
- authority to govern/decide
- authority to attest/sign
- authority to share/revoke
- authority to receive/use

A Party may hold several, but OFARM should not assume they always travel together.

This matters because:
- an advisor may help prepare but not decide
- a service provider may execute but not certify
- a buyer may receive a passport but not alter farm truth
- an inspector may review but not operate on behalf of the farm
- a software agent may assist but not silently gain human governance powers

---

## 10. Default safety bias

If OFARM lacks a clear valid authority path, the default is:
- do not assume authority
- do not assume sharing
- require explicit grant, valid role basis, or governing rule

OFARM should bias toward:
- explicit authority
- explicit sharing
- traceable delegation
- revocable access
- preserved history


## 11. Action classes and policy model

This policy now adopts the action-class and policy model defined by:

- **OFARM Authority Policy Model RFC v0.1**
- **OFARM Authority Action Matrix v0.1**

### 11.1 Action-based authorization
Authority evaluation must be tied to an explicit **AuthorityActionClass**, not only to broad role labels.

### 11.2 Default deny
If OFARM cannot justify a valid action path through grant, scope/time, inheritance, delegation, revocation, and non-human rules where relevant, the default is DENY.

### 11.3 Scope inheritance
Broad-scope grants do not automatically imply all narrower or derived-scope powers.
Inheritance must be explicit through a governed inheritance mode.

### 11.4 Non-human restriction baseline
Non-human actors and AI-assisted flows remain restricted by default for:
- govern/decide actions
- context-governance actions
- attestation/signing actions

unless later governance explicitly relaxes them.
