# OFARM AssertionRecord Submission Protected-Effect Contract v0.1

Date: 2026-09-03<br>
Status: Phase A candidate for `samovers/OFARM#22`; non-authoritative, not accepted law, and not a current/default machine contract<br>
Parent inventory: `samovers/OFARM#12`<br>
Depends on: the approved authorization candidate on issues #16 and #18 / PR #11 at `03a21f669ee04f96d444e14f00ae7212cab04803`, and the approved governed human-approval transaction candidate on issue #19 / PR #20 at `98f8c4fafbae42c8f7fd931f43f53adcb4733713`<br>
Blocking prerequisite: PR #20 closes the shared transaction protocol only for fresh approval and direct human final action; `ASSERT_OPERATION_CLAIM` remains non-executable until a separate transaction profile closes the `NOT_REQUIRED` finalization mode selected by PR #11<br>
Scope: define the AssertionRecord-specific mapping from one authorized assertion-submission intent to one immutable pending-review AssertionRecord

---

## 1. Decision requested

Stewards are asked to approve, reject, or amend these bounded decisions:

1. this contract validates exactly one new `AssertionRecord` for `ASSERT_STRUCTURE`, `ASSERT_OPERATION_CLAIM`, or `ASSERT_COMPLIANCE`;
2. the action fixes the result subtype: `STRUCTURE_ASSERTION`, `OPERATION_CLAIM_ASSERTION`, or `COMPLIANCE_ASSERTION` respectively;
3. every result created through these submission actions has `claimState` exactly `PENDING_REVIEW`;
4. fresh approval for structure or compliance authorizes submission of the exact assertion only; it does not accept the claim or make it current truth;
5. the result preserves the exact proposed ID, typed subject, sole anchor scope, asserting Party, assertion time, subject time, typed body, evidence, and branch-specific provenance or compliance basis;
6. for an operation claim, the current reporter remains separate from the alleged performer and performer authority remains `NOT_EVALUATED_BY_AUTHORIZATION`;
7. the governed acts have primary event families `StructureEvent`, `InterventionEvent`, and `GovernanceEvent` for structure, operation, and compliance submission respectively, while the records have commit classes `STRUCTURE_ASSERTION`, `OPERATION_CLAIM`, and `COMPLIANCE_ASSERTION`;
8. this contract creates no accepted structural state, accepted executed intervention consequence, compliance fact, ReviewDecision, SemanticEventEnvelope, current-state materialization, or mutation of prior history;
9. a narrow future `AssertionRecord v0.2` carrier is required because v0.1 cannot carry immutable subject, scope, evidence, body, temporal, and branch-specific bindings without relying on a competing sidecar description; and
10. a mapping or postcondition failure aborts the assertion effect without rewriting the prior authorization result.

The event-family choices for structure and compliance assertion submission are explicit Phase A proposals. The active Event Grammar supplies the families and selection rule but no repository ingress example currently closes those two mappings. Approval of this candidate approves those mappings for this contract; rejection requires a separate Event Grammar amendment or a revised candidate before machine materialization.

Approval of this candidate authorizes no schema, runtime, currentness, accepted-RFC, or promotion change.

---

## 2. Primary trust boundary and PR boundary

The primary trust boundary is **AssertionRecord submission semantics and commit classification**.

This candidate owns only:

- the v0.1 capability/gap inventory and minimum future carrier delta;
- the exact action-to-assertion-subtype mapping;
- exact intent-to-result mappings and permitted derivations;
- assertion-specific actor, temporal, subject, scope, evidence, and branch constraints;
- assertion-specific forbidden widening and postconditions;
- separation of the governed act from the committed assertion record; and
- the AssertionRecord-specific payload of the protected-effect validation trace.

This PR adds only this candidate in the historical phase-report lane. It does not own or change:

- authorization, grants, delegation, actor resolution, sharing, or revocation;
- generic transaction coordination, approval, finalization evidence, consumption, receipts, retention, encryption, or key custody;
- review, acceptance, supersession, accepted-consequence, or current-state semantics;
- generic event ingress, Event Grammar vocabulary, or a SemanticEventEnvelope contract;
- assertion body vocabularies for every domain or pack;
- current schemas, accepted RFCs, machine manifests, current/default indexes, runtime implementation, or currentness; or
- OFARM2 implementation.

If implementation needs a new authorization target, action, effect-intent field that changes eligibility, event family, commit class, transaction mode, review effect, evidence-retention rule, or current-state rule, work stops before that boundary and proceeds through a separate issue and PR.

---

## 3. Governing inputs and stop conditions

This candidate is constrained by:

- Constitution RC2.1 sections 7.24 through 7.25, 10.1 through 10.3, 10.10a, and 10.11;
- the accepted Source Truth Record Closure RFC v0.1;
- the Event Grammar and Commit Matrix v0.1;
- the accepted Event Ingress and Promotion Boundary Closure RFC v0.1;
- the Temporal Field Conformance Matrix v0.1;
- the accepted Quantity-Bearing Intervention and As-Applied RFC v0.1;
- current `AssertionRecord v0.1` and its ten repository examples;
- the protected-effect inventory on issue #12;
- the approved PR #11 action rows, exact effect-intent profiles, one-target `RP_SCOPE_ONE` resource policy, authority-subject semantics, and protected-effect handoff at `03a21f6`; and
- the approved PR #20 transaction protocol at `98f8c4f`, only for the finalization modes it actually covers.

The exact PR #11 head authorizes assertion submission and binds the whole effect intent. It does not authorize acceptance or define this result. A semantic change to that head invalidates this candidate's authorization dependency before schema or executable-contract materialization.

The materialization step must stop and return to a separate boundary when any of these conditions is found:

- the exact result cannot be built from one validated, digest-bound effect intent plus trusted transaction facts;
- an assertion subject or body field changes authorization eligibility but is absent from the approved authorization-relevant field set;
- the sole `RP_SCOPE_ONE` target cannot map completely to one immutable result anchor scope;
- a requested assertion body needs another result family or an implicit accepted consequence;
- the proposed event-family mapping is not accepted under the active Event Grammar;
- generic evidence, retention, approval, or transaction machinery must change; or
- the `NOT_REQUIRED` transaction path for `ASSERT_OPERATION_CLAIM` remains unclosed.

