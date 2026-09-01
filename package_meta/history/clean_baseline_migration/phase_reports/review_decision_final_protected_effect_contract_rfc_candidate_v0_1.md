# OFARM Final ReviewDecision Protected-Effect Contract v0.1

Date: 2026-09-01
Status: Phase A candidate for `samovers/OFARM#15`; non-authoritative, not accepted law, and not a current/default machine contract
Depends on: protected-effect inventory `samovers/OFARM#12` and the renewed Phase A authorization approval for `samovers/OFARM#11` at `baf9eed06c8db4b80d27355d7c05678e966f0eef`
Scope: define the exact domain-result contract for `REVIEW_ACCEPT`, `REVIEW_REJECT_OR_CONTEST`, and `REVIEW_SUPERSEDE`

---

## 1. Decision requested

This candidate asks OFARM stewards to approve, reject, or amend one bounded protected-effect design:

1. each authorized final-review intent may produce exactly one immutable `ReviewDecision` and no other governed effect;
2. the proposed result must preserve the exact target, action, outcome, scopes, rationale, evidence, human decision posture, decision time, and any declared decision-lineage input;
3. the result is classified as one `GovernanceEvent` with commit class `governance decision`;
4. accepted consequences, target mutation, current-state materialization, and promotion remain separate governed effects or downstream processes;
5. a content-addressed contract and immutable validation trace prove the mapping before commit; and
6. any mismatch aborts the protected effect without changing the authorization result.

This document precedes schema, machine-readable contract, conformance, accepted-law, currentness, and runtime work. Approval of this candidate does not create or promote any of them.

---

## 2. Primary trust boundary and PR boundary

### 2.1 Primary trust boundary

The primary trust boundary is **final review-decision domain semantics and commit classification**.

It owns:

- the exact mapping from an authorization-bound final-review intent to one proposed `ReviewDecision`;
- the minimum result carrier needed to preserve that mapping;
- permitted derivations and forbidden widening;
- the primary event family and commit class;
- result postconditions; and
- the validation evidence required before atomic commit.

### 2.2 Intended PR boundary

The Phase A PR adds only this candidate under the historical phase-report lane. It does not change:

- the authorization candidate, action matrix, grant, delegation, sharing, or revocation law;
- who may perform a final review;
- `ReviewDecision v0.1` or any other current/draft schema;
- the active Constitution, accepted RFCs, Event Grammar, or companion policy;
- `REVIEW_REQUEST` result or commit-class semantics;
- accepted-consequence creation or promotion law;
- materialization, pack, output, transport, retention, database, or runtime behavior;
- repository currentness or default selection; or
- OFARM2 implementation.

If review requires a change to the approved authorization intent or action meaning, work stops before editing that boundary and returns to a separate authorization-law prerequisite. An existing large governance document is not precedent for combining these boundaries.

---

## 3. Governing inputs

This candidate is constrained by:

- Constitution RC2.1 sections 10.1, 10.2, 10.8, 10.9, 10.14, 11, and 13;
- the accepted Source Truth Record Closure RFC v0.1;
- the Event Grammar and Commit Matrix v0.1;
- current `ReviewDecision v0.1`, `SemanticEventEnvelope v0.1`, and `AcceptedEventConsequence v0.1`;
- the protected-effect action inventory on `samovers/OFARM#12`; and
- the approved `EI_REVIEW_DECISION_V0_2` and `RP_FINAL_REVIEW_TARGET_ONE` semantics on PR #11 at `baf9eed`.

The authorization candidate determines what target and requested outcome are authorized. This contract does not reevaluate authority. It determines whether the proposed domain result faithfully implements that already bound intent.

---

## 4. Current `ReviewDecision v0.1` inventory

### 4.1 Field capability and gap table

| Current field or behavior | What v0.1 can express | Gap against the approved final-review intent | Phase A disposition |
|---|---|---|---|
| `schemaVersion` | fixes `ofarm.reviewdecision.v0.1` | cannot identify the stronger carrier proposed here | require a future `ofarm.reviewdecision.v0.2` branch |
| `reviewDecisionId` | stable proposed decision ID | no result-content digest or protected-intent equality | retain the ID; bind it exactly to the intent and external result digest |
| `reviewedArtifactFamily` | six broad families | omits `INTERVENTION_PLAN`, `EXECUTION_REPORT`, and `REVIEW_REQUEST`; cannot preserve which of the three authorized assertion kinds was selected; permits `EVIDENCE_SUFFICIENCY_CASE`, which the approved final-review policy does not | retain an exact domain family and add the exact approved target kind in v0.2 |
| `reviewedArtifactRef` | one logical target ref | no immutable target revision or digest | require one exact immutable target binding |
| `reviewAction` | all three final actions plus `REVIEW_REQUEST` | independent enum permits invalid action/outcome pairs and includes the excluded request action | close the three final branches conditionally; exclude `REVIEW_REQUEST` from this contract |
| `decisionOutcomeState` | `ACCEPTED`, `REJECTED`, `CONTESTED`, `SUPERSEDED`, or `REVIEW_REQUESTED` | independent enum does not bind outcome to action or intent | enforce the action/outcome matrix in section 9 |
| `anchorScopes` | one or more scope type/ref pairs | no rule requires exact equality with the reviewed intent | copy the complete ordered scope array exactly from the validated intent |
| `decidedByPartyRef` | one Party ref | cannot prove an accountable natural-person final act, distinguish a represented Party, or bind representation basis | replace with explicit human-principal and conditional representation fields |
| `decidedAt` | a date-time | no trusted source or relation to the human act and commit | derive only from trusted human-finalization evidence |
| `evidenceRefs` | optional logical refs | no exact evidence kind or immutable revision/digest and no equality with intent | require an explicit, possibly empty, array of immutable evidence bindings |
| `resultingAcceptedConsequenceRefs` | optional consequence refs | can imply or hide an additional unbound governed effect | prohibit it for this contract; accepted consequences remain separate effects |
| `supersedesReviewDecisionRef` | optional prior decision ref | no immutable binding, intent source, or lineage validation | replace with an optional exact intent-bound decision binding |
| `notes` | arbitrary optional prose | cannot prove equality with the approved rationale and permits result-local additions | replace with required exact `rationale`; no free result-local notes |
| conditional validation | none | every action/outcome/family combination can be schema-valid | require closed conditional branches and contract validation |
| event/commit classification | absent from the carrier | cannot prove `GovernanceEvent` / `governance decision` | fix both as contract constants and record them in finalization evidence |
| content integrity | no result or contract digest | cannot reconstruct which bytes and semantics were validated | bind intent, result, result-schema, contract, and trace digests |

