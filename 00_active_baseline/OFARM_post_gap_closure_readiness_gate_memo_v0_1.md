# OFARM post-gap-closure readiness gate memo v0.1

Date: 2026-05-17  
Status: refreshed readiness recommendation after ONT-SEMINT v0.3 semantic-integrity baseline harmonisation; AAI-CP10 final readiness and claim-limit addendum applied

---

## Gate outcome

**RECOMMENDATION: IMPLEMENTATION-DIRECTED WITH BOUNDED DEBT**

That recommendation still holds.
The v0.5 pass strengthens it by converting the biggest remaining pack/runtime drift seam into package-local executable evidence.

---

## What changed in the v0.5 closure pass

The package now includes, in delivered and rerunnable form:
- `PackActivationSet` machine contract and validated example
- `ActiveArtifactSet` machine contract and validated examples
- pack-activation request/result boundary envelopes plus reusable runtime-problem schema
- executable runner coverage for:
  - manifest-to-active-artifact-state consistency
  - capability-manifest registry/grounding checks
  - pack-activation allow / deny / governance-required / scope-separation outcomes

---

## Why the gate still passes

### 1. The active RC2.1 baseline remains sufficient
This pass did not reopen architecture and did not require a new charter round.
It realized already-decided pack/runtime law in a more executable form.

### 2. The biggest remaining governance/runtime ambiguity is now smaller
Earlier, `PackActivationSet` existed in law but not as a shipped machine contract.
Likewise, `activeArtifactSetRef` existed in manifests without a package-local object contract behind it.
That mismatch is now materially reduced.

### 3. Capability self-description is harder to fake accidentally
The package can now test whether a manifest’s declared active packs/profiles actually match the active artifact state it points to.
That is a direct reduction of the “capability honesty” risk.

### 4. Runtime boundary closure has started without overclaiming completion
The package now ships a minimal boundary envelope pattern for the pack-activation seam.
That is not the full runtime-boundary layer, but it is no longer purely prose.

---

## What this gate does **not** claim

This gate still does **not** claim full minimum-conformance closure.
The conformance matrix remains the truth source for what is covered, partial, or not started.

---

## Remaining bounded debt

The main remaining bounded debt is now concentrated in:
- runtime boundary envelopes for authority, materialization, query entry, and publication/export beyond the new pack-activation seam
- broader pack-conformance depth across more surface families and precedence cases
- lot pressure cases, alias stability, and output-taxonomy separation
- sharing/revocation and AI-assisted authority depth beyond the current starter subset
- richer active-artifact consistency beyond the current manifest-grounding subset

These are real gaps.
They do not currently justify reopening the architecture.

---

## Conditions of acceptance

### Condition 1
Treat **RC2.1** as the active implementation baseline, not earlier RC lines.

### Condition 2
Treat the accepted RFC set, colocated closure artifact, and machine contracts as part of the active implementation package.

### Condition 3
Use the coverage matrix as the truth source for what is currently covered, partial, or not started.

### Condition 4
Do not present design fixtures as if they were already executable.

### Condition 5
Continue with controlled closure work on contracts and conformance rather than reopening broad design.

---

## Practical next move

The next correct move remains:

**implementation-scale work plus deeper conformance expansion**

with priority on:
- authority/materialization/publication-export boundary envelopes
- deeper pack merge legality coverage and active-artifact consistency depth
- lot, alias, sharing/revocation, and output-taxonomy executable fixtures

not:
- another broad rewrite
- another charter round
- premature external-standard readiness claims


---

## AGR-P7 agronomic baseline-harmonisation addendum — 2026-05-13

**Gate outcome remains: IMPLEMENTATION-DIRECTED WITH BOUNDED DEBT.**

The AGR-P2 through AGR-P6 agronomic amendment line has now been reflected in baseline law at carrier-shell level. The package no longer treats agronomic observation context, measurement evidence, intervention/as-applied payloads, partial extents, code-binding profiles, or query/output reconstruction as merely supporting research or isolated examples.