This document may identify those dependencies. It cannot repair them locally.

---

## 4. Current `AssertionRecord v0.1` inventory

### 4.1 Capabilities and gaps

| Current field or behavior | v0.1 capability | Gap and Phase A disposition |
|---|---|---|
| `schemaVersion` | identifies `ofarm.assertionrecord.v0.1` | future carrier needs a distinct `ofarm.assertionrecord.v0.2` branch |
| `assertionRecordId` | stable logical assertion ID | retain and bind exactly to the prospective effect subject and result digest |
| `assertionType` | six assertion subtypes | `NARROWING`: this contract admits only structure, operation-claim, and compliance results |
| `subject` | one type and logical ref | retain logical identity and add explicit existing/prospective posture plus an immutable selector for an existing subject |
| `anchorScopes` | one or more type/ref pairs | close new v0.2 submissions to exactly one immutable anchor-scope binding from `RP_SCOPE_ONE` |
| `assertedByPartyRef` | accountable asserting Party | retain and bind to the selected path-specific authority subject, not an approver or alleged performer |
| `assertedAt` | one date-time | retain and bind to trusted protected-effect commit time; never copy `subjectTime` |
| `occurrenceTime`, `effectiveFrom`, `effectiveUntil` | optional flat temporal fields | replace for new v0.2 results with one exact schema-bound `subjectTime` value copied from the intent; do not guess a legacy projection |
| `evidenceRefs` | one or more logical refs | replace with a non-empty array of immutable typed evidence bindings |
| `provenanceRefs` | optional logical refs | replace loose provenance with branch-specific immutable bindings; do not preserve an untyped catch-all array |
| `claimState` | five postures, including `PENDING_REVIEW` and `IN_FORCE` | fix new results from these submission actions to `PENDING_REVIEW` |
| `supersedesAssertionRecordRef`, `supersededByReviewDecisionRef` | optional logical lineage | require absence on initial v0.2 submission; later governed review and lineage remain separate effects |
| `benefitingPartyRef` | optional Party ref | require absence unless a future digest-bound domain amendment defines its exact meaning and mapping |
| `notes` | arbitrary optional prose | replace with the exact typed assertion body; no result-local notes side channel |
| payload ref arrays | optional loose intervention/execution refs | permit only exact immutable payload bindings inside the typed operation-claim body |
| tenant/twin and finalization metadata | absent | keep authorization-only tenant/twin, challenge, approver, and finalization details in authorization/finalization evidence and the receipt rather than duplicating them in domain truth |
| classification and integrity | absent | bind event family, commit class, schema, contract, result, and trace digests outside result-local choice |

### 4.2 Example coverage

The repository has ten current `AssertionRecord v0.1` examples:

- one structure assertion, in `PENDING_REVIEW`;
- five operation-claim assertions, one in `PENDING_REVIEW` and four in `IN_FORCE`;
- three compliance assertions, two in `PENDING_REVIEW` and one in `IN_FORCE`; and
- one `LOT_ASSERTION`, in `IN_FORCE`, which is outside this contract.

All ten use `notes` as at least part of the human-readable claim content. All use logical evidence refs, six use logical provenance refs, and one operation claim uses a loose `executionRecordPayloadRefs` entry. No example carries an immutable subject selector, exact body schema binding, effect-intent digest, or protected-effect trace.

The existing `IN_FORCE` examples remain valid v0.1 history. They are not retroactively relabeled, rejected, or used as precedent for direct in-force creation under v0.2.

### 4.3 Carrier decision

A narrow future `AssertionRecord v0.2` carrier is required. A sidecar around v0.1 would leave the history-bearing assertion unable to state the exact body, subject and scope revisions, subject time, evidence revisions, and operation/compliance branch facts that the sidecar claims to validate.

The future carrier is a versioned extension. Existing v0.1 records remain valid v0.1 history and do not silently acquire v0.2 proof strength. No schema is created or edited in this PR.

---

## 5. Minimum future `AssertionRecord v0.2` carrier

### 5.1 Common fields

| Field | Required meaning |
|---|---|
| `schemaVersion` | exactly `ofarm.assertionrecord.v0.2` |
| `assertionRecordId` | exact proposed assertion ID |
| `assertionType` | exact action-derived subtype from section 7 |
| `subject` | exact typed logical subject with `EXISTING_SUBJECT` or `PROSPECTIVE_SUBJECT` posture and section 5.2 selector rules |
| `anchorScopes` | exactly one immutable scope binding copied from the sole `RP_SCOPE_ONE` `TARGET_SCOPE` |
| `assertedByPartyRef` | exact selected path-specific `authoritySubjectPartyRef` |
| `assertedAt` | trusted protected-effect commit time |
| `subjectTime` | exact schema-bound domain time from the validated intent; its shape is pinned by the action's intent/result schema pair |
| `assertionBody` | exact action-typed body copied from the validated intent |
| `evidenceBindings` | non-empty array of exact immutable evidence bindings copied from the validated intent |
| `subjectScopeProofBindings` | exact immutable relationship-proof bindings when subject-to-anchor equality alone does not establish the relationship; otherwise required absent |
| `claimState` | exactly `PENDING_REVIEW` |
| `operationClaimContext` | required only for `OPERATION_CLAIM_ASSERTION`; section 5.3 |
| `complianceBasis` | required only for `COMPLIANCE_ASSERTION`; section 5.4 |

Every object and branch rejects unknown properties. A field not admitted by its branch is absent, not `null`, empty, or populated with a placeholder.

The materialized contract binds one exact body-schema ref/version/digest for each assertion subtype. The review keys are `STRUCTURE_ASSERTION_BODY_V0_2`, `OPERATION_CLAIM_BODY_V0_2`, and `COMPLIANCE_ASSERTION_BODY_V0_2`; they are not mutable runtime registry entries and this candidate does not create their bytes.

