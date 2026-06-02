# OFARM final hostile review after gap closure v0.1

Date: 2026-05-17  
Status: refreshed hostile review after ONT-SEMINT v0.3 semantic-integrity baseline harmonisation; AAI-CP10 hostile-review closure update applied  
Scope: evaluate the harmonized RC2.1 baseline together with the accepted RFCs, companion artifacts, machine contracts, cleaned support layers, repaired spike package, new pack/runtime closure artifacts, and AAI-CP1 through AAI-CP10 controlled-promotion evidence and claim limits

Reviewed package:
- OFARM Reference Model and Artifact Constitution (RC2.1)
- OFARM Platform Runtime and Product Architecture (RC2.1)
- OFARM Alignment Register v0.13
- accepted post-charter RFC set
- accepted closure companion artifact introduced by RFC-4
- companion artifacts and policies
- repaired reference spike package and rerun results
- conformance seed set, coverage matrix, and executable-vs-prose policy
- machine-contract validation results
- governance/runtime closure runner results

---

## 1. Bottom line

**OFARM remains implementation-directed with bounded debt.**

The important v0.5 update is that the package now closes one of the most obvious remaining “law exists but executable object does not” gaps.

---

## 2. What is now materially stronger

### 2.1 Pack activation is no longer only a prose-governed concept
The active baseline already required a concrete `PackActivationSet`.
The package now ships a machine contract, example, request/result envelopes, and starter executable fixtures for that seam.

### 2.2 Capability manifests are better grounded in actual runtime state
`activeArtifactSetRef` is no longer hanging over a missing object contract.
The package now ships a minimal active-artifact-state contract and executable checks that compare manifest claims against the referenced state.

### 2.3 The package has begun a real runtime-boundary layer
This pass does not finish runtime boundary closure, but it does establish a reusable pattern:
- typed request envelope
- typed result envelope
- stable machine-readable problem object
- seam-specific executable checks

That is the right kind of closure work.

### 2.4 The conformance story is more honest and more useful
The coverage matrix can now move some lines from “not started/prose only” into actual executable evidence.
That improves trustworthiness for implementers and AI agents.

---

## 3. Why I am still not giving a stronger verdict

The package is stronger.
It is still not close to “spec complete” or “external-standard ready.”

### 3.1 The closure is still narrow
Pack activation and manifest grounding are materially better.
Many other runtime-boundary seams remain prose-thin.

### 3.2 Broader pack-conformance depth is still missing
The package now has activation outcomes across a few starter cases.
It still needs many more surface-family and precedence combinations before anyone should call the pack subsystem deeply tested.

### 3.3 Lot and alias remain the hardest divergence risks
Nothing in this pass changes that underlying judgment.
The highest domain/runtime drift risks are still elsewhere once pack activation is no longer the biggest obvious gap.

### 3.4 Output taxonomy and sharing/revocation are still too prose-heavy
The package still needs executable closure at the PassportView/DocumentAssembly boundary and in access-versus-authority enforcement depth.

---

## 4. What I would now classify as closed versus still open

### Closed enough for continuation
- package-level spike reproducibility
- accepted-RFC status hygiene
- supporting-research packaging cleanup
- explicit executable-vs-design fixture rule
- first trace/materialization machine-contract wave
- `PackActivationSet` starter contract and activation-outcome fixtures
- `activeArtifactSetRef` grounding through a minimal active-artifact-state contract

### Still open but bounded
- runtime boundary envelopes beyond pack activation
- broader pack conformance depth
- lot pressure cases
- alias stability suites
- sharing/revocation and AI-assisted authority depth
- executable output taxonomy checks

---

## 5. Hostile reader verdict

If I read this as a hostile reviewer now, I would say:

1. the baseline architecture is still not the main problem,
2. the package is now less likely to lie accidentally about pack/runtime support,
3. the remaining debt is narrower and easier to prioritize,
4. the next move is still closure work, not redesign.

That is another meaningful improvement in the predevelopment package without reopening architecture.


---

## AGR-P7 agronomic hostile-review addendum — 2026-05-13

**OFARM remains implementation-directed with bounded debt, but the agronomic payload gap is no longer the same class of risk.**

