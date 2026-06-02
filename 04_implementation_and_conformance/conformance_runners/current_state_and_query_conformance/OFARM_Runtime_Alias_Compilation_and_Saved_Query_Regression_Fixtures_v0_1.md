# OFARM Runtime alias-compilation and saved-query regression fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact

## Purpose

These fixtures test whether a saved query keeps the same meaning when it is recompiled under a later alias catalog version at runtime.

The bounded suite checks:

- direct version-pinned alias stability
- back-compatible pinned alias stability across catalog upgrades
- deprecated successor rollover with an explicit canonical trace
- saved-query repin notice where semantics stay the same
- ambiguity hard-fail for unpinned aliases
- hard-fail when a high-consequence saved query omits the alias version
- hard-fail when alias path drift changes canonical semantics

## Positive scenarios

1. field passport saved query pinned to `organic_status@1` on catalog `v1`
2. field passport saved query pinned to `organic_status@1` on catalog `v2` with backward-compatibility
3. evidence-backed spray-operation query using deprecated `spray_records@1` with successor trace to `operation_application_records@2`
4. advisory zone-overlap saved query upgraded with successor trace and explicit repin notice while preserving semantics
5. evidence-backed operation query stable across current-state and semantic-graph targets using `operation_evidence@2`

## Explicit blocked scenarios

1. advisory note query with ambiguous unpinned `note_text`
2. compliance submission query with missing alias version
3. lot-lineage saved query whose alias upgrade would broaden lineage scope and therefore drift semantically

## Boundary

This wave is about **runtime-integrated alias governance plus bounded saved-query regression**.
It does not replace:

- deployment-produced alias telemetry
- full saved-query fleet replay
- broader pack-merge legality coverage