### 5.2 Immutable binding and subject rules

An immutable binding contains one logical ref and exactly one immutable revision ref or `sha256:` content digest. Its exact kind is fixed by the containing field or an explicit closed kind discriminator. Every revision ref must resolve to immutable bytes, and the validation trace records the digest of those bytes.

`subject` has two closed postures:

| Posture | Required content and meaning |
|---|---|
| `EXISTING_SUBJECT` | exact `subjectType`, `subjectRef`, and exactly one immutable revision ref or content digest |
| `PROSPECTIVE_SUBJECT` | exact `subjectType` and proposed `subjectRef`; no revision/digest selector; the assertion records a claim about the proposed subject but does not create it |

The action-bound body schema closes the permitted `subjectType` values. This candidate does not enlarge the current domain vocabulary or let a caller supply an unregistered type. A prospective subject cannot be represented as existing, and an assertion about it cannot create durable identity or structural current state.

`anchorScopes` contains exactly one entry because all three approved action rows select `RP_SCOPE_ONE`, whose sole `TARGET_SCOPE` has cardinality one. The entry carries the exact scope kind, logical ref, and one immutable selector from the validated resource view. No ancestor, descendant, tenant, deployment, or convenient display scope may be added to the result.

When subject and anchor scope do not have the same exact identity and immutable revision, the validated intent must supply the complete immutable relationship proof selected by the action-bound body schema. The contract validates that relationship without treating it as another authority target. If the relationship cannot be proven, the assertion does not commit.

### 5.3 Operation-claim context

`operationClaimContext` contains:

- `claimPosture`, exactly `INTENDED` or `PERFORMED` as bound by `EI_OPERATION_ASSERTION_V0_2`;
- required `performedByPartyRef`, copied exactly from the intent and retained as claim provenance;
- `softwareAgentActorshipBindings`, required and non-empty only when `claimPosture` is `PERFORMED` and the claim alleges software-agent performance, otherwise absent; and
- `performerAuthorityEvidenceBindings`, optional only for `PERFORMED`, otherwise absent.

Each binding is immutable under section 5.2. Optional performer-authority evidence is evidence claimed by the reporter; its presence is not an authorization result and its absence cannot be filled from the reporter's path.

For `INTENDED`, the upstream-required `performedByPartyRef` identifies the Party named to perform the intended work; it does not assert that performance occurred. For `PERFORMED`, it identifies the alleged performer. The field name cannot upgrade either claim posture.

The current authorization path answers only whether the reporter may submit the operation claim. The selected `authoritySubjectPartyRef` maps to `assertedByPartyRef`; it never maps to `performedByPartyRef`. The authorization trace records performer authority as `NOT_EVALUATED_BY_AUTHORIZATION`. Evidence sufficiency, review, and promotion decide whether any claimed performance may later yield an accepted execution consequence.

An operation body may include intervention-intent or execution-record payload bindings only as exact immutable bindings covered by `effectIntentDigest`. A loose ref, latest-version lookup, or payload inserted after authorization fails.

### 5.4 Compliance basis

`complianceBasis` contains two non-empty arrays copied exactly from `EI_COMPLIANCE_ASSERTION_V0_2`:

- `ruleRevisionBindings`; and
- `evidencePolicyRevisionBindings`.

Each entry is immutable under section 5.2. The bound rules and policies identify what the assertion claims against; they do not prove that the claim is correct, that required evidence passed, or that a compliance fact exists.

Compiled outputs may be immutable evidence or intent inputs. They cannot replace `assertionBody`, select a different claim, or become the result. `EP_COMPLIANCE_ASSERTION_V0_2` remains a separately owned action evidence policy; this contract consumes its applicable gate disposition without copying that policy's evaluation rules.

### 5.5 Fields deliberately not copied

The result does not duplicate:

- `effectIntentDigest`, authorization rules, grants, roles, path candidates, or authority snapshots;
- tenant/twin authorization context that is not itself the assertion's typed subject or sole anchor scope;
- an agent sponsor, authenticated principal, human approver, challenge, display, finalization evidence, or consumption record;
- a generic provenance array, arbitrary notes, mutable URLs, or unversioned payload refs; or
- review, acceptance, supersession, materialization, or currentness fields.

Those facts remain in their owning immutable evidence, receipt, intent, or downstream domain records. The governed-effect receipt and validation trace bind the assertion result back to the exact intent, authorization, contract, finalization mode, and transaction evidence without making the AssertionRecord a second authorization ledger.

---

## 6. Actor and temporal ownership

### 6.1 Asserting Party

`assertedByPartyRef` is the `authoritySubjectPartyRef` from the one canonical sufficient authorization path selected under PR #11:

- for natural-person self action, it is that person's Party;
- for represented action, it is the represented Party;
- for a directly granted agent action, it is the recognized agent Party; and
- for explicitly delegated agent action, it is the represented Party selected by that path.

A sponsor, human approver, authenticated principal acting in representation, alleged performer, benefiting Party, compiled-output author, or caller-supplied mirror cannot replace it.

For `ASSERT_STRUCTURE` and `ASSERT_COMPLIANCE`, PR #11 requires fresh human approval for every invocation. A direct natural-person invocation still uses the governed fresh-approval lifecycle; an agent path requires an independently eligible natural-person approver for the same exact action and effect intent through PR #20. The approver is not thereby the asserting Party, and the approval does not change `claimState`.

### 6.2 Distinct times

This contract preserves these separate facts:

- `subjectTime`: when the asserted structural condition, intended/performed operation, or compliance condition applies;
- source capture or evidence times: retained in immutable evidence or payload bytes;
- `humanActedAt`, where fresh approval applies: retained in finalization evidence;
- `authorizationEvaluatedAt`: retained in authorization evidence;
- `assertedAt`: the trusted `effectCommittedAt` at which the assertion enters canonical history; and
- ingress receipt/processing times: retained by the separate event-ingress records where applicable.