A hostile reader should now see that the package has closed the main office-abstraction failure modes identified by the agronomist review at carrier-shell and fixture level:
- observations are no longer only narrative notes when high-consequence use needs method, stage, threshold, spatial, or measurement context;
- intervention records no longer have to collapse recommendation, prescription, plan, claim, as-applied evidence, acceptance, correction, and dispute;
- partial work and mixed field reality can be represented without whole-field overwrite or geometry sprawl;
- free-text product, organism, crop-stage, method, threshold, and unit labels cannot silently become compliance-grade identity;
- agronomic query/output reconstruction now has policy and trace controls.

The remaining hostile concerns are implementation depth, crop/profile breadth, live registry verification, wire-level interoperability, and field-pilot evidence. Those are still real, but they are not reasons to reopen the architecture.

---

## ONT-SEMINT hostile-review addendum — 2026-05-14

**OFARM remains implementation-directed with bounded debt, but the semantic-integrity drift risk is materially lower.**

A hostile reader should now see that the package has closed the main ontology-steward concerns at active baseline, RFC, machine-contract, and package-local conformance level:

- JSON shape validity can no longer be honestly presented as semantic conformance or high-consequence output eligibility;
- package-local references have a resolver/reporting surface;
- high-consequence external registry identity requires snapshot and verification-trace support when a profile requires currentness;
- agronomic carrier reference fields have canonical precedence and compatibility-conflict behavior;
- temporal semantics are protected against timestamp collapse;
- query aliases are version-pinned for high-consequence output;
- PassportView and DocumentAssembly have different refusal, disclosure, and annex behavior;
- operational break tests now cover delayed contractor sync after revoked authority, stale alias plus conflicting product binding, recommendation-to-execution chains, observation-to-treatment audit reconstruction, and schema/glossary/example drift.

The remaining hostile concerns are no longer primarily constitutional. They are implementation evidence concerns: live registry adapters, production runtime evidence, source-owner payload custody, broad jurisdictional profile coverage, wire-level standard mappings, and real field-pilot validation.

This addendum should not be read as external-standard readiness, production readiness, legal advice, live Phytoweb verification, or livestock coverage. It is a controlled baseline harmonisation of already-tested ONT-SEMINT closure work.

---

## ONT-SEMINT v0.3 hostile-review addendum — 2026-05-14

A hostile reader should now treat the original ontology-steward risks as materially reduced but not eliminated.

Closed or substantially reduced:

- schema-valid but semantically broken package-local references now have a resolution/reporting lane;
- high-consequence query aliases now have a baseline pinning/trace requirement;
- generic versus agronomic carrier-reference ambiguity now has precedence and conflict handling;
- high-consequence temporal collapse is explicitly prohibited;
- PassportView and DocumentAssembly failure/annex behavior is clearer;
- one narrow Belgium/Phytoweb external-currentness profile exists as package-local proof of concept;
- operational break tests now exercise the main farm-reality failure paths identified by the review.

Still open and hostile-reader relevant:

- no production runtime has proved these gates live under real load;
- no live Phytoweb integration is claimed;
- no broad external-standard readiness is claimed;
- no full Slovenia profile, livestock profile, or multi-jurisdiction profile family is closed;
- wire-level ISOXML, EFDI, ADAPT, NGSI-LD, or other external exchange mappings remain profile/runtime work, not baseline-complete proof.

Verdict: OFARM remains directionally right and implementation-directed with bounded debt. The next failure mode is no longer missing semantic-integrity law; it is insufficient production execution, registry integration, and field-pilot evidence.

---

## Agentic AI hostile-review addendum — 2026-05-14

A hostile reader should now treat the first agentic AI/world-model failure mode as partially closed at baseline-safety level: OFARM explicitly refuses hidden AI truth, hidden agent governance, hidden world-model current state, and hidden authority transfer through public surfaces or handoff.

Closed or substantially reduced:

- AI outputs and agent memory cannot honestly be treated as canonical truth by default;
- `AgentOutput` cannot become a generic truth bucket under the active clarification;
- tool-call or public-operation success cannot be presented as governance success;
- world-model and scenario state cannot be treated as Compliance Twin state or current-state materialization;
- handoff context cannot silently transfer authority;
- high-consequence AI-facing answers must preserve result qualifications.

Still open and hostile-reader relevant:

- agent actorship and lifecycle are not yet active machine contracts;
- `AgentRunEnvelope`, `AgentRunTrace`, and `AgentHandoffEnvelope` remain draft/supporting until promoted;
- Capability Manifest agent-support declarations remain draft/supporting;
- world-model advisory runtime contracts remain draft/supporting;
- EvidenceNeed and ObservationRequest remain draft/supporting;
- no implementation has executed multi-agent or world-model break tests;
- no two-agent compatibility proof exists.

