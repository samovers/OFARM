## CP15 currentness note — 2026-05-30

Current package: `OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized`.

Latest controlled amendment: **CP15 — Agentic Software Delivery and Model Deployment Governance**.

CP11, CP12, CP13, and CP14 remain active where merged. CP15 does not promote CP11, CP12, CP13, CP14, or CP15 machine contracts to current/default. CP15 does not claim production software-delivery readiness, production model-deployment readiness, generated-adapter production readiness, cybersecurity certification, autonomous release readiness, full CI/CD product readiness, generic MLOps platform readiness, cloud/vendor deployment architecture readiness, legal/security/compliance advice, or automatic current/default schema promotion.

Older CP10, CP11, CP12, CP13, and CP14 currentness sections below are historical prior endpoint notes unless explicitly referenced by this CP15 currentness note.

# Project authority — CP15 current package note

# PROJECT_AUTHORITY — CP14 currentness overlay

## CP14 currentness note — 2026-05-30

Current package: `OFARM2_2026-05-30_cp14_farm_to_farm_intelligence_boundary_merged_v0_1_steward_remediated`.

Latest controlled amendment: **CP14 — Farm-to-Farm Intelligence Boundary**.

CP11, CP12, and CP13 remain active where merged. CP14 does not promote CP11, CP12, CP13, or CP14 machine contracts to current/default. CP14 does not claim production farm-to-farm intelligence readiness, production federated-learning readiness, anonymisation guarantee, legal/privacy/certification/insurance/advisory readiness, OFARM Social constitution, OFARM Exchange constitution, public benchmark product law, generic reputation law, model/software deployment governance, CP15 readiness, or current/default CP14 machine-contract promotion.

Older CP10, CP11, CP12, and CP13 currentness sections below are historical prior endpoint notes unless explicitly referenced by this CP14 currentness note.

## CP13 currentness note — 2026-05-29

Current package: `OFARM2_2026-05-29_cp13_learning_experimentation_farm_memory_merged_v0_2_steward_remediated`.

Latest controlled amendment: **CP13 — Learning, Experimentation, and Farm Memory**.

CP11 and CP12 remain active where merged. CP13 does not promote CP11, CP12, or CP13 machine contracts to current/default. CP13 does not claim farm-to-farm intelligence readiness, federated learning readiness, cross-farm benchmark readiness, regional-alert readiness, generated-software delivery readiness, model/software deployment governance readiness, livestock-specific learning law, production autonomous self-improvement readiness, or production agronomic advice certification.


# OFARM 2 migration control plane v0.6.4

> CP12 steward-remediated currentness: current package endpoint is `OFARM2_2026-05-28_cp12_cyber_physical_mission_envelope_merged_v0_2_steward_remediated`. Latest controlled amendment is CP12 — Cyber-Physical Mission Envelope. AAI-CP10 remains historical agentic-AI controlled-promotion lineage, and CP11 remains the prior accepted Sustainable Autonomous Farming Charter amendment. CP12 machine contracts are draft/non-default only. No production robot/machine readiness, autonomous field-operation readiness, legal/safety certification, fleet optimisation law, vendor protocol conformance, or CP13/CP14/CP15 readiness is claimed.



Created: 2026-04-10T00:00:00Z  
Updated: 2026-05-20T16:30:00+02:00

## Purpose

This file tells a new OFARM 2 project what is:
- active substance
- active supporting material
- review holding material
- read-only contextualization
- package metadata/navigation

This is the authoritative interpretation rule for this migration package.

## Status classes

### ACTIVE_SUBSTANCE
Material that should be treated as part of the active OFARM 2 baseline.

This includes:
- `00_active_baseline/`
- `02_accepted_rfcs/`
- `01_companion_artifacts/`
- `03_machine_contracts/`

`02_accepted_rfcs/` may also contain accepted closure artifacts intentionally colocated with the accepted RFC set when they are introduced by those RFCs.

### ACTIVE_SUPPORTING_IMPLEMENTATION
Material that supports implementation, conformance, or spike work, but does not outrank baseline law.

This includes:
- `04_implementation_and_conformance/`

### ACTIVE_SUPPORTING_RESEARCH
Material that informs further OFARM 2 development, but does not outrank baseline law.

This includes:
- `06_active_supporting_research/`

### ACTIVE_SUPPORTING_CONTEXT
Material that supports onboarding, handoff, reviewer operation, linked-domain architectural framing, or research continuity, but is not active semantic/runtime law.

