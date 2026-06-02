# OFARM Sustainable Autonomous Farming Charter RFC v0.1

Date: 2026-05-21  
Status: accepted CP11 RFC; merged as controlled OFARM 2 active substance on 2026-05-28
Authority tier: accepted RFC; subordinate to `00_active_baseline/` and above companion artifacts under `PROJECT_AUTHORITY.md`
Scope: introduce a bounded Sustainable Autonomous Farming Charter contract layer for sustainability constraints, objectives, trade-offs, evidence, claim basis, charter evaluation, approval gates, exceptions, breaches, and conformance implications without reopening OFARM truth, current-state, pack, authority, output, or agent law

---

## 1. Purpose

OFARM already has a strong semantic and governance spine:

- assertion/history-first canonical truth;
- governed current-state materialisation;
- one semantic substrate with Compliance Twin and Advisory Twin partitions;
- explicit authority, delegation, sharing, revocation, and default-deny posture;
- pack/profile law;
- query/output qualification and high-consequence output gates;
- sponsor-bound software-agent actorship;
- bounded agent run, trace, blocked-action, tool-manifest, and handoff law;
- advisory world-model boundaries.

That foundation is necessary but not sufficient for the future target where AI agents, simulations, generated workflows, farm-to-farm intelligence, and eventually robots may participate in farming operations.

The missing layer is a governed sustainability charter that tells OFARM:

- what may never be optimised away;
- what may be optimised;
- how objective conflicts are evaluated;
- what evidence is required for sustainability-sensitive decisions and claims;
- which decisions require human approval;
- how exceptions and breaches are recorded;
- how sustainability claims are qualified;
- how agents expose charter evaluation;
- how packs and profiles can safely specialise sustainability policy;
- what later cyber-physical, learning, exchange, and generated-software amendments must respect.

This accepted RFC introduces the first CP11 contract layer for a **Sustainable Autonomous Farming Charter**.

The core decision is:

```text
Sustainability is executable governance, not marketing prose.
Optimisation is subordinate to hard constraints.
Claims require explicit evidence basis.
Agents may evaluate and recommend, but may not become hidden governors.
Robot/machine execution, self-improvement, farm-to-farm intelligence, and generated-software deployment require later controlled amendments.
```

---

## 2. Scope

This RFC covers sustainability governance for crop-farming OFARM contexts already within the active baseline scope.

It defines:

- `SustainableFarmingCharter`;
- `CharterApplicabilityContext`;
- charter rule classes;
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
- `RiskBudget` and `RegretBudget` as bounded hooks;
- interactions with Advisory Twin, Compliance Twin, current-state materialisation, packs, query/output surfaces, and agent runs;
- machine-contract implications;
- conformance implications;
- explicit deferrals to CP12, CP13, CP14, and CP15.

This RFC applies to **charter-sensitive uses**, including:

- sustainability-sensitive recommendations;
- sustainability-sensitive planning decisions;
- high-consequence intervention plans where ecological, resource, input, safety, or charter constraints materially apply;
- sustainability-sensitive agent runs;
- sustainability scenario outputs intended for reliance beyond exploratory use;
- sustainability claims;
- sustainability claim-bearing PassportViews, DocumentAssemblies, DossierAssemblies, SubmissionAssemblies, exports, dashboards, summaries, or AI-facing outputs;
- charter exceptions and breaches;
- activation of packs or profiles that alter sustainability constraints, objectives, evidence rules, claim rules, or trade-off rules.

---

## 3. Non-goals

This RFC does **not**:

1. Rewrite the OFARM Constitution.
2. Reopen assertion/history-first canonical truth.
3. Reopen governed current-state materialisation.
4. Reopen the Compliance Twin / Advisory Twin split.
5. Reopen pack merge law except for sustainability-specific surface-family additions.
6. Reopen core authority law except for charter-specific action-class additions or mappings.
7. Create autonomous compliance decisioning.
8. Create robot or machine mission authority.
9. Define robot command, geofence, emergency-stop, autonomy-level, or cyber-physical safety law.
10. Define full experimentation, farm-memory, causal-learning, or seasonal-learning law.
11. Define farm-to-farm intelligence, federated learning, benchmark exchange, or regional-alert law.
12. Define generated-software deployment, rollback, adapter-generation, SBOM, or software-supply-chain law.
13. Expand OFARM from crop-farming operational law into livestock identity, animal welfare, herd/flock, feeding, treatment, or animal-health law.
14. Treat external sustainability standards, buyer schemes, carbon methods, or certification programmes as hidden OFARM law.
15. Define a universal sustainability metric catalogue.
16. Define legal advice, certification advice, or production sustainability-certification readiness.

The full cyber-physical mission envelope belongs to **CP12**.  
The full learning, experimentation, causal-evidence, and farm-memory model belongs to **CP13**.  
The full farm-to-farm intelligence and federated exchange boundary belongs to **CP14**.  
The full agentic software delivery and generated-code governance layer belongs to **CP15**.

---

## 4. Authority relationship to the Constitution

This RFC is a controlled extension to the active OFARM model law.

Until harmonised into `00_active_baseline/`, this RFC is subordinate to:

```text
00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md
00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md
00_active_baseline/OFARM_Alignment_Register_v0_13.md
```

If this RFC conflicts with the active baseline, the active baseline wins until explicitly amended.

This RFC does not create canonical truth outside existing OFARM channels. A charter rule, evaluation, objective, policy trace, exception, or breach record is not canonical farm truth merely because it exists.

Charter material may affect canonical or compliance-relevant outcomes only through existing OFARM gates:

- authority;
- validation;
- evidence sufficiency;
- review/promotion;
- current-state materialisation;
- output qualification;
- sharing/redaction;
- pack/profile applicability;
- Compliance Twin promotion where applicable.

This RFC introduces new constitutional concepts for later baseline harmonisation, but it does not itself rewrite the Constitution.

---

## 5. Authority relationship to Platform Runtime

The Platform Runtime must treat charter evaluation as a governed enforcement concern when a surface is charter-sensitive.

A runtime implementation that supports CP11 must be able to determine, for a relevant recommendation, plan, query, output, agent run, claim, exception, breach, or pack activation:

- which charter version applies;
- which applicability context applies;
- which hard constraints apply;
- which objectives apply;
- which trade-off policy applies;
- which evidence requirements apply;
- whether current-state materialisation is fresh enough for the intended use;
- whether the result is Advisory Twin only, Compliance Twin eligible, output eligible, claim eligible, review-required, or refused;
- which authority action class and approval gate applies;
- which qualifications or limitations must be exposed;
- which trace must be retained.

This RFC adds a charter gate concept to the runtime enforcement chain. It does not create a separate truth store, separate decision store, or separate sustainability runtime that may bypass OFARM governance.

A CP11 runtime fails conformance if it treats:

- a charter evaluation trace as canonical truth;
- a sustainability objective as authority;
- a sustainability claim as true without claim basis;
- modelled or inferred sustainability values as measured values;
- stale materialisation as adequate for high-consequence sustainability claims;
- agent confidence as evidence sufficiency;
- tool success as charter compliance;
- pack activation as safe when sustainability surfaces conflict unresolved.

---

## 6. Definitions

### 6.1 SustainableFarmingCharter

