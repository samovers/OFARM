# CP9 patch apply guide

Apply this patch on top of `OFARM2_2026-05-16_agentic_ai_controlled_promotion_cp8_v0_1`.

CP9 adds only implementation/conformance artifacts and metadata updates. It does not modify active baseline files, accepted RFCs, companion artifacts, or machine contracts.

Primary folder added:

`04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP9_farmer_value_ux_scenario_conformance_v0_1/`

After applying, run:

```bash
python3 04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP9_farmer_value_ux_scenario_conformance_v0_1/conformance/ofarm_cp9_farmer_value_ux_conformance_runner_v0_1.py > 04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP9_farmer_value_ux_scenario_conformance_v0_1/conformance/validation_report.json
python3 package_meta/tools/validate_repo_hygiene.py
```
