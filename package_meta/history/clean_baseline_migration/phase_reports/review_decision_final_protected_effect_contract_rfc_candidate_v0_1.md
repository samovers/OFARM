# OFARM Final ReviewDecision Protected-Effect Contract v0.1

Date: 2026-09-01<br>
Status: Phase A candidate for `samovers/OFARM#15`; non-authoritative, not accepted law, and not a current/default machine contract<br>
Depends on: protected-effect inventory `samovers/OFARM#12`, governed-transaction protocol `samovers/OFARM#19`, and the approved authorization candidate on issues #16 and #18 / PR #11 at `03a21f669ee04f96d444e14f00ae7212cab04803`<br>
Blocking prerequisites: PR #11 semantic approval is satisfied; `samovers/OFARM#19` must close before machine materialization, hostile conformance, or runtime implementation claims the shared atomic transaction gate<br>
Scope: define the ReviewDecision-specific mapping from an authorized final-review intent to one immutable ReviewDecision record

---

## 1. Decision requested

Stewards are asked to approve, reject, or amend these bounded decisions:

1. this contract validates exactly one `ReviewDecision` record for `REVIEW_ACCEPT`, `REVIEW_REJECT_OR_CONTEST`, or `REVIEW_SUPERSEDE`;
2. it does not itself authorize or validate an `AcceptedEventConsequence`, current-state materialization, target mutation, or other companion effect;
3. only `REVIEW_ACCEPT` / `ACCEPTED` may carry companion accepted-consequence bindings, and only when a separately reviewed atomic composition binds their exact governing authority basis, contract-defined derivation, validation, and result digests before commit;
4. the governed final-review act has primary event family `GovernanceEvent`, while the `ReviewDecision` record has commit class `governance decision`;
5. the result preserves the exact authorized target, action, outcome, scopes, accountable deciding Party, authenticated human actor, finalization evidence, decision time, rationale, evidence, and optional lineage;
6. `anchorScopes` comes only from the complete rule-selected common authorization-envelope scope binding in the validated intent; no profile-local or result-only scope can add authority;
7. optional prior-decision lineage is a governed ReviewDecision-domain field inside the validated, digest-bound intent and cannot affect authorization eligibility under this candidate;
8. `WIDENING`: the future result-family enum grows from six v0.1 values to nine by adding `PLANNED_INTERVENTION`, `EXECUTION_REPORT`, and `REVIEW_REQUEST`;
9. `NARROWING`: within the retained `ASSERTION_RECORD` family, exact target resolution contracts from six v0.1 assertion subtypes to `STRUCTURE_ASSERTION`, `OPERATION_CLAIM_ASSERTION`, and `COMPLIANCE_ASSERTION` only;
10. a future `ReviewDecision v0.2` carrier is required because v0.1 cannot carry that proof without a competing sidecar description; and
11. a mapping or postcondition failure aborts the ReviewDecision effect without rewriting the prior authorization result.

Approval of this candidate authorizes no schema, runtime, currentness, acceptance, or promotion change.

---

## 2. Primary trust boundary and PR boundary

The primary trust boundary is **final ReviewDecision domain semantics and commit classification**.

This candidate owns only:

- the v0.1 capability/gap inventory and minimum future carrier delta;
- exact reviewed-target resolution;
- exact intent-to-result mappings and permitted derivations;
- action/outcome compatibility;
- ReviewDecision-specific forbidden widening and postconditions;
- separation of the governed act from the committed decision record; and
- the ReviewDecision-specific payload of the protected-effect validation trace.

This PR adds only this candidate in the historical phase-report lane. It does not own or change:

- authorization, grants, delegation, actor resolution, sharing, or revocation;
- accepted-consequence semantics or a generic effect-composition mechanism;
- `REVIEW_REQUEST` result semantics;
- generic transaction, finalization-evidence, receipt, transport, retention, or key-custody machinery;
- current schemas, accepted RFCs, Event Grammar, runtime implementation, or currentness; or
- OFARM2 implementation.

The `EVIDENCE_SUFFICIENCY_CASE` eligibility correction remains on PR #11. This document records that dependency but does not reproduce or approve authorization law.

---

## 3. Governing inputs and upstream stop condition

This candidate is constrained by:

- Constitution RC2.1 sections 10.1, 10.2, 10.8, 10.9, 10.14, 11, and 13;
- the accepted Source Truth Record Closure RFC v0.1;
- the accepted Authority Action Matrix v0.1;
- the Event Grammar and Commit Matrix v0.1;
- the accepted Event Ingress and Promotion Boundary Closure RFC v0.1;
- current `ReviewDecision v0.1`, `SemanticEventEnvelope v0.1`, and `AcceptedEventConsequence v0.1`, plus current/default `EvidenceSufficiencyCase v0.2` and valid compatibility `EvidenceSufficiencyCase v0.1`;
- the protected-effect inventory on issue #12;
- the separately governed atomic transaction and consumption protocol on issue #19 as a downstream materialization and conformance prerequisite; and
- the approved amended `EI_REVIEW_DECISION_V0_2` resource, scope-envelope, outcome, and deterministic-evaluation semantics on PR #11 at `03a21f6`.

Active law permits case-scope review for `REVIEW_ACCEPT` and `REVIEW_REJECT_OR_CONTEST`. The approved PR #11 head uses a separate exact resource policy for those two actions and leaves `REVIEW_SUPERSEDE` on its prior narrower policy. This candidate consumes that exact approved boundary without reopening it; any semantic change to that head requires a new dependency decision before schema or executable-contract materialization.

