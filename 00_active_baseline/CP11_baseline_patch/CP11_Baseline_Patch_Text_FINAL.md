# CP11 Final Baseline Patch Text

Date: 2026-05-21  
Status: final CP11 baseline patch candidate; controlled patch text only  
Scope: five affected active-baseline files

This file reconciles Phase 4 baseline patch planning with Phase 6 hostile review and Phase 6.1 remediation.

## Mandatory Phase 6.1 hardening overlay

The following hardening rules must be applied to the Phase 4 baseline patch text before merge:

1. **Approval-dependent charter states require explicit decision trace.**
   Active or approved exceptions, confirmed or resolved breaches, approved or active risk/regret budgets, and claim-ready/attestation-ready/filed sustainability claims require the relevant approval, authority, review, or decision trace.

2. **CP11 charters must declare non-bypass clauses.**
   The baseline should require CP11 charters to preserve truth, authority, evidence, freshness, Advisory/Compliance, agent-governance, robot-execution, and pack-core boundaries.

3. **Evidence type, evidence sufficiency, and freshness remain distinct.**
   The baseline must not allow evidence-status terms such as stale, insufficient, disputed, or invalidated to function as evidence source classes.

4. **Open-ended charter exceptions are invalid.**
   A CharterException must preserve the underlying rule and must carry a governed expiry posture.

5. **Sustainability claim readiness requires basis.**
   Claim-ready, attestation-ready, and filed sustainability claims require evidence sufficiency, freshness/materialisation basis where used, output disposition, output qualification where relevant, and authority/approval posture.

6. **Agent approval boundary is explicit.**
   Policy approval is not model confidence, tool success, workflow completion, prompt success, manifest support, or agent runtime success.

7. **Robot and machine execution remain out of scope.**
   CP11 charter evaluation, claim basis, output qualification, risk budget, and regret budget objects do not authorise robot missions, machine commands, or execution-bound autonomy.

8. **Sustainability pack surfaces must be merge-controlled.**
   CP11 sustainability surfaces require pack-surface family recognition and hard-fail or governance where conflicts exist.

9. **REPORT_ONLY_LIMIT is not a constraint strength.**
   Report-only posture belongs to objective/metric/priority surfaces, not hard constraints.

10. **Currentness remains bounded.**
    CP11 schema families remain draft/non-default until accepted and currentness maps are updated.

---

## Phase 4 baseline patch text, reconciled

# CP11 Phase 4 — Baseline Patch Plan

Date: 2026-05-21  
Status: draft baseline patch plan; not applied  
Depends on: `02_accepted_rfcs/OFARM_Sustainable_Autonomous_Farming_Charter_RFC_v0_1.md` draft candidate  
Patch posture: controlled addenda and narrow cross-reference updates only; no full rewrite

## Phase 4 verdict

CP11 should be baseline-harmonised through five controlled addenda:

1. Constitution addendum: CP11 model-law boundary and core charter concepts.
2. Platform Runtime addendum: charter gate placement in runtime enforcement.
3. Alignment Register addendum: CP11 concept classifications.
4. Readiness Gate addendum: CP11 claim limits and readiness posture.
5. Hostile Review addendum: CP11 hostile-reader interpretation and residual debt.

Do not rewrite the Constitution. Do not alter assertion/history-first truth, current-state materialisation, pack law, authority law, Advisory/Compliance split, query/output law, or agent law except to add CP11-specific hooks.

---

# 1. Patch target: `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`

## 1.1 Exact section to add or amend

Add a new addendum at the end of the file, after the existing `AAI-CP8 EvidenceNeed and ObservationRequest addendum — 2026-05-16`.

Recommended heading:

```md
## CP11 Sustainable Autonomous Farming Charter baseline addendum — 2026-05-21
```

Optional narrow cross-reference updates:

- In `### 1.2 Scope`, add one scope bullet: `sustainable autonomous farming charter rule classes, claim-basis discipline, and charter-sensitive output governance`.
- In `### 3.5 OFARM-owned semantic territory`, add one bullet: `sustainable autonomous farming charter, constraint, objective, trade-off, evidence, claim-basis, exception, and breach governance`.
- In `### 15.1 Minimum constitutional conformance baseline`, add CP11 conformance bullets listed below.

These cross-reference updates are useful but not strictly required if the addendum is inserted.

## 1.2 Proposed normative text

