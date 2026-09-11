# OFARM Authorization Evidence Qualifying-Record Governance v0.1

Date: 2026-09-11

Status: non-authoritative Phase A candidate; exact-head review and semantic approval pending

Issue: [samovers/OFARM#33](https://github.com/samovers/OFARM/issues/33). Parent: [#10](https://github.com/samovers/OFARM/issues/10). First consumer: [#32](https://github.com/samovers/OFARM/issues/32). CP2A-DEP01 remains open.

Inspected canonical main: `71ca724a8b6ec23f1655b086a6f549496d10a47f`.

## 1. Decision requested

Approve or amend one proposed source-governance mechanism, not an implementation:

1. A qualification is a new, immutable, directly human-governed statement about one exact committed authorization-refusal bundle, or about an earlier qualifying record under that root. The original decision never changes.
2. Use one closed, tagged `AuthorizationEvidenceQualification v0.1` profile in the proposed `AuthorizationDecisionEvidence v0.2` package, subject to the explicit carrier/classification binding in section 4. Do not create a history registry or status receipt.
3. Require a separately approved, dedicated authorization action and exact target/rule binding. The proposed action is `GOVERN_AUTHORIZATION_EVIDENCE_QUALIFICATION`. It is not in the pinned authorization contract and is not usable merely because this candidate names it.
4. Propose `GOVERN_DECIDE`, `HUMAN_ONLY`, `DIRECT_HUMAN_ACTION_REQUIRED`, an explicit scoped grant and no inheritance/delegation for that action. A runtime verifies and commits the human's act; it has no independent power to invent qualifications.
5. Support correction, record dispute, basis dispute, explicit resolution/reopening and append-only supersession. Preserve competing branches. All relationship targets must already be authoritatively committed before the qualifying transaction starts.
6. Reuse the human-finalization transaction owner's guards, complete atomic set, single use and reconciliation. Do not invent a second transaction protocol or claim a complete history cut.
7. Verify old admissions under their exact historical authority and rule bindings. Later revocation, a governed challenge and missing verification evidence are different facts.

Approval of this file would approve these design choices only. It would not create grants, approve the separate authorization amendment, materialize schemas, admit runtime records, approve #32's classifier, close CP2A-DEP01, merge a PR, promote contracts or unblock OFARM2 implementation.

## 2. Primary trust boundary and PR limit

Primary trust boundary: **admission authority and lifecycle of authorization-evidence qualifying records**.

This PR changes only this historical Phase A candidate. It proposes the protected source result, its relationship semantics and its required admission bindings. It does not edit another candidate or change active law. The exact authorization-owner delta is exposed in section 5 and remains a separate prerequisite, not an amendment hidden in this PR.

| Separate owner | Boundary preserved |
|---|---|
| PR #11 authorization | Existing evaluator, grants, principal/actorship, action/target rules, outcomes and retry eligibility remain unchanged |
| PR #17 final ReviewDecision | No new target family, ReviewDecision result mapping or accepted-consequence composition |
| PR #20 / #26 transactions | No new isolation, locks, atomic set, operation identity, cancellation or reconciliation protocol |
| PR #29 retention/proof strength | No new access, retention period, deletion/redaction or key-custody power |
| #32 source-history producer | No six-label mapping, overall history classifier, absence proof or reply-valid completeness policy |
| Approved PR #31 public consumer | No public fields/codes, disclosure rules, fallback or fresh-refusal shortcuts |
| Acceptance and implementation owners | No acceptance, extraction, current/default promotion, deployment or runtime changes |

If this design needs a change to one of those owners, identify the exact failed binding and stop before editing that boundary. A generic instruction to continue is not a cross-boundary exception.

## 3. Governing sources and exact pins

Apply `PROJECT_AUTHORITY.md`: active baseline outranks accepted RFCs, companion artifacts and machine contracts. Reader indexes are navigation/control, not new authority. The active references below are read at the canonical main pinned above.

| Active source | Constraint used here |
|---|---|
| Constitution, sections 7.9–7.18, 8 and 10; AAI-C.1–1.1 | Action-specific authority, prospective revocation, distinct times, preserved immutable history and visible material qualification |
| Platform Architecture, sections 3 and 14; AAI-P.6–6.1 | All applicable enforcement gates, evidence provenance, no implicit authority and honest result qualification |
| Alignment Register, sections 4.3a–4.6 | Identity, lifecycle, truth and authority semantics cannot be hidden runtime conventions |
| Post-gap readiness memo and final hostile review, AAI-CP1 qualification addenda | Qualification cannot be suppressed; a design or schema is not executed release-gate evidence |
| Authority, Delegation and Data Sovereignty Policy v0.2 | Explicit scope, separately governed grant power, no sharing-to-writing upgrade and historical revocation limits |
| Event Grammar and Commit Matrix v0.1, sections 3.6–4, 6.6, 6.8, 8 and 10 | Distinguish supporting evidence from formal governance; choose the dominant consequence; no undeclared promotion path |
| Evidence Sufficiency and Attestation Policy v0.1 | Bind original support, interpretation and provenance; a carrier or frozen reference is not sufficient evidence by itself |
| Accepted CP2 result-qualification and trace RFC | Truthful qualification and permission-limited access remain mandatory |

All six PRs were rechecked on 2026-09-11: open, draft, unmerged, with canonical base `71ca724a8b6ec23f1655b086a6f549496d10a47f`. Prior semantic approvals do not make them active law. PR #17's approval status was not re-audited.

| Candidate | Exact head | Sections / use |
|---|---|---|
| [PR #11](https://github.com/samovers/OFARM/pull/11) | `03a21f669ee04f96d444e14f00ae7212cab04803` | 7.5 closed targets; 17.2–17.6 evidence and authority bindings; 18 admission/digests; 24 delivery order |
| [PR #17](https://github.com/samovers/OFARM/pull/17) | `9ef08030b25eb3db1c2da14d6595300198384ff2` | Existing final-review target/result scope does not supply this authoring path |
| [PR #20](https://github.com/samovers/OFARM/pull/20) | `98f8c4fafbae42c8f7fd931f43f53adcb4733713` | 10–13 guards/finalization/atomic commit; 17 recovery; 18 evidence ownership; 20 future protected families |
| [PR #26](https://github.com/samovers/OFARM/pull/26) | `e042efa2911b2ef0a61603b8e0adaa6911c03ac0` | Original NOT_REQUIRED refusal durability where applicable; not the proposed qualifier's human-finalization mode |
| [PR #29](https://github.com/samovers/OFARM/pull/29) | `8e0994cae5610ac9c0d2652e02c8a8a2dd7b45c5` | 5 historical promise versus present byte/integrity proof; retained evidence and custody limits |
| [PR #31](https://github.com/samovers/OFARM/pull/31) | `092be94f3a67497ba619295932cd0b2b1e9443f3` | 5.3–5.4 committed refusal history/disclosure; 11.1 CP2A-DEP01 |

Dependency files, all under `package_meta/history/clean_baseline_migration/phase_reports/` at their pinned heads:

- `authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md`
- `review_decision_final_protected_effect_contract_rfc_candidate_v0_1.md`
- `governed_human_approval_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`
- `not_required_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`
- `authorization_evidence_retention_and_proof_strength_rfc_candidate_v0_1.md`
- `cp2_authorization_result_surface_and_public_reason_codes_rfc_candidate_v0_1.md`

A changed head requires inspection and renewed binding review; it does not silently replace a pin. [Issue #21](https://github.com/samovers/OFARM/issues/21) and PR #11 section 24 control staging over older #10 summaries. The [issue-level review](https://github.com/samovers/OFARM/issues/33#issuecomment-5630591207) authorized no semantics; its positive/unauthorized admission checkpoint and historical-authority case are addressed below.

## 4. Minimum carrier and semantic classification

The first root is the **complete committed v0.2 authorization request/result/full-trace bundle** for `DENY`, `REQUIRE_REVIEW` or `REQUIRE_HUMAN_APPROVAL`, as consumed by PR #31. An individual trace fragment, ingress rejection, uncommitted attempt, later decision or v0.1 bundle is not an eligible root. Do not rewrap old evidence as v0.2.

Existing inventory does not close the gap:

- PR #11 section 17.2 permits immutable evidence with linked later corrections/failures but supplies no governed qualifying-record lifecycle.
- Its `RP_EVIDENCE_TARGET_ONE` and final-review target sets do not admit authorization evidence as a primary review target. Read eligibility for an authorization trace is not writing authority.
- Current/default `ReviewDecision v0.1` has a closed target-family set without authorization evidence. Generic `SemanticEventEnvelope v0.1` references and `CommitIngressRequest/Result v0.1` do not establish qualifying authority.
- A draft materialization-freshness vector, visible record version or integrity digest is not proof that all incoming qualifications have been observed. Current/default status is taken from `CONTRACT_INDEX.json` and `CONTRACT_FAMILY_CURRENTNESS.json`, not a filename.

The proposed new profile is a **governed audit qualification**, not an ordinary evidence attachment. Its dominant act is `GovernanceEvent` / `governance decision` under Event Grammar sections 3.7 and 6.8. It does not become a `ReviewDecision`, accepted domain consequence or current-state materialization. Rationale/support attachments remain evidence records under their own classifications.

Only the qualifying act gets that governance classification. The original refusal and the new act's authorization/finalization evidence retain their existing `EvidenceEvent` / `evidence record` meanings. The transaction can bind those separately classified records without assigning two primary event families to one event or relabeling the whole authorization bundle.

Prefer placing this tagged profile in `AuthorizationDecisionEvidence v0.2`, beside the evidence it qualifies. Package membership does not grant authority. PR #11's existing evidence-record classification must not be silently applied to this formal act: the later source-profile/package binding must explicitly admit this governance-classified member and its event/commit mapping. That exact compatibility decision is open as QG-BIND02. Until it is approved, the proposed tagged profile is not an admitted package member. No new top-level event family or generic governance carrier is proposed.

The profile itself is the protected source result. It carries the exact attested statement and typed relationship; an extra durable status object is unnecessary. An ordinary allegation, later failure report or attachment may support a qualifying act but cannot acquire its effect through a flag, name, reference or classifier decision.

## 5. Concrete authority path and separate missing amendment

### 5.1 Proposed path

Use one dedicated action for all six relationship forms in section 7. Its exact closed intent determines which form is requested; authorization cannot accept an unrecognized form or omit its bound fields.

The proposed action is `GOVERN_AUTHORIZATION_EVIDENCE_QUALIFICATION`. The authorization-owner proposal is:

- Family `GOVERN_DECIDE`; actor posture `HUMAN_ONLY`; finalization `DIRECT_HUMAN_ACTION_REQUIRED`; no delegation and no scope inheritance.
- One eligible authorization-refusal root, plus only the exact earlier qualifying records/support bindings required by this act. The trusted extractor derives the full target and scope set from the intent and bound sources, not caller mirrors.
- An explicit `AuthorityGrant` with the exact action's `{actionClass, ruleId, ruleDigest}` binding, valid role/Party relationship, owning scope, validity interval and revocation state at the final evaluation. A broad administrator label or authority to read, attach evidence or review another family is insufficient.
- Preserve PR #11's existing principal resolution, sovereignty/purpose checks, default deny, single-use transaction-bound decision, evidence requirements and final-evaluation algorithm. The human who performs the act is the natural-person requester, not an agent's sponsor or synthetic approver.
- The source owner supplies the exact intent, extractor, result contract and validation bindings described here. The authorization owner must approve their selection by its new closed action/rule/target entry before use.

The proposed new resource policy has exactly one `AUTHORITY_TARGET`: the refusal root, using the new closed kind `AUTHORIZATION_REFUSAL_BUNDLE`. Its complete immutable identity and owner-derived scope anchor are resolved from the root, including when the act qualifies a prior qualifier. Earlier qualifiers use a new closed `AUTHORIZATION_EVIDENCE_QUALIFICATION` kind as `INTEGRITY_INPUT`; the specifically selected original basis is an exact typed integrity input; attested support is `EVIDENCE_INPUT`. These are proposed additions, not kinds that the current extractor accepts. The exact role/cardinality choices must be recorded in QG-DEP01 and QG-BIND03. One sufficient authority path must cover the root target by itself; grants across target branches cannot be unioned. Mixed-root or mixed-tenant predecessors fail before authorization can be treated as sufficient. The profile cannot widen the scope inherited from its root.

This is the precise **QG-DEP01** authorization prerequisite. It needs a separately reviewed owner amendment to PR #11's action catalog, closed target/extraction profile and corresponding rule binding. It must not enlarge existing `REVIEW_*` or evidence-link permissions. Actual authority issuance remains separately governed; no new grant-issuance route or role assignment is created here.

Until QG-DEP01 is accepted and bound, submitting the proposed unknown action follows PR #11 section 18.1 ingress rejection. It is not a fabricated authorization `DENY`, and cannot create a qualifying record. The worked path below is conditional on this exact prerequisite, not a claim that today's contract already accepts the action.

### 5.2 What the human and runtime each establish

The human explicitly attests the complete typed act, its exact subject, its bounded explanatory statement and the cited support. Every act requires a nonempty explanation, at least one exact support binding, and an explicit attestation that the support is sufficient for this stated audit qualification. Support may be a passage in the original bound evidence; an alleged absence requires the original relevant absence/predicate evidence, not a fruitless search today.

This v0.1 path establishes **an authorized, attributable governance position**, not machine proof that every explanatory assertion is objectively true. Inconsistent authorized positions can coexist and remain visible. The runtime verifies authority, support identity/provenance, complete attestation, relationship semantics and transaction conditions. It must not invent the statement, approve evidence on the human's behalf, infer governance from authentication or treat a model's confidence as authority.

Present reading/disclosure authority is separate. A verifier may inspect only evidence it is permitted to inspect. No write grant here grants disclosure or overrides retention/custody.

## 6. Immutable bindings and exact protected result

The following are semantic groups for later closed schemas, not a wire schema or existing field names. Every group is mandatory except where a relationship explicitly excludes it. No unresolved ref, placeholder digest or omitted critical field can be admitted.

| Group | Required binding |
|---|---|
| Profile and identity | Exact profile/schema/digest-profile versions and digests; one immutable qualifier ID; new content requires a new ID |
| Root | Package/profile kind; exact request and result identifiers from the owning bundle; v0.2 `decisionBundleDigest`; exact bundle schema bindings; tenant and full owner-derived scope; authoritative original commit proof |
| Subject / predecessors | Typed exact root or earlier qualifier refs, immutable IDs, content digests and schema bindings; each qualifier must resolve to the identical root binding |
| Historical basis | For a basis dispute, exact selected basis object/path in the subject's original evidence, with its source ID/version/digest and selection binding; no current substitute |
| Act | Closed relationship kind; exact statement; support refs/content bindings; direct-human attestation; kind-specific lineage fields |
| Authoring evidence | Exact final authorization request/result/trace bundle ref and digest, direct-human finalization evidence ref/digest, selected source-contract and admission-rule bindings, and transaction-owned operation/attempt identity |
| Time | Any asserted event/effective time is separately labeled; trusted act and final evaluation times come from their owner records; authoritative admission time/order comes from the commit evidence |

Use PR #11 section 18.8 for the root and authorizing bundle digest: the exact v0.2 request/result/trace projection and exclusions, not an ad hoc hash of selected fields. Each new qualifier's content digest is over its complete finalized canonical JSON bytes under a separately bound JCS/UTF-8/SHA-256 profile. Its full-byte digest is external to the qualifier bytes. Reject duplicate JSON keys before canonicalization. Do not copy the authorization-bundle self-digest exclusions to the new profile.

The intent fixes the proposed qualifier ID, root, subjects, kind, statement, support, asserted times and attestation content. Trusted authoring-evidence bindings are filled only by the prescribed finalization/result derivation. The result contract requires exact equality to intent for human-selected content, exact derivation for trusted content, closed fields and one qualifier result. A valid intent cannot yield additional qualifications, modified original bytes, a ReviewDecision or domain effects.

The qualifier does not embed its own full-byte digest, a future effect receipt digest, a future consumption digest or a future commit time. Those are bound externally by the existing transaction records. This avoids both digest cycles and mutation after validation.

The original request, outcome, evaluation time, selected authority/history, consumption posture and bytes remain immutable. A correction may explain an error in them; it cannot change them, reevaluate the old request, grant retry eligibility or turn an earlier refusal into permission. A different request, later result or cross-tenant copy cannot substitute for this root.

## 7. Closed relationship meanings

All six forms use the same proposed action, historical admission checks and root-binding rules. A free-text verb or unknown relationship is not a seventh form. Here, an **assessment** is an audit explanation, never a replacement authorization result.

| Form | Exact target and required content | Governed meaning / limit |
|---|---|---|
| `CORRECTION` | One root or earlier qualifier; identify the specific content/claim being corrected, corrected account and supporting evidence | Adds an attributable correction to that account. No JSON patch, automatic withdrawal of other qualifications or reversal of the original act |
| `OPEN_RECORD_DISPUTE` | One root or earlier qualifier; identify the contested recorded content/representation and grounds | Opens an explicit dispute about that record. An allegation alone has no such admitted effect |
| `OPEN_BASIS_DISPUTE` | One root or earlier qualifier plus exact original selected supporting/admission basis and grounds | Opens a dispute about the basis actually used, rather than replacing it with present policy or a different source |
| `RESOLVE_DISPUTE` | One earlier `OPEN_RECORD_DISPUTE`, `OPEN_BASIS_DISPUTE` or `REOPEN_DISPUTE`; repeat its original dispute identity, focus and basis; state `UPHELD` or `WITHDRAWN` with reasons/support | Records this human's resolution of that exact branch. `UPHELD` accepts the objection; `WITHDRAWN` withdraws it. Neither means the whole root history is clean; any correction is a separately admitted act |
| `REOPEN_DISPUTE` | One earlier `RESOLVE_DISPUTE`; preserve the original dispute identity, focus and basis; state new grounds/support | Reopens that exact resolution branch. It does not rewrite the resolution, open a different subject or infer that all other branches reopened |
| `SUPERSEDE` | The root alone, or a nonempty explicit set of earlier `CORRECTION` / `SUPERSEDE` records with the same assessment focus; provide the complete replacement assessment and support | The new record itself is the successor account. It replaces only the named assessment(s) for later reliance; the old decision, bytes and relationship history remain. It cannot resolve a dispute or target a resolution/reopening act |

For a correction, **assessment focus** is its exact subject record. For a supersession of the root, focus is the root. For supersession of corrections/supersessions, focus is inherited and must match across every named predecessor. A correction of a correction therefore addresses that correction's account explicitly; it does not silently become a rewrite of the original root.

For `SUPERSEDE` of the root, the replacement is a new **audit account of the original refusal**. It may say that the explanation is no longer reliable and supply the supported replacement explanation. It cannot supply a new authorization outcome in place of the old one. A later ALLOW/DENY remains a separate decision, not this replacement account.

For a basis dispute about the root, basis must occur in its original selected trace/evidence. For a basis dispute about a qualifier, it must occur in that qualifier's original authorizing bundle, rule/result validation or attested support. A grant revoked after admission may be cited as a later event, but does not by itself prove it was invalid when used. Unsupported basis identities or field substitutions fail source validation.

### 7.1 Corrections, disputes and their own histories

A correction can be corrected or disputed; a dispute/resolution/reopening record can receive a correction about its recorded account or a separate dispute. Such an annotation never mutates its relationship kind or performs its control transition. Use `RESOLVE_DISPUTE` / `REOPEN_DISPUTE` for those transitions. Every new act needs fresh authoring authority at its own admission.

Resolution addresses one explicit open/reopened node. Reopening addresses one explicit resolution. The origin identity/focus/basis is derived through this chain and checked, not selected anew by the caller. A new subject or different basis needs its own new dispute. A standalone resolution without an admitted opener is invalid.

There is deliberately **no global “currently open” or “only latest successor” precondition**. Two authorized humans may resolve the same opener differently, reopen different resolutions, or supersede the same account concurrently. Each locally valid branch is preserved. This avoids pretending a positive-row read establishes the absence of other branches. Any stronger exclusivity would require a separately approved source rule and its complete guarded predicate, not an implementation shortcut.

### 7.2 Supersession and conflicts

Every successor is the new qualifier itself. A `SUPERSEDE` record cannot create an edge between two older records. It may name several committed predecessors of the same focus to reconcile known competing assessments, but that does not assert that no unseen competing successor exists.

For a verified set of records, retain all explicit replacement edges. Superseding a superseder does not revive earlier accounts. Multiple incomparable successor tips remain competing accounts; neither commit time nor event time elects a winner. Two correction records alone do not supersede each other. Supersession of an assessment does not close disputes about it or clear unrelated corrections.

These are source relationship meanings, not the public history classification. A verifier can report local edges, competing branches and the proof limits of the observed set. Only #32 may decide their aggregate public significance and whether its observation is complete enough for any answer. This file does not assign any of PR #31's six labels.

### 7.3 Acyclicity without a new history service

All root/subject/predecessor/control references must identify exact records authoritatively committed and observable **before the new transaction's trusted start**. A reference to this new qualifier, another record in its prospective atomic set, a future record or a missing/unresolved object is inadmissible.

The authoritative dependency relation is therefore strictly backward: new record to an already committed record. Supersession's successor-is-new rule applies to its semantic edge as well, not merely to its storage references. This excludes both reference cycles and the hidden “A supersedes B, then B supersedes A” cycle between old nodes. Content that attempts either is rejected, not repaired by timestamp sorting. Conflicting root/digest claims, mixed assessment focuses and unknown transitions are rejected.

An import/delayed replica view cannot substitute for original admission proof. A graph with missing predecessors or unproven ordering cannot be declared valid merely because its visible part is acyclic.

## 8. Authoritative admission, ordering and visibility

The original refusal uses its existing owner durability path. The new qualifier uses **PR #20 direct-human finalization**, only after QG-DEP01, QG-BIND02 and the exact protected-result bindings are accepted. Section 20 of that candidate supplies common obligations for future human-finalized families; it does not provide this missing source result by itself.

One successful admission follows this construction order:

1. Resolve and verify the exact already-committed root, relationship targets and original support/basis. The human performs the exact act under the bound direct-human route. This creates no durable qualifier yet.
2. Start the short transaction with trusted time, exact `governedTransactionPolicyRef`/digest and the owner's snapshot/guard profile. Verify target commitment before start and the complete relevant source/admission state.
3. Build the prospective immutable direct-human finalization evidence as PR #20 requires. Run the final PR #11 evaluation against the final snapshot and exact intent; require a supported rule, `ALLOW`, correct human mode and all other applicable gates. Do not use an old portable ALLOW.
4. Build the exact qualifier from the intent and trusted final authorization/finalization bindings. Validate its schema, support/provenance, relationships, derived scope and protected-result postconditions. Fix its full-byte digest before downstream consumption/receipt construction.
5. Build the transaction owner's one decision-consumption record, protected-effect validation trace and governed-effect receipt. Bind the exact qualifier digest and complete atomic membership; the qualifier does not point forward to these records.
6. Recheck the deadline, complete relevant guards and uniqueness under PR #20, and atomically commit the whole owner-required set, including the qualifier and any required ingress evidence. Only then expose it as an admitted source fact.

The owner-required set still includes the final authorization request/result/full trace, direct-human finalization evidence, exactly one decision consumption, exact protected result, passing validation evidence and receipt. This candidate neither removes members nor adds a second commit. There is no approval challenge, sponsor approval, reservation or approval consumption in this direct-human path.

Required guards cover authority/revocation/rule applicability, target and support identity/visibility, qualified root/scope, immutable-ID conflicts and the owner's operation/attempt/replay uniqueness. Negative and set-valued conditions require the complete predicate guards already demanded by PR #20 section 10; positive rows alone do not suffice. This design does not require “no other qualification exists,” a root-history lock or global qualification-head uniqueness. The actual state mapping and proof mechanism must be bound and tested later, not invented as a watermark here.

An application log, staged file, upload success, classifier cache or insertion outside that atomic set is not authoritative admission. Unknown persistence stays unknown until the owning status/reconciliation protocol resolves it. Do not expose a success, create an alternate qualifier ID to evade uncertainty, consume the decision again or backfill missing evidence as if it had committed atomically.

### 8.1 Replay, time and late delivery

- Exact transaction replay uses the owner's original operation/attempt and status path. One committed act remains one act, even if delivered or referenced repeatedly.
- The same qualifier ID with different finalized bytes is an immutable-identity conflict. The same operation identity with changed intent follows the owner's conflicting-replay rule. A different ID is not a legitimate replay bypass.
- Separately authorized distinct human acts may contain similar statements; preserve their different identities and evidence. Do not collapse them by text or timestamp.
- Trusted admission/commit facts establish durability and dependency ordering. Asserted event/effective time does not move the commit backward or make an unseen record known earlier.
- A replica may deliver successors before predecessors. The observer holds the unresolved link as unverified until the necessary proof is available; it neither re-admits the act nor backdates its own observation.
- Original evaluation time, qualifier act/admission times, history-observation time and reply qualification time remain distinct. This file creates no promise that a newly committed refusal has no qualifying history.

## 9. Verification, historical authority and proof limits

The following are **internal verification dispositions**, not wire enums, public codes, new durable receipts or a complete history result.

| Disposition | Required evidence / consequence |
|---|---|
| Admission established for this exact record | Bytes, root, typed relationship, original authority/rule/finalization evidence, passing source validation and authoritative atomic commitment/ordering are all verified |
| Proven invalid under the bound admission contract | Positive evidence of a broken requirement: wrong tenant/subject, mismatched bytes, wrong writer/rule, unsupported link, cycle or contradictory atomic membership. Do not count it as a valid qualifying act |
| Admission not established | Required bytes, schema/rule, historical authority, target proof or commit outcome is missing, inaccessible, unsupported or unresolved. Do not promote it to a valid act, or infer that no act/history exists |

Record failures precisely: a mismatch in a retrieved copy disproves that copy's claimed integrity; it does not prove all retained copies or the original committed object are corrupt. A failed lookup is not proof of nonexistence, deletion or original unauthorized action. A known valid record plus unproven surrounding completeness is **not** “admission not established” for that record: keep its admission result and the separate observation limitation.

### 9.1 Historical authority, not current re-admission

At later inspection, verify the original act against the exact historical rule ID/digest, source-contract/schema bindings, authority-grant per-action binding, principal/Party/role relationship, scope, validity interval, revocation evidence, snapshot/guard proof and finalization/receipt that applied to that act. Current grant lookup is not a substitute for retained admission evidence. Verification checks the original governing evaluation; it does not run today's policy against the original request and replace its result.

| Later development | Source-side treatment |
|---|---|
| Writer's permission expires or is prospectively revoked after valid admission | Original admission remains established if historical proof is intact. A new act by that writer needs new valid authority |
| Admission policy/rule changes later | Retain the exact old binding for historical verification; neither silently reinterpret nor re-admit old records under the new rule |
| Writer had no required grant at original admission but receives one later | Later authority cannot legitimize the earlier act. A claimed earlier admission fails if that violation is proved; any new act needs a new identity and lawful admission |
| Governed record later challenges a qualifier's original grant, rule application or evidence | Preserve original admission evidence and the new exact basis-dispute relationship. A challenge is not itself proof of invalidity or permission to erase the original |
| Retained historical proof cannot now be inspected/verified | Admission is not established for this verifier at this observation; record the precise limit, without labeling the original admission proven unauthorized |

If an independent verification proves a requirement of the original bound contract was violated, report proven invalidity with that evidence. If a human only contests the basis, report the admitted challenge without converting it into such a proof. Resolution/reopening records preserve this distinction. This contract grants no retroactive revocation or special adjudication power beyond its defined audit qualifications.

Current access controls still apply to verification and disclosure. Loss of present permission to inspect does not alter the historical act. PR #29's exact-byte versus digest-only limits remain: a digest commitment alone cannot reconstruct content or prove admission; candidate bytes can support a comparison only under the exact original profile and available provenance. Unknown schema versions, missing policy bytes or absent relationship targets block the corresponding verification claim, not merely a cosmetic detail.

## 10. Worked admission pair and historical follow-through

This is a falsifiable design example, **not observed records, valid JSON fixtures or executed tests**. Names `D`, `H`, `J`, `G`, `R`, `Q` and `T` are symbols for future fully bound objects, not placeholder hashes that could pass validation. QG-DEP01 and QG-BIND02 must first be separately resolved and real reviewed bytes/digests supplied.

### 10.1 Positive case: admitted basis dispute

1. `D` is a durably committed v0.2 `DENY` request/result/full-trace bundle for tenant Farm-A and one exactly derived scope. The complete bytes match its `decisionBundleDigest`, and its original commit proof is available. Its trace selected immutable authority source `G` at a named original binding.
2. Human `H` has an independently issued, valid explicit grant for the proposed action, bound to the exact rule `R` and that scope. `H` is the resolved direct human with the required Party/role relationship. The grant, issuance basis, validity and revocation state are checked independently of anything asserted in `Q`.
3. `H` performs `OPEN_BASIS_DISPUTE`: “The scope evidence used for G is contested,” with the exact original `D`/`G` bindings, a specific support record and an explicit sufficiency attestation. This does not allege that a current replacement grant was the original basis.
4. Transaction `T` verifies that `D`, `G` and required support were already committed, binds the final trusted snapshot and constructs direct-human evidence. The final authorization under `R` is `ALLOW` for this **new qualifying act**, not a changed answer to D's request.
5. The source validator derives one new qualifier `Q`, verifies the exact basis link/statement/scope and passes the result. PR #20 commits `Q` and the complete required authorization/finalization/consumption/validation/receipt set atomically. Before this commit, `Q` was only a proposal.
6. A later authorized verifier checks the retained bytes and independent historical bindings. It establishes Q's admission, its exact relationship to D's original G and its authoritative admission facts. It passes those facts to #32. D is still the original DENY. The verifier has **not** proved that it has seen every other qualification or that any public label can yet be emitted.

### 10.2 Otherwise identical unauthorized writer

Replace only `H` with human `J`, who can authenticate and read D but has no grant for the new action. All intended content, target, support, time conditions and other gate inputs are otherwise identical. Authentication, read access and the human's attestation do not supply the missing action authority.

With the new action correctly installed, the final authorization fails its required grant check under PR #11; the qualifier does not enter a successful atomic set and is not an admitted source fact. Any refusal evidence follows its own owner path, not a fake qualifier success. If J copies the proposed bytes into an attachment and calls it Q, it still lacks lawful authorizing/finalization/commit evidence. If it claims H's authority bundle, the requester/act/intent binding mismatch proves that claim invalid.

This is different from unavailable evidence: if a purported Q has no inspectable original authority bundle or an unresolved commit outcome, admission is not established; do not assert “wrong writer” without proof. It is also different from the positive Q whose admission is established but whose incoming-history completeness is unknown.

### 10.3 Historical follow-through

After the positive commit, H's grant is revoked and rule R is replaced. Q remains historically verifiable using the original R/grant/interval/revocation/snapshot evidence; the current grant table is not used to re-admit it. If a newly authorized human challenges the original grant's validity, that is a new exact `OPEN_BASIS_DISPUTE` about Q's admission basis, with its own fresh authorization and commit. If the old rule bytes instead become inaccessible, verification reports the proof limit; it does not call Q invalid merely because today's policy differs.

Conversely, granting J permission later does not rescue the unauthorized version. These source facts and distinctions are supplied to #32; their aggregate public qualification remains that issue's decision.

## 11. Exact handoff to the source-history producer

This handoff is an internal, permission-governed verification procedure and source fact set. It is not a new history-status carrier, completeness certificate or disclosure permission.

For the exact eligible root, #32 can use:

- Root kind, immutable request/result identifiers, bundle digest, schema binding, tenant/scope and original authoritative commit facts.
- Each observed candidate qualifier's exact bytes/ref/digest, kind, subject/predecessors, dispute origin/focus, selected historical basis, attested statement/support and immutable authoring bindings.
- Per-record admission disposition with the actual verification evidence and limitations, including the original rule/grant/authority and source-validation bindings.
- Authoritative commit and dependency-order evidence, and the actual source locations/index/projection bindings used to retrieve the incoming relation set. A search result's timestamp alone is not such evidence.
- Explicit observed resolution/reopening/replacement edges and competing branches, separately from any completeness claim about the incoming set.

Procedure: verify the root; verify each candidate's exact bytes and historical admission; follow typed committed predecessors to validate its root/focus/basis and ordering; preserve invalidity evidence and unresolved inputs distinctly; pass the admitted source facts plus proof limits and actual observation inputs to #32. Do not silently discard an unresolved candidate from the observation and then call the history complete or clean.

The writer's local admission guard is **not** a complete-history proof for the reader. #32 must bind its observation to the actual authoritative source membership/incoming-relationship set, tenant/scope, supported profile/version universe, visibility and relevant admission/commit ordering. It must account for concurrent admission, delayed indexing/replication, missing or restricted records and invalid/unresolved candidates under its own reply-valid completeness policy. This candidate does not assert that an existing snapshot or watermark already covers that set.

No root fields, qualifier IDs/counts, support, hidden-history existence or verification details become public by this handoff. PR #31's history-independent disclosure check, withheld/unavailable behavior and safe fallback remain unchanged. A fresh refusal, empty lookup, readable root, passed digest check or valid individual qualifier does not establish a fresh `NONE` or `AVAILABLE` result. Permission to classify is not permission to disclose, and neither is permission to write.

## 12. Invariants, case specifications and ownership

These cases specify future conformance. No schema, admission, transaction-race or privacy test is claimed executed by Phase A. “Reject” below means reject the claimed source admission/result under its applicable owner path, not invent a new public error code.

| Invariant | Requirement |
|---|---|
| QG-I01 | Only the exact eligible committed root and same-root immutable qualifiers may be governed targets |
| QG-I02 | Qualification requires independent exact-action human authority and finalization; carrier/identity/label alone is insufficient |
| QG-I03 | Original authorization bytes, outcome, times and history are never rewritten or retroactively reauthorized |
| QG-I04 | Closed typed relationships preserve focus/basis; only explicit control transitions change that branch |
| QG-I05 | Backward committed links and successor-is-new prevent cycles; competing branches have no automatic winner |
| QG-I06 | Admission requires the complete existing owner atomic set and guards; replay/uncertainty cannot manufacture a second act |
| QG-I07 | Historical admission proof, proved invalidity, present proof limits and observation completeness remain separate |
| QG-I08 | Source facts do not grant complete-history, public classification, disclosure, currentness or runtime readiness |

| Case | Required result | Level / owner |
|---|---|---|
| QG-C01 — positive basis-dispute path | Section 10.1 produces one independently verifiable qualifying act after all owner prerequisites; D unchanged | Authority + semantic + later runtime; #33 / authorization / transaction |
| QG-C02 — ordinary allegation or failure | Attachment named “correction,” later failure, generic evidence event or caller flag does not become a qualification | Semantic/admission; #33 |
| QG-C03 — unauthorized near-twin | Section 10.2 cannot commit a qualifier; distinguish absent grant from missing verification proof | Authority/admission; #33 / authorization |
| QG-C04 — wrong exact binding | Wrong tenant, scope, kind, request/result revision, rule or digest rejected even with well-formed bytes and authenticated writer | Schema + semantic/authority; #33 / authorization |
| QG-C05 — record versus original basis | Different typed links; substituted current grant or unrelated basis rejected | Semantic; #33 |
| QG-C06 — correction of correction | New exact annotation; old content/relationship persists; no implicit root rewrite or dispute resolution | Semantic; #33 |
| QG-C07 — resolve then reopen | Preserve opener identity/focus/basis through explicit alternating nodes; missing opener or changed basis rejected | Semantic; #33 |
| QG-C08 — supersession chain and competing successors | Only new-node replacement; same-focus merge permitted; old bytes retained; no implicit revival, winner or clearing of disputes | Semantic + observation; #33 / #32 |
| QG-C09 — cycles or unsupported relationships | Self/future/same-transaction references, old-to-old successor edges, mixed focus and unknown kinds rejected; missing proof stays unresolved | Schema + semantic/admission; #33 |
| QG-C10 — later outcome, permission change or failure | Later ALLOW/DENY, revocation or failure creates no automatic qualifying relationship or retroactive authorization | Semantic/authority; #33 |
| QG-C11 — target not yet committed | Uncommitted or missing/unresolved root/target cannot pass admission; upload/cache visibility insufficient | Admission + later runtime; #33 / transaction |
| QG-C12 — replay and identity conflict | Exact replay returns/reconciles one original act; repeated reference not a second act; changed bytes/intent fail their owner identity checks | Semantic + later runtime; #33 / transaction |
| QG-C13 — concurrency and late delivery | Concurrent branches preserved; successor-first observation unresolved until proof arrives; earlier effective time cannot backdate knowledge | Later runtime + observation; transaction / #33 / #32 |
| QG-C14 — incomplete or uncertain proof | Digest-only, missing bytes/rule/grant, corruption and uncertain commit produce precise distinct limits; no invented admission or absence | Integrity + admission; #33 / #29 / transaction |
| QG-C15 — restricted history | No grant of access/disclosure; preserve producer uncertainty and PR #31's non-leaking fallback | Observation/privacy; #32 / #31 / retention owner |
| QG-C16 — historical authority checkpoint | Section 10.3: later revocation/rule change does not erase admission; governed challenge differs from proof loss; later grant cannot legitimize old unauthorized act | Authority/semantic; #33, aggregate result #32 |
| QG-C17 — bad atomic/result binding | Correct qualifier bytes but missing consumption, wrong intent, mutated after hashing, mismatched receipt membership or premature visibility cannot prove successful admission | Semantic + later runtime; #33 / transaction |
| QG-C18 — valid Q, incomplete incoming history | Preserve valid individual admission and separately unproven completeness; no fresh-history/public label inferred | Observation; #33 / #32 |
| QG-C19 — unknown action/carrier today | No admitted new action/package member before owner closure; unknown action follows ingress rejection, not a made-up DENY | Binding/admission; authorization / #33 |

Traceability to the ten issue acceptance criteria:

| Criterion | Design sections | Invariants | Named cases |
|---|---|---|---|
| 1 — concrete mechanism | 4–6 | I01, I02 | C01, C02, C19 |
| 2 — admission authority | 5, 8–10 | I02, I07 | C01, C03, C04, C16, C19 |
| 3 — immutable binding | 4, 6–7 | I01, I03 | C04, C05, C10, C11 |
| 4 — closed meanings | 7 | I03, I04 | C02, C05–C08, C10 |
| 5 — own lifecycle | 7.1–7.3 | I04, I05 | C06–C09, C13 |
| 6 — admission/visibility | 8 | I01, I05, I06 | C11–C13, C17 |
| 7 — failures/proof | 9–10 | I03, I07 | C03, C14, C16–C18 |
| 8 — usable handoff | 11 | I07, I08 | C05, C08, C13–C16, C18 |
| 9 — falsifiable cases | 10, 12 | I01–I08 | C01–C19 |
| 10 — later units/gates | 13–14 | I02, I08 | C01, C18, C19 and exact binding review |

In this traceability table, Ixx and Cxx abbreviate the full QG-Ixx and QG-Cxx identifiers above. Shape checks exercise closed fields and reference forms; semantic validators exercise relationship/root/focus/derivation rules; authority and admission fixtures need bound historical evidence. Races, durable visibility, uncertain commits and privacy require later real runtime evidence. None can be replaced by Markdown checks or a standalone JSON-schema pass.

## 13. Exact dependency and materialization ledger

No new prerequisite issue is opened by this candidate. One demonstrated authorization amendment is required; remaining rows are exact binding/materialization or downstream work, not speculative demands for new infrastructure.

| ID | Exact unit / accountable boundary | Required closure before use |
|---|---|---|
| QG-DEP01 | Separate authorization-owner action/rule/target amendment, section 5 | Approved dedicated action, human mode, scoped grant posture and exact closed rule/extractor/result selection. Existing actions unchanged; real authorized-rule bindings and grant instances required |
| QG-BIND02 | Source-owner tagged profile and package/event/commit binding, section 4 | Approved `AuthorizationEvidenceQualification v0.1` member of the proposed decision-evidence package, explicitly classified GovernanceEvent / governance decision; no blanket evidence-record assumption |
| QG-BIND03 | Source-owner effect-intent schema, target/scope extractor, result contract and trace profile | Exact content-addressed schemas/contracts, closed derivations, support/attestation checks, six relationships, one-result postconditions and external full-byte digest profile |
| QG-BIND04 | Source-to-transaction binding review | Real mapping of original commit proof, already-committed targets, guards, operation/attempt IDs, finalization, result/consumption/receipt membership and visibility to PR #20; no invented watermark or extra commit |
| QG-BIND05 | Source-validation examples and conformance fixtures | Real valid/invalid bytes with computed digests and expected QG-C01–C19 dispositions; original-authority near-twin and historical-authority cases must be independently reproducible |
| QG-DOWN06 | #32 classifier and observation contract, then PR #31 consumer binding | Exact authoritative incoming-set/visibility bindings, completeness and label/disclosure decisions. A valid source profile alone cannot close CP2A-DEP01 |

QG-BIND04 is a required test of the actual common protocol binding, not a finding that a new transaction protocol is necessary. The design uses no unique-current-head predicate and no history-completeness check during writing. If existing guarantees cannot substantiate an identified required guard or commit fact, report that exact failure to the transaction owner before implementation; do not silently choose locks/isolation or pre-open a generic “history service” issue.

Future non-default source materialization units are specifically: the tagged qualifier schema/digest profile; closed qualification intent schema; root/subject/basis/scope extractor; protected-result contract and validation trace; package/event/ingress binding; valid and hostile fixtures; source verifier/conformance specification. Concrete artifact paths/IDs, exact dependency versions and digests must be assigned and reviewed in their authorized materialization stage. These names do not create files or reserve current/default contracts here.

Preserve PR #11 section 24 and #21 ordering: finish and approve adjacent source/authority contracts; materialize the non-default policy/source/evidence and their exact interfaces in the authorized order; perform exact binding review and governance acceptance; run conformance; only then consider separately authorized current/default promotion and OFARM2 extraction. Do not jump from Phase A approval to schemas, runtime code or a production-ready claim.

The source handoff is usable only after its applicable acceptance and exact bindings, QG-DEP01 and all required source/transaction evidence are valid. #32 may use this draft for design review but cannot treat it as an admitted production source contract. CP2A-DEP01, other #21 gates and OFARM2 implementation gates remain open.

## 14. Review, validation and handoff limits

Decision ID: `OFARM-ISSUE33-AUTHORIZATION-EVIDENCE-QUALIFYING-RECORD-GOVERNANCE-001`.

Decision version: `1`. Status: proposed, not approved. Semantic approval must identify the reviewed exact candidate head and version; it is separate from the source-issue review and from approval of QG-DEP01. A changed decision requires its own review; this card grants no merge authority.

The issue review's main checkpoint is made concrete in section 10: a complete proposed admission path, an unauthorized near-twin, proof-failure distinctions and the later-authority case. Review should test whether the proposed authority delta is precise, the governance-classified carrier fits, every relationship has a non-circular committed-target path and no history completeness or public label is smuggled into admission.

Phase A validation is limited to source/pin checks, document structure and repository hygiene/currentness/cross-reference/guardrail checks. These do not execute the proposed schema, historical verifier, authorizer, transaction, concurrency or privacy behavior. No runtime or expensive OFARM2 baseline test is represented by these design checks.

Scope remains inside the qualifying-record source-governance design. No other candidate, active baseline/schema/index, permission, transaction/custody/public rule, runtime, approval, merge, promotion or extraction is changed. This design is a prerequisite input, not completion of the original implementation task: preserve OFARM2 #353 / PR #359 → #178 → the bounded #176 child sequence and its still-open canonical/runtime binding and implementation-card gates.

What is next: review this exact-head Phase A candidate, obtain explicit semantic direction, then separately take up the demonstrated QG-DEP01 authorization amendment and the staged source bindings. Resume #32 against approved actual source semantics; do not advance to runtime implementation from this draft alone.
