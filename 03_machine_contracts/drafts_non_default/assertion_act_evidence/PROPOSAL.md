# Assertion-act evidence v0.1 — proposed non-default owner contract

## Boundary and claim

The primary trust boundary is **trusted assertion-act identity, time and submitted-content evidence**. The intended PR is a separate non-default act-source contract, schemas, offline checker and fictional conformance inputs. Scope stays inside that boundary. Authorization policy and principal resolution, actual clock trust, signing/key custody, runtime deployment, transaction protection, domain interpretation, default promotion, CI activation and merge remain outside it.

This candidate closes the act record and verification-context shapes for conditional comparison. It covers both existing `TRUSTED_ONLINE_SUBMISSION` and `VERIFIED_OFFLINE_SUBMISSION` postures. It does **not** close the unidentified authorization-selected canonical-path source interface. A positive result is `CONDITIONAL_CONFORMANCE_PASS`, with `runtimeAdmission: NOT_ESTABLISHED` and an explicit list of unestablished claims. There is no generic admitted/success Boolean and no producer callback that can declare the checks passed.

`INTERFACE_ASSESSMENT.md` identifies the exact reused contracts and the remaining foreign gap. Main commit `4a3d88ea6eff4b3f8a2c521dc621595cbfd1657b` supplies the active event and measurement schemas and original example bytes. The existing non-default AssertionRecord v0.2 and three intent schemas are copied verbatim from the reviewed input component at `389a8f6b6bb2f43435c35f32df769e723d736856`. They retain their non-default status. The exact PR23 owner text is pinned at `6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f`; PR11's later owner text is pinned at `d1178fe07d57accedde5748672602db38346b3e6`, with the earlier operation-component source retained separately.

No runtime import or mutable path points to PR #47. The saved source-schema closure is self-contained and can be consumed independently. The candidate uses the existing intent shapes; it does not rewrite them or infer new body shapes from examples.

## What is trusted independently

The caller supplies raw byte strings for an act source record, submitted-content manifest, already-rendered pre-act content, complete intent, verification context, source-policy record and intent profile, plus the selected schema bundle. It also supplies an exact map from selected source IDs to original event/measurement bytes.

Independent caller configuration supplies four exact raw SHA-256 pins: contract, context, policy and intent profile. A separate selected-act object gives the exact immutable binding plus the resolved raw byte hash and whole-value JCS digest. The checker never fills these from the act record's claims.

The verification context is selected independently of the act/intent result. It fixes the expected Party and path-specific basis, source timestamp, posture, source kind, policy, source inputs, submitted/rendered bytes and complete intent digest. Its `INDEPENDENT_FICTIONAL_EXPECTATIONS` label states the supported offline capability. It is not an authorization decision or a proof that its source is trusted in production.

The four basis names come from PR11 §6.2: natural-person self, authorized representation, directly granted agent Party and explicit agent delegation to a represented Party. The checker compares the complete selected basis value and immutable basis-binding list; it does not select a sufficient path or test grant/delegation eligibility. The accountable Party is not replaced with the alleged performer, sponsor, approver or a caller mirror.

The selected authorization-path evidence schema remains unidentified in the searched source set. The active AuthorizationDecisionTrace v0.1 exposes `actingPartyRef`, which is not a substitute for PR11's path-specific `authoritySubjectPartyRef`. Domain mapping reports are downstream consumer artifacts and do not supply that missing authority source. Real integration needs the authorization owner to identify or separately materialize its exact output contract. Until then, the expected Party/basis selection is an explicit fictional assumption. Every report preserves this gap, including passing reports.

## Owned records

The eight owned schemas are explicit field declarations. The wire-interface schema states only required access locations; the independently pinned complete carrier schema closes all payload fields:

