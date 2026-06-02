<!--
Promotion review copy only. This file is included inside the Phase 2 supporting review folder.
It is not active OFARM law unless copied to the active target path by a separate controlled promotion.
Phase 2 classification: AMBER.
-->

# OFARM Offline Capture and Delayed Sync RFC v0.1

Date: 2026-05-13  
Status: draft implementation-facing RFC candidate  
Scope: Phase 6 practical farm contracts for offline capture, delayed contractor sync, idempotent replay, and authority recheck

## 1. Purpose

This draft defines the app/platform contract for offline-first farm work. It converts the existing delayed-sync and revocation fixtures into a product-facing contract that AI coding agents can implement without turning local drafts into accepted compliance truth.

## 2. Authority posture

This draft supports, but does not override:

- `01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`
- `02_accepted_rfcs/OFARM_Authority_Policy_Model_RFC_v0_1.md`
- `04_implementation_and_conformance/implementation_notes/runtime_surface_and_capability/OFARM_Runtime_Dispute_Path_and_Delayed_Sync_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_Offline_Revocation_and_Scope_Drift_Break_Test_v0_1.md`

## 3. Core decisions

1. Offline capture may preserve draft, candidate, claim, and evidence history.
2. Offline capture is not accepted OFARM truth.
3. Sync replay must recheck authority, delegation, revocation, scope, pack/profile context, identity, and materialization freshness.
4. Idempotency keys and fingerprints are required for offline replay.
5. Duplicate replay must reuse the previous replay result or block conflicting replay.
6. Revocation crossing, field geometry drift, partial failure, missing evidence, and dispute must return explicit review-required or blocked states.

## 4. Public operation candidates

| Operation | Purpose | Consequence |
|---|---|---|
| `sync.replay` | Submit offline capture for governed replay | state-affecting, idempotency required |
| `sync.result.get` | Retrieve replay result and trace | read-only |

## 5. Machine contracts

- `OFARM_OfflineCaptureEnvelope_schema_v0_1.json`
- `OFARM_SyncReplayResult_schema_v0_1.json`

## 6. Non-negotiable display rule

Apps must label pre-sync/offline records as draft/candidate/claim. They must not label them as accepted execution, verified compliance, current truth, or completed treatment until the governed replay result says so.
