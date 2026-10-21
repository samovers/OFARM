# Pre-verdict Event Ingress classification proof — proposed non-default contract

## Scope and status

The primary trust boundary is **Event Ingress classification and evidence admission**. The intended PR is one independent, non-default owner contract with its schemas, offline checker, pinned sources and conformance inputs. Scope stays inside that boundary. This packet does not modify authorization, credential verification, key custody, runtime admission, act time or transaction snapshot guards.

This is a concrete candidate for the `EVENT_PROOF_INTERFACE` prerequisite identified during the domain-verifier interface review. The packet depends on main commit `4a3d88ea6eff4b3f8a2c521dc621595cbfd1657b`, not PR #47 or any dependent verdict implementation. PR #47 can later consume this contract in its own boundary. This packet does not claim that either PR is complete or that a deployed proof producer exists.

The candidate defines the proof record, classification profile, independent verification context, exact source binding, admissibility predicates, permitted reevaluation and cycle-free declared order. A successful offline result is `CONDITIONAL_CONFORMANCE_PASS`; `runtimeAdmission` is always `NOT_ESTABLISHED`. There is no generic admitted, eligible or accepted Boolean.

## Pinned existing semantics

`source-pins.json` records nine verbatim copies, their original paths, source commit, lengths and SHA-256 values. The original SemanticEventEnvelope and CommitIngressRequest schemas are used without inference or edits. The two original agronomic envelopes and pruning request retain their exact source bytes.

The existing Event Grammar supplies all seven top-level families (§3), the dominant-semantic-consequence selection rule (§4), pack subtype limits (§5), and the independent commit classes (§6). The accepted Event Ingress RFC separates submission from final results and promotion traces. The Platform's staged ingress sequence supplies context for a proof completed during validation, before its dependent verdict. These sources do not establish that every proof must exist before submission.

The checker supports all seven source families and all nine source commit classes. The three-case sample profile covers two actual InterventionEvent examples and one explicitly authored subtype-absent variation. It is illustrative, not an enum restriction. Tests author an additional seven-case profile from the existing grammar and verify all 63 family/class combinations at the interface. Those combinations demonstrate representation and comparison support; they do not approve every combination as a business operation.

## Independent inputs and authority

The consuming verifier receives five byte strings: proof, original envelope, original request, owner context and owner classification profile. Its caller separately supplies exactly three trusted raw SHA-256 pins — contract, context and profile — and one selected proof `{ref, digest}`. The caller must select these through its existing trusted owner/configuration path. They must not be copied from the untrusted proof to make it pass.

This is the explicit conditional trust root. The checker does not authenticate the caller, prove who authored a profile, grant a principal a role, resolve arbitrary URLs or create a new key/signature authority. A fixed `ownerRole` identifies which contract role is being described; the string alone confers no authority. Runtime source selection and admission stay with their existing owners.

The independent context selects the expected proof identifier, profile case, full envelope and request bindings, raw envelope/request hashes, expected commit class, exact target-scope list, production mode and permitted use modes. It contains no verdict result. Context and profile bytes are independently pinned; the proof additionally binds their complete JCS values.

An owner profile contains exact, explicit classification cases. Each case gives the complete dominant-semantic-consequence string, explicit subtype presence/absence and value, one owner-authored primary family, and a clause and digest of the pinned event grammar. The checker selects by the full consequence and subtype posture, never by the envelope's family, commit class, an `admitted` flag, or a keyword. Case identifiers and selection signatures must both be unique. An unknown or ambiguous description fails closed.

This finite profile mechanism preserves the existing grammar. It does not decide new classification law or execute a general natural-language/body-policy engine. A trusted owner must justify a new profile under the existing grammar before selecting its pin. The checker verifies source binding and exact application of that decision; it cannot mechanically prove the owner's semantic judgment from prose.

## Conditional evidence admission

For this non-default contract, a proof can be used as conditional pre-verdict classification evidence only when all these predicates hold:

1. The independently selected contract matches its exact bytes and JCS self-digest. Its complete seven-schema closure, four semantic sources and checker/helper code closure match their pins. Source and owned schemas contain no references requiring resolution.
2. All five inputs are strict UTF-8 JSON, canonicalizable under the pinned RFC 8785 implementation, and valid against the exact selected schemas. Duplicate names, non-JSON numbers, unsafe JCS integers, invalid calendar values and malformed records fail.
3. The independent context and profile raw pins match. The selected proof reference and whole-value JCS digest match. No proof self-digest field is used.
4. Every proof/context contract and input binding matches the complete input value. Both the proof and context also match the original envelope and request **raw byte** SHA-256 values. A changed envelope with the same ID fails. Whitespace-only changes to an envelope/request fail even though their JCS digests are unchanged.
5. The request names the supplied semantic event and matches the independently selected commit class and target-scope list. This contract does not add an anchor-to-target scope authorization rule.
6. Exactly one owner case matches the complete dominant consequence and subtype posture. Its ID matches the selected context. The proof classification matches that case, and the envelope's family matches the owner-authored family. Commit-class equality is checked separately; no family/class coupling table is introduced.
7. Production mode, completion milestone, declared input roles and requested use satisfy the fixed order and reuse rules below. Every required rule is evaluated for a conditional pass.