A governed charter object that declares the sustainability constraints, objectives, trade-off rules, evidence obligations, claim rules, approval gates, exception rules, breach rules, and use limitations applicable to one or more OFARM scopes.

A `SustainableFarmingCharter` is not a marketing statement. It is a governance object.

### 6.2 CharterApplicabilityContext

A governed context record that resolves which charter version and which charter clauses apply to a target farm, field, zone, crop cycle, lot, operation, output, agent run, pack activation, or other governed scope.

The context may include:

- farm or organisation scope;
- spatial scope;
- crop-cycle scope;
- temporal scope;
- active pack/profile set;
- certification or buyer-programme references where admitted by governance;
- jurisdictional or regional references where admitted by governance;
- target twin;
- intended use class;
- output disposition;
- authority context.

### 6.3 Charter-sensitive use

A use is charter-sensitive when sustainability constraints, objectives, evidence, claims, exceptions, breaches, sustainability-disclosure limits, or future autonomous operation materially affect the allowed result.

Examples include:

- intervention planning where soil, water, biodiversity, chemical/input, erosion, residue, emissions, or habitat policy applies;
- sustainability-sensitive recommendations;
- generated sustainability claims;
- sustainability dashboards intended for reliance;
- advisory scenario outputs presented as decision support;
- pack activation affecting sustainability policy;
- agent runs that prepare, evaluate, or request approval for charter-sensitive actions.

### 6.4 Hard constraint

A non-tradeable charter rule that must not be violated under normal policy.

A hard constraint may be overridden only through an explicit `CharterException` path if the active charter allows such exception.

### 6.5 Optimisation objective

A goal the platform may use to compare, rank, recommend, simulate, plan, or explain candidate actions.

An optimisation objective does not create authority, does not create truth, and does not override a hard constraint.

### 6.6 Evidence obligation

A charter requirement defining the evidence basis needed before a recommendation, plan, output, claim, exception, breach finding, or Compliance Twin bridge may proceed.

### 6.7 Sustainability claim

A claim, statement, assertion, label, output, dossier element, export field, or AI-facing result that represents a sustainability posture, result, status, improvement, compliance, certification-like state, environmental effect, resource efficiency, or charter conformance.

Examples include:

```text
regenerative
charter-compliant
soil-health improving
reduced nitrogen use
low pesticide-risk
water-efficient
biodiversity-positive
carbon-beneficial
residue-safe
habitat-protective
```

### 6.8 SustainabilityClaimBasis

The machine-readable basis explaining which evidence, metric method, scope, time interval, current-state materialisation, uncertainty, authority posture, approval state, and limitations support a sustainability claim.

A `SustainabilityClaimBasis` is distinct from `TraceabilityClaimBasis`, although a sustainability claim may reference a traceability claim basis where lot, chain-of-custody, or provenance semantics matter.

### 6.9 SustainabilityPolicyEvaluationTrace

A retrievable trace of how a charter-sensitive subject was evaluated under an applicable charter.

It records the applicable context, constraints, objectives, trade-off policy, evidence requirements, current-state basis, result, blocked reasons, approval requirements, exception posture, and output qualifications.

### 6.10 CharterException

A governed, bounded, auditable override or deviation from a charter rule.

An exception is not a deletion of the rule and does not rewrite the charter. It records a permitted exceptional posture for a defined scope, interval, reason, evidence basis, approval basis, and consequence.

### 6.11 CharterBreach

A governed record that a charter rule may have been, or has been, violated.

A `CharterBreach` may be suspected, confirmed, contested, resolved, superseded, false-positive, or exception-covered. It does not automatically become a legal compliance fact unless a separate Compliance Twin path promotes that result.

### 6.12 RiskBudget

A governed bound on acceptable risk exposure for a charter-sensitive scope, objective, constraint, time interval, or action family.

### 6.13 RegretBudget

A governed bound on acceptable downside for a future experimentation, learning, or self-improvement path.

This RFC introduces `RegretBudget` as a CP13 hook only. It does not define trial design or learning-promotion law.

---

## 7. Sustainable Autonomous Farming Charter

### 7.1 Core stance

OFARM may support autonomous and semi-autonomous farming only if sustainability remains governed by explicit constraints, objectives, evidence, approval, exception, and audit rules.

The charter layer must preserve these rules:

1. Canonical truth remains assertion/history-first.
2. Current state remains a governed materialisation.
3. Advisory Twin material remains advisory unless bridged through normal gates.
4. Compliance Twin facts require existing evidence, authority, review, and promotion gates.
5. Agents do not become hidden governors.
6. Packs do not mutate core meaning.
7. External sustainability standards do not become hidden law.
8. Sustainability claims require explicit claim basis.
9. Hard constraints outrank optimisation objectives.
10. Exceptions are bounded and auditable.

### 7.2 Charter composition

A `SustainableFarmingCharter` must identify or reference:

- charter identity;
- charter version;
- authority source;
- effective interval;
- scope;
- applicability context rules;
- hard constraints;
- optimisation objectives;
- objective priorities;
- trade-off policies;
- evidence obligations;
- metric profiles;
- claim-basis rules;
- output-qualification rules;
- approval gates;
- agent authority limits;
- cyber-physical charter preconditions;
- learning-boundary hooks;
- sustainability-disclosure limits;
- exception rules;
- breach rules;
- pack/profile merge posture;
- conformance requirements;
- non-claims and prohibited uses.

### 7.3 Charter-sensitive result outcomes

A charter-sensitive evaluation may produce these outcomes:

```text
ALLOW
ALLOW_WITH_QUALIFICATION
REQUIRE_REVIEW
REQUIRE_HUMAN_APPROVAL
REQUIRE_EVIDENCE
REFUSE
BLOCKED_BY_HARD_CONSTRAINT
BLOCKED_BY_AUTHORITY
BLOCKED_BY_FRESHNESS
BLOCKED_BY_EVIDENCE
BLOCKED_BY_PACK_CONFLICT
EXCEPTION_PATH_AVAILABLE
EXCEPTION_REQUIRED
ADVISORY_ONLY
INSUFFICIENT_BASIS
```

These outcomes are evaluation results. They do not, by themselves, create accepted farm truth, accepted execution truth, Compliance Twin fact, official output approval, or evidence sufficiency.

### 7.4 Charter does not create a third twin

CP11 does not create a Sustainability Twin.

Charter-related material must be placed in the existing semantic substrate and resolved through existing twin posture:

- advisory sustainability modelling and scenario outputs belong to the Advisory Twin by default;
- accepted sustainability-relevant facts, if promoted, belong to the Compliance Twin or canonical substrate under existing law;
- claim-bearing outputs must carry their output disposition and claim basis;
- materialisation remains governed and purpose-sensitive.

---

## 8. Rule classes

Every active charter rule must declare at least one `CharterRuleClass`.

The baseline CP11 rule classes are:

```text
HARD_CONSTRAINT
OPTIMISATION_OBJECTIVE
EVIDENCE_OBLIGATION
HUMAN_APPROVAL_GATE
AGENT_AUTHORITY_LIMIT
CYBER_PHYSICAL_CHARTER_PRECONDITION
LEARNING_BOUNDARY_HOOK
DATA_SHARING_LIMIT
EXCEPTION_RULE
BREACH_RULE
CLAIM_BASIS_RULE
OUTPUT_QUALIFICATION_RULE
METRIC_PROFILE_RULE
PACK_MERGE_RULE
```

