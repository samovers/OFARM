# OFARM Deployment Evidence Obligations for Hard Scenarios v0.1

Date: 2026-04-14  
Status: proposed active supporting implementation artifact  
Scope: define the emitted evidence that implementations and pilots must produce to close the remaining deployment-only debt named by the newest OFARM package

---

## 1. Purpose

The newest package already says the remaining debt is concentrated in deployment-produced evidence rather than missing OFARM law.

That means the next pre-implementation move is not another rewrite. It is a **collection contract**.

---

## 2. Core stance

- package-local telemetry is not enough
- every high-consequence path must emit evidence as a first-class product
- redaction and sovereignty are part of the evidence contract

---

## 3. Required emitted record families

### 3.1 EnforcementGateSequenceRecord
Required for:
- every high-consequence compliance assertion path
- every dossier attestation path
- every submission filing path
- every path refused because state is stale/invalid or evidence is insufficient

Minimum fields:
- stable record id
- subject ref and subject type
- gate sequence id
- gate name
- gate order
- gate outcome
- reason code(s)
- acting party/agent ref
- relevant action class
- timestamp
- context snapshot ref where relevant
- materialization basis/snapshot refs where relevant

### 3.2 ProjectionTraceBackLinkageRecord
Required for:
- every live PassportView emitted for external sharing
- every frozen report/dossier/submission output
- every partner or buyer-facing output surface

Minimum fields:
- output ref
- output family
- query ref or saved-view ref
- materialization basis ref
- context snapshot ref
- canonical substrate refs or basis member refs
- shaping/profile refs
- generation time
- redaction profile or sharing-policy ref

### 3.3 MaterializationUseRecord
Required for:
- any high-consequence action that materially relied on current state

Minimum fields:
- action ref
- use class
- twin
- anchor scope
- freshness state at use time
- generated-at time of materialization
- trigger summary if recomputed or invalidated
- snapshot retained yes/no
- reason for refusal or review where relevant

### 3.4 AuthorityDecisionEmissionRecord
Required for:
- delegated contractor flows
- advisor-prepared submission flows
- buyer read-only flows
- certifier review flows
- AI-assisted preparation flows
- any denial/review/human-approval path

Minimum fields:
- authorization trace ref
- requested action class
- acting party/agent
- target scope/time
- decision outcome
- human-approval requirement yes/no
- revocation check result
- delegation basis ref where relevant

### 3.5 OfflineSyncConflictAndLateEvidenceRecord
Required for:
- offline field capture later synced online
- late evidence arrival after earlier weaker state
- stale local authority crossing a revocation boundary

Minimum fields:
- local draft ref
- sync batch ref
- stale grant/authority posture summary
- late-evidence relation
- conflict type
- resulting review/promotion path
- preserved earlier record refs
- supersession/output impact refs where relevant

### 3.6 BridgeEvidenceIntakeRecord
Required for:
- any same-standard bridge promotion request

Minimum fields:
- bridge surface id
- candidate status before review
- live field telemetry refs
- deployment trace-back linkage refs
- production approval refs
- resulting promotion decision

---

## 4. Scenario-to-record mapping

### Wet grain / storage campaign
Must emit:
- EnforcementGateSequenceRecord
- ProjectionTraceBackLinkageRecord
- MaterializationUseRecord
- OfflineSyncConflictAndLateEvidenceRecord when offline sensor data or late lab data exist

### Contractor late-record campaign
Must emit:
- EnforcementGateSequenceRecord
- AuthorityDecisionEmissionRecord
- OfflineSyncConflictAndLateEvidenceRecord

### Organic/conventional segregation or spray-drift dispute
Must emit:
- EnforcementGateSequenceRecord
- ProjectionTraceBackLinkageRecord
- AuthorityDecisionEmissionRecord

### Post-filing supersession
Must emit:
- EnforcementGateSequenceRecord for both old and new paths
- ProjectionTraceBackLinkageRecord for both output versions
- MaterializationUseRecord for both relied-upon states
- OfflineSyncConflictAndLateEvidenceRecord where applicable

---

## 5. Pre-implementation acceptance gate

Before a team may claim that a hard-scenario implementation is “ready for pilot”, the implementation plan should already show:
- which runtime component emits each required record family
- which identifiers link those records back to substrate/basis/output objects
- how sovereignty/redaction is handled
- where those records are retained and queryable
- how fixture scenarios will assert their presence

Without this, the pilot will produce anecdotes rather than reusable evidence.

---

## 6. Redaction and sovereignty rules

Deployment evidence should preserve enough linkage for audit and conformance while still supporting:
- scope-bounded sharing
- redacted external review where appropriate
- separation between farm truth and cross-farm/regional analytics
- non-disclosure of unrelated farm data in partner/buyer/certifier reviews

Recommended posture:
- emit stable refs plus redaction profile refs
- do not expose raw evidence unnecessarily when traceable linkage is enough
- keep farm-side control over full evidence unless stronger governing rules apply

---

## 7. What this note does not do

This note does **not** claim that deployment evidence already exists. It only makes the evidence obligation precise.

It also does **not** require a full credential ecosystem, public ledger, or novel trust fabric. The focus is ordinary pilot-grade emitted evidence.
