## CP15 draft/non-default currentness note — 2026-05-30

CP15 agentic software delivery and model deployment governance schemas are staged under `03_machine_contracts/drafts_non_default/agentic_software_delivery_model_deployment/`. They are not current/default schemas until a separate currentness-promotion decision.

# 03_machine_contracts

Status: active machine-contract source lane, subordinate to the active baseline/RFC authority order.

This folder holds source schemas, draft/non-default schemas, contract maps, and generated contract indexes. Examples and fixtures live under `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/` and `04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/` so they cannot be mistaken for active contract law.

Use these files first:

- `CONTRACT_FAMILY_CURRENTNESS.json` — current/default/draft family currentness map.
- `CONTRACT_INDEX.json` — file-level contract index for this folder.
- `EXAMPLE_SCHEMA_MAP.json` — map from tier-04 examples to the schemas they exercise.
- `DRAFT_NON_DEFAULT_INDEX.json` — draft and non-default contract/material index.
- `PATH_REMAPS.json` — old-to-new paths after cleanup moves.

This folder does not by itself promote draft contracts. Current/default selection remains governed by the baseline/RFC authority chain and the currentness map.

## Current package posture

AAI-CP10 promoted no new machine-contract families. It refreshed readiness and claim-limit posture only. Do not infer production readiness, autonomous compliance decisioning, world-model readiness, farmer UX readiness, live-pilot readiness, legal advice readiness, or external-standard readiness from these schemas.

## Active CP-promoted contract families

| CP | Contract area | Folder | Promoting / governing artifact | Non-claims |
|---|---|---|---|---|
| AAI-CP2 | public runtime surface, preflight, result qualification, trace retrieval, source fidelity | `schemas/runtime_surface/` | `02_accepted_rfcs/OFARM_AI_Facing_Result_Qualification_and_Trace_Surface_RFC_v0_1.md` and related runtime-surface RFCs | Does not establish production runtime readiness. |
| AAI-CP3 | sponsor-bound software-agent actorship and authority posture | `schemas/authority/` | `02_accepted_rfcs/OFARM_Agent_Actorship_and_Authority_RFC_v0_1.md` | Does not grant autonomous compliance decisioning or tool/run authority by itself. |
| AAI-CP4 | agent run envelope, trace, blocked action, approval checkpoint, handoff | `schemas/agent_runtime/` | `02_accepted_rfcs/OFARM_Agent_Run_Envelope_Trace_and_Handoff_RFC_v0_1.md` | Does not establish runtime AI-agent readiness. |
| AAI-CP5 | agentic capability/tool manifest and honesty limits | `schemas/agent_manifest/` | `02_accepted_rfcs/OFARM_Capability_Manifest_Agentic_Extension_RFC_v0_1.md` | Does not grant authority or prove capability; declarations remain bounded and auditable. |
| AAI-CP7 | Advisory Twin world-model runtime contracts | `schemas/world_model/` | `02_accepted_rfcs/OFARM_World_Model_Advisory_Runtime_RFC_v0_1.md` | Does not make world-model state current state or compliance evidence by itself. |
| AAI-CP8 | EvidenceNeed, ObservationRequest, request-burden/noise/display controls | `schemas/request_layer/` | `02_accepted_rfcs/OFARM_EvidenceNeed_and_ObservationRequest_RFC_v0_1.md` | Requests are not evidence, obligations, or blockers without explicit external basis. |

## Active non-default contract note

`03_machine_contracts/schemas/evidence/OFARM_EvidenceSufficiencyCase_schema_v0_1.json` is retained as `active_non_default_superseded_by_current_default`. The current default for `EvidenceSufficiencyCase` is `03_machine_contracts/schemas/evidence/OFARM_EvidenceSufficiencyCase_schema_v0_2.json`.

## Duplicate-name caution

Some support or review folders outside `03_machine_contracts/` contain draft or review-copy schemas with the same filenames as active schemas. They are not current/default contract sources. Select active schemas by `CONTRACT_FAMILY_CURRENTNESS.json` and `CONTRACT_INDEX.json`, not by filename search alone.

## Path remaps currentness

`PATH_REMAPS.json` separates `sourcePackage` lineage from `currentPackage` applicability. It is navigation metadata and does not create active law.


## CP11 draft/non-default sustainability-charter contracts — 2026-05-28

CP11 adds draft/non-default machine-contract schemas under:

- `03_machine_contracts/drafts_non_default/sustainability_charter/`
- `03_machine_contracts/drafts_non_default/pack_contract_patches/`

These schemas support the accepted CP11 RFC and conformance evidence, but they are **not current/default active machine contracts** until a separate currentness-promotion decision updates the main currentness maps.

## CP12 draft/non-default cyber-physical mission contracts — 2026-05-28

CP12 adds draft/non-default machine-contract schemas under:

- `03_machine_contracts/drafts_non_default/cyber_physical_mission/`

These schemas support the accepted CP12 RFC and conformance evidence, but they are **not current/default active machine contracts** until a separate currentness-promotion decision updates the main currentness maps. They do not claim production robot/machine readiness, autonomous field-operation readiness, safety certification, vendor protocol completeness, CP13, CP14, or CP15 readiness.


## CP14 draft/non-default currentness note — 2026-05-30

CP14 adds draft/non-default machine contracts under `03_machine_contracts/drafts_non_default/farm_to_farm_intelligence_boundary/`. They are not current/default until a separate currentness-promotion decision.