### 8.1 Hard constraints

A hard constraint is a non-tradeable floor.

Examples:

- protected habitat no-go area;
- water contamination prohibition;
- legal buffer-zone rule;
- high erosion-risk prohibition;
- prohibited chemical/input condition;
- residue/contamination threshold;
- farm data-sovereignty boundary;
- commercial confidentiality boundary;
- anti-lock-in boundary;
- prohibited external sharing without grant.

A hard constraint may be specialised by profiles or packs only through safe merge rules. A lower-precedence pack may not weaken a hard constraint unless a higher-precedence governance path explicitly allows it.

### 8.2 Optimisation objectives

An optimisation objective guides comparison among allowed alternatives.

Examples:

- yield stability;
- margin resilience;
- water-use efficiency;
- nutrient-use efficiency;
- pesticide-risk reduction;
- soil-health improvement;
- erosion-risk reduction;
- biodiversity improvement;
- energy efficiency;
- emissions reduction;
- labour or machinery efficiency;
- operational resilience.

Objectives must not be treated as authority grants, truth records, execution instructions, or evidence sufficiency.

### 8.3 Evidence obligations

An evidence obligation defines the required evidence posture before a charter-sensitive use may proceed.

Evidence obligations may differ by consequence class:

- exploratory advisory use;
- recommendation;
- execution-bound plan;
- high-consequence output;
- sustainability claim;
- attested output;
- exception approval;
- breach confirmation;
- Compliance Twin bridge.

### 8.4 Human approval gates

Some charter-sensitive actions remain human-governed or human-approval by default.

At minimum, human approval is required by default for:

- approving charter exceptions;
- changing objective priorities;
- accepting confirmed charter breaches;
- contesting or resolving charter breaches where consequences are high;
- approving high-consequence sustainability claim basis;
- attesting sustainability claims;
- activating packs that materially alter sustainability constraints, evidence rules, claim rules, or objective priorities;
- approving risk budgets or regret budgets;
- bridging sustainability advisory material into compliance-relevant posture.

### 8.5 Agent authority limits

A software agent may, where authorised:

- evaluate charter applicability;
- run advisory checks;
- propose recommendations;
- propose plans;
- request evidence;
- generate `SustainabilityPolicyEvaluationTrace` candidates;
- prepare review packages;
- explain constraints and trade-offs;
- prepare draft claim basis;
- block or refuse an action when policy says so.

A software agent may not by default:

- approve a charter exception;
- change objective priority;
- attest a sustainability claim;
- activate a charter-altering pack;
- turn Advisory Twin material into Compliance Twin fact;
- treat tool success as policy success;
- treat model confidence as evidence sufficiency;
- command robots or machines by virtue of CP11.

### 8.6 Cyber-physical charter preconditions

CP11 may require future robot or machine mission law to evaluate charter constraints and objectives before execution.

CP11 does not define robot mission authority.

A future CP12 mission path must decide:

- mission identity;
- command authority;
- geofence/no-go zones;
- emergency stop;
- autonomy level;
- local fallback;
- human override;
- machine capability;
- execution telemetry;
- mission verification;
- safety incident handling;
- liability boundary.

### 8.7 Learning-boundary hooks

CP11 may define whether a charter permits bounded experimentation or self-improvement in principle.

CP11 does not define experiment design, causal inference, farm-memory promotion, seasonal learning, or model-update promotion.

A future CP13 learning path must respect:

- hard constraints;
- risk budgets;
- regret budgets;
- evidence obligations;
- Advisory/Compliance boundary;
- promotion law;
- farmer approval where required.

### 8.8 Sustainability-disclosure limits

A charter may limit sharing of sustainability data, benchmark data, regional alerts, claim evidence, or model-learning contributions.

A CP11 data-sharing limit must respect existing authority, sharing-grant, revocation, data-sovereignty, redaction, and permission-limited result law.

Full farm-to-farm intelligence law remains CP14.

### 8.9 Exception rules

An exception rule defines when a hard constraint or approval rule may be overridden under a bounded exception path.

An exception rule must specify:

- eligible constraint or rule;
- eligible scope;
- permitted reasons;
- required evidence;
- required approver;
- expiry condition;
- review requirement;
- output/claim consequence;
- breach relationship;
- disclosure requirements.

### 8.10 Breach rules

A breach rule defines how suspected, confirmed, contested, resolved, superseded, false-positive, or exception-covered charter violations are recorded and surfaced.

A breach record must not silently become a legal nonconformity, certification failure, compliance fact, or public claim unless a separate governed path does so.

---

## 9. Objective hierarchy

### 9.1 Core rule

A charter must declare how sustainability objectives are prioritised.

The objective hierarchy prevents a runtime from flattening all goals into an opaque score.

### 9.2 Priority classes

CP11 recognises these objective priority classes:

```text
NON_TRADEABLE_FLOOR
REVIEW_REQUIRED_PRIORITY
OPTIMISABLE_OBJECTIVE
REPORT_ONLY_INDICATOR
EXPERIMENTAL_OBJECTIVE
```

### 9.3 NON_TRADEABLE_FLOOR

A non-tradeable floor cannot be traded away under normal policy.

Examples:

- minimum legal buffer zone;
- protected habitat no-go condition;
- water contamination prohibition;
- data-sovereignty prohibition;
- safety-critical environmental threshold.

### 9.4 REVIEW_REQUIRED_PRIORITY

A review-required priority may be considered in trade-offs only through human or governance review.

Examples:

- substantial soil-degradation risk;
- uncertain biodiversity impact;
- material increase in water-use risk;
- high uncertainty around residue or contamination posture;
- material deviation from a farm-owned charter objective.

### 9.5 OPTIMISABLE_OBJECTIVE

An optimisable objective may be optimised by agents, simulations, planners, or recommendation services within applicable constraints.

Examples:

- yield stability;
- margin resilience;
- input efficiency;
- machinery efficiency;
- emissions intensity reduction.

### 9.6 REPORT_ONLY_INDICATOR

A report-only indicator is tracked and may appear in outputs, but does not by itself rank or block actions unless another rule binds it.

### 9.7 EXPERIMENTAL_OBJECTIVE

An experimental objective may be used only under governed trial, learning, or exploratory policy.

Full treatment is deferred to CP13.

### 9.8 No hidden global weighting

A runtime must not invent global weights for charter objectives unless the active charter or applicable governance path declares them.

Where weights, ranks, thresholds, or preference functions are used, the result must expose them through evaluation trace or result qualification where material.

---

## 10. Trade-off policy

### 10.1 Purpose

`TradeoffPolicy` defines how objective conflicts are evaluated.

It prevents hidden value choices such as:

- accepting erosion risk for yield;
- accepting water contamination risk for short-term margin;
- accepting weak evidence for operational speed;
- accepting privacy leakage for benchmarking value;
- accepting unsafe autonomy for labour efficiency.

### 10.2 Trade-off outcome classes

CP11 recognises these trade-off outcomes:

```text
TRADEOFF_ALLOWED
TRADEOFF_ALLOWED_WITH_QUALIFICATION
TRADEOFF_REQUIRES_REVIEW
TRADEOFF_REQUIRES_HUMAN_APPROVAL
TRADEOFF_PROHIBITED
TRADEOFF_EMERGENCY_EXCEPTION_ONLY
TRADEOFF_INSUFFICIENT_BASIS
```