```md
## CP11 Sustainable Autonomous Farming Charter baseline addendum — 2026-05-21

Status: active baseline-law harmonisation candidate for CP11 once `OFARM_Sustainable_Autonomous_Farming_Charter_RFC_v0_1.md` is accepted.

This addendum introduces a bounded Sustainable Autonomous Farming Charter layer into the OFARM model law. It is a controlled extension. It does not replace the Constitution, does not create a second truth model, does not alter assertion/history-first authority, does not promote current-state materialisations into deeper truth, does not collapse Advisory Twin and Compliance Twin, and does not authorise robot, machine, or actuator execution.

### CP11-C.1 Charter purpose and boundary

The Sustainable Autonomous Farming Charter is OFARM's governed sustainability layer for crop-farming operational contexts. It defines how sustainability constraints, optimisation objectives, trade-offs, evidence requirements, claim-basis rules, approval gates, exceptions, breaches, risk budgets, and regret-budget hooks are represented and governed.

The charter is executable governance, not marketing prose. Every operative charter rule must be classifiable as one or more of:

- hard constraint;
- optimisation objective;
- evidence obligation;
- human approval gate;
- agent authority limit;
- robot authority hook;
- learning permission;
- data-sharing limit;
- exception rule;
- breach rule;
- claim-basis rule;
- output-qualification rule.

A charter rule, charter evaluation, sustainability objective, exception, breach record, or sustainability claim basis is not canonical farm truth merely because it exists. Any harder consequence must pass through existing OFARM truth, authority, evidence, review, promotion, current-state, output, sharing, and twin-boundary law.

### CP11-C.2 CP11 core concepts

The following CP11 concepts are baseline-recognised OFARM-governed concepts and must be represented in the Alignment Register before they are treated as constitutional core:

- `SustainableFarmingCharter`;
- `CharterApplicabilityContext`;
- `CharterRuleClass`;
- `SustainabilityConstraint`;
- `SustainabilityObjective`;
- `ObjectivePriority`;
- `TradeoffPolicy`;
- `SustainabilityEvidenceRequirement`;
- `SustainabilityMetricProfile`;
- `SustainabilityClaimBasis`;
- `SustainabilityOutputQualification`;
- `SustainabilityPolicyEvaluationTrace`;
- `CharterApprovalGate`;
- `CharterException`;
- `CharterBreach`;
- `RiskBudget`;
- `RegretBudget`.

These concepts may be detailed by accepted RFCs, companion artifacts, machine contracts, and conformance fixtures, but they may not be introduced silently through a pack, app, adapter, AI behaviour, dashboard, or external standard.

### CP11-C.3 Hard constraints and optimisation objectives

A `SustainabilityConstraint` is a non-tradeable or rule-bound charter condition that must not be violated under normal policy. A hard constraint may be overridden only through an explicit `CharterException` path if the active charter allows such an exception.

A `SustainabilityObjective` is an optimisation target used to compare, rank, recommend, simulate, plan, or explain candidate actions. An optimisation objective does not create authority, does not create truth, does not satisfy evidence sufficiency, and does not override a hard constraint.

A `TradeoffPolicy` must distinguish, at minimum, allowed trade-offs, review-required trade-offs, human-approval-required trade-offs, prohibited trade-offs, emergency-exception-only trade-offs, and insufficient-basis outcomes.

### CP11-C.4 Sustainability evidence, metrics, and claim basis

A sustainability-sensitive recommendation, plan, output, exception, breach finding, or claim-bearing artifact must declare its evidence posture according to the applicable `SustainabilityEvidenceRequirement`.

A `SustainabilityMetricProfile` must distinguish measured, sampled, lab-confirmed, machine-reported, sensor-derived, satellite-derived, modelled, inferred, estimated, self-declared, externally attested, certified, disputed, stale, and insufficient evidence postures where these distinctions are material.

A sustainability claim must not be produced, frozen, filed, exported, attested, or shown as claim-ready unless the required `SustainabilityClaimBasis` is present or the output clearly exposes that the claim basis is missing, insufficient, advisory-only, stale, disputed, or review-required.

Modelled or inferred sustainability values must not be represented as measured values. An AI summary, PassportView, DocumentAssembly, dashboard, generated document, or public operation result must not convert weak, stale, inferred, or partial evidence into stronger sustainability posture by presentation.

### CP11-C.5 Charter-sensitive current-state reliance

A charter-sensitive recommendation, charter evaluation, sustainability claim, exception, breach finding, or output that materially relies on current-state materialisation is a high-consequence use for the relevant materialisation basis.

Before such use, OFARM must ensure the relevant materialisation is freshly recomputed for that use or demonstrably still `FRESH` under the declared policy. If the materialisation is `STALE` or `INVALID`, the permitted outcomes are recompute, require review, require human approval, refuse action, refuse output, or another policy-declared blocked disposition.

### CP11-C.6 Advisory and Compliance Twin boundary for sustainability

Sustainability simulations, optimisation outputs, modelled natural-capital values, charter-risk flags, scenario results, and advisory sustainability recommendations belong to the Advisory Twin unless bridged through explicit OFARM governance.

Advisory sustainability material may request evidence, raise risk flags, generate scenario results, prepare a review package, propose a plan, propose a BridgeCandidate, or recommend a next step. It may not directly create a Compliance Twin fact, accepted executed consequence, official sustainability claim, charter breach with hard consequence, filed submission, attestation, or hidden current state.

### CP11-C.7 Charter authority and human-governed defaults

The following charter-sensitive actions are human-governed or human-approval-required by default unless a later active RFC explicitly relaxes the posture for a bounded action class:

- setting or changing objective priority;
- approving a prohibited or review-required trade-off;
- approving a charter exception;
- accepting, contesting, or resolving a charter breach with hard consequence;
- approving sustainability claim basis for high-consequence output;
- attesting or filing a sustainability claim;
- activating a pack/profile that changes sustainability constraints, evidence requirements, claim rules, or exception policy;
- approving risk or regret budgets where they affect high-consequence recommendations, experimentation, or future autonomous action.

A software agent may evaluate, recommend, simulate, explain, request evidence, prepare a dossier, or produce a charter evaluation trace only within its authority envelope. A software agent may not become a hidden governor of charter exceptions, objective hierarchy, claim attestation, pack activation, or Compliance Twin promotion.

### CP11-C.8 Charter exceptions and breaches

A `CharterException` is a governed, bounded, auditable override path. It is not a deletion of the rule. It must carry scope, time interval, affected rule, reason, evidence basis, approving authority, risk basis, expiry condition, review requirement, and output/claim consequence where applicable.

A `CharterBreach` records a suspected, confirmed, contested, resolved, superseded, false-positive, or exception-covered violation of a charter rule. A `CharterBreach` does not automatically become a legal nonconformity, Compliance Twin fact, accepted event consequence, or filed/attested claim unless a separate governed path creates that consequence.

### CP11-C.9 Pack/profile interaction

Packs and profiles may specialise charter constraints, objectives, evidence requirements, claim rules, metric profiles, trade-off policies, exception rules, and breach policies only through declared sustainability surface families and merge modes.

Sustainability pack/profile merge must fail closed where a conflict could weaken a hard constraint, hide an evidence requirement, misrepresent a metric method, alter claim basis, change objective priority without authority, or relax exception/breach policy without explicit governance.

External sustainability standards, buyer schemes, certification programmes, carbon methods, or environmental accounting methods may be admitted only as governed anchors, profiles, mappings, evidence sources, runtime-surface contracts, or attestation wrappers. They do not become hidden OFARM law, hidden truth stores, or hidden governance decisions.

### CP11-C.10 Deferrals

CP11 does not define robot mission law, command authority, geofence law, emergency-stop law, machine autonomy level, local fallback, physical safety incident law, or execution verification for cyber-physical systems. Those belong to CP12.

CP11 does not define the full experimentation, causal-learning, farm-memory, seasonal-learning, or learning-promotion model. Those belong to CP13.

CP11 does not define the full farm-to-farm intelligence, benchmark exchange, regional alert, federated learning, or derivative model-use boundary. Those belong to CP14.

CP11 does not define the full generated-software, adapter-generation, deployment, rollback, SBOM, or software-supply-chain governance model. Those belong to CP15.

CP11 does not expand OFARM beyond the crop-only release boundary into livestock identity, welfare, feeding, treatment, movement, herd/flock, or animal-health semantics.

### CP11-C.11 Non-claims

CP11 does not claim production sustainability-governance readiness, autonomous sustainability decisioning, robot/machine execution readiness, legal advice, certification advice, external sustainability-standard readiness, live environmental-registry integration, farm-to-farm intelligence readiness, generated-software deployment readiness, or livestock welfare readiness.
```

