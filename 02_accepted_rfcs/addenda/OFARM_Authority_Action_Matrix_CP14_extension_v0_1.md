
# OFARM Authority Action Matrix — CP14 Extension v0.1

Status: accepted/merged CP14 addendum; active RFC addendum below the active baseline

Add CP14 action classes for farm-to-farm intelligence governance. Default posture is human-governed or human-approval-required for high-consequence disclosure, public release, training use, anonymisation, revocation resolution, or recipient-use expansion.

## CP14 action classes

- INTELLIGENCE_SHARE_GRANT_CREATE
- INTELLIGENCE_SHARE_GRANT_AMEND
- INTELLIGENCE_SHARE_GRANT_REVOKE
- INTELLIGENCE_PACKAGE_CREATE
- INTELLIGENCE_PACKAGE_RELEASE
- INTELLIGENCE_OUTPUT_APPROVE
- REGIONAL_ALERT_PUBLISH
- REGIONAL_ALERT_CORRECT
- REGIONAL_ALERT_WITHDRAW
- BENCHMARK_DELTA_RELEASE
- ANONYMISATION_CLAIM_APPROVE
- DEIDENTIFICATION_CLAIM_APPROVE
- REIDENTIFICATION_RISK_ACCEPT
- DERIVATIVE_USE_APPROVE
- TRAINING_USE_APPROVE
- FEDERATED_CONTRIBUTION_SUBMIT
- FEDERATED_AGGREGATION_ACCEPT
- MODEL_IMPROVEMENT_SIGNAL_RECORD
- REVOCATION_PROPAGATION_ACCEPT
- POISONING_OR_ANOMALY_REVIEW_ACCEPT
- CROSS_FARM_APPLICABILITY_ACCEPT

Software agents may prepare candidates, traces, and review packages under authority envelope. They may not approve public disclosure, anonymisation, training use, recipient-use expansion, or revocation closure by default.