### 10.3 Required traceability

A high-consequence, claim-bearing, execution-bound, or Compliance Twin-bridged result that depends on a trade-off must produce or link to a `SustainabilityPolicyEvaluationTrace`.

The trace must disclose:

- objectives compared;
- constraints applied;
- priority class;
- trade-off outcome;
- evidence basis;
- uncertainty or missing basis;
- approval requirement;
- output qualification.

### 10.4 Prohibited trade-offs

A trade-off is prohibited when:

- it violates a hard constraint;
- it relies on stale or insufficient basis for a high-consequence use;
- it requires an exception that has not been approved;
- it would require an authority action the actor does not hold;
- it would treat Advisory Twin material as Compliance Twin fact;
- it would disclose or share data without required grant;
- it would require robot/machine execution outside CP12 mission law.

---

## 11. Evidence model

### 11.1 Core rule

A sustainability-sensitive recommendation, plan, output, claim, exception, breach finding, or Compliance Twin bridge must declare its evidence posture.

Evidence posture must be consequence-sensitive. Exploratory advisory use may tolerate weaker evidence than a public sustainability claim or attested submission.

### 11.2 Evidence classes

CP11 recognises these sustainability evidence classes:

```text
MEASURED
OBSERVED
SAMPLED
LAB_CONFIRMED
MACHINE_REPORTED
SENSOR_DERIVED
SATELLITE_DERIVED
MODELLED
INFERRED
ESTIMATED
SELF_DECLARED
EXTERNALLY_ATTESTED
CERTIFIED
DISPUTED
STALE
INSUFFICIENT
PERMISSION_LIMITED
REDACTED
UNKNOWN
```

A runtime must not display weaker classes as stronger classes.

In particular:

- modelled is not measured;
- inferred is not observed;
- estimated is not certified;
- self-declared is not externally attested;
- stale is not current;
- permission-limited is not absent;
- redacted is not absent;
- missing evidence is not negative evidence unless policy says so.

### 11.3 Evidence requirements by use class

A `SustainabilityEvidenceRequirement` may apply to:

```text
ADVISORY_EXPLORATION
RECOMMENDATION
EXECUTION_BOUND_PLAN
HIGH_CONSEQUENCE_OUTPUT
SUSTAINABILITY_CLAIM
ATTESTED_CLAIM
CHARTER_EXCEPTION
CHARTER_BREACH_CONFIRMATION
COMPLIANCE_TWIN_BRIDGE
PACK_ACTIVATION
SHARING_OR_EXPORT
```

### 11.4 EvidenceNeed and ObservationRequest integration

When a charter-sensitive path lacks evidence, it may emit or link to existing `EvidenceNeed` or `ObservationRequest` objects.

A request-layer object remains a request. It is not evidence, not an obligation, not an accepted assertion, not a blocker by itself, and not a promotion decision unless a separate policy makes it so.

### 11.5 Source and interpretation separation

CP11 preserves existing OFARM separation between raw/source material and normalised interpretation.

A sustainability evidence basis must not hide:

- source record;
- normalised interpretation;
- method;
- model or calculation basis;
- unit/quantity basis;
- time interval;
- spatial extent;
- uncertainty;
- freshness;
- dispute/correction/supersession posture;
- permission/redaction posture.

---

## 12. Sustainability claim rules

### 12.1 Core rule

A sustainability claim requires `SustainabilityClaimBasis`.

No PassportView, DocumentAssembly, DossierAssembly, SubmissionAssembly, dashboard, AI summary, export, generated report, recommendation, or agent answer may present a sustainability claim as supported unless it carries or links to an adequate claim basis for the intended use.

### 12.2 Claim classes

CP11 recognises these claim classes:

```text
INTERNAL_ADVISORY_STATEMENT
FARM_MANAGEMENT_CLAIM
BUYER_FACING_CLAIM
CERTIFICATION_RELEVANT_CLAIM
ATTESTED_CLAIM
PUBLIC_OR_REGULATED_CLAIM
```

### 12.3 Claim basis fields

A `SustainabilityClaimBasis` should identify or reference:

- claim identity;
- claim class;
- claim text or claim code;
- subject scope;
- spatial extent;
- temporal interval;
- applicable charter version;
- metric profile;
- evidence requirement;
- evidence basis;
- current-state materialisation basis, if used;
- method/calculation basis;
- source-fidelity basis;
- uncertainty;
- limitations;
- freshness;
- dispute/correction/supersession posture;
- permission/redaction posture;
- authority decision;
- approval or attestation posture;
- allowed use classes;
- prohibited use classes;
- output disposition.

### 12.4 Weak basis cannot masquerade as strong basis

A weaker claim basis may be legitimate for some internal advisory uses.

It must not masquerade as:

- measured improvement;
- certified status;
- attested status;
- legal compliance;
- public claim eligibility;
- buyer-programme conformity;
- carbon or natural-capital claim readiness;
- Compliance Twin fact.

### 12.5 Sustainability claim and traceability claim relationship

`SustainabilityClaimBasis` is distinct from `TraceabilityClaimBasis`.

A sustainability claim may reference traceability claim basis when lot lineage, chain of custody, physical continuity, mass balance, book-and-claim, or other claim-accounting models materially affect the sustainability claim.

The two models must not be collapsed into a generic claim bucket.

### 12.6 Claim output behaviour

If a claim basis is absent, stale, insufficient, disputed, redacted, permission-limited, or Advisory-only, the output must:

```text
REQUIRE_REVIEW
REFUSE_OUTPUT
or ALLOW_WITH_QUALIFICATION
```

according to policy.

It must not pass silently.

---

## 13. Interaction with Advisory Twin

### 13.1 Advisory default

Sustainability simulations, optimisation outputs, modelled natural-capital values, risk flags, scenario comparisons, and draft plans are Advisory Twin material by default.

They may:

- suggest likely implications;
- compare candidate plans;
- request evidence;
- raise risk flags;
- prepare review packages;
- propose BridgeCandidates;
- explain trade-offs;
- prepare draft claim basis.

They may not by themselves:

- create accepted farm truth;
- create Compliance Twin fact;
- satisfy evidence sufficiency;
- approve output;
- approve exception;
- confirm breach;
- attest claim;
- command a machine;
- activate a pack;
- share data outside granted scope.

### 13.2 Scenario and world-model interaction

Where a sustainability result uses `WorldModelRun`, `WorldModelState`, `ScenarioSpec`, or `ScenarioResultSet`, the result must preserve Advisory-only posture unless bridged through normal gates.

A sustainability scenario result must expose:

- horizon;
- assumptions;
- uncertainty;
- validity window;
- invalidation rules;
- input basis;
- charter applicability context;
- prohibited harder uses;
- next gate required for harder use.

### 13.3 Bridge discipline

A sustainability Advisory Twin artefact may support a `BridgeCandidate`.

A bridge does not create shortcut promotion. Any harder use requires authority, evidence, freshness, review, promotion, sharing, output disposition, and result qualification gates.

---

## 14. Interaction with Compliance Twin

### 14.1 Compliance Twin preservation

CP11 does not weaken Compliance Twin standards.

Sustainability material may become Compliance Twin-relevant only through existing Compliance Twin gates.

### 14.2 Charter breach is not automatically compliance fact

