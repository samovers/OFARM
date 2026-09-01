# OFARM Final ReviewDecision Protected-Effect Contract v0.1

Date: 2026-09-01
Status: Phase A candidate for `samovers/OFARM#15`; non-authoritative, not accepted law, and not a current/default machine contract
Depends on: protected-effect inventory `samovers/OFARM#12` and renewed semantic review of the authorization amendment on issue #16 / PR #11 at `5974bb916ac8a2c5a6230facbb9836f639c754c3`
Blocking prerequisite: the amended PR #11 head must receive renewed semantic approval before machine-readable materialization
Scope: define the ReviewDecision-specific mapping from an authorized final-review intent to one immutable ReviewDecision record

---

## 1. Decision requested

Stewards are asked to approve, reject, or amend these bounded decisions:

1. this contract validates exactly one `ReviewDecision` record for `REVIEW_ACCEPT`, `REVIEW_REJECT_OR_CONTEST`, or `REVIEW_SUPERSEDE`;
2. it does not itself authorize or validate an `AcceptedEventConsequence`, current-state materialization, target mutation, or other companion effect;
3. it does not prohibit an independently authorized and independently validated companion consequence that is bound by a separately reviewed atomic composition before commit;
4. the governed final-review act has primary event family `GovernanceEvent`, while the `ReviewDecision` record has commit class `governance decision`;
5. the result preserves the exact authorized target, action, outcome, scopes, accountable deciding Party, authenticated human actor, finalization evidence, decision time, rationale, evidence, and optional lineage;
6. a future `ReviewDecision v0.2` carrier is required because v0.1 cannot carry that proof without a competing sidecar description; and
7. a mapping or postcondition failure aborts the ReviewDecision effect without rewriting the prior authorization result.

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
- current `ReviewDecision v0.1`, `SemanticEventEnvelope v0.1`, `AcceptedEventConsequence v0.1`, and `EvidenceSufficiencyCase v0.2`;
- the protected-effect inventory on issue #12; and
- the amended `EI_REVIEW_DECISION_V0_2` resource and outcome semantics on PR #11 at `5974bb9`, subject to renewed approval.

Active law permits case-scope review for `REVIEW_ACCEPT` and `REVIEW_REJECT_OR_CONTEST`. PR #11 now proposes a separate exact resource policy for those two actions and leaves `REVIEW_SUPERSEDE` on its prior narrower policy. Until that amendment is re-approved, this candidate may be reviewed as a domain proposal but no schema or executable contract may be materialized from it.

---

## 4. Current `ReviewDecision v0.1` inventory

### 4.1 Capabilities and gaps

| Current field or behavior | v0.1 capability | Gap and Phase A disposition |
|---|---|---|
| `schemaVersion` | identifies `ofarm.reviewdecision.v0.1` | future carrier needs a distinct `ofarm.reviewdecision.v0.2` branch |
| `reviewDecisionId` | stable logical decision ID | retain and bind exactly to the intent and result digest |
| `reviewedArtifactFamily` | six broad families, including `EVIDENCE_SUFFICIENCY_CASE` | cannot preserve exact authorization target kind or immutable carrier posture; add exact kind and closed family resolution |
| `reviewedArtifactRef` | one logical target ref | add exactly one immutable revision or digest binding |
| `reviewAction` | three final actions plus `REVIEW_REQUEST` | close only the three final branches here |
| `decisionOutcomeState` | five independent outcomes | enforce the exact action/outcome matrix in section 9 |
| `anchorScopes` | one or more scope pairs | require complete equality with the intent under its declared array/set posture |
| `decidedByPartyRef` | accountable deciding Party | retain; add the authenticated human actor and immutable finalization-evidence binding |
| `decidedAt` | date-time | bind to trusted time of the human final act |
| `evidenceRefs` | optional logical refs | replace with an explicit, possibly empty array of immutable evidence bindings |
| `resultingAcceptedConsequenceRefs` | optional companion refs | retain the relationship as optional immutable companion bindings, allowed only under section 7 |
| `supersedesReviewDecisionRef` | optional logical prior-decision ref | replace with an optional immutable lineage binding |
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
| `reviewedArtifactBinding` | exactly one immutable revision ref or content digest |
| `reviewAction` | exact selected final-review action |
| `decisionOutcomeState` | exact intent-bound outcome |
| `anchorScopes` | complete intent-bound scopes |
| `decidedByPartyRef` | path-specific accountable authority subject |
| `decidedByHumanPrincipalRef` | authenticated natural person who performed the final act |
| `finalizationEvidenceBinding` | exact immutable binding to evidence proving actor, representation posture, basis, and human act |
| `decidedAt` | trusted time of the final human decision act |
| `rationale` | exact non-empty intent-bound rationale |
| `evidenceBindings` | required, possibly empty, array of exact immutable evidence bindings |
| `supersedesReviewDecisionBinding` | optional exact immutable decision-lineage binding |
| `resultingAcceptedConsequenceBindings` | optional exact immutable companion bindings allowed only by section 7 |

