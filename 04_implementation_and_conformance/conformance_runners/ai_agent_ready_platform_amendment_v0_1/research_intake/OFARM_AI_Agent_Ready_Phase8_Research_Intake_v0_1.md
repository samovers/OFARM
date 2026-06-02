# OFARM AI-Agent-Ready Phase 8 Research Intake v0.1

Date: 2026-05-14  
Status: active supporting research intake

## Intake summary

The attached research report recommends an OFARM-specific conformance suite aimed at known AI-agent shortcuts, not protocol compliance alone. Phase 8 adopts that recommendation directly.

The report specifically supports:

- semantic-law blocker tests for materialization/truth inversion, projection-as-evidence, advisory/compliance confusion, pack mutation, and candidate-only FMIS imports;
- contract-discipline tests for public/internal boundaries, strict schema validation, reason-code mapping, dry-run/trace advertising, and SDK generation from public contracts only;
- sync/import tests for idempotency, stale preconditions, semantic conflict payloads, expired cursors, duplicate imports, unsupported units, and source-fidelity loss;
- numeric/display tests for deterministic conversion, rounding, display-value separation, and preserving stale/disputed/redacted/evidence-insufficient states through API/SDK/UI;
- explainability regression tests for preflight, denial, query, publication, pack, and import traces;
- a readiness gate that treats semantic-law conformance as non-waivable.

## OFARM authority treatment

The research does not override active baseline law. Phase 8 translates research-supported testing patterns into implementation/conformance artifacts only.

## Adopted as Phase 8 artifacts

- `agent_readiness_conformance_v0_1/`
- conformance case/suite schemas
- two-agent compatibility build test
- offline contractor dispute hard-path break test
- Phase 8 gate and matrix

## Not promoted by this phase

Phase 8 does not promote any draft RFC, companion artifact, or machine contract into active law. Runtime conformance remains `NOT_RUN` until implemented and tested.