---

## 4. Current `ReviewDecision v0.1` inventory

### 4.1 Capabilities and gaps

| Current field or behavior | v0.1 capability | Gap and Phase A disposition |
|---|---|---|
| `schemaVersion` | identifies `ofarm.reviewdecision.v0.1` | future carrier needs a distinct `ofarm.reviewdecision.v0.2` branch |
| `reviewDecisionId` | stable logical decision ID | retain and bind exactly to the intent and result digest |
| `reviewedArtifactFamily` | six broad families, including `EVIDENCE_SUFFICIENCY_CASE` | `WIDENING`: add exact kind and closed family resolution and add `PLANNED_INTERVENTION`, `EXECUTION_REPORT`, and `REVIEW_REQUEST` to the future family enum |
| assertion subtype coverage | coarse `ASSERTION_RECORD` permits all six current `AssertionRecord.assertionType` values | `NARROWING`: admit only structure, operation-claim, and compliance assertions; observation, lot, and other assertions remain outside the approved exact target closure |
| `reviewedArtifactRef` | one logical target ref | retain as the sole logical target identity and add exactly one separate immutable revision-ref or digest selector |
| `reviewAction` | three final actions plus `REVIEW_REQUEST` | close only the three final branches here |
| `decisionOutcomeState` | five independent outcomes | enforce the exact action/outcome matrix in section 9 |
| `anchorScopes` | one or more scope pairs | bind only the complete common authorization-envelope scope value extracted under the selected rule; require exact representability and complete equality |
| `decidedByPartyRef` | accountable deciding Party | retain; add the authenticated human actor and immutable finalization-evidence binding |
| `decidedAt` | date-time | bind to trusted time of the human final act |
| `evidenceRefs` | optional logical refs | replace with an explicit, possibly empty array of immutable evidence bindings |
| `resultingAcceptedConsequenceRefs` | optional companion refs | retain the relationship as optional immutable companion bindings, allowed only under section 7 |
| `supersedesReviewDecisionRef` | optional logical prior-decision ref | replace with an optional immutable lineage binding sourced from a governed, digest-bound domain intent field that does not create authority |
| `notes` | arbitrary optional prose | replace with exact required rationale; no independent result-local notes |
| conditional validation | none | add closed target/action/outcome and companion conditions |
| classification and integrity | absent | bind record commit class, associated act family, schema, contract, result, and trace digests outside result-local choice |

### 4.2 Example coverage

The repository has ten current `ReviewDecision v0.1` examples:

- seven `REVIEW_ACCEPT` / `ACCEPTED` examples;
- one `REVIEW_SUPERSEDE` / `SUPERSEDED` example targeting `ACCEPTED_EVENT_CONSEQUENCE`; and
- two `REVIEW_REQUEST` / `REVIEW_REQUESTED` examples.

Two acceptance examples carry `resultingAcceptedConsequenceRefs`. No current example covers `REJECTED`, `CONTESTED`, or direct review of an `EVIDENCE_SUFFICIENCY_CASE`. Current examples use logical refs rather than immutable revision/digest bindings.

### 4.3 Carrier decision

A narrow future `ReviewDecision v0.2` carrier is required. A sidecar around v0.1 would leave the history-bearing decision unable to state the exact target, actor, rationale, evidence, lineage, and companion bindings that the sidecar claims to validate.

The future carrier is a versioned extension. Existing v0.1 records remain valid v0.1 history and do not silently acquire v0.2 proof strength. No schema is created or edited in this PR.

---

## 5. Minimum future `ReviewDecision v0.2` carrier

### 5.1 Required and conditional fields

| Field | Required meaning |
|---|---|
| `schemaVersion` | exactly `ofarm.reviewdecision.v0.2` |
| `reviewDecisionId` | exact proposed decision ID |
| `reviewedArtifactKind` | exact action-rule-authorized target kind |
| `reviewedArtifactFamily` | exact domain family derived only by section 6 |
| `reviewedArtifactRef` | exact logical target ref |
| `reviewedArtifactRevisionRef` | conditional immutable target revision ref; exactly one of this field or `reviewedArtifactDigest` is required |
| `reviewedArtifactDigest` | conditional `sha256:` target content digest; exactly one of this field or `reviewedArtifactRevisionRef` is required |
| `reviewAction` | exact selected final-review action |
| `decisionOutcomeState` | exact intent-bound outcome |
| `anchorScopes` | complete rule-extracted common authorization-envelope scope binding, represented as one or more exact scope pairs |
| `decidedByPartyRef` | path-specific accountable authority subject |
| `decidedByHumanPrincipalRef` | authenticated natural person who performed the final act |
| `finalizationEvidenceBinding` | exact immutable binding to evidence proving actor, representation posture, basis, and human act |
| `decidedAt` | trusted time of the final human decision act |
| `rationale` | exact non-empty intent-bound rationale |
| `evidenceBindings` | required, possibly empty, array of exact immutable evidence bindings |
| `supersedesReviewDecisionBinding` | optional exact immutable decision-lineage binding copied only from the validated, digest-bound domain intent |
| `resultingAcceptedConsequenceBindings` | conditional exact immutable companion bindings allowed only for `REVIEW_ACCEPT` / `ACCEPTED` by section 7 |