This includes:
- `05_project_handoff_and_prompts/`
- `07_linked_domain_architectures/`

### REVIEW_HOLDING
Reviewed candidate, deferred, review, and provenance material carried inside the repository for later selective merge.

This includes archived review-holding snapshots preserved under `archive/review_holding/`. The former root `reviewed_*` folders are no longer default-visible repository folders.

Aggregate navigation: `REVIEW_HOLDING_INDEX.json` and `archive/review_holding/REVIEW_HOLDING_ARCHIVE_INDEX.json`.

Rule:
- this material is not part of the active authority set by default
- it may inform later promotion or selective merge work
- active-looking paths inside archived review-holding snapshots, including copied `00_active_baseline/`, `02_accepted_rfcs/`, `01_companion_artifacts/`, or `03_machine_contracts/` folders, remain review-holding/source-context material
- the root active folders always outrank it

### READ_ONLY_CONTEXT
Legacy material preserved for reference only.

This includes:
- `legacy_reference/`

Rule:
- these materials may inform OFARM 2 decisions
- they must not override RC2.1 or accepted OFARM 2 RFCs
- they must remain clearly segregated from active baseline material

### PACKAGE_META
Package metadata, repository maps, inventories, changelogs, stewardship tools, and historical package assembly records.

This includes:
- root control files such as `README.md`, `CURRENT_PACKAGE_CHANGELOG.md`, `PROJECT_AUTHORITY.md`, `REVIEW_HOLDING_INDEX.*`, `05_project_handoff_and_prompts/prompts/PROJECT_PROMPT.md`, `MANIFEST.csv`, and `MATERIAL_STATUS.*`
- `package_meta/`
- navigational-only `README.md` or `INDEX.md` files inside numbered folders when their role is explicitly repository navigation rather than normative content

Rule:
- PACKAGE_META files help readers and tools navigate the package
- they do not create semantic or runtime law by themselves

## Authority order

When files disagree, use this order:

