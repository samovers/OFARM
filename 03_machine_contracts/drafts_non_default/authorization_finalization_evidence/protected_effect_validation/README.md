# Protected-effect validation-trace envelope

This proposed non-default component belongs to the existing
AuthorizationFinalizationEvidence family. Its primary trust boundary is shared
validation-evidence integrity. It supplies a common trace envelope and a finite
local integrity checker; it does not establish that domain validation occurred.

The component is stacked above the proposed operation-claim and data-read intent
component in PR #42. Prior transaction, assertion and intent component bytes and
their manifests remain unchanged. Nothing here selects a current/default schema
or creates a new event family. An admitted trace retains the existing
EvidenceEvent / evidence-record classification.

## Ownership and limits

The shared envelope binds immutable identity, authorization, intent, result,
protected-effect contract and selected action/body-schema selectors to an
externally schema-bound payload. PASS
and FAIL are carried dispositions. A shape-valid PASS is not proof that the
domain mappings, prerequisites or postconditions were evaluated successfully.
Those meanings remain with the protected-effect contract and payload owners.

The proposed shared payload interface requires these four fixed top-level
members inside the actual externally hashed payload, for both PASS and FAIL:

| Payload member | Must equal the verified trace member |
| --- | --- |
| `proposedResultDigest` | `proposedResult.resultDigest` |
| `effectIntentDigest` | `effectIntent.digest` |
| `protectedEffectContractDigest` | `protectedEffectContractBinding.contractDigest` |
| `selectedActionBodySchemaBinding` | Complete `selectedActionBodySchemaBinding` object |

Digest strings and all four body-binding fields must match exactly. The selected
payload schema must explicitly declare these properties and mark them required;
actual missing or
malformed values fail. Verification never fills them from trace claims. These
names are this envelope's proposed convention under PR23's separate envelope
delegation, not field names literally prescribed by PR23. No trace-root field,
configurable pointer or PR40 binding change is introduced.

This comparison binds the payload's declared subject. A producer can still
relabel all four fields and recompute hashes without performing domain
evaluation. Real payload adoption, AR/PC truth and intent-to-result identity/body
mappings remain owner responsibilities.

The required `selectedActionBodySchemaBinding` is separate from PR40's unchanged
four-field contract binding. It must match both the separately supplied owner
expectation and the body binding selected by the resolved contract for the same
action. Recomputing valid hashes cannot excuse disagreement. The F4 correction
also validates the bound result's actual `assertionBody` under that resolved
selected schema, while retaining validation of the complete result. Matching
bindings alone do not establish body conformance. The fictional single-body
contract uses `bodySchemaBinding`; real action-specific selection remains an
owner dependency. This schema-conformance check does not establish domain truth.

Real domain-owned payload schemas and the complete protected-effect contract
remain unavailable. Explicitly fictional schemas and records used by the checker
only demonstrate finite integrity controls; they cannot replace missing
production artifacts. No network lookup, wildcard schema or successful fallback
may stand in for an unavailable binding.

For each selected schema, the resolved target must declare `type: object` and
`additionalProperties: false`. These checks do not prohibit names admitted by
`patternProperties` or establish recursive restrictions on nested objects. Those
restrictions, including objects in arrays, remain with the selected schema's
owner. Validation still applies all constraints present in that schema. Resolving every schema
reference against pinned local documents is a separate dependency check.

PR40's existing trace reference and trace/disposition wrapper can be checked
against their actual preserved schema. Its complete admitted-result binding
requires the real AssertionRecord protected-effect contract identity and bytes,
which remain unavailable. Matching field names or a fictional contract do not
establish that complete binding.

Open dependencies retain their existing owners: temporal admission, prospective
global identity, source history, twin applicability, all three assertion branches,
domain payload/mapping rules, full authorization-policy binding and real
clock/guard/status producers. OFARM2 #392/#396 remains parked. This component
does not establish complete release closure, runtime permission or production
readiness.

## Exact bytes and digest order

The component manifest pins the envelope schema and design, the three accepted
source revisions selected for this component, and seven unchanged prior
artifacts. A schema digest hashes its exact UTF-8 file bytes. A trace or payload
digest hashes RFC 8785 canonical JSON of the complete value, excluding nothing.
The implementation uses pinned `rfc8785==0.1.4`; ordinary sorted JSON is not a
substitute.

Freeze schema bytes and finalize the intent/result/contract bindings, then
populate and hash the subject-bound payload, then finalize the trace. The contract
binds the payload schema, never a future concrete payload digest.
The trace's ref/digest stays outside its value, so no self-digest or future
receipt reference is needed. Later transaction evidence can bind the finalized
trace under the existing transaction protocol. Earlier traces are not rewritten.

A new trace ID does not permit replacing a FAIL with PASS for the same attempt.
Local hashes and ID collision controls protect individual record integrity;
they do not establish authoritative attempt history or retry eligibility.
PR26 distinguishes retryable current-state failures from terminal invalidity of
fixed caller content. A lawful later attempt needs the owner's eligibility
decision and fresh validation/authorization evidence. Those guarantees remain
UNAVAILABLE here.

