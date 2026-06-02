# ADR 0001: Authority model for runtime evidence, generated artifacts, and agent indexes

## Status

Accepted

## Context

The repository contains overlapping representations of the same system concerns:

- runtime code and tests
- ontology, SHACL, SQL, rulepacks, report packs, and layout maps
- generated FADL/JSON artifacts and manifests
- static contract snapshots such as `specs/api/v1/openapi-farm-rm.yaml`
- stable package metadata under `specs/v1.0.0/`
- onboarding and implementation documents
- AI-facing routing files under `docs/ai/indexes/`

Without an explicit authority model, agents can follow the easiest document instead of the most authoritative repository evidence.

This is especially risky in this repo because:

- static OpenAPI metadata can drift from runtime and tests
- generated artifact catalogs do not prove one-to-one runtime coverage
- reporting scope is easy to over-generalize beyond current crops-first support
- planned `Operation*` abstractions coexist with already-implemented event-specific runtime paths

## Decision

Adopt this precedence order when sources conflict:

1. runtime implementation and tests
2. ontology, SHACL, SQL, rulepacks, report packs, layout maps, and other canonical source specs
3. generation scripts and authoritative manifests
4. stable release-package metadata under `specs/v1.0.0/`
5. static contract snapshots such as `specs/api/v1/openapi-farm-rm.yaml`
6. narrative onboarding and implementation notes
7. thread memory or prior summaries

Additional rules:

- Generated artifacts are derivative and must not be edited manually unless the repo evidence explicitly treats that family as authored.
- `docs/ai/indexes/` is a routing layer for agents, not a second source of truth.
- `AGENTS.md` defines agent operating behavior but does not override repository evidence.
- When an index or doc is stale, update the stale artifact rather than forcing the repo to match it.
- Generic logging/attestation `Operation*` abstractions are not runtime truth unless code and tests prove they are implemented.

## Consequences

Positive:

- agents have a deterministic conflict-resolution model
- cleanup and drift audits can start from repo truth
- generated artifacts stay downstream of their authored sources
- the external brain can stay lightweight without becoming a parallel architecture manual

Costs:

- agents must verify authority before editing
- index files must be refreshed when repo structure changes
- onboarding pages may need explicit drift markers when runtime moves faster than docs
