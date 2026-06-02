# OFARM runtime-surface manifest and discovery linkage fixtures v0.1

Date: 2026-04-19  
Status: active supporting implementation fixture set  
Scope: bounded deployment-facing linkage proof connecting Capability Manifest draft surface rows, RuntimeSurfaceContract draft refs, governed discovery surfaces, ConformanceClaimSet grounding, and ActiveArtifactSet deployment state

---

## 1. Purpose

These fixtures harden the deployment-facing runtime-surface seam after the currentness/semantic-field refinement wave.

The bounded target is:
- keep `RuntimeSurfaceContract v0.1` and `Capability Manifest v0.1` as the default current families
- prove that a manifest draft can point at richer `RuntimeSurfaceContract v0.2 draft` artifacts without silently making that draft family the package default
- keep discovery linkage on governed OFARM surface identities rather than raw external document ids
- ground supported/partial runtime-surface lanes in an explicit `ActiveArtifactSet`

## 2. Positive fixtures

### Linked core deployment manifest draft
- manifest draft uses `contractRef` for export, discovery, query-façade, and event-ingress lanes
- mapping rows keep mapping identity in `targetRef`
- non-mapping rows keep stable surface identity in `targetRef`

### Linked active artifact state
- active artifact set grounds the linked manifest, substrate bundle, claim set, mapping coverage/loss artifacts, and the supported/partial runtime-surface contracts actually in force
- planned query/event lanes remain declared but not active

### Discovery linkage
- discovery refs on linked runtime-surface contracts resolve to the governed discovery-surface identity
- discovery visibility is restricted, so a supported discovery surface must be declared in the linked manifest

### Service-description alignment
- manifest `serviceDescriptionRefs` remain a subset of the linked runtime-surface contract `serviceDescriptionRefs`
- service-description artifacts remain references, not hidden semantic authority

## 3. Negative fixtures

- restricted discovery visibility without a declared discovery surface should fail linkage evaluation
- manifest/service-description drift should fail linkage evaluation
- missing supported runtime-surface contract in active artifact state should fail linkage grounding
- linked runtime-surface discovery ref that points at an undeclared discovery surface should fail
- export mapping row whose target mapping is not listed in the linked runtime-surface contract should fail

## 4. Expected result

The runner should emit `PASS_WITH_LIMITATIONS` when:
- the linked manifest, claim set, and active artifact set validate
- supported/partial runtime-surface contracts resolve and ground successfully
- discovery and service-description linkage checks pass
- planned surface rows are allowed to remain out of active artifact state
- negative mutations fail as expected

## 5. Limitation boundary

This wave is package-local deployment linkage proof only.
It does not fetch live `.well-known` endpoints, OpenAPI documents, or AsyncAPI documents from a running deployment.
