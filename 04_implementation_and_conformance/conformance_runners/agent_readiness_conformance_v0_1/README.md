# OFARM Agent Readiness Conformance Suite v0.1

Date: 2026-05-14  
Status: active supporting implementation/conformance candidate  
Authority posture: does not edit active baseline law; test definitions are candidate implementation gates.

## Purpose

This folder defines Phase 8 of the AI-agent-ready platform amendment: executable-style conformance and break-test definitions that catch AI coding-agent shortcuts before a platform is declared agent-ready.

The suite is aimed at semantic-law failures, not just protocol correctness. Passing HTTP/OpenAPI/SDK shape checks is not enough if an implementation still allows projections to become truth, AI output to become governance, FMIS imports to become accepted facts, stale current state to drive high-consequence outputs, or public apps to mutate platform internals.

## Test families

| File | Purpose |
|---|---|
| `OFARM_Agent_Readiness_Conformance_TestPlan_v0_1.json` | Master Phase 8 readiness plan |
| `semantic_law_blocker_tests_v0_1.json` | Truth/materialization/twin/pack/import/output semantic-law blockers |
| `contract_discipline_tests_v0_1.json` | Public/internal boundary, strict validation, manifest and SDK discipline |
| `sync_import_conflict_tests_v0_1.json` | Idempotency, preconditions, duplicate import, cursor, source-fidelity, delayed sync |
| `numeric_display_trace_tests_v0_1.json` | Calculation determinism, display qualification preservation, dry-run trace safety |
| `sdk_boundary_tests_v0_1.json` | Generated SDK and app import boundary checks |
| `explainability_regression_tests_v0_1.json` | Structured trace/explain output regression checks |
| `two_agent_fmis_build_test_manifest_v0_1.json` | Blinded two-agent FMIS compatibility test contract |

## Non-waivable blockers

A platform is not AI-coding-agent-ready if it allows any of these:

```text
AI output -> accepted compliance truth
client cache/current-state projection -> canonical truth
materialization store direct app write
query result -> source evidence without source refs
FMIS/machinery/sensor import -> accepted fact without promotion
offline contractor capture -> accepted execution without sync-time gates
operation claim -> accepted consequence without promotion
stale materialization -> high-consequence output
permission redaction -> fabricated or over-disclosed value
pack/profile -> silent mutation of core meaning
identity ambiguity -> silent merge
unit ambiguity -> hidden UI calculation
compiled output -> truth store
```

## Use

Use these tests after Phase 7 public contracts, SDK shapes, and skeleton boundaries exist. The suite can be used in three modes:

1. **package validation**: schemas, suite files, manifests, and fixtures parse and validate;
2. **static implementation validation**: public/internal boundaries, SDK exports, examples, and imports are scanned;
3. **runtime validation**: a platform instance executes the test cases and returns structured execution reports.

Runtime execution is intentionally not claimed by this package. The template execution report is marked `NOT_RUN` until a platform implementation exists.
