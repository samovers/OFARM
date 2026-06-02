# ADR 0005: Context-budgeted hot and cold routing for Codex

## Status

Accepted

## Context

The repository's Codex operational layer improved authority routing, but the default hot path still loaded too much advisory material before real code exploration. The largest recurring cost came from `docs/ai/indexes/symbol-index.yaml`, which mixed hot naming guidance with cold curated detail and generated discovery.

That design created two problems:

- common task routes paid a large fixed context cost before any task-specific repo search
- the heaviest symbol file was also doing three jobs at once: hot routing, deep curated evidence, and generated discovery

## Decision

Split the symbol and routing layer into hot and cold surfaces:

- keep `docs/ai/indexes/symbol-index.yaml` as the hot summary for naming-sensitive routing
- move deeper curated symbol evidence to `docs/ai/indexes/symbol-details.yaml`
- move generated runtime discovery and symbol warnings to `docs/ai/indexes/symbol-discovery.generated.yaml`
- add explicit `context_budget` targets to every reading path
- add a dedicated `change_operational_layer_routing` task route for operational-layer edits
- add `make ai-context-budget-report` and enforce hot-path budgets through `make ai-index-check`

## Consequences

### Positive

- lower default token burn for common Codex task routes
- clearer separation between always-hot guardrails and on-demand lookup material
- less duplication between `AGENTS.md`, `BRAIN.md`, and `reading-paths.yaml`
- budget regressions become visible in normal repo validation

### Negative

- more operational-layer files to keep coherent
- future contributors must understand when to stay on the hot summary and when to escalate to cold detail
- symbol split logic must stay aligned with `tools/ai_indexes.py`

## Guardrails

- runtime/tests/source specs remain authoritative over the operational layer
- naming-sensitive work must still route through `docs/ai/indexes/symbol-index.yaml`
- cold symbol files are on-demand lookups, not default hot context
- operational-layer changes must keep `AGENTS.md`, `BRAIN.md`, `reading-paths.yaml`, `change-checks.yaml`, `.codex/config.toml`, and `tools/ai_indexes.py` aligned
