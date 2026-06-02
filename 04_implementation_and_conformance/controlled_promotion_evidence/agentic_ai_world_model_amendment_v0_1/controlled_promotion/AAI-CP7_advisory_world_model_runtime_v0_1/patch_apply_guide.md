# CP7 patch apply guide

Apply this patch after AAI-CP6.

Main active additions:

- `02_accepted_rfcs/OFARM_World_Model_Advisory_Runtime_RFC_v0_1.md`
- `03_machine_contracts/schemas/world_model/`
- CP7 addenda to active baseline consistency files

Then run:

```bash
python3 04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP7_advisory_world_model_runtime_v0_1/conformance/ofarm_cp7_advisory_world_model_conformance_runner_v0_1.py
python3 package_meta/tools/validate_repo_hygiene.py
```

CP7 must not be described as world-model readiness or production readiness.
