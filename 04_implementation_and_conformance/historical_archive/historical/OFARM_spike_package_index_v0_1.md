
# OFARM spike package index v0.1

Date: 2026-04-10  
Status: repaired packaged spike index  
Scope: list the delivered packaged spike inputs, outputs, and fixture classes

## Executable spike inputs

### Fixtures
- `ofarm_spike_v0_1/fixtures/authority_buyer_deny.json`
- `ofarm_spike_v0_1/fixtures/authority_service_provider_allow.json`
- `ofarm_spike_v0_1/fixtures/current_state_invalidation_pack_change.json`
- `ofarm_spike_v0_1/fixtures/identity_cropcycle_replant.json`
- `ofarm_spike_v0_1/fixtures/identity_field_revision_vs_split.json`
- `ofarm_spike_v0_1/fixtures/identity_lot_commingle.json`
- `ofarm_spike_v0_1/fixtures/pack_merge_evidence_policy.json`
- `ofarm_spike_v0_1/fixtures/pack_merge_template_fail.json`

### Design fixture
- `ofarm_spike_v0_1/fixtures/vertical_slice.json`

### Schemas and examples
- `ofarm_spike_v0_1/schemas/capabilitymanifest_example_core.json`
- `ofarm_spike_v0_1/schemas/capabilitymanifest_v0_1.json`
- `ofarm_spike_v0_1/schemas/queryplanir_example_field_passport.json`
- `ofarm_spike_v0_1/schemas/queryplanir_v0_1.json`
- `ofarm_spike_v0_1/schemas/queryspec_example_field_passport.json`
- `ofarm_spike_v0_1/schemas/queryspec_v0_1.json`

### Harness and results
- `ofarm_spike_v0_1/ofarm_reference_spike_harness_v0_1.py`
- `ofarm_spike_v0_1/OFARM_reference_spike_harness_run_results_v0_1.json`
- `OFARM_reference_spike_harness_run_results_v0_1.json`
- `OFARM_spike_reproducibility_note_v0_1.md`

## Classification rule

- JSON fixtures validated or evaluated by the packaged harness are **executable fixtures**.
- `vertical_slice.json` is a **design fixture** that documents the integrated path without claiming executable full-stack implementation.

## Package-relative rerun command

From the package root:

```bash
python 04_implementation_and_conformance/spikes_incubation/ofarm_spike_v0_1/ofarm_reference_spike_harness_v0_1.py
```
