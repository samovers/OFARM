# OFARM AI-Agent Readiness Workstream Reset and Inclusion Boundary v0.1

Date: 2026-05-14  
Status: implementation/conformance governance memo  
Scope: pre-development amendment inclusion package

## Purpose

This memo corrects the phase-label drift that occurred after the original pre-development amendment plan. It defines the package-inclusion boundary for the OFARM AI-agent-readiness amendment.

## Controlled inclusion boundary

The pre-development amendment package includes only the original amendment sequence:

```text
A0 / Phase 0  Navigation and authority guardrails
A1 / Phase 1  Platform module boundary map
A2 / Phase 2  Public application/platform surface closure
A3 / Phase 3  AI-agent use, preflight, explain, trace, and reason-code closure
A4 / Phase 4  Query/current-state/output app contracts
A5 / Phase 5  Workflow cookbook and UI-safe state matrix
A6 / Phase 6  Practical farm contracts
A7 / Phase 7  SDK/API bundle and reference platform skeleton
A8 / Phase 8  AI-agent conformance suite and break tests
A9 / Phase 9  Baseline harmonization readiness, proposal-only
```

This is the completed **pre-development amendment track**.

## Reclassification of later work

Any files, packages, or previews previously labelled Phase 10, Phase 11, Phase 12, or Phase 13 are not part of this pre-development amendment package unless separately reviewed and deliberately imported.

They should be treated as separate workstreams:

```text
B1  Controlled promotion review candidate batch
C1  Runtime implementation kickoff planning
C2  Contract-pack/runtime-slice static kickoff
D1+ Runtime implementation slices
```

## Authority posture

This package is additive implementation/conformance support. It does not edit active baseline law and does not itself promote draft materials into active law.

Active authority remains:

1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`
5. `04_implementation_and_conformance/` as supporting implementation/conformance material

## Explicit non-claims

Including this package in the pre-development OFARM package does not claim:

- runtime AI-agent readiness
- external standard readiness
- executed Phase 8 conformance
- executed two-agent FMIS compatibility pass
- accepted promotion of draft RFCs or draft machine contracts
- acceptance of any Phase 10+ promotion or runtime implementation package
- live platform implementation
- live farm pilot readiness

## Why this package still belongs in pre-development

This package makes pre-development stronger by giving future platform implementers and AI coding agents clear, testable boundaries before implementation begins:

- public versus internal surfaces
- module boundaries
- preflight/dry-run/explain behavior
- RuntimeProblem reason-code registry
- result qualification envelopes
- workflow state matrices
- candidate-first import and offline-sync boundaries
- SDK/codegen boundaries
- conformance tests aimed at semantic-law shortcut failures
- baseline harmonization proposals that are explicit but not applied

## Safe inclusion rule

Overlay this package onto the pre-development OFARM repository as implementation/conformance support. Do not move files from `draft_rfcs/`, `draft_companion/`, or `draft_machine_contracts/` into active authority folders unless a later promotion decision explicitly records that move.

## Future work naming

After this package is included, future work should not continue as Phase 10, Phase 11, Phase 12, or Phase 13 of the pre-development amendment. Use separate workstream names:

```text
B-series: promotion review
C-series: runtime implementation planning
D-series: runtime implementation slices
E-series: runtime conformance execution
```
