# Canonical successful-path evidence interface

This is a non-default, opt-in `AuthorizationDecisionEvidence v0.2` profile for comparing one successful selected path with exact authorization-owner output. It does not implement an authorization evaluator or a complete v0.2 decision package.

Primary trust boundary: **canonical authorization decision evidence integrity**. The delivery stays inside this boundary. PR11 source law, principal resolution, grants/delegations, accepted CP3 inputs, canonical path selection, runtime protection, key custody and CI remain unchanged.

## Inputs and result

The API takes five byte inputs: evidence bytes, source-profile bytes, verification-context bytes, a dictionary of original source-record bytes, and a dictionary of original schema bytes. The caller must separately supply `expected_context_sha256`, obtained from its trusted selection boundary. Never compute that expected digest from the submitted context in a production consumer. Fictional test runners do so only to construct an explicit test scenario.

```python
from verify_success_path import verify
report = verify(
    evidence_bytes, profile_bytes, context_bytes,
    source_bytes, schema_bytes,
    expected_context_sha256=independently_selected_context_digest,
    contract_root=installed_contract_directory,
    source_root=installed_fixture_directory,
)
```

The context pins the selected contract, exact source profile, original raw and canonical-value digests, complete source set, action, and source-role assignments. It contains no expected Party or admitted Boolean. The source profile selects complete source schemas and fixed projection locations. Source profile selection is a trusted owner integration step; an untrusted caller cannot nominate or weaken it.

The result and full trace retain the selected path and all its Party/basis/source/visibility references. Every original record is validated under its selected full schema and hash before projection. Non-source references use a revision or digest; grant/delegation/sharing source identities require the one-record digest and reject different bytes under an identical source ID within the supplied set. A content-only complete intent may omit an embedded ID only when independently digest-bound. No source is fetched from a network or an implicit resolver.

This profile uses closed `resultProjection`, `traceProjection` and `path` schemas in `types.schema.json`. These are fields of the authorization owner's complete original records. An exact producer profile can point to the root or an embedded projection object. The full original records are retained and hashed, including fields outside the projection. A v0.1 acting-Party record, consumer report, or bare ALLOW flag cannot supply the required source graph. Fictional source schemas under the test lane demonstrate the protocol; they are not new production Party, grant, principal-resolution, policy, snapshot or CP3 contracts.

The rule record is the independently selected complete per-action semantic-closure representation; `ruleDigest` is its JCS digest. The policy digest similarly covers the selected complete packaged policy representation. Proving that those representations are complete and applicable remains with the policy/authorization owner. The verifier checks exact original-byte selection and output equality; it does not package rules or derive their semantics.

The decision-bundle digest follows PR11 §18.8 over the **complete** request/result/trace. Only the two top-level `decisionBundleDigest` members are removed. A nested member with that name remains included. Final records never accept the pre-digest sentinel. No later effect or receipt is required as an input.

`PASS` means only `SELECTED_OWNER_OUTPUT_INTEGRITY_COMPARED`. Every report separately marks eligibility, trusted principal resolution, candidate-set completeness, canonical-selection correctness, runtime source origin, source currentness/migration, CP3 admission, and runtime protection/effect permission `NOT_ESTABLISHED`. A passing fixture is not an admitted authorization decision.

## CLI and split installation

```text
python -B verify_success_path.py \
  --wire original-byte-wire.json \
  --context-sha256 INDEPENDENTLY_SELECTED_RAW_CONTEXT_SHA256 \
  --contract-root /path/to/installed/canonical_success_path \
  --source-root /path/to/installed/fixtures/canonical_success_path
```

The wire stores original bytes as strict base64, with a closed schema. Exit codes are 0 for the conditional integrity PASS, 1 for failed comparisons, and 2 for invalid input or package setup. Reports use the owned closed report schema. Package schemas and metadata are resolved relative to `contract_root`; verbatim `sources/` files are resolved only relative to the explicitly selected `source_root` (defaulting to `contract_root` for the original local packet). Verifier code hashes are checked next to the actually imported verifier. This supports the specified separate contract and conformance-runner lanes.

Dependencies are Python 3.11 or later, `jsonschema==4.26.0`, and `rfc8785==0.1.4`. The RFC8785 implementation bytes are checked. No dependency install, default promotion or CI activation is performed by this delivery.

`run_cases.py` is the installed opt-in fixture runner. It requires explicit package, fixture, and report paths. The construction scripts are retained as delivery evidence, not installed as runtime code. Do not run refresh/build scripts on the sealed packet.

## Scope limits

The selected path's tuple preserves PR11's path-type order and immutable source/delegation identifiers. Encoding checks do not prove that a lower eligible candidate is absent. Other paths remain in the complete trace and their source bindings remain retained; no aggregation lattice or eligibility rule is executed.

The four authority-subject bases keep their source roles separate. Self, representation, direct agent and explicit delegation paths must link to the selected Party through the actual supplied source records. Role assignments, CP3 instance/profile/sponsor/snapshot links, CP3 decision links, and delegation/source-authority links are compared. The current CP3 field names remain sufficient; this package adds no CP3 envelope field. Sponsors do not become authority subjects by being present.

Next: independently review this sealed interface and its exact installation map before a consumer selects it. Any need to change source eligibility, principal resolution, CP3 contracts, or another trust boundary requires separate scope review.