What is materially stronger:
- high-consequence agronomic observations now require structured context when policy needs it;
- measurement evidence can carry method, calibration, uncertainty, limits, quantity, unit, and provenance context;
- recommendation, prescription, plan, claim, as-applied evidence, accepted execution, correction, and dispute remain disjoint;
- partial areas and disputed geometries are represented without turning every slice into a durable identity;
- product/input/organism/crop-stage/method/threshold identities must be scheme-bound or explicitly unresolved;
- agronomic PassportView and DocumentAssembly reconstruction has policy and trace support.

What this still does not claim:
- external-standard readiness;
- licensed wire-level conformance to every machinery or registry standard;
- full production runtime execution;
- complete crop, jurisdiction, certification, nutrient, storage, or livestock coverage.

The remaining bounded debt has shifted from missing agronomic carrier semantics to pilot-depth conformance, broader crop/profile packs, jurisdiction-specific code-binding bundles, live registry checks, wire-level exchange mapping, and external verification.

---

## ONT-SEMINT baseline-harmonisation addendum — 2026-05-14

**Gate outcome remains: IMPLEMENTATION-DIRECTED WITH BOUNDED DEBT.**

ONT-SEMINT Phases 0 through 5 are now reflected in active baseline law at semantic-integrity and runtime-gate level. The package no longer treats reference resolution, agronomic carrier-field canonicalization, temporal field conformance, high-consequence alias pinning, external registry currentness, or PassportView refusal/review behavior as only supporting prose or isolated fixtures.

What is materially stronger:

- schema validation is explicitly separated from semantic conformance and high-consequence output eligibility;
- package-local references must resolve before they can support high-consequence use;
- externally anchored references require profile-declared snapshot and verification support before they can drive high-consequence output;
- agronomic carriers have canonical reference fields and compatibility-field conflict behavior;
- delayed/offline records must preserve distinct time meanings;
- high-consequence queries require version-pinned aliases and alias-resolution trace;
- PassportView must refuse or review unresolved, stale, ambiguous, disputed, externally unverified, or conflicting high-consequence material;
- DocumentAssembly may annex unresolved or failed verification evidence without promoting it;
- the Belgium/Phytoweb crop-protection currentness profile is accepted as a narrow package-local profile/conformance closure.

What this still does not claim:

- live Phytoweb or live external registry integration;
- legal advice;
- production runtime readiness;
- external-standard readiness;
- full wire-level interoperability;
- livestock coverage;
- broad jurisdictional profile coverage beyond the narrow Belgium package-local profile.

Remaining bounded debt is now concentrated in production implementation evidence, live registry integration evidence, broader jurisdiction/crop/profile coverage, wire-level exchange mapping, source-owner evidence, and field-pilot validation. These are real implementation and conformance gaps. They do not justify reopening the architecture.

The next correct move is implementation-scale closure against the harmonised baseline: runtime resolver integration, live-source adapters where appropriate, source-owner evidence checks, field-pilot scenarios, and jurisdiction-profile expansion under the same fail-closed posture.

---

## ONT-SEMINT v0.3 readiness-gate addendum — 2026-05-14

**Gate outcome remains: IMPLEMENTATION-DIRECTED WITH BOUNDED DEBT.**

ONT-SEMINT v0.3 harmonises the semantic-integrity closures from Phases 0–5 into active baseline posture. The active baseline now explicitly recognises:

- semantic conformance as distinct from schema validation;
- package-local reference-resolution gates;
- canonical agronomic carrier-reference precedence;
- temporal field conformance for high-consequence audit paths;
- version-pinned or traceably resolved aliases for high-consequence queries and outputs;
- external registry currentness and verification traces where active profiles require them;
- PassportView refusal/review behavior and DocumentAssembly annex behavior for unresolved, stale, ambiguous, disputed, or unavailable material.

What is materially stronger:

- JSON-shape validity can no longer be mistaken for high-consequence semantic conformance;
- package-local reference drift is a governed conformance failure instead of silent documentation debt;
- agronomic carrier compatibility fields have explicit precedence and conflict handling;
- delayed-sync, correction, dispute, materialization, and output times are protected from timestamp collapse;
- the Belgium/Phytoweb crop-protection authorisation profile gives one narrow package-local proof of currentness-oriented external binding;
- operational break tests now cover delayed contractor sync after revocation, stale alias/conflicting binding, recommendation-to-execution promotion, observation-to-treatment audit reconstruction, and schema/glossary/example drift.