`reviewedArtifactRef` is the sole logical identity of the reviewed target. Exactly one of `reviewedArtifactRevisionRef` or `reviewedArtifactDigest` selects its immutable bytes; neither field contains or repeats a logical ref, and neither zero nor two selectors is valid.

Every other field named `*Binding`, and each element of a `*Bindings` array, is a tagged value containing one logical ref and exactly one immutable revision ref or `sha256:` content digest. Unknown properties are rejected.

### 5.2 Deciding Party, human actor, and representation

`decidedByPartyRef` remains the canonical deciding Party:

- for self-action, it is the Party identity of the authenticated natural person;
- for represented action, it is the exact represented Party selected by the authorization path.

`decidedByHumanPrincipalRef` is always the authenticated natural person who performed the final act. `finalizationEvidenceBinding` proves the exact `SELF` or `REPRESENTED_PARTY` posture and, when represented, the immutable representation basis.

The domain record does not duplicate grants, roles, representation-basis internals, policy traces, challenges, or approval internals. An organization, sponsor, software agent, or caller-provided Party cannot substitute for the human principal.

### 5.3 Scope and lineage source ownership

Approved PR #11 section 7.6 requires every effect-intent profile, including `EI_REVIEW_DECISION_V0_2`, to carry a common authorization envelope containing scope. The profile table lists additional operation-specific authorization-relevant content; omission of scope from the `EI_REVIEW_DECISION_V0_2` row does not remove that common field. `RD_SCOPES` consumes only the complete scope value produced by the selected rule's `authorizationViewExtraction` from that common envelope.

The materialized intent schema and protected-effect contract must bind the exact source pointer or pointers, destination pointer, cardinality, and array/set posture that map the extracted scope value to one or more v0.1-compatible `{scopeType, scopeRef}` pairs in `anchorScopes`. No profile-local, caller-side, or result-only scope is permitted. If the approved common scope cannot be represented completely and unambiguously in `anchorScopes`, materialization stops and PR #11 requires a separately reviewed authorization amendment; this contract cannot label extra scopes non-authorization-relevant to avoid that gate.

`supersedesReviewDecisionBinding` is different: it is an optional governed ReviewDecision-domain field added to the validated `EI_REVIEW_DECISION_V0_2` intent under PR #11's allowance for governed fields that do not change authorization. It is covered by `effectIntentDigest`, copied exactly or required absent, and validated only by this protected-effect contract. It cannot change the selected action, authority target, outcome, scope, authority subject, or path eligibility. If lineage later affects any authorization decision, PR #11 must be amended and reapproved before materialization.

---

## 6. Exact target resolution

### 6.1 Action eligibility

| Action | Eligible target policy after renewed PR #11 approval |
|---|---|
| `REVIEW_ACCEPT` | eleven kinds in `RP_FINAL_REVIEW_CASE_ELIGIBLE_TARGET_ONE`, including `EVIDENCE_SUFFICIENCY_CASE` |
| `REVIEW_REJECT_OR_CONTEST` | the same eleven case-eligible kinds |
| `REVIEW_SUPERSEDE` | ten kinds in `RP_FINAL_REVIEW_TARGET_ONE`; `EVIDENCE_SUFFICIENCY_CASE` is not inferred |

### 6.2 Target-kind to domain-family map

| Exact `reviewedArtifactKind` | Required `reviewedArtifactFamily` | Resolved carrier posture |
|---|---|---|
| `STRUCTURE_ASSERTION` | `ASSERTION_RECORD` | `AssertionRecord.assertionType` is `STRUCTURE_ASSERTION` |
| `OPERATION_ASSERTION` | `ASSERTION_RECORD` | `AssertionRecord.assertionType` is `OPERATION_CLAIM_ASSERTION` |
| `COMPLIANCE_ASSERTION` | `ASSERTION_RECORD` | `AssertionRecord.assertionType` is `COMPLIANCE_ASSERTION` |
| `INTERVENTION_PLAN` | `PLANNED_INTERVENTION` | exact governed `PlannedIntervention` carrier |
| `EXECUTION_REPORT` | `EXECUTION_REPORT` | exact carrier selected by its separately reviewed composition closure |
| `REVIEW_REQUEST` | `REVIEW_REQUEST` | exact carrier selected by the separate review-request closure |
| `DOCUMENT_ASSEMBLY` | `DOCUMENT_ASSEMBLY` | exact document-assembly carrier |
| `DOSSIER_ASSEMBLY` | `DOSSIER_ASSEMBLY` | exact dossier-assembly carrier |
| `SUBMISSION_ASSEMBLY` | `SUBMISSION_ASSEMBLY` | exact submission-assembly carrier |
| `ACCEPTED_EVENT_CONSEQUENCE` | `ACCEPTED_EVENT_CONSEQUENCE` | exact accepted-consequence carrier |
| `EVIDENCE_SUFFICIENCY_CASE` | `EVIDENCE_SUFFICIENCY_CASE` | exact active governed carrier version selected by the immutable target selector; v0.2 is current/default for new cases and v0.1 remains valid for compatibility; eligible only for the first two actions |

The following directional labels reuse PR #11 section 7.5.1 vocabulary so the disclosures are comparable, but they classify this result-carrier resolution axis rather than reclassifying the separate authorization-target axis.

`WIDENING`: compared with the six-value v0.1 `reviewedArtifactFamily` enum, this exact map retains all six values and adds three: `PLANNED_INTERVENTION`, `EXECUTION_REPORT`, and `REVIEW_REQUEST`. This applies only to new v0.2 decisions and is not a rename or inferred compatibility rule.

