# OFARM Lot Traceability and Claim Basis RFC v0.1

Date: 2026-04-11  
Status: accepted post-charter RFC  
Scope: formalize lot continuity decisions, explicit lot-lineage change records, and machine-readable traceability/claim-basis declarations without reopening OFARM’s core identity model

---

## 1. Problem statement

The active baseline and the Identity RFC already say the right high-level thing:
- Lot identity is cohort-first.
- Split, merge/commingling, transformation, and strong claim-basis reset create a new lot identity.
- Shipment/order/invoice references alone do not create a new lot.

That direction is correct, but it is still too abstract for safe implementation.

The remaining drift-prone questions are:
- how a runtime records a governed lot continuity decision
- how split, merge, commingling, transform, and shipment-reference cases become machine-checkable
- how a claim-basis transition becomes query-visible rather than being hidden inside prose or local business logic
- how OFARM distinguishes stronger physical-lineage models from weaker accounted-claim models without pretending they mean the same thing

This RFC closes that gap with a lot-first patch.

It does **not** reopen OFARM’s constitutional identity model.
It makes the existing lot law executable.

---

## 2. Core stance

### 2.1 Lot-first closure, not a new generic traceability ontology
This RFC intentionally stays lot-first.
It does **not** introduce a broad constitutional `TraceObject` family.

If a future contradiction proves that Lot is insufficient, OFARM can reopen that question later.
That is not needed for this closure pass.

### 2.2 Physical cohort continuity and claim basis both matter
Lot identity remains grounded in materially coherent cohort continuity.

But where claims, certification posture, or governed chain-of-custody semantics materially affect what the lot means, claim basis is part of the traceability basis and must be made explicit.

### 2.3 Explicit lineage is preferred over hidden ambiguity
If the system cannot clearly justify same-lot continuity, it should prefer:
- a new lot identity
- explicit lineage
- preserved derivation trace

over hidden ambiguity.

### 2.4 Shipment and commercial references do not create new lots by themselves
Shipment, order, invoice, or delivery references are usually attached context.
They do not create a new lot unless the underlying traceability cohort changes.

### 2.5 Weaker accounting models must not masquerade as physical same-lot continuity
A weaker claim model may be legitimate under some profiles or packs.
But OFARM must not let:
- mass-balance semantics
- book-and-claim semantics
- other weaker accounted-claim models

pretend to be one-to-one physical same-lot continuity by default.

The model used must be query-visible.

---

## 3. Formal artifacts produced by this RFC

This RFC creates:

- **OFARM LotLineageChange schema v0.1** (`ofarm.lotlineagechange.v0.1`)
- **OFARM TraceabilityClaimBasis schema v0.1** (`ofarm.traceabilityclaimbasis.v0.1`)

This RFC also introduces executable example payloads for:
- lot split
- lot merge / commingling
- lot transformation
- shipment-reference continuity without false new-lot creation
- claim-basis reset with visible lineage consequences
- stronger and weaker claim-basis declarations

---

## 4. Lot continuity decision model

### 4.1 The decision that must be made
When a red-flag lot event occurs, OFARM must answer:

**Is this still the same lot, or must OFARM create a new lot identity with explicit lineage?**

At minimum the decision must consider:
- one-to-one material continuity
- cohort continuity
- whether multiple lots became one cohort
- whether one lot became multiple cohorts
- whether handling or transformation broke the prior cohort identity
- whether claim basis changed strongly enough to require a new traceability object

### 4.2 Red-flag triggers
This RFC treats at least these as red-flag triggers for explicit lot continuity evaluation:
- split
- merge
- commingling
- transformation
- strong claim-basis reset
- other material continuity failures

Shipment-reference attachment, label attachment, or invoice attachment are **not** red-flag identity breakers by themselves.
They still may require a recorded continuity decision when a system needs explainability for why the lot stayed the same.

### 4.3 Allowed continuity outcomes
For the purposes of this closure wave, OFARM recognizes these continuity outcomes:
- **SAME_LOT_CONTINUES**
- **NEW_LOT_REQUIRED**
- **LOT_REVISION_ONLY**

`LOT_REVISION_ONLY` is included for completeness when the durable lot identity stays the same but a governed revision-level distinction is still useful.
The primary closure cases in this RFC are `SAME_LOT_CONTINUES` and `NEW_LOT_REQUIRED`.

---

## 5. Operation-specific rules

### 5.1 Split
If one lot becomes two or more distinct traceability cohorts, OFARM must create new successor lot identities.

Minimum expectations:
- one predecessor lot
- two or more successor lots
- explicit lineage edges from predecessor to successors
- `NEW_LOT_REQUIRED`

The normal lineage relation on the successor lots is `splitFrom`.

