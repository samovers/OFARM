# OFARM Wave 24 alias-runtime and saved-query regression hardening memo v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact

## Purpose

This wave closes the remaining direct alias-governance conformance seam identified in the coverage matrix:

- fixture-level alias catalog law already existed
- graph-pattern equivalence already existed after alias resolution
- cross-target QueryPlanIR semantic equivalence already existed
- but runtime-integrated alias resolution during query compilation and saved-query regression was still only implied

## Scope

This wave adds a bounded runtime-shaped proof layer for:

1. loading a saved query with alias references
2. resolving those references against a catalog version available at execution time
3. emitting explicit alias-resolution traces inside the compilation path
4. comparing the resulting canonical semantics against the saved query's baseline fingerprint
5. comparing bounded result digests across allowed execution targets
6. blocking execution when alias ambiguity, missing version pinning, or semantic drift would silently change meaning

## Boundary

This wave does **not**:

- change baseline law
- change accepted RFCs
- change machine-contract substance
- claim deployment-produced alias telemetry
- claim full registry-scale saved-query replay

It stays inside `04_implementation_and_conformance/` and only hardens the runtime proof posture around alias stability.