What this still does not claim:

- production runtime readiness;
- live external registry integration;
- legal advice;
- broad external-standard readiness;
- full jurisdiction/crop/product profile coverage;
- Slovenia profile closure;
- livestock semantic closure.

The remaining bounded debt is now concentrated in production runtime implementation, live registry integration evidence, broader jurisdiction/profile packs, wire-level external exchange mappings, field-pilot evidence, and standard-readiness packaging.

---

## Agentic AI baseline-safety readiness addendum — 2026-05-14

**Gate outcome remains: IMPLEMENTATION-DIRECTED WITH BOUNDED DEBT.**

Phase AAI-P1 adds a narrow active-baseline safety clarification for agentic AI and world-model readiness. It prevents AI outputs, agent memory, public surfaces, tool-call success, scenario state, world-model state, projections, caches, and compiled-output previews from becoming hidden truth stores or hidden governance decisions.

What is materially stronger:

- software-agent action must remain explicitly authorized and sponsor/accountability-aware;
- generated-by-agent status is provenance and authority context, not an artifact family;
- agent and app operations must pass through governed public/runtime surfaces;
- tool-call success is not OFARM governance success;
- agent handoff may transfer task context but not authority;
- world-model state is Advisory-only unless bridged and accepted through normal OFARM governance;
- AI-facing summaries, briefs, and generated outputs must preserve result qualifications.

What this still does not claim:

- implemented multi-agent runtime readiness;
- implemented world-model runtime readiness;
- production runtime readiness;
- two-agent compatibility;
- autonomous compliance decisioning;
- live external tool or registry integration;
- external-standard readiness;
- legal/regulatory certification.

Remaining bounded debt is concentrated in controlled promotion of agent actorship, agent run envelope, run trace, handoff, capability/tool manifests, world-model advisory state contracts, EvidenceNeed/ObservationRequest contracts, and executable multi-agent/world-model hostile tests. Those are the correct next phases; they do not justify reopening the OFARM architecture.

## Agentic AI CP1 release-qualification readiness addendum — 2026-05-16

**Gate outcome remains: IMPLEMENTATION-DIRECTED WITH BOUNDED DEBT.**

AAI-CP1 strengthens the active baseline by making hidden result limitations a release-gate failure for AI-facing, public-operation, state-affecting, and high-consequence surfaces. A release surface must be able to produce machine-readable qualification for the governed basis and material limitations of a result, and those qualifications must be faithfully represented to users or downstream systems.

What is materially stronger:

- hidden stale, uncomputed, permission-limited, advisory-only, disputed, or evidence-insufficient results are now release-gate failures for state-affecting or high-consequence use;
- free-text explanation alone is not enough when a user, downstream system, or agent could treat the result as operational or compliance-ready;
- review/refusal behavior is required when material qualification cannot be produced or retrieved;
- candidate `ResultQualificationEnvelope` and trace/public-surface contracts are reserved for later controlled promotion but are not promoted by this addendum.

What this still does not claim:

- active `ResultQualificationEnvelope` machine-contract law;
- active public-operation, preflight, or trace-retrieval RFC closure;
- implemented multi-agent runtime readiness;
- implemented world-model runtime readiness;
- two-agent compatibility;
- autonomous compliance decisioning;
- production runtime readiness;
- external-standard readiness.

Remaining bounded debt now concentrates first in CP2: public surfaces, preflight/dry-run, trace retrieval, result-qualification contracts, examples, negative fixtures, and runtime conformance evidence.


## AAI-CP3 readiness-gate update — 2026-05-16

AAI-CP3 promotes a bounded active actorship layer for sponsor-bound software-agent authority. The readiness implication is limited: OFARM can now require software-agent profiles, agent instances, sponsor references, model/tool profile basis, authority envelopes, revocation state, actorship bindings, and agent authorization decision traces as active machine-contract shapes.

This is not runtime AI-agent readiness. A runtime readiness claim remains blocked until a running implementation demonstrates policy re-checks, revocation handling, blocked-action traces, trace retrieval, result qualification, and the later agent-run/handoff gates.