`NARROWING`: within the retained `ASSERTION_RECORD` family, the map deliberately contracts exact review eligibility from all six current `AssertionRecord.assertionType` values to three. `STRUCTURE_ASSERTION`, `OPERATION_CLAIM_ASSERTION` through the exact `OPERATION_ASSERTION` target kind, and `COMPLIANCE_ASSERTION` are included. `OBSERVATION_ASSERTION`, `LOT_ASSERTION`, and `OTHER_ASSERTION` are excluded. No current example breaks, but a new v0.2 final decision cannot review an excluded assertion subtype. Re-enabling one requires a separate PR #11 authorization amendment followed by a matching amendment to this domain contract.

The coarse v0.1 token `ASSERTION_RECORD` is a result family, not an intent alias for one of the three exact assertion kinds. A target kind without a governed content-addressed carrier or resolution profile is unavailable at the domain gate even if authorization returned `ALLOW`. The runtime cannot invent a carrier, use a mutable latest lookup, or coerce another family.

Case-target resolution binds the exact schema ref, version, digest, and immutable case bytes. Valid v0.1 cases are not upgraded to v0.2 proof strength and are not rejected solely because v0.2 is the default for new work. The superseded `v0.2-draft`, unknown versions, and mutable or unresolved case records fail target resolution.

---

## 7. Companion-effect boundary

This contract's own result cardinality is exactly one `ReviewDecision`. That is not a transaction-wide prohibition on every other governed record.

The companion field is closed by review branch:

| Review branch | `resultingAcceptedConsequenceBindings` rule |
|---|---|
| `REVIEW_ACCEPT` / `ACCEPTED` | absent for standalone validation; may be present and non-empty only under the separately reviewed composition below |
| `REVIEW_REJECT_OR_CONTEST` / `REJECTED` | absent |
| `REVIEW_REJECT_OR_CONTEST` / `CONTESTED` | absent |
| `REVIEW_SUPERSEDE` / `SUPERSEDED` | absent; no accepted correction-composition rule currently authorizes a replacement consequence |

For the accepted branch, a non-empty companion field is valid only when:

1. a separate accepted-consequence contract owns and validates each companion consequence;
2. a separately reviewed enclosing composition identifies the exact governing authority basis for the decision and every companion result;
3. when active promotion law permits the consequence as a contract-defined derived companion of the authorized review intent, the composition binds that derivation and does not invent a second action class or require a nonexistent second effect intent;
4. the composition pins the ReviewDecision contract, intent, and result digest plus each companion contract, derivation rule, and result digest before commit;
5. `resultingAcceptedConsequenceBindings` is an exact copy of the companion results selected by that binding; and
6. failure of either contract or the composition aborts the composed commit.

This candidate defines only the ReviewDecision side of that interface. It recognizes no separate consequence action and does not define accepted-consequence construction or create a generic composition contract. Requiring a new consequence action would first need a separate authorization amendment and renewed review of this boundary. Without the exact governing authority, contract, derivation, and composition bindings, a non-empty companion list or inserted consequence is an unbound effect and fails. Any future proposal to attach a replacement consequence to `REVIEW_SUPERSEDE` requires a separately reviewed amendment rather than inference from the accepted branch.

Current-state materialization is always downstream and is never a companion effect of this contract.

---

## 8. Contract identity and exact mappings

### 8.1 Contract identity

| Property | Closed value |
|---|---|
| contract ID | `ofarm.protectedeffect.reviewdecision.final.v0.1` |
| contract version | `0.1` |
| owning domain family | `REVIEW_DECISION_FINAL` |
| intent profile | `EI_REVIEW_DECISION_V0_2` |
| result carrier | future `ofarm.reviewdecision.v0.2` final-decision branch |
| own result cardinality | exactly one immutable `ReviewDecision` |
| canonicalization | `JCS_RFC8785_SHA256` |

The materialized contract must bind its exact intent-schema and result-schema refs, versions, and digests plus every mapping, derivation, forbidden widening rule, classification, postcondition, and trace requirement below.

### 8.2 Stable field mappings

| Mapping ID | Authoritative source | Result destination and rule |
|---|---|---|
| `RD_SCHEMA` | selected result-schema binding | `schemaVersion` is exactly `ofarm.reviewdecision.v0.2` |
| `RD_EFFECT_SUBJECT` | intent effect-subject kind | constant `REVIEW_DECISION`; any other kind fails |
| `RD_ID` | intent proposed decision ID | exact copy to `reviewDecisionId` |
| `RD_TARGET_KIND` | intent `PRIMARY_RECORD.resourceKind` | exact copy to `reviewedArtifactKind`; no aliasing |
| `RD_TARGET_FAMILY` | target kind plus exact schema ref/version/digest and immutable resolved bytes | closed section 6 derivation to `reviewedArtifactFamily` |
| `RD_TARGET_REF` | intent `PRIMARY_RECORD.resourceRef` | exact copy to `reviewedArtifactRef` |
| `RD_TARGET_BINDING` | intent target revision/digest | exact copy to one and only one of `reviewedArtifactRevisionRef` or `reviewedArtifactDigest`; no second logical ref exists |
| `RD_SCOPES` | complete rule-extracted common authorization-envelope scope value defined in section 5.3 | exact complete mapping to `anchorScopes` under the contract-bound cardinality and array/set posture; no additional scope |
| `RD_ACTION` | selected action rule and intent action | both must agree; exact copy to `reviewAction` |
| `RD_OUTCOME` | intent outcome | exact section 9 branch value |
| `RD_DECIDING_PARTY` | selected authority subject in finalization evidence | exact copy to `decidedByPartyRef` |
| `RD_HUMAN` | authenticated natural-person principal | exact copy to `decidedByHumanPrincipalRef` |
| `RD_FINALIZATION_EVIDENCE` | trusted finalization-evidence binding | exact copy to `finalizationEvidenceBinding` |
| `RD_TIME` | trusted human-act time | exact copy to `decidedAt` |
| `RD_RATIONALE` | intent rationale | exact Unicode value; no normalization or summarization |
| `RD_EVIDENCE` | intent evidence bindings | complete exact array; no addition, omission, or ref-only downgrade |
| `RD_PRIOR_DECISION` | optional governed `supersedesReviewDecisionBinding` inside the validated, digest-bound intent as defined in section 5.3 | exact copy or required absence; no lookup or caller side channel |
| `RD_COMPANION_CONSEQUENCES` | section 7 branch plus separately reviewed composition binding | exact accepted-branch companion array or required absence |