### 5.2 Merge versus commingling
OFARM distinguishes:
- **merge**: governed unification of previously distinct lots into one governed successor cohort
- **commingling**: physical mixing where the prior one-to-one identity basis no longer holds

Both require a new successor lot identity.
Both must preserve explicit lineage from source lots to the successor lot.

The distinction is still worth recording because it affects later interpretation, evidence expectations, and claim-basis evaluation.

### 5.3 Transformation
When processing, handling, or transformation breaks the prior cohort identity, OFARM must create a new successor lot.

The typical lineage relation is `derivedFrom`.
A transformation may preserve strong traceability, but it still does not keep the old lot identity when the old cohort identity no longer holds.

### 5.4 Claim-basis reset
A strong claim-basis reset can require a new lot even when physical material continuity remains one-to-one.

This rule exists to prevent hidden semantic drift.
If a lot moves from a stronger physical-lineage model to a weaker accounted-claim model, OFARM should create a new lot identity when the claim-basis change is important enough that later queries, reviews, attestations, or compliance outputs must distinguish it.

The point is not to outlaw weaker models.
The point is to stop them from being mistaken for unchanged same-lot continuity.

### 5.5 Shipment-reference continuity
If a lot only gains shipment/order/invoice/delivery references and the materially coherent cohort remains the same, OFARM should keep the same lot identity.

The continuity decision may still be recorded for explainability.
But a commercial reference alone is not a new lot.

### 5.6 Ambiguity rule
If the runtime cannot safely justify same-lot continuity, it should prefer:
- `NEW_LOT_REQUIRED`
- explicit lineage
- explicit rationale

rather than silent continuity.

---

## 6. TraceabilityClaimBasis

### 6.1 Purpose
`TraceabilityClaimBasis` is a small machine-readable declaration of which traceability/claim model a lot is under when that distinction matters.

It is intentionally narrow.
It is not a second ontology of all certification semantics.

### 6.2 What it must make explicit
At minimum, a claim-basis declaration should make explicit:
- the traceability model being asserted
- the physical continuity class that model implies
- whether the model may ever support same-lot continuity
- the governing artifact references that declare or constrain it

### 6.3 Minimum model distinctions in this RFC
This RFC recognizes at least these traceability models:
- `IDENTITY_PRESERVED`
- `SEGREGATED`
- `MASS_BALANCE`
- `BOOK_AND_CLAIM`
- `DECLARED_OTHER`

This RFC also recognizes at least these physical continuity classes:
- `ONE_TO_ONE_PHYSICAL`
- `SEGREGATED_MULTI_SOURCE`
- `COMMINGLED_ACCOUNTED`
- `NO_PHYSICAL_CONTINUITY_ASSERTED`

### 6.4 Why this artifact exists
The purpose of this artifact is to make the difference between stronger and weaker models query-visible.

Without that, the runtime risks collapsing:
- physical continuity
- segregation discipline
- accounted-claim continuity
- no-physical-continuity claim models

into one ambiguous “lot still means the same thing” shortcut.

OFARM must not do that.

---

## 7. LotLineageChange

### 7.1 Purpose
`LotLineageChange` records the governed continuity decision at a lot red-flag boundary.

It is not the whole substrate copied into a blob.
It is the minimum machine-readable explanation object for why a lot stayed the same, became a new lot, or changed lineage.

### 7.2 What it should capture
At minimum, a lot-lineage change record should capture:
- evaluated time
- change type
- continuity outcome
- source/predecessor lots where relevant
- successor lots where relevant
- explicit lineage edges where new lots are created
- material continuity class
- pre-change and post-change claim-basis references where relevant
- governing event, decision, or evidence references where available
- rationale

### 7.3 Claim-basis transition visibility
If claim basis changes as part of the lot decision, the before/after claim-basis references should be explicit.

This is especially important for:
- commingling into weaker accounted pools
- claim-basis reset without physical mixing
- attestation-sensitive transitions

---

## 8. Conformance posture

This RFC is intentionally a closure artifact.
It should be implemented with:
- schema validation
- executable fixture payloads
- narrow semantic fixture checks

This wave is complete only when the package can validate and exercise:
- split
- merge / commingling
- transform
- shipment continuity without false new-lot creation
- claim-basis reset with visible lineage consequences

---

## 9. Non-goals

This RFC does **not**:
- rewrite RC2.1 identity law
- legalize any external certification model by itself
- decide whether a specific pack/profile should allow a weaker claim model
- create a hidden second truth store
- collapse documents, shipment labels, or commercial references into traceability truth

---

## 10. Follow-on harmonization targets

After acceptance and successful executable closure, the smallest harmonization pass should update only:
- Constitution lot lifecycle wording where needed
- Alignment Register lot wording where needed
- conformance coverage artifacts

No broader redesign is required for this amendment wave.
