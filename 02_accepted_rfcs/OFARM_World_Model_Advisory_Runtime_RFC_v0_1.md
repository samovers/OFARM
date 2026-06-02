# OFARM World Model Advisory Runtime RFC v0.1

Status: accepted RFC extension by AAI-CP7  
Date: 2026-05-16  
Authority tier: accepted RFC, subordinate to `00_active_baseline/`  
Scope: bounded advisory world-model runtime contracts only

## 1. Purpose

This RFC promotes a narrow active contract layer for advisory world-model and scenario execution.

The promoted layer lets OFARM represent a governed simulation run, its scenario specification, input basis, assumptions, uncertainty, validity window, invalidation rules, output disposition, advisory state, result set, governance blockers, and reconciliation record.

It does not promote world-model readiness, autonomous compliance decisioning, production runtime readiness, external-standard readiness, or a third AI Twin.

## 2. Governing rule

A world-model run is a governed Advisory Twin event. A world-model state is Advisory Twin material.

Neither one is canonical truth, Compliance Twin state, current-state materialization, evidence sufficiency, accepted event consequence, official output approval, or compliance basis by itself.

Any harder use requires the normal OFARM gates: bridge candidate, authority, evidence, freshness, review, promotion, sharing, output disposition, and result qualification.

## 3. Required semantic boundaries

1. `twinRef` for `WorldModelRun`, `WorldModelState`, and `ScenarioSpec` must resolve to `ADVISORY`.
2. `advisoryOnly` must remain true for world-model run/state/scenario/result artifacts.
3. World-model contracts may reference current-state materialization as input basis only; they may not mutate current state.
4. World-model state must carry horizon, uncertainty, validity, invalidation, provenance split, and reconciliation status.
5. Model confidence, simulated state, and scenario output are not evidence sufficiency.
6. A public or AI-facing answer based on world-model material must carry result qualification.
7. An invalidated or expired world-model output must be blocked, rerun, reviewed, or visibly qualified according to policy.
8. World-model output dispositions are limited to advisory results such as hypothesis, risk flag, scenario result, draft plan, candidate request, or BridgeCandidate proposal.
9. A bridge reference may be null. If non-null, it must point to a separately accepted bridge/review path; CP7 does not create shortcut promotion.
10. Runtime conformance cannot be claimed merely because the world-model schemas validate.

## 4. Promoted contract families

AAI-CP7 promotes these active machine-contract families under `03_machine_contracts/schemas/world_model/`:

- `WorldModelRun`
- `WorldModelState`
- `WorldModelInputBasis`
- `WorldModelObservationBasis`
- `WorldModelAssumptionSet`
- `WorldModelUncertaintyStatement`
- `WorldModelValidityWindow`
- `WorldModelInvalidationRule`
- `WorldModelOutputDisposition`
- `WorldModelGovernanceBlocker`
- `WorldModelReconciliationRecord`
- `ScenarioSpec`
- `ScenarioResultSet`

`WorldModelCalibrationEvidence` is deliberately not promoted. Calibration references must point to existing governed evidence, source-fidelity, model-card, or package records until a later RFC promotes a dedicated calibration-evidence contract.

## 5. Public-surface and result-qualification rule

If a result uses world-model material, the public surface must expose at least:

- Advisory-only status;
- simulation horizon;
- validity window;
- uncertainty summary;
- source/input basis limitations;
- invalidation status;
- reconciliation status;
- prohibited harder uses;
- required next gate for compliance or current-state use.

Suppression of these qualifications is a CP1/CP2 release-gate failure.

## 6. Conformance requirements

A CP7-conformant implementation or fixture must prove:

- a world-model run can be allowed for advisory use;
- a world-model state cannot materialize current state without a separately accepted bridge and normal promotion gates;
- a scenario result cannot become compliance basis without evidence, freshness, authority, review, and promotion gates;
- invalidated or expired world-model outputs are blocked, rerun, reviewed, or qualified;
- result qualification and trace retrieval identify the world-model basis and limitations.

## 7. Non-claims

CP7 does not claim:

- implemented world-model runtime readiness;
- production runtime readiness;
- two-agent compatibility;
- autonomous compliance decisioning;
- live model monitoring sufficiency;
- external-standard readiness;
- legal or agronomic advice.

CP7 is a controlled contract promotion and conformance-fixture phase only.
