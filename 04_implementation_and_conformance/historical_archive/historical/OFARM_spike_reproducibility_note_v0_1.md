
# OFARM spike reproducibility note v0.1

Date: 2026-04-10  
Status: active supporting implementation note  
Scope: document how to rerun the delivered spike package from package-relative inputs

## Exact command

Run from the package root:

```bash
python 04_implementation_and_conformance/spikes_incubation/ofarm_spike_v0_1/ofarm_reference_spike_harness_v0_1.py
```

## Runtime requirement

The harness requires the Python `jsonschema` package.

## Package-relative inputs

The harness reads only from:
- `04_implementation_and_conformance/spikes_incubation/ofarm_spike_v0_1/fixtures/`
- `04_implementation_and_conformance/spikes_incubation/ofarm_spike_v0_1/schemas/`

It writes:
- `04_implementation_and_conformance/spikes_incubation/ofarm_spike_v0_1/OFARM_reference_spike_harness_run_results_v0_1.json`

A package-level copy is also maintained at:
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_reference_spike_harness_run_results_v0_1.json`

## What this proves

The spike remains intentionally narrow. It proves that the packaged schemas and seed fixtures are executable together, not that the vertical slice is a production implementation.
