
# OFARM Pack Merge Semantics — CP14 Surface Extension v0.1

Status: accepted/merged CP14 addendum; active RFC addendum below the active baseline

CP14 adds pack/profile surfaces for farm-to-farm intelligence boundary policy. These surfaces must not weaken farm data sovereignty, sharing/revocation law, recipient-use constraints, CP11 claim limits, CP12 mission/incident disclosure controls, CP13 farm-memory locality, or Advisory-default posture without explicit governance.

## CP14 pack surfaces

- FARM_INTELLIGENCE_SHARE_POLICY
- FARM_INTELLIGENCE_RECIPIENT_USE_POLICY
- FARM_INTELLIGENCE_DERIVATIVE_USE_POLICY
- FARM_INTELLIGENCE_TRAINING_USE_POLICY
- FARM_INTELLIGENCE_REVOCATION_POLICY
- REGIONAL_ALERT_POLICY
- BENCHMARK_DELTA_POLICY
- AGGREGATION_FLOOR_POLICY
- DEIDENTIFICATION_POLICY
- ANONYMISATION_POLICY
- REIDENTIFICATION_RISK_POLICY
- FEDERATED_LEARNING_CONTRIBUTION_POLICY
- CONTRIBUTION_QUALITY_POLICY
- POISONING_ANOMALY_REVIEW_POLICY
- CROSS_FARM_APPLICABILITY_POLICY
- INTELLIGENCE_OUTPUT_QUALIFICATION_POLICY

Default merge posture: strongest requirement for disclosure, privacy, evidence, recipient-use, training-use, revocation, and risk controls; hard fail on incompatible anonymisation, deidentification, aggregation, or public-disclosure semantics.