`assertedAt` is never copied from caller time, `subjectTime`, evidence capture time, or `humanActedAt`. `subjectTime` is never replaced by `assertedAt`. Delayed sync preserves both even when the asserted occurrence predates platform receipt by a long interval.

The future intent and result schemas must pin an exact branch-specific `subjectTime` shape. Until those bytes exist and are reviewed, no executable contract may infer whether a value is an instant, interval, effective window, intended window, performed interval, or compliance as-of time.

---

## 7. Contract identity and exact action closure

### 7.1 Contract identity

| Property | Closed value |
|---|---|
| contract ID | `ofarm.protectedeffect.assertionrecord.submit.v0.1` |
| contract version | `0.1` |
| owning domain family | `ASSERTION_RECORD_SUBMISSION` |
| intent profiles | `EI_STRUCTURE_ASSERTION_V0_2`, `EI_OPERATION_ASSERTION_V0_2`, `EI_COMPLIANCE_ASSERTION_V0_2` |
| result carrier | future `ofarm.assertionrecord.v0.2` submission branches |
| own result cardinality | exactly one immutable `AssertionRecord` |
| canonicalization | `JCS_RFC8785_SHA256` |

The materialized contract must bind the exact intent-schema and result-schema refs, versions, and digests plus the three exact body-schema bindings, mappings, derivations, forbidden-widening rules, classifications, postconditions, and trace requirements below.

### 7.2 Exact action, effect-subject, result, and classification map

| Authorized action | Required intent profile | Required effect-subject kind | Required `assertionType` | Primary event family | Record commit class |
|---|---|---|---|---|---|
| `ASSERT_STRUCTURE` | `EI_STRUCTURE_ASSERTION_V0_2` | `STRUCTURE_ASSERTION` | `STRUCTURE_ASSERTION` | `StructureEvent` | `STRUCTURE_ASSERTION` |
| `ASSERT_OPERATION_CLAIM` | `EI_OPERATION_ASSERTION_V0_2` | `OPERATION_ASSERTION` | `OPERATION_CLAIM_ASSERTION` | `InterventionEvent` | `OPERATION_CLAIM` |
| `ASSERT_COMPLIANCE` | `EI_COMPLIANCE_ASSERTION_V0_2` | `COMPLIANCE_ASSERTION` | `COMPLIANCE_ASSERTION` | `GovernanceEvent` | `COMPLIANCE_ASSERTION` |

The `OPERATION_ASSERTION` to `OPERATION_CLAIM_ASSERTION` mapping is deliberate: the first is the approved authorization effect-subject token, while the second is the current AssertionRecord subtype. Neither may be used as a free alias outside this row.

Every other action, intent profile, effect-subject kind, subtype, event family, or commit class fails this contract. `OBSERVATION_ASSERTION`, `LOT_ASSERTION`, and `OTHER_ASSERTION` remain valid v0.1 history but are not new-result branches here.

### 7.3 Classification meaning

The primary event family classifies the dominant semantics of the governed assertion-submission act and its claimed domain context:

- a structure submission is associated with `StructureEvent` but does not itself create or change durable structure;
- an intended or performed operation claim is associated with `InterventionEvent` but does not prove execution; and
- a formal compliance assertion submission is associated with `GovernanceEvent` but does not create a compliance fact.

The immutable AssertionRecord separately enters under its record commit class. Event family and commit class are not interchangeable and neither is a caller-selected result field.

A `SemanticEventEnvelope`, `CommitIngressResult`, or `PromotionTrace`, when required by the active ingress path, is a separate governed record linked to the exact assertion and classification. This contract neither creates nor validates those records. Authorization/finalization evidence, the protected-effect trace, and the governed-effect receipt remain `EvidenceEvent` / evidence-record material under their owning contracts.

---

## 8. Exact intent-to-result mappings

### 8.1 Stable common mappings

| Mapping ID | Authoritative source | Result destination and rule |
|---|---|---|
| `AR_SCHEMA` | selected result-schema binding | `schemaVersion` is exactly `ofarm.assertionrecord.v0.2` |
| `AR_ACTION_PROFILE` | selected action rule and rule-bound intent schema | both must match one row in section 7.2 |
| `AR_EFFECT_SUBJECT` | intent effect subject | kind and proposed ID match section 7.2 and `assertionRecordId` exactly |
| `AR_ID` | intent proposed assertion ID | exact copy to `assertionRecordId` |
| `AR_TYPE` | section 7.2 action/effect-subject row | exact derived `assertionType`; no caller or result override |
| `AR_SUBJECT` | intent assertion-subject binding covered by `effectIntentDigest` | exact copy to `subject`, including posture and conditional immutable selector |
| `AR_SCOPE` | sole rule-extracted `RP_SCOPE_ONE` `TARGET_SCOPE` | exact one-element mapping to `anchorScopes`, including kind, ref, and immutable selector |
| `AR_SUBJECT_SCOPE_PROOF` | intent relationship-proof bindings, conditional under section 5.2 | exact copy or required absence, followed by relationship validation |
| `AR_ASSERTOR` | canonical selected path's `authoritySubjectPartyRef` | exact copy to `assertedByPartyRef` |
| `AR_ASSERTED_AT` | trusted final transaction `effectCommittedAt` | exact copy to `assertedAt` |
| `AR_SUBJECT_TIME` | intent `subjectTime` | exact schema-preserving copy; no temporal substitution or normalization |
| `AR_BODY` | intent action-typed assertion body | exact complete copy to `assertionBody`; no summarization, compilation replacement, or notes side channel |
| `AR_EVIDENCE` | intent evidence revision bindings | exact complete non-empty array in `evidenceBindings`; no addition, omission, mutable ref, or ref-only downgrade |
| `AR_CLAIM_STATE` | contract constant | exactly `PENDING_REVIEW` |

Every mapping receives one explicit disposition. A missing, duplicated, ambiguous, type-invalid, mutable, unresolved, or conflicting authoritative source fails the contract.

