# Offline pre-verdict Event Ingress proof candidate

This bundle is a proposed non-default contract in the **Event Ingress classification and evidence admission** boundary. Scope stays inside that boundary. Read `PROPOSAL.md` for the exact trust root, admission predicates, source qualifications and reuse rules. Success means conditional offline conformance; runtime admission is not established.

## Run the portable suite

Use Python with locally installed `rfc8785==0.1.4` and `jsonschema`. The tested dependency versions and RFC 8785 implementation hashes are in `dependency-manifest.json`. No download happens in these commands.

```sh
python3 -B run_conformance.py --output-dir /absolute/path/to/check-results
```

An optional `--dependency-dir /absolute/path/to/local/site-packages` selects existing dependencies. It is a caller-provided environment location, not a repository dependency. Omit it when the dependencies are installed normally.

For a split installation, use the unchanged runner with explicit roots:

```sh
python3 -B /absolute/path/to/checker/run_conformance.py \
  --package-root /absolute/path/to/contracts/event_ingress_classification_proof \
  --fixture-root /absolute/path/to/fixtures/event_ingress_classification_proof \
  --output-dir /absolute/path/to/check-results
```

The fixture root contains `classification-profile.json` and the saved `fixtures/` subtree. The package root contains `contract.json`, `schemas/`, `source-contracts/`, `sources/` and `source-pins.json`. Checker and helper remain adjacent. No repository files are written by the suite; disposable package copies and results stay in the selected output directory. Without `--output-dir`, a temporary directory under the checker is cleaned on exit.

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
)
```

The caller must obtain pins and proof selection independently of the proof. Fixture manifests provide fictional selections for tests only. The checker never promotes proof self-claims into trusted configuration.

The CLI takes `--proof`, `--envelope`, `--request`, `--context`, `--profile`, `--trusted-contract-sha256`, `--trusted-context-sha256`, `--trusted-profile-sha256`, `--expected-proof-ref` and `--expected-proof-digest`. Optional flags are `--package-root`, `--use-mode`, `--dependency-dir` and `--output`. The default package root is the checker directory for a portable bundle. Every result is a structured report, including missing-input and dependency failures; command-line syntax errors remain ordinary argparse errors.

`integration-map.json` lists the exact recommended destinations. `assemble_packet.py`, `baseline.json`, the task request copy and local check captures remain construction/review history. The assembly script is not part of the installed execution path.

Next: the coordinator should independently inspect this packet, integrate its saved artifacts and run the suite from the agreed split layout before opening the separate draft PR.

Repository integration keeps semantic source copies in the implementation fixture lane. Pass `source_root` (API) or `--source-root` (CLI) as that lane root; the four fixed `sources/` names and raw pins are unchanged. Omit it for the original portable layout. The offered proof cannot select this path.

Repository integration keeps verbatim semantic-source copies in the implementation evidence lane. Pass `source_root` (API) or `--source-root` (CLI) as that lane root. The four fixed `sources/` names and raw pins are unchanged. Omit this parameter for the original portable layout. The offered proof cannot select the path.
