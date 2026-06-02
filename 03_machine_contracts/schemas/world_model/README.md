# world_model schemas

Status: active machine-contract lane added by AAI-CP7.

These schemas define the bounded advisory world-model contract layer. They do not create world-model readiness, production runtime readiness, a third AI Twin, current-state materialization, evidence sufficiency, or Compliance Twin mutation.

Promoted families:

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

`WorldModelCalibrationEvidence` remains unpromoted. Calibration references must point to existing governed evidence or package records until a later policy explicitly promotes a dedicated calibration-evidence contract.
