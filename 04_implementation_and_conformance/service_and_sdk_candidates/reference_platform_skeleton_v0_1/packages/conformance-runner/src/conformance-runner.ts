// Conformance runner skeleton.
// Must execute contract and semantic-law gates before platform is called AI-agent-ready.

export const REQUIRED_PHASE7_GATES = [
  "public_contract_pack_validates",
  "sdk_generated_only_from_public_contracts",
  "internal_operations_absent_from_sdk",
  "skeleton_import_boundaries_enforced",
  "forbidden_sdk_methods_absent"
] as const;