### 4.2 Example coverage

The repository has ten current `ReviewDecision v0.1` examples:

- seven `REVIEW_ACCEPT` / `ACCEPTED` examples;
- one `REVIEW_SUPERSEDE` / `SUPERSEDED` example targeting `ACCEPTED_EVENT_CONSEQUENCE`; and
- two `REVIEW_REQUEST` / `REVIEW_REQUESTED` examples.

There is no current `REJECTED` or `CONTESTED` example and no hostile example proving that the combined action cannot substitute one for the other. The accepted-consequence supersession example binds only a logical target ref, not an immutable revision or digest.

### 4.3 Carrier decision

A minimal future `ReviewDecision v0.2` carrier is required. A sidecar around v0.1 would leave the authoritative source-truth record unable to state the exact target binding, actor posture, rationale, evidence, and conditional outcome that the sidecar claims to validate. That would create two competing descriptions of the decision.

The future v0.2 carrier is a versioned extension, not an in-place reinterpretation. Existing v0.1 records remain valid v0.1 history and do not silently acquire v0.2 proof strength.

No schema is created or edited in this Phase A PR.

---

## 5. Protected-effect contract identity

The proposed machine-readable contract profile is:

| Property | Closed value |
|---|---|
| Contract ID | `ofarm.protectedeffect.reviewdecision.final.v0.1` |
| Contract version | `0.1` |
| Owning domain family | `REVIEW_DECISION_FINAL` |
| Intent profile | `EI_REVIEW_DECISION_V0_2` |
| Result carrier | future `ofarm.reviewdecision.v0.2` final-decision branch |
| Authorized action set | `REVIEW_ACCEPT`, `REVIEW_REJECT_OR_CONTEST`, `REVIEW_SUPERSEDE` |
| Result cardinality | exactly one immutable `ReviewDecision` |
| Additional governed-effect cardinality | zero |
| Primary event family | `GovernanceEvent` |
| Commit class | `governance decision` |
| Canonicalization | `JCS_RFC8785_SHA256` |

The later materialized contract must carry `contractId`, `contractVersion`, `contractDigest`, owning family, intent/result-schema bindings, the complete mapping table, permitted derivations, forbidden fields/effects, classification, postconditions, validation-trace profile, and digest rules. There is no placeholder ref or digest in this Phase A document.

All three final actions may bind the same contract ref/digest because they are closed branches of one result family. The selected action determines the exact branch; result content cannot select a different branch.

---

## 6. Minimum future `ReviewDecision v0.2` carrier

### 6.1 Required result fields

| Result field | Required meaning |
|---|---|
| `schemaVersion` | exactly `ofarm.reviewdecision.v0.2` |
| `reviewDecisionId` | exact proposed decision ID from the validated intent |
| `reviewedArtifactKind` | one exact authorization target token from section 6.2 |
| `reviewedArtifactFamily` | exact domain carrier family derived only by the closed map in section 6.2 |
| `reviewedArtifactRef` | exact target ref from `PRIMARY_RECORD` |
| `reviewedArtifactRevisionRef` or `reviewedArtifactDigest` | exactly one immutable target binding; never neither or both |
| `reviewAction` | exact selected final action and matching intent constant |
| `decisionOutcomeState` | exact intent-bound value allowed by section 9 |
| `anchorScopes` | complete ordered scope array copied exactly from the intent |
| `decidedByHumanPrincipalRef` | authenticated natural-person principal from trusted finalization evidence |
| `decisionRepresentationPosture` | exactly `SELF` or `REPRESENTED_PARTY`, derived under section 8 |
| `representedPartyRef` | required only for `REPRESENTED_PARTY`; otherwise absent |
| `representationBasisRef` | required only for `REPRESENTED_PARTY`; otherwise absent |
| `representationBasisRevisionRef` or `representationBasisDigest` | exactly one required only for `REPRESENTED_PARTY`; otherwise both absent |
| `decidedAt` | trusted timestamp of the bound human final act |
| `rationale` | non-empty exact rationale from the validated intent; no normalization |
| `evidenceBindings` | required array, possibly empty; every item carries exact evidence kind/ref and exactly one immutable revision ref or digest |
| `supersedesReviewDecisionBinding` | optional only when present in the validated intent; exact prior decision ref plus exactly one immutable revision ref or digest |