| Record | Purpose |
| --- | --- |
| Intent profile | Selects an exact carrier schema/version, claim-language revision and extra schema-byte closure under the fixed act metadata layout. |
| Wire interface | Checks the minimum top-level locations used by this act verifier without imposing a legacy body vocabulary. |
| Submitted content | Binds the complete already-rendered pre-act intent content by raw byte hash and JCS digest, plus every selected original source input by role, immutable selector, raw byte hash and resolved JCS digest. |
| Source policy | Selects one existing posture/source kind and the fixed canonical-time, exact-content and independent-Party comparison rules. It does not prove clock trust or producer eligibility. |
| Act evidence | Records the pre-existing accountable Party/basis, exact canonical `assertedAt`, source policy and submitted-content binding. Online and offline source kinds are distinct. It has no complete-intent, verification-context, verdict, effect or receipt dependency slot. |
| Verification context | Supplies the independent expected values and selected immutable byte mappings, including the complete intent selection. It is constructed after those inputs exist; the act record does not bind it. |
| Report | Returns structured conditional results or failures, with runtime admission and the foreign source gaps explicit. |
| Contract | Pins the schema/source/code closure, exact rule set, hash rules and dependency order. |

The existing source `immutableBinding` and canonical timestamp definitions are reused through a pinned local schema registry. All fourteen base owned/source schemas, plus every extra schema selected by the intent profile, must resolve within that registry. No remote/latest reference retrieval is allowed. The existing intent dependency declarations are checked against the exact AssertionRecord and operation-intent byte pins they name.


## Versioned intent profiles and the complete typed carrier

The legacy v0.2 carrier cannot validate the domain owner's new `ofarm.complete-typed-claims.v0.1` bodies. That mismatch was identified before sealing. The verifier therefore has no schema-version-to-old-carrier switch: a concrete `ofarm.assertionActIntentProfile.v0.1` record selects the exact intent schema ID/version, claim-language revision and a complete extra schema bundle by raw byte hashes. Its raw pin is independent caller configuration, and both the submitted-content manifest and verification context bind its whole value. Changing the profile requires new selected content/act bindings; it cannot weaken validation under an old act.

The profile fixes `ofarm.assertion-act-top-level.v0.1` and the same three excluded act metadata fields. It cannot choose extra excluded fields, a renderer, executable predicates or arbitrary extraction pointers. The small wire-interface schema checks locations needed by this verifier; the selected full carrier schema owns all typed body structure. Complete nested propositions and all other admitted fields remain part of the exact content comparison. A future carrier that moves these metadata locations needs a reviewed wire-interface revision.

The API takes profile bytes and an exact schema-ID-to-byte map. The profile enumerates every extra schema and hash. Missing, extra, duplicate, changed, unresolved or conflicting schemas fail; a profile cannot replace base schema bytes under an existing ID. Resolution uses only the combined pinned local registry. There is no network fallback or arbitrary owner-code callback.

Saved profiles cover the existing v0.2 carriers and exact snapshots of all three domain-owned typed carrier schemas, their result definitions, proposition schema and owned value types. `typed-interface-source-pins.json` records these task-local snapshots and their unsealed, unapproved source status. The eighteen typed cases retain full propositions extracted from the owner's existing examples. They establish byte/schema compatibility only, not domain approval or complete end-to-end validity. These optional schema snapshots are supplied fixture data, not act-owned domain law. The schema named result supplies shared static type definitions; no later result record is an earlier act input. The fixture generator does not edit the owner's source files. Final consumer integration must select the exact independently reviewed final profile/schema bytes; no mutable path to the owner's construction directory is used by the installed checker.

## Content and immutable bytes

The pre-act rendered content contains every complete-intent field except exactly three top-level metadata fields: `assertedAt`, `assertionActPosture` and `assertionActEvidenceBinding`. This keeps all subject, sole authority resource/scope, branch-specific body, supporting evidence, subject-time, lineage, governance/context and other admitted intent fields in the original content. The checker compares the entire projection, not a hand-picked body subset.

The submitted-content manifest binds the raw rendered bytes and their whole JCS value. The act record and independent context both bind the manifest's exact raw bytes and JCS value. The checker additionally compares the exact JSON value fragments for every rendered top-level field with the complete intent. Appending act metadata cannot re-render the claim body, subject, resources or evidence fields. Whitespace-only or escaping changes inside a rendered field are therefore detectable even when the parsed value is unchanged.