Every mapping receives one explicit disposition. A missing, duplicated, ambiguous, type-invalid, or conflicting authoritative source fails the contract.

### 8.3 Permitted derivations

These are the only permitted derivations:

| Derived value | Exact source and rule |
|---|---|
| `schemaVersion` | constant from the selected result-schema binding |
| `reviewedArtifactFamily` | section 6 map, confirmed against immutable target bytes |
| canonical scope representation | only the contract-bound transformation from the complete rule-extracted common-envelope scope value to `anchorScopes`; otherwise exact copy |
| associated primary event family | contract constant `GovernanceEvent`, recorded outside the ReviewDecision carrier |
| record commit class | contract constant `governance decision`, recorded outside result-local choice |
| result and resolution digests | shared JCS/SHA-256 profile over the exact validated or resolved bytes |

Everything else is an exact copy or required absence. There is no default action, outcome, actor, target, scope, rationale, evidence, lineage, companion, or decision time. There is no local sorting, name search, family coercion, latest-revision lookup, lineage search, or generated consequence ID.

---

## 9. Exact action/outcome closure

| Authorized action | Required `reviewAction` | Allowed `decisionOutcomeState` |
|---|---|---|
| `REVIEW_ACCEPT` | `REVIEW_ACCEPT` | exactly `ACCEPTED` |
| `REVIEW_REJECT_OR_CONTEST` | `REVIEW_REJECT_OR_CONTEST` | exactly the one intent-bound value `REJECTED` or `CONTESTED` |
| `REVIEW_SUPERSEDE` | `REVIEW_SUPERSEDE` | exactly `SUPERSEDED` |

Every other pairing fails. The combined reject-or-contest action is not split; the human-bound intent selects one closed outcome before authorization. The `REVIEW_REQUEST` action and its `REVIEW_REQUESTED` outcome are outside this final-decision contract. That exclusion does not apply to a governed record whose exact `reviewedArtifactKind` and `reviewedArtifactFamily` are `REVIEW_REQUEST`; such a record remains an eligible target of the three final-review actions under section 6.

Supersession never rewrites or deletes the reviewed target or a prior decision. `supersedesReviewDecisionBinding` records decision lineage only when the exact immutable binding is present in the validated intent and an applicable lineage rule passes.

---

## 10. Event family and commit class

The governed final-review **act** has primary event family `GovernanceEvent`. The immutable `ReviewDecision` **record** has commit class `governance decision`. These are separate semantic dimensions.

A `SemanticEventEnvelope`, when required by the active ingress path, is a separate governed event record linked to the exact target and decision. The ReviewDecision is never retyped as an event envelope and carries no caller-selected event family.

The validation trace, authorization/finalization evidence, and governed-effect receipt remain separate evidence records. Their `EvidenceEvent` classification does not change the review act or decision record.

---

## 11. ReviewDecision-specific postconditions

### 11.1 Common postconditions

| Postcondition ID | Required proposed-state condition |
|---|---|
| `PC_ONE_DECISION` | exactly one new ReviewDecision ID resolves to one schema-valid immutable result |
| `PC_VALIDATED_BYTES` | committed decision bytes equal the bytes validated by this contract |
| `PC_INPUTS_IMMUTABLE` | target, evidence, finalization evidence, prior decision, and companion inputs remain byte-identical |
| `PC_ACTION_OUTCOME` | action and outcome satisfy section 9 |
| `PC_ACTOR_BINDING` | deciding Party, human principal, finalization evidence, and decision time satisfy sections 5 and 8 |
| `PC_CLASSIFICATION` | associated act is `GovernanceEvent` and the decision record's commit class is `governance decision` |
| `PC_NO_UNBOUND_EFFECT` | no target rewrite, consequence, event envelope, materialization, promotion record, or other governed effect is inserted or changed without the exact governing authority, contract, and composition bindings required by its applicable boundary |
| `PC_COMPANION_BINDING` | the companion field is absent except for the section 7 accepted branch; every permitted link exactly matches a separately validated composed result |
| `PC_NO_CURRENT_STATE` | this contract writes no current-state materialization |
| `PC_ATOMIC_EVIDENCE` | the shared transaction gate reports atomic commit of the decision, any bound composed results, passing evidence, and single-use consumption |
| `PC_UNIQUE_ID` | a duplicate decision ID with different bytes is rejected |

### 11.2 Branch postconditions