## 1.3 Reason for the change

This puts the stable CP11 constitutional content in one controlled addendum, matching the existing OFARM pattern for ONT-SEMINT and AAI addenda. It prevents a rewrite while making sustainability an executable governance concern.

## 1.4 Interaction with existing law

- Preserves assertion/history-first truth.
- Preserves current-state materialisation as derived and freshness-qualified.
- Preserves Advisory Twin / Compliance Twin split.
- Preserves authority default-deny and human-governed defaults.
- Preserves pack law, but adds sustainability surface hooks.
- Preserves AI/agent law by making agents evaluators/recommenders, not hidden governors.

## 1.5 Risk of contradiction

Low if inserted as an addendum. Main risks:

- `CharterBreach` could be misread as `NonConformity`; mitigated by explicit no-auto-compliance rule.
- `SustainabilityClaimBasis` could be confused with `TraceabilityClaimBasis`; mitigated by keeping the claim basis domain-specific.
- `RiskBudget` and `RegretBudget` could be mistaken for experimentation law; mitigated by CP13 deferral.

## 1.6 Baseline law now or RFC law

Baseline now:

- charter boundary;
- rule classes;
- no-truth/no-authority/no-execution rules;
- current-state freshness rule for charter-sensitive use;
- Advisory/Compliance boundary;
- human-governed defaults;
- exception/breach principles;
- deferrals and non-claims.

Remain RFC law:

- detailed fields;
- schema shapes;
- surface-family merge defaults;
- conformance fixture definitions;
- exact action-class rows.

## 1.7 Migration note

Existing OFARM artifacts are not retroactively charter-sensitive unless a pack/profile/context or accepted RFC declares such use. Existing sustainability prose, dashboards, reports, or AI summaries do not become CP11-compliant claims until they carry `SustainabilityClaimBasis` and required output qualification.

## 1.8 Conformance implication

Add conformance checks for:

- sustainability claim requires claim basis;
- stale materialisation blocks or qualifies claim-bearing output;
- hard constraint outranks optimisation objective;
- charter exception requires scope, expiry, evidence, and approval;
- `CharterBreach` does not auto-promote into compliance fact;
- agent cannot approve charter exception by default;
- sustainability pack conflict fails closed.

