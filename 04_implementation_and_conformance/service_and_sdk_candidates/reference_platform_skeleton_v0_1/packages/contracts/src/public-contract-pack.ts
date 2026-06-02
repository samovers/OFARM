// Public contract pack boundary.
// Generated clients consume public OpenAPI, AsyncAPI, public schema catalog, agent tool manifest, and reason-code registry.

export const PUBLIC_CONTRACT_PACK_INPUTS = [
  "openapi_platform_core_phase7_v0_1.json",
  "asyncapi_platform_events_v0_1.json",
  "ofarm_public_schema_catalog_v0_1.json",
  "ofarm_agent_tool_manifest_v0_1.json",
  "OFARM_RuntimeProblemReasonCodeRegistry_example_core_v0_1.json"
] as const;

export const INTERNAL_CONTRACTS_NOT_FOR_SDK = [
  "ofarm_internal_schema_catalog_v0_1.json",
  "platform module interfaces",
  "storage models"
] as const;
