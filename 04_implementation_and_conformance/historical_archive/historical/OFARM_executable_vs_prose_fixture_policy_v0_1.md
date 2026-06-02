
# OFARM executable vs prose fixture policy v0.1

Date: 2026-04-10  
Status: active supporting implementation policy  
Scope: define when a fixture may be presented as executable rather than merely descriptive

---

## 1. Rule

A fixture may be called **executable** only when all of the following are true:
- it is machine-readable
- the package contains a validator, runner, or test path that actually consumes it
- the package contains a result artifact or a clearly documented rerun command

If any of those are missing, the fixture is **design/prose only**.

---

## 2. Definitions

### Executable fixture
A machine-readable fixture that the delivered package can run or validate directly.

Examples in this package:
- `04_implementation_and_conformance/spikes_incubation/ofarm_spike_v0_1/fixtures/*.json` except `vertical_slice.json`
- `04_implementation_and_conformance/spikes_incubation/ofarm_spike_v0_1/schemas/*.json`
- machine-contract examples validated by `04_implementation_and_conformance/historical_archive/historical_archive/historical/ofarm_contract_validation_runner_v0_1.py`

### Design fixture
A scenario, negative case, or expected-behavior artifact that documents intent but is not yet wired into a runnable/validatable path.

Examples in this package:
- `04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/pack_merge/OFARM_Pack_Merge_Semantics_Fixtures_v0_1.md`
- `04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/runtime_surface/OFARM_Capability_Manifest_Fixtures_v0_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_spike_failure_case_examples_v0_1.md`
- `04_implementation_and_conformance/spikes_incubation/ofarm_spike_v0_1/fixtures/vertical_slice.json`

---

## 3. Presentation rule

Package docs must not present a prose/design fixture as if it were already executable.

Allowed wording:
- “design fixture”
- “prose fixture”
- “scenario target for future executable conformance”

Disallowed wording unless a runner exists:
- “validated fixture”
- “runnable test case”
- “packaged pass result”

---

## 4. Current package mapping

| Artifact | Class | Evidence path |
|---|---|---|
| `ofarm_spike_v0_1/fixtures/identity_*` | Executable | `ofarm_reference_spike_harness_v0_1.py` |
| `ofarm_spike_v0_1/fixtures/pack_merge_*` | Executable | `ofarm_reference_spike_harness_v0_1.py` |
| `ofarm_spike_v0_1/fixtures/authority_*` | Executable | `ofarm_reference_spike_harness_v0_1.py` |
| `ofarm_spike_v0_1/fixtures/current_state_*` | Executable | `ofarm_reference_spike_harness_v0_1.py` |
| `ofarm_spike_v0_1/fixtures/vertical_slice.json` | Design fixture | documented only |
| query/capability/trace/materialization example JSONs in `03_machine_contracts/` | Executable | `ofarm_contract_validation_runner_v0_1.py` |
| markdown fixture sets in `03_machine_contracts/` | Design fixture | documented only |

---

## 5. Upgrade path

A design fixture becomes executable only when:
- a machine-readable representation exists
- a validator/runner exists
- the result is captured in package evidence
