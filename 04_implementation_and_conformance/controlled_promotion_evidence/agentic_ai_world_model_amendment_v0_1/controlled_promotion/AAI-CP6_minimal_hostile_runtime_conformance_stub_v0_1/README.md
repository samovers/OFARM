# AAI-CP6 — Minimal hostile runtime conformance stub

Date: 2026-05-16
Status: IMPLEMENTATION_CONFORMANCE_EXECUTED_SELECTED_STUB

## Purpose

CP6 adds a selected minimal hostile runtime conformance stub. It executes synthetic hostile cases against the promoted CP2 through CP5 controls: public surfaces, result qualification, sponsor-bound authority, run tracing, handoff, and manifest honesty.

## Core rule

A passing CP6 stub proves only that selected synthetic hostile cases emitted the expected blocks, qualifications, and traces. It does not prove production readiness, runtime AI-agent readiness, two-agent compatibility, autonomous compliance decisioning, external-standard readiness, live deployment readiness, full Phase 9 execution, or world-model readiness.

## What CP6 exercises

- agent identity without authority is denied
- revoked authority is rechecked
- preflight/dry-run creates no side effect
- stale or limited basis produces result qualification
- blocked actions are trace retrievable
- handoff does not transfer authority
- tool success cannot become governance success
- world-model state cannot become current state
- EvidenceNeed and ObservationRequest do not create evidence, obligations, or blockers by themselves
- sharing and offline sync recheck revocation
- manifest overclaim and redaction leaks are blocked
- agent memory is not evidence

## Non-claims

CP6 does not change active baseline law, add accepted RFCs, promote new machine contracts, promote world-model runtime, promote EvidenceNeed/ObservationRequest, or claim production/runtime AI-agent readiness.