---

# 2. Patch target: `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`

## 2.1 Exact section to add or amend

Add a new runtime addendum at the end of the file, after the existing `AAI-CP8 request-layer runtime-surface addendum — 2026-05-16`.

Recommended heading:

```md
## CP11 Sustainable Autonomous Farming Charter runtime-enforcement addendum — 2026-05-21
```

Optional narrow cross-reference updates:

- In `### 3.1 EnforcementChain`, add `charter applicability and policy-evaluation gate where the use is charter-sensitive`.
- After `### 3.5 Pack/profile applicability gate`, add a short `### 3.5a Charter applicability and policy-evaluation gate` cross-reference.
- In `### 8.4 AI enforcement path`, add CP11 linkage for sustainability-sensitive agent runs.
- In `### 10.4 Output semantics`, add CP11 sustainability-claim output-basis requirement.

The end addendum is sufficient for Phase 4.

## 2.2 Proposed normative text

```md
## CP11 Sustainable Autonomous Farming Charter runtime-enforcement addendum — 2026-05-21

Status: active runtime baseline-law harmonisation candidate for CP11 once `OFARM_Sustainable_Autonomous_Farming_Charter_RFC_v0_1.md` is accepted.

This addendum extends the runtime enforcement posture for charter-sensitive recommendations, plans, outputs, claims, agent runs, exceptions, breaches, and pack/profile activations. It does not create a separate sustainability runtime, separate truth store, separate decision store, or cyber-physical execution authority.

### CP11-P.1 Charter-sensitive runtime surface

A runtime surface is charter-sensitive when sustainability constraints, optimisation objectives, evidence obligations, claim rules, exceptions, breaches, sustainability-disclosure limits, or future autonomous-operation hooks materially affect the result.

Charter-sensitive surfaces include, where applicable:

- sustainability-sensitive recommendations;
- sustainability-sensitive intervention plans;
- high-consequence plans with soil, water, biodiversity, chemical/input, erosion, residue, emissions, habitat, or charter constraints;
- sustainability scenario outputs intended for reliance beyond exploratory use;
- sustainability claim-bearing PassportViews, DocumentAssemblies, DossierAssemblies, SubmissionAssemblies, exports, dashboards, summaries, daily briefs, generated documents, and AI-facing outputs;
- charter exception or breach workflows;
- agent runs that prepare, evaluate, request approval for, or output charter-sensitive material;
- pack/profile activation that changes sustainability constraints, objectives, evidence rules, claim rules, trade-off rules, exception rules, or breach rules.

### CP11-P.2 Charter applicability gate

For a charter-sensitive use, the runtime must resolve the applicable `SustainableFarmingCharter` and `CharterApplicabilityContext` before presenting the result as operationally reliable, claim-ready, Compliance Twin eligible, execution-bound, or approved.

The applicability resolution must consider the relevant scope, time, target twin, output disposition, active pack/profile set, authority context, intended use class, and any governed external standard or certification reference admitted by profile.

If the applicable charter or applicability context cannot be resolved, the permitted runtime outcome is `REQUIRE_REVIEW`, `REQUIRE_HUMAN_APPROVAL`, `ADVISORY_ONLY`, `REFUSE_OUTPUT`, `REFUSE_ACTION`, or another policy-declared blocked disposition. It must not pass silently.

### CP11-P.3 Charter policy-evaluation gate

For a charter-sensitive use, the runtime must evaluate applicable hard constraints, objectives, objective priorities, trade-off policy, evidence requirements, approval gates, claim-basis rules, exception rules, and breach rules at the relevant consequence level.

The runtime must produce or link to a `SustainabilityPolicyEvaluationTrace` where the charter evaluation materially affects recommendation, review, approval, output, claim, exception, breach, pack activation, or future execution-bound packaging.

A charter evaluation trace records gate evaluation. It is not canonical farm truth, not evidence sufficiency by itself, not authority, not approval, not a Compliance Twin fact, and not proof of execution.

### CP11-P.4 Runtime outcomes

Where CP11 gates apply, the runtime must distinguish at least these outcomes:

- allowed;
- allowed with qualification;
- advisory-only;
- evidence-needed;
- require review;
- require human approval;
- blocked by hard constraint;
- blocked by stale or invalid current-state materialisation;
- blocked by insufficient claim basis;
- blocked by unresolved pack/profile conflict;
- exception path required;
- refused output;
- refused action.

A runtime may use implementation-specific reason codes, but they must preserve the material distinction among evidence failure, authority failure, freshness failure, hard-constraint failure, claim-basis failure, pack/profile conflict, and advisory-only limitation.

### CP11-P.5 Current-state and evidence coupling

A charter-sensitive result that materially relies on current-state materialisation must satisfy the existing high-consequence freshness rule. Stale, invalid, uncomputed, disputed, or insufficiently based materialisation must trigger recompute, review, human approval, refusal, or visible qualification according to policy.

Model confidence, AI fluency, tool-call success, public-operation success, or schema-shape validity is not sustainability evidence sufficiency and is not charter compliance.

### CP11-P.6 Sustainability claim output gate

A runtime must not emit, freeze, export, file, attest, or present as claim-ready a sustainability claim unless the relevant `SustainabilityClaimBasis` is present and the output exposes required `SustainabilityOutputQualification`.

Where the claim basis is missing, insufficient, stale, disputed, modelled-only, inferred-only, permission-limited, or review-required, the result must expose that limitation or refuse the stronger output disposition.

### CP11-P.7 Agent-run integration

A sustainability-sensitive software-agent run must preserve CP3, CP4, and CP5 agent law. It must link the relevant `AgentRunEnvelope`, `AgentRunTrace`, `AgentOutputDisposition`, `AgentBlockedActionTrace`, tool invocation trace, approval checkpoint, freshness requirement, and result qualification to the CP11 charter evaluation where the charter materially affects the run.

An agent may evaluate, recommend, simulate, explain, request evidence, prepare a review package, or propose a charter-sensitive output inside its authority envelope. It may not approve charter exceptions, change objective priority, activate charter packs, attest sustainability claims, create Compliance Twin facts, or authorise physical execution unless later active law explicitly grants that bounded action class.

### CP11-P.8 Pack/profile runtime interaction

When pack/profile activation touches sustainability surfaces, the runtime must evaluate merge legality and conflict posture before use. A conflict that could weaken a hard constraint, hide an evidence requirement, alter claim-basis rules, misrepresent a metric method, change objective priority, relax an exception rule, or conceal a breach posture must fail closed or require governance according to active pack law.

### CP11-P.9 Deferral and non-authorisation

CP11 runtime enforcement does not authorise robot or machine execution. A charter-passing evaluation is not a mission command, not a geofence, not a command signature, not an emergency-stop policy, not local fallback, not execution verification, and not a physical-safety proof.

CP11 runtime enforcement does not authorise autonomous experimentation, farm-to-farm intelligence exchange, or generated-software deployment. Those require later controlled amendments.

### CP11-P.10 Runtime non-claims

This addendum does not claim implemented production sustainability governance, autonomous sustainability decisioning, robot/machine execution readiness, external sustainability-standard readiness, live registry integration, legal/certification advice, farm-to-farm intelligence readiness, or generated-software deployment readiness.
```

