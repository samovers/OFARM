# OFARM RuntimeSurface manifest/discovery linkage closure note v0.1

Date: 2026-04-19  
Status: accepted closure companion artifact (colocated with the runtime-surface and Capability Manifest RFC family)  
Scope: clarify bounded deployment-facing linkage rules among Capability Manifest draft surface rows, RuntimeSurfaceContract draft references, governed discovery surfaces, and ActiveArtifactSet grounding

---

## Decision

This note closes a bounded hostile-integrator gap without reopening RC2.1 baseline law and without promoting `RuntimeSurfaceContract v0.2 draft` to the package default.

For deployment-facing linkage hardening:

- `OFARM_Capability_Manifest_schema_v0_1.json` remains the default current manifest family.
- `OFARM_Capability_Manifest_schema_v0_2_draft.json` may be used for bounded linkage proof where declared surfaces need explicit `contractRef` resolution and service-description alignment.
- `OFARM_RuntimeSurfaceContract_schema_v0_1.json` remains the default current runtime-surface family.
- `OFARM_RuntimeSurfaceContract_schema_v0_2_draft.json` may be referenced from a manifest draft when deployment-facing comparison needs explicit surface binding, auth posture, delivery semantics, and idempotency posture.

## Linkage rules

### 1. `targetRef` meaning stays explicit by surface row kind

For `Capability Manifest v0.2 draft` surface rows:

- `IMPORT_MAPPING` and `EXPORT_MAPPING` rows keep `targetRef` as the governed mapping identity.
- `API_CONTRACT`, `EVENT_IMPORT`, `EVENT_EXPORT`, `QUERY_FACADE`, and `DISCOVERY_SURFACE` rows should use `targetRef` as the stable governed surface identity.

This avoids overloading `targetRef` with raw endpoint, topic, or `.well-known` document ids.

### 2. `contractRef` may point at a richer draft surface contract

Where a manifest row carries `contractRef`:

- the ref may resolve to a default-current `RuntimeSurfaceContract v0.1`, or
- it may resolve to a bounded `RuntimeSurfaceContract v0.2 draft`

If the linked contract is `v0.2 draft`:

- mapping rows should link a contract whose `mappingModuleRefs` include the manifest row `targetRef`
- non-mapping surface rows should link a contract whose `surfaceIdentityRef` matches the manifest row `targetRef`

### 3. Discovery linkage should prefer governed discovery-surface identity

Where a governed discovery surface exists, `discoveryRefs` on runtime-surface contracts should prefer the governed discovery-surface identity rather than a raw external discovery-document identifier.

This keeps discovery linkage on governed OFARM artifact identities while still allowing service-description documents to remain external references.

### 4. Service-description refs must not drift silently

If a manifest surface row includes `serviceDescriptionRefs`, those refs should be a subset of the linked runtime-surface contract `serviceDescriptionRefs`.

This does not make OpenAPI, AsyncAPI, or `.well-known` documents semantic authority. It only prevents silent manifest/contract drift.

### 5. ActiveArtifactSet grounding stays explicit

For bounded deployment-facing linkage proof, the `ActiveArtifactSet` used by the manifest should ground at minimum:

- the manifest artifact itself
- the linked `SemanticSubstrateBundle`, where declared
- the linked `ConformanceClaimSet`, where declared
- each `SUPPORTED` or `PARTIAL` runtime-surface `contractRef` actually in force for that deployment-facing lane

`PLANNED` surface rows do not need to appear in the active artifact set.

## What this note does not do

This note does not:

- promote `RuntimeSurfaceContract v0.2 draft` to the default current package family
- require partner-facing endpoints or topics to become constitutional identities
- elevate service-description documents above governed OFARM artifacts
- add a new baseline discovery subsystem
- require live deployment endpoint fetches for package-local closure

## Practical implication

A package-local hardening lane may now prove all of the following together without changing active default currentness:

- a manifest draft can point at richer runtime-surface draft contracts
- discovery linkage can stay on governed surface identities
- service-description refs stay aligned across manifest and runtime-surface artifacts
- active deployment grounding can show which declared surfaces are actually in force
