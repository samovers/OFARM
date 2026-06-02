# OFARM Runtime QueryPlan target-equivalence fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact

## Purpose

These fixtures test whether semantically identical approved queries keep the same meaning after target-specific QueryPlanIR shaping across the bounded OFARM execution targets:

- `CURRENT_STATE_MATERIALIZATION`
- `READ_MODEL`
- `SEARCH_INDEX`
- `SEMANTIC_GRAPH`

The runner compiles target-shaped plans into canonical semantics, executes them over a bounded shared data model, compares canonical result digests, and emits explicit blocks when a target is insufficient or semantically divergent.

## Positive equivalence scenarios

1. field passport current-organic summary across all four targets
2. lot lineage descendant listing across read-model, search-index, and semantic-graph targets
3. evidence-backed spray-operation compliance listing across all four targets
4. frozen submission lookup across read-model and search-index targets
5. advisory zone-overlap view across read-model, search-index, and semantic-graph targets
6. advisory note search-and-hydrate across search-index and read-model targets

## Explicit blocked scenarios

1. compliance query on a search target that lacks a freshness gate
2. lot-passport query on a read-model target that silently drops a required stage filter

## Boundary

This wave is about **execution-target semantic equivalence**.
It does not replace:
- alias-governance stability tests
- graph-pattern equivalence tests
- deployment-produced executor telemetry