Still blocked after CP3:

- two-agent compatibility;
- agent run/handoff readiness;
- tool-manifest readiness;
- world-model readiness;
- EvidenceNeed or ObservationRequest readiness;
- autonomous compliance decisioning;
- production readiness;
- external-standard readiness.


## AAI-CP4 readiness-gate update — 2026-05-16

AAI-CP4 promotes a bounded active contract layer for software-agent run envelopes, run traces, tool-invocation traces, output dispositions, blocked-action traces, handoff envelopes, input bundles, stop conditions, approval checkpoints, and freshness requirements.

The readiness implication is limited: OFARM can now require these shapes as active contract obligations for a governed agent run. This is still not runtime AI-agent readiness and not two-agent compatibility. A runtime readiness claim remains blocked until an implementation executes hostile tests proving policy re-checks, revocation handling, blocked-action traces, trace retrieval, result qualification, handoff reauthorization, and no hidden authority transfer.

Still blocked after CP4:

- two-agent compatibility;
- tool-manifest readiness;
- world-model readiness;
- EvidenceNeed or ObservationRequest readiness;
- autonomous compliance decisioning;
- production readiness;
- external-standard readiness.

## AAI-CP5 readiness-gate update — 2026-05-16

AAI-CP5 promotes a bounded active contract layer for capability/tool manifest honesty. OFARM can now require manifest and tool self-description to declare side effects, target surfaces, schemas and hashes, data classes, auth/scopes, approval requirements, semantic preconditions, external-call posture, trace-retention expectations, redaction/permission-limited result policy, data-learning posture, untrusted declared hints, and readiness claim limits.

The readiness implication is limited: CP5 makes manifest claims inspectable and policy-checkable. It is still not runtime AI-agent readiness, not two-agent compatibility, not production readiness, and not autonomous compliance decisioning. Static schema validation, examples, manifests, vendor descriptions, or tool annotations are not runtime evidence.

Still blocked after CP5:

- runtime AI-agent readiness;
- two-agent compatibility;
- world-model runtime readiness;
- EvidenceNeed or ObservationRequest promotion;
- output assembly preview promotion;
- autonomous compliance decisioning;
- production readiness;
- live-registry integration;
- legal advice;
- external-standard readiness.

## AAI-CP7 advisory world-model readiness-gate addendum — 2026-05-16

CP7 closes the narrow contract-shape gap for Advisory Twin world-model material. It does not close world-model runtime readiness.

Allowed claim: OFARM has active machine-contracts and an accepted RFC for bounded advisory world-model runs, states, scenarios, uncertainty, validity, invalidation, output disposition, governance blockers, and reconciliation.

Blocked claims remain: world-model ready, production runtime ready, autonomous compliance support, live model-monitoring sufficiency, legal advice, agronomic advice, external-standard readiness, and current-state materialization from world-model state.

Next evidence required: runtime execution evidence, calibration/validation evidence, invalidation and reconciliation telemetry, farmer-facing comprehension evidence, and post-deployment monitoring policy.

## AAI-CP8 request-layer readiness-gate addendum — 2026-05-16

CP8 closes the narrow contract-shape gap for EvidenceNeed, ObservationRequest, and supporting request-burden/noise/display artifacts. It does not close farmer UX readiness or production runtime readiness.

Allowed claim: OFARM has active machine contracts and an accepted RFC for bounded request-layer artifacts that preserve non-evidence, non-obligation, non-blocker-by-itself semantics and require burden, relevance, deduplication, lifecycle, satisfaction, display, and blocking-basis records.

Blocked claims remain: requests as evidence, requests as obligations, requests as blockers by themselves, farmer UX ready, production runtime ready, autonomous compliance support, minimum-capture-profile sufficiency, formula/default calculation sufficiency, legal advice, agronomic advice, and external-standard readiness.

Next evidence required: runtime execution evidence, farmer-facing comprehension evidence, request-fatigue/burden pilot evidence, live revocation and offline replay evidence, dispute reconstruction evidence, and post-deployment monitoring policy.

---

## AAI-CP10 final readiness and claim-limit addendum — 2026-05-17