| Postcondition ID | Branch-specific meaning |
|---|---|
| `PC_ACCEPT` | acceptance is recorded for the exact target; companion bindings are absent unless the exact section 7 accepted-branch composition passes |
| `PC_REJECT` | rejection is recorded without deleting the target or creating a contrary accepted state; companion bindings are absent |
| `PC_CONTEST` | contested posture is explicit and is not treated as accepted, rejected, or resolved; companion bindings are absent |
| `PC_SUPERSEDE` | supersession is recorded without rewriting prior history; companion bindings are absent and downstream freshness is re-evaluated separately |

---

## 12. Content addressing and validation trace

### 12.1 Digest closure

The machine contract's `contractDigest` is `sha256:` plus SHA-256 over RFC 8785 JCS bytes of the complete contract after removing exactly the top-level `/contractDigest` member. No nested or other top-level member is excluded.

`resultDigest` covers the complete schema-valid proposed ReviewDecision with no excluded member. `resultSchemaDigest` binds the exact selected schema bytes. Every revision-ref resolution records the digest of the resolved immutable bytes.

These short application rules do not define a competing generic digest framework. The later shared finalization-evidence profile may carry them by reference but cannot weaken or omit this contract's semantic closure.

### 12.2 ReviewDecision validation payload

The immutable protected-effect validation trace must bind:

- authorization result/rule and effect-intent refs/digests;
- result ID/ref/digest and result-schema ref/version/digest;
- contract ID/version/ref/digest;
- exact target and every resolved immutable input digest;
- one `PASS`, `FAIL`, legitimate `NOT_APPLICABLE`, or dependency-bound `NOT_EVALUATED` disposition for every `RD_*` mapping;
- one such disposition for every `PC_*` postcondition;
- source/destination selectors or pointers and compared digests;
- associated act family and record commit class; and
- an overall `PASS` or `FAIL` disposition.

`NOT_APPLICABLE` means that an item's contract-declared condition does not apply; a required item cannot use it. `NOT_EVALUATED` means no pass-or-fail conclusion was reached because a named prerequisite did not pass. A required dependent item may be `NOT_EVALUATED`, but that disposition prevents overall `PASS`. The materialized contract must enumerate the prerequisite IDs for every dependency that can produce `NOT_EVALUATED`; a runtime cannot use it to suppress an independent failure or omit an evaluation arbitrarily. Overall `PASS` requires every required mapping and postcondition to pass. The trace itself is immutable and content-addressed under the separately reviewed shared evidence envelope; until that envelope exists with a real ref/digest, no executable binding exists.

This section owns the ReviewDecision-specific validation payload. It does not restate generic challenge, receipt, retention, transaction sequencing, or persistence machinery.

---

## 13. Validation and failure semantics

Before commit, the protected-effect gate must:

1. verify the selected action rule's exact effect-intent-schema and protected-effect-contract bindings;
2. load and digest-verify the referenced protected-effect contract;
3. verify the result-schema ref, version, and digest owned by that contract;
4. validate the proposed result against that result schema;
5. evaluate every applicable `RD_*` mapping and `PC_*` postcondition; and
6. supply an overall passing immutable trace to the shared atomic transaction gate whose protocol remains separately owned by `samovers/OFARM#19`.

If any item fails, no ReviewDecision or companion effect commits and single-use consumption does not commit. The existing authorization result remains its authority-gate result; `ALLOW` is not rewritten to `DENY` or treated as proof that the domain gate passed.

This candidate states only those ReviewDecision-specific preconditions and effects. It does not implement or redefine the generic transaction manager.

---

## 14. Production-reachable hostile cases