### 8.2 Branch mappings

| Mapping ID | Branch | Source and result rule |
|---|---|---|
| `AR_OPERATION_POSTURE` | operation only | exact copy of intent `claimPosture` to `operationClaimContext.claimPosture` |
| `AR_OPERATION_PERFORMER` | operation only | exact copy of intent `performedByPartyRef`; never derive from reporter or authority subject |
| `AR_OPERATION_AGENT_ACTORSHIP` | operation only | exact immutable array when posture is `PERFORMED` and the intent alleges agent performance; otherwise required absence |
| `AR_OPERATION_PERFORMER_AUTHORITY` | operation only | exact optional immutable array only for `PERFORMED`; trace retains `NOT_EVALUATED_BY_AUTHORIZATION` regardless of presence |
| `AR_OPERATION_PAYLOADS` | operation only | any admitted intent/execution payload bindings remain exact inside the typed body; otherwise required absence |
| `AR_COMPLIANCE_RULES` | compliance only | exact complete non-empty rule-revision array to `complianceBasis.ruleRevisionBindings` |
| `AR_COMPLIANCE_EVIDENCE_POLICY` | compliance only | exact complete non-empty evidence-policy-revision array to `complianceBasis.evidencePolicyRevisionBindings` |
| `AR_STRUCTURE_BRANCH_ABSENCE` | structure only | `operationClaimContext` and `complianceBasis` are absent |
| `AR_OPERATION_BRANCH_ABSENCE` | operation only | `complianceBasis` is absent |
| `AR_COMPLIANCE_BRANCH_ABSENCE` | compliance only | `operationClaimContext` is absent |
| `AR_LEGACY_ABSENCE` | all branches | `benefitingPartyRef`, flat legacy time fields, loose provenance/payload refs, both supersession refs, and `notes` are absent |

### 8.3 Permitted derivations

These are the only permitted derivations:

| Derived value | Exact source and rule |
|---|---|
| `schemaVersion` | constant from the selected result-schema binding |
| `assertionType` | section 7.2 action/effect-subject map |
| `claimState` | contract constant `PENDING_REVIEW` |
| associated primary event family | section 7.2 action map, recorded outside result-local choice |
| record commit class | section 7.2 action map, recorded outside result-local choice |
| canonical result and resolved-input digests | shared JCS/SHA-256 profile over exact validated or resolved bytes |

Everything else is an exact copy, a contract-validated relationship, a trusted transaction fact, or required absence. There is no default subject, scope, actor, subject time, body, evidence, performer, compliance basis, lineage, current state, or accepted consequence. There is no local sorting, name search, family coercion, latest-revision lookup, body compilation, or generated companion ID.

---

## 9. Forbidden widening and companion-effect boundary

This contract's own domain result cardinality is exactly one new AssertionRecord. Transaction evidence required by other contracts is not a second AssertionRecord or a companion domain effect.

The contract forbids:

- creating or mutating durable structure from a structure assertion;
- treating `INTENDED` as performed, or `PERFORMED` as accepted execution;
- creating an accepted executed intervention consequence from an operation claim;
- treating evidence, compiled output, or a passed evidence policy as a compliance fact;
- creating a ReviewDecision, accepted consequence, current-state materialization, or supersession effect;
- editing, deleting, relabeling, or replacing an earlier AssertionRecord, evidence item, payload, scope, subject, or rule revision;
- adding a second assertion, event envelope, or domain record because it seems implied by the body; and
- using fresh human approval as acceptance, attestation, performer-authority proof, or promotion.

If another governed result is needed, an enclosing composition must separately identify its authority basis, protected-effect contract, exact derivation, result digest, and atomicity rule. This candidate defines no such composition and recognizes no implicit companion domain result.

---

## 10. Assertion-specific postconditions

### 10.1 Common postconditions

| Postcondition ID | Required proposed-state condition |
|---|---|
| `PC_ONE_ASSERTION` | exactly one new assertion ID resolves to one schema-valid immutable result |
| `PC_VALIDATED_BYTES` | committed AssertionRecord bytes equal the bytes validated by this contract |
| `PC_INPUTS_IMMUTABLE` | subject, scope, proof, evidence, payload, rule, and evidence-policy inputs remain byte-identical |
| `PC_ACTION_TYPE` | action, intent profile, effect subject, assertion subtype, event family, and commit class match one section 7.2 row |
| `PC_PENDING_REVIEW` | result `claimState` is `PENDING_REVIEW`; no accepted or in-force result is emitted |
| `PC_SUBJECT_SCOPE` | subject posture is truthful and the subject is exactly equal to, or proven within the governed relation to, the sole anchor scope |
| `PC_ASSERTOR` | asserting Party is the canonical selected authority subject and is not substituted by an approver, sponsor, principal, performer, or beneficiary |
| `PC_TEMPORAL_SEPARATION` | trusted assertion time and intent-bound subject time are both preserved without forbidden substitution |
| `PC_NO_UNBOUND_EFFECT` | no prior record mutation, event envelope, review, consequence, materialization, or other governed result is inserted or changed without its own applicable authority and contract |
| `PC_NO_CURRENT_STATE` | this contract neither writes current state nor marks the assertion accepted solely because submission passed |
| `PC_TRANSACTION_HANDOFF` | the applicable transaction gate binds the exact passing result/trace and commits the effect, authorization/finalization evidence, receipt, and single-use consumption atomically |
| `PC_UNIQUE_ID` | a duplicate assertion ID with different bytes is rejected |

### 10.2 Branch postconditions

| Postcondition ID | Branch-specific meaning |
|---|---|
| `PC_STRUCTURE` | only a pending structure claim is created; no durable structure identity, revision, boundary, role, pack state, or current structural state changes |
| `PC_OPERATION` | claim posture, reporter, performer, agent actorship, performer-authority evidence, subject time, and payloads satisfy section 5.3; no execution is accepted |
| `PC_COMPLIANCE` | exact rules, evidence policies, evidence, subject time, and body satisfy section 5.4; no compliance fact or certification state is created |
| `PC_BRANCH_ABSENCE` | every field inapplicable to the selected branch is absent |