For the current trace resolved from an authoritative attempt's
`protectedEffectValidation.trace`, the transaction consumer must compare the
complete `trace.authorizationResult` with `attempt.authorizationBundle.result`,
and `trace.decisionBundleDigest` with
`attempt.authorizationBundle.decisionBundleDigest`. The result record digest and
decision-bundle digest have different meanings. A prior admitted-result trace
stays provenance for its owning historical attempt and cannot replace the current
attempt's fresh trace. This checker supplies no authoritative attempt resolution
or enforcement.

PR26/issue #25 retains complete-set verification, decision single-use, immutable
failure history, eligible fresh-attempt retry and original-receipt replay. An
independent `(authorizationResult, proposedResult)` trace quota is not adopted:
it would neither stop an unconsumed FAIL-to-PASS replacement nor prohibit
decision reuse with a different result. Repeated verification or replay of the
original completed evidence is not another consumption.

The proposed wire choices include one result per trace, exact full selectors,
an external schema-bound payload exposing `/overallDisposition` and the four
fixed subject members, and an external content-addressed trace reference. [DESIGN.md](DESIGN.md) explains the source
mapping, exact construction, non-schema checks and owner dependencies.

## Local verification

The independent runner is registered once in the existing repository suite.
It uses real pinned local schemas and explicitly fictional foreign records.
It compares carried bindings to separate fictional expected-context inputs,
checks the selected body binding against the resolved fictional contract,
validates the actual bound body under that schema as well as the complete result,
checks the payload's schema/digest/copied verdict and four declared subject
bindings, and verifies the complete trace hash.
The harness does not produce trusted runtime context. Copying a changed trace
into its expectation is not independent validation. DESIGN lists every concrete
comparison and the domain and transaction relationships it cannot establish.
Missing real foreign bytes remain unavailable, including for a FAIL trace.

The F4 correction applies the already resolved selected-body validator to
`result.value.assertionBody`. Its focused counterexample makes the trace, expected
context and fictional contract all select `structureAssertionBody`, with honestly
recomputed hashes, while the actual operation-claim body does not conform. The
complete result remains valid under its result schema. The committed regression
case `selected_body_agreement_rejects_nonconforming_actual_result_body` requires
rejection at `resultBody` with the exact root `additionalProperties` witness.

From the repository root with the existing validation dependencies:

```sh
python3 -m pip install 'jsonschema>=4.22,<5' 'rfc8785==0.1.4'
python3 04_implementation_and_conformance/conformance_runners/ofarm_protected_effect_validation_trace_envelope_v0_1.py
python3 package_meta/tools/run_repository_validation_suite.py
```

The committed fixture contains 307 cases: 24 accepted controls and 283 expected
rejections, including 124 exact schema witnesses. The component manifest records
all rejection-layer totals. All schema rejections require the intended target and exact
error witness. The 265 controls inherited from `9185519` retain their purposes,
order, expectations and 103 schema witnesses while payload fields and affected
digests are mechanically rebased. The identity-only case is named
`new_identity_is_a_distinct_record_only`; it grants no admission permission.
The repository suite retains its thirteen existing checks, including this
runner. Public verification refers to the committed fixture and reproduction
commands above.

F1 controls retain a payload for one valid result while honestly finalizing a
different valid result/context/trace/reference, plus isolated intent, contract
and complete body-binding mismatches. Missing/malformed fields have exact schema
witnesses; matching subject bindings exercise both PASS and FAIL. These controls
test declared-subject agreement, not whether evaluation occurred. The committed
result-subject regressions are named
`payload_proposedResultDigest_mismatch_pass` and
`payload_proposedResultDigest_mismatch_fail`. Their matching re-finalized
companions deliberately retain the limit that relabelling does not prove truth.
Nine `payload-interface` helper controls edit declaration metadata after real
pinned resolution; they do not claim a changed schema passed its original hash.

The preserved controls cover selected-body omission and shape, mismatched independent
expectations, honestly re-finalized contract drift, missing schema fragments,
schema-reference cycles and unsupported dynamic references. Oversized integers
and deeply nested JSON now return the existing JSON rejection result rather than
uncaught interpreter exceptions. A missing-document helper control deliberately
removes the document after preflight; it does not claim that entry-point missing
dependencies reach that helper.

No database, clock, transaction or runtime test result is claimed by these
fictional controls.

## Review status

The external re-review at `453bfe5` reported zero blockers, four follow-ups
(B1, F1, F2, F4) and two preferences (P3, P4). The original selected-body binding
blocker and P1/P2 are resolved; F3's remaining hygiene guards are now P3. All
previously missing sections are supplied. The reviews use the author account;
they do not establish an independent-review gate or formal approval.

F4's later internal independent review cleared the correction published at
`e07a333`. F2/P4's wording and reproducible-evidence correction is complete at
`9185519`. Those checks are distinct from the earlier author-account GitHub
feedback and create no formal GitHub approval.

F1 adds the fixed declared payload-subject convention and its comparisons; real
domain evaluation and production adoption remain unavailable. B1's exact
current-attempt consumer handoff and historical-provenance distinction are
specified, while transaction enforcement, failure terminality and retry
eligibility remain a separate PR26/issue #25 prerequisite. No independent pair
quota or recursive schema policy is adopted. Optional P3 hygiene coverage
remains open.

Next: materialize the separate real domain payload/context and transaction-owner
enforcement prerequisites before governed binding or runtime use; retain the
remaining domain-mapping and optional P3 obligations.