AAI-CP10 updates readiness posture after the controlled-promotion sequence CP1 through CP9. This is a readiness and claim-limit update, not a new semantic-law expansion.

### Bounded continuation posture

OFARM now has a bounded active agentic AI governance contract layer for:

- AI-facing release qualification;
- public operations, preflight/dry-run, trace retrieval, public read-model envelopes, source-fidelity envelopes, runtime reason codes, and result qualification;
- sponsor-bound software-agent actorship and authority decision traces;
- agent run envelopes, run traces, tool-invocation traces, blocked-action traces, output disposition, stop conditions, approval checkpoints, freshness requirements, and handoff envelopes;
- capability/tool manifest honesty and readiness-claim limits;
- Advisory Twin-only world-model runs/states and scenario result contracts;
- EvidenceNeed and ObservationRequest request-layer contracts with burden, noise, display, blocking-basis, and satisfaction controls;
- synthetic farmer-value UX scenario conformance fixtures.

This supports implementation continuation under controlled claim limits.

### Evidence currently available

The package includes CP1 through CP9 conformance reports. The strongest runtime evidence remains the CP6 selected synthetic hostile runtime stub. The strongest farmer-facing evidence remains CP9 synthetic scenario conformance.

These are useful conformance signals, but they are not production runtime evidence, live farmer-pilot evidence, live registry integration, legal/regulatory validation, or external-standard conformance.

### Claims allowed after CP10

The package may claim:

- implementation-directed agentic AI/world-model governance support with bounded debt;
- bounded active contract support for the CP2 through CP8 promoted layers;
- selected CP6 synthetic hostile runtime-stub conformance;
- CP9 synthetic farmer-value UX scenario conformance.

### Claims still blocked after CP10

The package must not claim:

- production readiness;
- full runtime AI-agent readiness;
- general two-agent compatibility;
- full Phase 9 conformance;
- autonomous compliance decisioning;
- world-model readiness;
- world-model state as current state or compliance basis by itself;
- requests as evidence, obligations, or blockers by themselves;
- farmer UX readiness or live farmer-pilot validation;
- legal advice;
- live registry integration;
- external-standard readiness.

### Evidence required before stronger claims

Stronger readiness claims require production or pilot evidence, including runtime policy logs, trace retrieval under load, revocation and sharing telemetry, full hostile-suite execution, post-deployment monitoring, farmer comprehension/burden validation, and profile-specific regulatory or external-standard review where applicable.


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

# OFARM post-gap-closure readiness memo — CP12 addendum candidate

Date: 2026-05-28  
Status: final CP12 readiness addendum merged active baseline addendum

## Readiness posture

CP12 improves OFARM by adding cyber-physical mission-envelope law for mission preparation, preflight, dispatch authority, command integrity, safety envelope, telemetry, receipt, verification, and physical-safety incident handling.

CP12 does **not** make OFARM production robot-ready or machine-control-ready.

## Claims allowed after CP12 acceptance

OFARM may claim bounded model-law and draft machine-contract support for:

- cyber-physical mission envelope semantics;
- mission stage separation;
- dispatch-authorisation boundary;
- command-envelope and command-integrity posture;
- geofence/no-go/geometry-validation posture;
- emergency-stop, human-override, local-fallback, lost-link, and remote-takeover posture;
- mission telemetry/receipt/verification truth-boundary posture;
- physical-safety incident and near-miss record posture;
- executable CP12 conformance fixtures.

## Claims still blocked

OFARM must not claim:

- production robot/machine readiness;
- autonomous field-operation readiness;
- legal or safety certification;
- vendor protocol conformance;
- fleet optimisation law;
- CP13, CP14, or CP15 readiness;
- livestock-specific mission law;
- current/default CP12 machine-contract status.

## Evidence required for stronger claims

Stronger claims require:

- current/default promotion of CP12 machine contracts;
- runtime implementation evidence;
- physical-actor integration evidence;
- safety test evidence;
- emergency-stop and human-override testing evidence;
- vendor adapter conformance evidence;
- field-pilot evidence;
- external safety/legal review where applicable.


## Explicit deferrals

CP12 does not create:

- CP13 learning, experimentation, farm-memory, or learning-promotion law;
- CP14 farm-to-farm intelligence, regional mission coordination, or federated-learning law;
- CP15 generated-software delivery, robot-adapter deployment, rollback, or SBOM law;
- livestock-specific mission law;
- vendor protocol conformance;
- legal or safety certification.

# CP13 readiness addendum — merged active baseline addendum

CP13 improves OFARM's model-law coverage for governed learning, experimentation, causal evidence, farm memory, seasonal learning, and learning-output qualification.

CP13 does not claim production autonomous self-improvement readiness, production agronomic advice certification, cross-farm learning readiness, federated learning readiness, model/software deployment readiness, CP14 readiness, or CP15 readiness.

CP13 machine contracts remain draft/non-default until separate currentness promotion.

## CP13 Learning, Experimentation, and Farm Memory readiness and claim-limit addendum — 2026-05-29

### Readiness posture

CP13 improves the active baseline by adding a governed learning, experimentation, causal-evidence, farm-memory, seasonal-learning, and learning-output qualification layer.

CP13 is a model/runtime governance closure. It is not production autonomous self-improvement, production agronomic advice certification, farm-to-farm intelligence readiness, model deployment readiness, or generated-software delivery readiness.

The correct post-CP13 posture remains:

`implementation-directed with bounded debt.`

### Evidence currently available

CP13 currently provides:

- an accepted CP13 RFC;
- baseline patch text for Constitution, Platform Runtime, Alignment Register, readiness, and hostile-review addenda;
- draft/non-default CP13 machine-contract families;
- CP13 conformance fixture families and current CP13 runner;
- explicit deferrals to CP14 and CP15.

This is design and governance evidence. It is not production runtime evidence, live farm-trial evidence, external scientific-method validation, production causal inference validation, farmer-facing memory UX validation, model deployment evidence, or farm-to-farm learning evidence.

### Claims allowed after CP13 baseline acceptance

After CP13 is accepted and reconciled, the package may claim:

- bounded model-law support for governed learning, experimentation, causal evidence, and farm memory;
- explicit separation between learning output and truth;
- explicit separation between agent memory and farm memory;
- explicit separation between experiment protocol and operation/mission authority;
- explicit promotion law for farm memory candidates;
- explicit retrieval qualification for farm memory use;
- explicit CP11 and CP12 preservation where learning depends on charter-sensitive or mission-sensitive inputs;
- explicit deferral of CP14 farm-to-farm intelligence and CP15 generated-software/model-deployment governance.

### Claims still blocked after CP13

The package must not claim:

- production autonomous self-improvement readiness;
- production agronomic advice certification;
- autonomous experiment design or execution readiness;
- autonomous learning-promotion readiness;
- farm-to-farm intelligence readiness;
- federated learning readiness;
- regional alert readiness;
- benchmark exchange readiness;
- derivative model-use readiness;
- model deployment readiness;
- generated-software readiness;
- generated adapter deployment readiness;
- CP14 readiness;
- CP15 readiness;
- legal, insurance, certification, or regulatory advice;
- livestock-specific learning readiness.

### Evidence required for stronger claims

Stronger CP13 claims require:

- accepted CP13 machine contracts;
- passing CP13 conformance fixtures;
- runtime policy logs showing learning-governance gate execution;
- trace retrieval for `LearningEvaluationTrace`;
- test cases proving farm memory cannot be used outside scope without qualification;
- test cases proving agent memory cannot become farm memory;
- test cases proving experiment protocol does not authorise operations or missions;
- test cases proving causal estimates do not create Compliance Twin facts;
- farmer-facing comprehension and burden validation for farm-memory retrieval, invalidation, uncertainty, and learning-output limitations;
- real-world pilot or simulated-trial evidence before any production autonomous self-improvement claim.

### Explicit deferrals

CP13 defers CP14 farm-to-farm intelligence, federated learning, cross-farm benchmark exchange, regional alerts, derivative model use, aggregation-floor, and re-identification-risk governance.

CP13 defers CP15 generated software, model deployment, adapter generation, canary, rollback, SBOM, build provenance, model-card, and deployment-promotion governance.


## CP14 Farm-to-Farm Intelligence Boundary readiness addendum — 2026-05-29

### Bounded continuation posture

