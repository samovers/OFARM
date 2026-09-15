# OFARM Governed-Read Transaction, Coverage and Disclosure Protocol v0.1

Date: 2026-09-14. Amended: 2026-09-15, Scope A and Scope B version 1 alignment drafts.

Status: non-authoritative Phase A amendment draft to decision version 2; both drafting scopes authorized, revised wording pending exact-text review and renewed semantic approval. No implementation or merge authorization.

Approval history: [version 2 approval](https://github.com/samovers/OFARM/pull/37#issuecomment-5662707529) applies only to predecessor head `41cd45b90fb8e133f6377d8f389858b89c3dd7ae`. The task user's subsequent “approve both” authorizes Scope A version 1 (read-evidence settlement) and Scope B version 1 (the explicit deadline-based privacy downgrade) for drafting. It does not approve these eventual words. Section 15.2 separates their owner-derived clauses; prior approval does not transfer to amended bytes.

Issue: [samovers/OFARM#36](https://github.com/samovers/OFARM/issues/36). Parent: [#10](https://github.com/samovers/OFARM/issues/10). Required by [#21](https://github.com/samovers/OFARM/issues/21), predecessor 5, and [#32 / PR #35](https://github.com/samovers/OFARM/pull/35), HSP-BIND03. Implementation destination: [OFARM2 #353 / PR #359](https://github.com/samovers/OFARM2/pull/359), then #178, then the bounded #176 child.

Canonical base: `71ca724a8b6ec23f1655b086a6f549496d10a47f`.

## 1. Decision requested

Approve or amend this read-owner protocol, not its implementation:

1. One trusted read attempt owns one governed observation, current authorization, real pre-evaluation qualification evidence, complete result coverage, exact buffered bytes and one possible disclosure attempt.
2. Every returned item is covered by the one independently sufficient selected access path. An artifact-scoped SharingGrant can cover the governed contents of that exact artifact; it does not grant independent access to every underlying record. Section 7 makes that distinction testable.
3. Complete decision, consumption, receipt, coverage and payload evidence commits atomically before disclosure. The evidence commit is not the disclosure point and does not prove delivery.
4. The original live attempt alone may make one guarded handoff of the complete immutable buffer. Currentness protection and exclusive time bounds continue through that handoff; a committed receipt cannot recreate permission after a crash.
5. Read receipts have separately tagged preparation and observed-outcome records in the proposed finalization-evidence package. Preparation proves only completed preparation. An outcome records only an observed stop or disclosure attempt; missing outcome evidence means uncertainty, not success or non-disclosure.
6. Repeated requests under the same logical read identity never replay protected bytes. Reconciliation can establish evidence commitment, but cannot revive the spent decision or the lost live attempt. A separately requested new read needs a new identity and all current checks.
7. Historical refusal reads consume PR #35's complete observation and original-admission verification in the same read context. Preserve its known-candidate refresh rule. For a policy-permitted limited reply with history WITHHELD, require the explicit source-backed sealing guarantee in §8.3 before final observation and preparation; a hidden-only candidate must not become a post-commit cancellation condition. Policy-selected exclusion remains uniform. These ordering and history-verification requirements remain; only Scope B's declared deadline tradeoff changes public-outcome privacy.
8. Retention, original authorization outcomes and adjacent-owner allocation remain unchanged. Scope A aligns only with PR #11's proposed read-only late settlement; Scope B aligns only with PR #31's proposed deadline-based privacy exception. These are explicit semantic changes, not an implementation of the predecessor's stronger timing/privacy guarantees. Actual source, guard, egress and package bindings remain open; a static worked path is not runtime evidence.

These are proposed semantics for exact-text review. The [issue re-review](https://github.com/samovers/OFARM/issues/36#issuecomment-5659896617) cleared the amended issue framing, not this protocol. The user's subsequent “no blockers, go” authorized the original draft, not its semantic acceptance or later stages. [Protocol review 5194803845](https://github.com/samovers/OFARM/pull/37#pullrequestreview-5194803845) then identified B1 at `c2c52fa27bec24e72285564057cab198e4654e36`: sealed-reply suppression could reveal hidden history. Version 2's explicit-guarantee design was subsequently reviewed and approved at the predecessor head above, without proving the actual provider binding. These new owner amendments leave OFARM2 #392's feasibility/progress blocker open; they are not a new mechanism or a claim that B1 is solved.

## 2. Primary trust boundary and PR limit

Primary trust boundary: **governed-read transaction integrity and protected disclosure**.

The entire canonical PR adds this one historical Phase A document. This worktree changes only that document. The separately authorized Scope A and B drafts belong to PR #11 and PR #31 respectively; this PR only aligns read ordering/evidence with those stated owner proposals and invents no independent authorization or privacy exception. No active law, schema, currentness pointer, database object, runtime code or OFARM2 asset changes.

| Adjacent owner | What this candidate does not change |
|---|---|
| PR #11 and identity/source owners | Principal resolution, representation, grant powers, selected-path ordering, evidence eligibility, authorization outcomes or exact per-action consent comparison; only the separately drafted Scope A timing rule is aligned here |
| PR #20 / PR #26 | Human-finalization and state-affecting NOT_REQUIRED transaction semantics, retry rights or effect receipts |
| PR #34 / PR #35 | Qualifier authorship/admission/lifecycle, history classification, historical source universe or permission to inspect it |
| PR #31 | Public fields, reason codes, safe sentences, withholding-policy selection or endpoint activation; only its separately drafted Scope B availability exception is aligned here |
| PR #29 and custody owners | Retention duration, encryption, deletion, plaintext access, key custody or independent delivery attestation |
| Storage and runtime owners | Database isolation/locks/roles/migrations, new reader privileges, credential/session policy, trusted selection or a new audit service |
| Governance owners | Accepted law, materialization, promotion, extraction, merge or deployment |

This owner may define read ordering and its evidence truth claims. If satisfying them requires a new permission rule, cross-source access, storage guarantee or custody authority, stop before editing that boundary and name the exact prerequisite or stacked change. Missing future schema bytes alone do not justify another architecture issue.

## 3. Sources and compatibility

The active baseline outranks accepted RFCs, companions and machine contracts. Historical candidates and reader/currentness views do not override it. CP11–CP15 draft contracts remain non-default.

The seven owner heads below were rechecked on 2026-09-14: all open, draft and unmerged. The three affected PRs #11, #31 and #37 were rechecked unchanged before drafting on 2026-09-15. Their recorded Phase A approvals are design inputs, not accepted law or executable package admission. Each candidate file is under `package_meta/history/clean_baseline_migration/phase_reports/` at its named head. The PR #11/#31 pins below identify approved predecessors, not the subsequently published, unapproved Scope A/B amendments. Section 15.2 pins those amendment inputs separately, with exact remote-text readback on publication. Their revised semantics still require review and approval before acceptance; recording these review-input pins transfers no approval or machine binding.

| Owner | Exact head | Candidate filename and clauses used |
|---|---|---|
| [PR #11](https://github.com/samovers/OFARM/pull/11) | `4494924998183fe3fa7bc1b63b76a85893335044` | `authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md`; §§7.2.1, 7.4–7.8, 12–13, 17.2, 18.1–18.2, 18.5, 18.7–18.8, 20, 24–24.1 |
| [PR #20](https://github.com/samovers/OFARM/pull/20) | `98f8c4fafbae42c8f7fd931f43f53adcb4733713` | `governed_human_approval_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`; §§5–6, 10, 12–13, 17, 20 |
| [PR #26](https://github.com/samovers/OFARM/pull/26) | `e042efa2911b2ef0a61603b8e0adaa6911c03ac0` | `not_required_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`; §§4–8, 10; explicit read exclusion in §7.1 |
| [PR #29](https://github.com/samovers/OFARM/pull/29) | `8e0994cae5610ac9c0d2652e02c8a8a2dd7b45c5` | `authorization_evidence_retention_and_proof_strength_rfc_candidate_v0_1.md`; §§5–6, 8–10 |
| [PR #31](https://github.com/samovers/OFARM/pull/31) | `092be94f3a67497ba619295932cd0b2b1e9443f3` | `cp2_authorization_result_surface_and_public_reason_codes_rfc_candidate_v0_1.md`; §§5–6, 9, 11; C31–C39, especially C38 |
| [PR #34](https://github.com/samovers/OFARM/pull/34) | `c59fdbc75f26ee4694355adedd4df021f64b5131` | `authorization_evidence_qualifying_record_governance_rfc_candidate_v0_1.md`; §§4, 6–9, 11, 13 |
| [PR #35](https://github.com/samovers/OFARM/pull/35) | `b9ccdc96c5b3961eb672290cd32019364b56f8e6` | `authorization_evidence_source_history_qualification_rfc_candidate_v0_1.md`; §§4–6, 8–9, 12 |

### 3.1 Governing compiled-output and disclosure sources

At the canonical base:

- [Constitution RC2.1](https://github.com/samovers/OFARM/blob/71ca724a8b6ec23f1655b086a6f549496d10a47f/00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md), §§7.8–7.17, distinguishes scoped authority, explicit delegation and the right to see/retrieve/receive specific data, views, evidence or compiled outputs. It preserves provenance and prospective revocation.
- [Platform RC2.1](https://github.com/samovers/OFARM/blob/71ca724a8b6ec23f1655b086a6f549496d10a47f/00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md), §§10.1–10.6, defines live PassportViews versus frozen/versioned DocumentAssemblies, governed assembly, derivation trace and policy-bound annexes. §§14.3–14.11 require explicit authorization, purpose/scope/delegation constraints and compiled-output sharing without implied write authority. AAI-P.6 preserves truthful qualification and protected-effect gates.
- [Authority, Delegation and Data Sovereignty Policy v0.2](https://github.com/samovers/OFARM/blob/71ca724a8b6ec23f1655b086a6f549496d10a47f/01_companion_artifacts/OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md), §§3.9, 6–8, makes receiving an identified compiled output a real access right, while retaining scope, purpose, farm boundaries and provenance.
- The [accepted CP2 qualification RFC](https://github.com/samovers/OFARM/blob/71ca724a8b6ec23f1655b086a6f549496d10a47f/02_accepted_rfcs/OFARM_AI_Facing_Result_Qualification_and_Trace_Surface_RFC_v0_1.md) governs qualification, not a new grant of read authority.

The current/default `03_machine_contracts/schemas/output_assembly/OFARM_DocumentAssemblyMetadata_schema_v0_1.json` provides frozen output, durable-artifact and derivation metadata. The current `03_machine_contracts/schemas/authority/OFARM_SharingGrant_schema_v0_1.json` confirms the family/ref/grantee distinction. Neither supplies v0.2 revision-bound permission, complete content membership, the read transaction or automatic source migration. Existing metadata is supporting evidence, never the missing proof by itself.

### 3.2 Explicit compatibility ledger

| Concept or historical reference | Disposition here |
|---|---|
| PR #20 / #26 complete guards, authoritative commitment, immutable evidence and single-use uniqueness | Compatible principles adopted for this read boundary; the actual read guarantees and evidence set are specified below |
| PR #20 / #26 protected effect linearizes at atomic commit | Not imported: read evidence commits at C, protected disclosure is later at L |
| PR #26 `EFFECT_COMMITTED`, `NO_EFFECT`, retryable no-effect attempts and replay of an original result | Not imported. A committed read evidence set can have no disclosure or uncertain disclosure. This protocol offers no protected replay under an old read identity |
| Human approval, challenge, reservation generation or direct-human final act | Absent. The read row selects NOT_REQUIRED; no synthetic human record or empty approval value |
| PR #11 §18.5 receipt and disclosure truth | Refined as preparation plus linked observed outcome (§§9–11). A preparation receipt cannot assert a future disclosure time. Later truthful owner evidence is append-only, as §17.2 already allows; it is not a second decision ledger |
| PR #29 original posture and later availability | Retained unchanged. Custody, a pre-release receipt and a candidate-byte match never prove delivery |
| PR #35 ban on classifier explanation commits | Retained. The classifier cannot repair a finalized payload or write a durable status. The read owner may record an actual stop/disclosure observation; that record cannot change the history label, original decision or old payload |
| PR #35 §6 refresh versus PR #31 §5.4/C38 privacy | Refresh retained. Scope B imports only PR #31's proposed §5.4.1 deadline exception; the actual-C post-commit positive pair and uniform exclusion remain intact. Section 8.3 retains the required sealing guarantee. Actual source/storage support remains RD-BIND03-W, a sub-obligation of open RD-BIND03 |
| PR #11 §24.1 cites PR #34 at `69682c2f918ef18756261a1186294cc3a5ebe44d` as unapproved | That is publication history, not the current source input. This draft uses approved version 2 at `c59fdbc75f26ee4694355adedd4df021f64b5131`, with [approval evidence](https://github.com/samovers/OFARM/pull/34#issuecomment-5654388700) |
| PR #11 read timing and compatibility update | Scope A originates in that owner's proposed §§18.2/18.5.1 amendment, not a local read workaround. Sharing, classifier, source-consent comparison and non-read finalization remain unchanged. Before selected-closure review, reconcile the newer source input and reviewed receipt/guard refinement with exact revised owner bytes; this draft does not close that binding |

PR #34 approval does not close QG-DEP01 or QG-BIND02–05. PR #35 approval does not close HSP-BIND01–04 or CP2A-DEP01. Neither today's excluded writer nor today's policy digest settles original admission or history completeness.

## 4. Exact admitted read shape

The initial release remains exactly `ASSERT_OPERATION_CLAIM` and `RECEIVE_READ_DATA`, with complete action coverage and transitive dependencies. Only the explicit Scope A read-timing amendment changes the selected authorization semantics; target/path coverage and exact-digest consent checks are not weakened. This document covers the latter action's full selected scope, not only reads of operation claims. It adds no third action or new read target.

The selected read row retains `TRANSACTION_BOUND_V0_2`, `CURRENT_ONLY`, `SINGLE_USE`, `NO_EXTERNAL_DISPATCH`, `EP_CP2_READ_QUALIFICATION_V0_2`, `NOT_REQUIRED` and `NO_SEPARATE_APPROVAL_POLICY`. Actual software-agent reads require `AGENT_ALLOWED_WITH_POLICY_CHECK`; preflight is not disclosure permission.

`RP_READ_TARGET_ONE` has exactly one `READ_TARGET` authority target:

- One of the ten closed scope kinds: FARM, SITE, FIELD, ZONE, CROP_CYCLE, LOT, FACILITY, OPERATION, DEPLOYMENT, TENANT; or
- One of the twenty record/artifact kinds: OBSERVATION, EVIDENCE_RECORD, STRUCTURE_ASSERTION, OPERATION_ASSERTION, COMPLIANCE_ASSERTION, INTERVENTION_PLAN, EXECUTION_REPORT, REVIEW_REQUEST, REVIEW_DECISION, PACK_INSTALLATION, PACK_ACTIVATION_SET, DOCUMENT_ASSEMBLY, DOSSIER_ASSEMBLY, SUBMISSION_ASSEMBLY, EVIDENCE_BUNDLE, CURRENT_STATE_MATERIALIZATION, SHARING_GRANT, REVOCATION_DECISION, PASSPORT_VIEW, AUTHORIZATION_TRACE.

| Read form | Required binding |
|---|---|
| Direct | Exact target kind/ref/revision and governing content/projection; neither QUERY_SPECIFICATION nor QUERY_PLAN is required or invented |
| Query | Same one target, plus exactly one QUERY_SPECIFICATION and one QUERY_PLAN as INTEGRITY_INPUTs. Bind immutable revisions, executable plan, parameters and all applicable context/qualification policies |

An assembly's historical derivation query references do not turn a direct read into query form. Query inputs, constituent origins and coverage proof do not become additional authority targets. Nor does an origin reference create permission to disclose it.

The rule-selected EI_DATA_READ intent binds the exact requested target/form, purpose, projection, redaction, buffered execution, snapshot policy and requested metadata/lineage. Ingress follows PR #11 §18.1, including duplicate-member rejection, exact admitted-package/rule verification and declarative extraction. There are no caller-authoritative mirrors of extracted facts or trusted frame fields. Protected streaming fails the selected intent schema. Non-protected preflight planning/qualification remains permitted.

Every selected kind and permitted direct/role/delegated/sharing path needs its appropriate production-reachable conformance coverage later. Sharing is applicable only to the artifact families permitted by its source contract, not all thirty read kinds. Lack of a future kind-specific proof binding is a closure gap, not permission to silently drop that kind from the selected rule.

## 5. Attempt ownership and trusted inputs

### 5.1 One request identity, one live attempt

Use the existing valid request identifier, not a newly required caller idempotency field. The logical read lookup tuple is:

```text
(operationBoundaryKind, operationBoundaryRef,
 authenticatedRequestingPrincipalRef, representedPartyRef-or-null,
 RECEIVE_READ_DATA, requestIdentifier)
```

For the first OFARM2 binding the operation boundary is the trusted tenant. A deployment-scoped target still needs an explicit permitted boundary/tenant mapping; caller target text cannot select a broader lookup or observation domain. Typed identities and request identifiers use their owning contract's exact equality, never aliases, normalization or display names. The future profile must bind that encoding, including exact null representation. Profile version, session, selected policy, handler and outcome are not lookup dimensions that could hide an older attempt.

After valid ingress and trusted identity/representation resolution, the read owner atomically claims the tuple and records an immutable attempt-admission record A. It binds the canonical caller submission, its digest, selected contract, independently resolved tenant/principal/session, intent/derived-view digests and a newly assigned trusted attempt and read-transaction identity. The comparison projection contains all caller request facts; only byte formatting eliminated by the bound canonical JSON encoding is ignored. It omits no AI-assistance or intent field. A changed submission under an existing tuple is a conflict, not a new attempt.

A claims only admission and single ownership, not authorization, successful qualification, consumption or disclosure. It is a limited read-attempt profile in the existing finalization-evidence package, not an approval reservation, domain write or new top-level ledger. Before capturing A, independently resolve and bind a compatible retention policy for its actual admission evidence, including the caller-submission and identity material retained. The later read snapshot still resolves the applicable payload and complete decision-evidence postures; admission cannot override those checks. If admission evidence itself cannot be lawfully retained, do not create A. Any derived coordination row must reconcile to the immutable admission and later evidence. Admission persistence failure or uncertain admission acknowledgement permits no evaluation-to-disclosure continuation.

Exactly one live owner can advance A. Its invocation capability is non-caller-constructible, bound to the admitted session, attempt and read-transaction identity, and invalid after owner loss. Duplicate handlers can observe permitted status but cannot take over, resume or reconstruct the capability. A crash ends this attempt's eligibility even when all durable inputs remain available. Do not create a new request identifier automatically to disguise transport retry as a fresh read.

### 5.2 Independently established context

Before evaluation, the trusted runtime supplies and verifies:

- tenant/boundary, authenticated principal, immutable resolution and representation basis, session validity, and CP3 actorship/qualification evidence where applicable;
- the exact independently selected policy package, admitted-action manifest, rule, intent schema/extractor, read protocol and producer/verifier implementations;
- trusted read-transaction identity, start time and fixed deadline, source snapshot identity and cut, and the exact provider/guard interfaces;
- all authority, purpose, evidence, redaction, serialization, retention and public-projection policy bindings; and
- the non-transferable association of those facts with A and this invocation.

A returned frame containing matching strings, a digest or `trusted = true` is not provenance. The consuming evaluator/receipt/egress path checks the protected invocation and independently selected contract, not values supplied by a request or substituted producer. No new identity, secret, signing service or runtime selector is created here. Missing actual selection/provenance bindings are RD-BIND02, not a fallback to caller claims.

`authorizationEvaluatedAt` comes from trusted evaluation, not request time. **D is `decisionValidUntil`**, PR #11 §18.2's full effective minimum of the original fixed read-transaction deadline and all applicable session, representation, authority, rule, freshness, resource, evidence and sovereignty ends. D never means only the potentially later request deadline. Ends are exclusive UTC instants. Failure to construct a required cutoff prevents a consumable decision. Under the Scope A proposal, actual finalization initiation I and disclosure L must be strictly before D; only the already-initiated evidence operation may settle later under §9.2.1. The clock is never restarted after I or C. Scope B uses the same D and does not change this timing permission.

## 6. One governed observation and real qualification

### 6.1 Snapshot and protection contract

S is one actual, consistent committed read view with a trusted cut c. A ContextSnapshot for interpretation, a transaction label or a list digest is not S. The owner must bind the source collections, membership predicates, exact revision resolution, query/plan/parameters, visibility rules, page/range exhaustion, negative/set-valued facts and authoritative commit-order evidence used by every required provider.

The same S must cover authorization, source retrieval, redaction, qualification, history observation, coverage and payload construction. Immutable external objects may participate only with an owner-supplied mapping proving the exact version and applicable membership/currentness at S. A remote “latest” fetch, sequential command snapshots or unrelated cached qualification do not join S merely by copying its ID. If all sources cannot join the view, this invocation cannot establish the protocol.

Positive membership alone is insufficient. Revocation absence, complete role/grant candidate sets, exhaustive query results and historical candidate absence each need their own complete observation. Tenant filtering cannot hide an applicable cross-source candidate and still support an all-clear claim. Conversely, this requirement grants no broader source access; unavailable lawful access is an owner binding/failure condition.

The read owner derives a complete guard set from actual dependencies, including principal/session/representation, applicable authority and revocations, target/input currentness, scope/sovereignty, rule selection, evidence freshness, relevant EnforcementChain facts, redaction/retention constraints and exact buffer identity. It must prove that relevant invalidation and L are ordered: a relevant change preceding L either is reflected in the admitted view/validation or prevents L. For the C38-limited WITHHELD path, hidden-history-only changes require the stronger §8.3 ordering: reflected before sealing or committed after L, not an optimistic conflict that cancels the public reply. A check just before an unguarded send is not either guarantee.

The guard contract must span the evidence commit C through L, including exclusive deadline validation at L. A database commit that releases all relevant protection does not satisfy that interval by itself. The eventual provider must identify the real mechanism, every participating mutation path, failure/owner-loss behavior and the order witness. RD-BIND03 remains open until that mapping is reviewed; its specific WITHHELD sealing sub-obligation RD-BIND03-W is defined in §8.3. This proposal selects no database isolation level, advisory lock, cross-service lease or privileged reader. It requires an observable ordering property, not a particular implementation. If satisfying it needs a new source/storage/authority guarantee, its owner must supply that separately before the binding can close.

Not every new committed record invalidates a read. Currentness follows the bound relevant-state policies; unrelated history advance alone is not a failure. Historical qualification is as of c with §8's known-candidate rule and conditional sealing guarantee, not a promise of latest global history throughout network delivery. Section 8.3 protects the bound root's complete candidate universe only through L or irrevocable attempt termination. It creates no lock-through-network-delivery requirement or new global history service.

### 6.2 Acyclic qualification ordering

The permitted dependency order is:

```text
admitted attempt + trusted selected rule + valid intent
  -> same-view plan/source facts and genuine required qualification inputs
  -> current authorization evaluation
  -> remaining applicable gates, final coverage/redaction and CP2 projection
  -> exact immutable buffer and complete evidence set
  -> actual I -> C -> acknowledged C -> guarded L
```

Before authorization evaluation, the policy-selected read-qualification producer obtains or verifies genuine evidence under `EP_CP2_READ_QUALIFICATION_V0_2`, using the exact intent digest, target/form and S. Internal planning and inspection occur only through already authorized provider roles; pre-authorization planning never gives the recipient protected bytes. If the provider needs a new source-access permission, stop at that owner rather than evaluating an unqualified read first.

The selected evidence policy may derive required references from `effectIntentDigest` and the trusted context, as preserved by OFARM2 PR #359 finding F4. This protocol does not require a redundant caller/frame field merely to transport those references. Whether derived or explicitly carried, each reference must resolve to real, eligible, same-context evidence with independent provenance. Ref spelling, a fabricated empty envelope and a producer's unverified pass flag are not evidence.

Pre-evaluation evidence is not the final disclosure receipt. It must not depend on this attempt's future ALLOW, committed receipt or actual delivery. Later gate/coverage results are bound into the final CP2 envelope and receipt without rewriting earlier qualification. If a selected evidence policy actually requires a future fact to authorize the same read, that circular policy needs owner correction before binding; this protocol provides no success stub or delayed check exemption.

The final envelope carries its genuine qualification outcome, stable problems, trace/lineage and prescribed next actions. Every applicable EnforcementChain gate has its actual disposition and proof; inapplicable gates are not reported as passed. ALLOW satisfies only the authority gate. A later failure does not rewrite an already issued valid authorization result.

Preserve the distinction between established authorization failures and failures of another gate. PR #11 §20 already defines `READ_RESULT_COVERAGE_NOT_PROVEN` as DENY/rank 1440 and `TRACE_DISCLOSURE_NOT_AUTHORIZED` as DENY/rank 1450, alongside its expiry, consumed-decision and authority-change reasons. Where that governing evaluator establishes such a failure, use its unchanged outcome/ranking and non-ALLOW persistence protocol. If an earlier evaluation exists, retain it and identify the later evaluation separately; do not mutate its result. The read owner supplies verified coverage/guard facts to that evaluator, not a second permission decision or local rank. Storage, serializer, retention and other non-authority gate failures must not be disguised as those authorization reasons or collapsed into a generic fabricated DENY.

## 7. Complete result coverage, including sharing

### 7.1 One selected path and a complete information inventory

PR #11 evaluates independently sufficient direct Party, role-targeted, delegated and SharingGrant paths, selects its canonical winning path and records one final policy decision/trace. This read protocol neither reranks paths nor performs a second permission decision. All disclosed content must be covered by that selected path, including its exact target, purpose, scope, tenant, sovereignty and redaction constraints. If that path cannot cover the final payload, do not silently substitute another path or combine partial paths after evaluation.

Construct an internal coverage manifest before disclosure. Its exact profile must account for every payload location and every origin revision contributing information, including:

- rows and fields, with exact source kind/ref/revision and derivation/projection mapping;
- aggregate inputs and transformations, counts, empty-result claims and inference-sensitive omissions;
- metadata, lineage, identifiers, links, CP2 fields, safe messages and response metadata that convey protected facts; and
- fixed serialization/control bytes, identified as non-protected structure under the bound serializer, not fabricated source records.

Each information-bearing location records the governing target/content binding; complete contributing origin membership or an exact independently verifiable manifest reference; selected-path coverage witness; applicable purpose/tenant/scope/sovereignty and redaction/inference rule; and a returned, redacted or withheld disposition. Redaction entries must themselves not reveal protected existence/counts in the public output. The internal manifest remains protected evidence.

The verifier independently compares manifest locations and derivation membership to the complete final buffer and underlying observation. Missing origins, unaccounted fields, unexplained counts and uncertain aggregate inference cannot pass. A count over unauthorized source rows is not harmless because those rows are absent from the visible list. Apply the bound policy's authorized redaction/recomputation or withhold; if no completely covered final payload exists, deny disclosure with the existing owner failure handling. That is not permission to invent a new authorization reason rank.

### 7.2 Artifact content is not independent source-record access

The positive sharing rule below is an interpretation of the specific-output permission in Constitution §7.15, Platform §§10 and 14.10, companion policy §6 and PR #11 §13; it is not a grant-inheritance rule:

1. Resolve an actual governed artifact revision with an exact content boundary: frozen bytes/components or a governed live-view definition plus its exact computed revision at S. Verify the artifact's own assembly/materialization/reconstruction and qualification requirements. A caller's arbitrary concatenation is not governed content.
2. Verify the independently sufficient SharingGrant for that grantee and exact artifact family/ref/revision, exact read-rule binding, delivery/use restrictions, scope, purpose, validity and revocation. All resource-control and sovereignty constraints still apply. Grantor identity alone is not proof of these facts.
3. The permission to receive that artifact covers the information actually constituting its governed, permitted content, including an aggregate embedded in it. Map each returned item to that artifact content and all contributing origins. Origin membership proves where the artifact information came from; it does not require treating each origin as a new separately requested authority target.
4. Merely referenced source material, unselected attachments, raw fields, private lineage and out-of-artifact query expansion are not made disclosable by that mapping. Returning a source identifier is also an information disclosure and needs coverage. Dereferencing an embedded link for the recipient is a separate read unless the exact referenced bytes are already part of the authorized artifact content and its verified content boundary.
5. Explicit source/sovereignty/assembly restrictions that survive into the artifact remain constraints. A label saying “shared” cannot launder forbidden cross-farm data or override an exclusion. Redaction may produce only a permitted projection under the bound artifact/read policy; it does not create a new shared revision or expand a grant.

Thus an artifact can legitimately disclose an aggregate without granting the recipient a separate read of each raw input. The opposite shortcut is also forbidden: provenance of an arbitrary value from a shared artifact is not sufficient if the value was not part of that artifact's authorized content. For a family whose governing contracts cannot determine that boundary or resolve an applicable restriction, RD-BIND04 remains open; seek the precise content/authorization owner decision, not a universal sharing refusal or invented permission.

### 7.3 Worked positive shared aggregate

This is a symbolic design case, not existing fixture bytes or deployed proof. A governed frozen DossierAssembly revision DOC1 contains one approved table and a computed total from exact origin revisions O1 and O2, within one permitted farm/tenant scope. Its verified assembly trace and immutable component membership show those table cells and the total are part of DOC1. The bound policies permit sharing those contents for purpose P; they exclude a raw personnel field and a private annex. A current SharingGrant grants party G receipt of DOC1 at that exact revision for P, satisfies its entire read rule and passes sovereignty and all other constraints. G need not possess independent receive/use authority over O1 and O2.

The direct read of DOC1 requires no query pair. The internal manifest maps each visible cell and total to DOC1's exact component locations, O1/O2 revisions, derivation and the selected SharingGrant; it proves the excluded personnel field/annex contribute no unauthorized inference to the result. Private origin identifiers are not copied into the public bytes. The final CP2 projection and serialized buffer are fully covered. With §§6 and 9–10 satisfied, C then L is a positive sharing path.

Change only the request to include the excluded annex, a live raw-source expansion or a cross-farm contribution forbidden by policy: the same grant no longer proves that payload. Authorized redaction/recomputation may produce a completely covered payload; otherwise disclosure stops. Change the target to O1 itself: DOC1's SharingGrant is not authority for that separate read. Change only origin discovery to an unexplained partial list: coverage is unproved even if the visible total happens to match.

An independently sufficient direct or delegated RECEIVE_USE path can also cover DOC1. Each is checked in full on its own; a direct path supplying action plus a SharingGrant supplying missing purpose/evidence never forms a sufficient combined path.

## 8. Historical refusal and public qualification

### 8.1 Original-result and history verification

A `RECORDED_RESULT` lookup first verifies the original complete committed v0.2 refusal bundle and current read permission. It does not re-evaluate yesterday's authority to rewrite the original outcome, treat a v0.1 trace as v0.2, or reuse the original refusal as permission to disclose it. A full internal trace requires its separate exact AUTHORIZATION_TRACE read and all these controls.

Invoke the independently selected PR #35 producer/verifier for the exact original root, tenant/scope, A and S. Its observation enumerates the entire eligible historical source universe before admission filtering, including qualifications of qualifiers, former packages and applicable imports/migrations. It establishes each act's original admission or proved invalidity; unresolved original authority, membership or identity is not absence. Use its independently verified exhaustion/source/order evidence, not today's admitted writer list, an index watermark or a receipt saying only that the original refusal committed.

Current writer exclusion is compatible in principle with verifying an older valid qualifier. It proves neither that the historical universe is empty nor that authoring can be deferred for this release. HSP-BIND02/03 and the applicable QG bindings still owe that actual proof.

### 8.2 Preserve refresh without a hidden-history cancellation channel

The producer's verified cut and transcript belong to the same read as every returned original-result byte. PR #35's rule is unchanged: before reply finalization at L, learning of a potentially material committed candidate after c requires a new complete observation/revalidated reply or its permitted limited/failure handling, even if original admission or the eventual label is unresolved. Do not ignore the candidate, splice a new cut into old bytes or invent a completed classification.

First select the reader/scope/record-class disclosure policy independently of hidden history, including its choice between a permitted limited reply and exclusion. That selection is a binding in the read evidence, not a policy branch chosen after a candidate appears. The affected paths are:

| Independently selected path | Required handling |
|---|---|
| History status/time may be disclosed | Retain the whole-read refresh and post-seal suppression rules below. Missing classification is handled under PR #31's permitted UNAVAILABLE rules; it is not relabelled WITHHELD to avoid refresh |
| History status/time may not be disclosed, and limited RECORDED_RESULT is permitted | WITHHELD/null/null remains fixed regardless of history. Before final S and sealing, require §8.3's actual source-backed ordering guarantee; no normal hidden-history-dependent post-C suppression path exists |
| Historical lookup is excluded by that policy | Prepare no historical-result payload and no successful read C/L for that excluded result. Use the same owner-permitted qualified failure whether hidden history is absent, present, newly learned or unresolved. Internal history work cannot change this choice, failure category or omission pattern |

For a history-dependent reply that can be refreshed, or for a candidate learned before the protected final observation of a WITHHELD reply, the owner may:

- Before final payload/evidence sealing, discard all dependent preparation and obtain a new complete S, rebuild/revalidate the whole read and use a fresh authorization evaluation within the original fixed deadline. The original caller intent, requested target revision, logical identity and live owner cannot change; if that unchanged request is no longer eligible, stop rather than silently retarget it. No old decision or observation is spliced into the replacement; no earlier evaluation is consumed or misreported as the final decision.
- Use PR #31's independently permitted UNAVAILABLE/WITHHELD limited reply, rebuilding and re-covering that entire payload before sealing. WITHHELD is available only under the independently selected non-disclosure policy and §8.3, not as a new branch chosen because a candidate appeared. A failed authorization/currentness guard cannot be rescued merely by changing the history field.
- If payload or evidence is already sealed and history status/time is disclosable, suppress this attempt. Do not edit the buffer, receipt, decision or history label, and do not let the classifier append an “explanation” commit. A new protected reply requires a separately requested new read with new identity and full checks. This is not an alternative to the required WITHHELD guarantee: §8.3 must prevent that hidden-only interleaving before claiming this path is supported.

These rules do not let the classifier rerun a command or write qualification history. For a disclosable history observation, genuinely unlearned post-cut events remain outside that as-of claim; the public time is c, never a claim of later completeness. The WITHHELD path has the additional ordering requirement below. A source that cannot support the required complete cut or sealing guarantee cannot claim readiness by returning UNAVAILABLE forever.

### 8.3 Required WITHHELD history-sealing guarantee

**RD-BIND03-W is required for every policy-permitted WITHHELD limited historical reply**, not only when a query finds a qualifier. It is part of the read transaction's existing RD-BIND03 binding, not a new policy, history writer, record family or implemented locking mechanism. Its absence leaves that path unbound for the whole applicable reader/scope/record-class policy, including empty-history requests. This does not narrow the selected rule or certify blanket refusal as completed positive coverage.

The admitted provider/transaction contract must supply all of the following. Acquire and verify its actual protection before final S/sealing/C; verify continuing protection again at L. Stating these obligations alone is not provider admission:

1. **Complete scope and participation.** Bind the exact original root, full candidate universe from PR #35, authoritative locations, membership predicates and every admission/import/migration/commit path that can introduce a potentially relevant committed candidate. Include qualifications of qualifiers and unresolved or malformed-root candidates through the required enclosing partition. Do not filter protection by successful admission, valid form, today's executable writer, currently known IDs or a predicted public label.
2. **Protected final observation.** Establish protection before acquiring the final S/c used for authorization, retrieval, history, qualification, coverage and the buffer. Reconcile previously committed candidates and pending source notifications against that complete view. A candidate committed before this protection cannot be omitted because a replica or notification has not exposed it yet. Earlier unsealed preparation may be discarded and rebuilt in full within the fixed attempt/deadline; it cannot be spliced into S.
3. **Commit ordering through L.** After that final c, no additional candidate in the protected universe may commit until L or irrevocable termination of the attempt. The provider must order a competing commit before the protected final c, where it is included, or after L/termination. Protection survives C and cannot be released merely because the evidence transaction committed. This is exclusion of the conflicting interleaving, not detection followed by read cancellation.
4. **No concealed knowledge.** The owner still processes material knowledge and rejects inconsistent observation proof. It cannot defer delivery of a notification about an already committed candidate, blind the observer, suspend required verification or call a known event “unlearned” to satisfy item 3. A delayed notification for an already included candidate is reconciled by exact membership/commit identity; it is not new post-cut membership. A genuine newly discovered pre-cut omission disproves the observation guarantee.
5. **Policy-independent control, with Scope B's explicit deadline exception.** Whether protection is required, its scope, its policy and processing rules must not depend on hidden candidate presence, value, validity, count or classification. Protect the same candidate universe for equivalent requests. Only §8.3.1's import of PR #31 §5.4.1 permits a covered causal storage wait through D to change success into deadline failure. Optimistic conflict aborts, arbitrary early timeouts, hidden-selected exclusion/readiness changes and unlisted processing failures remain outside that exception. A permitted timeout is an amended-privacy outcome, not a C38 pass under the stronger predecessor. Actual-C post-commit obligations remain intact.
6. **Independently verified evidence.** Bind the provider/implementation identity, protected invocation, source-inventory digest, actual protection/acquisition witness, protected cut, membership/exhaustion proof, participating commit paths and exact continuity contract to A/S and the preparation receipt. The receipt binds only evidence already established before C. The actual continuous-through-L/time witness is verified by the live owner at L and, if recorded, linked afterward in its truthful outcome evidence; no future observation is asserted at C. A claimed seal flag, lock name, lease time or snapshot ID is insufficient. Actual closure requires source/transaction-owner review and paired race evidence under RD-C20/RD-C21, not merely a new field or this prose.

The seal proves membership/order, not a history label. It may contain candidates whose original admission cannot yet be established; PR #35 must still return its truthful determination or permitted UNAVAILABLE, and PR #31 still projects WITHHELD regardless of that status. No required authorization, eligibility, CP2 evidence, original-result verification, retention or other guard is waived. If a bound rule requires additional evidence, it must be supplied normally.

For the paired executions after **actual C, not its acknowledgement**, with the seal intact the unchanged limited reply reaches its one L in both executions, provided the same independent authority/session/retention, fault and other conditions permitting L hold. In the execution with a newly offered competing qualifier, the provider orders that candidate's authoritative commit after L. It must not let that writer delay C's acknowledgement past D and then claim the deadline exception. This holds even if the candidate's later admission/classification is unresolved. The read neither cancels because of hidden history nor ignores a known intervening commit; the latter cannot occur under the required guarantee. Rejecting or dropping the writer is not proof of the required later actual commit. Genuine independent acknowledgement loss still suppresses L; the positive pair does not override that rule.

If a candidate really commits or a previously omitted candidate first becomes known in the protected interval, that disproves the provider's claimed guarantee. Keep the read fail-closed, spent consumption and immutable evidence intact, with truthful uncertainty and the existing incident path. **That failure is not claimed to satisfy C38 or to resolve B1 by changing its name.** A provider permitting this execution fails RD-C20/RD-C21 and cannot be admitted as this path's implementation. Missing or false protection cannot be detected by per-request hidden-history probing and then presented as a privacy-safe fallback. Independent faults still stop disclosure under §§10–11; the paired tests must vary only hidden history while holding those faults fixed.

Protection ends at L or irrevocable attempt termination, not recipient acknowledgement or full network delivery. Expiry, connection loss or a missing heartbeat alone is not the provider's proof that protection may safely be released; the binding must establish that no L can still occur. It does not roll back spent consumption, revive an attempt, permit same-identity replay or authorize a new writer. The actual mechanism is deliberately not selected here. If existing source/transaction guarantees cannot supply the retained property, RD-BIND03-W remains open under the existing OFARM2 #392 work; no new mechanism or prerequisite is invented here. Any further owner semantic change beyond the two authorized drafting scopes needs separate owner review.

### 8.3.1 Scope B alignment — closed progress exception, not a seal waiver

PR #31's proposed §5.4.1 owns the sole exception. At the unchanged full D, a policy-permitted WITHHELD limited historical read may expire without L because required protection/preparation or authoritative C acknowledgement is still waiting on one of that owner's enumerated dependencies: an already-running relevant source transaction's finalization/visibility/protection release, direct storage persistence/acknowledgement needed to establish the read's protection, or the single C operation's actual atomic/durable completion and acknowledgement. The binding must identify the exact covered storage operation and causal wait through D. This paragraph imports that closed list; it does not add another storage-progress category.

The corresponding no-hidden-writer execution may succeed. This is an explicit success-versus-deadline-failure privacy downgrade, potentially revealing hidden activity or contention; repeated reads may strengthen inference and no leakage bound is established. Do not describe it as an independent fault, history-independent availability or conformance to version 2's stronger guarantee.

History discovery/classification difficulty, incomplete source coverage, missing retention capability, arbitrary pool exhaustion and unrelated processing failures do not qualify. Nor do immediate hidden-writer refusal, shorter internal timeouts, hidden-dependent budgets/queue priorities, artificial delays, readiness changes or policy-exclusion/fallback switches. Reaching D cannot convert an unrelated failure into a covered wait. Covered public deadline failures use PR #31 §5.4.1's proposed uniform HISTORICAL_READ_EXPIRED projection, not a choice between RESULT_UNAVAILABLE and COMMIT_UNCONFIRMED. That owner defines all fields, labels, non-reporting warnings and withholding; this protocol supplies truthful cutoff/wait and commitment facts without turning the public omission into a claim of owner uncertainty. Apart from the authorized success-versus-deadline-failure difference, hidden history cannot select extra content, diagnostics, hints, references, failure categories or omissions. Other failure surfaces and their confirmation rules remain unchanged.

Scope B grants no late I/C permission, rollback fiction or cancellation/retry authority. Scope A separately permits only eligible I's late settlement. A candidate or C that actually committed stays committed. Required full observation, source participation and non-temporal guard proof remain intact; no incomplete preparation can enter I and no missing/unknown C can enter L. Policy-excluded history remains uniformly excluded, and disclosable history keeps its refresh/suppression rule.

RD-C20 remains positive from actual C. A newly offered candidate that delays acknowledgement past D or otherwise defeats L solely through hidden history violates that retained guarantee, even though the owner has not yet learned C's outcome. Fail closed and report provider failure, not an allowed timeout. Independent acknowledgement loss still stops disclosure. Scope B therefore leaves a real post-C progress obligation and the B1 feasibility question open; it does not select or admit a PostgreSQL provider.

### 8.4 Public content and unchanged command-reply boundary

PR #31's history object remains exactly availability, asOf and disputeStatus. AVAILABLE requires the verified six-label determination and actual observation time. UNAVAILABLE and WITHHELD have both other fields null; WITHHELD takes precedence whenever status or time is not disclosable. Use the approved safe sentences, original outcome/time, recorded-not-current labeling and trace posture unchanged. Internal counts, source IDs, diagnostics and admission failures do not become public fields.

A missing/unadmitted producer or broken binding is a readiness/interface failure, distinct from a valid bound producer's temporary inability. An independently permitted limited response may handle either safely but does not certify the missing producer. If the original result itself cannot be verified or read, no history fallback creates existence disclosure.

For C38 pairs with equivalent readable originals and differing only in hidden history, choose limited reply versus exclusion from the same independently selected reader/scope/record-class policy. Except for §8.3.1's expressly permitted success-versus-deadline-failure difference, hidden label, candidate count or observation success cannot change response category, text, diagnostics, references, hints, omission pattern or fallback choice. This includes history learning around sealing, actual C and its acknowledgement, and L, not just fields in a delivered response. Sections 8.2–8.3.1 and RD-C20/RD-C21 supply the combined handling; the same coverage/egress guard applies to safe projections, headers, denial paths and caches.

Fresh-refusal command replies remain with their command transaction owners plus PR #35/#31. This historical-read protocol does not close that separate HSP-BIND03 path.

## 9. Evidence ownership and truthful receipts

### 9.1 Proposed package placement

Use PR #11 §17.2's existing four package families. The names in this table are proposed tagged profiles, not materialized schema IDs or runtime bindings. Read evidence entering authority remains append-only `EvidenceEvent` / `evidence record`, never domain current state, a qualifier act or filing-delivery truth. The classifier creates no durable status record.

| Evidence element | Semantic owner / proposed package | Truth claim and membership | Failure rule |
|---|---|---|---|
| Attempt admission A | This protocol / AuthorizationFinalizationEvidence v0.2 read-attempt profile | One logical request and live attempt admitted; separately durable before preparation, not part of C's success claim | No authoritative acknowledgement, no continuing attempt |
| Request/result/full trace | PR #11 / AuthorizationDecisionEvidence v0.2 | Exact original evaluation and selected path; complete bundle is in C | Apply applicable decision-bundle persistence failure; never fabricate DENY or success |
| Pre-evaluation qualification and final gate/CP2 proof | Evidence/Platform owners; references in decision/read evidence | Genuine inputs with their original times, plus later actual gate results; required immutable bindings are in C | Missing required proof blocks preparation/commit; no invented envelope |
| Single-use consumption | PR #11 semantics, this read ordering / AuthorizationFinalizationEvidence v0.2 | One exact read transaction, intent and prepared payload; in C. Scope A's late complete C proves permanent non-reusability, not timely authority use | Uniqueness and complete atomic membership required; no second consumption or late L |
| Governed-read preparation receipt | This protocol / AuthorizationFinalizationEvidence v0.2 | Preparation completed and exact buffer/evidence frozen before I; complete membership at C, not a claim of current disclosure eligibility. Binds the independent disclosure branch and, for limited WITHHELD history, §8.3 seal contract/acquisition/cut proof; no future C time, L or delivery asserted; in C | Incomplete or uncertain set, or missing required seal binding, permits no L; this cannot certify a hidden-history-dependent fallback |
| Coverage manifest | This protocol with source/authority/redaction owner witnesses / referenced read-evidence profile in AuthorizationFinalizationEvidence v0.2 | Every final item/location and origin accounted for under the selected path and S; in C | Incomplete coverage prevents disclosure; digest alone cannot prove it |
| Payload digest, serializer/media/policy bindings | This protocol / preparation receipt | Exact immutable buffered application bytes intended for the one handoff; in C | Any post-hash change invalidates the attempt |
| Retained payload ref/bytes and custody/schedule bindings, when required | PR #29 / referenced by preparation receipt | Exact bytes already verifiably retained under the promised policy; required membership/reference activation in C | Future upload, missing bytes or incompatible policy prevents C/L |
| Read outcome observation | This protocol / AuthorizationFinalizationEvidence v0.2 linked read-outcome profile | A stop before L or an actually observed handoff/completion/failure, with precise time/proof limits; after the event, not in C | Missing record leaves outcome unknown; never fill it from intention or receipt presence |
| Source-history transcript | PR #35 / its derived internal decision-evidence profile | Complete verified as-of determination and invocation-bound proof, or valid inability; relevant retained evidence bindings in C | No separate history receipt/writer; incomplete required proof cannot become NONE |

### 9.2 Exact preparation set

After successful authorization and all applicable gates, freeze the final CP2 projection and exact serialized payload. Bind the preparation receipt to A, tenant/principal/session, selected read transaction and S/c, target and every contributing origin revision, conditional query/plan/parameters, intent/derived view, selected path, policy/rule/manifest, all guards and deadlines, qualification/gate/coverage proofs, serializer/media/serialization policy and payload digest, retention policy/posture/schedule and exact retained ref when applicable. For a limited WITHHELD historical reply, the independently selected policy branch and already established RD-BIND03-W acquisition/scope/observation proof are required before sealing; they are not retrofitted after a hidden candidate arrives. Actual L continuity remains a later live-owner check, not a predicted receipt fact.

The complete atomic set C is exactly the decision bundle, single-use consumption binding, preparation receipt, coverage manifest, payload digest/bindings and required retained payload evidence. Under Scope A, that consumption binding means the attempt is permanently spent; its presence alone does not assert timely authority use. Referenced immutable proof objects must already exist and verify under the selected retention/commit contract; a dangling or future ref is not membership. Atomic activation of a previously staged content-addressed blob may satisfy the byte component only if the selected storage/custody owner proves its durability, immutability, permitted access and required retention before C. This does not assume a distributed transaction or make an unverified blob acknowledgement sufficient.

Authoritative commit proof must identify the whole set, its unique attempt/decision membership and atomic outcome. It is obtained from the transaction owner, not a success flag inside the candidate receipt. Store constraints must prohibit another consumption or preparation success set for the same attempt/decision. An authoritatively committed incomplete or inconsistent set is an integrity breach, not a smaller valid success set. Incomplete uncommitted preparation instead prevents finalization; an unconfirmed set remains unknown pending authoritative reconciliation.

Avoid digest cycles: payload bytes do not contain their own digest or preparation-receipt digest. Preassigned immutable IDs may connect records; external content digests cover the exact declared projections. The decision bundle retains PR #11 §18.8's exact two JSON-pointer exclusions, not a generic exclusion by field name. Coverage/transcript hashes cover their complete canonical bytes externally with no self-hash field. Later outcome records reference the already final receipt digest; the earlier immutable receipt is not backfilled with their digest. Future schemas must make every projection and reference edge exact.

### 9.2.1 Scope A alignment — actual initiation and late settlement

Consume PR #11's proposed §18.5.1 rule without broadening it. **I is the transaction owner's actual entry into execution of the single finalization operation for the complete, validated, frozen C set and the original live attempt.** At I, the owner must enforce trusted time strictly before D and the original attempt's still-live right to initiate, ordered against irreversible termination without a check-to-start gap. A preparation step, earlier clock check, request send, queued intention or acknowledgement of queueing is not I. The actual entry event, trusted time and exact set/attempt identity must be independently verifiable by the read owner through the bound transaction source, not a claimed flag or pre-commit timestamp. No PostgreSQL mechanism is selected by this requirement; RD-BIND03 remains open.

Before I, complete all preparation and non-temporal/source/coverage guards and independently verify lawful persistence/retention of the exact immutable set, including continuation after read expiry. Incompatible custody, sovereignty or retention authority prevents I; this timing exception supplies none. After I, continuation is only the same operation's settlement, not a new evaluation, buffer, retry or finalization request. I at or after D or after irreversible termination is forbidden, even if a precheck was before D. No knowingly late start or retry is allowed.

The already-initiated operation may reach actual C after D if its independent persistence policy permits it. Every complete C permanently spends the decision/attempt, including late C or lost acknowledgement. Late evidence proves non-reusability, not valid authority at the later commitment instant, timely consumption or delivery. Actual C and its later acknowledgement remain distinct. Unknown commit time stays unknown; do not backdate or rewrite any immutable evidence from a prior clock sample. The preparation receipt describes only established preparation facts, while the transaction owner's authoritative evidence and later linked observations establish actual initiation/settlement facts without predicting them at P.

If D is reached without L, disclosure eligibility is irreversibly lost regardless of pending finalization. The original owner must have conclusive acknowledgement of complete C and pass every atomic handoff guard strictly before D for L. Settlement or reconciliation afterward cannot restore it. Source protection, full membership, non-temporal guards, no takeover/replay, and truthful failure axes are unchanged. This read-only exception changes no state-affecting write, human finalization, filing or custody rule.

### 9.3 Preparation is not disclosure

The preparation receipt's completion claim means **read preparation completed before disclosure**. It records trusted preparation facts and the transaction identity, but has no asserted actual-disclosure time or delivered flag. Actual commit outcome/time comes from the transaction owner's authoritative commit evidence after C; a timestamp sampled while constructing the receipt is not reported as the commit instant. Outcome evidence separately records which of these owner-observed facts can be established:

- `STOPPED_BEFORE_DISCLOSURE`: the sole live owner was irreversibly fenced before L; proof establishes no other path could disclose, with the stop time and actual cause.
- `DISCLOSURE_ATTEMPT_OBSERVED`: the owner observed L for the exact bound buffer, with its trusted time and egress/invocation witness. This proves the disclosure attempt at the defined output boundary, not full delivery.
- A linked completion/failure observation after L: exactly which portion of the bound buffer the egress contract proves it accepted, or that acceptance extent is unknown. “Whole buffer accepted” is permitted only on authoritative evidence for the complete buffer, not a successful database transaction or a queued send.

These are internal read-outcome tags, not authorization outcomes or public codes. Each record carries its actual observation/recording times separately. L's time cannot be invented from C's time. The buffer digest identifies the complete intended application response, not a claim that every byte reached the recipient; an acceptance-extent observation must bind the exact supported subset/prefix or explicitly leave extent unknown. Absence of a stop/attempt record leaves disclosure unknown. A crash can lose the truthful observation before it is recorded; the model deliberately does not claim an atomic database/network event or exactly-once delivery.

Existing observed release time/facts remain immutable after retention expiry or later failure. A later observation can add supported facts or limits, never rewrite the original bytes, posture, authorization or claim that a previously unproved delivery was known at C. The read-outcome tag is not a PR #34 dispute/correction and cannot change PR #35 classification.

## 10. Ordering from admission to disclosure

The logical read transaction is the trusted lifetime from A's live invocation through L or an irrevocable stop. Its database evidence commit is a step inside that lifetime, not permission to transfer the consumed decision to another transaction.

| Point | Required action and permitted fact |
|---|---|
| A — admission | Persist/verify unique attempt ownership and immutable binding. No protected bytes or consumption |
| S — observation | Obtain the one governed view, real pre-evaluation qualification and complete source/authority inputs; evaluate current authorization. A limited WITHHELD historical reply's final S must be inside §8.3's already established protection |
| P — preparation | Verify remaining gates, history, coverage and retention; finalize CP2 and freeze/hash exact buffer; construct/validate complete evidence. Preserve the independently selected disclosure branch and required seal proof |
| I — actual finalization initiation (Scope A) | Transaction owner actually enters the one operation under §9.2.1, with complete frozen preparation, independent persistence authority, a live original attempt and trusted time before D. Prior checking/queueing is insufficient |
| C — actual atomic evidence commit | The §9.2 set and single-use binding actually commit together. C is not its acknowledgement. An operation initiated at eligible I may settle after D under §9.2.1, permanently spending the attempt without disclosure authority. Conclusive acknowledgement is separately required before L; the WITHHELD seal survives C |
| L — one disclosure linearization point | In the same original live invocation, atomically validate/consume the non-transferable handoff capability under the guards and deadline, and irrevocably hand the exact buffer to the bound protected-output boundary |
| O — observed outcome | Append only supported stop/attempt/acceptance/failure evidence. Delivery beyond that boundary is not inferred |

L is the first irreversible handoff at which any protected bytes from this buffer may become available outside the protected read owner. If a proxy, middleware queue, cache or logger can expose them earlier, that is the real boundary and it must be guarded as L. A mere “send scheduled” call that leaves an unguarded queue to decide later is insufficient. The actual egress binding must name the boundary and enforce at most one handoff, no handler/proxy retry or replay cache, and no mutation of the bound application payload. Ordinary network packetization of an already complete buffer is not permission for incremental protected-result production.

At L, all of these must hold together:

1. A's original sole live owner, exact invocation/session and read-transaction identity remain valid; no cancellation, owner-loss or prior handoff has consumed/fenced the capability.
2. C has been conclusively acknowledged with complete exact membership; no partial set, pending commit or unresolved storage integrity is present.
3. Trusted time is strictly before D as defined in §5.2. Relevant authority, currentness, sovereignty, retention, policy and byte-availability guards cover through L under §6.1. Scope A permits no late handoff, and Scope B supplies no extra time.
4. The final buffer and all receipt/coverage/serializer bindings remain exact, and the history reply meets its §8 branch. A limited WITHHELD reply has continuous, independently verified RD-BIND03-W protection from its final S through L; no hidden-history conflict/cancellation check can substitute for it. A disclosable-history reply must not use an invalidated observation. Policy-excluded original results have no successful read C/L to authorize here.
5. The bound egress can accept the one immutable buffer under its reviewed semantics, with no alternative unguarded response path.

Failure of any condition irrevocably suppresses this attempt; no protected bytes may cross L. A committed consumption remains spent even when L never occurs. Record that distinction truthfully. Scope B permits only §8.3.1's specific deadline outcome; it does not certify a provider that permits §8.3's forbidden hidden-only interleaving or post-actual-C acknowledgement delay. Those failures still violate C38/RD-C20 and block the binding. Do not trade stale disclosure for privacy or call fail-closed suppression a conforming positive case. If L has already occurred, cancellation or later revocation cannot unsend bytes; do not claim zero disclosure. This protocol creates no later independent dispatch or filing transport attempt: `NO_EXTERNAL_DISPATCH` is unchanged, and #13/PR #11 §18.6 filing transport semantics are outside scope.

## 11. Failure, uncertain commitment and retry

Evidence commitment and disclosure are separate axes. Internal reconciliation distinguishes `EVIDENCE_COMMITTED`, `EVIDENCE_NOT_COMMITTED`, `EVIDENCE_COMMIT_UNKNOWN` and `EVIDENCE_INTEGRITY_BREACH`. Disclosure remains not attempted, observed attempted or unknown according to actual evidence, with any supported acceptance extent separately stated. These are runtime facts, not additions to the authorization lattice.

| Failure or race | Required behavior |
|---|---|
| Invalid ingress or missing trusted admission context | Zero protected bytes; no fabricated authorization bundle. Existing rejection/audit rules only |
| Non-ALLOW evaluation | No consumption or protected payload. Persist the valid refusal bundle through PR #11's existing non-ALLOW protocol; use only the approved safe response |
| Qualification/coverage/retention failure before I | Prevent finalization, discard uncommitted payload under its policy, retain only truthfully owned failure evidence. A valid earlier ALLOW is not changed to DENY |
| Cancellation or D reached before actual I, including a precheck followed by a pause | Refuse initiation and fence the attempt; no L. An earlier check/send/queue entry cannot authorize late I |
| D or irreversible termination reached after eligible I but before C | Fence L permanently; no new initiation/retry. Reconcile the already-running operation's real outcome; complete late C stays spent only under Scope A and independent persistence authority |
| Relevant guard invalidation before I | Abort/rebuild the whole unsealed read where §8 permits, otherwise stop. Never retain a stale decision or buffer as the winning attempt |
| Relevant non-temporal guard invalidation after I | No waived guard or replacement preparation; fence L and resolve the actual operation outcome through its owner. Scope A does not certify a violated source/persistence contract |
| Definitive C rollback/persistence failure | Zero protected bytes. `READ_EVIDENCE_PERSISTENCE_FAILED` or the applicable decision-bundle failure is a runtime/integrity disposition with no authorization reason rank |
| C acknowledgement lost or commit result uncertain | Immediately fence further handoff. Zero protected bytes from this attempt; preserve uncertainty and reconcile with the authoritative transaction owner. A later discovered complete C does not reopen L |
| An authoritatively committed C set is incomplete or inconsistent | Integrity breach; suppress disclosure, quarantine this attempt's execution and report through an already authorized incident path. Do not fill missing members, delete fragments, grant repair powers or call it NO_EFFECT; incomplete preparation or unknown commitment is not this finding |
| Expiry, cancellation or independently relevant guard invalidation after C but before L | Consumption stays spent; fence L; append a proved stop if possible. No finalized evidence rewrite, rollback fiction or automatic retry. Hidden-history-only conflict is not an ordinary guard-failure substitute for §8.3 |
| Newly learned potentially material committed history after C before L, where status/time is disclosable | Suppress the old attempt under §8.2, including unresolved admission/classification. Consumption stays spent; no stale reply, rewrite or replay |
| Covered pre-disclosure storage wait still outstanding at D | Only §8.3.1 permits a limited WITHHELD success-versus-deadline-failure difference. Prove the exact causal wait, fence L and preserve actual commit uncertainty; do not label this a version 2 privacy pass |
| Competing hidden qualifier while a permitted WITHHELD reply is sealed | A conforming RD-BIND03-W provider orders its commit after L/termination. With the same independent conditions permitting L, a candidate newly offered after actual C must preserve the same limited reply, including timely C acknowledgement. If it delays that acknowledgement past D, actually commits in the protected interval or exposes a pre-cut omission, fail closed and fail provider conformance; no permitted deadline exception |
| Hidden candidate learned on a policy-excluded historical lookup | Keep the same existing qualified exclusion response and omissions. There is no successful C/L for that excluded historical-result payload; do not create one or change the public failure category because of internal history |
| Crash before C, including after actual I | No protected handoff; resolve admission/finalization uncertainty from owner evidence. An already-initiated operation may still settle as Scope A permits; a surviving admission or complete C cannot be taken over |
| Crash after C but before or around L | No replay/takeover. Commit may be established independently; a receipt alone cannot establish whether L occurred. Record disclosure uncertainty unless independent exact egress/stop evidence resolves it |
| Disconnect known before L | Fence and stop; no L. Mere absence of a client acknowledgement is not proof that no earlier handoff occurred |
| Disconnect, expiry or crash after L | Preserve the attempt fact and any known acceptance extent; delivery may be partial/unknown. No rollback of consumption and no promise of zero bytes |
| Outcome-observation persistence failure after L | Never report overall zero disclosure or undo C. Preserve/reconcile independently available observation evidence; otherwise outcome is unknown. No second handoff to repair audit evidence |
| Required retained payload later unavailable | Preserve original posture/receipt/observed facts; report current reconstruction limits and retention failure under PR #29. Missing bytes cannot be silently replaced |

Reconciliation uses authoritative exact admission/transaction membership/uniqueness evidence and the bound egress observation source, with the same tenant/principal/intent identity and verified original contracts. A missing lookup row, stale replica, timeout or absence of O is not conclusive rollback or non-disclosure. Full matching C proves evidence commitment only. A STOPPED_BEFORE_DISCLOSURE claim additionally needs the irreversible sole-owner fence and proof that L was never crossed. If the actual provider cannot establish one of these, keep that axis unknown.

There is no same-identity protected response retry in v0.1. An exact duplicate may receive only its independently authorized non-protected status/qualification projection; it cannot return the old buffer, receipt internals or trace. A changed request/session/profile does not start another lifecycle under that tuple. A separately requested new read uses a new request identifier, fresh current authority and a newly constructed evidence/coverage set, even for identical content. No old ALLOW, consumption, history result or retained bytes confer authority on it.

Keep the immutable admission identity and required reconciliation/tombstone evidence under PR #29's compatible schedule so expiry or cleanup cannot make the tuple appear unused. If that retention cannot coexist with policy limits, reject new admission under the conflicting profile. This read identity discipline does not amend PR #26's retryable no-effect operations.

## 12. Retention and public-path stops

Resolve the immutable evidence-retention policy independently at S, with purpose, tenant, sovereignty and evidence-class constraints. Bind the exact schedule and its pending/terminal event semantics; if a terminal event is unknown, do not invent a completed schedule. Guard policy and required byte availability for actual persistence and disclosure. Scope A requires independently lawful continuation/settlement of the already-initiated evidence operation after read expiry; it does not extend any custody, sovereignty or retention limit. If that authority is incompatible, prevent I rather than infer permission from audit needs.

| Pre-disclosure condition | Required result |
|---|---|
| No applicable verifiable policy | Read ineligible; no protected bytes and no claim of v0.2 conforming evidence |
| DIGEST_ONLY but necessary transient processing is prohibited | Read ineligible before payload construction; no hidden persistent copy, log or crash-dump workaround |
| Mandatory immutable receipt/coverage/decision/trace retention remains incompatible after permitted minimization | Read ineligible; report the exact conflict to #14/PR #29's owner. Do not drop required proof or promise later receipt redaction |
| RETAINED_BYTES without already verifiable exact-byte custody and required retention capability | No C/L; a future upload or unverified storage pointer cannot satisfy the promise |

With RETAINED_BYTES, original exact application bytes remain reconstructible only while actually available. With DIGEST_ONLY, later supplied candidate bytes can be compared under current authorized access, but the receipt does not reconstruct them or prove their origin/delivery. Later deletion never downgrades the original posture or removes immutable evidence. Retention minimums, maximums, holds, cleanup, encryption and keys stay with their owners; this protocol grants none of them.

The same protected-output choke point covers successful payloads, caches, errors, counts, metadata, trace lookup, qualification and retry. A safe-response path can return only what PR #31 and the bound disclosure policy independently permit. It cannot leak a private failure reason, reveal original-record existence or include a debug trace because the protected read failed. Public code registration and constant safe-message text are not changed here.

## 13. Named invariants and review cases

These are acceptance obligations and symbolic cases, not executed tests or claims that the currently missing bindings work.

| Invariant | Required property |
|---|---|
| RD-I01 | Valid ingress, independent selection, trusted invocation and one tenant/principal/session-bound live attempt |
| RD-I02 | One complete governed view and actual positive/negative/set-valued source proof; source/non-temporal guards remain intact. Under Scope A, actual I and L are strictly before full D; only already-initiated evidence may settle late under independent persistence authority |
| RD-I03 | Genuine eligible pre-evaluation qualification; no future-fact cycle, dummy evidence or reference-as-proof |
| RD-I04 | One exact target/form and independently sufficient selected path; no cross-path/layer union or hidden target narrowing |
| RD-I05 | Complete information/origin coverage, including legitimate artifact contents and inference-sensitive metadata/counts |
| RD-I06 | Exact immutable buffer/serializer and full atomic decision/consumption/receipt/coverage/payload set acknowledged before L; every complete C spends the attempt, including Scope A late settlement or acknowledgement loss |
| RD-I07 | Preparation, one possible disclosure attempt, acceptance extent and delivery are distinct truthful facts |
| RD-I08 | No stale/late handoff, late initiation/retry, lost-owner takeover, protected replay, duplicate consumption, backdating or guessed reconciliation; continuation of the one eligible I is not a new attempt |
| RD-I09 | PR #35 complete same-context history, original admission and known-candidate refresh; no finalized rewrite |
| RD-I10 | PR #31 nulls/withholding/safe messages/C38 with only its proposed Scope B deadline exception; no extra hidden-selected public differences, and safe fallback does not prove producer readiness |
| RD-I11 | PR #29 pre-disclosure eligibility and truthful retention/reconstruction limits |
| RD-I12 | Exact binding, owner and stage separation; no approval, currentness or runtime claim from this draft |
| RD-I13 | Scope B allows only the explicit covered-wait success-versus-failure difference at D. A permitted WITHHELD reply still requires actual RD-BIND03-W ordering; the positive pair begins at actual C, including before acknowledgement. Uniform exclusion stays uniform; hidden-only post-C suppression/acknowledgement delay is provider failure |

| Case | Required observation and expected result | Invariants |
|---|---|---|
| RD-C01 Direct read, including separately permitted AUTHORIZATION_TRACE | Exact target and permitted projection, no invented query inputs; full positive C/L path. Full trace bytes cannot piggyback on another result | I01–I08, I10 |
| RD-C02 Query read | Exactly one specification and plan as integrity inputs; complete result/origin membership, correct parameters and positive C/L path. Missing/extra query input fails | I02–I06 |
| RD-C03 SharingGrant aggregate | §7.3's DOC1/O1/O2 positive content mapping without independent raw-origin grants; negative twins for raw expansion, private annex, forbidden cross-farm input, wrong revision and incomplete origin enumeration | I04–I06 |
| RD-C04 Direct versus delegated versus sharing basis | Each applicable complete path succeeds independently in the one policy decision; partial action/purpose/evidence paths never combine. Post-evaluation path substitution fails | I04–I05 |
| RD-C05 Historical complete empty history | Independently exhaustive original-source enumeration yields AVAILABLE/NONE at actual c, not hard-coded empty success; original result remains unchanged | I02, I09–I10 |
| RD-C06 Older valid qualifier, current writer excluded | Verify original admitted package/rule/source/commit proof and complete history. No current write authority inferred; absence of old proof stays unresolved | I02, I09, I12 |
| RD-C07 Mixed snapshots or incomplete membership | Missing page/partition, hidden row, stale index, unsupported historical version or unresolved candidate identity prevents complete classification; independently permitted limited handling only | I02, I09–I10 |
| RD-C08 Known post-cut committed candidate with disclosable history | Inject before sealing and after C, including unresolved admission/label. First rebuilds whole read or independently permitted limited payload; second suppresses old attempt. No label-only patch or policy switch to WITHHELD. Hidden-history combinations are C20/C21 | I02, I08–I10, I13 |
| RD-C09 Authority/guard/time invalidation | Race revocation, session/policy/resource expiry and retained-byte loss around I/C/L using full D, not just the later request deadline. Precheck before D, pause until D before actual I: refuse I. Actual I and L at D fail; eligible I before D followed by complete C after D stays spent with no L. No backdated timely-consumption claim; post-L cannot unsend | I02, I06–I08, I11 |
| RD-C10 Uncovered information | Inject aggregate, count, metadata, lineage, link, header or error detail outside coverage. Redact/recompute only under policy or stop; no alternate path/cache leak | I05–I06, I10 |
| RD-C11 Forged or circular qualification/context | Mixed tenant/session/attempt/cut, caller policy, fake proof and missing real qualification fail; a policy-derived real evidence reference is accepted without a redundant carrier | I01–I03 |
| RD-C12 Persistence and uncertain commitment | Distinguish incomplete preparation (prevents I/C), definite rollback, unknown commitment/lost acknowledgement and authoritatively committed incomplete/inconsistent C (integrity breach). No L in those paths, fabricated DENY, second consumption or repair-by-replay. Later complete C, including late settlement, remains spent and does not revive L | I06–I08 |
| RD-C13 Crash/disconnect/retry | Fault immediately before/after I, C, L and O; preparation never proves delivery. Include a precheck/pause across D before I, termination before I, eligible I followed by late settlement and a requested late retry: no late initiation/retry/L, no takeover or old-buffer replay. Continuing the already-initiated operation may settle truthfully; fresh requested read needs new current decision | I01–I02, I06–I08 |
| RD-C14 Three retention stops | Missing policy, prohibited transient buffer, incompatible immutable proof retention: no protected bytes, truthful ineligibility/conflict, no weakened posture. Scope A variant: independent policy cannot authorize settlement after read expiry; refuse incompatible I, no assumed audit/retention waiver | I02, I11 |
| RD-C15 Proof posture and later loss | Positive RETAINED_BYTES and DIGEST_ONLY paths, later permitted deletion/unexpected loss/candidate comparison. Preserve original posture; never invent reconstruction, origin or delivery | I06–I07, I11 |
| RD-C16 C38 hidden-history pairs | For each independently allowed limited/excluded policy path, vary only hidden history, including NONE/disputed/unavailable. Public outputs match apart from Scope B's explicit covered-wait success-versus-deadline-failure distinction; exclusions always match. Include PR #31's C38 cross-expiry pair: acquisition blocked with settled commitment facts versus unresolved read-evidence finalization, both using that owner's identical HISTORICAL_READ_EXPIRED projection while internal facts remain distinct. No additional content/category/diagnostic/hint/reference/omission difference. Include C20/C21, not just delivered-field comparisons | I09–I10, I13 |
| RD-C17 Concurrent duplicate admission | Same tuple/different handlers or sessions yields one live owner; differing caller facts conflict. Lost A acknowledgement yields no continuing protected attempt | I01, I08 |
| RD-C18 Boundary and payload bypass | Proxy queue retry, middleware auto-send, altered serializer, buffer mutation, embedded self-digest or forged commit flag fails. Genuine one-buffer handoff remains positive | I06–I08 |
| RD-C19 Full selected closure | Cover all ten scope and twenty record/artifact target alternatives with their applicable paths; reject unselected actions. No fixture silently makes a selected branch permanently unavailable | I04, I12 |
| RD-C20 Combined late hidden history and C38 | Pair same permitted original, authority/session/retention, deadline and independent faults, varying only a hidden candidate offered between actual C and L, including before C acknowledgement and with unresolved admission. Both limited WITHHELD replies reach L and the candidate actually commits afterward. Candidate-induced acknowledgement delay past D is provider failure, not Scope B expiry. Actual intervening commit also fails. Policy exclusions remain identical with no invented successful C/L. Retain C08's disclosable-history comparator | I02, I06–I10, I13 |
| RD-C21 Seal closure and admission adversaries | Candidate committed before acquisition but notified after C, omitted partition/import path, malformed/unresolved root, qualifier of qualifier, excluded current writer, forged/released seal, optimistic abort and hidden-dependent waits. Require complete pre-seal reconciliation and full protection. Timely acquisition retains the positive pair; only an evidenced §8.3.1 wait through D permits failure versus success under the amended privacy rule. Early timeout, artificial delay, history-classification difficulty, missing coverage/retention and arbitrary pool exhaustion are not covered. No notification blindness or empty-history fallback | I01–I03, I09–I13 |

For C20's limited-reply positive pair, observe **actual commit order, C acknowledgement and public output**, not merely whether the gate returns success. One execution has no competing candidate; the other attempts to commit it in the protected interval. With the same independent conditions permitting L, both disclose their covered limited result exactly once, and the latter candidate's actual commit is proved later than L. A harness that permits the candidate to commit first, or to delay acknowledgement of already-complete C beyond D, and then reports sanitized failure has reproduced the retained blocker and must fail. A candidate already committed before protection belongs to final S; its absence is a completeness defect even if admission remains unresolved.

The required acknowledgement variant is explicit:

| Case | Required result |
|---|---|
| Actual C commits; before acknowledgement reaches the original owner, a newly offered hidden candidate's writer delays that acknowledgement past D | Provider failure under RD-C20, not Scope B's deadline exception. Fail closed; suppression does not count as privacy conformance |
| C acknowledgement is genuinely lost through the same independent fault in the compared executions | Suppress L under §§10–11. Never force disclosure without acknowledged complete C or treat subsequent reconciliation as revival |

For C21's allowed deadline variant, prove a covered causal storage wait through the original D and compare with a no-hidden-writer execution that succeeds. Label the difference as the new privacy tradeoff, never a passing version 2 case. C09/C12/C13 separately verify Scope A's late-settlement and initiation boundaries; Scope B does not authorize late C by itself.

For C20's exclusion pair, compare the governing safe-response preparation/finalization boundaries rather than inventing a successful read receipt for an excluded original. Vary the same hidden candidate before/after that preparation and before outward response. Both keep the identical policy-permitted exclusion category, text, hints, references and omission pattern. If that response contains any independently protected information, its own existing owner controls still apply identically; exclusion is not a disclosure bypass. C08 separately confirms that disclosable-history changes still require refresh or suppression. Tests of actual provider faults record conformance failure honestly; they do not claim C38 from fail-closed behavior alone.

### 13.1 Issue acceptance traceability

| Issue #36 criterion | Protocol sections | Invariants / cases |
|---|---|---|
| 1 — trusted attempt and selection | 4–5 | I01–I02; C11, C17 |
| 2 — one view and real guards | 6, 8, 10 | I02, I09, I13; C05–C09, C18, C20–C21 |
| 3 — pre-evaluation qualification | 6.2 | I03; C11 |
| 4 — coverage, direct/query and sharing | 4, 7 | I04–I05; C01–C04, C10, C19 |
| 5 — atomic evidence and ownership | 9–10 | I06–I07; C12–C13, C18 |
| 6 — failure, expiry, uncertain commit and retry | 10–11; compatibility §3.2 | I07–I08, I13; C09, C12–C13, C17–C18, C20–C21 |
| 7 — historical source observation/reply | 8 | I09, I13; C05–C08, C20–C21 |
| 8 — public privacy and retention stops | 8, 12 | I10–I11, I13; C14–C16, C20–C21 |
| 9 — explicit invariants and positive/hostile coverage | 7.3, 13 | I01–I13; C01–C21 |
| 10 — exact later bindings and stages | 3, 14–15 | I12–I13; C19–C21 |

## 14. Actual bindings still owed

No existing live read provider is certified here. At inspected OFARM2 main `9d7541d96bc708e9270b986927d7f4b8a035454f`, `kernel/tenant_uow.py` supplies tenant/write transaction facilities; `kernel/migrations/0003_tenant_knowledge_position.sql` supplies tenant write ordering; and `kernel/store.py` provides tenant-scoped historical record queries. Those do not establish a complete v0.2 read observation, all historical admissions, C-to-L guard or egress contract. `kernel/api.py` still blocks governed routes. This is a missing capability, not evidence of an unsafe enabled reader.

At the separately authorized draft stages, materialize closed read profiles within the existing package families, with actual content-addressed dependencies. Proposed destination for the read-specific evidence/protocol profiles:

```text
03_machine_contracts/drafts_non_default/authorization_finalization_evidence_v0_2/
```

This is a proposed directory, not a current asset or selected identifier. Final exact filenames, IDs, versions, canonicalization/digest projections, example bytes and dependency hashes belong to that bounded materialization review. Authority-snapshot and source-history profiles retain their decision-evidence owners; required-evidence policy/intent/extractor bindings retain the policy-bundle owner. Do not create a fifth package family or substitute this prose's name for real bytes.

| Binding | Exact deliverable needed | Owner / current status |
|---|---|---|
| RD-BIND01 — read contract/evidence closure | Closed attempt, preparation, coverage, consumption, outcome and guard-proof schemas; exact package/intent/evidence/serializer projections and real example bytes/digests; atomic membership verification. No self-hash or future-outcome cycles | #36 with #10/#21 bounded policy/decision/finalization drafts; open |
| RD-BIND02 — trusted invocation and qualification | Actual tenant/principal/session and independent package/role/implementation selection, protected attempt provenance, qualification source/verifier, exact policy-derived evidence-reference behavior and an acyclic producer-to-evaluator path | Identity/selection and read/qualification runtime owners; design/selection bindings needed before closure, executable implementation at stage 11; open |
| RD-BIND03 — transaction/observation/egress | Named authoritative collections/providers, consistent cut/time mapping and visibility/exhaustion proofs; currentness/negative/set guards with all participating mutation paths; admission/success uniqueness; actual I proof, atomic C distinct from acknowledgement, truthful late settlement/reconciliation, actual C-to-L protection, owner-loss fencing and one-handoff egress. RD-BIND03-W requires §8.3's complete-universe acquisition/final-cut/commit-order guarantee, only §8.3.1's enumerated deadline exception, and C20/C21 actual-C/acknowledgement/public-output proof | Source/storage/read transaction owners under existing OFARM2 #392; no isolation, role or lock chosen here; open, including RD-BIND03-W and the retained post-C progress obligation |
| RD-BIND04 — full target/content coverage | Exact source/assembly/live-view content and origin-membership contracts for all selected targets; applicable direct/delegated/sharing coverage, redaction/inference proofs and conditional query/plan binding, including §7.3's positive case | Existing source/artifact and authorization owners with read coverage verifier; open. New content permission needs separate owner approval |
| RD-BIND05 — history producer/consumer | HSP-BIND01–04's exact profile, historical inventory/original admission, complete same-S observation, invocation verifier, reply-validity and PR #31 projection; QG original source dependencies preserved. Verify §8.3 ordering, unchanged refresh and only the owner-approved Scope B privacy exception once reviewed; no producer exemption for hidden data | #32/#33/#30 with read owner; historical path only here, fresh-command reply separate; open |
| RD-BIND06 — retention/public safety | Exact PR #29 policy/schedule/custody capability, mandatory immutable proof minimization, post-outcome uncertainty handling, safe lookup/status and C38 policy/verifier bindings | #14/#30 and storage/custody owners; no new grants or public codes; open |
| RD-BIND07 — selected conformance | Production-reachable positive/negative assets for C01–C21 and the full selected read scope, real concurrency/fault/byte-observation harness, exact versions and results; C20/C21 must measure actual commit order and both C38 public policy paths together | Canonical hostile conformance then separately scoped OFARM2 runtime verification; open |

Each binding must name the exact source/profile/version/digest, its semantic owner, verified authority and implementation/selection boundary, equality/proof rules, failure behavior and the evidence closing it. A digest only identifies bytes; the supplied proof must establish the promised property. Design bindings and static conformance precede runtime implementation; live durability/concurrency tests cannot be required before their own implementation is authorized, and cannot be claimed from this document.

The decisive external gap is the actual complete observation and C-to-L provider/egress mapping, not the syntax of a frame. Existing database commands or write positions are candidates for reuse only. If the mapping requires database changes, broader source inspection, a new authority action or altered selected-rule semantics, that is a separately reviewed owner change before binding. Do not automatically open a new service/prerequisite for every empty table row.

## 15. Stages and approval record

Preserve all eleven PR #11 §24 stages for the complete selected closure:

1. This Phase A candidate only.
2. Exact-head semantic-profile/release-scope approval; no accepted law yet.
3. Complete applicable adjacent contracts, including the separate read, write, public/history and retention owners.
4. Separate non-default policy-bundle draft with exact selected intent/extractor/evidence/transaction bindings and real digests.
5. Separate source-bundle draft for the closed immutable authority sources; no automatic v0.1 promotion or migration.
6. Separate bounded decision/finalization-evidence drafts with the complete selected profile closure, including this read's distinct receipt truth claims.
7. Exact selected binding/closure review and scoped accepted law. Reconcile historical dependency pins, writer-deferral proof and every remaining owner obligation. Semantic changes return to stage 2.
8. Separate hostile conformance for all selected branches, with positive cases and honest result reporting.
9. Explicit scoped current/default promotion, proving no omitted action/profile becomes executable.
10. Byte-identical canonical extraction into OFARM2, checked by digest.
11. Separately authorized OFARM2 runtime work and live verification in its own trust-boundary PRs, returning to #359 and the established backlog sequence.

No stage authorizes the next by implication. G2, G3-READ, G3-HANDOFF, other applicable G3 obligations and G4 remain open. The four package families and the two-action selected scope are unchanged; the other eighteen catalogue actions remain deferred, not passed. This proposal neither activates qualifying-record writing nor proves it deferrable. It does not merge any PR.

Proposed decision ID: `OFARM-ISSUE36-GOVERNED-READ-TRANSACTION-COVERAGE-DISCLOSURE-001`.

Version 2 is the approved predecessor at `41cd45b90fb8e133f6377d8f389858b89c3dd7ae`; these Scope A/B amendments are **draft-authorized only, not semantically approved**. Version 1 at `c2c52fa27bec24e72285564057cab198e4654e36` received the B1 request for changes, not semantic approval. Renewed owner review/approval must identify the revised exact bytes/head; a self-referential commit hash is not embedded in the candidate.

Renewed review covers the bounded owner-derived changes in §15.2 and their affected invariants, not a reopening of unchanged artifact-content, selected-path, source-history or identity decisions. Approval would not certify the missing bindings in §14, including RD-BIND03-W, or grant another owner's authority. In particular, review must preserve the distinction between the permitted pre-disclosure deadline difference and the still-required positive pair from actual C, including the acknowledgement race. Static consistency is not proof that a provider can supply it.

Original draft verification on 2026-09-14: all seven live owner heads and both main refs matched the recorded pins; the reviewed issue body was unchanged. Static checks found all ten issue criteria, twelve named invariants and nineteen case rows, balanced fences/table columns and the required Markdown spacing. `validate_repo_hygiene.py`, `check_generated_currentness.py`, `check_repository_cross_references.py` and `check_repository_steward_guardrails.py` passed without generated-file changes. These were document/repository checks only, not independent protocol review.

### 15.1 B1 correction and re-review scope

[Review 5194803845](https://github.com/samovers/OFARM/pull/37#pullrequestreview-5194803845) showed a valid counterexample: after C, a newly known hidden qualifier caused the old draft to suppress an otherwise permitted WITHHELD result, while its paired no-qualifier execution disclosed it. This contradicted C38 through result omission, even with a sanitized failure. The defect was in the proposed protocol, not a demonstrated deployed leak.

| Requested correction | Proposed version 2 response |
|---|---|
| Reconcile sealed invalidation and withholding | Sections 6.1 and 8.2–8.3 select the review's explicit-guarantee option: actual protected final observation and candidate commit ordering through L for every permitted WITHHELD limited reply. Optimistic conflict cancellation, hidden-only admission failure and delayed notification are explicitly insufficient |
| Add the combined hostile case | I13 and C20/C21 pair actual commit order with public behavior for limited replies and exclusions, include unresolved admission, pre-cut omissions and protection failure, and retain C08's disclosable-history refresh/suppression |
| Keep owner boundary explicit | RD-BIND03-W is an open source/transaction binding requirement within RD-BIND03, not a claimed existing capability or implemented database change. PR #31/#35 semantics and all source pins stay unchanged; any needed change to those owners requires separate review |
| Preserve consumption, immutable evidence, no replay and uncertainty | Sections 9–11 bind established seal evidence before C and verify actual continuity at L without predicting it. Existing suppression remains fail-closed on a real guarantee breach, but is not misreported as privacy conformance; spent consumption and finalized bytes remain unchanged |

Revision verification on 2026-09-14: all four cheap repository checks passed, all seven source heads and both main refs matched, and the one-file diff/whitespace and Markdown/table/traceability checks passed. The revision has ten issue criteria, thirteen invariants and twenty-one symbolic cases. Seven unaffected sections were compared byte-for-byte with the reviewed head, including full read scope, attempt identity, qualification ordering, sharing coverage and retention. Published-head/text read-back belongs to the external handoff after commit. No source-provider, database, concurrency, durability, delivery or privacy experiment is supplied by these static cases, and no such result or reviewer clearance is claimed. The actual binding remains open until its own reviewed evidence exists.

The version 2 revision stayed within **governed-read transaction integrity and protected disclosure**; its adjacent candidate bytes, runtime and active authority were unchanged.

### 15.2 Scope A/B drafting authorization and owner traceability

The task user approved both version 1 drafting scopes, including Scope B's explicit privacy downgrade, after the scope review found no blocking objection. The review's required definitions and acceptance refinements are included here; they create no third scope or new prerequisite. Authorization permits these draft revisions only, not eventual normative approval, implementation, provider admission, merge, promotion or extraction. Not provisional: no temporary implementation or waiver is introduced.

| Drafting scope / semantic owner | Owner draft above the pinned predecessor | Consumer alignment in this PR | Unchanged boundary |
|---|---|---|---|
| A — read-consumption timing and truthful evidence persistence; PR #11 | `authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md` at `e9052efcf3c673360d939e856ac866cb27d709ae`, §§18.2/18.5.1, affected invariants/cases | §§5.2, 9.2–9.3, 10–12; I02/I06/I08; C09/C12–C14: full D, actual owner-verifiable I, complete late C stays spent, strict L, no backdating/replay | No public-privacy weakening from A; no state-affecting write, human finalization, filing or custody/retention amendment |
| B — confidentiality of hidden history in public read outcomes; PR #31 | `cp2_authorization_result_surface_and_public_reason_codes_rfc_candidate_v0_1.md` at `907b934b44617fba01cd81b4ddb4ab8ca6979190`, §§5.2/5.4/5.4.1, 6, 8, I04/C38 | §§8.3–8.4, 10–11; I10/I13; C16/C20/C21: closed causal waits at D, uniform covered-expiry projection and C38 pair, explicit privacy cost, no extra public differences, actual-C positive pair including acknowledgement | No late-C permission from B; no uniform-exclusion, disclosable-history, fresh-command, classifier or source-admission amendment |

The owner entries identify the published, unapproved [Scope A amendment](https://github.com/samovers/OFARM/commit/e9052efcf3c673360d939e856ac866cb27d709ae) and [corrected Scope B amendment](https://github.com/samovers/OFARM/commit/907b934b44617fba01cd81b4ddb4ab8ca6979190), not amendments present in the predecessor source pins in §3. Both exact remote files were verified byte-for-byte against the authorized local drafts before this consumer revision was published. Their revised semantics must be reviewed together with these consumer clauses and subsequently bound; no old approval or rule digest silently changes. Shared D, C and L terminology does not transfer semantic ownership. Each owner can approve or amend its own text independently; this consumer cannot use approval of one scope to incorporate the other.

The existing attempt tuple, one original live owner, complete S/source universe, frozen buffer and full atomic C membership, protection through L/irrevocable termination, independent lawful retention, no protected replay, two selected actions, four packages and eleven stages remain in force. No scheduler, extension, new service, authority or runtime waiver is selected. OFARM2 #392 still owes the real initiation, observation, protection, progress, durability and egress proof; B1 is not closed by these drafts.

Scope stays within this PR's **governed-read transaction integrity and protected disclosure** boundary through traceable owner alignment. The independent authorization and public-privacy decisions stay in PR #11 and PR #31; no cross-boundary implementation is bundled here.

The [Scope B review](https://github.com/samovers/OFARM/pull/31#pullrequestreview-5213227671) requires a uniform truthful public projection for two covered expiry paths. The task user's subsequent “go” authorizes the owner's corrective draft and this limited alignment: §8.3.1 consumes that projection, RD-C16 consumes the added C38 pair, and the Scope B reference pins the corrected owner text. PR #37's [review of 56e549d](https://github.com/samovers/OFARM/pull/37#pullrequestreview-5213223286) found no separate corrective issue. This alignment does not change Scope A, source protection, C/L ordering, retry authority or any provider binding, and does not transfer the earlier review to the new bytes.

What is next: re-review PR #31's covered-expiry correction and only this corresponding consumer alignment, then obtain renewed semantic approval. Keep #392/B1 and every actual binding, acceptance, conformance, promotion, extraction, implementation and merge gate open.
