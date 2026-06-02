# CP11 Sustainability Charter Draft/Non-default Schemas

These schemas are final CP11 draft candidates staged under `drafts_non_default`. They are not current/default active schemas until the CP11 acceptance gate is passed and `CONTRACT_FAMILY_CURRENTNESS.md` is updated.

# CP11 sustainability_charter schema family — draft

Status: draft CP11 machine-contract package; not active default law until CP11 is accepted and currentness maps are updated.

Authority source:
- `02_accepted_rfcs/OFARM_Sustainable_Autonomous_Farming_Charter_RFC_v0_1.md` draft
- CP11 baseline patch plan for Constitution, Platform Runtime, Alignment Register, readiness memo, and hostile review memo

Boundary:
- This family defines Sustainable Autonomous Farming Charter contract objects only.
- It does not define robot mission, geofence, command, emergency-stop, autonomy-level, or physical-safety schemas. Those are CP12.
- It does not define full trial design, causal-estimate, farm-memory, or seasonal-learning schemas. Those are CP13.
- It does not define farm-to-farm intelligence, federated-learning contribution, benchmark-delta, or regional-alert schemas. Those are CP14.
- It does not define generated-software artifact, deployment-candidate, SBOM, rollback, or adapter-generation schemas. Those are CP15.

Current draft schemas:

| Family | Schema |
|---|---|
| SustainableFarmingCharter | `OFARM_SustainableFarmingCharter_schema_v0_1.json` |
| CharterApplicabilityContext | `OFARM_CharterApplicabilityContext_schema_v0_1.json` |
| SustainabilityConstraint | `OFARM_SustainabilityConstraint_schema_v0_1.json` |
| SustainabilityObjective | `OFARM_SustainabilityObjective_schema_v0_1.json` |
| ObjectivePriority | `OFARM_ObjectivePriority_schema_v0_1.json` |
| TradeoffPolicy | `OFARM_TradeoffPolicy_schema_v0_1.json` |
| SustainabilityEvidenceRequirement | `OFARM_SustainabilityEvidenceRequirement_schema_v0_1.json` |
| SustainabilityMetricProfile | `OFARM_SustainabilityMetricProfile_schema_v0_1.json` |
| SustainabilityPolicyEvaluationTrace | `OFARM_SustainabilityPolicyEvaluationTrace_schema_v0_1.json` |
| CharterApprovalGate | `OFARM_CharterApprovalGate_schema_v0_1.json` |
| SustainabilityClaimBasis | `OFARM_SustainabilityClaimBasis_schema_v0_1.json` |
| SustainabilityOutputQualification | `OFARM_SustainabilityOutputQualification_schema_v0_1.json` |
| CharterException | `OFARM_CharterException_schema_v0_1.json` |
| CharterBreach | `OFARM_CharterBreach_schema_v0_1.json` |
| RiskBudget | `OFARM_RiskBudget_schema_v0_1.json` |
| RegretBudget | `OFARM_RegretBudget_schema_v0_1.json` |

Implementation note: these draft schemas use JSON Schema 2020-12, OFARM `schemaVersion` constants, explicit IDs/refs, strict `additionalProperties: false`, and trace/current-state/authority references rather than hidden runtime state.