CP14 improves OFARM by adding a governed boundary for farm-to-farm intelligence, sharing, received intelligence, regional alerts, benchmark deltas, deidentification/anonymisation claims, re-identification-risk assessment, federated-learning contribution boundaries, model-improvement signals, revocation propagation, contribution quality, poisoning/anomaly review, and intelligence-output qualification.

CP14 is a model/runtime governance closure, not a production farm-to-farm intelligence platform.

CP14 remains **implementation-directed with bounded debt** until the CP14 RFC, baseline patch, machine contracts, conformance fixtures, hostile review, implementation evidence, and steward validation are complete.

### Claims allowed after CP14 acceptance and reconciliation

After CP14 is accepted and reconciled, OFARM may claim:

- bounded model-law support for farm-to-farm intelligence boundaries;
- explicit Advisory-default posture for received cross-farm intelligence;
- explicit separation between sharing and authority;
- explicit boundaries for regional alerts, benchmark deltas, aggregation/deidentification/anonymisation claims, re-identification risk, derivative use, training use, federated contributions, and model-improvement signals;
- controlled hooks for CP15 model/software deployment governance without creating CP15 law;
- conformance-oriented posture for cross-farm intelligence output qualification and sharing/use restrictions.

### Claims still blocked after CP14

OFARM must not claim:

- production farm-to-farm intelligence platform readiness;
- production federated-learning platform readiness;
- public benchmark product readiness;
- OFARM Social readiness;
- OFARM Exchange readiness;
- legal/privacy/certification/insurance/advisory readiness;
- anonymisation guarantee;
- irreversible deidentification guarantee;
- regional-alert accuracy guarantee;
- benchmark fairness or public ranking readiness;
- model deployment readiness;
- generated-software deployment readiness;
- CP15 readiness;
- cross-farm intelligence as local farm truth;
- received intelligence as current state;
- benchmark delta as compliance fact;
- federated-learning contribution as deployment authority;
- current/default CP14 machine-contract promotion.

### Evidence required before stronger claims

Stronger CP14 claims require:

- accepted CP14 machine contracts;
- passing CP14 conformance fixtures;
- runtime evidence for share-grant enforcement;
- recipient-use, derivative-use, training-use, and revocation-propagation evidence;
- output qualification evidence;
- re-identification-risk and aggregation-floor validation;
- poisoning/anomaly-review evidence;
- CP13-to-CP14 learning-artifact share package tests;
- regional-alert correction/withdrawal tests;
- benchmark-delta cohort/aggregation tests;
- farmer-facing comprehension and burden validation;
- legal/privacy review where real personal/commercial data is involved;
- external data-space and sister-platform boundary review.


## CP15 Agentic Software Delivery and Model Deployment Governance readiness and claim-limit addendum — 2026-05-30

### Readiness posture

CP15 improves OFARM by adding bounded model/runtime governance for agentic software delivery and model deployment. It is a governance closure, not a production software-delivery platform, model-deployment platform, MLOps platform, cybersecurity certification, or CI/CD implementation.

The package remains **implementation-directed with bounded debt**.

### Evidence currently available

CP15 currently provides or proposes:

- a CP15 RFC;
- controlled baseline patch text;
- alignment register updates;
- authority/action/event/pack addendum requirements;
- draft/non-default machine-contract candidates to be developed later;
- conformance fixture requirements to be developed later.

This is design and governance evidence. It is not production deployment evidence, cybersecurity-certification evidence, live runtime deployment evidence, model-performance validation, legal/security advice, or pilot/farmer validation.

### Claims allowed after CP15 baseline acceptance

After CP15 is accepted and reconciled, the package may claim:

- bounded model-law support for agentic software delivery and model deployment governance;
- explicit separation of generated artifacts, build evidence, security evidence, conformance evidence, deployment candidates, deployment authorization, release bundles, runtime-surface bindings, canary/rollback, deployment telemetry, and promotion decisions;
- explicit baseline hooks preventing generated artifacts, test success, scan success, conformance success, canary success, telemetry, or agent tool success from becoming deployment authority or current/default promotion by themselves;
- explicit preservation of CP11, CP12, CP13, and CP14 gates in delivery-sensitive paths.

