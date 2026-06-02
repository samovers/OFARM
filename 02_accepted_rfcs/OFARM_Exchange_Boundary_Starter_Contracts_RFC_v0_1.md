# OFARM Exchange Boundary Starter Contracts RFC v0.1

Date: 2026-04-21  
Status: accepted post-charter RFC  
Scope: promote the smallest sister-platform boundary artifacts needed now for contract-linked access and cross-platform grant traceability without importing commerce or payment truth into OFARM

---

## 1. Problem statement

The active baseline, lot-traceability RFC, partner-output boundary closure, and runtime-surface work already get the high-level boundary stance right:
- external mappings and partner channels are integration surfaces, not canonical truth
- shipment, order, invoice, and delivery references do not create new lot identity by themselves
- partner-facing outputs and sharing remain governed by OFARM authority, publication, and traceability law

That direction remains correct.

What remains open is a smaller seam:
OFARM still needs explicit boundary artifacts for:
- why an external commercial or partner system is in the picture
- how a governed OFARM grant was externalised or consumed by a sister platform

This RFC closes only that narrow seam.

---

## 2. Core stance

### 2.1 Reference and receipt objects only

The objects promoted by this RFC are boundary reference and receipt artifacts.
They are not new truth stores.

### 2.2 No silent authority

A contract reference does not grant access.
A cross-platform grant receipt does not create independent authority.
The underlying OFARM grants still govern.

### 2.3 No silent commercial truth mutation

These starter artifacts must not:
- create accepted delivery facts
- create lot identity changes
- create settlement truth
- create payment truth
- create title transfer by implication

---

## 3. New contract families created by this RFC

This RFC creates these active machine-contract families in `03_machine_contracts/`:
- `OFARM_ContractReference_schema_v0_1.json`
- `OFARM_CrossPlatformGrantReceipt_schema_v0_1.json`

---

## 4. Contract minimums

### 4.1 ContractReference minimums

A `ContractReference` contract must be able to carry at least:
- stable contract-reference identifier
- external system reference
- contract type
- external contract identifier
- validity interval
- reference posture
- one or more linked OFARM targets (party, scope, and/or output)
- optional evidence references

It carries the existence of a linked external contract reference and the OFARM linkage.
It does **not** carry full contract law, fulfilment, settlement, or payment truth.

### 4.2 CrossPlatformGrantReceipt minimums

A `CrossPlatformGrantReceipt` contract must be able to carry at least:
- stable receipt identifier
- source grant family and source grant reference
- external platform reference
- issue time
- optional expiry time
- linked scopes and/or linked artifact references
- external credential/token/reference identifier
- delivery mode
- revocation-check posture
- receipt state

It records that an OFARM grant was externalised or consumed by a sister platform.
It is not independent authority.
If the underlying grant is revoked or expires, the receipt becomes stale, revoked, or expired.

---

## 5. Compatibility and explicit deferral

### 5.1 Delivery evidence

`DeliveryEvidenceBundle` is still justified.
In this wave it stays deferred to a narrower evidence/profile decision.
Preferred default: use a typed/profiled delivery lane over existing evidence structures unless a standalone schema becomes necessary.

### 5.2 Dispute path

`DisputeEvent` should remain an explicit `GovernanceEvent` subtype or profile, not a new top-level constitutional family.
This RFC therefore does not create a separate dispute family.

### 5.3 Settlement and payment

`SettlementReceipt` and `PaymentReceipt` remain candidate/reference artifacts only.
They are not promoted by this RFC.

---

## 6. Out of scope

This RFC does not:
- standardize offers, bids, orders, or invoicing
- create native OFARM payment execution or settlement workflows
- create delivery acceptance by implication
- create title transfer by implication
- import a marketplace, ERP, or dispute-resolution system into OFARM

---

## 7. Outcome

After this RFC:
- OFARM can explicitly link farm scopes, lots, and outputs to external contracts
- OFARM can explicitly record when grants are externalised to sister platforms
- buyer/service/lease integration can proceed without hidden truth-store drift
- broader delivery, dispute, settlement, and payment semantics remain outside core OFARM unless later promotion is proven necessary
