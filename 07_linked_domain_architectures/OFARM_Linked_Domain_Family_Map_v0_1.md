# OFARM linked-domain family map v0.1

Date: 2026-04-21  
Status: active supporting context artifact  
Scope: establish the high-level family picture for OFARM-adjacent sister platforms without pretending those platforms already have full constitutions or implementation law

---

## 1. Why this note exists

The OFARM package now has explicit OFARM-side boundary law for sister platforms.
Readers still need one visible high-level map that answers a simpler question:

**What is the intended platform family picture around OFARM?**

This note exists to answer that question in one place.

---

## 2. Current family picture

| Domain lane | What it primarily owns | What it may consume from OFARM | What it must not silently do | Current maturity |
|---|---|---|---|---|
| **OFARM core** | farm-scoped operational truth, evidence, review lineage, current-state materialization, authority/delegation/sharing, governed outputs | boundary references from adjacent systems when explicitly admitted | absorb social or commercial truth by convenience | active law |
| **OFARM Exchange** | offer/order/contract process state, commercial dispute context, settlement summaries, payment references | recipient-shaped OFARM outputs, contract-linked references, explicit grant/receipt artifacts | rewrite OFARM truth, widen OFARM access by contract alone, treat payment success as agronomic truth | tenets only |
| **OFARM Social** | groups, messages, moderation, social graph, peer alerts, community discussion, reputation-like signals | bounded OFARM publications where explicitly shared; OFARM-facing signal ingress only through governed paths | convert popularity or discussion into compliance truth or blanket farm access | tenets only |
| **Regulated payment providers / external rails** | payment execution, money movement, financial-service state | exchange/payment references only as needed | become OFARM truth or decide agronomic/compliance state | external infrastructure |

---

## 3. Architectural picture

The intended current picture is:

- **OFARM core** remains the authoritative governed farm system.
- **OFARM Exchange** is the sister platform for commerce/process state around selling, contracting, and dispute handling.
- **OFARM Social** is the sister platform for community, peer interaction, and social/advisory-network behavior.
- **Regulated payment providers** remain outside OFARM core and outside OFARM Exchange core truth, even when Exchange coordinates with them.

None of those adjacent systems is a hidden replacement for OFARM.

---

## 4. Writing order and maturity rule

The preferred writing order is:
1. **OFARM-side boundary policy** inside the active OFARM authority set.
2. **Linked-domain family map** so the reader sees the whole picture.
3. **Constitutional tenets** for each sister platform.
4. **Full sister-platform constitutions** only when a real implementation, pilot, or dedicated charter exists.

This is the smallest useful sequence.
It gives architectural clarity without pretending the adjacent platforms are already implementation-ready.

---

## 5. Priority order

Current priority order is:
1. **OFARM Exchange** — first deeper sister-platform lane because contract-linked access, delivery windows, disputes, and settlement references create the highest risk of hidden truth drift back into OFARM.
2. **OFARM Social** — establish now at the tenets level so the boundary is explicit, but defer deeper law until a real community/moderation implementation trigger exists.

---

## 6. Guardrail

This family map is an architectural framing aid.
It is not active OFARM law and it does not create runtime or schema commitments for the sister platforms by itself.
