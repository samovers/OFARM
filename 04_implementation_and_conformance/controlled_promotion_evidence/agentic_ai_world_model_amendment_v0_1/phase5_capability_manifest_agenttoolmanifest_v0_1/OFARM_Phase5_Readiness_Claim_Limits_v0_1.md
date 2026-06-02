# OFARM Phase 5 Readiness Claim Limits

## Claim levels

Phase 5 introduces candidate readiness claim levels:

- `DECLARED_ONLY`
- `STATIC_SCHEMA_VALIDATED`
- `STATIC_EXAMPLE_VALIDATED`
- `IMPLEMENTATION_PRESENT_NOT_TESTED`
- `RUNTIME_EXECUTED`
- `RUNTIME_PASSED`
- `TWO_AGENT_COMPATIBILITY_PASSED`
- `EXTERNAL_CONFORMANCE_REVIEWED`

## Pre-implementation limit

In this package, every Phase 5 capability must remain at one of:

- `DECLARED_ONLY`
- `STATIC_SCHEMA_VALIDATED`
- `STATIC_EXAMPLE_VALIDATED`

It must not claim runtime execution.

## Forbidden claims before implementation

A Phase 5 manifest must not claim:

- production readiness;
- runtime readiness;
- legal/regulatory certification;
- autonomous compliance decisioning;
- world-model compliance automation;
- two-agent compatibility;
- external standard readiness.
