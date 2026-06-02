# ADR 0008: Backend audit boundary defaults for claim validation, report readiness, and stale profile recovery

## Status

Accepted

## Context

The backend-stack audit closed the highest-risk drift and completeness gaps, but it left three cross-layer boundary decisions that should not stay as local thread memory:

1. Claim validation already has a strong semantic owner in `specs/v0.1/validation/bin/validate-claim.sh`, while the FastAPI route and OpenAPI snapshot now expose a typed transport contract through `ClaimValidationRequest`, `ClaimValidationResponse`, and `ClaimValidationRuleResult`.
2. The additive operation-assessment layer now has a first-class `reportReady` field and `report_ready` lifecycle state, but Control Center review detail can still derive stricter binder-backed readiness from `reportBindings[]`.
3. Control Center now fails fast when an existing managed profile DB is stale, points the operator to the explicit reset path, and now also exposes that same reset path through a dedicated UI action.

Without one repo-level decision, later cleanup can reopen the same ambiguity:

- claim-validation ownership can drift back into "shell versus runtime" confusion
- assessment readiness can be mistaken for official-report readiness
- stale profile recovery can drift toward silent reset or silent auto-migration without proof

## Decision

Adopt these backend boundary defaults:

### 1. Claim validation

- Keep `specs/v0.1/validation/bin/validate-claim.sh` as the canonical semantic owner for claim validation.
- Keep the FastAPI route and checked-in OpenAPI snapshot as the typed transport wrapper around that semantic owner.
- Do not migrate claim-validation semantics into runtime Python without a separate deliberate batch and a new ADR or ADR update.

### 2. `reportReady`

- Keep additive assessment readiness and binder-backed official-report readiness as separate layers.
- Treat `assessment.reportReady` as additive workbench completeness for the covered generic operation families.
- Treat review-item or report-binding readiness as binder-backed official-report readiness.
- Do not collapse those meanings into one field or one promise unless runtime, binder logic, and tests prove a safe unification.

### 3. Stale managed-profile recovery

- Keep the current fail-fast rule for stale managed profile DB reuse.
- Keep the explicit reset/rebuild path as the supported recovery mechanism.
- Do not silently auto-migrate or silently reset existing managed profile DBs.
- A dedicated UI reset action is allowed as long as it keeps the same explicit reset semantics and does not become silent reset or silent auto-migration.

## Consequences

Positive:

- Claim-validation semantics stay anchored to the already-proven rulepack and schema owner.
- API consumers keep a typed transport contract without pretending the runtime wrapper is the semantic authority.
- Operators and later docs can distinguish additive readiness from official-report readiness without inventing a false single state.
- Managed profile DB safety stays conservative and explicit.

Costs:

- Claim validation remains split between shell semantics and Python transport.
- `reportReady` remains intentionally layered, which is less simple than a single readiness flag.
- Stale profile recovery still resets local profile-only data deliberately, so operators need to understand the confirmation before using it.

## Guardrails

- Keep `test_openapi_contract_alignment.py` guarding the typed claim-validation route contract.
- Keep docs describing the two-layer `reportReady` model explicitly.
- Keep stale managed-profile reuse fail-fast unless the repo later proves a safe auto-migration path with tests and documentation.