Before any implementation is described as multi-agent-ready or world-model-ready, hostile review must verify that agents cannot activate packs, self-certify, promote their own advisory outputs, treat world-model state as current state, transfer authority by handoff, hide stale or permission-limited results, over-disclose through sharing tools, or bypass semantic-law blockers through public operation success.

Verdict: OFARM remains implementation-directed with bounded debt. Phase AAI-P1 makes the baseline safer for agentic continuation, but the next failure mode is missing executable agent/world-model contracts and runtime conformance evidence, not missing broad architecture.

## Agentic AI CP1 hostile-review addendum — 2026-05-16

A hostile reader should now treat hidden or suppressed material qualifications as an active-baseline violation for AI-facing, public-operation, state-affecting, and high-consequence release surfaces.

Closed or substantially reduced:

- a stale, uncomputed, permission-limited, advisory-only, disputed, corrected, or evidence-insufficient result cannot honestly be shipped as if it were complete operational or compliance-ready truth;
- free-text explanation cannot substitute for machine-readable qualification where a user, system, or agent may rely on the result;
- absence of retrievable material qualification must force review, refusal, or a policy-declared successor disposition for state-affecting or high-consequence use.

Still open and hostile-reader relevant:

- `ResultQualificationEnvelope`, trace-retrieval, public-operation, and preflight contracts remain candidate/supporting until CP2 or later promotion;
- no implementation has executed the release-qualification gate against runtime traces;
- no two-agent, world-model, or production-readiness claim is supported by CP1.

CP1 narrows the next failure mode: the architecture now says the release gate exists, but CP2 and CP6 must make the gate contract-shaped, example-backed, and runtime-tested.


## AAI-CP3 hostile-review update — 2026-05-16

AAI-CP3 closes only the narrow actorship ambiguity: a software agent may not rely on model identity, tool identity, API key, session state, prompt instruction, or manifest declaration as authority. The promoted contract layer requires sponsor-bound actorship, action-class posture, authority snapshot, revocation state, and authorization trace.

Residual hostile cases remain open for later phases: a receiving agent inheriting authority through handoff, a successful tool call being shown as governance success, a manifest overclaiming safety, a world-model state being treated as current state, and an EvidenceNeed or ObservationRequest becoming evidence or obligation by itself. These remain blocked from readiness claims after CP3.


## AAI-CP4 hostile-review update — 2026-05-16

AAI-CP4 closes the narrow run/trace/handoff ambiguity: a software-agent run must be bounded, traceable, qualified, and blocked when it exceeds its envelope. A blocked action is now required audit material, tool success is explicitly separated from governance success, and handoff may not silently transfer authority.

Residual hostile cases remain open for later phases: a manifest overclaiming safety or side effects, a public tool catalog being treated as trust, a world-model state being treated as current state, EvidenceNeed or ObservationRequest becoming evidence or obligation by itself, and any runtime readiness claim made without executed hostile-test evidence.

## AAI-CP5 hostile-review update — 2026-05-16

AAI-CP5 closes the narrow manifest-overclaim ambiguity: capability manifests, tool manifests, tool descriptors, declared hints, API catalogs, and readiness claims cannot honestly be treated as authority, approval, safety proof, evidence sufficiency, or governance success. A manifest may describe a callable surface, but it must remain subordinate to authority, evidence, freshness, pack/context, sharing, output, trace, and twin-boundary gates.

Residual hostile cases remain open for later phases: an implementation claiming runtime or two-agent readiness without executed hostile tests, a world-model state being treated as current state, EvidenceNeed or ObservationRequest becoming evidence or obligation by itself, output preview becoming publication, or a live deployment leaking restricted data after revocation. CP6 must execute hostile runtime tests before stronger readiness claims are allowed.

## AAI-CP7 hostile-review update — 2026-05-16

AAI-CP7 partially closes the world-model contract-shape seam but not the world-model readiness seam. A hostile reader should now expect advisory world-model artifacts to identify their Advisory Twin posture, input basis, assumptions, uncertainty, validity window, invalidation rules, output disposition, governance blockers, and reconciliation route.