## 2.3 Reason for the change

The Constitution defines CP11 model law; the Platform Runtime must state how CP11 is enforced at runtime without turning charter evaluation into truth or execution authority.

## 2.4 Interaction with existing law

- Extends `EnforcementChain` with a charter-sensitive gate.
- Reuses existing authority, evidence, materialisation, output, pack/profile, and agent gates.
- Preserves AAI-P.2: tool success is not governance success.
- Preserves AAI-P.5: world-model output is Advisory unless bridged.

## 2.5 Risk of contradiction

Low if phrased as additive runtime enforcement. Main risk is overburdening low-consequence exploratory advisory use. Mitigation: charter gates are required only where the use is charter-sensitive, high-consequence, claim-bearing, execution-bound, Compliance-bridged, or pack/profile activating.

## 2.6 Baseline law now or RFC law

Baseline now:

- runtime must recognise charter-sensitive use;
- runtime must resolve charter applicability for such use;
- runtime must produce/link evaluation trace when material;
- runtime must enforce claim-basis/output qualification;
- runtime must preserve agent and pack boundaries;
- CP11 is not physical execution authority.

Remain RFC law:

- exact trace fields;
- exact reason-code registry entries;
- exact schema locations;
- exact pack merge defaults;
- exact conformance fixtures.

## 2.7 Migration note

Existing runtime surfaces may continue as non-CP11 surfaces until they are declared charter-sensitive. Once declared, they must expose CP11 qualification rather than silently presenting old sustainability language as claim-ready.

## 2.8 Conformance implication

Add runtime tests for:

- unresolved charter context fails closed;
- charter evaluation trace required for sustainability-sensitive recommendation;
- stale materialisation blocks claim-bearing output;
- missing claim basis refuses claim-ready disposition;
- agent-run trace links charter gate;
- pack conflict blocks or requires governance.

---

# 3. Patch target: `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

## 3.1 Exact section to add or amend

Add a new section after the existing `AAI-CP8 alignment register addendum — 2026-05-16`.

Recommended heading:

```md
## CP11 Sustainable Autonomous Farming Charter alignment addendum — 2026-05-21
```

## 3.2 Proposed normative text