Every binding is a tagged value containing a logical ref and exactly one immutable revision ref or `sha256:` content digest. Neither zero nor two immutable selectors is valid. Unknown properties are rejected.

### 5.2 Deciding Party, human actor, and representation

`decidedByPartyRef` remains the canonical deciding Party:

- for self-action, it is the Party identity of the authenticated natural person;
- for represented action, it is the exact represented Party selected by the authorization path.

`decidedByHumanPrincipalRef` is always the authenticated natural person who performed the final act. `finalizationEvidenceBinding` proves the exact `SELF` or `REPRESENTED_PARTY` posture and, when represented, the immutable representation basis.

The domain record does not duplicate grants, roles, representation-basis internals, policy traces, challenges, or approval internals. An organization, sponsor, software agent, or caller-provided Party cannot substitute for the human principal.

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
| `EVIDENCE_SUFFICIENCY_CASE` | `EVIDENCE_SUFFICIENCY_CASE` | exact current/default `EvidenceSufficiencyCase v0.2` carrier; eligible only for the first two actions |

The coarse v0.1 token `ASSERTION_RECORD` is a result family, not an intent alias for one of the three exact assertion kinds. A target kind without a governed content-addressed carrier or resolution profile is unavailable at the domain gate even if authorization returned `ALLOW`. The runtime cannot invent a carrier, use a mutable latest lookup, or coerce another family.

---

## 7. Companion-effect boundary

This contract's own result cardinality is exactly one `ReviewDecision`. That is not a transaction-wide prohibition on every other governed record.

`resultingAcceptedConsequenceBindings` is absent for standalone validation. It may be present only when:

1. a separate accepted-consequence contract owns and validates each companion consequence;
2. each companion effect has its own valid authority and intent binding;
3. a separately reviewed enclosing composition binding pins both contracts, intents, and result digests before commit;
4. `resultingAcceptedConsequenceBindings` is an exact copy of the companion results selected by that binding; and
5. failure of either contract aborts the composed commit.

This candidate defines only the ReviewDecision side of that interface. It does not create a generic composition contract or authorize a consequence. Without the separate binding, a non-empty companion list or inserted consequence is an unbound effect and fails.

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
| `RD_TARGET_FAMILY` | target kind plus immutable resolved bytes | closed section 6 derivation to `reviewedArtifactFamily` |
| `RD_TARGET_REF` | intent `PRIMARY_RECORD.resourceRef` | exact copy to `reviewedArtifactRef` |
| `RD_TARGET_BINDING` | intent target revision/digest | exact tagged copy to `reviewedArtifactBinding` |
| `RD_SCOPES` | intent scopes | complete equality under the intent schema's declared array/set posture |
| `RD_ACTION` | selected action rule and intent action | both must agree; exact copy to `reviewAction` |
| `RD_OUTCOME` | intent outcome | exact section 9 branch value |
| `RD_DECIDING_PARTY` | selected authority subject in finalization evidence | exact copy to `decidedByPartyRef` |
| `RD_HUMAN` | authenticated natural-person principal | exact copy to `decidedByHumanPrincipalRef` |
| `RD_FINALIZATION_EVIDENCE` | trusted finalization-evidence binding | exact copy to `finalizationEvidenceBinding` |
| `RD_TIME` | trusted human-act time | exact copy to `decidedAt` |
| `RD_RATIONALE` | intent rationale | exact Unicode value; no normalization or summarization |
| `RD_EVIDENCE` | intent evidence bindings | complete exact array; no addition, omission, or ref-only downgrade |
| `RD_PRIOR_DECISION` | optional intent lineage binding | exact copy or required absence |
| `RD_COMPANION_CONSEQUENCES` | separately reviewed composition binding | exact companion array under section 7 or required absence |

