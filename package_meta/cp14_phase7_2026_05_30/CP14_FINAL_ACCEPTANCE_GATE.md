
# CP14 Final Acceptance Gate

Status: final CP14 acceptance-gate candidate  
Date: 2026-05-30

## Validation summary

```text
schemaCount: 27
exampleCount: 27
allSchemasValid: True
allExamplesValid: True
fixtureCount: 69
positiveFixtureCount: 17
negativeFixtureCount: 52
allFixturesPassed: True
schemaAware: True
semanticHardeningAware: True
crossRecordAware: True
```

## Acceptance-gate recommendation

```text
Recommendation: proceed to CP14 final acceptance-gate review.
Do not merge without acceptance-gate review.
Do not promote CP14 schemas to current/default.
Do not start CP15 until CP14 is accepted and, if merged, steward-clean.
```

## Required acceptance checks

- Cross-farm intelligence remains Advisory by default.
- Farm-to-farm sharing is not authority.
- Received intelligence is not local truth or current state.
- Regional alerts are not farm-level occurrence truth.
- Benchmark deltas are not compliance facts.
- Aggregation does not equal anonymisation.
- Deidentification and anonymisation claims require re-identification-risk posture.
- CP11 sustainability, CP12 mission/incident, and CP13 learning/farm-memory boundaries are preserved.
- Federated-learning contribution does not create model deployment authority.
- Poisoning/anomaly review blocks downstream use where required.
- Machine contracts remain draft/non-default.


## CP14 Phase 7.2 cross-record policy/disclosure/federated-use hardening note

This package variant includes CP14 Phase 7.2 cross-record policy/disclosure/federated-use hardening. Machine contracts remain draft/non-default with schemaVersion `cp14-v0.1-draft-phase7-2-cross-record-policy-disclosure-federated-use-hardening`. The current conformance runner is `ofarm_cp14_phase7_2_conformance_runner.py`; Phase 6.1 runner is superseded.