The future schema must reject unknown properties. It must not contain a second caller/result-local target, outcome, rationale, evidence, actor, scope, or time selector.

### 6.2 Exact reviewed-artifact tokens

`reviewedArtifactKind` is deliberately closed to the exact `RP_FINAL_REVIEW_TARGET_ONE` target kinds. `reviewedArtifactFamily` preserves the domain carrier family without collapsing the authorized kind:

| Exact `reviewedArtifactKind` | Required `reviewedArtifactFamily` | Required resolved carrier posture |
|---|---|---|
| `STRUCTURE_ASSERTION` | `ASSERTION_RECORD` | `AssertionRecord.assertionType` is `STRUCTURE_ASSERTION` |
| `OPERATION_ASSERTION` | `ASSERTION_RECORD` | `AssertionRecord.assertionType` is `OPERATION_CLAIM_ASSERTION` |
| `COMPLIANCE_ASSERTION` | `ASSERTION_RECORD` | `AssertionRecord.assertionType` is `COMPLIANCE_ASSERTION` |
| `INTERVENTION_PLAN` | `PLANNED_INTERVENTION` | exact `PlannedIntervention` carrier selected by the reviewed schema binding |
| `EXECUTION_REPORT` | `EXECUTION_REPORT` | exact execution-report carrier selected by the reviewed schema binding |
| `REVIEW_REQUEST` | `REVIEW_REQUEST` | exact review-request carrier selected by its separately reviewed result family |
| `DOCUMENT_ASSEMBLY` | `DOCUMENT_ASSEMBLY` | exact document-assembly carrier |
| `DOSSIER_ASSEMBLY` | `DOSSIER_ASSEMBLY` | exact dossier-assembly carrier |
| `SUBMISSION_ASSEMBLY` | `SUBMISSION_ASSEMBLY` | exact submission-assembly carrier |
| `ACCEPTED_EVENT_CONSEQUENCE` | `ACCEPTED_EVENT_CONSEQUENCE` | exact accepted-consequence carrier |

The coarse v0.1 token `ASSERTION_RECORD` is a result family, not an executable target-kind alias. The v0.1-only `EVIDENCE_SUFFICIENCY_CASE` token is not eligible in this profile. A future migration may resolve a v0.1 assertion's exact kind from immutable bytes, but it may not guess or broaden a target.

This contract does not create missing target carriers. Every enabled target kind must have a separately governed, content-addressed resolution profile that proves the family, schema, ref, and immutable revision/digest. In particular, the inventory on #12 identifies no single current `EXECUTION_REPORT` carrier and keeps the `REVIEW_REQUEST` result family separate. Until those owners are closed, authorization may return `ALLOW` for an exact target while the protected-effect domain gate still fails safely; the runtime may not invent a carrier or reinterpret another family.

### 6.3 Immutable-binding rule

Every target, evidence item, representation basis, and optional prior decision uses one tagged immutable binding:

- a revision ref that resolves to exactly one immutable byte sequence; or
- a `sha256:` content digest over the governing canonical bytes.

Supplying both is rejected rather than reconciled. A logical ref without one immutable binding is insufficient. Resolution proof and the resolved byte digest are recorded in the validation trace even when the carrier uses a revision ref.

### 6.4 Representation conditions

For `SELF`:

- the authenticated principal is a natural person;
- `representedPartyRef` and all representation-basis fields are absent; and
- the selected authority subject is that natural person.

For `REPRESENTED_PARTY`:

- the authenticated principal is a natural person;
- `representedPartyRef`, `representationBasisRef`, and exactly one immutable representation-basis binding are present;
- those values equal the trusted authorization/finalization evidence; and
- the selected authority subject is the represented Party.

An organization ref cannot be placed in `decidedByHumanPrincipalRef`. A sponsor, software agent, account owner, or caller-provided Party ref cannot substitute for the direct human actor.

### 6.5 Fields prohibited by this contract

The final-decision branch prohibits:

- `REVIEW_REQUEST` as the result action;
- `REVIEW_REQUESTED` as the result outcome;
- `resultingAcceptedConsequenceRefs` or any equivalent non-empty consequence list;
- free-form `notes` distinct from the bound rationale;
- mutable state fields on the reviewed target;
- caller-selected event family or commit class;
- a result-local default for any required field; and
- any extension property not selected by the reviewed schema and contract.

---

## 7. Complete protected input set

### 7.1 Validated effect-intent inputs

The `EI_REVIEW_DECISION_V0_2` instance supplies exactly these domain-result inputs:

- effect-subject kind fixed to `REVIEW_DECISION` and the proposed decision ID;
- one `PRIMARY_RECORD` target kind/ref and exactly one immutable revision ref or digest;
- the complete ordered `anchorScopes` array;
- review action fixed by the selected action class;
- exact `decisionOutcomeState`;
- exact non-empty rationale;
- the complete ordered evidence-binding array, including an explicit empty array; and
- optional exact prior-review-decision binding for declared lineage.

The optional lineage binding is protected-effect content, not a second authority target. It remains inside the one intent digest and cannot contribute authority or replace `PRIMARY_RECORD`.

The materialized intent schema must expose exact JSON Pointers for these selectors. The later protected-effect contract bytes and AuthorizationPolicyBundle binding pin those pointers and their schema digest. A runtime may not locate fields by name search or mutable registry lookup.