For `ASSERT_STRUCTURE` and `ASSERT_COMPLIANCE`, `PC_TRANSACTION_HANDOFF` relies on the PR #20 fresh-approval mode when that dependency is later materialized. For `ASSERT_OPERATION_CLAIM`, it cannot pass at an executable commit boundary until a separately reviewed `NOT_REQUIRED` transaction profile supplies the equivalent atomic handoff without inventing human approval.

---

## 11. Content addressing and validation trace

### 11.1 Digest closure

The machine contract's `contractDigest` is `sha256:` plus SHA-256 over RFC 8785 JCS bytes of the complete contract after removing exactly the top-level `/contractDigest` member. No nested or other top-level member is excluded.

`resultDigest` covers the complete schema-valid proposed AssertionRecord with no excluded member. `resultSchemaDigest` binds the exact selected result-schema bytes. Each action's intent-schema and body-schema digest binds its exact bytes. Every revision-ref resolution records the digest of the resolved immutable bytes.

These application rules do not create a competing generic digest framework. The later shared validation-trace and receipt profiles may carry these bindings by reference but cannot weaken or omit this contract's semantic closure.

### 11.2 Assertion validation payload

The immutable protected-effect validation trace must bind:

- authorization result/rule and effect-intent refs/digests;
- result ID/ref/digest and result-schema ref/version/digest;
- contract ID/version/ref/digest and selected action/body-schema binding;
- sole authority-target scope and every resolved subject, relationship-proof, evidence, payload, rule, and evidence-policy digest;
- one `PASS`, `FAIL`, legitimate `NOT_APPLICABLE`, or dependency-bound `NOT_EVALUATED` disposition for every `AR_*` mapping;
- one such disposition for every `PC_*` postcondition;
- source/destination selectors or pointers and compared digests;
- associated primary event family and record commit class;
- operation performer-authority disposition, exactly `NOT_EVALUATED_BY_AUTHORIZATION` for the operation branch; and
- an overall `PASS` or `FAIL` disposition.

`NOT_APPLICABLE` means that an item's contract-declared branch condition does not apply; a required item cannot use it. `NOT_EVALUATED` means no pass-or-fail conclusion was reached because a named prerequisite did not pass. A required dependent item may be `NOT_EVALUATED`, but that prevents overall `PASS`.

The materialized contract enumerates the prerequisite IDs for every dependency that can produce `NOT_EVALUATED`. A runtime cannot use it to suppress an independent failure or omit an evaluation arbitrarily. Overall `PASS` requires every required mapping and postcondition to pass. The trace itself is immutable and content-addressed under the separately reviewed shared evidence envelope; until that envelope exists with a real ref/digest, no executable binding exists.

This section owns only the AssertionRecord-specific validation payload. It does not restate generic approval, reservation, challenge, receipt, retention, transaction sequencing, or persistence machinery.

---

## 12. Validation and failure semantics

Before commit, the protected-effect gate must:

1. verify the selected action rule's exact effect-intent-schema and protected-effect-contract bindings;
2. load and digest-verify the referenced protected-effect contract;
3. verify the result-schema and selected body-schema refs, versions, and digests owned by that contract;
4. validate the proposed result against that exact result/body schema branch;
5. evaluate every applicable `AR_*` mapping and assertion-specific `PC_*` postcondition; and
6. supply an overall passing immutable trace to the applicable atomic transaction gate.

If any item fails, no AssertionRecord or companion domain effect commits and single-use consumption does not commit. The existing authorization result remains its authority-gate result; `ALLOW` is not rewritten to `DENY` or treated as proof that the domain gate passed.

An authorization `ALLOW` for `ASSERT_OPERATION_CLAIM` is not executable merely because this domain result validates. Until the separate `NOT_REQUIRED` transaction profile is approved and materialized, the transaction prerequisite remains absent and the operation has no compliant commit path.

This candidate states only AssertionRecord-specific preconditions and effects. It does not implement or redefine a transaction manager.

---

## 13. Production-reachable hostile cases

