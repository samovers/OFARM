# Conditional assertion-act verifier

Primary trust boundary: **trusted assertion-act identity, time and submitted-content evidence**. Scope stays inside it. Read `PROPOSAL.md` and `INTERFACE_ASSESSMENT.md` before treating a result as usable evidence. The authorization-selected canonical-path source contract is still unidentified; no runtime admission or clock/actor trust is established.

## Run the saved cases

Use locally installed `rfc8785==0.1.4` and `jsonschema` with Python. The runner never downloads dependencies.

```sh
python3 -B run_act_conformance.py --output-dir /absolute/path/to/results
```

For a split installation, pass separate roots:

```sh
python3 -B /absolute/path/to/checker/run_act_conformance.py \
  --package-root /absolute/path/to/contracts/assertion_act_evidence \
  --fixture-root /absolute/path/to/fixtures/assertion_act_evidence \
  --output-dir /absolute/path/to/results
```

An optional `--dependency-dir /absolute/path/to/existing/site-packages` selects an existing local dependency directory. No repository-local path is baked into the installed code. Without `--output-dir`, temporary results are created below the checker and cleaned on exit. All disposable test packages stay in the selected output directory.

The package root contains contract/schema/source closure and source pins. The fixture root contains the `fixtures/` subtree and transformation ledger. The checker, `act_common.py` and `act_report_contract.py` stay adjacent. The assembly script is not part of the installed execution path.

## Callable interface

```python
from verify_assertion_act import verify

report = verify(
    act_bytes, content_manifest_bytes, rendered_content_bytes,
    complete_intent_bytes, context_bytes, policy_bytes,
    source_inputs={selected_source_ref: original_source_bytes},
    trusted_pins={
        "contractSha256": independently_selected_contract_hash,
        "contextSha256": independently_selected_context_hash,
        "policySha256": independently_selected_policy_hash,
        "intentProfileSha256": independently_selected_profile_hash,
    },
    expected_act_selection={
        "binding": selected_immutable_act_binding,
        "bytesSha256": selected_act_raw_hash,
        "valueDigest": selected_act_jcs_digest,
    },
    intent_profile_bytes=independently_selected_intent_profile_bytes,
    schema_bundle={selected_extra_schema_id: exact_schema_bytes},
    package_root=selected_contract_directory,
)
```

Every source entry in `content.sourceInputs` and `context.selectedSourceInputs` has this shape:

```json
{
  "role": "MEASUREMENT_EVIDENCE",
  "binding": {"ref": "measurement:example", "revisionRef": "revision:example:r1"},
  "bytesSha256": "<raw SHA256 hex>",
  "valueDigest": "sha256:<whole-object JCS SHA256 hex>"
}
```

`SEMANTIC_EVENT_ENVELOPE` uses the same shape. A binding may instead contain `ref` and `digest`; the digest must equal `valueDigest` and the computed source digest. Preserve the submitted selector exactly in the rendered/final intent, manifest and context. The independent context pin selects the exact resolution mapping; no revision spelling or offered source claim supplies it. Both hashes are required for either selector branch. The original source bytes remain separate and unchanged.

All expected pins and selection must come from independent caller configuration. The saved fixture manifest gives fictional test selections only. A passing report retains the unresolved authorization-source interface and other unestablished claims.

The single-proof CLI requires `--act`, `--content`, `--rendered`, `--intent`, `--context`, `--policy`, `--selection`, `--source-inputs` `--intent-profile`, `--schema-bundle` and the four `--trusted-…-sha256` arguments. `--selection` names a JSON file containing the exact selection object above. `--source-inputs` names a JSON map from selected source IDs to file paths, resolved relative to that map's directory. `--schema-bundle` names a JSON map from exact schema IDs to file paths, relative to that map. The profile independently pins those bytes. Legacy profiles use an empty map; complete-typed profiles supply their declared closure. Optional arguments are `--package-root`, `--dependency-dir` and `--output`. The default package root is the checker directory for a portable bundle.

`integration-map.json` lists exact byte-preserving destinations. `checks/conformance-report.json` is captured validation evidence, never an expectation oracle. `assemble_packet.py` and generated scratch input/report copies remain construction history.

Next: independently review and replay the saved packet, retaining its explicit source gap and conditional result limits before publication of the separate draft.