### 7.2 Trusted transaction and finalization inputs

The protected transaction supplies, from already validated evidence:

- authorization request/result/trace refs and digests;
- authorization outcome `ALLOW` for the same action, intent digest, target, and rule;
- selected rule and protected-effect-contract binding;
- authenticated natural-person principal ref and immutable resolution binding;
- represented Party and immutable representation basis when applicable;
- selected path-specific authority subject;
- trusted human-act time;
- trusted transaction snapshot and proposed commit time;
- result-schema ref/version/digest; and
- single-use decision/finalization consumption reservation.

These facts are not caller-authored effect-intent fields. The domain validator consumes their validated evidence; it does not rerun authorization or infer a Party from names.

### 7.3 Non-authoritative inputs

UI labels, display strings, request hints, result defaults, cache state, latest-record queries outside the transaction snapshot, and caller-supplied actor/time/classification fields have no mapping authority. They may be diagnostic only and cannot repair a missing or conflicting protected input.

---

## 8. Exact intent-to-result mapping

### 8.1 Required field mappings

The names in the source column are stable semantic selectors. The later machine-readable binding replaces each selector with one exact JSON Pointer into the reviewed intent or finalization schema; changing a pointer changes the contract digest.

| Mapping ID | Authoritative source | Result destination | Required mapping |
|---|---|---|---|
| `RD_SCHEMA` | selected result-schema binding | `/schemaVersion` | constant `ofarm.reviewdecision.v0.2` |
| `RD_EFFECT_SUBJECT` | intent effect-subject kind | selected result branch | constant `REVIEW_DECISION`; any other kind fails |
| `RD_ID` | intent `proposedDecisionId` | `/reviewDecisionId` | code-point exact copy |
| `RD_TARGET_KIND` | intent `PRIMARY_RECORD.resourceKind` | `/reviewedArtifactKind` | exact token; no kind aliasing |
| `RD_TARGET_FAMILY` | intent target kind plus immutable resolved target bytes | `/reviewedArtifactFamily` | exact closed derivation in section 6.2; resolved carrier posture must match |
| `RD_TARGET_REF` | intent `PRIMARY_RECORD.resourceRef` | `/reviewedArtifactRef` | code-point exact copy |
| `RD_TARGET_REVISION` | intent `PRIMARY_RECORD.resourceRevisionRef` | `/reviewedArtifactRevisionRef` | exact copy when revision posture selected; digest destination absent |
| `RD_TARGET_DIGEST` | intent `PRIMARY_RECORD.resourceDigest` | `/reviewedArtifactDigest` | exact copy when digest posture selected; revision destination absent |
| `RD_SCOPES` | intent `anchorScopes` | `/anchorScopes` | exact complete array; no sorting, union, or narrowing |
| `RD_ACTION` | selected action class and intent `reviewAction` | `/reviewAction` | both sources must be equal; exact copy |
| `RD_OUTCOME` | intent `decisionOutcomeState` | `/decisionOutcomeState` | exact copy after section 9 branch validation |
| `RD_HUMAN` | finalization `authenticatedPrincipalRef` | `/decidedByHumanPrincipalRef` | exact natural-person ref |
| `RD_REPRESENTATION_POSTURE` | trusted principal/representation and selected authority subject | `/decisionRepresentationPosture` | deterministic rule in section 8.2 |
| `RD_REPRESENTED_PARTY` | finalization `representedPartyRef` | `/representedPartyRef` | exact conditional copy or required absence |
| `RD_REPRESENTATION_BASIS` | finalization representation ref and immutable binding | representation-basis result fields | exact conditional copy or required absence |
| `RD_TIME` | finalization trusted human-act time | `/decidedAt` | exact timestamp; not request time or commit time |
| `RD_RATIONALE` | intent `rationale` | `/rationale` | exact Unicode code points; no trim, translation, or summarization |
| `RD_EVIDENCE` | intent `evidenceBindings` | `/evidenceBindings` | exact complete array; no addition, omission, reordering, or ref-only downgrade |
| `RD_PRIOR_DECISION` | optional intent `supersedesReviewDecisionBinding` | `/supersedesReviewDecisionBinding` | exact copy when present; otherwise destination absent |

Every mapping disposition is recorded. A required source that is absent, ambiguous, duplicated, type-invalid, or inconsistent makes the overall contract disposition `FAIL`.

### 8.2 Permitted derived fields

These are the only permitted derivations:

| Derived value | Authoritative source and rule |
|---|---|
| `schemaVersion` | constant from the exact result-schema binding |
| `reviewedArtifactFamily` | exact section 6.2 mapping from intent-bound `reviewedArtifactKind`, confirmed against the immutable resolved target bytes |
| `decisionRepresentationPosture` | `SELF` only when no represented Party exists and the selected authority subject is the authenticated natural person; otherwise `REPRESENTED_PARTY` only when all representation conditions in section 6.4 pass |
| primary event family | contract constant `GovernanceEvent`, recorded in commit/finalization evidence rather than selected by result content |
| commit class | contract constant `governance decision`, recorded in commit/finalization evidence rather than selected by result content |
| `resultDigest` | JCS/SHA-256 over the complete schema-valid proposed `ReviewDecision` |
| resolution digests | digest of the immutable bytes resolved by each revision ref, recorded in the validation trace |
| validation and trace timestamps | trusted validator/transaction clocks; they are evidence times, not `decidedAt` |