The original SemanticEventEnvelope and MeasurementEvidence inputs remain separate complete byte strings. The manifest and independent context select their exact role, original immutable binding, resolved whole-value JCS digest (`valueDigest`) and raw byte SHA-256 (`bytesSha256`). The binding preserves either `ref` plus `digest` or `ref` plus `revisionRef`, exactly as submitted. The caller must provide exactly that set, with no missing, duplicate or extra records. Source records must pass their actual pinned schemas and match both digests and identity. The associated event binding must identify a supplied event; supplied measurements must appear in the submitted evidence bindings. Additional selected event bytes may be retained as evidence context; only the explicit associated-event field declares an association.

For both source kinds, the independently pinned context contains the complete selector-to-byte mapping in `selectedSourceInputs`, which must equal the manifest's `sourceInputs`. Every entry requires `valueDigest` and `bytesSha256`, including digest selectors. Both are checked against the complete original record, and a digest selector must additionally equal the computed JCS digest. A revision selector is never silently replaced by its resolved digest. Changing or omitting the selected mapping fails; revision spelling does not establish immutable resolution. The external trusted source owner supplies that resolution before selection. The checker verifies the exact mapping rather than performing a runtime lookup.

This preserves complete event metadata, measurement method/source context, phenomenon time, qualifiers and original result forms. It does not rebuild a scalar measurement or rewrite a censored result. Existing source `evidenceStatus`, source notes or event family claims do not become trusted admission flags. Other immutable references already present in the rendered intent are copied exactly; this act checker does not resolve their foreign semantic/authority proofs. That limitation is distinct from checking all bytes in the explicitly selected source-input set.

The fixtures retain two actual envelopes and two actual measurement records byte-for-byte. They combine them with fictional act/intent cases to exercise preservation. These combinations demonstrate act/content integrity, not domain compatibility, event-time validity or measurement sufficiency for the fictional claims. The domain consumer retains those checks, including its separate event/time cells.

## Online and offline comparisons

The selected Party, basis, time, policy and content must all match the source record and independent context. `assertedAt` must exactly equal the complete intent's canonical string. It is not derived from subject time, measurement/record time, authorization check time, human approval time or commit time.

For online submission, the act source kind is `TRUSTED_RUNTIME_SUBMISSION_OBSERVATION`. It represents the trusted runtime's observation supplied before complete-intent hashing. The intent must omit `assertionActEvidenceBinding`. The source-record schema and comparison are concrete; real runtime identity, authenticated observation and clock trust are not established by fictional inputs.

For offline submission, the source kind is `IMMUTABLE_OFFLINE_ASSERTION_ACT`. The intent must contain exactly the independently selected `assertionActEvidenceBinding`. A digest selector is checked against the complete act value. A revision selector is accepted only as part of the explicit independently pinned revision-to-byte mapping, with exact raw hash and JCS digest; the checker does not resolve a mutable alias or infer that a revision is immutable from its spelling. Changing a selected revision fails. Actual immutable resolution remains an external source-owner obligation.

Source-policy bytes and binding must match the independent selection. Its rules are concrete format/comparison rules for this non-default capability. It is not a real time-trust admission policy, and the checker does not establish that a clock or observation was trustworthy. The report names that limit rather than replacing it with an admitted bit.

## Cycle-free declared order

The required order is:

`source policy and fixed content → online observation/offline act → top-level intent act metadata and offline selector → complete intent digest → independent verification context and Party expectation → conditional act comparison → later domain verdict/effect/receipt`

The act record binds the earlier content, policy and pre-existing Party basis. It does not bind the later verification context, authorization result or final intent. The verification context can therefore contain a complete-intent selector without creating a back edge. Offline intent hashing includes the already finalized act binding.