| Case | Required disposition |
|---|---|
| any invalid action/outcome pair | branch mapping fails; no decision commits |
| intent binds `REJECTED` but result says `CONTESTED`, or vice versa | `RD_OUTCOME` fails without changing intent or authorization result |
| target kind/ref/revision/digest is substituted | target mapping fails |
| zero or both target immutable selectors are present, or a second logical target ref is introduced | `RD_TARGET_REF` / `RD_TARGET_BINDING` fails |
| caller uses coarse `ASSERTION_RECORD` as an intent alias | `RD_TARGET_KIND` fails |
| an `OBSERVATION_ASSERTION`, `LOT_ASSERTION`, or `OTHER_ASSERTION` is offered through the coarse v0.1 assertion family or coerced to an admitted exact kind | exact target eligibility or `RD_TARGET_KIND` / `RD_TARGET_FAMILY` fails; no v0.2 decision commits |
| target carrier is unsupported, unresolved, mutable, or inconsistent with its kind | `RD_TARGET_FAMILY` or binding fails |
| a final-review action targets an exact governed `REVIEW_REQUEST` record but the validator treats the excluded `REVIEW_REQUEST` action token as excluding that target | conformance failure; section 6 target eligibility remains available |
| `EVIDENCE_SUFFICIENCY_CASE` is used by `REVIEW_SUPERSEDE` or while the exact PR #11 dependency pin is absent or invalidated | action-rule/target eligibility fails |
| a case target for accept/reject is omitted or substituted by the evaluator | authorization extractor conformance fails; no domain result commits |
| a valid immutable `EvidenceSufficiencyCase v0.1` is rejected solely because v0.2 is current/default, or is silently upgraded to v0.2 | `RD_TARGET_FAMILY` fails |
| a case target uses superseded `v0.2-draft`, an unknown version, or mutable/unresolved bytes | `RD_TARGET_FAMILY` / `RD_TARGET_BINDING` fails |
| result scope is sourced from a profile-local field or caller side channel instead of the complete rule-extracted common-envelope scope, or one scope is added, dropped, or changed | `RD_SCOPES` fails |
| deciding Party is replaced by the human principal for represented action | `RD_DECIDING_PARTY` fails |
| human principal is replaced by an organization, sponsor, or agent | `RD_HUMAN` fails |
| finalization evidence is missing, mutable, or substituted | `RD_FINALIZATION_EVIDENCE` fails |
| request, caller, or commit time replaces trusted human-act time | `RD_TIME` fails |
| rationale differs by whitespace, case, translation, or summarization | `RD_RATIONALE` fails |
| evidence binding is changed, omitted, added, or reordered contrary to schema posture | `RD_EVIDENCE` fails |
| prior-decision lineage is supplied outside the validated intent, omitted when present there, added when absent there, replaced, or changed after `effectIntentDigest` | `RD_PRIOR_DECISION` fails |
| accepted-branch consequence is created without the exact governing authority basis, contract-defined derivation, validation, and composition binding | `PC_NO_UNBOUND_EFFECT` fails |
| `REJECTED`, `CONTESTED`, or `SUPERSEDED` carries any companion consequence binding | `RD_COMPANION_CONSEQUENCES` / branch postcondition fails |
| companion list differs from the composed result digests | `RD_COMPANION_CONSEQUENCES` / `PC_COMPANION_BINDING` fails |
| target or prior decision is mutated or deleted | `PC_INPUTS_IMMUTABLE` fails |
| contract writes current state or treats acceptance as automatic promotion | `PC_NO_CURRENT_STATE` fails |
| ReviewDecision is retyped as an event envelope or assigned an event family field | `PC_CLASSIFICATION` fails |
| associated act is not `GovernanceEvent` or record class is not `governance decision` | `PC_CLASSIFICATION` fails |
| contract, schema, intent, result, or resolved-input digest changes | binding or mapping fails |
| `RD_TARGET_KIND` fails but dependent `RD_TARGET_FAMILY` is reported as `PASS`, `FAIL`, or `NOT_APPLICABLE` instead of dependency-bound `NOT_EVALUATED` | trace conformance fails; no domain result commits |
| one required mapping/postcondition disposition is missing | overall trace cannot pass |
| duplicate decision ID resolves to different bytes | `PC_UNIQUE_ID` fails |
| relevant state changes between validation and atomic commit | shared transaction gate fails and requires re-evaluation |
| domain failure rewrites authorization `ALLOW` | conformance failure; authorization evidence remains unchanged |

Fixtures must enter through the production result builder, contract validator, and transaction boundary rather than unit-only helpers.

---

## 15. Migration and currentness

`ReviewDecision v0.1` remains current/default until a separately governed promotion says otherwise. Existing records and examples remain v0.1 history.

A v0.1 record cannot claim v0.2 strength unless immutable source evidence establishes every required field and mapping. Missing target revision, actor/finalization evidence, rationale, evidence revision, decision-time basis, outcome intent, or companion binding cannot be guessed.

Migration never rewrites a v0.1 family token. The three new family values apply only to new schema-valid v0.2 decisions. Existing v0.1 decisions over `ASSERTION_RECORD` remain valid history regardless of subtype, but they do not make `OBSERVATION_ASSERTION`, `LOT_ASSERTION`, or `OTHER_ASSERTION` eligible targets for a new v0.2 final-review decision. Likewise, a v0.1 `anchorScopes` array cannot be upgraded unless the exact validated intent and rule-extracted common-envelope scope prove the complete mapping; missing scope or lineage provenance is not reconstructed from the result.

Draft schema or contract presence changes no currentness. Later promotion must preserve links to v0.1 history rather than rewrite it.

---

## 16. Later `AuthorizationPolicyBundle v0.2` binding

This PR does not create or edit the policy bundle.

After renewed PR #11 approval and materialization of real content-addressed protected-effect contract bytes, the bundle PR must:

1. bind the exact contract ID/version/ref/digest and owning family;
2. bind the reviewed contract to the three final-review action rules;
3. preserve the action-specific case-target policy split from PR #11;
4. exclude `REVIEW_REQUEST` from this final-decision contract; and
5. include that protected-effect contract binding in each affected complete per-action `ruleDigest` closure.

The result-schema binding, `RD_*` selectors, derivations, forbidden-widening rules, classification, postconditions, and trace requirements remain solely inside the content-addressed protected-effect contract. Changing any of them changes `contractDigest`, which changes each affected action-rule digest. The bundle must not copy them or become a second source of domain semantics.

A later runtime index may expose digest-checked contract metadata for lookup only when it is explicitly derived and non-authoritative. Such an index is not a Phase A semantic requirement.

The bundle cannot point at this prose file as an executable contract.

---

## 17. Traceability to issue #15