Everything else is an exact copy or required absence. No default action, outcome, actor, target, scope, rationale, evidence, lineage, or decision time is permitted. No text normalization, set sorting, family coercion, latest-revision lookup, lineage search, or generated consequence ID is permitted.

---

## 9. Exact action/outcome closure

| Selected authorization action | Required result `reviewAction` | Allowed intent/result `decisionOutcomeState` | Every other pairing |
|---|---|---|---|
| `REVIEW_ACCEPT` | `REVIEW_ACCEPT` | exactly `ACCEPTED` | `FAIL` |
| `REVIEW_REJECT_OR_CONTEST` | `REVIEW_REJECT_OR_CONTEST` | exactly the one intent-bound value `REJECTED` or `CONTESTED` | `FAIL` |
| `REVIEW_SUPERSEDE` | `REVIEW_SUPERSEDE` | exactly `SUPERSEDED` | `FAIL` |

The combined reject-or-contest action is not split. The human-bound intent selects one closed outcome before authorization and result construction. The result cannot infer, default, or switch that value.

`REVIEW_REQUEST` / `REVIEW_REQUESTED` is not a fourth branch. It requires its own result and commit-class closure.

---

## 10. Supersession and consequence separation

### 10.1 Exact supersession target

For `REVIEW_SUPERSEDE`, the exact `PRIMARY_RECORD` target is the artifact whose in-force interpretation is being superseded. The validator proves the target kind/ref/immutable binding and its applicable pre-effect posture under the transaction snapshot. It does not search for a newer target or substitute a related decision.

Supersession never rewrites or deletes the target. The new `ReviewDecision` becomes an immutable governance basis that downstream truth and currentness logic must honor.

### 10.2 Optional prior-decision lineage

`supersedesReviewDecisionBinding` records decision-to-decision lineage only when the validated intent contains the exact immutable binding. It does not replace the reviewed target and does not create authority. The referenced prior decision remains immutable.

The validator must also receive a passing disposition from any applicable accepted lineage rule. If no accepted rule can establish the claimed relationship, the field is not guessed into meaning and validation fails. Absence in the intent requires absence in the result.

### 10.3 Accepted consequences are separate effects

This contract creates no `AcceptedEventConsequence`, no consequence ID, and no non-empty consequence-reference list. A later accepted consequence may refer back to the committed ReviewDecision through its own separately authorized intent, result contract, validation trace, and atomic commit.

An authorization `ALLOW` for one prospective `REVIEW_DECISION` is never authority to create a second consequence effect. A runtime cannot treat `REVIEW_ACCEPT` as an implicit multi-effect grant.

---

## 11. Event family and commit class

The primary event family is exactly `GovernanceEvent` because the dominant semantic consequence is a formal final-review act. The commit class is exactly `governance decision`.

These classifications are contract constants. They are recorded in the governed-effect receipt and validation trace. If a `SemanticEventEnvelope` represents the same act, it must carry `primaryEventFamily: GovernanceEvent`, the exact decision ID as its governed subject, the exact scopes, and the same trusted decision-time semantics. It cannot create another primary family for the same act.

The validation trace, authorization evidence, and governed-effect receipt are separately classified as `EvidenceEvent` / `evidence record`. Evidence classification of those records never changes the ReviewDecision's domain classification.

Linked accepted consequences, invalidation evidence, and later materialization updates retain their own governing event/effect classifications. They are not secondary outputs of this contract.

---

## 12. Postconditions

### 12.1 Common postconditions

The proposed transaction state must satisfy all of these before commit:

| Postcondition ID | Required proposed-state condition |
|---|---|
| `PC_ONE_RESULT` | exactly one new `ReviewDecision` ID resolves to exactly one schema-valid byte sequence and result digest |
| `PC_VALIDATED_BYTES` | committed decision bytes equal the bytes validated by this contract |
| `PC_INPUTS_IMMUTABLE` | reviewed target and every referenced evidence, representation, and prior-decision record remain byte-identical and unmodified |
| `PC_CLASSIFICATION` | the decision is visible only with primary family `GovernanceEvent` and commit class `governance decision` |
| `PC_NO_EXTRA_EFFECT` | no `AcceptedEventConsequence`, target rewrite, current-state materialization, separately governed output-promotion record, or unrelated governed effect is inserted or changed by this effect |
| `PC_ATOMIC_EVIDENCE` | complete passing validation trace, governed-effect receipt, authorization/finalization evidence, and single-use consumption commit atomically with the decision |
| `PC_UNIQUE_ID` | a duplicate decision ID with different bytes is rejected |

### 12.2 Action-specific postconditions

| Postcondition ID | Branch | Required semantic postcondition |
|---|---|---|
| `PC_ACCEPT` | `REVIEW_ACCEPT` / `ACCEPTED` | the committed decision records acceptance of the exact target; it does not itself create an accepted consequence or materialized fact, and downstream promotion still applies every governing gate |
| `PC_REJECT` | `REVIEW_REJECT_OR_CONTEST` / `REJECTED` | the committed decision records rejection of the exact target while preserving the target in history; no deletion or contrary accepted status is created |
| `PC_CONTEST` | `REVIEW_REJECT_OR_CONTEST` / `CONTESTED` | the committed decision records an explicit contested posture; the target is not silently treated as accepted, rejected, or resolved |
| `PC_SUPERSEDE` | `REVIEW_SUPERSEDE` / `SUPERSEDED` | the committed decision records supersession of the exact target; prior history remains immutable, and dependent current-state or output eligibility must no longer claim freshness without applying the new decision basis |