Every mapping receives one explicit disposition. A missing, duplicated, ambiguous, type-invalid, or conflicting authoritative source fails the contract.

### 8.3 Permitted derivations

These are the only permitted derivations:

| Derived value | Exact source and rule |
|---|---|
| `schemaVersion` | constant from the selected result-schema binding |
| `reviewedArtifactFamily` | section 6 map, confirmed against immutable target bytes |
| canonical scope representation | only a transformation explicitly fixed by the intent schema's declared set/array posture; otherwise exact copy |
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

Every other pairing fails. The combined reject-or-contest action is not split; the human-bound intent selects one closed outcome before authorization. `REVIEW_REQUEST` / `REVIEW_REQUESTED` is outside this contract.

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
| `PC_NO_UNBOUND_EFFECT` | no target rewrite, consequence, event envelope, materialization, promotion record, or other governed effect is inserted or changed without its own reviewed binding |
| `PC_COMPANION_BINDING` | every optional consequence link exactly matches a separately validated composed result under section 7 |
| `PC_NO_CURRENT_STATE` | this contract writes no current-state materialization |
| `PC_ATOMIC_EVIDENCE` | the shared transaction gate reports atomic commit of the decision, any bound composed results, passing evidence, and single-use consumption |
| `PC_UNIQUE_ID` | a duplicate decision ID with different bytes is rejected |

### 11.2 Branch postconditions

| Postcondition ID | Branch-specific meaning |
|---|---|
| `PC_ACCEPT` | acceptance is recorded for the exact target; any consequence remains separately bound and governed |
| `PC_REJECT` | rejection is recorded without deleting the target or creating a contrary accepted state |
| `PC_CONTEST` | contested posture is explicit and is not treated as accepted, rejected, or resolved |
| `PC_SUPERSEDE` | supersession is recorded without rewriting prior history; downstream freshness is re-evaluated separately |

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
- one `PASS`, `FAIL`, or legitimate `NOT_APPLICABLE` disposition for every `RD_*` mapping;
- one such disposition for every `PC_*` postcondition;
- source/destination selectors or pointers and compared digests;
- associated act family and record commit class; and
- an overall `PASS` or `FAIL` disposition.

A required item cannot be `NOT_APPLICABLE`. Overall `PASS` requires every required mapping and postcondition to pass. The trace itself is immutable and content-addressed under the separately reviewed shared evidence envelope; until that envelope exists with a real ref/digest, no executable binding exists.

This section owns the ReviewDecision-specific validation payload. It does not restate generic challenge, receipt, retention, transaction sequencing, or persistence machinery.

---

## 13. Validation and failure semantics

Before commit, the protected-effect gate must:

1. verify the selected action rule's exact intent, result-schema, and contract bindings;
2. validate the proposed result against the selected future v0.2 schema;
3. evaluate every applicable `RD_*` mapping and `PC_*` postcondition; and
4. supply an overall passing immutable trace to the shared atomic transaction gate.

If any item fails, no ReviewDecision or companion effect commits and single-use consumption does not commit. The existing authorization result remains its authority-gate result; `ALLOW` is not rewritten to `DENY` or treated as proof that the domain gate passed.