### Claims still blocked after CP15

The package must not claim:

- production software-delivery readiness;
- production model-deployment readiness;
- autonomous release readiness;
- cybersecurity certification;
- legal/security/compliance/privacy/certification advice;
- full CI/CD product implementation;
- generic MLOps readiness;
- cloud/vendor deployment architecture readiness;
- automatic current/default schema promotion;
- CP11/CP12/CP13/CP14/CP15 draft schema promotion;
- mission authority through generated adapters;
- farm-to-farm intelligence deployment authority;
- OFARM Social or OFARM Exchange constitution.

### Evidence required before stronger claims

Stronger CP15 claims require:

- accepted CP15 draft/non-default machine contracts;
- executable CP15 conformance runners and fixtures;
- cross-record validation proving deployment authority cannot be created by build/test/scan/conformance/canary/tool success;
- runtime logs showing CP15 gates in delivery-sensitive paths;
- security review of CP15 evidence and waiver posture;
- runtime-surface binding tests;
- rollback/canary/incident fixtures;
- CP11/CP12/CP13/CP14 gate integration tests;
- steward validation of package currentness and non-claims.


# OFARM readiness memo — CP15 addendum

Status: accepted/merged CP15 amendment addendum  
Date: 2026-05-30

CP15 adds model-law and runtime-boundary support for agentic software delivery and model deployment governance.

## CP15 allowed claims after acceptance

OFARM may claim bounded model-law support for:

- generated software and generated adapter delivery-governance boundaries;
- model deployment candidate governance;
- supply-chain evidence, SBOM, dependency, static/security scan, waiver, conformance, canary, rollback, telemetry, runtime receipt, incident, and output-qualification boundaries;
- explicit non-bypass of CP11 sustainability gates, CP12 mission/adapter gates, CP13 learning/model-output gates, and CP14 training/federated/model-improvement gates;
- draft/non-default CP15 machine-contract candidates and executable conformance fixtures.

## CP15 blocked claims

OFARM must not claim:

- production software-delivery readiness;
- production model-deployment readiness;
- generated-adapter production readiness;
- cybersecurity certification;
- autonomous release readiness;
- full CI/CD product readiness;
- generic MLOps platform readiness;
- cloud/vendor deployment architecture readiness;
- legal/security/compliance advice;
- current/default CP15 machine-contract promotion;
- automatic current/default schema or contract promotion.

## Evidence required before stronger claims

Stronger claims require accepted current/default promotion, implementation evidence, runtime evidence, security review, conformance execution in target environments, operational rollback drills, model-deployment governance evidence, and external review where required.


# OFARM Readiness Gate Memo — CP14 Addendum

Status: final CP14 readiness addendum candidate  
Amendment: CP14 — Farm-to-Farm Intelligence Boundary

CP14 adds a governed farm-to-farm intelligence boundary. It is a model/runtime governance closure, not production farm-to-farm intelligence readiness.

## Claims allowed after CP14 acceptance

After acceptance and merge, OFARM may claim bounded model-law support for:

- cross-farm Advisory-default intelligence boundary;
- intelligence-specific sharing grants and recipient-use constraints;
- derivative-use, training-use, and revocation-propagation controls;
- aggregation/deidentification/anonymisation/re-identification-risk separation;
- regional alerts, risk signals, benchmark deltas, and applicability assessment as governed Advisory intelligence;
- federated-learning contribution boundaries without model-deployment authority;
- CP11/CP12/CP13 boundary preservation for cross-farm disclosure and derivative use.

## Claims still blocked

OFARM must not claim:

- production farm-to-farm intelligence readiness;
- production federated-learning readiness;
- anonymisation guarantee;
- legal, privacy, certification, insurance, or advisory readiness;
- OFARM Social constitution;
- OFARM Exchange constitution;
- public benchmark product law;
- generic reputation law;
- model/software deployment governance;
- CP15 readiness;
- current/default CP14 machine-contract promotion.

## Evidence required before stronger claims

Stronger claims require steward-accepted merge, passing CP14 conformance, privacy/risk-method review, implementation evidence, farmer-facing disclosure/burden validation, and legal/privacy review where required by jurisdiction or programme.