A `CharterBreach` may be serious and may affect outputs or claims.

But it is not automatically:

- legal nonconformity;
- certification failure;
- regulatory breach;
- compliance assertion;
- accepted Compliance Twin fact;
- public disclosure obligation.

Those require separate governance paths.

### 14.3 Sustainability claim is not automatically compliance assertion

A sustainability claim may be advisory, farm-management, buyer-facing, certification-relevant, attested, or regulated depending on its claim class and approval posture.

Only a governed path may make it Compliance Twin-relevant.

### 14.4 Compliance outputs must carry charter basis where material

Where a Compliance Twin output, DocumentAssembly, SubmissionAssembly, attested package, or public-facing surface includes sustainability-sensitive claims or charter-sensitive reasoning, it must carry or link to:

- `SustainabilityClaimBasis` where claim-bearing;
- `SustainabilityPolicyEvaluationTrace` where evaluation-dependent;
- current-state materialisation basis where used;
- evidence sufficiency result;
- authority decision;
- output qualification.

---

## 15. Interaction with current-state materialisation

### 15.1 Current-state reliance rule

A charter-sensitive recommendation, evaluation, claim, exception, breach finding, or output that materially relies on current state must satisfy the relevant freshness and materialisation-basis requirements for the intended use.

### 15.2 High-consequence sustainability use

For high-consequence sustainability use, stale or invalid materialisation must trigger one of:

```text
RECOMPUTE
REQUIRE_REVIEW
REQUIRE_EVIDENCE
REFUSE_OUTPUT
ALLOW_WITH_QUALIFICATION
```

according to policy.

### 15.3 Current state does not become deeper truth

CP11 does not change the existing rule that current-state materialisation is derived from assertion/history, accepted consequences, review decisions, lifecycle state, packs/profiles, and context constraints.

A materialisation snapshot may be input basis for charter evaluation. It is not a new canonical truth layer.

### 15.4 Sustainability claim and current-state basis

If a sustainability claim uses current-state materialisation, the claim basis must expose:

- materialisation reference;
- materialisation scope;
- generated-at time;
- evaluation-time policy;
- basis records;
- freshness status;
- invalidation status;
- limitations;
- reconstruction trace where required.

---

## 16. Interaction with packs

### 16.1 Sustainability pack surfaces

CP11 adds these sustainability-relevant pack surface families for later Pack Merge Semantics extension:

```text
SUSTAINABILITY_CONSTRAINT
SUSTAINABILITY_OBJECTIVE
OBJECTIVE_PRIORITY
TRADEOFF_POLICY
SUSTAINABILITY_EVIDENCE_POLICY
SUSTAINABILITY_METRIC_PROFILE
SUSTAINABILITY_CLAIM_RULE
SUSTAINABILITY_OUTPUT_QUALIFICATION
CHARTER_EXCEPTION_POLICY
CHARTER_BREACH_POLICY
RISK_BUDGET_POLICY
REGRET_BUDGET_POLICY
DATA_SHARING_LIMIT
```

### 16.2 Merge posture

Default CP11 merge posture:

| Surface family | Preferred merge posture |
|---|---|
| `SUSTAINABILITY_CONSTRAINT` | `CONSTRAINT_INTERSECTION` or `STRONGEST_REQUIREMENT` |
| `SUSTAINABILITY_EVIDENCE_POLICY` | `STRONGEST_REQUIREMENT` |
| `SUSTAINABILITY_CLAIM_RULE` | `STRONGEST_REQUIREMENT` |
| `SUSTAINABILITY_OUTPUT_QUALIFICATION` | `STRONGEST_REQUIREMENT` |
| `SUSTAINABILITY_METRIC_PROFILE` | `IDENTICAL_ONLY` or `HARD_FAIL` where method conflicts |
| `OBJECTIVE_PRIORITY` | `ORDERED_COMPOSITION` only when explicit; otherwise `HARD_FAIL` |
| `TRADEOFF_POLICY` | `ORDERED_COMPOSITION` only when explicit; otherwise `HARD_FAIL` |
| `CHARTER_EXCEPTION_POLICY` | `STRONGEST_REQUIREMENT` or `HARD_FAIL` |
| `CHARTER_BREACH_POLICY` | `STRONGEST_REQUIREMENT` or `HARD_FAIL` |
| `DATA_SHARING_LIMIT` | `STRONGEST_REQUIREMENT` unless higher authority explicitly permits narrower release |

### 16.3 Pack conflict rule

If sustainability packs conflict and no declared safe merge applies, the platform must hard fail or require governance.

It must not silently:

- weaken a hard constraint;
- lower evidence requirements;
- reclassify a claim as stronger;
- replace a metric method;
- change objective priority;
- bypass an exception rule;
- relax sustainability-disclosure limits;
- treat an external standard as hidden law.

### 16.4 External sustainability schemes

External sustainability standards, certification programmes, buyer specifications, carbon methods, and natural-capital methods may be admitted as:

- semantic anchors;
- semantic profiles;
- exchange mappings;
- evidence or metric method references;
- attestation wrappers;
- pack/profile content;
- output/sharing constraints.

They do not become hidden OFARM law by being referenced.

---

## 17. Interaction with future CP12–CP15

### 17.1 CP12 — Cyber-Physical Mission Envelope

CP12 must define physical mission law.

CP11 requires only this boundary:

```text
A future robot or machine mission path must evaluate applicable charter constraints, objectives, evidence obligations, approval gates, exception rules, sustainability-disclosure limits, and output qualifications before execution where material.
```

CP11 does not create:

- `RobotMission`;
- `MissionPlan`;
- `GeoFence`;
- `CommandEnvelope`;
- `CommandSignature`;
- `AutonomyLevel`;
- `EmergencyStopPolicy`;
- `HumanOverridePolicy`;
- `MissionVerification`.

### 17.2 CP13 — Learning, Experimentation, and Farm Memory

CP13 must define trial, learning, causal-evidence, farm-memory, and learning-promotion law.

CP11 requires only this boundary:

```text
Future learning and self-improvement must remain inside hard constraints, approved risk/regret budgets, evidence requirements, Advisory/Compliance boundaries, and farmer authority.
```

CP11 does not create:

- `TrialDesign`;
- `ControlCondition`;
- `TreatmentPlan`;
- `CausalEstimate`;
- `FarmMemoryEntry`;
- `SeasonalLearningSummary`;
- `LearningPromotionDecision`.

### 17.3 CP14 — Farm-to-Farm Intelligence Boundary

CP14 must define farm-to-farm learning, benchmark exchange, regional alerts, aggregation floors, federated learning, derivative-use limits, and reidentification-risk controls.

CP11 requires only this boundary:

```text
Sustainability data sharing and benchmark use must respect data sovereignty, explicit grants, purpose limits, redaction, permission posture, and commercial confidentiality.
```

CP11 does not create:

- `FarmIntelligenceShareGrant`;
- `RegionalAlert`;
- `BenchmarkDelta`;
- `FederatedLearningContribution`;
- `ModelUpdateArtifact`;
- `AggregationFloor`;
- `DerivativeUsePolicy`;
- `ReidentificationRiskAssessment`.

### 17.4 CP15 — Agentic Software Delivery Governance

CP15 must define generated-software, adapter-generation, deployment, rollback, test, and supply-chain law.

CP11 requires only this boundary:

