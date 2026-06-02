# CP6 conformance fixture plan

## Goal

Execute hostile cases that test whether CP2 through CP5 controls behave as a runtime enforcement chain under synthetic conditions.

## Required pass conditions

- Each hostile block emits a reason code.
- Each block is trace retrievable.
- Tool success is recorded separately from governance outcome.
- No prohibited case mutates canonical truth or governed current state.
- Result qualification is present for stale, permission-limited, advisory-only, request-only, or review-bound outcomes.
- Handoff does not transfer authority.
- Revocation is checked at action time, answer time, share time, and offline replay time where relevant.

## Non-scope

Full Phase 9 execution, live deployment, production telemetry, external protocol interoperability, farmer UX acceptance, world-model promotion, and EvidenceNeed/ObservationRequest promotion.
