# OFARM Agentic AI / World-Model Amendment — Phase 5

Phase: **AAI-P5 — Capability Manifest and AgentToolManifest**
Date: 2026-05-14
Status: **SUPPORTING_REVIEW_ONLY_NOT_PROMOTED**

This phase is a supporting-only amendment package. It does not promote files into `00_active_baseline/`, `01_companion_artifacts/`, `02_accepted_rfcs/`, or `03_machine_contracts/`.

## Purpose

Phase 5 turns the Phase 3 actorship model and Phase 4 run-governance model into deployable self-description candidates:

- `agentSupport` candidate extension for the OFARM Capability Manifest
- `worldModelSupport` candidate extension for advisory-only world-model support declarations
- `AgentToolManifest` candidate contract
- tool descriptor, approval, effect, semantic precondition, declared-hint, external-call, learning, trace-retention, redaction, and readiness-claim-limit contracts

## Core rule

A manifest describes capability. It does **not** grant authority.

A tool manifest describes discovery metadata, schemas, side effects, approval requirements, semantic preconditions, and trace expectations. It does **not** waive OFARM authority, evidence, pack, freshness, query, promotion, publication, or twin-separation law.

## Research incorporation

The attached Deep Research report materially influenced this phase. It reinforced that tool metadata and MCP-style hints are useful for discovery, but cannot be treated as trust or approval; readiness claims need runtime evidence; and manifests should remain layered rather than monolithic.

## Runtime posture

Runtime conformance is **not run** because there is no implementation. Two-agent compatibility is **not run**.
