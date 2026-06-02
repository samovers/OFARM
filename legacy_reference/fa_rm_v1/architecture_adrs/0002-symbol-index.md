# ADR 0002: Cross-layer symbol index for semantic and contract identity

## Status

Accepted

## Context

The repository spans semantic-core sources, runtime contracts, generated artifacts, reporting assets, local integrations, and tests.

This makes it easy for an agent to:

- recreate a concept under a near-duplicate name
- add a second request or response model that already exists
- confuse endpoint groups with transport models
- confuse rulepacks, report packs, layout maps, and control-pack surfaces
- rename or move code without understanding the cross-layer symbol identity it carries

The existing external-brain indexes route work by topic and authority, but they do not by themselves provide a cross-layer lookup of semantically-loaded symbols and aliases.

## Decision

Add `docs/ai/indexes/symbol-index.yaml` as a derivative cross-layer identity map.

The symbol index:

- tracks high-value semantic entities, transport models, endpoint groups, regulatory assets, compatibility-sensitive names, and other semantically-loaded symbols
- records canonical names, aliases, authority paths, related tests, and collision warnings
- is consulted before creating, renaming, moving, or consolidating code with semantic weight
- remains derivative; runtime, tests, and authoritative source specs still win when conflicts occur

The symbol index complements rather than replaces:

- `concept-index.yaml`
- `contract-index.yaml`
- authoritative repository files

## Consequences

Positive:

- lower duplicate concept and contract risk
- better naming discipline during cleanup and refactor work
- faster task-scoped retrieval for Codex
- an explicit place to record aliases, collisions, and compatibility-sensitive names

Costs:

- `symbol-index.yaml` needs refresh and review to avoid staleness
- some symbol ownership decisions still require human judgment
- automated ambiguity detection is heuristic and must remain review-only

## Implementation notes

- Keep `symbol-index.yaml` hybrid: curated canonical entries plus refreshable machine-derived sections.
- Prefer canonical repo paths over narrative descriptions.
- Add aliases instead of inventing alternate canonical names.
- Record uncertainty explicitly.
- Surface collisions and ambiguous near-duplicates for review; do not rename the repo automatically.
