# Patch apply guide — AAI-CP3

Apply CP3 on top of the AAI-CP2 package.

## Active changes

1. Amend the five active baseline files with sponsor-bound software-agent authority and readiness-gate language.
2. Add `02_accepted_rfcs/OFARM_Agent_Actorship_and_Authority_RFC_v0_1.md`.
3. Add eight active authority-lane schemas under `03_machine_contracts/schemas/authority/`.
4. Add tier-04 examples and authority fixtures.
5. Add CP3 controlled-promotion support material.
6. Regenerate manifests, material-status files, contract indexes, traceability indexes, and package metadata.
7. Run:

```bash
python3 04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP3_agent_actorship_sponsor_bound_authority_v0_1/conformance/runners/ofarm_aai_cp3_agent_actorship_contract_runner_v0_1.py
python3 package_meta/tools/validate_repo_hygiene.py
```

## Non-claims

CP3 does not claim runtime AI-agent readiness, two-agent compatibility, agent-run/handoff readiness, tool-manifest readiness, world-model readiness, EvidenceNeed/ObservationRequest readiness, autonomous compliance decisioning, production readiness, or external-standard readiness.

## CP3 quality patch — authority-action posture map

Added `03_machine_contracts/maps/authority/OFARM_Agent_Authority_Action_Class_Posture_Map_v0_1.json` so every software-agent AuthorityActionClass posture is explicitly declared rather than left as prose-only guidance.