Materialization invalidation or recomputation may be required downstream, but this protected effect does not write a materialization. The ReviewDecision is the new canonical history input; a separate governed process applies it to current-state views.

---

## 13. Content addressing and digest projections

### 13.1 Contract digest

The future machine-readable contract uses this deterministic construction:

1. reject duplicate JSON member names and non-I-JSON input;
2. construct the complete contract document without `contractDigest`;
3. compute RFC 8785 JCS over that document;
4. compute SHA-256 and prefix the lowercase hexadecimal digest with `sha256:`;
5. insert the value as the one top-level `/contractDigest` member; and
6. on verification, remove exactly that top-level member and repeat the calculation.

No nested member and no other top-level member is excluded. Missing, malformed, duplicated, mutable, or mismatched contract identity makes the action-rule binding non-executable.

The resolved contract closure includes every semantic element in sections 5 through 14: action branches, result-schema binding, mapping IDs/selectors, derivations, forbidden fields/effects, classification, postconditions, trace requirements, and digest rules. Diagnostic wording that cannot change validation may remain outside the closure only when the materialized contract identifies it as non-semantic.

### 13.2 Intent, result, and schema digests

- `effectIntentDigest` is the already approved JCS/SHA-256 digest of the complete validated effect intent.
- `resultDigest` is JCS/SHA-256 over the complete schema-valid proposed ReviewDecision with no excluded member; the candidate result has no self-digest field.
- `resultSchemaDigest` is the exact immutable digest selected by the reviewed schema binding.
- every revision-ref resolution records the digest of the immutable resolved bytes in the validation trace.

A logical ref or version without its governing digest is insufficient for a v0.2 proof claim.

### 13.3 Validation-trace digest

The trace uses the same provisional/final construction as the contract, excluding exactly the one top-level `/validationTraceDigest` member. No name-based recursive exclusion is permitted.

---

## 14. Immutable protected-effect validation trace

The trace is a tagged `protected-effect-contract validation` profile inside the planned `AuthorizationFinalizationEvidence v0.2` package. It is not a new domain-event family or an independent truth store.

It records at least:

- trace ID, version, trusted validation time, transaction-snapshot ref/digest, and `validationTraceDigest`;
- authorization request/result/trace refs and digests, selected action, rule ID/digest, and `ALLOW` disposition;
- human-finalization evidence ref/digest and single-use reservation ref;
- effect-intent schema ref/version/digest, effect-intent ref/digest, and canonicalization;
- proposed ReviewDecision schema ref/version/digest, result ref/ID/digest, and canonicalization;
- protected-effect contract ID/version/ref/digest and canonicalization;
- fixed `GovernanceEvent` and `governance decision` classifications;
- exactly one disposition for every applicable mapping ID in section 8.1;
- exactly one disposition for every applicable `PC_*` postcondition ID in section 12;
- immutable resolution refs/digests for the target, evidence, representation basis, and optional prior decision;
- overall disposition `PASS` or `FAIL`; and
- stable non-authorization failure codes and safe diagnostic pointers.

Each mapping or postcondition disposition is exactly `PASS`, `FAIL`, or `NOT_APPLICABLE`. A required item cannot be `NOT_APPLICABLE`. Overall disposition is `PASS` only when every required item passes and every optional item is either passing or legitimately not applicable.

The trace records source and destination JSON Pointers plus compared digests. It need not duplicate sensitive values. A missing mapping, postcondition, schema binding, or resolution proof is a failure, not an implied pass.

A passing trace commits atomically with the protected effect. A failing trace may be retained as separately governed failure evidence, but it cannot claim a committed ReviewDecision or rewrite the authorization result.

---

## 15. Validation and atomic commit protocol

One protected transaction must:

1. select this exact contract ref/digest from the already selected action rule;
2. verify the action-rule, intent-schema, result-schema, contract, and relevant evidence bindings;
3. revalidate the authorization/finalization decision, target binding, trusted actor/representation facts, and transaction snapshot at the effect boundary;
4. construct the proposed ReviewDecision only from section 8 mappings and permitted derivations;
5. validate the complete result against the exact future v0.2 schema;
6. compute the result digest and every immutable-resolution digest;
7. evaluate every field mapping, action/outcome constraint, classification, forbidden-effect rule, and proposed-state postcondition;
8. construct the immutable validation trace and governed-effect receipt;
9. require every applicable EnforcementChain gate to pass without treating authorization `ALLOW` as another gate's result; and
10. atomically commit the ReviewDecision, passing trace, receipt, authorization/finalization evidence, and single-use consumption.

If any comparison, proof, gate, or proposed postcondition fails:

- no ReviewDecision or other protected effect commits;
- no single-use consumption commits;
- the authorization result remains its original authority-gate result and is not rewritten to `DENY` or another authorization outcome; and
- any retry must still use the same unexpired intent/rule/contract bindings and a newly valid transaction snapshot.

No effect becomes externally visible before its complete passing evidence commits.

---

## 16. Production-reachable hostile cases

The later conformance suite must enter through the real result builder, contract validator, and transaction path. Unit-only helpers are insufficient.