Consumers must gate use on the exact `CONDITIONAL_CONFORMANCE_PASS` status and retain its qualifications. A diagnostic classification on a failing report is not usable proof. Failure means that this candidate proof is not usable through this interface. It does not decide the final commit result, assertion truth/effect, actor eligibility, body-domain invariants, evidence sufficiency outside this proof, clock trust, review acceptance or operation execution.

## Cycle-free order and availability

The declared dependency order is:

`pinned schemas/sources → contract → selected owner profile → fixed envelope/request → independent owner context → completed classification proof → consumer verification → dependent verdict and later trace/effect/receipt`

`PREEXISTING_PROOF` and `VALIDATION_PHASE_PROOF` are both supported. The context selects one; the proof must match it. The fixed completion milestone is `CLASSIFICATION_COMPLETE_BEFORE_DEPENDENT_VERDICT`. Validation-phase production therefore works without a pre-submission availability promise.

The context has an exact closed input-role list. Both context and proof reject extra late-result fields. Neither schema accepts a dependent verdict, its trace, a final assertion effect, this attempt's receipt or a later ingress result as an earlier proof dependency. Missing proof fails; no dependent consumer can synthesize success from its own verdict.

These are concrete declared-input and ordering rules. Offline comparison does not prove wall-clock execution, detect concealed dependencies inside a producer, or authenticate a claim that a producer ran at a particular stage. Actual production and selection must respect this order under the existing runtime owner. That is an integration obligation, not a missing schema or an implied new clock/signing service.

## Reuse

The only use modes are `INITIAL_EVALUATION` and `EXACT_REEVALUATION`. The fixed reuse rule is `EXACT_ENVELOPE_REQUEST_PROFILE_CONTEXT_AND_PROOF`. An independent context may allow initial use alone or also allow exact reevaluation. Reevaluation must keep the selected immutable proof value, source envelope/request bytes, profile bytes, context bytes, contract and all expected pins unchanged. New context, request, profile or proof selection is a new independently governed selection, not permission obtained from the old proof.

Proof serialization whitespace may change because its immutable identity is a whole-value JCS digest. Source envelope and request serialization may not change because their raw bytes are also pinned. Context/profile raw pins are exact. Repeat verification does not authorize a commit replay, a new attempt or reuse of a final ingress result.

## Implementation and report behavior

The public API accepts byte strings and explicit trusted pins/selector. It has no network, runtime resolver callback or implicit admission mode. Its package root is explicit; the portable bundle defaults to the checker directory. The CLI exposes the same package-root choice. No repository-local dependency path is embedded.

The checker requires RFC 8785 package version `0.1.4`, checks both implementation-file hashes, and exercises an independent ordering/number vector before processing a package. The suite also tests escaping, UTF-16 property ordering, number boundaries and invalid values. JSON Schema validation uses locally installed `jsonschema`; tested versions are recorded in `dependency-manifest.json`. Installation is an external environment step; the runner never downloads code.

The package pins both `verify_event_proof.py` and `report_contract.py`. These checks detect drift in trusted local verifier code; they are not a sandbox or a boot-time code authentication mechanism. The helper freezes the same explicitly authored report schema and checks every return, including dependency and early input failures, without needing optional dependencies. It implements only the finite keywords used by this owned report. The test suite independently validates every returned report with Draft 2020-12 JSON Schema and checks that the frozen and JSON report schemas are equal.

Statuses and CLI exit codes are `CONDITIONAL_CONFORMANCE_PASS`/0, `FAIL`/1, `INPUT_ERROR`/2 and `DEPENDENCY_UNAVAILABLE`/3. Package pin mismatches are input errors; missing files, malformed selected schemas or unavailable/mismatched dependencies are dependency failures. None is a runtime admission claim. Reports are deterministic for identical inputs and the same supported environment.

Resource limits are 2 MiB per JSON document and 64 nesting levels. They are explicit offline checker limits, not additions to the source event grammar. Date-time validation first checks ASCII numeric ranges explicitly (hours 00–23, minutes/seconds 00–59, including offset ranges), then checks actual calendar validity with Python's datetime parser. Leap-second representations are not supported by this candidate runner. It does not determine event chronology, causal order or clock authority. A future requirement to broaden those semantics needs separate review, not a silent fallback.

## Evidence and handoff

`run_conformance.py` constructs hostile inputs from pinned actual envelope bytes, with independent expected results. It distinguishes attacks that retain the original trusted pins from deliberately selected alternate owner profiles/contexts used to test supported representations and invalid owner configurations. `checks/` preserves executable input bytes, expected outcomes and fresh reports. No expectation is derived from verifier output.

The local fixture generator is construction history. Its schemas are explicit field declarations, not inferred from the shape of examples. The installed checker consumes the saved artifacts and never runs that generator. The packet has no import, path or runtime dependency on the domain-verifier branch.

Next: integrate the reviewed packet in the three agreed non-default repository locations, run the portable checks there, and obtain independent owner review before publishing the separate draft PR.
