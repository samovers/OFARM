# OFARM AI-Agent-Ready Phase 6 Research Intake v0.1

Date: 2026-05-13

## Intake source

- `deep-research-report-25.md`

## Adopted as implementation support

Phase 6 adopts these research-supported patterns as implementation support, not baseline law:

1. Candidate-first sync and imports with idempotency keys, duplicate detection, conditional/precondition behavior, and explicit conflict payloads.
2. Governed unit conversion, formula versioning, rounding policy, and numeric test vectors instead of ad hoc UI logic.
3. Source-fidelity and loss-map envelopes for FMIS, machinery, sensor, weather, inventory, and other adapter inputs.
4. Result qualification and blocked-use posture for candidate-only, stale, disputed, unresolved, or evidence-insufficient practical-farm records.

## Rejected as incompatible shortcuts

- CRUD-first mutation of current-state materializations.
- Direct promotion of FMIS/machinery/sensor data to accepted truth.
- Last-write-wins conflict handling for canonical or promotion-sensitive state.
- Open-ended public schemas that allow packs or apps to mutate core OFARM meaning.
- AI-agent formula or identity guesses becoming governance decisions.

## Authority posture

The research informs Phase 6. Active baseline law governs. Minimum capture and FMIS shadow import remain draft/non-default until separately reviewed and promoted.