| Case | Required disposition |
|---|---|
| action, intent profile, or effect-subject kind is substituted | `AR_ACTION_PROFILE` or `AR_EFFECT_SUBJECT` fails; no assertion commits |
| `OPERATION_ASSERTION` is copied directly into `assertionType` instead of mapping to `OPERATION_CLAIM_ASSERTION` | `AR_TYPE` fails |
| observation, lot, other, or an unknown assertion subtype is offered through this contract | result-schema or `AR_TYPE` fails |
| proposed assertion ID differs between effect subject, intent, and result | `AR_EFFECT_SUBJECT` / `AR_ID` fails |
| duplicate assertion ID resolves to different bytes | `PC_UNIQUE_ID` fails |
| result uses `IN_FORCE`, `CONTESTED`, `REJECTED`, or `SUPERSEDED` | `AR_CLAIM_STATE` / `PC_PENDING_REVIEW` fails |
| fresh approval is treated as acceptance or a compliance fact | `PC_PENDING_REVIEW` / `PC_NO_CURRENT_STATE` fails |
| existing subject lacks exactly one immutable selector, or prospective subject carries one | `AR_SUBJECT` fails |
| prospective subject is treated as a created durable identity | `PC_STRUCTURE` or `PC_NO_UNBOUND_EFFECT` fails |
| a second anchor scope, ancestor, tenant, or display scope is added | `AR_SCOPE` fails |
| subject differs from anchor scope and relationship proof is missing, mutable, stale, or invalid | `AR_SUBJECT_SCOPE_PROOF` / `PC_SUBJECT_SCOPE` fails |
| asserted Party is replaced by human approver, authenticated representative, agent sponsor, performer, or beneficiary | `AR_ASSERTOR` fails |
| caller, evidence, subject, human-act, authorization, or ingress time replaces trusted `effectCommittedAt` | `AR_ASSERTED_AT` / `PC_TEMPORAL_SEPARATION` fails |
| `assertedAt` replaces delayed occurrence, intended, performed, effective, or compliance as-of time | `AR_SUBJECT_TIME` / `PC_TEMPORAL_SEPARATION` fails |
| assertion body differs by whitespace-bearing string value, case, translation, normalization, summarization, or compiled substitution | `AR_BODY` fails |
| evidence is changed, omitted, added, reordered contrary to schema posture, unresolved, mutable, or downgraded to a logical ref | `AR_EVIDENCE` fails |
| `EP_NONE` is interpreted as permission to omit the intent-bound evidence array | `AR_EVIDENCE` fails; the action policy and assertion evidence binding are different axes |
| operation reporter is copied into `performedByPartyRef` | `AR_OPERATION_PERFORMER` fails |
| `PERFORMED` is changed to `INTENDED`, or vice versa | `AR_OPERATION_POSTURE` fails |
| agent performance is alleged without exact actorship bindings, or agent bindings are added to a non-agent claim | `AR_OPERATION_AGENT_ACTORSHIP` fails |
| performer authority is reported as authorized because an evidence ref is present or the reporter was authorized | mapping or trace conformance fails; disposition remains `NOT_EVALUATED_BY_AUTHORIZATION` |
| loose or latest intervention/execution payload ref is added | `AR_OPERATION_PAYLOADS` fails |
| compliance rule or evidence-policy revision is missing, changed, mutable, or substituted | `AR_COMPLIANCE_RULES` / `AR_COMPLIANCE_EVIDENCE_POLICY` fails |
| compiled output replaces the exact compliance body | `AR_BODY` fails |
| branch-inapplicable operation or compliance fields are present as `null`, empty, or populated | applicable branch-absence mapping / `PC_BRANCH_ABSENCE` fails |
| notes, benefiting Party, loose provenance, legacy flat time, payload-ref, or supersession field is inserted | `AR_LEGACY_ABSENCE` fails |
| structure assertion creates a new field, boundary, role, or activation state | `PC_STRUCTURE` / `PC_NO_UNBOUND_EFFECT` fails |
| operation claim creates accepted execution or changes operation current state | `PC_OPERATION` / `PC_NO_CURRENT_STATE` fails |
| compliance assertion creates compliance fact, certification, or enforcement state | `PC_COMPLIANCE` / `PC_NO_CURRENT_STATE` fails |
| assertion creation mutates or deletes a prior assertion, evidence item, payload, subject, scope, or rule | `PC_INPUTS_IMMUTABLE` / `PC_NO_UNBOUND_EFFECT` fails |
| contract silently creates a SemanticEventEnvelope, ReviewDecision, consequence, or materialization | `PC_NO_UNBOUND_EFFECT` fails |
| event family or commit class differs from section 7.2 | `PC_ACTION_TYPE` fails |
| AssertionRecord is retyped as an event envelope or given caller-selected classification fields | result schema / `PC_ACTION_TYPE` fails |
| contract, schema, intent, result, or resolved-input digest changes | binding or mapping fails |
| one required mapping or postcondition disposition is missing | overall trace cannot pass |
| a failed prerequisite's dependent item is marked `PASS`, `FAIL`, or `NOT_APPLICABLE` instead of dependency-bound `NOT_EVALUATED` | trace conformance fails |
| operation claim reaches commit through PR #20 even though its selected finalization mode is `NOT_REQUIRED` | transaction binding fails; no assertion or consumption commits |
| relevant state changes between validation and atomic commit | applicable transaction guard fails and requires re-evaluation |
| domain failure rewrites authorization `ALLOW` | conformance failure; authorization evidence remains unchanged |

Fixtures must enter through the production result builder, protected-effect validator, applicable transaction boundary, persistence path, and receipt lookup rather than unit-only helpers.

---

## 14. Migration and currentness

`AssertionRecord v0.1` remains current/default until a separately governed promotion says otherwise. Existing records and examples remain v0.1 history, including their recorded `IN_FORCE` values.

A v0.1 record cannot claim v0.2 strength unless immutable source evidence establishes every required field and mapping. Missing body schema, subject/scope revision, relationship proof, subject time, evidence revision, asserting-party basis, operation provenance, compliance basis, or trusted assertion time cannot be guessed.

Migration never rewrites a v0.1 claim state, notes field, logical evidence/provenance ref, payload ref, or supersession ref. A new v0.2 record may refer to old history only through a separately governed and exact immutable binding admitted by its schema; this submission contract defines no such lineage branch.

Draft schema or contract presence changes no currentness. A v0.2 `PENDING_REVIEW` assertion does not enter an in-force materialization merely because it is schema-valid, authorized, human-approved for submission, or protected-effect-valid. Review and materialization remain downstream governed boundaries.

---

## 15. Later `AuthorizationPolicyBundle v0.2` binding

This PR does not create or edit the policy bundle.

After semantic approval and materialization of real content-addressed protected-effect contract bytes, the bundle PR must:

1. bind the exact contract ID/version/ref/digest and owning family;
2. bind the same reviewed contract to the three assertion action rules;
3. preserve each rule's exact intent profile, effect-subject kind, `RP_SCOPE_ONE` policy, evidence policy, human-finalization mode, and historical-authority posture from PR #11; and
4. include the protected-effect contract binding in each affected complete per-action `ruleDigest` closure.

The result-schema and body-schema bindings, `AR_*` selectors, derivations, forbidden-widening rules, classification, postconditions, and trace requirements remain solely inside the content-addressed protected-effect contract. Changing any of them changes `contractDigest`, which changes each affected action-rule digest. The bundle must not copy them or become a second source of domain semantics.

The bundle cannot point at this prose file as an executable contract. It also cannot make `ASSERT_OPERATION_CLAIM` executable while the separately owned `NOT_REQUIRED` transaction profile is missing.

---

## 16. Traceability to issue #22

