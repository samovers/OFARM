# OFARM Phase 5 Tool Annotation Untrusted Hint Rule

## Rule

Declared tool hints are descriptive and non-authoritative.

The following are examples of hints:

- `readOnlyHint`
- `destructiveHint`
- `idempotentHint`
- `openWorldHint`
- `externalDisclosureHint`
- `draftOnlyHint`
- `agentSafeHint`

These hints may help a planner, UI, or runtime preflight system. They may not, by themselves, allow execution.

## Required enforcement

The runtime must independently decide:

- whether the action class is allowed;
- whether the target twin is allowed;
- whether the requested scope is allowed;
- whether a SharingGrant or redaction profile permits the call;
- whether preflight is required;
- whether human approval is required;
- whether freshness or pack/profile constraints block the call;
- whether output disposition is allowed;
- whether trace obligations can be met.

## Hostile case

A tool declares `readOnlyHint=true` but has `effectClass=STATE_AFFECTING_GOVERNED_OPERATION` or attempts to create an accepted compliance fact.

Expected result: blocked.