| Case | Required disposition |
|---|---|
| `REVIEW_ACCEPT` proposes `REJECTED`, `CONTESTED`, or `SUPERSEDED` | mapping/branch `FAIL`; transaction aborts |
| `REVIEW_SUPERSEDE` proposes any outcome except `SUPERSEDED` | mapping/branch `FAIL`; transaction aborts |
| `REVIEW_REJECT_OR_CONTEST` intent binds `REJECTED` but result says `CONTESTED`, or vice versa | `RD_OUTCOME` fails; transaction aborts without changing the intent or authorization result |
| result action differs from the selected action or intent constant | `RD_ACTION` fails; transaction aborts |
| exact `ACCEPTED_EVENT_CONSEQUENCE` target is replaced by an assertion or another consequence | target-family/ref/binding mapping fails; no decision commits |
| target logical ref matches but immutable revision or digest changes | target-binding mapping fails; no decision commits |
| runtime accepts `ASSERTION_RECORD` as a caller/intent alias for one of the three exact assertion target kinds | `RD_TARGET_KIND` fails; no local kind aliasing |
| result drops, adds, reorders, or substitutes one anchor scope | `RD_SCOPES` fails |
| organization ref is substituted for the authenticated human | `RD_HUMAN` fails |
| represented Party or representation basis is omitted, changed, or supplied under `SELF` | representation mapping fails |
| trusted human acted at time A but result uses request time, commit time, or caller time B | `RD_TIME` fails |
| rationale differs by whitespace, case, translation, summarization, or content | `RD_RATIONALE` fails |
| evidence ref is retained but its revision/digest is changed, omitted, or reordered | `RD_EVIDENCE` fails |
| result adds a prior-decision ref absent from intent or substitutes a newer decision | `RD_PRIOR_DECISION` fails; no latest-record inference |
| proposed result contains `resultingAcceptedConsequenceRefs` or transaction creates a consequence | forbidden-field/effect postcondition fails; both effects abort |
| transaction mutates or deletes the reviewed target or prior ReviewDecision | immutable-history postcondition fails |
| transaction directly inserts or marks a CurrentStateMaterialization as accepted/current | no-current-state-effect postcondition fails |
| ReviewDecision is classified as `EvidenceEvent`, `StructureEvent`, or another family | classification fails; authorization evidence remains separately `EvidenceEvent` |
| commit class is not `governance decision` | classification fails |
| result validates only against v0.1 or the result-schema digest differs | result-schema binding fails |
| contract ID/version matches but contract bytes or digest differ | contract binding fails before result validation |
| one required mapping or postcondition is missing from the trace | overall trace cannot be `PASS`; no commit |
| duplicate decision ID already resolves to different bytes | uniqueness/immutability postcondition fails |
| relevant target or supersession state changes after validation but before commit | transaction serialization/revalidation fails; no effect |
| protected-effect failure is reported by rewriting authorization `ALLOW` to `DENY` | conformance failure; domain failure remains distinct from authorization outcome |

---

## 17. AuthorizationPolicyBundle registration

This PR does not create or edit `AuthorizationPolicyBundle v0.2`.

After steward approval and later materialization of real contract and schema bytes, the separate authorization-policy-bundle PR must:

1. add the exact contract ID/version/content ref/digest and owning family to its immutable binding manifest;
2. bind the same contract to the `REVIEW_ACCEPT`, `REVIEW_REJECT_OR_CONTEST`, and `REVIEW_SUPERSEDE` rules;
3. bind the exact `ReviewDecision v0.2` result-schema ref/version/digest and intent-to-result selector pointers;
4. exclude `REVIEW_REQUEST` from this binding;
5. include the resolved contract binding in each action's complete `ruleDigest` closure; and
6. require exact digest equality at evaluation and effect consumption.

The policy bundle cannot point at this prose file as an executable contract. It must point at reviewed immutable machine-readable bytes produced in a later bounded PR. Changing any semantic mapping, postcondition, selector, or classification changes the contract digest and therefore the affected action-rule digests.

---

## 18. Migration and currentness

`ReviewDecision v0.1` remains current/default until a separately governed promotion says otherwise. Existing records and examples remain v0.1 evidence and history.

There is no automatic claim that a v0.1 record satisfies this v0.2 contract. Migration requires enough immutable source evidence to establish every required v0.2 field and mapping. Missing target revision, actor representation, rationale, evidence revision, decision-time basis, or exact outcome intent cannot be guessed from current prose or latest-record state.

Draft schema or contract presence changes no currentness. A later accepted/promoted version must preserve links to v0.1 history rather than rewriting it.

---

## 19. Invariants

The accepted design and conformance suite must preserve these invariants:

1. one authorized final-review intent creates at most one immutable ReviewDecision and no additional governed effect;
2. the exact intent target kind/ref/immutable binding equals the result target, and the derived domain family matches the resolved carrier;
3. action and outcome satisfy the closed matrix and exact intent equality;
4. `REJECTED` and `CONTESTED` are never inferred from each other;
5. scope, rationale, and evidence are complete exact copies, not normalized or supplemented result data;
6. the deciding human and any represented Party/basis remain distinct and traceable;
7. trusted human-act time, validation time, and commit time are not silently substituted;
8. supersession preserves prior history and never mutates the target in place;
9. a ReviewDecision cannot smuggle an accepted consequence, materialization, or promotion effect;
10. the ReviewDecision is one `GovernanceEvent` / `governance decision`; its validation evidence is separately `EvidenceEvent` / `evidence record`;
11. contract, intent, result, schema, and validation-trace digests bind the exact bytes and semantic closure;
12. every required mapping and postcondition has one explicit disposition;
13. only a complete `PASS` trace can accompany a committed effect;
14. protected-effect failure never rewrites the authorization result;
15. validation and all required evidence commit atomically with the decision; and
16. v0.1 records never silently claim v0.2 proof strength.

