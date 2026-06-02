# OFARM SDK contracts candidate v0.1

Status: implementation/conformance support only.

This folder defines the SDK/codegen shape for an AI-agent-ready OFARM platform. SDKs must be generated from the public contract pack, not from runtime storage models or platform internals.

## Required SDK posture

- Thin, operation-centric clients.
- Capability bootstrap before execution.
- Public schema validation only.
- RuntimeProblem reason-code enums.
- Trace references and result-qualification envelopes preserved.
- Async listeners generated from AsyncAPI where supported.
- No direct helpers for canonical assertion-store, materialization-store, authority-state, promotion-state, or pack-activation-state mutation.

## Files

- `OFARM_SDK_Codegen_Manifest_v0_1.json`
- `OFARM_SDK_Boundary_Assertions_v0_1.json`
- `typescript/` candidate client shape and examples.
- `python/` candidate client shape and examples.