| Acceptance criterion | Disposition |
|---|---|
| inventory v0.1 capabilities and gaps | section 4 |
| decide whether a minimal v0.2 carrier is required | sections 4.3 and 5 |
| exact action/result constraints | section 9 |
| bind ID, target, scopes, human/Party posture, rationale, evidence, time, lineage, and companions | sections 5 through 8 |
| disclose family-enum widening and assertion-subtype narrowing | sections 1, 4, 6, 15, and 18 |
| distinguish the excluded review-request action/outcome from an eligible review-request target | sections 6, 9, and 14 |
| enumerate permitted derivations | section 8.3 |
| forbid substitution, unbound consequence creation, mutation, and promotion shortcuts | sections 7, 11, 13, and 14 |
| separate `GovernanceEvent` act from `governance decision` record | section 10 |
| content-address contract and deterministic digest projection | sections 8.1 and 12.1 |
| immutable dependency-aware mapping/postcondition trace with required digests | sections 12.2 and 14 |
| validate before atomic commit without rewriting authorization | section 13 |
| production-reachable hostile cases | section 14 |
| later whole-contract bundle registration without duplicating domain semantics or creating the bundle here | section 16 |

---

## 18. Steward approval card

| Decision | Proposed answer | Approval required |
|---|---|---|
| Is a future `ReviewDecision v0.2` carrier required? | yes | yes |
| Does this contract cover exactly the three final review actions? | yes | yes |
| Does it validate exactly one ReviewDecision while allowing only separately bound companion effects? | yes | yes |
| Has the exact PR #11 authorization candidate, including the case-target and deterministic-evaluation amendments, received renewed approval? | yes, at `03a21f669ee04f96d444e14f00ae7212cab04803` | yes |
| Are case targets eligible only for accept and reject-or-contest under the proposed action split? | yes | yes |
| Does case resolution preserve valid v0.1 compatibility while rejecting superseded, unknown, mutable, or unresolved carriers? | yes | yes |
| Are target kind, sole logical ref, one immutable selector, and domain-family resolution exact? | yes | yes |
| Is the future `reviewedArtifactFamily` enum change classified `WIDENING`, from six values to nine by adding `PLANNED_INTERVENTION`, `EXECUTION_REPORT`, and `REVIEW_REQUEST`? | yes | yes |
| Is exact `ASSERTION_RECORD` target coverage classified `NARROWING`, from six current subtypes to structure, operation-claim, and compliance, excluding observation, lot, and other assertions? | yes; re-enabling an excluded subtype requires separate authorization and domain amendments | yes |
| Are action/outcome pairs fixed exactly by section 9? | yes | yes |
| Must reject versus contest be intent-bound? | yes | yes |
| Are deciding Party, authenticated human, and immutable finalization evidence separate fields? | yes | yes |
| Is `decidedAt` the trusted human-act time? | yes | yes |
| Does `RD_SCOPES` map only the complete rule-extracted common authorization-envelope scope to `anchorScopes`, with materialization stopped if that mapping is not exact and unambiguous? | yes | yes |
| Is optional lineage a governed, digest-bound ReviewDecision-domain intent field that cannot affect authority without a separately approved PR #11 amendment? | yes | yes |
| Are rationale and evidence exact rather than defaulted? | yes | yes |
| May consequence links exist only for accept/accepted under the separately governed composition in section 7? | yes; reject, contest, and supersede require absence | yes |
| Does that composition bind the exact governing authority basis without inventing a consequence action? | yes | yes |
| Is the act `GovernanceEvent` while the record class is `governance decision`? | yes | yes |
| Must every `RD_*` and `PC_*` item have an explicit `PASS`, `FAIL`, legitimate `NOT_APPLICABLE`, or dependency-bound `NOT_EVALUATED` trace disposition, with overall `PASS` requiring every required item to pass? | yes | yes |
| Does protected-effect failure leave authorization evidence unchanged? | yes | yes |
| Must `samovers/OFARM#19` close the shared atomic transaction and consumption protocol before machine materialization, hostile conformance, or runtime implementation relies on that gate? | yes | yes |
| Does the later bundle bind the protected-effect contract as one unit while schema, mappings, shared evidence, conformance, acceptance, and promotion remain separately owned? | yes | yes |

Any requested authorization, consequence-contract, generic composition, shared-evidence, runtime, or currentness change must remain in its own trust-boundary PR.

---

## 19. Staged delivery and completion

1. **Authorization prerequisite:** satisfied by renewed semantic approval for exact PR #11 head `03a21f669ee04f96d444e14f00ae7212cab04803`; re-open this gate if that head's semantics change.
2. **Phase A domain approval:** approve or amend this one-file ReviewDecision candidate.
3. **Governed transaction prerequisite:** close `samovers/OFARM#19` as its own trust-boundary PR before machine materialization, hostile conformance, or runtime implementation claims the shared atomic transaction and consumption gate used by this contract.
4. **Domain materialization:** separately create the non-default machine contract, exact selectors, and `ReviewDecision v0.2` schema; stop and return to the authorization prerequisite if the common-envelope scope cannot map completely and unambiguously to `anchorScopes`.
5. **Shared evidence materialization:** separately create the finalization-evidence, validation-trace envelope, and governed-effect receipt profiles.
6. **Optional composition closure:** if accepted-branch companion consequences are implemented, separately review their exact governing authority basis, derived-result rule, consequence contract, and composition binding without inventing a new action locally.
7. **Bundle binding:** separately bind the exact reviewed protected-effect contract identity/ref/digest as one unit into `AuthorizationPolicyBundle v0.2`.
8. **Hostile conformance:** exercise section 14 through production-reachable paths.
9. **Acceptance and promotion:** accept exact bytes and change current/default status only through separate governed steps.
10. **OFARM2 extraction:** consume only promoted, digest-verified canonical bytes.

Phase A is complete when issue #15's criteria are reviewed, the exact PR #11 dependency remains approved, and this PR still changes only this non-authoritative candidate file.
