# OFARM Runtime Materialization Freshness and Basis Trace Fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded current-state explainability hardening that adds runtime-produced freshness telemetry and basis traces after the post-amendment drift check

---

## 1. Purpose

These fixtures return the continuation path to a central hardest-design seam:
governed current state must remain explainable under runtime trigger pressure.

They stay inside `04_implementation_and_conformance/` and do not change OFARM law.

---

## 2. Trigger families covered

The runtime-shaped traces cover:
- `TIME_FRESHNESS_CHECK`
- `CONTEXT_DRIFT`
- `EVIDENCE_UPDATE`
- `EXPLICIT_INVALIDATION`
- `MANUAL_RECOMPUTE_REQUEST`
- `OUTPUT_CONSEQUENCE_GATE`

---

## 3. Decision families covered

The runtime-shaped traces cover:
- `REUSE`
- `REUSE_WITH_WARNING`
- `RECOMPUTE`
- `REFUSE`

Across the two logical twins:
- `COMPLIANCE`
- `ADVISORY`

---

## 4. Starter scenarios

1. compliance fresh reuse for a high-consequence field passport
2. advisory stale reuse-with-warning for exploratory dashboard use
3. compliance recompute after context drift
4. compliance recompute after evidence update
5. attested dossier reuse refusal after explicit invalidation
6. submission filing stop for invalid basis under a high-consequence gate
7. manual recompute after a context change request

---

## 5. Guardrails

This wave does **not** claim deployment-collected materialization telemetry.
It is executor-produced/package-local proof only.

It also does **not** close the separate authority-depth follow-on work.
