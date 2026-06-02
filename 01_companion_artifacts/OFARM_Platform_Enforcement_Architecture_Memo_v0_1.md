# OFARM Platform Enforcement Architecture Memo v0.1

Date: 2026-04-08  
Status: phase-11 baseline artifact  
Scope: runtime realization of constitutional law through deterministic enforcement points in OFARM Platform

---

## 1. Purpose

The OFARM Constitution now defines:
- truth law
- twin law
- event grammar
- commit classes
- pack safety
- authority and sharing law
- query law
- output taxonomy

But a Constitution is not enough unless the platform has a concrete way to enforce it.

This memo defines the runtime enforcement architecture.

---

## 2. Executive stance

The platform must not rely on:
- developer discipline alone
- UI discipline alone
- “normal usage”
- ad hoc review habits
- hidden runtime conventions

Instead, it must enforce the constitutional rules through a **deterministic gate chain**.

That gate chain does not mean one giant synchronous pipeline.
It means every state-affecting path must cross the relevant governed checkpoints.

---

## 3. EnforcementChain

The baseline OFARM Platform enforcement chain is:

1. **ingress normalization gate**  
   Normalize capture/import into typed OFARM draft material.

2. **authority gate**  
   Check whether the acting Party/agent/path has the right authority family, scope, time, and delegation basis.

3. **structural/semantic validation gate**  
   Validate structure, semantic type, alignment constraints, event family, and content/path consistency.

4. **pack/profile applicability gate**  
   Resolve active PackActivationSet and the rules/evidence/constraints that actually apply.

5. **evidence sufficiency gate**  
   Check whether the current action/promotion path has the required evidence or acceptable durable evidence references.

6. **review/promotion gate**  
   Decide whether the material stays draft, becomes accepted, becomes contested, or requires formal review/decision.

7. **current-state materialization gate**  
   Only accepted/in-force material may change the relevant current-state materialization.

8. **publication/export gate**  
   PassportViews, DocumentAssemblies, APIs, and exports must assemble from the governed substrate and remain traceable back to it.

Not every path hits every gate equally, but every path that wants to affect authoritative outcomes must cross the relevant gates.

---

## 4. Failure classes

A failed or incomplete enforcement path should not always mean the same thing.

The platform should support at least these outcomes:

- **reject**: structurally or semantically invalid, or authority clearly absent
- **retain as draft**: captured but not promotable yet
- **contested / under review**: contradiction or authority/review dispute exists
- **require more evidence**: evidence insufficiency blocks promotion
- **deferred due to pack/context conflict**: active context cannot be resolved safely
- **accepted with trace**: all required gates passed

This prevents the common bad pattern where everything becomes either “saved” or “not saved.”

---

## 5. Where truth actually changes

Truth changes only in two places:

- **assertion/history-first substrate**
- **governed current-state materializations**

The platform must not let:
- UI state
- API payload state
- search indexes
- cached read models
- report stores
- AI memory
- local device caches

become hidden truth stores.

---

## 6. Twin-specific enforcement

### 6.1 Compliance Twin
The Compliance Twin may only materialize from:
- in-force accepted assertions
- accepted event consequences
- valid review decisions
- applicable context and evidence rules

### 6.2 Advisory Twin
The Advisory Twin may materialize from a wider set:
- hypotheses
- advisory outputs
- risk flags
- scenario outputs
- competing candidate interpretations

But the Advisory Twin may not directly mutate Compliance Twin current state without the constitutionally governed bridge.

---

## 7. Edge/offline enforcement

The edge may do:
- local typing
- local validation
- local authority hints
- local evidence capture
- local draft graph maintenance

The edge should **not** finalize:
- compliance facts
- accepted executed intervention consequences
- context activation requiring central compatibility/governance
- final attested compiled outputs

unless a later explicit architecture version makes that safe and governed.

---

## 8. AI enforcement

AI is part of the runtime, not outside it.

Therefore AI outputs must enter through the same enforcement architecture:
- interpretation AI -> draft assertions / hypotheses
- query AI -> QuerySpecification / QueryPlanIR
- advisory AI -> advisory outputs only
- authoring AI -> draft artifacts pending governance

No AI route may bypass:
- authority checks
- evidence checks
- pack/context checks
- promotion/review gates

---

## 9. Registry and capability enforcement

The platform registry and capability surfaces are not just catalogs.
They are also enforcement inputs.

They should declare and/or constrain:
- supported artifact types
- supported pack activation behavior
- supported event families and commit classes
- supported authority families
- supported query/runtime capabilities
- supported evidence/attestation behavior

This allows tooling and partners to know what can be enforced before integration starts.

---

## 10. Projection trace-back

Every important projection should be traceable back to:
- assertion/history substrate identifiers
- current-state materialization version or generation basis
- relevant pack/profile context
- relevant query/view assembly basis where needed

That is the only reliable way to keep projections useful without letting them silently mutate into hidden truth.

---

## 11. Why this matters

This phase is where the platform stops being a nice architecture sketch and starts becoming an enforceable operating system.

Without this enforcement model, OFARM would still be vulnerable to:
- accidental truth drift
- silent AI overreach
- UI shortcuts bypassing governance
- inconsistent pack behavior
- reports/passports assembled from stale or untraceable data
- integrations writing around the semantic core

---

## 12. Minimal v2 enforcement baseline

A serious OFARM Platform v2 must have at least:

- deterministic gate chain design
- authority checks
- pack applicability checks
- evidence sufficiency enforcement where policy requires it
- review/promotion gating
- current-state materialization gating
- projection trace-back
- capability-manifest declarations for enforcement-relevant surfaces

That is the minimum credible baseline.
