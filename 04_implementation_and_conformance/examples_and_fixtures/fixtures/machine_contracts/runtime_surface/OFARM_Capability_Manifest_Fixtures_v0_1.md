# OFARM Capability Manifest Fixtures v0.1

Date: 2026-04-08  
Status: example/conformance fixture set  
Scope: baseline fixture scenarios for RFC-5 capability manifests

---

## Fixture 1 — valid core deployment manifest
Manifest:
- core deployment
- supports pack activation
- supports query schemas v0.1
- has restricted discovery visibility
- references a real manifest registry, artifact registry, and active artifact set

Expected:
- schema valid
- registry relation complete

---

## Fixture 2 — valid tenant-specific manifest
Manifest:
- tenant-scoped deployment
- narrower capability set than core deployment
- private discovery visibility
- references tenant activation set

Expected:
- schema valid
- compatible as a narrower derivative deployment description

---

## Fixture 3 — missing registry relation
Manifest omits `activeArtifactSetRef`.

Expected:
- schema invalid

Reason:
- capability claims are not grounded in active runtime state

---

## Fixture 4 — unsupported public expert query mismatch
Manifest claims:
- supportsPublicExpertQuery = true
- but declared query support does not include the relevant public expert-query surface

Expected:
- validation or compatibility check should fail under deployment-specific rules

---

## Fixture 5 — active pack inconsistency
Manifest declares:
- activePackRefs includes `pack:orchard:v1`
- but activeArtifactSetRef points to an activation set without that pack active

Expected:
- manifest-to-active-artifact-set consistency check fails

---

## Fixture 6 — missing enforcement support claims
Manifest omits enforcementSupport.

Expected:
- schema invalid

Reason:
- the baseline platform requires enforcement-relevant self-description


---

## Update in v0.5

The package now ships a minimal `ActiveArtifactSet` contract plus executable consistency checks.
That means fixtures 1, 2, and 5 are no longer only design intent; they are now wired into package-local executable evidence through:
- `03_machine_contracts/schemas/pack_merge/OFARM_ActiveArtifactSet_schema_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/pack_merge/OFARM_ActiveArtifactSet_example_*.json`
- `04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/ofarm_governance_runtime_closure_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_governance_runtime_closure_results_v0_1.json`


## Update in v0.6

The package now adds a bounded linked manifest example for deployment-facing runtime-surface and discovery hardening:
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/drafts_non_default/runtime_surface/OFARM_Capability_Manifest_example_core_deployment_surface_linkage_v0_2_draft.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/pack_merge/OFARM_ActiveArtifactSet_example_core_deployment_surface_linkage_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/runtime_surface/OFARM_ConformanceClaimSet_example_core_deployment_surface_linkage_v0_1.json`

This linked example proves that a manifest draft can reference richer runtime-surface draft contracts while still grounding supported/partial deployment-facing surfaces in an explicit active artifact set.
