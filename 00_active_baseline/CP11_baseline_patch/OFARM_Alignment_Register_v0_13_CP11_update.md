# OFARM Alignment Register CP11 Update

Target file: `00_active_baseline/OFARM_Alignment_Register_v0_13.md`  
Status: CP11 final patch candidate

## Rows to add to Section 3 Register

| Concept | Area | Alignment class | External alignment | OFARM naming | Rationale |
|---|---|---|---|---|---|
| SustainableFarmingCharter | Governance / Sustainability | OFARM_OWNED | External sustainability schemes as anchors only | SustainableFarmingCharter | Governed charter object for sustainability constraints, objectives, evidence, claims, exceptions, breaches, and future autonomy hooks. |
| CharterApplicabilityContext | Governance / Context | OFARM_OWNED | Context/profile foundations only | CharterApplicabilityContext | Resolves farm, crop, scope, time, pack/profile, region, certification, claim, output, and use context for charter evaluation. |
| SustainabilityConstraint | Governance / Sustainability | OFARM_OWNED | Regulatory/certification/environmental standards as profile anchors only | SustainabilityConstraint | Hard non-tradeable sustainability constraints without allowing external schemes to become hidden law. |
| SustainabilityObjective | Advisory / Governance / Sustainability | OFARM_OWNED | Agronomic/environmental objective families as anchors only | SustainabilityObjective | Optimisable sustainability objectives that guide recommendations without conferring authority or overriding constraints. |
| ObjectivePriority | Governance / Sustainability | OFARM_OWNED | None | ObjectivePriority | Priority posture distinguishing non-tradeable floors, review-required priorities, optimisable objectives, report-only indicators, and experimental objectives. |
| TradeoffPolicy | Governance / Sustainability | OFARM_OWNED | None | TradeoffPolicy | Evaluation of allowed, qualified, review-required, prohibited, emergency-only, and insufficient-basis trade-offs. |
| SustainabilityEvidenceRequirement | Evidence / Sustainability | OFARM_OWNED | Evidence and attestation standards as anchors only | SustainabilityEvidenceRequirement | Consequence-sensitive evidence requirements for sustainability recommendations, outputs, claims, exceptions, and breaches. |
| SustainabilityMetricProfile | Evidence / Measurement / Sustainability | OFARM_OWNED | QUDT, PROV-O, method-specific standards as anchors | SustainabilityMetricProfile | Method, unit, uncertainty, freshness, source, and claim-eligibility profile for sustainability metrics. |
| SustainabilityClaimBasis | Output / Evidence / Sustainability | OFARM_OWNED | Claim/attestation standards as anchors only | SustainabilityClaimBasis | Basis for sustainability claims so weak, stale, inferred, or modelled values cannot masquerade as stronger claims. |
| SustainabilityOutputQualification | Output / Runtime / Sustainability | OFARM_OWNED | Result-qualification foundations only | SustainabilityOutputQualification | Sustainability-sensitive output disclosure of claim basis, evidence, freshness, uncertainty, authority, and allowed/prohibited use. |
| SustainabilityPolicyEvaluationTrace | Governance / Traceability / Sustainability | OFARM_OWNED | PROV-O foundations only | SustainabilityPolicyEvaluationTrace | Trace explaining how a charter-sensitive subject passed, failed, required review, or required qualification. |
| CharterApprovalGate | Authority / Sustainability | OFARM_OWNED | None | CharterApprovalGate | Approval requirements for charter-sensitive actions, claims, exceptions, breaches, priorities, packs, and budgets. |
| CharterException | Governance / Sustainability | OFARM_OWNED | Review/governance foundations only | CharterException | Scoped, evidence-linked, expiry-aware exception that does not delete or weaken the underlying charter rule. |
| CharterBreach | Governance / Sustainability | OFARM_OWNED | Nonconformity/corrective-action foundations only | CharterBreach | Suspected, confirmed, contested, resolved, superseded, false-positive, and exception-covered breach records without automatic compliance facts. |
| RiskBudget | Governance / Sustainability / Advisory | OFARM_OWNED | Risk-management standards as anchors only | RiskBudget | Bounded risk concept for charter-sensitive planning and future autonomous-operation hooks. |
| RegretBudget | Governance / Sustainability / Advisory | OFARM_OWNED | Experiment/risk-management ideas as anchors only | RegretBudget | Bounded downside concept for future experimentation and self-improvement hooks, with detailed trial law deferred to CP13. |

## CP11 alignment register addendum

CP11 promotes the Sustainable Autonomous Farming Charter concept family as OFARM-owned governance/sustainability surfaces for charter-sensitive use.

CP11 does not promote robot mission contracts, experimentation/farm-memory contracts, farm-to-farm intelligence contracts, or generated-software delivery contracts. Those remain future CP12, CP13, CP14, and CP15 work.

Residual debt: machine-contract final promotion, conformance fixture execution, sustainability metric-profile specialisation, live runtime evidence, farmer-facing comprehension evidence, external sustainability scheme review, and production/pilot validation.
