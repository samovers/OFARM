# ADR 0003 — Codex operational layer

## Context

The repository already has a root `AGENTS.md`, a lightweight `BRAIN.md`, an onboarding pack, and an external-brain index layer. A symbol-index update also exists.

That stack improves authority routing and naming discipline, but it still leaves four operational gaps:

1. Codex can start work without a repo-local behavior profile.
2. Agents can miss the correct verification commands for a change.
3. Long-horizon tasks can still drift as context compacts across many turns.
4. Reusable repo-specific workflows are not packaged as skills.

The onboarding material already documents the authority order, runtime and reporting risks, and concrete build, test, and generation entrypoints that should drive this layer.

## Decision

Add an operational layer consisting of:

- `.codex/config.toml` for repo-local Codex behavior
- `docs/ai/indexes/change-checks.yaml` as the validation matrix
- repo-local skills under `.agents/skills/`
- long-horizon task-memory templates under `docs/ai/plans/templates/`

This layer remains secondary to repository truth.
It is not a second source of semantics.

## Consequences

### Positive

- More deterministic context loading and review behavior.
- Less chance of skipping critical repo-native checks.
- Lower risk of duplicate or drifting workflows because repeatable jobs become repo skills.
- Better inspectability for long multi-milestone tasks.

### Negative

- More operating files to maintain.
- The validation matrix and skill descriptions can themselves go stale if not refreshed.
- Repo-local config must stay conservative to avoid surprising user-level Codex behavior.

## Guardrails

- Keep `.codex/config.toml` minimal and project-scoped.
- If `change-checks.yaml` conflicts with real commands or tests, update it to repo truth immediately.
- Skills must stay narrow and should not become broad duplicate documentation.
- Task-memory templates are required for long-horizon work, not for every small edit.