---

## 20. Traceability to issue #15

| Acceptance criterion | Proposed disposition |
|---|---|
| inventory current `ReviewDecision v0.1` capabilities and gaps | section 4 |
| decide whether minimal v0.2 carrier is required | sections 4.3 and 6 |
| exact action/result constraints | section 9 |
| bind ID, target, scopes, human/representation, rationale, evidence, time, and supersession inputs | sections 6 through 10 |
| enumerate permitted derivations and sources | section 8.2 |
| forbid target/action/outcome/rationale/evidence substitution and hidden effects | sections 6.5, 10, 12, 15, and 16 |
| fix event family and commit class | sections 5 and 11 |
| content-address contract identity and deterministic digest projection | sections 5 and 13 |
| immutable mapping/postcondition validation trace with required digests | section 14 |
| validate before atomic commit; do not rewrite authorization result | section 15 |
| production-reachable hostile cases | section 16 |
| later AuthorizationPolicyBundle binding without creating it here | section 17 |

---

## 21. Steward approval card

Before machine-readable contract or schema work begins, stewards should explicitly decide every item:

| Decision | Proposed answer | Approval required |
|---|---|---|
| Is a future `ReviewDecision v0.2` carrier required rather than a v0.1 sidecar? | yes | yes |
| Does this contract cover exactly the three final review actions and exclude `REVIEW_REQUEST`? | yes | yes |
| Does each intent create exactly one ReviewDecision and zero other governed effects? | yes | yes |
| Are the ten target tokens exactly the approved `RP_FINAL_REVIEW_TARGET_ONE` closure? | yes | yes |
| Must target, evidence, representation basis, and prior decision use exact immutable bindings? | yes | yes |
| Are action/outcome pairs fixed exactly as in section 9? | yes | yes |
| Must reject versus contest be selected inside the validated intent? | yes | yes |
| Are accountable human and represented Party/basis separate conditional fields? | yes | yes |
| Is `decidedAt` the trusted human-act time rather than caller/request/commit time? | yes | yes |
| Are rationale, scopes, and evidence exact copies with no normalization or defaults? | yes | yes |
| Is optional prior-decision lineage allowed only when exactly intent-bound and separately valid? | yes | yes |
| Are non-empty accepted-consequence links prohibited for this single-effect contract? | yes | yes |
| Are primary family `GovernanceEvent` and commit class `governance decision` fixed constants? | yes | yes |
| Do target history and prior decisions remain immutable under every branch? | yes | yes |
| Does this effect avoid direct current-state materialization or promotion? | yes | yes |
| Is the content-addressed semantic closure and one-member digest projection accepted? | yes | yes |
| Must every required mapping and postcondition have an explicit trace disposition? | yes | yes |
| Must a complete passing trace and finalization evidence commit atomically with the decision? | yes | yes |
| Does a protected-effect failure leave the authorization result unchanged? | yes | yes |
| Does later bundle registration remain a separate authorization-policy PR? | yes | yes |
| Does current/default promotion remain a separate final step? | yes | yes |

Any amendment that changes authorization meaning, current Event Grammar, accepted-consequence creation, current-state mutation, runtime transactions, or another effect family must be split before editing that boundary.

---

## 22. Staged delivery and completion criteria

The required sequence is:

1. **Phase A candidate:** this document only; no authority or currentness effect.
2. **Semantic approval:** stewards approve or amend section 21; no schema or executable contract exists yet.
3. **Draft domain-contract materialization:** a separate bounded domain PR creates the machine-readable protected-effect contract, exact selectors, and future non-default `ReviewDecision v0.2` schema branch with real refs/digests.
4. **Finalization-evidence draft:** a separate authorization-evidence PR materializes the tagged validation-trace and governed-effect-receipt profiles required here without changing the domain mapping.
5. **Binding review:** a separate authorization-policy-bundle PR binds the reviewed bytes to the three action rules and updates their complete rule digests.
6. **Hostile conformance:** production-reachable fixtures exercise section 16 through the real validator and atomic transaction path.
7. **Accepted law and contract review:** governed review accepts the exact RFC/contract/schema bytes; semantic change returns to step 2.
8. **Explicit promotion:** a separate human-governed PR changes current/default indexes only after all prerequisites pass.
9. **Byte-identical downstream extraction:** OFARM2 may consume only promoted canonical bytes and their verified digests.

Phase A is complete when:

- every issue #15 acceptance criterion has the proposed disposition in section 20;
- the v0.1 inventory and v0.2 carrier decision are reviewed;
- exact mappings, derivations, forbidden effects, classification, and postconditions are accepted or amended;
- content-addressing and validation-trace evidence are mechanically closed enough to materialize without semantic invention;
- hostile cases cover action/outcome, target, actor, time, rationale, evidence, lineage, consequence, mutation, classification, and digest substitution;
- registration into the later AuthorizationPolicyBundle is explicit but not performed here;
- the primary trust boundary remains final ReviewDecision domain semantics and commit classification; and
- the PR changes only this non-authoritative candidate file.

What is next: steward review of this one-file Phase A candidate before any `ReviewDecision v0.2`, executable contract, validation-trace, conformance, or promotion edit.
