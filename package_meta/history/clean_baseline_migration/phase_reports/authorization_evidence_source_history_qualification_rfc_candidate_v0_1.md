# OFARM Authorization Evidence Source-History Qualification v0.1

Date: 2026-09-13

Status: non-authoritative Phase A candidate; exact-head review and semantic approval pending

Issue: [samovers/OFARM#32](https://github.com/samovers/OFARM/issues/32). Parent: [#10](https://github.com/samovers/OFARM/issues/10). Source prerequisite: [#33 / PR #34](https://github.com/samovers/OFARM/pull/34). First consumer: [#30 / PR #31](https://github.com/samovers/OFARM/pull/31), through **CP2A-DEP01, still open**.

Canonical base: `71ca724a8b6ec23f1655b086a6f549496d10a47f`.

## 1. Decision requested

Approve or amend this bounded reader-side design, not its implementation:

1. Classify one exact committed authorization-refusal bundle and the complete applicable history of its qualifying records. Preserve the original outcome, bytes and time.
2. Require a closed historical source inventory and a complete authoritative snapshot enumeration. An individual valid record, an empty search, a fresh refusal or an inactive writer is not that proof. Section 5 specifies what the actual source binding must establish and what remains unbound.
3. Verify each qualifying act under its original package admission, rule, authority and commitment evidence. Keep established admission, proved invalidity, missing proof and incomplete observation separate.
4. Fold verified typed relationships deterministically into the existing six public labels. Preserve branches and annotations; do not elect the newest account, interpret free text as a transition, or turn uncertainty into NONE or MIXED.
5. Treat an upheld record-content objection as a known composite posture, mapped to MIXED: it is resolved procedurally but the objection remains upheld. It is neither an open dispute nor a correction. An upheld objection to D's original basis remains DISPUTED_BASIS; an objection only to a qualifier's basis uses MIXED, avoiding a false claim about D's original basis. These are proposed classifier choices, not amendments to the source lifecycle.
6. Use a closed internal, derived read-side profile within the proposed decision-evidence package. It creates no durable history-status receipt, registry, new signing key or qualification-writing authority.
7. Bind the producer to the governed consumer invocation and its reply-valid observation. A valid producer's temporary inability to establish history differs from a missing or unadmitted producer contract.
8. Preserve PR #31's disclosure, null-field and safe-message rules. Keep all later binding, acceptance, conformance, promotion, extraction and runtime gates separate.

Approval would settle these proposed semantics at the reviewed head. It would not prove that a deployed source can supply the required snapshot, approve a writer, expand a release, close CP2A-DEP01 or authorize later stages.

## 2. Primary trust boundary and PR limit

Primary trust boundary: **authorization-evidence history classification and trusted producer determinations**.

The entire PR is this one historical Phase A document. It does not edit approved owner candidates, active law, a schema, an index or runtime code. The producer describes reliance on evidence; it does not decide current permission or whether a human's assertion is objectively true.

| Owner outside this PR | Boundary retained |
|---|---|
| PR #11 authorization and release admission | Original evaluation, action catalogue, selected admitted set, grants, principal/actorship, exact per-action rule comparison and retry eligibility |
| PR #34 source governance | Qualifier writing authority, six relationship forms, target eligibility, immutable bytes, original admission and lifecycle |
| PR #20 / PR #26 and the governed-read owner | Isolation, locking, commit guards, atomic membership, single use, reconciliation and disclosure linearization |
| PR #31 public consumer | Envelope fields, registered codes, safe sentences, disclosure policy and history-independent fallback |
| PR #29 retention and storage/custody owners | Current byte access, retention, deletion/redaction, provenance strength and key custody |
| Governance and implementation owners | Accepted law, package admission, current/default promotion, extraction, deployment and executable producer/consumer selection |

Stop before changing one of those boundaries. Name the exact missing guarantee and its owner; do not add a writer, stronger transaction, privileged reader or second policy to make a classifier test pass. A missing future schema is binding work, not by itself a reason to create another prerequisite issue.

## 3. Source pins and compatibility

Apply `PROJECT_AUTHORITY.md`: the active baseline outranks accepted RFCs, companion artifacts and machine contracts. Reader/currentness views are navigation, not new law. CP11–CP15 draft contracts remain non-default.

At the pinned canonical base, Constitution sections 7, 8, 10 and AAI-C.1–1.1 require exact authority, distinct times, preserved history and visible material qualification. Platform sections 3, 14 and AAI-P.6–6.1 retain enforcement and provenance. Alignment sections 4.3a–4.6 prohibit hiding lifecycle, truth or authority semantics in runtime conventions. The readiness and hostile-review qualification addenda do not equate a schema with release evidence.

The [accepted CP2 qualification RFC](https://github.com/samovers/OFARM/blob/71ca724a8b6ec23f1655b086a6f549496d10a47f/02_accepted_rfcs/OFARM_AI_Facing_Result_Qualification_and_Trace_Surface_RFC_v0_1.md), especially sections 2–4 and 9, requires truthful qualification without creating canonical truth or disclosure permission. The current/default `03_machine_contracts/schemas/runtime_surface/OFARM_ResultQualificationEnvelope_schema_v0_1.json` supplies the six labels; it does not supply this classifier.

All six PRs below were checked on 2026-09-13: open, draft and unmerged, based on the pinned main. Their Phase A approval records are not acceptance or executable promotion.

| Source | Exact head | Clauses used |
|---|---|---|
| [PR #34](https://github.com/samovers/OFARM/pull/34) | `c59fdbc75f26ee4694355adedd4df021f64b5131` | Sections 4, 6–9 and 11: exact root, six forms, backward committed references, original admission and producer handoff; section 13: open source bindings |
| [PR #11](https://github.com/samovers/OFARM/pull/11) | `4494924998183fe3fa7bc1b63b76a85893335044` | Sections 7.2.1, 7.4, 17.2–17.3, 18.1, 18.5, 18.8 and 24–24.1: package admission, evidence, read snapshot, digests and unresolved history closure |
| [PR #31](https://github.com/samovers/OFARM/pull/31) | `092be94f3a67497ba619295932cd0b2b1e9443f3` | Sections 5.3–5.4, 6, 9 and 11.1; C01–C04 and C31–C39 |
| [PR #20](https://github.com/samovers/OFARM/pull/20) | `98f8c4fafbae42c8f7fd931f43f53adcb4733713` | Sections 10, 12–13, 17 and 20: transaction-owned proof, atomic commitment and limits on reuse |
| [PR #26](https://github.com/samovers/OFARM/pull/26) | `e042efa2911b2ef0a61603b8e0adaa6911c03ac0` | Sections 7.1 and 8: write-only NOT_REQUIRED scope and complete guards; not the missing governed-read transaction binding |
| [PR #29](https://github.com/samovers/OFARM/pull/29) | `8e0994cae5610ac9c0d2652e02c8a8a2dd7b45c5` | Section 5: original promises versus present bytes, independent provenance and proof limits |

The six files are, respectively, under `package_meta/history/clean_baseline_migration/phase_reports/` at those exact heads:

- `authorization_evidence_qualifying_record_governance_rfc_candidate_v0_1.md`
- `authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md`
- `cp2_authorization_result_surface_and_public_reason_codes_rfc_candidate_v0_1.md`
- `governed_human_approval_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`
- `not_required_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`
- `authorization_evidence_retention_and_proof_strength_rfc_candidate_v0_1.md`

### 3.1 Re-entry after source approval

Issue #32's [earlier source checkpoint](https://github.com/samovers/OFARM/issues/32#issuecomment-5630051446) correctly stopped at missing admission/lifecycle semantics. PR #34 now has [version 2 exact-head Phase A approval](https://github.com/samovers/OFARM/pull/34#issuecomment-5654388700), following [review 5191266887](https://github.com/samovers/OFARM/pull/34#pullrequestreview-5191266887). That supplies a design input; QG-DEP01 and QG-BIND02–05 remain open. This candidate does not turn the draft source profile into a currently admitted source.

Issue #32's opening body and PR #31 refer to the earlier authorization pin `03a21f669ee04f96d444e14f00ae7212cab04803`. This candidate explicitly uses PR #11's [renewed release-scope approval](https://github.com/samovers/OFARM/pull/11#issuecomment-5634389303) at `4494924998183fe3fa7bc1b63b76a85893335044`. The revision retains the twenty action definitions and exact complete per-action rule/source-consent comparison, while distinguishing them from the immutable admitted-action set. The initial selected set remains exactly `ASSERT_OPERATION_CLAIM` and `RECEIVE_READ_DATA`, with both complete rules and all transitive dependencies. No claim-only read restriction or additional target is introduced.

PR #11's embedded older PR #34 pin and pending label remain publication history. This candidate's newer source pin and approval are explicit; no owner bytes are silently updated. Historical verification must retain the original selected package/manifest/admitted-rule proof. Current writer exclusion neither erases an old valid act nor proves no history. Overall current-policy digest equality does not replace the unchanged exact per-action grant comparison.

Compatibility conclusion: the source lifecycle is usable for this Phase A design, and the consumer's approved three-field history object remains sufficient. No inspected contract proves complete historical membership or the actual reader snapshot binding. Those obligations are made testable in sections 4–6, not declared satisfied. PR #11 section 24.1 still establishes neither writer deferral nor the need to activate a writer. PR #31's [approval](https://github.com/samovers/OFARM/pull/31#issuecomment-5624225401) leaves CP2A-DEP01 open.

## 4. Exact source universe and per-record verification

### 4.1 Root and candidate selection

The root `D` is one complete, authoritatively committed v0.2 authorization request/result/full-trace bundle with original outcome `DENY`, `REQUIRE_REVIEW` or `REQUIRE_HUMAN_APPROVAL`. Bind its exact kind, schema/version, request ID, result ID, `decisionBundleDigest`, tenant and owner-derived scope. Verify its original commit evidence. Ingress rejection, ALLOW, an uncommitted attempt, a trace fragment or v0.1 rewrapping is not an eligible root. An invalid or unverified root fails the consumer's original-result verification; it is not repaired by a history status.

The bounded universe contains potential qualifying acts about D and about any qualifier under that same exact root, together with the evidence needed to verify their original admission. PR #34 requires every qualifier to bind D, so discovery is root-keyed rather than a search of all domain history. Following only D's direct incoming links is insufficient: annotations, controls and replacements of qualifiers also matter.

The immutable source-inventory binding must identify every authoritative source location, commit-result collection and historical admission/profile path that could contain such an act at the cut. It must cover the root's entire eligible history, including former packages, imports and migrations where applicable, not only the currently executable writer or visible tenant rows. The v0.1 classifier supports PR #34's `AuthorizationEvidenceQualification v0.1` semantics only. A historically applicable but unsupported version blocks complete classification; it is not silently outside the universe.

Selection must occur before successful-admission filtering. Obtain every potentially relevant committed candidate and independently verifiable exclusions. A missing or malformed root key in a potentially relevant source cannot make that candidate disappear: the binding must resolve it through its authoritative result/intent membership or enumerate the enclosing candidate partition and prove it unrelated. If it cannot, observation is incomplete. Ordinary allegations, generic reference events, later failures and later authorization outcomes have no qualifying effect, but may be excluded only on verified type/admission grounds, not a text search or today's permissions.

No new source store is proposed. The inventory is a content-addressed mapping in the existing evidence profile's dependency closure, not a mutable history registry. It names existing governed sources and their coverage obligations; its digest does not itself prove coverage.

### 4.2 Verification before folding

For each candidate, verify PR #34 sections 6–9: exact canonical bytes/digest and immutable identity; root/tenant/scope; form-specific subject, basis, focus and predecessor bindings; original selected package/manifest/admitted-action and complete rule; original grant/principal/Party/role, validity and revocation evidence; validation, direct-human finalization, complete atomic membership and authoritative ordering. Apply the original contracts, not today's evaluator to yesterday's request.

The root bundle digest uses PR #11 section 18.8's exact projection. A qualifier's external full-byte digest uses the separately bound canonical JSON profile; it does not inherit the bundle's self-digest exclusions. Reject duplicate keys. A referenced digest is an integrity binding, not admission or completeness proof.

| Internal disposition | Treatment in this classifier |
|---|---|
| Admission established | Include the exact act and its typed edges. A present challenge to its basis does not by itself invalidate it |
| Proved invalid under its original contract | Preserve the evidence and exclude that purported act from the valid graph. It cannot open, correct, resolve or supersede anything |
| Admission not established | Preserve the unresolved candidate and limitation; no ESTABLISHED determination for the surrounding history, even if other records verify |

An invalid retrieved copy is not proof that the original committed object was invalid. Try the owner-permitted exact-source verification path; otherwise retain an unresolved input. A claim of conflicting bytes for one immutable ID cannot be collapsed into a chosen copy. A candidate dependent on an invalid predecessor cannot pass admission; one with unavailable predecessor proof remains unresolved. Missing historical grant/package bytes are not proved unauthorized admission.

Only a complete observation with every candidate either verified or independently proved ineligible/invalid can proceed. Fully proved invalid debris may coexist with an established status, including NONE: that means no valid material qualification at the cut, not a clean security audit or absence of failed acts. Inconsistent authoritative membership/order or ambiguity about the real committed object prevents that result. Separate security reporting remains with its owner.

## 5. Complete observation comes before status

### 5.1 Proposed v0.1 observation method

Use **complete authoritative snapshot enumeration** for the bounded universe. The source owner must provide an actual consistent committed view, and the observer must exhaust the relevant membership predicate in that view. A materialized index, cache, list digest or claimed watermark is not an alternative v0.1 proof method. An index may accelerate discovery only if the same authoritative snapshot's full candidate membership is independently reconciled; any unexplained difference fails the proof.

This names a read-side proof obligation, not a new persistence guarantee. PR #34 supplies exact root keys and original commitment obligations. PR #11 section 18.5 supplies the same-snapshot governed-read requirement. Neither specifies the actual collections, predicate, snapshot provider or complete reader access. **Those actual bindings are not present in the inspected sources and remain HSP-BIND02/HSP-BIND03.** No deployed positive observation or existing absence watermark is claimed here.

Let `U(D, c)` mean all potentially relevant authoritative committed candidates for D in the governed historical universe at cut `c`, before admission filtering. Let `V(D, c)` be the subset whose admission is established. These are mathematical names for the bound sources, not new stores or wire fields. To classify V, prove both the completeness of U and the treatment of every member of U.

| Required evidence | Exact obligation; failure cannot be replaced by a flag |
|---|---|
| Governed source-inventory closure | Reviewed immutable source/profile inventory maps every eligible historical admission path to the actual committed sources and root-selection predicate. It accounts for predecessor histories, imports/migrations, partitions and versions. A config list without coverage review is insufficient |
| Authoritative committed snapshot | Trusted provider/boundary identity and actual immutable snapshot proof establish one committed view containing D. Across partitions, prove a joint consistent cut under an existing owner guarantee; otherwise this method is unsupported. Do not splice independently fresh snapshots |
| Exhaustive predicate execution | Exact query/plan and parameter binding, candidate partitions, page/range completion and source-owner exhaustion evidence establish that every member of U was examined, including unreadable or unresolved candidates. A client cursor saying done, row count or response digest alone is insufficient |
| Exact set and dependency binding | The internal transcript binds candidate identities/content/commit proofs, every exclusion and every verification limitation to the same snapshot. All typed predecessors and original basis/admission evidence are verified; no filter-after-error completeness claim |
| Time/order evidence | Cut identity and its trusted observation date-time are bound by the actual provider. Original commit ordering, not asserted event times or wall-clock sorting, determines membership and backward dependencies |
| Reply binding | Section 6 binds this observation to the current consumer invocation and its owner-governed snapshot/release conditions. A transferable cached all-clear is not allowed |

The consumer does not trust an author-supplied completeness boolean. Verification must trace the snapshot and exhaustion evidence to the selected authoritative provider and its reviewed source coverage, independently of the returned list. A forged producer object, even with self-consistent hashes, cannot create that provenance.

### 5.2 Storage, visibility and failure boundaries

Records count when authoritatively committed at or before c under their original owner, not when a search index first sees them. A committed-at-c record delivered later is an omission from a purported complete observation; repair the source binding and re-observe, never backdate the reader's knowledge. A record committed after c is outside that historical cut even if its asserted event time is earlier. Section 6 separately controls whether c is still valid for this reply.

An authoritative snapshot must include all relevant admission paths; local replica freshness cannot establish this. A successor arriving before its predecessor remains unresolved until both original admission/order proofs are available. Exact replay/reference duplication is one act; different admitted IDs remain different acts, even with identical text. Unknown commit outcomes stay with the transaction/status owner and cannot be resolved by assuming absence.

The producer must have independently governed current access sufficient to verify the whole bounded universe. Viewer-level row filtering cannot establish complete history. The classifier receives no new custody or cross-tenant privilege from this document. If available permissions expose only part of the universe, it cannot establish the status; PR #31 still decides whether even that limitation may be disclosed. Hidden details may coexist with a complete internal observation only when the designated verifier actually has lawful access and the public policy separately permits the aggregate status/time.

PR #20 section 10 admits serializable coverage, explicit complete locks/version guards, or optimistic complete revision/predicate guards for its own finalization. PR #26 has corresponding write obligations and expressly does not cover RECEIVE_READ_DATA. Their writer-local positive, negative and set guards do not prove that this reader enumerated incoming history. This candidate selects no new lock, isolation level, global log, unique history head, writer participation rule or second commit.

At binding review, identify the actual source/predicate and read snapshot/release proof. If existing source and transaction guarantees supply it, bind and test them. If not, stop at the concrete missing guarantee and obtain the separate owner amendment before implementing it. Do not turn HSP-BIND03 into an invented generic history-service project, and do not call a permanently unavailable producer complete.

## 6. Observation time, fresh refusals and reply validity

Keep four times distinct: D's original evaluation/result time; each qualifier's asserted event/effective time and independently proved admission time/order; the history observation cut's trusted `asOf`; and the public reply's `qualifiedAt`. A timestamp alone cannot identify a snapshot or prove order. Equal clock values do not imply equal cuts; source-native ordering proof remains internal.

Use a newly acquired owner-governed observation for this invocation, not a caller-selected date or a cache TTL. For RECORDED_RESULT, the cut must be the governed read snapshot covering authorization, retrieval, redaction, qualification, coverage and buffered payload under PR #11 section 18.5. Other required public/transaction facts retain their own exact owner bindings. For CURRENT_ATTEMPT, D must first be authoritatively committed, and the history cut must be admitted by the current reply's owner protocol and contain D.

The source observer and consumer must reject a cut that their existing owner rules have invalidated. If they learn of a potentially material committed candidate after c but before finalizing the reply, they must not deliberately keep c to hide it. Obtain a new complete owner-governed observation and rebuild/revalidate the affected reply, or use the permitted unavailable/withheld path. An unverified new candidate is reason to refresh or report a limit, not permission to ignore it because its status is not known yet.

Refreshing history cannot splice a new history snapshot into an old governed-read payload. Rebuild through the owning same-snapshot read protocol. If the payload/evidence is already finalized, the classifier cannot rewrite it or add an explanation commit: the owner must suppress/restart the release or use its permitted failure path. The later read binding must demonstrate this boundary. This PR invents neither a retry permission nor a new commit protocol.

A complete as-of observation is not a promise that no later record can exist. A genuinely post-cut act is outside that observation; real race tests must distinguish it from a pre-cut act hidden by replica/index lag. Existing transaction/read release guards still control disclosure. No new requirement to lock the history until network delivery is introduced.

### 6.1 Can a refusal-commit cut establish NONE?

**Yes, conditionally, but never from recency or causality alone.** The same cut must satisfy all section 5 evidence, contain D's verified first commitment and satisfy this invocation's reply-validity rules. Every candidate must be resolved, and section 7's fold must produce NONE. This is an ordinary complete observation whose cut happens to coincide with the refusal commit, not a separate shortcut.

PR #34 section 7.3 requires a valid qualifier's targets to be committed and observable before its transaction starts. Therefore, if that rule covers the entire historically eligible universe and original identity/order are proved, a qualifier newly targeting D cannot precede D's first commit. This is a consistency check, not evidence of source-inventory closure, complete enumeration, absence of conflicting/imported candidates or current reply validity. The original refusal transaction's receipt normally proves its own atomic set, not U(D, c).

If Q commits between D's commit and the required read/reply cut, include Q. If the producer learns of Q before completing a reply using the earlier cut, refresh as above; do not rely on the earlier causal argument. If complete proof is unavailable, emit no invented NONE. PR #31 permits UNAVAILABLE, or policy-prioritized WITHHELD, only for an otherwise permitted limited reply. A missing producer/read binding remains a readiness failure despite such a reply.

### 6.2 Reader versus writer release closure

Verifying an old valid act is distinct from permission to write a new one. Its originally selected admitted package may differ from today's package. A current package excluding qualification writing can, in principle, consume independently verifiable historical evidence; enabling a writer cannot repair missing original proof or missing observation.

This is not proof that authoring can be deferred in the initial claim/read release. HSP-BIND02/03 must demonstrate the actual historical universe, admission evidence, complete cut and reply path for that exact release. Conversely, this candidate identifies no reason to enable a writer merely to interpret evidence. The initial two-action set and all four package families remain unchanged. Any needed QG-DEP01 action definition/admission or release expansion requires its own approval and complete gates, not a second selected-policy workaround.

## 7. Deterministic fold of the verified graph

Only run this fold after sections 4–6 establish complete, reply-valid input. All six source forms retain PR #34's meaning. The fold describes material reliance limitations, not truth adjudication. Free-text similarity, alleged severity, timestamps and actor rank never choose a winner.

In this bounded profile, every valid typed qualification under D is material unless its explicit source control/replacement semantics remove the particular current posture below. There is no caller-selected materiality filter or silent dismissal of an inconvenient annotation. Preserve the entire original graph internally; the fold calculates a view, not new canonical state.

### 7.1 Dispute control branches

For each OPEN_RECORD_DISPUTE or OPEN_BASIS_DISPUTE origin, construct its exact control graph using only RESOLVE_DISPUTE and REOPEN_DISPUTE edges. Follow the verified origin/focus/basis unchanged. A control leaf is a node with no observed valid control child in this complete graph. Correction, supersession and separate dispute annotations do not count as control children.

| Leaf / branch posture | Contribution |
|---|---|
| OPEN_RECORD_DISPUTE or REOPEN_DISPUTE with record origin | `O`: an open record-content dispute |
| OPEN_BASIS_DISPUTE or REOPEN_DISPUTE with basis origin focused on D | `B`: disputed original supporting/admission basis of D |
| OPEN_BASIS_DISPUTE or REOPEN_DISPUTE with basis origin focused on a qualifier | `K`: the history's supporting/admission basis is disputed, not necessarily D's original basis |
| RESOLVE_DISPUTE / WITHDRAWN | No current contribution from this branch; it does not clear another branch or annotation |
| RESOLVE_DISPUTE / UPHELD with basis origin | `B` if its focus is D, otherwise `K`: the basis objection remains upheld; no assertion that original admission was invalid |
| RESOLVE_DISPUTE / UPHELD with record origin | `K`: known composite posture, objection upheld but procedure resolved; not O, CORRECTED or NONE |

Within one origin, compare the leaf postures `OPEN`, `UPHELD`, `WITHDRAWN`. Different postures on concurrent leaves set `K` in addition to their contributions. Several leaves with the same posture preserve their identities but do not alone set K. A reopened resolution ceases to be a leaf on that branch; its history is retained. Multiple separate origins of the same category do not alone make MIXED.

`K` is an internal fold fact, not a seventh public status. Mapping an upheld record objection to MIXED deliberately uses PR #31's truthful generic material-history sentence. Calling it OPEN_DISPUTE would falsely claim the resolution had not occurred; calling it CORRECTED would invent a separate act. This particular choice requires semantic review.

Likewise, the source owner permits a basis dispute about a qualifier's own authorization, validation or support. That exact basis is not automatically D's original authorization basis. Its outstanding or upheld objection sets K rather than B so that the consumer does not falsely display that D's original basis is disputed. Withdrawal clears only that branch's contribution. No target is changed to obtain a more specific label.

### 7.2 Correction and replacement assessments

Group CORRECTION and SUPERSEDE records by their exact assessment focus from PR #34. A correction's focus is its subject. A root SUPERSEDE has focus D; another SUPERSEDE inherits the identical focus of all named predecessors. Retain every replacement edge from a new SUPERSEDE to the exact earlier root or assessment(s) it names.

An assessment tip is a CORRECTION or SUPERSEDE not named as a predecessor by any valid observed SUPERSEDE. Removed tips never revive when their successors are themselves replaced: the earlier edges remain. More than one tip at the same focus sets K, meaning multiple unreconciled accounts. This is a structural rule even if the text appears compatible; the classifier does not decide semantic agreement. One explicit same-focus successor naming every competing tip can remove that particular multiplicity, but does not claim unseen tips or clear other histories.

Each surviving tip contributes as follows:

- A CORRECTION contributes `C`.
- A SUPERSEDE whose backward replacement ancestry reaches D itself contributes `S`. Only an explicit root-replacement lineage has this effect.
- A SUPERSEDE of a correction lineage without such a root-replacement ancestry contributes `C`: it replaces a corrective account, not D. This avoids displaying that the original evidence was superseded merely because a correction was replaced.

Every SUPERSEDE must reach either D or at least one CORRECTION through its replacement ancestry; otherwise its claimed source graph fails verification. A same-focus successor merging a root-replacement lineage and correction tips contributes S; the named correction tips no longer contribute separately. Other surviving tips and annotations still do.

A correction of a correction has its own focus and contributes C without rewriting the first correction. A correction or dispute about a resolution/reopening does not resolve or reopen the original dispute. Histories of replaced assessments remain in scope: replacing an account does not erase independent annotations about it or close its disputes. Thus a remaining correction/dispute about a replaced record can combine with S. This conservative materiality rule is explicit, not a hidden current-state convention.

### 7.3 Exhaustive label composition

Collect distinct contributions from every origin and assessment focus. Let `L` be the subset of `{O, B, C, S}` and let K record the known composite/multiple-account conditions above. Multiplicity within one category does not by itself add another category, except the explicit same-focus assessment-tip rule. Apply exactly this table:

| Complete verified fold | Existing public label | Meaning in this profile |
|---|---|---|
| K present, or two or more distinct members of L | MIXED | Known material qualifications cannot be represented by one more specific label; includes upheld record objections, qualifier-basis objections and unreconciled branches/accounts |
| No K; L empty | NONE | No applicable material limitation under these rules at the proved cut; not no records, perfect evidence or current permission |
| No K; L = {O} | OPEN_DISPUTE | Open record-content dispute(s), including supported histories of qualifiers |
| No K; L = {B} | DISPUTED_BASIS | Open/reopened or upheld dispute(s) of D's exact original selected basis |
| No K; L = {C} | CORRECTED | A linked correction or its surviving corrective replacement account qualifies the history |
| No K; L = {S} | SUPERSEDED | An explicit root-audit replacement lineage qualifies D, with no other remaining category or structural multiplicity |

This table is exhaustive after verified finite graph construction. Missing bytes, unsupported versions, incomplete sets, unresolved links or conflicting authoritative proofs do not enter L/K and cannot produce MIXED as an uncertainty fallback. They prevent ESTABLISHED. A graph may be valid and branched, yielding MIXED; a graph whose validity cannot be established is a different case.

Different valid evaluation orders, page order or duplicate transport deliveries must produce the same graph and status. Stable sorting by immutable IDs is permitted for transcript serialization only, never for precedence. Source ordering must prove a finite acyclic dependency graph; sorting a cycle or dropping its last edge is not a repair.

## 8. Closed producer contract and trusted responsibility

### 8.1 Minimal carrier and producer role

Propose `ofarm.authorization-evidence.source-history-qualification.v0.1`, a closed derived read-side profile bound within the proposed `AuthorizationDecisionEvidence v0.2` package. This is an internal determination about existing records, not a new GovernanceEvent, accepted domain consequence, persistent history head or protected source result. Its proof transcript may be included in existing governed read/qualification evidence where that owner's contract requires it; this profile requires no additional durable write.

The authorization-evidence owner governs the classifier profile, rule digest and source verification procedure. A separately reviewed trusted runtime/consumer binding names the designated producer and authoritative observation verifier, their exact executable/profile identities, permitted source scope and invocation path. The public projector may consume the result but may not discover history, run a private alternative fold or assert producer authority from an authenticated caller identity.

The initial interface is internal to the governed runtime trust domain. Provenance comes from the independently selected runtime binding and protected invocation path, not a caller-populated `producerId` or a self-signed result. This document creates no network service, remote attestation, signer or new secret custody. If a deployment requires a new cross-process trust mechanism or wider read authority, it needs the separate owner binding/approval; a JSON signature is not an assumed substitute.

### 8.2 Versioned internal command

The command has exactly these required top-level members; unknown members, duplicate keys, unsupported versions and incomplete nested records fail validation. The later schemas must close every nested record too. These are semantic field specifications, not placeholder JSON fixtures.

A content binding below has exactly `ref` and `digest`, resolved and verified under the referenced artifact's admitted immutable identity/digest profile. The command does not choose a digest algorithm or treat a mutable URL as an immutable ref. `rootBinding` has exactly `kind`, `schemaBinding`, `requestId`, `resultId`, `decisionBundleDigest`, `tenantId` and `scopeBinding`; its schema/scope bindings are content bindings to the owner-defined objects. `invocationBinding` has exactly `invocationId`, `consumerBinding`, `mode` and `ownerContextBinding`; the two bindings are content bindings. Their referenced owner-context schemas must distinguish the two modes below without arbitrary extension fields. Ref syntax, canonical bytes, field types and all nested proof schemas remain exact-byte materialization obligations, not an invitation to accept untyped metadata.

| Member | Closed meaning |
|---|---|
| `profileVersion` | Exactly `ofarm.authorization-evidence.source-history-qualification.v0.1` |
| `contractBinding` | Exact immutable profile/package ref and digest; its reviewed closure uniquely selects fold rules, root/qualifier schemas, historical source inventory, proof schemas and observation/producer bindings. No caller-selected alternatives |
| `rootBinding` | Exact root kind `AUTHORIZATION_REFUSAL_BUNDLE`, schema/version, request ID, result ID, decisionBundleDigest, tenant and owner-derived scope binding from section 4; complete original source/commit proof is resolved through the owner, not asserted by the caller |
| `invocationBinding` | Trusted invocation identity, consuming profile ref/digest, CURRENT_ATTEMPT or RECORDED_RESULT, and the exact owner context ref/digest. Current mode binds the original attempt/confirmed commitment and current reply context; recorded mode binds the governed lookup/read snapshot context. Neither is an access credential |

The ordinary caller may supply the consumer's allowed lookup/request inputs, not this trusted command's policy, cut, candidate set, producer or proof. The selected producer resolves authoritative source evidence itself through the bound interfaces. It cannot accept a user-provided array of qualifiers as the complete universe. Candidate bytes offered for authorized comparison remain untrusted until independently bound to the original object and source membership.

### 8.3 Output alternatives and proof transcript

A valid output has exactly `profileVersion`, `contractBinding`, `rootBinding`, `invocationBinding`, `producerBinding` and `determination`. The first four must exactly match the trusted command; producerBinding must match the independently selected runtime role/scope and invocation evidence. All refs/digests follow their actual admitted profiles. The result is invocation-bound, not a reusable all-clear or authorization token.

`producerBinding` has exactly `runtimeRoleBinding` and `implementationBinding`, both content bindings. They identify the selected producer and observation-verifier path; they do not authenticate their own bytes. The protected invocation supplies independent provenance. `contractBinding` is a content binding to the complete selected profile closure, not a bag of optional policy refs.

`determination` is exactly one closed alternative:

| Alternative | Required members and constraints |
|---|---|
| `ESTABLISHED` | `kind`, `asOf`, `disputeStatus`, `proof`. asOf is the actual cut's trusted date-time; disputeStatus is exactly one of the six existing labels. proof is the fully bound internal transcript below |
| `UNAVAILABLE` | `kind`, `asOf`, `disputeStatus`, `limitations`. Both asOf and disputeStatus are null. limitations is a nonempty, duplicate-free collection from the closed internal classes below, with typed evidence references permitted only inside the trusted boundary |

The ESTABLISHED proof has exactly five components, with separately materialized closed schemas and real source bindings:

1. `observation`: source-inventory binding, provider/boundary identity, actual snapshot proof and trusted cut-time mapping, exact predicate/query/plan/parameters, complete range/page/source coverage and independent exhaustion evidence from section 5.
2. `sourceVerification`: the exact root proof plus complete candidate membership and per-candidate established-admission or independently proved-invalid/ineligible disposition, with original source/authority/package/commit/order evidence. No unresolved candidate is permitted in this branch.
3. `graph`: normalized immutable identities and verified typed subject, focus, origin/basis, control and replacement edges. A transcript is not a new source of those relationships.
4. `fold`: exact rule binding, control leaves, assessment tips, L and K with their source witnesses, and resulting existing label. This is reproducible from sourceVerification/graph, not an opaque classifier score.
5. `replyValidity`: exact consumer invocation/owner context and proof that this cut meets section 6 and the existing read/reply owner's conditions. It cannot be a bare valid-until field or producer assertion.

A transcript digest binds its canonical bytes externally without a self-hash cycle; it proves neither authenticity nor completeness by itself. References resolve only through the selected trusted interfaces and current access rules. No internal candidate counts, IDs, rule/grant refs, support, proofs or producer diagnostics become public fields.

The closed UNAVAILABLE limitation classes are `OBSERVATION_UNAVAILABLE`, `REQUIRED_EVIDENCE_UNAVAILABLE`, `SOURCE_VERIFICATION_FAILED`, `UNSUPPORTED_OBSERVED_INPUT`, `INCONSISTENT_AUTHORITATIVE_EVIDENCE`, `REPLY_OBSERVATION_INVALIDATED` and `VERIFICATION_ACCESS_UNAVAILABLE`. Each limitation has exactly `class` and `evidenceBindings`, an array of available content bindings to the selected proof schemas; it may be empty when no evidence object can lawfully be supplied. Classes must be unique across the nonempty limitations array. They describe this valid invocation's proof limit, not a public code, negative authority decision or assertion that a record is absent. Preserve all applicable classes; their order cannot change the public result. The materialized schema must constrain the referenced proof families to the exact admitted closure; arbitrary diagnostic strings or untyped metadata are forbidden at this interface.

### 8.4 Missing contract is not ordinary unavailability

An absent/unadmitted producer profile, unresolved dependency closure, wrong selected executable, unbound historical source universe, unsupported command version or substituted invocation is an **interface/binding failure**, not a valid output from this contract. Reject it and keep the relevant readiness gate open. The trusted public consumer may still use its already approved limited-reply behavior when allowed, but that handling cannot certify an installed producer.

A correctly selected, completely bound producer can instead return UNAVAILABLE when an otherwise supported observation temporarily fails or required evidence cannot be established. A newly encountered historically applicable unsupported source version also prevents the current observation and requires binding review; repeated UNAVAILABLE cannot hide an incomplete supported universe. Neither failure path grants a fallback profile or private enum. Invalid original-result proof cannot be downgraded merely to unavailable history.

### 8.5 Consumer verification procedure

1. Independently verify the original committed refusal and current permission for the requested public surface. Select the admitted producer/consumer profile and runtime binding through the trusted owner path, not response fields.
2. Build the closed command from exact owner facts. Reject missing contract/dependency bindings before treating any output as governed producer evidence.
3. Verify output shape/version, protected invocation provenance, selected producer identity/scope and exact contract/root/invocation equality. Reject cross-tenant, wrong-result, replayed invocation or substituted package/cut.
4. For ESTABLISHED, use the designated observation/source-proof verifier bound by the contract to validate the five proof components, completeness and reply validity. The verifier must bind the reproducible fold to this result. The public projector consumes this verified result; it does not invent its own classification. Hash equality or a claimed trusted flag alone never passes this step.
5. For UNAVAILABLE, verify the valid producer/invocation and null fields; retain the internal proof limits. A malformed or forged output is rejected rather than repaired into an apparently successful determination.
6. Apply PR #31's current disclosure policy independently, including withholding precedence, safe messages and its permitted fallback. No read or retry permission comes from the history determination. Do not release a payload whose governing snapshot/release proof has failed.

## 9. Public and retention handoff

The internal producer does not emit WITHHELD or decide what the human may see. PR #31 owns that policy. Its `sourceHistoryQualification` remains exactly `availability`, `asOf`, `disputeStatus`; root disputeStatus remains forbidden in the authorization branch.

| Independently permitted public observation | Existing PR #31 output |
|---|---|
| Status/time disclosable and valid ESTABLISHED proof | AVAILABLE, actual history asOf and exact six-label result |
| Status/time disclosable but no trustworthy determination | UNAVAILABLE, null asOf and null disputeStatus, only where the limited reply is otherwise permitted |
| Status or observation time not disclosable | WITHHELD, both null, whether the producer knows the history, knows it empty or cannot observe it |
| Details restricted but status/time permitted | Keep AVAILABLE and truthful status/time; existing DETAILS_REDACTED and matching permission/absence posture |

Use PR #31 section 6's unchanged exact safe sentences for each non-NONE status and both unavailable/withheld alternatives. Its original outcome/code, root asOf, recorded-not-current label, trace posture and retry restrictions remain unchanged. A later ALLOW or changed grant is not a correction or permission to retry the old operation.

If policy does not permit both the original category and the required limited statement, use the governing lookup's permitted qualified failure, not a newly invented DENY or private reason code. For equivalent readable originals, changing only undisclosable history must change neither limited-reply versus exclusion choice, response/failure category, display, hints, references nor omission pattern. The reader/scope/record-class policy must be selected independently of hidden history. Test both uniform policy paths under CP2A-C38; an access-denied original gains no existence signal.

PR #29 remains controlling: original RETAINED_BYTES promise is not present byte availability; DIGEST_ONLY does not reconstruct a record, prove origin or grant comparison access. Independently supplied candidate bytes may be compared only through the authorized exact-profile verifier and still need original admission and complete membership proof. Missing bytes, denied access, redacted derivatives and integrity failure remain distinct internal limits. Optional diagnostic loss need not destroy an otherwise proved determination; loss of proof required by sections 4–6 does. The producer cannot weaken required evidence merely because retention expired.

## 10. Worked positive and hostile paths

The symbols below describe future test objects, not existing records, concrete fixture bytes, invented digests or executed conformance. Every ESTABLISHED example assumes the real admitted profile/source/observation/producer bindings in sections 4–8. Their present absence is not filled by these examples.

### 10.1 Complete empty observation, including a fresh refusal

D is a verified committed DENY. A designated observer lawfully enumerates the entire reviewed authoritative candidate partition at the owner-bound snapshot c containing D. Its independent provider/exhaustion proof, version/admission coverage, exclusions and reply binding all verify. There are no valid qualifying acts and no unresolved candidates. The graph is empty, L is empty and K absent, so the result is ESTABLISHED / NONE at c. A permitted public reply is AVAILABLE / NONE, retaining the original DENY/time.

For a fresh D, c may equal the first-commit cut only with the same complete proof and reply conditions; the receipt's recency is irrelevant. If a pre-cut hidden candidate exists, the asserted exhaustion proof must fail. If a known post-cut candidate arrives before completion, section 6 requires a refreshed owner observation or the permitted limited path. These near-twins distinguish a positive mechanism from a hard-coded NONE.

### 10.2 Historical correction while new authoring is excluded

Q is a valid CORRECTION of D, originally admitted under an exact package that admitted its defined action, with all original rule/grant/finalization/atomic proof retained. Today's selected package excludes that action. The lawful historical verifier establishes Q's original admission without granting current authoring power. Complete snapshot enumeration at c establishes that Q is the sole assessment tip and no other material history exists. L = {C}, K absent: ESTABLISHED / CORRECTED. D remains DENY. A disclosable reply uses PR #31's linked-correction sentence, not a new outcome.

If only Q's original package proof is missing, admission is not established and the result becomes UNAVAILABLE, not proved invalidity or NONE. If independent original proof instead establishes that Q's action was excluded then, Q is not a valid qualification; a complete otherwise empty history can yield NONE. Today's later inclusion cannot rescue it. No actual historical package, valid Q or working closed reader is claimed by this hypothetical path.

### 10.3 Branches and annotations

For one record dispute O, complete cuts after O, after WITHDRAWN resolution W, and after REOPEN_DISPUTE R yield OPEN_DISPUTE, NONE, OPEN_DISPUTE, respectively, if nothing else contributes. A correction about W's text does not reopen O: W alone plus that correction yields CORRECTED. A sole UPHELD record resolution yields MIXED, not an open dispute or invented correction. The corresponding basis-dispute progression focused on D uses DISPUTED_BASIS, NONE, DISPUTED_BASIS; its sole UPHELD resolution yields DISPUTED_BASIS. A new basis dispute about W's own admission/support instead yields MIXED: it qualifies the withdrawal history without inventing a challenge to D's original basis or reopening O.

Concurrent UPHELD and WITHDRAWN resolutions under one opener yield MIXED. Reordering their delivery cannot choose a winner. Two unresolved record-dispute origins alone yield OPEN_DISPUTE, while record and basis origins together yield MIXED. Missing original admission evidence for either branch prevents ESTABLISHED rather than resolving the conflict by omission.

### 10.4 Replacement chains and restricted histories

For D, direct root replacement S1 followed by replacement S2 of S1 remains SUPERSEDED; D does not revive. Competing same-focus successor tips S2 and S3 yield MIXED. A valid new S4 naming both reconciles that multiplicity and yields SUPERSEDED if no other contribution remains. It does not close an independent dispute about S1: that dispute combines with S to yield MIXED.

For correction C1 of D, replacing C1 by C2 of form SUPERSEDE preserves CORRECTED, because the replacement ancestry reaches a correction, not D itself. Correcting C1 also creates a separate-focus C contribution without changing C1's relationship. Two unmerged correction tips for D yield MIXED; a same-focus successor naming both yields CORRECTED. All histories remain observed.

If a trusted observer sees a complete corrected history but the viewer may see only the status/time, the public result stays CORRECTED with details redacted. If the status/time is hidden, corrected and uncorrected near-twins both use the same policy-selected WITHHELD reply or the same permitted exclusion path. The producer's privileged knowledge cannot choose that path. If the producer itself cannot lawfully observe the whole set, it establishes no status.

## 11. Invariants and required case specifications

Case levels: **SHAPE** means later schema/closed-field checks; **SEMANTIC** means later source/proof/fold fixtures and binding review; **RUNTIME** means actual production-reachable source, transaction, race, access and adapter evidence. None is claimed executed by this Phase A document. An internal rejection does not invent a public error code.

| Invariant | Requirement |
|---|---|
| HSP-I01 | Exact committed root, immutable content and tenant/scope; no original-outcome/time rewrite |
| HSP-I02 | Closed historical universe and exhaustive authoritative snapshot proof precede every established status, including NONE and non-NONE |
| HSP-I03 | Original admission, proved invalidity, missing proof and whole-set completeness remain separate; no current-package re-admission |
| HSP-I04 | Only typed controls/replacements change the relevant posture; branches and qualifier histories remain visible; no newest-wins or free-text transition |
| HSP-I05 | Deterministic exhaustive six-label fold; known composite facts differ from uncertainty; no seventh public status |
| HSP-I06 | Actual trusted cut, distinct times, same-snapshot/reply validity and no fresh-commit or cached all-clear shortcut |
| HSP-I07 | Closed invocation-bound producer contract, independently selected role/provenance and consumer verification; no caller authority |
| HSP-I08 | Disclosure and retention limits remain separate; withholding precedence and both hidden-history-independent fallback paths |
| HSP-I09 | No new writer, release expansion, transaction, custody or public rule; all later gates and readiness limits remain explicit |

| Case | Required result | Level / invariants / owner link |
|---|---|---|
| HSP-C01 — complete fresh DENY | Section 10.1: NONE only with complete actual source/cut/reply proof; original result unchanged | SEMANTIC + RUNTIME; I01/I02/I06; CP2A-C01/C39 |
| HSP-C02 — other fresh refusals | Independently bound REQUIRE_REVIEW and both human-required owner variants retain their meanings; same NONE proof obligation | SEMANTIC + RUNTIME; I01/I02/I06; CP2A-C02–C04 |
| HSP-C03 — fresh but no observation | Receipt/clock alone cannot produce NONE; permitted UNAVAILABLE/WITHHELD, no readiness claim | SEMANTIC + RUNTIME; I02/I06/I09; CP2A-C39 |
| HSP-C04 — historical complete empty graph | NONE after exhaustive historical/profile coverage, not empty visible search | SEMANTIC + RUNTIME; I01/I02/I06; CP2A-C23/C34 |
| HSP-C05 — historical correction, writer now excluded | Section 10.2 yields CORRECTED with original package proof; no new authoring power | SEMANTIC + RUNTIME; I01/I03/I09; CP2A-C31, QG-C16/C20 |
| HSP-C06 — missing original package/grant proof | UNAVAILABLE, not original invalidity, current re-admission or NONE | SEMANTIC; I02/I03; QG-C14/C16 |
| HSP-C07 — proved excluded original act | Exclude proved invalid act; later grant/package inclusion cannot rescue it; NONE only with complete otherwise clean proof | SEMANTIC; I02/I03; QG-C16/C20 |
| HSP-C08 — lone record versus basis dispute | OPEN_DISPUTE versus DISPUTED_BASIS from exact original typed focus/basis; outstanding basis objection focused on a qualifier yields MIXED, not a claim about D's original basis | SEMANTIC; I04/I05; CP2A-C35, QG-C05 |
| HSP-C09 — withdrawal and reopening | O → W → R yields open → none → open for that branch; other contributions preserved | SEMANTIC; I04/I05; QG-C07 |
| HSP-C10 — upheld objections | Record UPHELD yields MIXED; basis UPHELD yields DISPUTED_BASIS only for D's basis, otherwise MIXED; neither creates correction or invalidates original admission | SEMANTIC; I03/I04/I05 |
| HSP-C11 — concurrent resolution branches | UPHELD/WITHDRAWN or OPEN/resolved leaves under one origin yield MIXED; same-posture leaves are not alone a conflict | SEMANTIC + RUNTIME; I04/I05; QG-C13 |
| HSP-C12 — correction of correction/control | Separate focus stays observed; correction of W never reopens its original dispute; a basis dispute about W yields MIXED without changing O's control leaves | SEMANTIC; I02/I04/I05; QG-C06/C07 |
| HSP-C13 — root supersession chain | S1 → S2 remains SUPERSEDED; no root revival or outcome change | SEMANTIC; I01/I04/I05; QG-C08, CP2A-C35 |
| HSP-C14 — competing/merged successors | Multiple same-focus tips yield MIXED; explicit complete observed-tip merge can remove that multiplicity, not other annotations | SEMANTIC + RUNTIME; I04/I05; QG-C08/C13 |
| HSP-C15 — corrective replacement | Replacement of correction(s) without root-replacement ancestry stays CORRECTED; two unmerged same-focus corrections yield MIXED | SEMANTIC; I04/I05 |
| HSP-C16 — dispute on replaced assessment | Dispute is not silently closed; combine its contribution with remaining replacement/correction posture | SEMANTIC; I02/I04/I05 |
| HSP-C17 — same-category versus mixed | Two separate open record origins yield OPEN_DISPUTE; record plus basis or correction plus dispute yield MIXED | SEMANTIC; I04/I05; CP2A-C35 |
| HSP-C18 — cycles/unsupported edges | Invalid self/future/same-atomic-set or mixed-focus references rejected; missing order/predecessor proof stays unresolved, not timestamp-repaired | SHAPE + SEMANTIC; I03/I04; QG-C09 |
| HSP-C19 — direct-only or filtered discovery | Hidden/nested qualifier, malformed root key or omitted partition fails complete observation; preserve a valid Q's individual admission but no status from the remaining valid subset | SEMANTIC + RUNTIME; I02/I03; CP2A-C34, QG-C18 |
| HSP-C20 — fake completeness | Empty result, list digest, cache version, nominal watermark, per-writer guard or caller complete flag cannot replace authoritative exhaustion | SHAPE + SEMANTIC + RUNTIME; I02/I07; QG-C18 |
| HSP-C21 — before/after cut and late delivery | Pre-cut committed delayed Q defeats incomplete replica proof; genuine post-cut Q is outside c, subject to reply refresh when known; no event-time backdating | SEMANTIC + RUNTIME; I02/I06; QG-C13 |
| HSP-C22 — correction between commit and reply | Include at later required cut; known new candidate invalidates use of earlier cut; no fresh NONE shortcut or snapshot splicing | RUNTIME; I02/I06; CP2A-C39 |
| HSP-C23 — multi-source cut or snapshot loss | Unproved joint cut, page snapshot change or lost exhaustion proof prevents ESTABLISHED; no new distributed transaction inferred | SEMANTIC + RUNTIME; I02/I06/I09 |
| HSP-C24 — replay/order/identity conflict | Exact replay counted once; permutations same status; distinct IDs preserved; conflicting committed identity cannot be repaired by last-write-wins | SEMANTIC + RUNTIME; I03/I04/I05; QG-C12 |
| HSP-C25 — other result/tenant/source substitution | Wrong root kind, tenant/scope, digest or immutable IDs rejected; later changed-permission result alone has no qualifying effect | SHAPE + SEMANTIC; I01/I03/I07; CP2A-C20/C35/C36 |
| HSP-C26 — forged producer or policy | Caller-selected profile/cut, arbitrary array, authenticated identity alone, fabricated provenance or replayed invocation rejected | SHAPE + SEMANTIC + RUNTIME; I02/I07 |
| HSP-C27 — unsupported historical version | Do not filter by current v0.1 support/current action set; block observation and require exact universe/binding review | SEMANTIC; I02/I03/I07/I09 |
| HSP-C28 — missing producer versus outage | Absent/unadmitted/unbound contract is readiness failure; valid bound producer's failed observation is UNAVAILABLE; neither completes CP2A-DEP01 | SEMANTIC + RUNTIME; I07/I09; CP2A-C39 |
| HSP-C29 — internal output shape | Wrong enum/version/extra field; non-null unavailable status/time; missing established proof; arbitrary limitation string all rejected | SHAPE + SEMANTIC; I05/I07 |
| HSP-C30 — hidden details | Established CORRECTED with disclosable status/time remains AVAILABLE plus existing redaction posture, no IDs/counts | SEMANTIC + RUNTIME; I08; CP2A-C32 |
| HSP-C31 — hidden qualification | WITHHELD precedes known/empty/unavailable history; status/time null and existing safe sentence | SEMANTIC + RUNTIME; I08; CP2A-C33/C36 |
| HSP-C32 — paired limited reply and fallback | Both CP2A-C38 policy paths preserve category/display/hints/refs/omissions for otherwise equal originals differing only in hidden history | RUNTIME; I08; CP2A-C38 |
| HSP-C33 — public shape and safe messages | Only nested three-field object; root disputeStatus always rejected; fixed sentences including MIXED; no original-outcome/retry change | SHAPE + SEMANTIC + RUNTIME; I01/I05/I08; CP2A-C31–C37 |
| HSP-C34 — retention/copy/proof limits | Digest-only, missing original bytes, denied access, redacted derivative and bad copy stay distinct; unresolved required proof prevents status; optional diagnostics do not invent failure | SEMANTIC + RUNTIME; I03/I08; QG-C14, CP2A-C25/C34 |
| HSP-C35 — privileged versus filtered observer | Lawfully complete internal observation may feed permitted redacted status; viewer-filtered or unauthorized observation never proves completeness | SEMANTIC + RUNTIME; I02/I07/I08 |
| HSP-C36 — release/dependency near-twins | No third action, policy fallback, permanent-unavailable success stub or promotion from draft tests; historical read/new-write separation needs actual binding proof | SEMANTIC + RUNTIME; I03/I09; QG-C20, PR #11 section 24.1 |

`I01`–`I09` abbreviate HSP-I01–HSP-I09 in the tables. Cases requiring full source/proof bindings must be marked NOT EXECUTED or BLOCKED at a stage without those bindings, not passed from illustrative arrays. Positive cases must enter the real producer/consumer path at runtime; helper-only fold tests cannot establish complete observation or privacy.

| Issue #32 criterion | Design / invariants | Case and review evidence |
|---|---|---|
| 1. Source inventory/minimum carrier | Sections 3–5, 8.1; I02/I03/I09 | C05–C07/C19/C20/C27; actual inventory/package binding review |
| 2. Producer responsibility/authority | Section 8; I07/I09 | C26/C28/C35; independent runtime role/source-access binding |
| 3. Exact source binding | Sections 4, 8; I01/I03/I07 | C05–C07/C18/C24/C25 |
| 4. Deterministic six meanings | Section 7; I04/I05 | C08–C18/C24; explicit upheld-record and corrective-replacement semantic review |
| 5. Observation/completeness | Sections 4–6; I02/I03/I06 | C01/C04/C19–C23/C27/C35; actual provider/predicate/exhaustion evidence |
| 6. Fresh refusal | Section 6.1; I01/I02/I06 | C01–C03/C21/C22; CP2A-C01–C04/C39 |
| 7. Verifiable I/O | Section 8; I07 | C25–C29; closed schema, provenance, rule/root/cut equality |
| 8. Public/retention compatibility | Section 9; I01/I03/I08 | C30–C35; CP2A-C31–C39 and original-result proof limits |
| 9. Named invariants/cases | Sections 10–11; I01–I09 | C01–C36; distinguish shape, semantic and actual runtime evidence |
| 10. Later units/closure | Sections 12–13; I09 | C28/C36; exact-byte cross-binding, stage evidence and open dependency ledger |

## 12. Later units, ownership and closure gates

These are proposed destinations, not created assets or approved current/default names. Confirm placement conventions at the separately authorized non-default materialization stage; a placement adjustment cannot alter semantics without review. Refs/digests must be calculated from actual reviewed bytes, never placeholders.

| ID / unit | Proposed exact destination / accountable owner | Closure requirement |
|---|---|---|
| HSP-BIND01 — profile and closed command/output/proof schemas | `03_machine_contracts/drafts_non_default/authorization/OFARM_AuthorizationEvidenceSourceHistoryProfile_v0_1.md` and `03_machine_contracts/drafts_non_default/schemas/authorization/OFARM_AuthorizationEvidenceSourceHistory_schema_v0_1_draft.json`; #32 evidence-profile owner | Materialize sections 4–9, exact package/rule/proof dependencies and conditional shapes; no standalone authoritative status record |
| HSP-BIND02 — historical source inventory/admission verifier | `03_machine_contracts/drafts_non_default/authorization/OFARM_AuthorizationEvidenceHistorySourceBinding_v0_1.json`; #32 source-binding owner with #33 acceptance/bindings | Real immutable root/qualifier/basis/authority schemas, original package selection/admission proof and full historical universe mapping; QG-BIND02–05 as applicable to verification; no automatic need to enable new authoring |
| HSP-BIND03 — authoritative observation and reply binding | `03_machine_contracts/drafts_non_default/authorization/OFARM_AuthorizationEvidenceHistoryObservationBinding_v0_1.json`; #32 proof consumer with actual source/governed-read/transaction owners | Actual source locations, candidate predicate, provider identity, consistent snapshot/exhaustion evidence, access coverage and owner release validity. Existing writer guards are not a binding. New owner guarantees require separate scoped work |
| HSP-BIND04 — trusted producer and public consumer | Exact producer/observation-verifier role mapping in the selected runtime bundle; exact CP2 public profile and applicable operation/adapter binding; runtime integration and PR #31 owners | Real executable/profile selection, protected invocation, same root/cut/proof and current disclosure, no remote-signing assumption. Separate owner PRs if semantics or authority must change |
| HSP-CONF05 — producer/source fixtures | `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/drafts_non_default/authorization_evidence_source_history_v0_1/positive/` and `negative/`; #32 conformance owner | Named HSP-Cnn variants with real dependency bytes/digests and explicit shape/semantic expected predicates; consumer fixtures bind the same sources |
| HSP-CONF06 — manifest and checker | `04_implementation_and_conformance/conformance_runners/authorization_evidence_source_history_v0_1/OFARM_AuthorizationEvidenceHistory_Conformance_Matrix_v0_1.json` and `validate_authorization_evidence_history_contracts_v0_1.py`; #32 conformance owner | Check exact schemas/bindings, graph/fold invariance and cross-consumer cases; record execution level honestly, not runtime success from static examples |
| HSP-RUN07 — executable evidence | Separately planned OFARM2 producer/observer/adapter work and its governed test evidence; no runtime files selected by this candidate | Actual authoritative positive observations, hostile source access, concurrency/replay, same-snapshot release and paired C38 tests through production paths; one trust boundary per PR |

The observation mapping is decisive. A reference that says complete, a fake provider, synthetic source list or self-signed proof cannot close HSP-BIND03. Real execution must demonstrate the provider's coverage of every eligible admission path and the reader's exhaustive view at its cut. A missing exact mapping is not proof that a new transaction is required; a demonstrated missing owner guarantee must be split before implementation.

QG-DEP01 remains the separate action/rule/target/admission owner for new qualifying writes. Source profile/verification dependencies may still need acceptance and binding for historical reads without executing that writer. Record their exact selected-closure disposition rather than blanket-deferring everything with the action. QG-DOWN06 and CP2A-DEP01 remain open until their actual governed owner/consumer bindings satisfy the required stage; no decision here closes the wider #21 or OFARM2 G2/G3/G4 gates.

### 12.1 Existing ordered stages

Preserve all eleven stages in PR #11 section 24 and [issue #21](https://github.com/samovers/OFARM/issues/21): Phase A candidate; exact semantic-profile/release-scope approval; adjacent contract prerequisites; separately authorized non-default policy-bundle draft; source-bundle draft; decision-evidence drafts; exact binding review and scoped accepted law; hostile conformance; explicit scoped promotion; byte-identical OFARM2 extraction; separately authorized runtime work. Apply every stage to the complete selected closure and record truly deferred obligations without passing them.

This document belongs only to the Phase A prerequisite design. Its own exact-head approval must precede its later materialization. Before complete owner/consumer binding can be claimed, supply the actual HSP-BIND01–04 dependencies and their reviewed/admitted state, including source acceptance appropriate to historical verification. Complete conformance and the other required governance stages before claiming promotion or runtime readiness. A design approval, schema pass or synthetic positive fixture cannot close CP2A-DEP01.

Scope remains the approved complete claim/read package unless separately amended. Do not let family-level promotion select omitted actions or unbound profiles. The implementation destination remains OFARM2 [#353 / PR #359](https://github.com/samovers/OFARM2/pull/359), then [#178](https://github.com/samovers/OFARM2/issues/178), then the bounded [#176](https://github.com/samovers/OFARM2/issues/176) child. This candidate does not resume or change those runtime designs.

## 13. Review card, validation and handoff

Decision ID: `OFARM-ISSUE32-AUTHORIZATION-EVIDENCE-SOURCE-HISTORY-QUALIFICATION-001`.

Decision version: `1`. Status: proposed, not approved. The decision identifier is not a live approval record. Review and any later semantic approval must bind the exact candidate head; no merge authority follows from either.

Review the source universe and complete-observation contract first. Then test the graph fold, especially upheld record objections, root versus qualifier basis, correction-line replacement versus root replacement, competing/merged tips and annotations on resolved/replaced records. Finally verify trusted provenance, the fresh-cut/reply race, null/withholding compatibility and missing-contract versus unavailable-observation behavior. If a real owner guarantee is missing, report it precisely rather than endorsing a nominal proof wrapper.

Phase A checks cover exact source pins/approval links, all ten issue criteria, invariant/case traceability, table/Markdown structure, whitespace and the one-file boundary. Run existing cheap hygiene, generated-currentness, cross-reference and steward-guardrail checks. Several exclude historical phase reports; a pass is package hygiene, not semantic approval, executed graph proof, authoritative enumeration or privacy/concurrency conformance.

Scope stayed inside authorization-evidence history classification and trusted producer determinations. No other candidate, active source/schema/index, authoring/read grant, transaction, custody/public rule, runtime, approval, merge, promotion, extraction or deployment is changed. No existing writer is activated and no first-release history-closure claim is made.

What is next: exact-head review of this one-file Phase A candidate, then explicit semantic direction for decision version 1. Keep CP2A-DEP01 and source/observation/consumer bindings open; do not start materialization or implementation from this draft alone.