The main remaining hostile concern is operational overclaim: a UI, agent, or product team could still present a world-model state as current state or compliance fact. CP7 therefore preserves blocked-use fixtures and claim limits. No world-model result may honestly be treated as current state, accepted evidence, Compliance Twin mutation, or official output without separately passing the ordinary OFARM gates.

## AAI-CP8 hostile-review update — 2026-05-16

AAI-CP8 partially closes the request-layer contract-shape seam but not the farmer UX readiness seam. A hostile reader should now expect EvidenceNeed and ObservationRequest artifacts to declare that they are not evidence, not obligations, and not blockers by themselves, and to expose burden, relevance, priority, lifecycle, deduplication, display, satisfaction, and blocking-basis records.

The main remaining hostile concern is operational overclaim: a UI, agent, or product team could still present a request as a compliance duty, evidence requirement, or blocker without a separate external rule or gate. CP8 therefore preserves blocked-use fixtures and claim limits. No request may honestly be treated as accepted evidence, accepted assertion, compliance obligation, or compliance blocker without separately passing ordinary OFARM gates.

---

## AAI-CP10 hostile-review closure update — 2026-05-17

A hostile reader should now treat the agentic AI/world-model controlled-promotion track as **bounded and implementation-directed**, not production-ready.

Closed or substantially reduced:

- public AI-facing surfaces have qualification, preflight, trace, reason-code, and source-fidelity contract support;
- software-agent identity, sponsorship, authority envelope, and revocation posture are explicit;
- governed agent runs and handoffs require envelopes, traces, blocked-action traces, output disposition, freshness requirements, and reauthorization;
- manifests are descriptive and cannot grant authority, prove safety, or make readiness claims without evidence;
- world-model runs/states are Advisory Twin-only and carry uncertainty, validity, invalidation, output disposition, and reconciliation controls;
- EvidenceNeed and ObservationRequest artifacts are request-layer artifacts, not evidence, obligations, or blockers by themselves;
- synthetic farmer-value UX scenarios preserve qualification, stale-data visibility, permission limits, dispute reconstruction, and request-burden controls.

Still open and hostile-reader relevant:

- CP6 is a selected synthetic hostile runtime stub, not a production runtime;
- full Phase 9 conformance has not been executed;
- two-agent compatibility is not a general platform claim;
- world-model readiness is not established because VVUQ, monitoring, calibration, and observed-outcome reconciliation remain implementation/profile work;
- farmer UX readiness is not established because CP9 is synthetic and lacks live farmer validation;
- production readiness, legal advice, live-registry integration, autonomous compliance decisioning, and external-standard readiness remain blocked.

Verdict: OFARM is ready for implementation continuation with bounded agentic AI/world-model governance contracts. The next failure mode is overclaiming readiness beyond executed evidence, not missing core architecture.


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

# OFARM final hostile review after gap closure — CP12 update candidate

Date: 2026-05-28  
Status: final CP12 hostile-review update merged active baseline addendum

## Hostile-reader verdict

CP12 is the correct next bounded amendment after CP11 if, and only if, it remains mission-envelope law and does not become a robotics product specification, vendor protocol, or production autonomy claim.

## Closed or substantially reduced

CP12 closes or reduces the following gaps:

- mission intent/plan/preflight/dispatch/command/telemetry/receipt/verification separation;
- preflight-success-as-dispatch-authority risk;
- command-acknowledgement-as-execution-truth risk;
- telemetry-as-accepted-truth risk;
- CP11-charter-pass-as-dispatch-authority risk;
- agent-tool-success-as-physical-authority risk;
- mission geometry and no-go-zone validation gap;
- command-integrity and replay-protection gap;
- emergency stop, human override, local fallback, lost-link, and remote takeover posture gap;
- mission incident and near-miss recording gap.

## Still open

CP12 does not close:

- production robot/machine safety certification;
- vendor protocol profiles;
- CP13 learning/farm-memory;
- CP14 farm-to-farm intelligence;
- CP15 generated-software delivery governance;
- livestock-specific mission law;
- full fleet optimisation;
- field-pilot validation.

## Hostile-review conclusion

CP12 should be accepted only with the draft/non-default currentness posture preserved and with conformance evidence retained in implementation/conformance material.


## Explicit deferrals

CP12 does not create:

- CP13 learning, experimentation, farm-memory, or learning-promotion law;
- CP14 farm-to-farm intelligence, regional mission coordination, or federated-learning law;
- CP15 generated-software delivery, robot-adapter deployment, rollback, or SBOM law;
- livestock-specific mission law;
- vendor protocol conformance;
- legal or safety certification.