This candidate states only those ReviewDecision-specific preconditions and effects. It does not implement or redefine the generic transaction manager.

---

## 14. Production-reachable hostile cases

| Case | Required disposition |
|---|---|
| any invalid action/outcome pair | branch mapping fails; no decision commits |
| intent binds `REJECTED` but result says `CONTESTED`, or vice versa | `RD_OUTCOME` fails without changing intent or authorization result |
| target kind/ref/revision/digest is substituted | target mapping fails |
| caller uses coarse `ASSERTION_RECORD` as an intent alias | `RD_TARGET_KIND` fails |
| target carrier is unsupported, unresolved, mutable, or inconsistent with its kind | `RD_TARGET_FAMILY` or binding fails |
| `EVIDENCE_SUFFICIENCY_CASE` is used by `REVIEW_SUPERSEDE` or before the PR #11 prerequisite is approved | action-rule/target eligibility fails |
| a case target for accept/reject is omitted or substituted by the evaluator | authorization extractor conformance fails; no domain result commits |
| one scope is added, dropped, or changed outside declared schema posture | `RD_SCOPES` fails |
| deciding Party is replaced by the human principal for represented action | `RD_DECIDING_PARTY` fails |
| human principal is replaced by an organization, sponsor, or agent | `RD_HUMAN` fails |
| finalization evidence is missing, mutable, or substituted | `RD_FINALIZATION_EVIDENCE` fails |
| request, caller, or commit time replaces trusted human-act time | `RD_TIME` fails |
| rationale differs by whitespace, case, translation, or summarization | `RD_RATIONALE` fails |
| evidence binding is changed, omitted, added, or reordered contrary to schema posture | `RD_EVIDENCE` fails |
| prior-decision lineage is added, removed, or replaced | `RD_PRIOR_DECISION` fails |
| consequence is created without separate authority, contract validation, and composition binding | `PC_NO_UNBOUND_EFFECT` fails |
| companion list differs from the composed result digests | `RD_COMPANION_CONSEQUENCES` / `PC_COMPANION_BINDING` fails |
| target or prior decision is mutated or deleted | `PC_INPUTS_IMMUTABLE` fails |
| contract writes current state or treats acceptance as automatic promotion | `PC_NO_CURRENT_STATE` fails |
| ReviewDecision is retyped as an event envelope or assigned an event family field | `PC_CLASSIFICATION` fails |
| associated act is not `GovernanceEvent` or record class is not `governance decision` | `PC_CLASSIFICATION` fails |
| contract, schema, intent, result, or resolved-input digest changes | binding or mapping fails |
| one required mapping/postcondition disposition is missing | overall trace cannot pass |
| duplicate decision ID resolves to different bytes | `PC_UNIQUE_ID` fails |
| relevant state changes between validation and atomic commit | shared transaction gate fails and requires re-evaluation |
| domain failure rewrites authorization `ALLOW` | conformance failure; authorization evidence remains unchanged |

Fixtures must enter through the production result builder, contract validator, and transaction boundary rather than unit-only helpers.

---

## 15. Migration and currentness

`ReviewDecision v0.1` remains current/default until a separately governed promotion says otherwise. Existing records and examples remain v0.1 history.

A v0.1 record cannot claim v0.2 strength unless immutable source evidence establishes every required field and mapping. Missing target revision, actor/finalization evidence, rationale, evidence revision, decision-time basis, outcome intent, or companion binding cannot be guessed.

Draft schema or contract presence changes no currentness. Later promotion must preserve links to v0.1 history rather than rewrite it.

---

## 16. Later `AuthorizationPolicyBundle v0.2` binding

This PR does not create or edit the policy bundle.

After renewed PR #11 approval and separate materialization of real domain-contract, result-schema, and shared-trace bytes, the bundle PR must:

1. bind the exact contract ID/version/ref/digest and owning family;
2. bind the exact result-schema ref/version/digest;
3. bind the exact intent/result selector pointers for every `RD_*` mapping;
4. bind the reviewed contract to the three final-review action rules;
5. preserve the action-specific case-target policy split from PR #11;
6. exclude `REVIEW_REQUEST` from this final-decision contract; and
7. include every binding in the affected complete per-action `ruleDigest` closure.

