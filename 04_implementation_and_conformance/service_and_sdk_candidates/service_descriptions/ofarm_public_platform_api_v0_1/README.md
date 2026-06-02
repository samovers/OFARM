# OFARM public platform API candidate v0.1

Status: `ACTIVE_SUPPORTING_IMPLEMENTATION` / candidate public surface. This folder does not create active baseline law.

Phase 7 adds a contract-pack shape for AI-agent-ready platform development:

- `openapi_platform_core_phase7_v0_1.json` — candidate synchronous public operation bundle.
- `asyncapi_platform_events_v0_1.json` — candidate runtime event and notification bundle.
- `OFARM_PublicContractPackManifest_v0_1.json` — public/internal contract-pack boundary.
- `OFARM_PublicApplicationSurfaceManifest_example_core_phase7_v0_1.json` — combined candidate operation manifest through Phase 7.
- `ofarm_public_schema_catalog_v0_1.json` — public schema catalog with Phase 7 SDK/codegen entries.
- `ofarm_internal_schema_catalog_v0_1.json` — internal schema catalog; not SDK input.
- `ofarm_agent_tool_manifest_v0_1.json` — candidate agent-callable tool affordances.
- `phase7_public_operation_descriptors_v0_1.json` — Phase 7 discovery and SDK operation descriptors.

## Non-negotiable boundary

Generated SDKs and AI coding agents must consume only the public contract pack. Runtime storage models, platform module internals, internal projection stores, and conformance-only examples are not public app contracts.

## Safe generation path

1. Load `OFARM_PublicContractPackManifest_v0_1.json`.
2. Load `OFARM_PublicApplicationSurfaceManifest_example_core_phase7_v0_1.json`.
3. Load public OpenAPI/AsyncAPI and public schema catalog.
4. Generate thin operation-centric clients.
5. Apply SDK boundary assertions.
6. Fail generation if internal operations, storage paths, or generic CRUD truth helpers appear.
