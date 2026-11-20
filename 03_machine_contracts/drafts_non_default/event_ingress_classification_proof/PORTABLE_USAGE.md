# Offline pre-verdict Event Ingress proof candidate

This is a non-default contract in the **Event Ingress classification and evidence admission** boundary. Scope stays inside that boundary. Read `PROPOSAL.md` for the trusted inputs, source qualifications and reuse rules. Success means conditional offline conformance; runtime admission is not established.

## Dependencies and repository layout

Use Python with locally installed `rfc8785==0.1.4` and `jsonschema`. Historical tested versions and the required RFC 8785 implementation hashes are in `dependency-manifest.json`. No command below downloads code. An optional `--dependency-dir /absolute/path/to/local/site-packages` selects existing dependencies for the direct runner or checker; omit it when dependencies are installed normally.

The repository uses three separate roots:

| Root | Repository path | Contents |
| --- | --- | --- |
| Contract | `03_machine_contracts/drafts_non_default/event_ingress_classification_proof/` | `contract.json`, `schemas/`, `source-contracts/`, `source-pins.json`, documentation |
| Checker | `04_implementation_and_conformance/conformance_runners/event_ingress_classification_proof/` | `verify_event_proof.py`, adjacent `report_contract.py`, `run_conformance.py` |
| Fixture and source | `04_implementation_and_conformance/examples_and_fixtures/fixtures/event_ingress_classification_proof/` | `classification-profile.json`, `fixtures/`, verbatim `sources/`, compact conformance and historical review evidence |

## Run from a repository checkout

With dependencies installed normally, run this wrapper from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  04_implementation_and_conformance/conformance_runners/ofarm_event_ingress_classification_proof_v0_1.py
```

The wrapper sets all three roots and uses an external temporary output directory. To retain fresh evidence, use the direct runner from the repository root with an output directory outside the checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  04_implementation_and_conformance/conformance_runners/event_ingress_classification_proof/run_conformance.py \
  --package-root 03_machine_contracts/drafts_non_default/event_ingress_classification_proof \
  --fixture-root 04_implementation_and_conformance/examples_and_fixtures/fixtures/event_ingress_classification_proof \
  --source-root 04_implementation_and_conformance/examples_and_fixtures/fixtures/event_ingress_classification_proof \
  --output-dir /absolute/path/outside-checkout/check-results
```

`--source-root` names the parent of `sources/`, not `sources/` itself. It is required for the repository split because the semantic-source copies are in the fixture lane. The four fixed names and raw pins are unchanged; the offered proof cannot choose this root.

## Run a portable copy

Create a new external directory, copy the contract root's contents into it, then copy the three checker files, `classification-profile.json`, and the fixture root's `fixtures/` and `sources/` directories into that same directory. Preserve their bytes. This creates the portable layout in which all three roots coincide; no assembly script or repository metadata is needed.

From that directory, run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B run_conformance.py \
  --output-dir /absolute/path/to/check-results
```

The runner writes `case-catalog.json`, generated `cases/` and `reports/`, and the aggregate `conformance-report.json` to the selected output directory. Package/dependency probes run against disposable copies and are recorded in the aggregate report. These outputs are regenerated evidence, not committed files under `checks/`. Without `--output-dir`, the runner uses a temporary directory under the checker and removes it on exit.

The committed fixture lane contains the compact authored expectation index `conformance-catalog.json` and saved `baseline-conformance-report.json`. The runner does not use either saved result as an oracle. `independent-timestamp-review.json` and `independent-review-03/` are historical review evidence with their original version pins. Their broader historical local snapshot seal is not a claim that every member of that snapshot is committed or reproducible from this repository.

## Verify one selected proof

```python
from verify_event_proof import verify

report = verify(
    proof_bytes, envelope_bytes, request_bytes, context_bytes, profile_bytes,
    trusted_pins={
        "contractSha256": selected_contract_raw_sha256,
        "contextSha256": selected_context_raw_sha256,
        "profileSha256": selected_profile_raw_sha256,
    },
    expected_proof_binding={"ref": selected_proof_ref, "digest": selected_proof_jcs_digest},
    use_mode="INITIAL_EVALUATION",
    package_root=selected_contract_directory,
    source_root=selected_fixture_directory,
)
```

For a portable copy, both directory arguments may point to that copy, or both may be omitted. For a repository checkout, explicitly supply the contract and fixture roots. The caller obtains pins and proof selection independently of the proof. Fixture selections are fictional test inputs only.

The CLI requires `--proof`, `--envelope`, `--request`, `--context`, `--profile`, `--trusted-contract-sha256`, `--trusted-context-sha256`, `--trusted-profile-sha256`, `--expected-proof-ref` and `--expected-proof-digest`. Optional flags are `--package-root`, `--source-root`, `--use-mode`, `--dependency-dir` and `--output`. Every verification result is a structured report, including missing-input and dependency failures; argument syntax errors remain ordinary argparse errors.

The pinned JSON report schema must equal the frozen schema in `report_contract.py`. A mismatch returns `DEPENDENCY_UNAVAILABLE` with `REPORT_SCHEMA_MISMATCH` using the supported frozen report format. This also preserves structured diagnostics when optional dependencies cannot load.

Next: recheck the corrected draft at its exact head. Canonical acceptance, CI activation, runtime integration and merge require separate decisions.