```text
Generated software that affects charter-sensitive paths must not bypass active OFARM authority, validation, conformance, traceability, evidence, output qualification, or charter gates.
```

CP11 does not create:

- `GeneratedSoftwareArtifact`;
- `AdapterGenerationRequest`;
- `SemanticMappingCandidate`;
- `ConformanceTestPlan`;
- `BuildProvenance`;
- `SBOMReference`;
- `DeploymentCandidate`;
- `CanaryResult`;
- `RollbackPlan`.

---

## 18. Machine-contract implications

This RFC requires a future CP11 machine-contract family under:

```text
03_machine_contracts/schemas/sustainability_charter/
```

### 18.1 Required first-wave contracts

CP11 should promote these schemas after schema drafting and conformance review:

```text
OFARM_SustainableFarmingCharter_schema_v0_1.json
OFARM_CharterApplicabilityContext_schema_v0_1.json
OFARM_SustainabilityConstraint_schema_v0_1.json
OFARM_SustainabilityObjective_schema_v0_1.json
OFARM_ObjectivePriority_schema_v0_1.json
OFARM_TradeoffPolicy_schema_v0_1.json
OFARM_SustainabilityEvidenceRequirement_schema_v0_1.json
OFARM_SustainabilityPolicyEvaluationTrace_schema_v0_1.json
OFARM_SustainabilityClaimBasis_schema_v0_1.json
OFARM_SustainabilityOutputQualification_schema_v0_1.json
OFARM_SustainabilityMetricProfile_schema_v0_1.json
OFARM_CharterApprovalGate_schema_v0_1.json
OFARM_CharterException_schema_v0_1.json
OFARM_CharterBreach_schema_v0_1.json
OFARM_RiskBudget_schema_v0_1.json
OFARM_RegretBudget_schema_v0_1.json
```

### 18.2 Contracts CP11 must reuse

CP11 must reuse, not duplicate, active contract families for:

```text
AuthorityGrant
AuthorizationDecisionRequest
AuthorizationDecisionResult
AuthorizationDecisionTrace
AgentActorshipBinding
AgentAuthorityEnvelope
AgentRunEnvelope
AgentRunTrace
AgentBlockedActionTrace
AgentToolInvocationTrace
AgentToolManifest
EvidenceNeed
ObservationRequest
EvidenceSufficiencyCase
MaterializationBasis
MaterializationSnapshot
ContextSnapshot
QuerySpecification
QueryPlanIR
ResultQualificationEnvelope
PackActivationSet
PackMergeResolutionTrace
PassportViewMetadata
PublicationAssemblyRequest
PublicationAssemblyResult
ReviewDecision
TraceabilityClaimBasis
WorldModelRun
WorldModelState
ScenarioSpec
ScenarioResultSet
```

### 18.3 Contracts CP11 does not promote

CP11 must not promote schemas for:

```text
RobotMission
MissionPlan
GeoFence
CommandEnvelope
CommandSignature
AutonomyLevel
EmergencyStopPolicy
HumanOverridePolicy
TrialDesign
CausalEstimate
FarmMemoryEntry
FarmIntelligenceShareGrant
FederatedLearningContribution
GeneratedSoftwareArtifact
DeploymentCandidate
RollbackPlan
```

Those belong to CP12–CP15.

---

## 19. Conformance implications

CP11 conformance must prove the charter is executable and does not override settled OFARM law.

A CP11-conformant implementation or fixture must prove at least:

1. A hard sustainability constraint blocks a high-yield or high-profit plan when the plan violates the constraint.
2. An optimisation objective cannot override a hard constraint.
3. A stale materialisation blocks, qualifies, or requires review for a sustainability claim.
4. Weak, modelled, inferred, or permission-limited evidence cannot support a stronger claim class without qualification.
5. A sustainability claim-bearing output requires `SustainabilityClaimBasis`.
6. A charter-sensitive agent recommendation links to `SustainabilityPolicyEvaluationTrace` or equivalent traceable evaluation.
7. A software agent cannot approve a charter exception by default.
8. Tool success does not equal charter compliance.
9. A charter exception requires scope, expiry, evidence, authority, and approval posture.
10. A charter breach does not automatically become a Compliance Twin fact.
11. A sustainability scenario result remains Advisory Twin material unless bridged through normal gates.
12. Conflicting sustainability pack surfaces hard-fail or require governance.
13. External sustainability standards do not become hidden OFARM law.
14. A data-sharing request for sustainability benchmark or claim material requires sharing authority and redaction/permission posture.
15. Result qualification exposes stale, advisory-only, evidence-insufficient, disputed, redacted, permission-limited, or claim-limited posture where material.

Recommended fixture family location:

```text
04_implementation_and_conformance/conformance_runners/sustainability_charter_conformance/
```

Recommended fixture names:

```text
charter_constraint_blocks_high_yield_plan
objective_cannot_override_hard_constraint
stale_materialization_blocks_sustainability_claim
weak_evidence_downgrades_claim_basis
agent_recommendation_requires_charter_evaluation_trace
agent_cannot_approve_charter_exception
sustainability_claim_requires_claim_basis
charter_exception_requires_scope_expiry_evidence_approval
charter_breach_does_not_auto_create_compliance_fact
regional_pack_adds_stricter_constraint_by_safe_merge
conflicting_sustainability_pack_rules_hard_fail
world_model_sustainability_scenario_remains_advisory
data_sharing_request_requires_grant
claim_basis_distinguishes_measured_modelled_inferred
```

---

## 20. Migration notes

### 20.1 Baseline harmonisation

After acceptance, CP11 should be harmonised into the active baseline through a narrow patch to:

```text
00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md
00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md
00_active_baseline/OFARM_Alignment_Register_v0_13.md
00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md
00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md
```

The baseline patch should add only:

- charter authority and non-goal statement;
- CP11 concept references;
- charter-sensitive high-consequence use rule;
- charter evaluation gate posture;
- agent/AI boundary note;
- pack/profile boundary note;
- non-claims and readiness limitations.

It should not rewrite the Constitution.

### 20.2 Alignment Register

The Alignment Register should add CP11 concepts and classify each as:

```text
OFARM constitutional core
OFARM-owned extension concept
external-anchor/profile-admissible concept
machine-contract-only concept
future-amendment hook
```

### 20.3 Authority Action Matrix

The Authority Action Matrix should add or map charter-specific actions such as:

```text
CHARTER_EVALUATE_POLICY
CHARTER_SET_OBJECTIVE_PRIORITY
CHARTER_APPROVE_EXCEPTION
CHARTER_ACCEPT_BREACH_FINDING
CHARTER_CONTEST_BREACH_FINDING
CHARTER_RESOLVE_BREACH
CHARTER_APPROVE_CLAIM_BASIS
CHARTER_ATTEST_SUSTAINABILITY_CLAIM
CHARTER_ACTIVATE_POLICY_PACK
CHARTER_APPROVE_RISK_BUDGET
CHARTER_APPROVE_REGRET_BUDGET
```

Default posture should be human-only or human-approval by default for high-consequence charter governance actions.

### 20.4 Pack Merge Semantics

Pack Merge Semantics should add sustainability surface families and merge-mode defaults from section 16.

### 20.5 Query and output hardening

High-consequence query/output hardening should treat sustainability claims and charter-sensitive outputs as high-consequence where they materially affect:

