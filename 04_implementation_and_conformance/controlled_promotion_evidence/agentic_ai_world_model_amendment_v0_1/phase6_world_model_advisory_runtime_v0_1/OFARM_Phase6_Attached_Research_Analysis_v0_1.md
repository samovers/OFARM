# OFARM Phase 6 Attached Research Analysis v0.1

## Source input

`source_inputs/deep-research-report-28.md`

## Phase 6 conclusions from the research

The research supports the conservative OFARM amendment path. For world models, it recommends Advisory Twin placement, explicit assumptions, uncertainty, validity windows, invalidation rules, observed-outcome reconciliation, and hostile tests against scenario-to-truth leakage.

## Adopted into Phase 6

Phase 6 adopts these research-derived requirements:

1. `WorldModelRun`, `WorldModelState`, `ScenarioSpec`, `ScenarioResultSet`, `WorldModelAssumptionSet`, `WorldModelUncertaintyStatement`, and `WorldModelInvalidationRule` remain Advisory Twin material.
2. World-model state answers the seven practical questions: what observations grounded it, what assumptions extended it, what model/method produced it, what uncertainty applies, what validity window applies, what invalidates it, and how later observed outcomes are reconciled.
3. Invalidation rules trigger on time expiry, stale/missing observations, forecast divergence, crop-stage transition, management actions outside scenario bounds, pack/profile changes, materialization staleness, model version supersession, evidence conflict, or authority/sharing changes.
4. Reconciliation records compare scenario outputs to later observations for calibration and learning, but cannot mutate canonical history.
5. Output dispositions prevent scenario results from being treated as compliance facts.
6. Governance blockers explicitly record attempted misuse of world-model state.

## Not adopted as active law in this phase

The research's recommendations are not promoted into active baseline law in Phase 6. They are expressed as supporting RFC candidates, schemas, examples, and conformance planning material.

## Open architectural question left for later

Phase 6 does not define the farmer-facing `EvidenceNeed` or `ObservationRequest` contracts. Those remain Phase 7, but Phase 6 includes references to them because world-model results commonly generate bounded requests for missing evidence or observation.