```md
## CP11 Sustainable Autonomous Farming Charter alignment addendum — 2026-05-21

Status: alignment-register candidate for CP11 once `OFARM_Sustainable_Autonomous_Farming_Charter_RFC_v0_1.md` is accepted.

CP11 introduces the following baseline-recognised charter-governance concepts. These concepts are not introduced by one pack, app, adapter, AI behaviour, dashboard, output template, or external sustainability standard.

| OFARM canonical concept | Main layer | Alignment class | Primary external semantic anchor(s) | Canonical naming choice | Reason for choice |
|---|---|---|---|---|---|
| SustainableFarmingCharter | Governance / Sustainability | OFARM_OWNED | Policy/governance foundations only | OFARM uses `SustainableFarmingCharter` | OFARM needs an executable charter object governing constraints, objectives, evidence, claims, exceptions, and breaches. |
| CharterApplicabilityContext | Governance / Context | OFARM_OWNED | Context/provenance foundations only | OFARM uses `CharterApplicabilityContext` | OFARM needs an explicit context object resolving which charter version and rules apply to a scope/time/twin/output/action. |
| CharterRuleClass | Governance | OFARM_OWNED | None | OFARM uses `CharterRuleClass` | OFARM needs its own rule-class taxonomy so charter prose becomes executable governance. |
| SustainabilityConstraint | Governance / Sustainability | OFARM_OWNED | Environmental policy and constraint foundations only | OFARM uses `SustainabilityConstraint` | OFARM needs non-tradeable or rule-bound sustainability constraints that cannot be optimised away. |
| SustainabilityObjective | Governance / Advisory / Sustainability | OFARM_OWNED | Multi-objective optimisation foundations only | OFARM uses `SustainabilityObjective` | OFARM needs objectives that guide recommendation and simulation without creating authority or truth. |
| ObjectivePriority | Governance | OFARM_OWNED | Priority/decision-policy foundations only | OFARM uses `ObjectivePriority` | OFARM needs explicit hierarchy so objectives are not flattened into arbitrary scoring. |
| TradeoffPolicy | Governance | OFARM_OWNED | Decision-policy foundations only | OFARM uses `TradeoffPolicy` | OFARM needs governed treatment of allowed, review-required, prohibited, emergency-only, and insufficient-basis trade-offs. |
| SustainabilityEvidenceRequirement | Evidence / Governance | OFARM_OWNED | PROV-O, SOSA/SSN, evidence-policy foundations | OFARM uses `SustainabilityEvidenceRequirement` | OFARM needs consequence-sensitive evidence requirements for sustainability decisions, exceptions, breaches, and claims. |
| SustainabilityMetricProfile | Evidence / Sustainability | OFARM_ALIGNED | QUDT, SOSA/SSN, PROV-O, ENVO/PECO where applicable, profile-declared external methods | OFARM uses `SustainabilityMetricProfile` | OFARM needs method, unit, uncertainty, measured/modelled/inferred posture, and claim eligibility around sustainability metrics without inventing all metric science. |
| SustainabilityClaimBasis | Output / Evidence / Governance | OFARM_OWNED | Provenance and claim-basis foundations only | OFARM uses `SustainabilityClaimBasis` | OFARM needs explicit basis for sustainability claims distinct from traceability claim basis and generic output evidence. |
| SustainabilityOutputQualification | Output / Governance | OFARM_OWNED | Result qualification foundations only | OFARM uses `SustainabilityOutputQualification` | OFARM needs material limitations for sustainability-sensitive and claim-bearing outputs. |
| SustainabilityPolicyEvaluationTrace | Traceability / Governance | OFARM_OWNED | PROV-O trace foundations only | OFARM uses `SustainabilityPolicyEvaluationTrace` | OFARM needs a traceable record of charter constraints, objectives, trade-offs, evidence, gates, and outcomes. |
| CharterApprovalGate | Authority / Governance | OFARM_OWNED | Authority/action-class foundations only | OFARM uses `CharterApprovalGate` | OFARM needs explicit approval gates for exceptions, objective changes, claim approval, and charter-sensitive actions. |
| CharterException | Governance / Audit | OFARM_OWNED | Exception/waiver governance foundations only | OFARM uses `CharterException` | OFARM needs bounded, scoped, evidence-linked, expiring exception records that do not delete the rule. |
| CharterBreach | Governance / Audit | OFARM_OWNED | Nonconformity/audit foundations only | OFARM uses `CharterBreach` | OFARM needs sustainability charter breach posture without automatically creating legal nonconformity or Compliance Twin fact. |
| RiskBudget | Governance / Advisory | OFARM_OWNED | Risk-management foundations only | OFARM uses `RiskBudget` | OFARM needs bounded risk allowances for sustainability-sensitive operations and future autonomy hooks. |
| RegretBudget | Governance / Advisory / Learning | OFARM_OWNED | Experimentation/risk foundations only | OFARM uses `RegretBudget` | OFARM needs bounded downside hooks for future experimentation and self-improvement without defining CP13 learning law here. |

### CP11 alignment consequences

CP11 strengthens OFARM-owned governance around sustainability, but it does not create a new sustainability truth substrate.

External sustainability standards, certification programmes, buyer schemes, carbon or natural-capital methods, and environmental accounting frameworks may be admitted as anchors, profiles, mappings, evidence sources, runtime-surface contracts, or attestation wrappers. They do not become hidden OFARM law by being referenced.

`SustainabilityMetricProfile` is intentionally `OFARM_ALIGNED`, not `OFARM_OWNED` in the scientific-method sense: OFARM owns the governed profile carrier, not the underlying measurement science. Quantity, unit, observation, provenance, environmental vocabulary, and method anchors remain external where appropriate.
```

## 3.3 Reason for the change

The Constitution requires every v2-must constitutional core concept to appear in the Alignment Register. CP11 introduces constitutional core concepts, so they need alignment classification.

