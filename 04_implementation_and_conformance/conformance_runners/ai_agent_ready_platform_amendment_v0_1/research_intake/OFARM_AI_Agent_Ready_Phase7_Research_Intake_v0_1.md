# OFARM AI-agent-ready Phase 7 research intake v0.1

Status: implementation/conformance support only.

## Research used

`deep-research-report-25.md`

## Phase 7 intake decisions

1. Public API and SDK generation should be driven by a layered public contract pack: OpenAPI, AsyncAPI, JSON Schema/catalog, agent tool manifest, and reason-code registry.
2. Generated SDKs should be thin, operation-centric clients. They must not expose generic CRUD helpers for canonical truth, materializations, promotion state, authority state, or pack activation state.
3. SDK bootstrap should fetch capability discovery, validate it, bind allowed operations, and execute only through public operation methods.
4. Async listeners should be generated from AsyncAPI where possible, rather than inferred by client applications.
5. Public/internal boundary checks should be build-enforced, not left as prose.
6. A reference platform skeleton should prevent AI coding agents from inventing module boundaries or importing platform internals into apps.

## Authority posture

Research informs implementation support only. Active OFARM baseline law continues to govern.