- Compliance Twin use;
- claim-bearing output;
- publication/export;
- buyer/certifier-facing output;
- regulated or attested output;
- execution-bound planning;
- human approval gate.

### 20.6 Evidence policy

Evidence Sufficiency and Evidence Quality companion artifacts should add sustainability-specific evidence-class interpretation.

### 20.7 Capability manifests

Capability manifests and agent tool manifests should declare whether a runtime/tool/agent supports CP11 and which charter-sensitive surfaces it can evaluate, qualify, or refuse.

Capability support does not grant authority.

### 20.8 Readiness and non-claims

CP11 acceptance does not create:

- production sustainability governance readiness;
- autonomous sustainability decisioning readiness;
- robot/machine execution readiness;
- legal advice;
- certification readiness;
- external sustainability standard readiness;
- live environmental registry integration;
- livestock welfare readiness;
- farm-to-farm intelligence readiness;
- generated-software deployment readiness.

These non-claims should be explicit in readiness and hostile-review material.

---

## 21. Risks and open questions

### 21.1 Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Charter becomes values prose | high | Require rule classes, machine contracts, and conformance fixtures |
| Charter overrides truth law | existential | State that CP11 never creates truth outside assertion/history and accepted gates |
| Objectives override constraints | high | Define non-tradeable floors and trade-off outcomes |
| Agents become hidden governors | existential | Add charter authority actions and human-governed defaults |
| Sustainability claims become greenwashing | high | Require `SustainabilityClaimBasis`, output qualification, and evidence classes |
| Modelled values masquerade as measured values | high | Require `SustainabilityMetricProfile` and evidence-class disclosure |
| Packs weaken constraints | high | Add sustainability pack surfaces and strong merge defaults |
| External standards become hidden law | high | Keep external standards as anchors/profiles/mappings/attestation wrappers only |
| CP11 accidentally authorises robots | high | Explicitly defer mission law to CP12 |
| CP11 accidentally becomes experimentation law | medium/high | Introduce only risk/regret budget hooks; defer learning law to CP13 |
| CP11 overburdens exploratory advisory use | medium | Apply heavy gates to high-consequence, claim-bearing, execution-bound, or Compliance-bridged uses |
| CP11 overclaims readiness | high | Add non-claims to readiness and capability surfaces |
| Legal/certification compliance blurs with charter compliance | high | Keep legal/certification paths separate unless explicitly bound |
| Crop-only baseline is silently expanded | medium/high | Keep livestock law out of CP11 except future hooks |

### 21.2 Open questions

1. Should the active baseline promote `SustainableFarmingCharter` immediately after RFC acceptance, or should it remain RFC-only until conformance fixtures pass?
2. Should `SustainabilityMetricProfile` be P0 or P1 for CP11 machine contracts?
3. Which charter authority action classes should be new values versus mappings onto existing govern/decide, output approval, attestation, context-governance, and share/revoke families?
4. How strict should CP11 be for purely internal advisory dashboards that contain sustainability language but no formal claim?
5. Which sustainability claim classes require human approval by default?
6. Should CP11 define a minimal default charter, or only the structure for active charters?
7. How should buyer or certification programme packs be prevented from weakening farm sovereignty while still allowing stricter rules?
8. Which metric-method conflicts should hard-fail rather than be qualified?
9. Should charter breaches have lifecycle states aligned with existing nonconformity/corrective-action records, or remain a separate charter-specific family until later harmonisation?
10. Should risk budgets be actionable in CP11, or only definitional until CP13?
11. Should external sustainability standards be added to the standards alignment register now, or deferred until concrete profile packs exist?
12. What is the minimal CP11 conformance fixture suite required before baseline harmonisation?

---

## 22. Acceptance gate for CP11

CP11 should not be accepted unless hostile review confirms that it:

- does not rewrite OFARM truth law;
- does not create a third twin;
- does not let sustainability objectives override hard constraints;
- does not let agents approve exceptions or attest claims by default;
- does not authorise robot or machine execution;
- does not create farm-to-farm intelligence law;
- does not create generated-software deployment law;
- does not let packs weaken core meaning;
- does not let external sustainability standards become hidden law;
- requires claim basis for sustainability claims;
- requires traceability for charter-sensitive evaluation;
- respects current-state freshness and output qualification;
- has a clear machine-contract plan;
- has a clear conformance-fixture plan;
- states non-claims and remaining bounded debt.

---

## 23. Phase 7 reconciliation and hardening clauses

This section incorporates the Phase 6 hostile-review and Phase 6.1 remediation findings. Where this section is more specific than earlier CP11 draft text, this section controls for the final CP11 amendment package candidate.

### 23.1 Non-bypass clauses

A `SustainableFarmingCharter` must carry these non-bypass clauses:

```text
NO_TRUTH_BYPASS
NO_AUTHORITY_BYPASS
NO_EVIDENCE_BYPASS
NO_FRESHNESS_BYPASS
NO_ADVISORY_TO_COMPLIANCE_SHORTCUT
NO_AGENT_GOVERNANCE_BY_DEFAULT
NO_ROBOT_EXECUTION_AUTHORITY
NO_PACK_CORE_MUTATION
```

It must also carry explicit deferrals:

```text
CP12_CYBER_PHYSICAL_MISSION
CP13_LEARNING_EXPERIMENTATION_FARM_MEMORY
CP14_FARM_TO_FARM_INTELLIGENCE
CP15_AGENTIC_SOFTWARE_DELIVERY
```

A CP11 charter object must not create canonical truth, authorise execution, override authority law, override pack law, authorise robot missions, authorise machine commands, or bypass the need for CP12 before physical execution.

### 23.2 Approval-dependent states

A state that depends on approval is invalid unless the relevant `CharterApprovalGate`, `AuthorityDecisionTrace`, `ReviewDecision`, or equivalent governance decision is linked.

This applies at least to:

- active or approved `CharterException`;
- confirmed, resolved, or exception-covered `CharterBreach`;
- approved or active `RiskBudget`;
- approved or active `RegretBudget`;
- `SustainabilityClaimBasis` with `CLAIM_READY`, `ATTESTATION_READY`, or `FILED` readiness.

### 23.3 Evidence source, evidence quality, and freshness separation

CP11 must not conflate evidence source/type, evidence quality/status, and freshness.

The machine-contract model must separate:

```text
evidenceSourceClass
minimumEvidenceQualityState
freshnessRequirement
```

`INSUFFICIENT`, `STALE`, `DISPUTED`, and `INVALIDATED` are not evidence source classes. They are quality, sufficiency, or freshness states.

### 23.4 Trade-off defaults

For high-consequence use, absence of a matching trade-off rule must not default to allow.

The default outcome of a `TradeoffPolicy` must be one of:

```text
REQUIRE_REVIEW
REQUIRE_HUMAN_APPROVAL
REFUSE
INSUFFICIENT_BASIS
EMERGENCY_EXCEPTION_ONLY
```

`ALLOW_WITH_QUALIFICATION` is allowed only at individual rule level and only when the rule proves:

- target twin is Advisory;
- no hard constraint is implicated;
- no claim-bearing output is produced;
- no execution-bound preparation occurs;
- output qualification is required.

### 23.5 Agent approval boundary

Policy approval is not model confidence, tool success, workflow completion, manifest support, or agent runtime success.

