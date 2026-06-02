# OFARM Offline Revocation and Scope Drift Break Test v0.1

Date: 2026-04-19
Status: active supporting implementation artifact
Scope: hostile test for delayed offline contractor sync after delegation revocation and field identity split

---

## 1. Purpose

This hostile break test composes three seams that commonly fail in real farm software:
- offline contractor draft/report capture
- prospective delegation revocation before queued sync promotion completes
- scope drift caused by a later governed field split

The goal is not to prove a full sync engine.
The goal is to prove that OFARM can keep the historical record, force the right review path, and refuse stale parent-scope current-state reuse.

---

## 2. Required composed artifacts

This test composes existing active and support artifacts:
- delegation grant and revocation source records
- the delayed-sync authorization trace and dispute-path support result
- the new active `IdentityLifecycleChange` field-split object
- the new materialization refusal example that names `IDENTITY_LIFECYCLE` explicitly

---

## 3. Expected hostile behavior

The runner must prove all of the following:
- the original delegated contractor action remains historically recorded
- sync-time authorization recheck does not silently auto-promote after revocation
- the field split is explicit and produces child identities with lineage
- the old parent-field materialization is invalid for high-consequence reuse
- the refusal path points at the concrete field-split lifecycle artifact
- the combined terminal posture is review plus recomputation, not silent success

---

## 4. Non-goals

This break test does not prove:
- a full product-grade sync queue
- every future field merge/split permutation
- UI/operator workflow
- deployment telemetry collection

It is a bounded executable hostile test for one high-risk composed seam.
