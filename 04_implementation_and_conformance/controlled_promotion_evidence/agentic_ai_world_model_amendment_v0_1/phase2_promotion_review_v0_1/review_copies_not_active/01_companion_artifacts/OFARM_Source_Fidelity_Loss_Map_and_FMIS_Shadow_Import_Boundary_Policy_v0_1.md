<!--
Promotion review copy only. This file is included inside the Phase 2 supporting review folder.
It is not active OFARM law unless copied to the active target path by a separate controlled promotion.
Phase 2 classification: GREEN_WITH_REVIEW.
-->

# OFARM Source Fidelity, Loss Map, and FMIS Shadow Import Boundary Policy v0.1

Date: 2026-05-13  
Status: draft companion candidate; implementation support only

## Purpose

This policy makes external source fidelity visible for AI-built platform and app code. It applies especially to FMIS shadow imports, machinery telemetry, sensors, weather, inventory, and finance inputs.

## Boundary

External source payloads do not become accepted OFARM truth just because the platform can parse them. They normally enter as candidate material, claim material, observation assertions, or evidence references, then pass through governed review/promotion if stronger use is requested.

## Required app/adapter outputs

Every external adapter should emit:

- source system reference
- source record references
- retrieval and receipt times
- payload hash and original-payload reference
- source fidelity posture
- identity resolution references
- unit assumptions
- loss map references
- promotion eligibility posture
- high-consequence block status

## FMIS shadow import rule

An FMIS shadow adapter MVP is allowed to reconstruct candidate records and review queues. It is not allowed to emit accepted governance facts, Compliance Twin decisions, frozen outputs, or authoritative current state.

## Required refusals / blocks

High-consequence use must be blocked when:

- actor identity is unresolved
- product identity is unresolved
- geometry/extent version is stale or ambiguous
- source time semantics are ambiguous
- loss map contains material/high-risk loss
- evidence is absent or insufficient for the requested output
- source record is candidate-only