## 3.4 Interaction with existing law

- Preserves external standards as anchors/profile inputs, not hidden law.
- Preserves no-hidden-core rule.
- Preserves OFARM ownership over operational governance concepts.

## 3.5 Risk of contradiction

Low. The main issue is whether `SustainabilityMetricProfile` should be `OFARM_OWNED` or `OFARM_ALIGNED`. Recommended classification is `OFARM_ALIGNED` because OFARM owns the carrier/profile discipline, not the external measurement methods.

## 3.6 Baseline law now or RFC law

Baseline now:

- concept names;
- alignment classes;
- no-hidden-core consequence.

Remain RFC law:

- exact field definitions;
- machine-contract schemas;
- conformance examples.

## 3.7 Migration note

Existing sustainability terms in packages, dashboards, reports, or notes are not constitutional CP11 concepts until mapped to the new registered concepts.

## 3.8 Conformance implication

Add alignment-register coverage checks for every CP11 machine contract and conformance fixture.

---

# 4. Patch target: `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

## 4.1 Exact section to add or amend

Add a new addendum after `AAI-CP10 final readiness and claim-limit addendum — 2026-05-17`.

Recommended heading:

```md
## CP11 Sustainable Autonomous Farming Charter readiness and claim-limit addendum — 2026-05-21
```

## 4.2 Proposed normative text

```md
## CP11 Sustainable Autonomous Farming Charter readiness and claim-limit addendum — 2026-05-21

CP11 updates readiness posture by adding a bounded Sustainable Autonomous Farming Charter governance layer. CP11 is a constitutional and contract-layer extension, not production sustainability-governance evidence.

### Bounded continuation posture

After CP11 acceptance, OFARM may claim bounded implementation-directed support for representing and evaluating sustainability charter governance concepts, including:

- sustainable farming charter identity and applicability context;
- sustainability constraints and optimisation objectives;
- objective priority and trade-off policy;
- sustainability evidence requirements;
- sustainability metric-profile posture;
- sustainability claim-basis requirements;
- sustainability output qualification;
- charter policy-evaluation traces;
- charter approval gates;
- charter exceptions and breaches;
- risk/regret budget hooks;
- CP11 interaction with Advisory Twin, Compliance Twin, current-state materialisation, packs, query/output surfaces, and agent runs.

This supports continuation of implementation and conformance work under controlled claim limits.

### Evidence currently required for stronger CP11 claims

Stronger CP11 readiness claims require:

- accepted CP11 RFC text;
- baseline harmonisation;
- Alignment Register updates;
- promoted CP11 machine-contract schemas;
- executed CP11 conformance fixtures;
- runtime traces proving charter applicability, policy evaluation, output qualification, evidence posture, claim-basis handling, stale-state refusal/review, pack conflict handling, and agent-run linkage;
- profile-specific review where external sustainability standards, certification schemes, buyer schemes, or environmental accounting methods are invoked;
- farmer-facing validation where CP11 requests, qualifications, limitations, or review gates affect operational workload or comprehension.

### Claims allowed after CP11 baseline acceptance

The package may claim:

- bounded constitutional support for sustainable autonomous farming charter governance;
- bounded RFC-level design for charter constraints, objectives, trade-offs, evidence, claims, exceptions, breaches, and evaluation traces;
- implementation-directed CP11 conformance path if machine contracts and fixtures are present;
- explicit deferral of robot execution, experimentation/farm memory, farm-to-farm intelligence, and generated-software governance to later controlled amendments.

### Claims still blocked after CP11

The package must not claim:

- production sustainability-governance readiness;
- autonomous sustainability decisioning;
- autonomous compliance decisioning;
- robot or machine execution readiness;
- cyber-physical safety readiness;
- legal advice;
- certification advice;
- external sustainability-standard readiness;
- live environmental or product-registry integration;
- full natural-capital accounting readiness;
- farm-to-farm intelligence readiness;
- federated learning readiness;
- generated-software deployment readiness;
- livestock welfare readiness;
- live farmer UX readiness for CP11 surfaces without separate validation.
```

## 4.3 Reason for the change

The readiness memo must prevent CP11 from being marketed as implemented autonomy or certification capability. CP11 changes governance law but does not by itself prove runtime, pilot, external-standard, certification, or robot readiness.

## 4.4 Interaction with existing law

Consistent with CP10 claim-limit posture: bounded active contracts and synthetic conformance are not production evidence.

## 4.5 Risk of contradiction

Low. The patch only narrows claims.

## 4.6 Baseline law now or RFC law

Baseline now:

- readiness/claim limits;
- CP11 non-claims.

Remain RFC/conformance law:

- specific fixture results;
- runtime evidence requirements;
- schema promotion evidence.

## 4.7 Migration note

Once CP11 is accepted, package status files should identify CP11 as a constitutional extension but not as a production readiness milestone.

## 4.8 Conformance implication

CP11 readiness claims must be blocked unless conformance artifacts exist and execute. Capability manifests must not advertise CP11 runtime readiness without evidence references.

---

# 5. Patch target: `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

## 5.1 Exact section to add or amend

