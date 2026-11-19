# Complete typed AssertionRecord submission draft

[OFARM #46](https://github.com/samovers/OFARM/issues/46) owns AssertionRecord domain meaning and validation integrity. This draft contains the three-branch protected-effect contract and the offline evaluator for original intent, result and owner-evidence bytes. Its status is `INCOMPLETE`. A reviewer can reproduce the draft references and individual findings. Policy admission and the protected write have separate owners.

## Reproduce the references

Run this command at the root of an exact checkout of PR #47 with Python and `rfc8785==0.1.4`. It uses the local checkout and does not require the external evidence packages.

```sh
runner=04_implementation_and_conformance/conformance_runners/complete_typed_assertion
python3 -B "$runner/ofarm_assertion_record_domain.py" references
```

The command verifies every checkout file in the worker manifest. It checks the registry, duty graph, all three action bindings and all references in the 13 selected schemas offline. The output includes repository paths, schema identifiers and raw hashes, body pointers, payload and trace bindings, hashes for the callable and its package, and the expected file hashes from two separate source owners. Evaluating a claim verifies those external bytes as well. Pin the full Git commit alongside the output when reproducing this review.

| Draft item | Reproduced value |
| --- | --- |
| Contract ID and version | `ofarm.protectedeffect.assertionrecord.complete-typed.submit.v0.1`, version `0.1` |
| Contract reference | `candidate:assertion-domain:complete-typed-submit:v0.1` |
| Whole-contract digest | `sha256:ab41daa1426672b38bf98e6b4358f133b4a97639e26b8847e35116a70ef48e24` |
| Contract file SHA-256 | `3cf908fdc73a2048bdcf015277c2269e1b5a16035dd779d15ee5097c3b2327c3` |
| Operation intent | `ofarm.operationassertioneffectintent.typed.v0.1` · raw SHA-256 `bacf7bc27ae430e79fc5c5c084a7fe1bef529ef8d6a5487c384ee5e69b485c71` |
| Result | `ofarm.assertionrecord.typed.v0.1` · raw SHA-256 `f3362cbbb135584f8d7c96dcf01c27c60e727b48b1b1f8700f9f57ec0bbe9f05` |
| Operation body | Result schema at `#/$defs/operationClaimBody` · language `ofarm.complete-typed-claims.v0.1` · same containing-file SHA-256 |
| Validation payload schema | `ofarm.assertionRecordDomainValidationPayload.v0.4` · raw SHA-256 `674c84e2c8fe56da2c10e95dd25957d323f911f5771ff86bf04ba5381e278557` |
| Validation trace envelope | `ofarm.protectedEffectValidationTrace.v0.1` · raw SHA-256 `a5150119555a2faaa0531ae96e650dcefd5cb491fa30fd8ffe337c873f6cdae3` |
| Worker manifest SHA-256 | `49c57b9c593510400afa393c9a9a75dd73a15b5ec152ad3ffa973d9f5c6e1d78` |

The contract digest is SHA-256 over the RFC 8785 encoding of the full contract object with only its top-level `contractDigest` removed. The registry digest covers `{"definitions": registry["definitions"]}` under the owner's projection. The original construction still bound an earlier C17 definition. Recomputing the registry from the shipped rows gives `sha256:f9d22cfc6a2af4b08e48fef60da175672ca57fbe2cbfbbf74534a6d6b0d19117`. The verifier checks this dependency even when a supplied contract is internally consistent with its own digest.

## Evaluate original bytes

Use Python 3.12 for the public function or CLI. The evaluator runs in the pinned isolated interpreter. Supply the following directories under one external root, obtained from the respective owners. Directory locations may differ between installations. The worker verifies the interpreter bytes, standard library, Python libraries and each selected original package against its exact file inventory before importing owner code.

| Directory under the external root | Expected selection |
| --- | --- |
| `runtime` | Selected Darwin ARM64 CPython 3.12.14 installation containing `bin/python3.12` and `lib/python3.12` |
| `libraries` | The 146 selected library files. The selection includes RFC 8785 0.1.4 and jsonschema 4.26.0. |
| `owners/act`, `owners/event`, `owners/authorization`, `owners/occupancy` | Exact reviewed owner subsets of 29, 15, 14 and 12 files respectively |
| `owners/state` | 259 selected protected-state files from [OFARM #51 at 538d040](https://github.com/samovers/OFARM/pull/51/commits/538d04075881b885ed370d14326acfab7aaf429e) |
| `condition-property-source` and `si-c17` | The six pinned files for condition-property resolution and five pinned files for SI evidence interpretation, supplied by their separate owners. The `externalSourceFilePins` output identifies each file. |

All selected event, state, authorization and occupancy file contents occur in the respective pinned Git trees. The pinned assertion-act Git tree supplies 26 of its 29 files. Its owner packet also supplies `DELIVERY_MANIFEST.json`, `sources/approved-proposal.md` and `sources/interface-review.md`. The isolated evaluator checks all three against the act inventory. The reference reproduction command works from the OFARM checkout alone. [Assertion-act source revision](https://github.com/samovers/OFARM/tree/3a51d046ebf823e0faa4252e9c37ccfa182036f3)

The worker retains the domain owner's construction and the five external verification interfaces. The checkout reuses previously tracked files by digest. A fresh temporary directory holds the verified worker files for each call. Its manifest preserves original member hashes and records the checkout locations. The draft changes the contract and performs its reference checks before evaluating claim semantics. The underlying construction snapshot has manifest SHA-256 `496f54a246e5704a2914d7d9ca3cd6a2f96805c3ef06dcee21285e4ea0e00a4d`. The worker's dependency manifests list the required relative names, sizes and SHA-256 values. A missing or changed package prevents evaluation.

```sh
fixtures=04_implementation_and_conformance/examples_and_fixtures/fixtures/complete_typed_assertion
python3 -B "$runner/ofarm_assertion_record_domain.py" verify \
  --intent "$fixtures/intent.json" --result "$fixtures/result.json" \
  --action ASSERT_OPERATION_CLAIM --external "$OFARM_TYPED_EXTERNAL" \
  --owner-inputs "$fixtures/owner-inputs.json" \
  --evaluation-selection-sha256 e61a6a30757d4e7962ba940eb5cf2715ef042c5972d2e630c6d1715a250fec7c
```

The Python entry point is `verify_domain(intent_bytes, result_bytes, *, package, owner_inputs)` in `ofarm_assertion_record_domain.py`. The package contains `externalRoot`, `selectedAction` and, when a selection is supplied, its independently pinned `evaluationSelectionRawSha256`. Python callers supply bytes for original evidence. The JSON CLI represents each byte string as a single `originalBytesBase64` member. Both entry points use the same evaluator. Exit code 1 indicates a completed failure report and 2 indicates input or dependency failure. A successful reference reproduction exits with 0.

The saved example is fictional. Its typed intent and pending result pass their respective schemas. Its original Event Ingress proof passes its owner check. The event omits the selected operation payload, and the independently pinned selection omits records cited by the claim, including its first evidence binding. The domain report therefore records `AR_EVENT_ASSOCIATION` and `PC_INPUTS_IMMUTABLE` as failed. Of the 49 duties, 19 pass, 22 remain unevaluated and six are inapplicable. The verifier returns no public validation payload or trace for this claim.

The comparisons under `PC_ACTION_TYPE` and `PC_PENDING_REVIEW` identify the original document and JSON pointer for each value digest. The operation action selects effect kind `OPERATION_ASSERTION`, result subtype `OPERATION_CLAIM_ASSERTION` and commit class `operation claim` with token `OPERATION_CLAIM`. The verifier checks the action row against both typed schemas and the submission rules. It can detect an invalid time window, operation posture, assertion timestamp or payload binding even when an unrelated owner record is missing.

To reproduce a passing submission, the domain owner still needs a single matching set of assertion-act, authorization, event (when cited), and protected-state originals. The evidence-use owner must identify the rule that admits each required use. The transaction owner must independently identify the same attempt and its protected reads and proposed write. The domain verifier still needs to finish tracing those inputs and comparing the full protected set. The focused tests run through the sealed worker when `OFARM_TYPED_EXTERNAL` is set.

```sh
python3 -B "$runner/test_domain.py" -v
```

## Handoff to the policy-package owner

Both the v0.2 operation intent and v0.2 AssertionRecord schema reject the three members `claimLanguageRevision`, `proposition` and `performedByBinding` on the saved typed claim. Both typed schemas require them. Changing just the version labels preserves the rejection. The older v0.2 fixture passes its own schema. The operation subtype and pending state agree across versions. The duty graph retains `PC_ONE_ASSERTION`, `PC_VALIDATED_BYTES` and `PC_PENDING_REVIEW` as separate checks.

OFARM2 approved version 2 of the `SUBMIT_OPERATION_CLAIM` binding for development. Its RFC pins the typed draft for review. Admission still requires the completed domain contract and matching policy-package approval for the assertion and read rules. [OFARM2 version 2 decision](https://github.com/samovers/OFARM2/blob/a087e3352e7588e56cabf6cf622cb449ce04f93e/docs/rfcs/OFARM2_Operation_Claim_Submission_Command_Binding_RFC_v0_2.md) · [Canonical policy package](https://github.com/samovers/OFARM/issues/21)
