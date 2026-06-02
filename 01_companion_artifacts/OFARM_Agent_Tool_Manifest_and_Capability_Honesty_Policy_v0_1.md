# OFARM Agent Tool Manifest and Capability Honesty Policy v0.1

Status: COMPANION_ARTIFACT
Date: 2026-05-16
Authority role: active normative support below active baseline and accepted RFCs.

## Policy

Agentic runtime capabilities must be visible, inspectable, bounded, and honest. Capability Manifest agentic overlays and `AgentToolManifest` files are self-description surfaces; they are not trust shortcuts.

## Required distinctions

- capability declaration versus authority;
- discovery metadata versus approval;
- declared tool hint versus policy decision;
- tool execution outcome versus governance outcome;
- static validation versus executed conformance;
- manifest version support versus runtime readiness;
- data access versus data sharing;
- redacted detail versus redacted summary;
- advisory support versus Compliance Twin mutation.

## Manifest honesty requirements

A manifest or descriptor should expose, at minimum:

- publisher/source identity and version;
- signature or digest reference;
- input and output schema references and hashes;
- side-effect class and target state surface;
- data classes read, written, disclosed, or retained;
- authentication mode and required scopes;
- approval requirement and semantic preconditions;
- external-call posture and allowed/prohibited egress;
- trace-retention and blocked-action trace promises;
- redaction and permission-limited result behavior;
- farm-data learning or memory-use posture;
- known limitations and prohibited uses;
- readiness claim status, evidence references, public-claim allowance, and expiry.

## Non-authoritative hints

Declared hints such as read-only, safe, idempotent, destructive, external-network, or low-risk are useful for discovery and UI preparation only. They must not be treated as policy decisions unless reconciled with effect classification, authority, approval, sharing, evidence, freshness, and runtime trace evidence.

## Farmer/admin-facing implication

A farmer, farm administrator, auditor, or implementer should be able to answer:

> What can this agent/tool do, what does it need approval for, what data can it see or disclose, what does it retain or learn from, what will be traced, and what claims are merely declared rather than tested?

The answer should come from manifests, trace surfaces, and result qualification, not vendor prose alone.

## Readiness claim discipline

Static schemas, examples, manifest files, and tool annotations are not runtime evidence. Any public claim above declared/static readiness must point to executed conformance evidence and remain within the claim limits declared by active OFARM readiness artifacts.