By default, software agents must not approve charter exceptions, attest sustainability claims, set objective priority, activate charter-sensitive policy packs, accept breach findings, resolve breach findings, approve risk budgets, or approve regret budgets.

Those high-governance action classes require `HUMAN_ONLY`, `HUMAN_APPROVAL_REQUIRED`, or `POLICY_APPROVAL_REQUIRED` with an explicit authority-decision trace.

### 23.6 Charter exceptions

Open-ended charter exceptions are invalid.

A `CharterException` must preserve the underlying rule and must carry expiry. An active or approved exception must carry approval, authority trace, start condition, expiry, and disclosure posture.

### 23.7 Sustainability claim readiness

A sustainability claim is not claim-ready merely because it is plausible, model-generated, dashboard-visible, or supported by weak evidence.

A claim-ready state must prove:

- evidence sufficiency;
- evidence requirements used;
- metric profile and method basis;
- current-state reliance and materialisation basis where current state is used;
- approval gate or explicit approval-not-required reason;
- output disposition;
- output qualification where relevant.

Attestation-ready and filed states require authority decision trace and approval decision trace.

### 23.8 Output qualification contradictions

If an output is advisory-only, it must block stronger use classes including high-consequence decision, claim-bearing output, attestation candidate, execution-bound preparation, and partner disclosure.

If evidence is insufficient or missing, claim-bearing and attestation use must be blocked.

If material state is stale-blocking, invalidated, or unknown for the use, high-consequence decision and claim-bearing use must be blocked.

### 23.9 Data-sharing and external scheme posture

Partner-facing or public sustainability disclosure requires a sharing grant or explicit lawful/public-authority basis. Aggregated disclosure requires aggregation floor. Redacted disclosure requires redaction policy.

External sustainability standards, buyer programmes, certification schemes, carbon methods, and regional instruments must declare their OFARM role:

```text
SEMANTIC_ANCHOR
SEMANTIC_PROFILE
EXCHANGE_MAPPING
EVIDENCE_SOURCE
ATTESTATION_WRAPPER
AUTHORITY_SOURCE_BY_EXPLICIT_GRANT
REFERENCE_ONLY
```

They may not override the farm charter by default.

### 23.10 Pack-surface execution requirement

CP11 sustainability pack surfaces must be represented in pack-merge/currentness machinery before any pack-related CP11 conformance claim is made.

The required CP11 pack surfaces are:

```text
SUSTAINABILITY_CONSTRAINT
SUSTAINABILITY_OBJECTIVE
SUSTAINABILITY_OBJECTIVE_PRIORITY
SUSTAINABILITY_TRADEOFF_POLICY
SUSTAINABILITY_EVIDENCE_POLICY
SUSTAINABILITY_METRIC_PROFILE
SUSTAINABILITY_CLAIM_RULE
CHARTER_EXCEPTION_POLICY
CHARTER_BREACH_POLICY
```

Conflicting sustainability pack rules must hard-fail or require governance according to surface-family merge law.

### 23.11 Constraint versus report-only indicator

`REPORT_ONLY_LIMIT` is not a valid `SustainabilityConstraint.constraintStrength`.

Report-only indicators belong to `SustainabilityObjective`, `SustainabilityMetricProfile`, or `ObjectivePriority`, not to hard constraints.

### 23.12 Risk and regret budget non-authorisation

`RiskBudget` and `RegretBudget` are CP11 hooks. They do not authorise experimentation, execution, robot missions, machine commands, or learning promotion. Full experimentation and farm-memory law remains CP13.

### 23.13 Final CP11 acceptance dependencies

Final CP11 acceptance requires:

- remediated draft schemas staged as non-default until acceptance;
- SustainabilityConstraint removal of `REPORT_ONLY_LIMIT`;
- pack-surface patch for CP11 sustainability surfaces;
- executable P0 conformance fixtures;
- currentness addendum that prevents schema overclaiming;
- explicit non-claims for production readiness, certification readiness, autonomous compliance, robot execution, CP13 learning, CP14 exchange, and CP15 generated-software delivery.


## 24. Phase 7.1 boundary repair clauses

Phase 7.1 tightens CP11 package boundaries without broadening CP11 scope.

The repair requires all CP11 schemas to remain draft/non-default until currentness promotion, separates sustainability metric evidence source from quality/freshness status, adds executable draft pack-surface patch schemas, adds positive and schema-aware conformance fixtures, enforces output-use disjointness, blocks empty disclosure grant arrays, forces `traceRequired: true` for high-governance approval gates, requires rule-level trade-off `ALLOW` to prove hard-constraint safety, types policy-evaluation result objects, renames hook headings that could invite CP12/CP13/CP14 scope creep, and repairs RFC subsection numbering.


## 24. CP11 Phase 7.2 final-gate hardening note

Phase 7.2 applies narrow final-gate hardening only. It does not reopen CP11 scope, split CP11, or create CP12, CP13, CP14, or CP15 law.

The hardening repairs four executable edge cases:

1. `SustainabilityClaimBasis` now blocks `CLAIM_READY`, `ATTESTATION_READY`, and `FILED` where `currentStateReliance = UNKNOWN_BLOCKING`; attestation/filed claims must either not rely on current state with a declared reason, or rely on current state with a materialisation basis and output/freshness qualification.
2. `SustainabilityOutputQualification` now prevents disclosure-use contradictions between `allowedUseClasses` and `dataSharingPosture`, including partner/public disclosure without an applicable grant or public-authority basis.
3. `SustainabilityPolicyEvaluationTrace` now prevents `ALLOW` or `ALLOW_WITH_QUALIFICATION` where a blocking failed/review/insufficient result is present, and requires typed results or a `noApplicableRulesBasis` for complete `ALLOW` evaluations.
4. `CharterException` temporal coherence is enforced by conformance: expiry must be after `validFrom`, review deadlines must not exceed expiry, and active exceptions must not be expired at evaluation time.

All CP11 machine contracts remain draft/non-default. Phase 7.2 does not promote schemas to current/default and does not support production-readiness, certification-readiness, robot-readiness, autonomous-compliance, farm-to-farm intelligence, or generated-software delivery claims.


## 25. CP11 Phase 7.3 final boundary and claim-disposition hardening note

Phase 7.3 applies a narrow final hardening pass only. It does not reopen CP11 scope, split CP11, promote schemas to current/default, or create CP12, CP13, CP14, or CP15 law.

The Phase 7.3 package hardens the following boundary conditions:

1. `SustainabilityClaimBasis.claimReadiness` is bound to the exact required `outputDisposition`:
   - `CLAIM_READY` requires `CLAIM_BEARING`;
   - `ATTESTATION_READY` requires `ATTESTATION_CANDIDATE`;
   - `FILED` requires `FILED_SUBMISSION`.
2. A failed hard `SustainabilityConstraint` cannot produce `ALLOW` or `ALLOW_WITH_QUALIFICATION`, even where an implementation attempts to mark the failed constraint result as non-blocking.
3. Complete `ALLOW` or `ALLOW_WITH_QUALIFICATION` evaluations with no typed evaluation results require `noApplicableRulesBasis`.
4. Advisory-only outputs block public disclosure by default under CP11.

All Phase 7.3 schemas remain draft/non-default and use `cp11-v0.1-draft-phase7-3-final-boundary-and-claim-disposition-hardening`.
