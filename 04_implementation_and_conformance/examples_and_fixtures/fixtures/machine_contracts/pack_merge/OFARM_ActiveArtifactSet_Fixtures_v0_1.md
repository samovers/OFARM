# OFARM ActiveArtifactSet fixtures v0.1

Date: 2026-04-10  
Status: executable/conformance fixture note  
Scope: baseline active-artifact-state fixtures used to ground capability-manifest consistency checks

---

## Purpose

The Capability Manifest RFC already requires `activeArtifactSetRef`, but the earlier package did not ship an executable contract for the referenced state.
These fixtures close that gap for a minimal deployment/tenant subset.

---

## Fixtures

### Fixture 1 — core deployment active state
Expected:
- core deployment manifest grounds successfully against the core active artifact set

### Fixture 2 — partner deployment active state
Expected:
- partner tenant manifest grounds successfully against the tenant active artifact set

### Fixture 3 — partner mismatch missing orchard
Expected:
- consistency check fails because the manifest claims `pack:orchard:v1` active while the referenced active artifact state omits it

---

## Executable evidence

Machine-contract examples live under:
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/pack_merge/OFARM_ActiveArtifactSet_example_*.json`

Executable results are written to:
- `04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_governance_runtime_closure_results_v0_1.json`


### Fixture 4 — linked runtime-surface grounding lane
Expected:
- the linked Capability Manifest draft grounds against a dedicated ActiveArtifactSet
- supported and partial runtime-surface contract refs used by the linked manifest are present in active artifact state
- planned query/event surface lanes may remain outside active artifact state without failing linkage grounding