## CP12 exact non-claim wording — 2026-05-28

CP12 does not claim production robot/machine readiness, autonomous field-operation readiness, legal/safety certification, fleet optimisation law, vendor protocol conformance, CP13 readiness, CP14 readiness, or CP15 readiness.

# CP13 hostile-review update — merged active baseline addendum

CP13 closes a conceptual gap around learning and farm memory but remains implementation-directed with bounded debt.

Hostile-review non-claims:
- no production autonomous self-improvement readiness;
- no production agronomic advice certification;
- no cross-farm intelligence or federated-learning readiness;
- no model/software deployment readiness;
- no CP14 or CP15 readiness;
- no automatic promotion from learning outputs to truth, current state, farm memory, compliance fact, mission authority, or model deployment.

## CP13 Learning, Experimentation, and Farm Memory hostile-review addendum — 2026-05-29

A hostile reader should treat CP13 as a bounded learning-governance extension, not as proof that OFARM can autonomously learn, experiment, deploy models, or certify agronomic advice in production.

### Hostile-reader verdict

CP13 is the correct next bounded amendment after CP11 and CP12 if it remains learning, experimentation, causal-evidence, farm-memory, and learning-output governance.

CP13 must not become generic AI memory, cross-farm intelligence, federated learning, model deployment governance, generated-software delivery governance, or autonomous self-improvement readiness.

### Closed or substantially reduced by CP13

CP13 closes or reduces the following gaps:

- learning-output-as-truth risk;
- experiment-result-as-causal-fact risk;
- farm-memory-as-hidden-current-state risk;
- agent-memory-as-farm-memory risk;
- causal-estimate-as-compliance-fact risk;
- model-improvement-as-deployment-authority risk;
- mission/operation-records-as-learning-law risk;
- post-hoc outcome-hacking risk;
- farm-memory retrieval outside scope without qualification;
- learning promotion without governance;
- CP11 risk/regret budget use without learning boundary;
- CP12 mission evidence reuse without truth-boundary protection.

### Still open and hostile-reader relevant

CP13 does not close:

- production autonomous self-improvement readiness;
- production agronomic advice certification;
- farm-to-farm intelligence, federated learning, regional alerts, benchmark exchange, or derivative model-use law;
- generated-software delivery, model deployment, adapter deployment, canary, rollback, SBOM, build provenance, or model-card governance;
- external scientific-method validation or universal causal-inference standardisation;
- farmer-facing farm-memory UX validation;
- livestock-specific learning law;
- live farm-trial validation;
- implementation/runtime evidence for CP13 gates until conformance and steward review exist.

### Hostile-reader risks after CP13

The main remaining risks are:

- treating a causal estimate as stronger than its design/evidence supports;
- treating farm memory as current state;
- retrieving memory outside scope without limitation;
- treating agent memory or vector memory as governed farm memory;
- using CP12 mission telemetry as learning truth without evaluation;
- using CP11 regret budget as authority to experiment;
- allowing agents to approve learning promotion;
- hiding uncertainty, missingness, or post-hoc outcome changes;
- letting learning outputs become claim basis, mission authority, or deployment authority;
- overclaiming autonomous self-improvement before implementation evidence exists.

### Hostile-review conclusion

CP13 should be accepted only if it preserves OFARM truth law, Advisory/Compliance separation, CP11 charter gates, CP12 mission gates, human-governed defaults, explicit promotion law, farm-memory retrieval qualification, and draft/non-default machine-contract currentness until a later promotion decision.

### Explicit deferrals

CP13 does not create:

- CP14 farm-to-farm intelligence, federated learning, regional alert, cross-farm benchmark, derivative model-use, aggregation-floor, or re-identification-risk law;
- CP15 generated-software, model deployment, adapter generation, canary, rollback, SBOM, build provenance, model-card, or deployment-promotion law;
- production autonomous self-improvement readiness;
- production agronomic advice certification;
- livestock-specific learning law.

### CP13 exact non-claim wording — 2026-05-29

CP13 does not claim production autonomous self-improvement readiness, production agronomic advice certification, autonomous experiment execution readiness, autonomous learning-promotion readiness, farm-to-farm intelligence readiness, federated learning readiness, regional alert readiness, benchmark exchange readiness, derivative model-use readiness, model deployment readiness, generated-software readiness, CP14 readiness, CP15 readiness, legal advice, insurance advice, certification advice, or livestock-specific learning readiness.