| Acceptance criterion | Disposition |
|---|---|
| inventory current AssertionRecord capabilities, examples, and gaps | section 4 |
| decide whether a minimal v0.2 carrier is required | sections 4.3 and 5 |
| exact action, intent profile, effect-subject, result subtype, event family, and commit class map | section 7 |
| bind ID, subject, sole scope, asserting Party, times, body, evidence, and branch content | sections 5, 6, and 8 |
| preserve reporter/performer separation and `NOT_EVALUATED_BY_AUTHORIZATION` | sections 5.3, 6, 8.2, 11.2, and 13 |
| keep all new assertion submissions pending review | sections 1, 8, 10, and 14 |
| enumerate permitted derivations and required absences | section 8 |
| forbid mutation, acceptance, current state, and implicit companion effects | sections 9, 10, 12, and 13 |
| distinguish act event family from record commit class | section 7.3 |
| content-address contract and deterministic digest projection | sections 7.1 and 11.1 |
| immutable dependency-aware mapping/postcondition trace | sections 11.2 and 13 |
| validate before atomic commit without rewriting authorization | section 12 |
| production-reachable hostile cases | section 13 |
| later whole-contract bundle registration without duplicating domain semantics | section 15 |
| expose the unclosed `NOT_REQUIRED` transaction dependency without editing that boundary | sections 3, 10, 12, 13, 15, 17, and 18 |

---

## 17. Steward approval card

| Decision | Proposed answer | Approval required |
|---|---|---|
| Is a future `AssertionRecord v0.2` carrier required? | yes | yes |
| Does this contract cover exactly three assertion-submission actions and exactly one new result? | yes | yes |
| Is the exact action-to-result subtype map in section 7.2 approved? | yes | yes |
| Must every result created by these submission actions be `PENDING_REVIEW`? | yes | yes |
| Does fresh approval authorize only the exact structure/compliance submission rather than acceptance? | yes | yes |
| Is the sole immutable anchor scope copied only from `RP_SCOPE_ONE`? | yes | yes |
| Is an existing subject immutable while a prospective subject remains only claimed and uncreated? | yes | yes |
| Must a different subject-to-scope relationship have exact immutable proof? | yes | yes |
| Is `assertedByPartyRef` the selected authority subject rather than approver, sponsor, principal, performer, or beneficiary? | yes | yes |
| Is `assertedAt` trusted `effectCommittedAt`, kept separate from subject, evidence, approval, authorization, and ingress times? | yes | yes |
| Are body and evidence exact, typed, immutable, and free of notes or ref-only side channels? | yes | yes |
| Does the operation branch preserve required performer provenance without claiming historical performer authorization? | yes | yes |
| Must operation performer authority remain `NOT_EVALUATED_BY_AUTHORIZATION`? | yes | yes |
| Does the compliance branch bind exact rule and evidence-policy revisions without creating a compliance fact? | yes | yes |
| Are structure, operation, and compliance acts classified `StructureEvent`, `InterventionEvent`, and `GovernanceEvent` respectively? | yes; the first and third are explicit new contract mappings requiring steward approval | yes |
| Are record commit classes fixed to `STRUCTURE_ASSERTION`, `OPERATION_CLAIM`, and `COMPLIANCE_ASSERTION`? | yes | yes |
| Does this contract create no event envelope, review, accepted consequence, current state, supersession, or other companion domain effect? | yes | yes |
| Must every `AR_*` and `PC_*` item have an explicit allowed trace disposition, with overall `PASS` requiring every required item to pass? | yes | yes |
| Does protected-effect failure leave authorization evidence unchanged? | yes | yes |
| Does PR #20 close fresh-approval transaction handling for structure/compliance but not `NOT_REQUIRED` handling for operation claims? | yes | yes |
| Must operation-claim execution wait for a separate `NOT_REQUIRED` transaction profile rather than borrowing fresh approval? | yes | yes |
| Do schema, transaction, shared evidence, hostile conformance, acceptance, promotion, and runtime remain separately owned? | yes | yes |

Any requested authorization, transaction, review, event-vocabulary, evidence-retention, runtime, or currentness change must remain in its own trust-boundary PR.

---

## 18. Staged delivery and completion

1. **Authorization prerequisite:** satisfied by semantic approval for exact PR #11 head `03a21f669ee04f96d444e14f00ae7212cab04803`; re-open this gate if that head's semantics change.
2. **Human-finalized transaction prerequisite:** PR #20 at `98f8c4fafbae42c8f7fd931f43f53adcb4733713` supplies the approved fresh-approval protocol selected by structure and compliance; later machine materialization must bind its exact promoted bytes.
3. **Phase A domain approval:** approve or amend this one-file AssertionRecord candidate.
4. **Missing transaction-mode closure:** separately define the atomic `NOT_REQUIRED` transaction path selected by `ASSERT_OPERATION_CLAIM`; do not edit PR #20 or this domain contract to simulate approval.
5. **Domain materialization:** separately create the non-default `AssertionRecord v0.2` schema, three exact body-schema branches, protected-effect contract, selectors, and digest fixtures. Stop if the intent/result pair cannot close subject type or `subjectTime` shape without changing another boundary.
6. **Shared evidence materialization:** separately create the validation-trace envelope and governed-effect receipt profiles, together with finalization/consumption profiles owned by their existing boundaries.
7. **Bundle binding:** separately bind the exact reviewed protected-effect contract identity/ref/digest as one unit into `AuthorizationPolicyBundle v0.2`.
8. **Hostile conformance:** exercise section 13 through production-reachable paths, including delayed sync, fresh approval, agent-assisted submission, represented action, reporter/performer separation, and conflicting replay.
9. **Acceptance and promotion:** accept exact bytes and change current/default status only through separate governed steps in the sequence fixed by PR #11.
10. **OFARM2 extraction:** consume only promoted, digest-verified canonical bytes.

Phase A is complete when issue #22's criteria are reviewed, the exact PR #11 and PR #20 dependencies remain approved, the event-family choices and missing transaction-mode dependency are explicit, and this PR still changes only this non-authoritative candidate file.