1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`
5. `04_implementation_and_conformance/`
6. `06_active_supporting_research/`
7. `07_linked_domain_architectures/`
8. `05_project_handoff_and_prompts/`
9. `archive/review_holding/`
10. `legacy_reference/`

PACKAGE_META does not create semantic/runtime law. Use it for navigation, inventory, and package-history interpretation only.

## Naming rule

Inside the new project:
- OFARM and OFARM Platform are the only active names
- `fa_rm`, `farm_rm`, and `Farm-RM` remain legacy names and belong only in `legacy_reference/`

## Practical import rule

If you import this package into a new project:
- import `00_active_baseline/` first
- then `02_accepted_rfcs/`
- then `01_companion_artifacts/`
- then `03_machine_contracts/`
- optionally import `04_implementation_and_conformance/`
- optionally import `06_active_supporting_research/`
- optionally import `07_linked_domain_architectures/` when sister-platform or adjacent-domain framing matters
- optionally import `05_project_handoff_and_prompts/`
- preserve review-held snapshots through `archive/review_holding/` and `REVIEW_HOLDING_INDEX.json` only as reviewed holding areas unless and until selective promotion occurs
- import `legacy_reference/` only as read-only archival context

## Machine-readable status map

The authority classes in this file are the governing interpretation classes. `MATERIAL_STATUS.csv` and `MATERIAL_STATUS.json` use finer package-inventory labels so tools can distinguish active baseline, companion artifacts, accepted RFCs, machine contracts, implementation/conformance material, research, handoff/context, review holding, legacy, and package metadata.

Use `STATUS_TAXONOMY.md` and `STATUS_TAXONOMY.json` as the required crosswalk between:

- authority classes in this file;
- material-status inventory classes;
- AI-agent source classes in `AGENT_NAVIGATION.md`.

See:
- `STATUS_TAXONOMY.md`
- `STATUS_TAXONOMY.json`
- `MATERIAL_STATUS.csv`
- `MATERIAL_STATUS.json`

See also:
- `05_project_handoff_and_prompts/prompts/PROJECT_PROMPT.md`


### ONT-SEMINT active additions — 2026-05-14

The ONT-SEMINT v0.1 amendment adds active companion artifacts, accepted RFC extensions, and machine contracts under the existing authority order. It also adds supporting conformance runners under `04_implementation_and_conformance/`.

At v0.1, the amendment did not edit active RC2.1 baseline files. That no-baseline-edit posture is superseded by ONT-SEMINT v0.3 Phase 6 baseline harmonisation. Review-holding and legacy material still are not promoted into active law.


## ONT-SEMINT v0.2 continuation — authority posture

The Phase 4/5 continuation adds active supporting research, accepted RFC extension material, machine contracts, examples, and conformance runners for a narrow Belgium/Phytoweb external currentness profile and operational break-test suite.

These additions do not amend the active RC2.1 baseline. They do not claim live registry integration, legal advice, production readiness, external-standard readiness, or livestock scope expansion. Review-holding and legacy material remain subordinate to the active authority set.

## ONT-SEMINT v0.3 baseline harmonisation — authority posture

The Phase 6 continuation amends the active RC2.1 baseline files with controlled ONT-SEMINT semantic-integrity addenda. These baseline addenda now sit at the top of the normal authority order because they are inside `00_active_baseline/`.

The harmonisation is narrow. It promotes the already-supported semantic-integrity closures for reference resolution, semantic conformance levels, carrier-field canonicalization, temporal conformance, high-consequence query/output gating, external-currentness verification, and PassportView/DocumentAssembly disposition. It does not promote review-holding material, does not import external registries as hidden OFARM law, and does not claim production readiness, live registry integration, legal advice, external-standard readiness, or livestock scope expansion.

## Final pre-implementation consolidation marker — 2026-05-14

`OFARM2_2026-05-14_preimplementation_consolidated_FINAL_v1_0` is the historical final consolidated package for the ONT-SEMINT pre-implementation scope. It is superseded as the current package by `OFARM2_2026-05-17_agentic_ai_controlled_promotion_cp10_v0_1`.

Authority status of final additions:

- `package_meta/preimplementation_final_consolidation_2026-05-14/` is package metadata and does not override active baseline law.
- `06_active_supporting_research/source_inputs/deep-research-report-27.md` is active supporting research source input and does not override active baseline law by itself.
- `05_project_handoff_and_prompts/prompts/OFARM_Implementation_Live_Pilot_Lane_Prompt_v0_1.md` is handoff/prompt material for implementation continuation.

The active RC2.1 baseline was harmonised by ONT-SEMINT v0.3 Phase 6 before this final consolidation. This final consolidation adds no further baseline-law changes.

## Agentic AI / World Model Amendment AAI-P1 — authority posture

AAI-P1 amends the active RC2.1 baseline files with protective baseline-safety clarifications for agentic AI and world-model continuation. Because the addenda are inserted into `00_active_baseline/`, they sit at the top of the normal authority order.

The AAI-P1 harmonisation is narrow. It does not promote supporting draft schemas or RFCs into active law. It clarifies that AI outputs, agent memory, world-model state, public surfaces, tool-call success, projections, caches, and compiled-output previews do not create canonical truth or governance decisions by themselves.

The supporting folder `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/` remains active supporting implementation/conformance material unless specific artifacts are explicitly promoted later.


## Agentic AI / World Model Controlled Promotion CP1 — authority posture

AAI-CP1 amends the active RC2.1 baseline files with a narrow AI-facing release-qualification gate. Because the addenda are inserted into `00_active_baseline/`, they sit at the top of the normal authority order.

The CP1 harmonisation is limited to baseline law for release eligibility. It requires AI-facing, public-operation, state-affecting, and high-consequence surfaces to produce machine-readable material qualification and to fail review/refusal when required qualification is unavailable.

CP1 does not promote `ResultQualificationEnvelope`, public-operation, preflight, trace-retrieval, agent-run, agent-actorship, tool-manifest, world-model, EvidenceNeed, or ObservationRequest schemas into active machine-contract law by itself. Later CP2 through CP8 sections below explicitly promote bounded active RFC/contract layers; remaining AAI-P support material remains supporting-only unless explicitly promoted.


## Repository stewardship currentness patch — 2026-05-15

This patch updates package metadata, navigation, generated indexes, and validation controls only.

It does not:
- change active baseline law;
- promote draft agentic/world-model schemas or RFCs;
- promote review-holding material;
- change the active authority order;
- claim production/runtime/external-standard readiness.

New package-control files added by this patch include:
- `CURRENT_DELTA.md`
- `STATUS_TAXONOMY.md`
- `STATUS_TAXONOMY.json`
- `TRACEABILITY_INDEX.md`
- `TRACEABILITY_INDEX.json`
- `SOURCE_INPUT_INDEX.md`
- `SOURCE_INPUT_INDEX.json`
- `03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.md`
- `03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json`
- local folder README files in `00_active_baseline/`, `01_companion_artifacts/`, and `02_accepted_rfcs/`

## Repository cleanup and handover-readiness note — 2026-05-15

The repository-cleanup pass reorganizes package metadata, root overlays, machine-contract placement, implementation/conformance lanes, and review-holding indexes. It does not change active model law, does not promote draft machine contracts, and does not promote review-holding or legacy material.

Current cleanup artifacts live under `package_meta/repository_cleanup_2026_05_15/`. Root-level current package navigation remains governed by this file, `CURRENT_ACTIVE_ENTRYPOINT.md`, `STATUS_TAXONOMY.json`, `MATERIAL_STATUS.json`, and `AGENT_NAVIGATION.md`.

## Agentic AI / World Model Controlled Promotion CP2 — authority posture

AAI-CP2 adds accepted RFC extensions and active machine contracts for the public-surface layer required to execute the CP1 release-qualification gate. CP2 is active substance through `02_accepted_rfcs/` and `03_machine_contracts/`; it does not edit `00_active_baseline/`.

The CP2 promotion is limited to public operation descriptors, preflight/dry-run request/result, runtime problem reason-code registry, result qualification envelope, trace retrieval result, public read-model envelope, and source-fidelity envelope.

CP2 does not promote agent actorship, agent run/trace/handoff, tool-manifest, world-model, EvidenceNeed, ObservationRequest, output assembly preview, runtime AI-agent readiness, two-agent compatibility, autonomous compliance decisioning, production readiness, live-registry integration, legal advice, or external-standard readiness.

## Agentic AI / World Model Controlled Promotion CP3 — authority posture

AAI-CP3 adds a bounded active sponsor-bound software-agent actorship layer. CP3 amends active baseline files, adds one accepted RFC, and promotes eight authority-lane machine contracts.

The CP3 promotion is limited to `SoftwareAgentProfile`, `AgentInstance`, `AgentSponsorRef`, `AgentModelToolProfile`, `AgentAuthorityEnvelope`, `AgentRevocationState`, `AgentActorshipBinding`, and `AgentAuthorizationDecisionTrace`.

CP3 does not promote agent run/trace/handoff, tool-manifest, world-model, EvidenceNeed, ObservationRequest, runtime AI-agent readiness, two-agent compatibility, autonomous compliance decisioning, production readiness, live-registry integration, legal advice, or external-standard readiness.



## Agentic AI / World Model Controlled Promotion CP4 — authority posture

AAI-CP4 adds a bounded active software-agent run, trace, blocked-action trace, output-disposition, and handoff layer. CP4 amends active baseline files, adds one accepted RFC, and promotes ten agent-runtime machine contracts.

The CP4 promotion is limited to `AgentRunEnvelope`, `AgentRunTrace`, `AgentToolInvocationTrace`, `AgentOutputDisposition`, `AgentBlockedActionTrace`, `AgentHandoffEnvelope`, `AgentRunInputBundle`, `AgentRunStopCondition`, `AgentRunApprovalCheckpoint`, and `AgentRunFreshnessRequirement`.

CP4 does not promote `AgentToolManifest`, world-model runtime, `EvidenceNeed`, `ObservationRequest`, output assembly preview, runtime AI-agent readiness, two-agent compatibility, autonomous compliance decisioning, production readiness, live-registry integration, legal advice, or external-standard readiness.

## Agentic AI / World Model Controlled Promotion CP5 — authority posture

AAI-CP5 adds a bounded active capability/tool manifest honesty layer. CP5 amends active baseline consistency files, adds one accepted RFC, adds one companion policy, and promotes active machine contracts under `03_machine_contracts/schemas/agent_manifest/`.

CP5 does not make a tool manifest an authority grant, safety proof, runtime-readiness proof, or autonomous compliance basis. It does not promote world-model runtime, `EvidenceNeed`, `ObservationRequest`, production readiness, live-registry integration, legal advice, or external-standard readiness.

## Agentic AI / World Model Controlled Promotion CP6 — authority posture

AAI-CP6 adds selected hostile runtime conformance stub evidence under `04_implementation_and_conformance/`. CP6 does not add active baseline law, accepted RFCs, companion artifacts, or machine-contract schemas.

The CP6 evidence is synthetic, package-local, and implementation/conformance-only. It may support implementation targeting of already-promoted bounded layers, but it does not claim full runtime AI-agent readiness, general two-agent compatibility, production readiness, legal advice, live-registry integration, or external-standard readiness.

## Agentic AI / World Model Controlled Promotion CP7 — authority posture

AAI-CP7 adds a bounded active Advisory Twin world-model contract layer. CP7 amends active baseline consistency files, adds one accepted RFC, and promotes active machine contracts under `03_machine_contracts/schemas/world_model/`.

The CP7 promotion is limited to `WorldModelRun`, `WorldModelState`, `WorldModelInputBasis`, `WorldModelObservationBasis`, `WorldModelAssumptionSet`, `WorldModelUncertaintyStatement`, `WorldModelValidityWindow`, `WorldModelInvalidationRule`, `WorldModelOutputDisposition`, `WorldModelGovernanceBlocker`, `WorldModelReconciliationRecord`, `ScenarioSpec`, and `ScenarioResultSet`.

CP7 does not promote `WorldModelCalibrationEvidence`, `EvidenceNeed`, `ObservationRequest`, output assembly preview, world-model readiness, runtime AI-agent readiness, autonomous compliance decisioning, production readiness, legal advice, live registry integration, or external-standard readiness.

## Agentic AI / World Model Controlled Promotion CP8 — authority posture

AAI-CP8 adds a bounded active request-layer contract family for EvidenceNeed, ObservationRequest, and farmer-burden/noise/display controls. CP8 amends active baseline consistency files, adds one accepted RFC, adds one companion policy, and promotes active machine contracts under `03_machine_contracts/schemas/request_layer/`.

The CP8 promotion is limited to request-layer semantics. Requests may ask for information and cite external consequences, but they do not become evidence, obligations, or blockers by themselves.

CP8 does not promote minimum capture profile law, formula/default calculation law, output assembly preview, farmer UX readiness, runtime AI-agent readiness, autonomous compliance decisioning, production readiness, legal advice, live registry integration, or external-standard readiness.

## Agentic AI / World Model Controlled Promotion CP9 — authority posture

AAI-CP9 adds farmer-value UX scenario conformance fixtures and a runner under `04_implementation_and_conformance/`. CP9 does not add active baseline law, accepted RFCs, companion artifacts, or machine-contract schemas.

The CP9 evidence is synthetic, package-local, and implementation/conformance-only. It does not claim farmer UX readiness, live farmer-pilot evidence, production readiness, autonomous compliance decisioning, legal advice, live-registry integration, or external-standard readiness.

## Agentic AI / World Model Controlled Promotion CP10 — authority posture

AAI-CP10 updates final readiness and claim-limit posture after CP1 through CP9. It amends two active baseline memo files, so those readiness/hostile-review addenda are active baseline interpretation material.

CP10 does not add accepted RFCs, companion artifacts, or machine contracts. It does not create new semantic law, does not promote reviewed material, and does not claim production readiness, full runtime AI-agent readiness, general two-agent compatibility, autonomous compliance decisioning, world-model readiness, farmer UX readiness, legal advice, live-registry integration, or external-standard readiness.

Supporting CP10 artifacts live under `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP10_final_readiness_claim_limits_v0_1/` and remain active supporting implementation/conformance material.


## Phase 12 legacy-reference cleanup

The repository-cleanup pass now includes `legacy_reference/LEGACY_REFERENCE_INDEX.json` and `.md`, plus local README/status guardrails for legacy folders. This does not promote legacy material into active law. Legacy FA_RM / FARM_RM / Farm-RM material remains read-only contextualization and loses to the active baseline, accepted RFCs, companion artifacts, and machine-contract currentness maps.

## Phase 14 repository cross-reference cleanup

The repository-cleanup pass now includes `REPOSITORY_CROSS_REFERENCE_SCAN.json` and `.md`, plus `package_meta/tools/check_repository_cross_references.py`. These files enforce repository stewardship checks for current-repository links, stale currentness language, duplicate basenames, and non-active schema-copy indexing. They are PACKAGE_META only and do not create active semantic/runtime law.


## CP12 Cyber-Physical Mission Envelope — current package posture

Current package endpoint: `OFARM2_2026-05-28_cp12_cyber_physical_mission_envelope_merged_v0_2_steward_remediated`.

CP12 is the latest controlled amendment. It is active as bounded baseline/RFC/companion/conformance law after steward remediation. CP12 machine contracts remain draft/non-default and are not current/default machine contracts.

CP10 and CP11 are historical prior endpoints; CP11 remains merged active law where accepted, but CP12 is current.

CP12 does not claim production robot/machine readiness, autonomous field-operation readiness, legal/safety certification, fleet optimisation law, vendor protocol conformance, livestock-specific mission law, or CP13/CP14/CP15 readiness.