## CP14 Farm-to-Farm Intelligence Boundary hostile-review update — 2026-05-29

A hostile reader should treat CP14 as a necessary farm-to-farm intelligence boundary extension, not as evidence that OFARM is now a production intelligence network, social platform, exchange platform, federated-learning platform, public benchmarking product, anonymisation engine, or model-deployment platform.

### Closed or substantially reduced

CP14 closes or reduces the following conceptual gaps:

- cross-farm intelligence is explicitly Advisory by default;
- farm-to-farm sharing is separated from authority;
- recipient-use, derivative-use, and training-use boundaries become explicit;
- revocation propagation becomes traceable;
- CP13 local learning and farm memory cannot cross farm boundaries without CP14 governance;
- regional alerts and risk signals cannot silently become farm-level truth;
- benchmark deltas cannot silently become compliance facts or public ranking authority;
- aggregation is not treated as anonymisation by assertion;
- deidentification and anonymisation claims require explicit method and risk basis;
- re-identification risk becomes a governed assessment surface;
- federated-learning contribution does not become model deployment authority;
- model-improvement signal does not become model/software deployment authority;
- contribution quality and poisoning/anomaly review become explicit;
- CP11 sustainability and CP12 mission/incident intelligence preserve source limitations when disclosed cross-farm;
- agents cannot approve sharing, derivative use, training use, anonymisation, public benchmark outputs, or model deployment by default.

### Still open and hostile-reader relevant

CP14 does not close:

- production farm-to-farm intelligence platform readiness;
- production federated-learning platform readiness;
- public benchmark product governance;
- OFARM Social constitution;
- OFARM Exchange constitution;
- CP15 generated-software/model-deployment governance;
- legal/privacy/certification/insurance/advisory readiness;
- real anonymisation guarantee;
- real-world re-identification-risk validation;
- external data-space integration readiness;
- benchmark fairness and cohort-design validation;
- farmer-facing comprehension and coercion-risk validation;
- production/pilot validation.

### Hostile-reader verdict

CP14 is the correct next extension if it remains a boundary amendment.

The main failure mode is not conceptual absence; it is overclaiming. Cross-farm intelligence can become coercive, commercially dangerous, privacy-invasive, or operationally misleading if Advisory-default, sovereignty, recipient-use, derivative-use, training-use, revocation, applicability, output qualification, and re-identification-risk gates are not mechanically enforced.

The correct post-CP14 posture remains:

**implementation-directed with bounded debt, not production-ready, not a social platform, not an exchange platform, not a public benchmark product, not federated-learning-platform ready, not anonymisation-guarantee ready, not model-deployment ready, and not CP15-ready.**


## CP15 Agentic Software Delivery and Model Deployment Governance hostile-review addendum — 2026-05-30

### Hostile-reader verdict

CP15 is a necessary governance extension if OFARM is to operate in a future where agents generate software, adapters, mappings, workflows, prompts, policies, and model deployments.

A hostile reader should not treat CP15 as production software-delivery readiness, model-deployment readiness, cybersecurity certification, or an MLOps/CI-CD product implementation.

### Closed or substantially reduced by CP15

CP15 closes or reduces these conceptual gaps:

- generated software is no longer an untyped implementation side-effect;
- generated adapters and semantic mappings are governed candidates rather than hidden source-of-meaning changes;
- build success, test success, security scan success, conformance run success, canary success, deployment receipt, and telemetry are separated from deployment authority;
- security waivers require governed authority rather than informal override;
- release bundles and runtime-surface bindings become explicit;
- deployment authorization and deployment promotion decisions are separated;
- model deployment candidates require model-evaluation evidence and use constraints;
- CP13 learning output and CP14 model-improvement signals cannot become model deployment authority;
- CP11, CP12, CP13, and CP14 gates remain active for deployment-sensitive paths;
- current/default promotion remains governed and separate from deployment tooling.

### Still open and hostile-reader relevant

CP15 does not close:

- production CI/CD implementation;
- cloud/vendor deployment topology;
- generic MLOps implementation;
- cybersecurity certification;
- legal/security/privacy/compliance advice;
- real-world runtime deployment evidence;
- model performance validation in production;
- supply-chain security assurance;
- live rollback/canary proof;
- human/operator UX for release governance;
- current/default schema promotion;
- CP11/CP12/CP13/CP14 draft-schema currentness promotion.

