# OFARM Agentic AI Public Surface and No-Hidden-Truth Policy v0.1

Date: 2026-05-14  
Status: draft companion artifact; not active companion law until promoted.  
Role: policy bridge between existing AI-agent support material and new agent/world-model runtime contracts.

## 1. Purpose

This policy states the public-surface discipline for AI agents, multi-agent workflows, and world-model runtimes in OFARM.

## 2. Core rule

Agents may assist with interpretation, query, drafting, evidence capture, advisory scenarios, document preparation, and user guidance, but every state-affecting or high-consequence action must use governed public operations and produce traceable outcomes.

## 3. Hidden-truth prohibition

The following are not canonical truth merely because they exist:

- agent output
- agent memory
- agent scratch state
- tool invocation result
- public read model
- projection
- cache
- output preview
- world-model state
- scenario result
- benchmark signal
- model confidence score

They may become useful only when routed into OFARM-governed artifact, evidence, advisory, bridge, review, promotion, publication, or sharing paths.

## 4. Store-mutation rule

Agents and apps must not directly write:

- canonical assertion/history stores
- governed materialization stores
- pack activation state
- authority or sharing grants
- publication/export records
- attestation/signature records

They must call governed runtime operations that apply authority, evidence, freshness, pack/profile, query, promotion, and output gates.

## 5. Output disposition rule

Every agent-produced item must be classified as one of:

- ephemeral scratch
- query proposal
- draft artifact
- evidence attachment candidate
- advisory output
- hypothesis
- scenario result
- EvidenceNeed
- ObservationRequest
- BridgeCandidate
- review request
- compiled-output preview
- permission-limited answer
- blocked/refused action

A generic `AgentOutput` truth bucket is forbidden.

## 6. Handoff rule

Agent handoff may transfer task context, never authority. The receiving agent must recheck authority, scope, freshness, data-sharing limits, target twin, and write-surface permissions.

## 7. Farmer-facing display rule

Apps must preserve distinctions between:

- draft
- advisory
- planned
- claimed
- accepted
- disputed
- corrected
- superseded
- stale
- permission-limited
- compliance-blocking

UI convenience must not collapse these states.