Closed schemas reject self-binding, complete-intent digest, context binding, domain verdict/trace, final assertion effect, receipt and arbitrary dependency fields in the act. The rendered content cannot contain act metadata. The checker rejects known identity aliases among act, content, policy, context and proposed assertion identities, and refuses immutable bindings in rendered content, every selected source (including secondary event context) or Party basis that alias those identities. Only the two exact typed original-source roles are supported; a caller cannot relabel a later verdict as a third input role. There is no alias graph traversal or arbitrary resolver callback.

These checks establish the declared byte/input order under explicit source assumptions. They do not prove a producer's actual execution chronology or inspect concealed dependencies inside an unresolved foreign authority basis. Those authority-source semantics remain unestablished; the packet does not claim a universal producer-cycle proof.

Repeated verification of unchanged selected inputs yields the same result. It grants no new invocation, approval, commit replay or assertion effect. A different proposed assertion ID or content requires a separately selected act/content binding; an old act does not authorize changed bytes.

## Runtime, error and dependency behavior

`verify_assertion_act.verify` accepts bytes, selected source bytes, independent pins/act selection and an explicit package root. The CLI exposes the same inputs. The default portable package root is the checker directory; the installed split layout needs no code modification. Helper names are specific to this component so it can coexist with other proof checkers in one process.

RFC 8785 package version `0.1.4`, both implementation-file hashes and an independent canonicalization vector are checked before use. The contract pins checker/helper source bytes, all schemas and both selected owner texts. These code checks detect drift in trusted local code; they are not a sandbox or authenticated boot mechanism.

Every return, including missing dependency, malformed JSON, package failure and early rejection, is checked against the frozen owned report schema without optional dependencies. The suite independently validates reports with Draft 2020-12 JSON Schema. Selected malformed schemas and unresolved references produce structured failures; no network retrieval occurs. Identical inputs produce deterministic reports.

The statuses/CLI exit codes are `CONDITIONAL_CONFORMANCE_PASS`/0, `FAIL`/1, `INPUT_ERROR`/2 and `DEPENDENCY_UNAVAILABLE`/3. Consumers must gate on the exact conditional-pass status and retain the qualifications. Failed reports have no result projection. CLI argument syntax errors remain ordinary argparse diagnostics.

Each JSON input is limited to 2 MiB and 64 nesting levels. Duplicate object names, invalid UTF-8, non-JSON numbers and unsafe canonical JSON values fail. Source date-time numeric components use explicit ASCII ranges before calendar parsing. Act timestamps additionally follow PR23's exact uppercase UTC spelling, seconds and nonzero-ending 1–9 digit fractions. No input is normalized, rounded or repaired. The existing profile excludes leap seconds. Calendar syntax checks do not establish clock trust or temporal domain meaning.

## Delivery and remaining work

`run_act_conformance.py` owns independently authored expectations and constructs hostile cases without reading saved results. Positive coverage includes both postures, all four Party-basis forms, all three legacy and complete-typed intent branches, exact nanosecond strings and an explicitly selected revision mapping. Negatives cover changed rendered fields and source bytes, Party/basis/time/policy/selectors, posture confusion, self/later references, malformed input, dependency/schema failures and numeric timestamp ranges. Generated scratch bytes and detailed reports stay local; the integration map lists compact evidence and reproducible inputs/runner.

The assembly script is construction history, not an installed production component. This packet claims conditional act/content conformance only. Its source search and report keep the authorization-selected path interface gap visible, while actual actor identity, time trust and admission remain separate runtime claims.

Next: independently review and replay the non-default act packet, obtain the exact authorization-selected path source interface from its owner before a real integration claim, and publish only the separately authorized draft Delivery/PR.

## Review repair 01

This separately versioned repair addresses the independent review finding that valid source revision selectors were narrowed to digest-only entries. It changes only assertion-act source fidelity and its verifying schemas, fixtures, checker and documentation. The sealed original packet is retained unchanged. Positive fixtures now cover digest, revision and mixed selectors across both postures, all Party bases and all six legacy/typed profiles. No authorization source, resolver implementation, domain semantics or runtime admission is added. Next: independently replay this revision and integrate only its updated exact map.