The bundle cannot point at this prose file as an executable contract.

---

## 17. Traceability to issue #15

| Acceptance criterion | Disposition |
|---|---|
| inventory v0.1 capabilities and gaps | section 4 |
| decide whether a minimal v0.2 carrier is required | sections 4.3 and 5 |
| exact action/result constraints | section 9 |
| bind ID, target, scopes, human/Party posture, rationale, evidence, time, lineage, and companions | sections 5 through 8 |
| enumerate permitted derivations | section 8.3 |
| forbid substitution, unbound consequence creation, mutation, and promotion shortcuts | sections 7, 11, 13, and 14 |
| separate `GovernanceEvent` act from `governance decision` record | section 10 |
| content-address contract and deterministic digest projection | sections 8.1 and 12.1 |
| immutable mapping/postcondition trace with required digests | section 12.2 |
| validate before atomic commit without rewriting authorization | section 13 |
| production-reachable hostile cases | section 14 |
| later bundle registration without creating it here | section 16 |

---

## 18. Steward approval card

| Decision | Proposed answer | Approval required |
|---|---|---|
| Is a future `ReviewDecision v0.2` carrier required? | yes | yes |
| Does this contract cover exactly the three final review actions? | yes | yes |
| Does it validate exactly one ReviewDecision while allowing only separately bound companion effects? | yes | yes |
| Must the PR #11 case-target amendment receive renewed approval first? | yes | yes |
| Are case targets eligible only for accept and reject-or-contest under the proposed action split? | yes | yes |
| Are target kind/ref/binding and domain-family resolution exact? | yes | yes |
| Are action/outcome pairs fixed exactly by section 9? | yes | yes |
| Must reject versus contest be intent-bound? | yes | yes |
| Are deciding Party, authenticated human, and immutable finalization evidence separate fields? | yes | yes |
| Is `decidedAt` the trusted human-act time? | yes | yes |
| Are rationale, scopes, evidence, and lineage exact rather than defaulted? | yes | yes |
| May consequence links exist only under the separately governed composition in section 7? | yes | yes |
| Is the act `GovernanceEvent` while the record class is `governance decision`? | yes | yes |
| Must every `RD_*` and `PC_*` item have an explicit trace disposition? | yes | yes |
| Does protected-effect failure leave authorization evidence unchanged? | yes | yes |
| Do schema, shared evidence, bundle binding, conformance, acceptance, and promotion remain separate PRs? | yes | yes |

Any requested authorization, consequence-contract, generic composition, shared-evidence, runtime, or currentness change must remain in its own trust-boundary PR.

---

## 19. Staged delivery and completion

1. **Authorization prerequisite:** obtain renewed semantic approval for PR #11 head `5974bb9`.
2. **Phase A domain approval:** approve or amend this one-file ReviewDecision candidate.
3. **Domain materialization:** separately create the non-default machine contract, exact selectors, and `ReviewDecision v0.2` schema.
4. **Shared evidence materialization:** separately create the finalization-evidence, validation-trace envelope, and governed-effect receipt profiles.
5. **Optional composition closure:** if atomic companion consequences are implemented, separately review their authorization, contract, and composition binding.
6. **Bundle binding:** separately bind exact reviewed bytes into `AuthorizationPolicyBundle v0.2`.
7. **Hostile conformance:** exercise section 14 through production-reachable paths.
8. **Acceptance and promotion:** accept exact bytes and change current/default status only through separate governed steps.
9. **OFARM2 extraction:** consume only promoted, digest-verified canonical bytes.

Phase A is complete when issue #15's criteria are reviewed, the PR #11 prerequisite is approved, and this PR still changes only this non-authoritative candidate file.

What is next: renewed authorization review on PR #11 and steward re-review of this bounded ReviewDecision candidate before any schema or executable-contract work.