Add a new addendum after `AAI-CP10 hostile-review closure update — 2026-05-17`.

Recommended heading:

```md
## CP11 Sustainable Autonomous Farming Charter hostile-review addendum — 2026-05-21
```

## 5.2 Proposed normative text

```md
## CP11 Sustainable Autonomous Farming Charter hostile-review addendum — 2026-05-21

A hostile reader should treat CP11 as a bounded constitutional extension that makes sustainability governable, not as proof that OFARM can autonomously run sustainable farming operations.

### Closed or substantially reduced by CP11

CP11 closes or materially reduces the following future-readiness gaps:

- sustainability is no longer only aspirational or output prose;
- hard sustainability constraints are distinguished from optimisation objectives;
- objective hierarchy and trade-off policy have a governed place in OFARM;
- sustainability evidence requirements and metric-profile posture are explicit;
- sustainability claims require claim basis and output qualification;
- charter-sensitive current-state reliance is tied to high-consequence freshness discipline;
- charter evaluation traces are required where charter gates materially affect outcomes;
- charter exceptions and breaches become governed records rather than ad hoc notes;
- agents may evaluate and recommend, but may not approve exceptions, attest claims, activate charter packs, or become hidden governors by default;
- packs/profiles that touch sustainability surfaces must merge safely or fail closed;
- CP12 through CP15 dependencies are explicitly deferred rather than silently assumed.

### Still open and hostile-reader relevant

CP11 does not close:

- production sustainability-governance readiness;
- live runtime implementation of charter gates;
- full CP11 machine-contract promotion until schemas are accepted;
- full CP11 conformance until fixtures are executed;
- robot/machine mission safety, geofence, command signing, emergency stop, autonomy-level, local fallback, and physical safety law;
- full experimentation, causal-learning, farm-memory, risk/regret-budget execution, and learning-promotion law;
- full farm-to-farm intelligence, benchmarking, regional alerts, federated learning, derivative use, and reidentification-risk law;
- generated-software deployment, adapter generation, rollback, SBOM, and software-supply-chain law;
- external sustainability-standard, certification, carbon/natural-capital method, or legal-advice readiness;
- livestock welfare or livestock operational semantics.

### Hostile-reader risks after CP11

The main remaining risks are:

- treating charter evaluation as truth;
- treating sustainability claim basis as certification;
- treating agent recommendation as approval;
- treating a charter-passing result as robot/machine execution authority;
- overburdening farmer-facing surfaces with evidence requests and qualifications;
- letting regional, buyer, or certification packs weaken core constraints or create hidden governance;
- overclaiming natural-capital precision from weak, modelled, or inferred evidence.

Verdict: CP11 is appropriate as a controlled extension if it ships with baseline harmonisation, Alignment Register updates, machine contracts, and conformance fixtures. It should not be treated as a green light for autonomous sustainability decisioning or cyber-physical execution.
```

## 5.3 Reason for the change

The hostile-review memo must reflect the new CP11 closure without overclaiming. It should guide future reviewers to attack the right residual risks.

## 5.4 Interaction with existing law

Consistent with the prior hostile-review posture: OFARM remains implementation-directed with bounded debt. CP11 changes what is closed enough, but it does not eliminate production/runtime/robot/federated-learning/generated-code debt.

## 5.5 Risk of contradiction

Low. This is interpretive and claim-limiting.

## 5.6 Baseline law now or RFC law

Baseline now:

- hostile-review interpretation;
- residual-risk map;
- non-claim guardrails.

Remain RFC/conformance law:

- exact machine-contract and fixture acceptance.

## 5.7 Migration note

Once CP11 is accepted, hostile-review and handoff materials should no longer say “sustainability charter absent” as a generic gap. They should instead say “CP11 charter law exists, but runtime implementation, conformance, CP12–CP15, and external-standard/livestock readiness remain bounded debt.”

## 5.8 Conformance implication

Hostile review should require CP11 conformance fixtures before allowing stronger claims. Future CP12–CP15 reviews must verify that they respect CP11 rather than bypass it.

---

# 6. Consolidated acceptance criteria for Phase 4

CP11 baseline harmonisation should be accepted only if:

1. The Constitution addendum preserves assertion/history-first truth and current-state materialisation law.
2. The Platform Runtime addendum makes charter evaluation a gate, not a truth store.
3. The Alignment Register contains every CP11 constitutional concept.
4. The readiness memo blocks production, autonomous, robot, certification, farm-to-farm, generated-software, and livestock claims.
5. The hostile review explicitly records what CP11 closes and what remains open.
6. CP11 does not define robot mission law, experimentation/farm-memory law, farm-to-farm intelligence law, or generated-software deployment law.
7. CP11 conformance fixture families are queued for Phase 5/6.

# 7. Files that should not be directly patched in Phase 4

Do not patch these baseline-adjacent files in Phase 4 except through RFC/conformance work:

- existing accepted RFCs beyond cross-reference notes;
- companion artifacts;
- machine-contract schemas;
- implementation/conformance runners;
- package status JSON files;
- legacy reference material.

Those belong to Phase 5 and Phase 6.
