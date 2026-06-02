# OFARM Phase 7 SDK/API/Skeleton Conformance Gates v0.1

Status: implementation/conformance support only.

Phase 7 closes the delivery-tooling path: public API bundle, SDK/codegen manifest, generated client shape, AsyncAPI event contract, and reference platform skeleton.

## Gates

1. **Public contract pack parses**
   - `openapi_platform_core_phase7_v0_1.json` parses as JSON and has unique operationIds.
   - `asyncapi_platform_events_v0_1.json` parses as JSON and has named receive operations.
   - `OFARM_PublicContractPackManifest_v0_1.json` validates against `OFARM_PublicContractPackManifest_schema_v0_1.json`.

2. **SDK/codegen manifest validates**
   - `OFARM_SDK_Codegen_Manifest_v0_1.json` validates against `OFARM_SDKCodegenManifest_schema_v0_1.json`.
   - Generated targets are `OPERATION_CENTRIC_THIN_CLIENT`.
   - Forbidden generated affordances are listed.

3. **Public/internal boundary is enforceable**
   - Public OpenAPI paths must not include `/internal`, `/assertion-store`, `/materialization-store`, `/promotion-state`, `/authority-state`, or `/pack-activation-state`.
   - Public schema catalog entries are the only schema inputs for generated SDKs.
   - Internal schema catalog does not become SDK input.

4. **SDK shape preserves OFARM law**
   - SDK examples use dry-run/preflight before high-consequence submission.
   - SDK type stubs include RuntimeProblem codes and qualified results.
   - SDK forbidden-pattern examples show shortcuts that must remain absent.

5. **Reference skeleton preserves module boundaries**
   - Apps use SDK only.
   - SDK imports public contracts only.
   - Adapter service emits candidate imports/loss maps and does not call promotion internals directly.
   - Materialization and publication paths do not expose direct truth-store mutation.

6. **No active law mutation**
   - Phase 7 remains additive under implementation/conformance.
   - No active baseline files are edited.