### Hostile-reader risks after CP15

The main CP15 failure modes are:

- agent-generated code being treated as deployable because it compiles;
- conformance success being mistaken for deployment authority;
- security scan success being mistaken for security certification;
- canary success being mistaken for promotion authority;
- runtime deployment receipt being mistaken for production readiness;
- model-improvement signals becoming model deployment without review;
- semantic mappings weakening OFARM meaning;
- generated adapters bypassing CP11/CP12/CP13/CP14 gates;
- current/default promotion occurring through release tooling rather than governance.

### Hostile-review conclusion

CP15 should proceed only if it remains a delivery-governance amendment. It must not become a product implementation, CI/CD/MLOps platform, automatic release engine, legal/security certification framework, or currentness promotion shortcut.

### CP15 exact non-claim wording — 2026-05-30

CP15 does not claim production software-delivery readiness, production model-deployment readiness, autonomous release readiness, cybersecurity certification, legal/security/compliance/privacy/certification advice, full CI/CD product implementation, generic MLOps readiness, cloud/vendor deployment architecture readiness, automatic current/default schema promotion, CP11/CP12/CP13/CP14/CP15 draft schema promotion, mission authority through generated adapters, farm-to-farm intelligence deployment authority, OFARM Social constitution, or OFARM Exchange constitution.


# OFARM hostile review — CP15 update

Status: accepted/merged CP15 amendment hostile-review addendum  
Date: 2026-05-30

CP15 closes a major conceptual gap: generated software, generated adapters, generated mappings, prompt/workflow changes, model candidates, and release bundles are now governed as explicit delivery artifacts rather than hidden runtime authority.

## Closed or reduced

- Generated artifact does not become deployment authority.
- Build success, test success, scan success, conformance success, canary success, runtime receipt, telemetry, and agent tool success do not create production readiness.
- Deployment candidates, plans, authorizations, promotion decisions, release bundles, runtime bindings, receipts, canaries, rollback plans, and incidents are distinct.
- Model deployment candidates cannot bypass CP13 learning-output and CP14 training/model-improvement boundaries.
- Mission/robot-facing adapters must respect CP12.
- Sustainability-sensitive deployment surfaces must respect CP11.
- Machine contracts remain draft/non-default.

## Still open

- no production software-delivery readiness;
- no production model-deployment readiness;
- no generated-adapter production readiness;
- no cybersecurity certification;
- no autonomous release readiness;
- no full CI/CD product implementation;
- no generic MLOps platform;
- no cloud/vendor deployment topology;
- no automatic current/default schema promotion.

Hostile-reader verdict: CP15 is the correct governance closure if it remains narrow and draft/non-default until steward acceptance and currentness promotion.


# OFARM Final Hostile Review — CP14 Update

Status: final CP14 hostile-review update candidate  
Amendment: CP14 — Farm-to-Farm Intelligence Boundary

A hostile reader should treat CP14 as a necessary farm-to-farm intelligence boundary extension, not as evidence that OFARM is now a production intelligence network, social platform, exchange platform, federated-learning platform, public benchmarking product, anonymisation engine, legal/privacy compliance engine, or model-deployment platform.

## Closed or substantially reduced

CP14 reduces these conceptual gaps:

- received intelligence is Advisory by default;
- farm-to-farm sharing is not authority;
- aggregation is not anonymisation by assertion;
- regional alerts do not become farm-level truth;
- benchmark deltas do not become compliance facts;
- CP13 farm memory and local learning require CP14 governance before crossing farm boundaries;
- CP11 sustainability and CP12 mission/incident disclosures remain qualified;
- federated-learning contributions do not become model deployment authority;
- poisoning/anomaly review and contribution quality can block downstream use.

## Still open and hostile-reader relevant

CP14 does not close:

- production farm-to-farm intelligence readiness;
- production federated-learning readiness;
- privacy-law compliance;
- anonymisation guarantee;
- public benchmark product readiness;
- OFARM Social or Exchange constitution;
- CP15 model/software deployment governance;
- jurisdiction-specific cross-border data-space compliance;
- current/default CP14 machine-contract promotion.

## Hostile-reader verdict

CP14 is the correct boundary amendment if it remains narrow. The post-CP14 posture remains implementation-directed with bounded debt.
