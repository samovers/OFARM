# OFARM Governed-Read Transaction, Coverage and Disclosure Protocol v0.1

Date: 2026-09-14

Status: non-authoritative Phase A proposal; exact-head review and semantic approval pending.

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
7. Historical refusal reads consume PR #35's complete observation and original-admission verification in the same read context. Newly learned potentially material committed history before reply finalization invalidates the whole prepared reply even when its classification is unresolved.
8. Retention, public privacy, original authorization outcomes and every adjacent owner's authority remain unchanged. Actual source, guard, egress and package bindings remain explicit prerequisites; a static worked path is not runtime evidence.

These are proposed semantics for exact-head review. The [issue re-review](https://github.com/samovers/OFARM/issues/36#issuecomment-5659896617) cleared the amended issue framing, not this protocol. The user's subsequent “no blockers, go” authorized this draft, not its semantic acceptance or later stages.

## 2. Primary trust boundary and PR limit

Primary trust boundary: **governed-read transaction integrity and protected disclosure**.

The entire canonical PR adds this one historical Phase A document. It changes no approved adjacent candidate, active law, schema, currentness pointer, database object, runtime code or OFARM2 asset.

| Adjacent owner | What this candidate does not change |
|---|---|
| PR #11 and identity/source owners | Principal resolution, representation, grant powers, action rules, selected-path ordering, evidence eligibility, authorization outcomes or exact per-action consent comparison |
| PR #20 / PR #26 | Human-finalization and state-affecting NOT_REQUIRED transaction semantics, retry rights or effect receipts |
| PR #34 / PR #35 | Qualifier authorship/admission/lifecycle, history classification, historical source universe or permission to inspect it |
| PR #31 | Public fields, reason codes, safe sentences, withholding policy or endpoint activation |
| PR #29 and custody owners | Retention duration, encryption, deletion, plaintext access, key custody or independent delivery attestation |
| Storage and runtime owners | Database isolation/locks/roles/migrations, new reader privileges, credential/session policy, trusted selection or a new audit service |
| Governance owners | Accepted law, materialization, promotion, extraction, merge or deployment |

This owner may define read ordering and its evidence truth claims. If satisfying them requires a new permission rule, cross-source access, storage guarantee or custody authority, stop before editing that boundary and name the exact prerequisite or stacked change. Missing future schema bytes alone do not justify another architecture issue.

## 3. Sources and compatibility

The active baseline outranks accepted RFCs, companions and machine contracts. Historical candidates and reader/currentness views do not override it. CP11–CP15 draft contracts remain non-default.

The seven owner heads below were rechecked on 2026-09-14: all open, draft and unmerged. Their recorded Phase A approvals are design inputs, not accepted law or executable package admission. Each candidate file is under `package_meta/history/clean_baseline_migration/phase_reports/` at its named head.

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
| PR #11 §24.1 cites PR #34 at `69682c2f918ef18756261a1186294cc3a5ebe44d` as unapproved | That is publication history, not the current source input. This draft uses approved version 2 at `c59fdbc75f26ee4694355adedd4df021f64b5131`, with [approval evidence](https://github.com/samovers/OFARM/pull/34#issuecomment-5654388700) |
| Whether PR #11 needs a compatibility update | Before selected-closure review, its ledger must reconcile the newer source input and approved read receipt refinement. No conflicting sharing, classifier or per-action-consent rule was identified by this comparison; no owner file is amended here. A substantive contradiction found in review returns to that owner, not to a local workaround |

PR #34 approval does not close QG-DEP01 or QG-BIND02–05. PR #35 approval does not close HSP-BIND01–04 or CP2A-DEP01. Neither today's excluded writer nor today's policy digest settles original admission or history completeness.

## 4. Exact admitted read shape

The initial release remains exactly `ASSERT_OPERATION_CLAIM` and `RECEIVE_READ_DATA`, with both complete unchanged action rules and their transitive dependencies. This document covers the latter's full selected scope, not only reads of operation claims. It adds no third action or new read target.

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

`authorizationEvaluatedAt` comes from trusted evaluation, not request time. `decisionValidUntil` is PR #11 §18.2's exact minimum of the transaction deadline and all applicable session, representation, authority, rule, freshness, resource, evidence and sovereignty ends. Ends are exclusive UTC instants. Failure to construct a required cutoff prevents a consumable decision. Consumption at C and disclosure at L must both occur before this minimum; the clock cannot be restarted after C.

## 6. One governed observation and real qualification

### 6.1 Snapshot and protection contract

S is one actual, consistent committed read view with a trusted cut c. A ContextSnapshot for interpretation, a transaction label or a list digest is not S. The owner must bind the source collections, membership predicates, exact revision resolution, query/plan/parameters, visibility rules, page/range exhaustion, negative/set-valued facts and authoritative commit-order evidence used by every required provider.

The same S must cover authorization, source retrieval, redaction, qualification, history observation, coverage and payload construction. Immutable external objects may participate only with an owner-supplied mapping proving the exact version and applicable membership/currentness at S. A remote “latest” fetch, sequential command snapshots or unrelated cached qualification do not join S merely by copying its ID. If all sources cannot join the view, this invocation cannot establish the protocol.

Positive membership alone is insufficient. Revocation absence, complete role/grant candidate sets, exhaustive query results and historical candidate absence each need their own complete observation. Tenant filtering cannot hide an applicable cross-source candidate and still support an all-clear claim. Conversely, this requirement grants no broader source access; unavailable lawful access is an owner binding/failure condition.

The read owner derives a complete guard set from actual dependencies, including principal/session/representation, applicable authority and revocations, target/input currentness, scope/sovereignty, rule selection, evidence freshness, relevant EnforcementChain facts, redaction/retention constraints and exact buffer identity. It must prove that relevant invalidation and L are ordered: a relevant change preceding L either is reflected in the admitted view/validation or prevents L. A check just before an unguarded send is not this guarantee.

The guard contract must span the evidence commit C through L, including exclusive deadline validation at L. A database commit that releases all relevant protection does not satisfy that interval by itself. The eventual provider must identify the real mechanism, every participating mutation path, failure/owner-loss behavior and the order witness. RD-BIND03 remains open until that mapping is reviewed. This proposal selects no database isolation level, advisory lock, cross-service lease or privileged reader. If a new storage/authority guarantee is needed, its owner must supply it separately.

Not every new committed record invalidates a read. Currentness follows the bound relevant-state policies; unrelated history advance alone is not a failure. Historical qualification is as of c with the additional known-candidate rule in §8, not a promise of latest global history throughout network delivery. No history-wide delivery lock is introduced.

### 6.2 Acyclic qualification ordering

The permitted dependency order is:

```text
admitted attempt + trusted selected rule + valid intent
  -> same-view plan/source facts and genuine required qualification inputs
  -> current authorization evaluation
  -> remaining applicable gates, final coverage/redaction and CP2 projection
  -> exact immutable buffer and complete evidence set
  -> C -> guarded L
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

This is a symbolic design case, not existing fixture bytes or deployed proof. A governed frozen DossierAssembly revision D contains one approved table and a computed total from exact origin revisions O1 and O2, within one permitted farm/tenant scope. Its verified assembly trace and immutable component membership show those table cells and the total are part of D. The bound policies permit sharing those contents for purpose P; they exclude a raw personnel field and a private annex. A current SharingGrant grants party G receipt of D at that exact revision for P, satisfies its entire read rule and passes sovereignty and all other constraints. G need not possess independent receive/use authority over O1 and O2.

The direct read of D requires no query pair. The internal manifest maps each visible cell and total to D's exact component locations, O1/O2 revisions, derivation and the selected SharingGrant; it proves the excluded personnel field/annex contribute no unauthorized inference to the result. Private origin identifiers are not copied into the public bytes. The final CP2 projection and serialized buffer are fully covered. With §§6 and 9–10 satisfied, C then L is a positive sharing path.

Change only the request to include the excluded annex, a live raw-source expansion or a cross-farm contribution forbidden by policy: the same grant no longer proves that payload. Authorized redaction/recomputation may produce a completely covered payload; otherwise disclosure stops. Change the target to O1 itself: D's SharingGrant is not authority for that separate read. Change only origin discovery to an unexplained partial list: coverage is unproved even if the visible total happens to match.

An independently sufficient direct or delegated RECEIVE_USE path can also cover D. Each is checked in full on its own; a direct path supplying action plus a SharingGrant supplying missing purpose/evidence never forms a sufficient combined path.

## 8. Historical refusal and public qualification

A `RECORDED_RESULT` lookup first verifies the original complete committed v0.2 refusal bundle and current read permission. It does not re-evaluate yesterday's authority to rewrite the original outcome, treat a v0.1 trace as v0.2, or reuse the original refusal as permission to disclose it. A full internal trace requires its separate exact AUTHORIZATION_TRACE read and all these controls.

Invoke the independently selected PR #35 producer/verifier for the exact original root, tenant/scope, A and S. Its observation enumerates the entire eligible historical source universe before admission filtering, including qualifications of qualifiers, former packages and applicable imports/migrations. It establishes each act's original admission or proved invalidity; unresolved original authority, membership or identity is not absence. Use its independently verified exhaustion/source/order evidence, not today's admitted writer list, an index watermark or a receipt saying only that the original refusal committed.

Current writer exclusion is compatible in principle with verifying an older valid qualifier. It proves neither that the historical universe is empty nor that authoring can be deferred for this release. HSP-BIND02/03 and the applicable QG bindings still owe that actual proof.

The producer's verified cut and transcript belong to the same read as every returned original-result byte. Before reply finalization at L, learning of a potentially material committed candidate after c invalidates the prepared history reply even if original admission or its effect on the label is still unresolved. The owner must do one of the following:

- Before final payload/evidence sealing, discard all dependent preparation and obtain a new complete S, rebuild/revalidate the whole read and use a fresh authorization evaluation within the original fixed deadline. The original caller intent, requested target revision, logical identity and live owner cannot change; if that unchanged request is no longer eligible, stop rather than silently retarget it. No old decision or observation is spliced into the replacement; no earlier evaluation is consumed or misreported as the final decision.
- Use PR #31's independently permitted UNAVAILABLE/WITHHELD limited reply, rebuilding and re-covering that entire payload before sealing. A failed authorization/currentness guard cannot be rescued merely by changing the history field.
- If payload or evidence is already sealed, suppress this attempt. Do not edit the buffer, receipt, decision or history label, and do not let the classifier append an “explanation” commit. A new protected reply requires a separately requested new read with new identity and full checks.

This is an owner refresh/stop rule, not permission for the classifier to rerun a command, write qualification history or hold a history-wide lock through delivery. Genuinely unlearned post-cut events are outside the observation; the public time remains c, never a claim of later completeness. A source that cannot support the required complete cut cannot claim readiness by returning UNAVAILABLE forever.

PR #31's history object remains exactly availability, asOf and disputeStatus. AVAILABLE requires the verified six-label determination and actual observation time. UNAVAILABLE and WITHHELD have both other fields null; WITHHELD takes precedence whenever status or time is not disclosable. Use the approved safe sentences, original outcome/time, recorded-not-current labeling and trace posture unchanged. Internal counts, source IDs, diagnostics and admission failures do not become public fields.

A missing/unadmitted producer or broken binding is a readiness/interface failure, distinct from a valid bound producer's temporary inability. An independently permitted limited response may handle either safely but does not certify the missing producer. If the original result itself cannot be verified or read, no history fallback creates existence disclosure.

For C38 pairs with equivalent readable originals and differing only in hidden history, choose limited reply versus exclusion from the same independently selected reader/scope/record-class policy. Hidden label, candidate count or observation success cannot change response category, text, references, hints, omission pattern or fallback choice. The same coverage/egress guard applies to safe projections, headers, denial paths and caches.

Fresh-refusal command replies remain with their command transaction owners plus PR #35/#31. This historical-read protocol does not close that separate HSP-BIND03 path.

## 9. Evidence ownership and truthful receipts

### 9.1 Proposed package placement

Use PR #11 §17.2's existing four package families. The names in this table are proposed tagged profiles, not materialized schema IDs or runtime bindings. Read evidence entering authority remains append-only `EvidenceEvent` / `evidence record`, never domain current state, a qualifier act or filing-delivery truth. The classifier creates no durable status record.

| Evidence element | Semantic owner / proposed package | Truth claim and membership | Failure rule |
|---|---|---|---|
| Attempt admission A | This protocol / AuthorizationFinalizationEvidence v0.2 read-attempt profile | One logical request and live attempt admitted; separately durable before preparation, not part of C's success claim | No authoritative acknowledgement, no continuing attempt |
| Request/result/full trace | PR #11 / AuthorizationDecisionEvidence v0.2 | Exact original evaluation and selected path; complete bundle is in C | Apply applicable decision-bundle persistence failure; never fabricate DENY or success |
| Pre-evaluation qualification and final gate/CP2 proof | Evidence/Platform owners; references in decision/read evidence | Genuine inputs with their original times, plus later actual gate results; required immutable bindings are in C | Missing required proof blocks preparation/commit; no invented envelope |
| Single-use consumption | PR #11 semantics, this read ordering / AuthorizationFinalizationEvidence v0.2 | One decision consumed for this exact read transaction, intent and prepared payload; in C | Uniqueness and complete atomic membership required; no second consumption |
| Governed-read preparation receipt | This protocol / AuthorizationFinalizationEvidence v0.2 | Preparation completed, exact buffer/evidence ready at C; no disclosure yet asserted; in C | Incomplete or uncertain set permits no L |
| Coverage manifest | This protocol with source/authority/redaction owner witnesses / referenced read-evidence profile in AuthorizationFinalizationEvidence v0.2 | Every final item/location and origin accounted for under the selected path and S; in C | Incomplete coverage prevents disclosure; digest alone cannot prove it |
| Payload digest, serializer/media/policy bindings | This protocol / preparation receipt | Exact immutable buffered application bytes intended for the one handoff; in C | Any post-hash change invalidates the attempt |
| Retained payload ref/bytes and custody/schedule bindings, when required | PR #29 / referenced by preparation receipt | Exact bytes already verifiably retained under the promised policy; required membership/reference activation in C | Future upload, missing bytes or incompatible policy prevents C/L |
| Read outcome observation | This protocol / AuthorizationFinalizationEvidence v0.2 linked read-outcome profile | A stop before L or an actually observed handoff/completion/failure, with precise time/proof limits; after the event, not in C | Missing record leaves outcome unknown; never fill it from intention or receipt presence |
| Source-history transcript | PR #35 / its derived internal decision-evidence profile | Complete verified as-of determination and invocation-bound proof, or valid inability; relevant retained evidence bindings in C | No separate history receipt/writer; incomplete required proof cannot become NONE |

### 9.2 Exact preparation set

After successful authorization and all applicable gates, freeze the final CP2 projection and exact serialized payload. Bind the preparation receipt to A, tenant/principal/session, selected read transaction and S/c, target and every contributing origin revision, conditional query/plan/parameters, intent/derived view, selected path, policy/rule/manifest, all guards and deadlines, qualification/gate/coverage proofs, serializer/media/serialization policy and payload digest, retention policy/posture/schedule and exact retained ref when applicable.

The complete atomic set C is exactly the decision bundle, successful single-use consumption, preparation receipt, coverage manifest, payload digest/bindings and required retained payload evidence. Referenced immutable proof objects must already exist and verify under the selected retention/commit contract; a dangling or future ref is not membership. Atomic activation of a previously staged content-addressed blob may satisfy the byte component only if the selected storage/custody owner proves its durability, immutability, permitted access and required retention before C. This does not assume a distributed transaction or make an unverified blob acknowledgement sufficient.

Authoritative commit proof must identify the whole set, its unique attempt/decision membership and atomic outcome. It is obtained from the transaction owner, not a success flag inside the candidate receipt. Store constraints must prohibit another consumption or preparation success set for the same attempt/decision. A fragment is an integrity breach, not a smaller valid success set.

Avoid digest cycles: payload bytes do not contain their own digest or preparation-receipt digest. Preassigned immutable IDs may connect records; external content digests cover the exact declared projections. The decision bundle retains PR #11 §18.8's exact two JSON-pointer exclusions, not a generic exclusion by field name. Coverage/transcript hashes cover their complete canonical bytes externally with no self-hash field. Later outcome records reference the already final receipt digest; the earlier immutable receipt is not backfilled with their digest. Future schemas must make every projection and reference edge exact.

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
| S — observation | Obtain the one governed view, real pre-evaluation qualification and complete source/authority inputs; evaluate current authorization |
| P — preparation | Verify remaining gates, history, coverage and retention; finalize CP2 and freeze/hash exact buffer; construct/validate complete evidence |
| C — atomic evidence commit | With valid guards and time, commit the full §9.2 set and single-use consumption; obtain conclusive authoritative acknowledgement. Still no disclosure assertion |
| L — one disclosure linearization point | In the same original live invocation, atomically validate/consume the non-transferable handoff capability under the guards and deadline, and irrevocably hand the exact buffer to the bound protected-output boundary |
| O — observed outcome | Append only supported stop/attempt/acceptance/failure evidence. Delivery beyond that boundary is not inferred |

L is the first irreversible handoff at which any protected bytes from this buffer may become available outside the protected read owner. If a proxy, middleware queue, cache or logger can expose them earlier, that is the real boundary and it must be guarded as L. A mere “send scheduled” call that leaves an unguarded queue to decide later is insufficient. The actual egress binding must name the boundary and enforce at most one handoff, no handler/proxy retry or replay cache, and no mutation of the bound application payload. Ordinary network packetization of an already complete buffer is not permission for incremental protected-result production.

At L, all of these must hold together:

1. A's original sole live owner, exact invocation/session and read-transaction identity remain valid; no cancellation, owner-loss or prior handoff has consumed/fenced the capability.
2. C has been conclusively acknowledged with complete exact membership; no partial set, pending commit or unresolved storage integrity is present.
3. Trusted time is strictly before decisionValidUntil and the fixed read deadline. Relevant authority, currentness, sovereignty, retention, policy and byte-availability guards cover through L under §6.1.
4. The final buffer and all receipt/coverage/serializer bindings remain exact, and the history reply has not been invalidated under §8.
5. The bound egress can accept the one immutable buffer under its reviewed semantics, with no alternative unguarded response path.

Failure of any condition irrevocably suppresses this attempt; no protected bytes may cross L. A committed consumption remains spent even when L never occurs. Record that distinction truthfully. If L has already occurred, cancellation or later revocation cannot unsend bytes; do not claim zero disclosure. This protocol creates no later independent dispatch or filing transport attempt: `NO_EXTERNAL_DISPATCH` is unchanged, and #13/PR #11 §18.6 filing transport semantics are outside scope.

## 11. Failure, uncertain commitment and retry

Evidence commitment and disclosure are separate axes. Internal reconciliation distinguishes `EVIDENCE_COMMITTED`, `EVIDENCE_NOT_COMMITTED`, `EVIDENCE_COMMIT_UNKNOWN` and `EVIDENCE_INTEGRITY_BREACH`. Disclosure remains not attempted, observed attempted or unknown according to actual evidence, with any supported acceptance extent separately stated. These are runtime facts, not additions to the authorization lattice.

| Failure or race | Required behavior |
|---|---|
| Invalid ingress or missing trusted admission context | Zero protected bytes; no fabricated authorization bundle. Existing rejection/audit rules only |
| Non-ALLOW evaluation | No consumption or protected payload. Persist the valid refusal bundle through PR #11's existing non-ALLOW protocol; use only the approved safe response |
| Qualification/coverage/retention failure before C | Stop, discard uncommitted payload under its policy, retain only truthfully owned failure evidence. A valid earlier ALLOW is not changed to DENY |
| Cancellation or exclusive cutoff reached before C | No C success set/consumption; fence the live attempt; no L |
| Relevant guard invalidation before C | Abort/rebuild the whole unsealed read where §8 permits, otherwise stop. Never retain a stale decision or buffer as the winning attempt |
| Definitive C rollback/persistence failure | Zero protected bytes. `READ_EVIDENCE_PERSISTENCE_FAILED` or the applicable decision-bundle failure is a runtime/integrity disposition with no authorization reason rank |
| C acknowledgement lost or commit result uncertain | Immediately fence further handoff. Zero protected bytes from this attempt; preserve uncertainty and reconcile with the authoritative transaction owner. A later discovered complete C does not reopen L |
| Partial C set or conflicting immutable/consumption evidence | Integrity breach; suppress disclosure, quarantine this attempt's execution and report through an already authorized incident path. Do not fill missing members, delete fragments, grant repair powers or call it NO_EFFECT |
| Expiry, cancellation, guard invalidation or known new history after C but before L | Consumption stays spent; fence L; append a proved stop if possible. No finalized evidence rewrite, rollback fiction or automatic retry |
| Crash before C | No protected handoff; resolve any admission/commit uncertainty from owner evidence. A surviving admission tuple cannot be taken over |
| Crash after C but before or around L | No replay/takeover. Commit may be established independently; a receipt alone cannot establish whether L occurred. Record disclosure uncertainty unless independent exact egress/stop evidence resolves it |
| Disconnect known before L | Fence and stop; no L. Mere absence of a client acknowledgement is not proof that no earlier handoff occurred |
| Disconnect, expiry or crash after L | Preserve the attempt fact and any known acceptance extent; delivery may be partial/unknown. No rollback of consumption and no promise of zero bytes |
| Outcome-observation persistence failure after L | Never report overall zero disclosure or undo C. Preserve/reconcile independently available observation evidence; otherwise outcome is unknown. No second handoff to repair audit evidence |
| Required retained payload later unavailable | Preserve original posture/receipt/observed facts; report current reconstruction limits and retention failure under PR #29. Missing bytes cannot be silently replaced |

Reconciliation uses authoritative exact admission/transaction membership/uniqueness evidence and the bound egress observation source, with the same tenant/principal/intent identity and verified original contracts. A missing lookup row, stale replica, timeout or absence of O is not conclusive rollback or non-disclosure. Full matching C proves evidence commitment only. A STOPPED_BEFORE_DISCLOSURE claim additionally needs the irreversible sole-owner fence and proof that L was never crossed. If the actual provider cannot establish one of these, keep that axis unknown.

There is no same-identity protected response retry in v0.1. An exact duplicate may receive only its independently authorized non-protected status/qualification projection; it cannot return the old buffer, receipt internals or trace. A changed request/session/profile does not start another lifecycle under that tuple. A separately requested new read uses a new request identifier, fresh current authority and a newly constructed evidence/coverage set, even for identical content. No old ALLOW, consumption, history result or retained bytes confer authority on it.

Keep the immutable admission identity and required reconciliation/tombstone evidence under PR #29's compatible schedule so expiry or cleanup cannot make the tuple appear unused. If that retention cannot coexist with policy limits, reject new admission under the conflicting profile. This read identity discipline does not amend PR #26's retryable no-effect operations.

## 12. Retention and public-path stops

Resolve the immutable evidence-retention policy independently at S, with purpose, tenant, sovereignty and evidence-class constraints. Bind the exact schedule and its pending/terminal event semantics; if a terminal event is unknown, do not invent a completed schedule. Guard policy and required byte availability through C/L.

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
| RD-I02 | One complete governed view and actual positive/negative/set-valued source proof; relevant guards and exclusive time bounds cover C through L |
| RD-I03 | Genuine eligible pre-evaluation qualification; no future-fact cycle, dummy evidence or reference-as-proof |
| RD-I04 | One exact target/form and independently sufficient selected path; no cross-path/layer union or hidden target narrowing |
| RD-I05 | Complete information/origin coverage, including legitimate artifact contents and inference-sensitive metadata/counts |
| RD-I06 | Exact immutable buffer/serializer and full atomic decision/consumption/receipt/coverage/payload set before L |
| RD-I07 | Preparation, one possible disclosure attempt, acceptance extent and delivery are distinct truthful facts |
| RD-I08 | No stale handoff, lost-owner takeover, protected replay, duplicate consumption or guessed reconciliation |
| RD-I09 | PR #35 complete same-context history, original admission and known-candidate refresh; no finalized rewrite |
| RD-I10 | PR #31 nulls/withholding/safe messages/C38; safe fallback does not prove producer readiness |
| RD-I11 | PR #29 pre-disclosure eligibility and truthful retention/reconstruction limits |
| RD-I12 | Exact binding, owner and stage separation; no approval, currentness or runtime claim from this draft |

| Case | Required observation and expected result | Invariants |
|---|---|---|
| RD-C01 Direct read, including separately permitted AUTHORIZATION_TRACE | Exact target and permitted projection, no invented query inputs; full positive C/L path. Full trace bytes cannot piggyback on another result | I01–I08, I10 |
| RD-C02 Query read | Exactly one specification and plan as integrity inputs; complete result/origin membership, correct parameters and positive C/L path. Missing/extra query input fails | I02–I06 |
| RD-C03 SharingGrant aggregate | §7.3's D/O1/O2 positive content mapping without independent raw-origin grants; negative twins for raw expansion, private annex, forbidden cross-farm input, wrong revision and incomplete origin enumeration | I04–I06 |
| RD-C04 Direct versus delegated versus sharing basis | Each applicable complete path succeeds independently in the one policy decision; partial action/purpose/evidence paths never combine. Post-evaluation path substitution fails | I04–I05 |
| RD-C05 Historical complete empty history | Independently exhaustive original-source enumeration yields AVAILABLE/NONE at actual c, not hard-coded empty success; original result remains unchanged | I02, I09–I10 |
| RD-C06 Older valid qualifier, current writer excluded | Verify original admitted package/rule/source/commit proof and complete history. No current write authority inferred; absence of old proof stays unresolved | I02, I09, I12 |
| RD-C07 Mixed snapshots or incomplete membership | Missing page/partition, hidden row, stale index, unsupported historical version or unresolved candidate identity prevents complete classification; independently permitted limited handling only | I02, I09–I10 |
| RD-C08 Known post-cut committed candidate | Inject before sealing and after C, including unresolved admission/label. First rebuilds whole read or permitted limited payload; second suppresses old attempt. No label-only patch | I02, I08–I10 |
| RD-C09 Authority/guard/time invalidation | Race revocation, session/policy/resource expiry and retained-byte loss around C/L. Exact-cutoff equality fails. Change ordered before L prevents handoff; post-L cannot unsend | I02, I07–I08, I11 |
| RD-C10 Uncovered information | Inject aggregate, count, metadata, lineage, link, header or error detail outside coverage. Redact/recompute only under policy or stop; no alternate path/cache leak | I05–I06, I10 |
| RD-C11 Forged or circular qualification/context | Mixed tenant/session/attempt/cut, caller policy, fake proof and missing real qualification fail; a policy-derived real evidence reference is accepted without a redundant carrier | I01–I03 |
| RD-C12 Persistence and uncertain commitment | Definite rollback, lost C acknowledgement, stale status and partial set: zero pre-L bytes, separate runtime failure/uncertainty, no fabricated DENY, no second consumption or repair-by-replay | I06–I08 |
| RD-C13 Crash/disconnect/retry | Fault immediately before/after C, L and O; preparation receipt never proves delivery. Same tuple cannot take over or emit old buffer; fresh requested read needs new current decision | I01, I06–I08 |
| RD-C14 Three retention stops | Missing policy, prohibited transient buffer, incompatible immutable proof retention: no protected bytes, truthful ineligibility/conflict, no weakened posture | I11 |
| RD-C15 Proof posture and later loss | Positive RETAINED_BYTES and DIGEST_ONLY paths, later permitted deletion/unexpected loss/candidate comparison. Preserve original posture; never invent reconstruction, origin or delivery | I06–I07, I11 |
| RD-C16 C38 hidden-history pairs | For each independently allowed limited/excluded policy path, vary only hidden history, including NONE/disputed/unavailable. Public category/text/hints/refs/omissions remain indistinguishable | I09–I10 |
| RD-C17 Concurrent duplicate admission | Same tuple/different handlers or sessions yields one live owner; differing caller facts conflict. Lost A acknowledgement yields no continuing protected attempt | I01, I08 |
| RD-C18 Boundary and payload bypass | Proxy queue retry, middleware auto-send, altered serializer, buffer mutation, embedded self-digest or forged commit flag fails. Genuine one-buffer handoff remains positive | I06–I08 |
| RD-C19 Full selected closure | Cover all ten scope and twenty record/artifact target alternatives with their applicable paths; reject unselected actions. No fixture silently makes a selected branch permanently unavailable | I04, I12 |

### 13.1 Issue acceptance traceability

| Issue #36 criterion | Protocol sections | Invariants / cases |
|---|---|---|
| 1 — trusted attempt and selection | 4–5 | I01–I02; C11, C17 |
| 2 — one view and real guards | 6, 8, 10 | I02, I09; C05–C09, C18 |
| 3 — pre-evaluation qualification | 6.2 | I03; C11 |
| 4 — coverage, direct/query and sharing | 4, 7 | I04–I05; C01–C04, C10, C19 |
| 5 — atomic evidence and ownership | 9–10 | I06–I07; C12–C13, C18 |
| 6 — failure, expiry, uncertain commit and retry | 10–11; compatibility §3.2 | I07–I08; C09, C12–C13, C17–C18 |
| 7 — historical source observation/reply | 8 | I09; C05–C08 |
| 8 — public privacy and retention stops | 8, 12 | I10–I11; C14–C16 |
| 9 — explicit invariants and positive/hostile coverage | 7.3, 13 | I01–I12; C01–C19 |
| 10 — exact later bindings and stages | 3, 14–15 | I12; C19 |

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
| RD-BIND03 — transaction/observation/egress | Named authoritative collections/providers, consistent cut/time mapping and visibility/exhaustion proofs; currentness/negative/set guards with all participating mutation paths; admission/success uniqueness; atomic C and authoritative reconciliation; actual C-to-L protection, owner-loss fencing and one-handoff egress observation contract | Source/storage/read transaction owners; no isolation, role or lock chosen here; open |
| RD-BIND04 — full target/content coverage | Exact source/assembly/live-view content and origin-membership contracts for all selected targets; applicable direct/delegated/sharing coverage, redaction/inference proofs and conditional query/plan binding, including §7.3's positive case | Existing source/artifact and authorization owners with read coverage verifier; open. New content permission needs separate owner approval |
| RD-BIND05 — history producer/consumer | HSP-BIND01–04's exact profile, historical inventory/original admission, complete same-S observation, invocation verifier, reply-validity and PR #31 projection; QG original source dependencies preserved | #32/#33/#30 with read owner; historical path only here, fresh-command reply separate; open |
| RD-BIND06 — retention/public safety | Exact PR #29 policy/schedule/custody capability, mandatory immutable proof minimization, post-outcome uncertainty handling, safe lookup/status and C38 policy/verifier bindings | #14/#30 and storage/custody owners; no new grants or public codes; open |
| RD-BIND07 — selected conformance | Production-reachable positive/negative assets for C01–C19 and the full selected read scope, real concurrency/fault/byte-observation harness, exact versions and results | Canonical hostile conformance then separately scoped OFARM2 runtime verification; open |

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

Version: 1. Status: **proposed; not approved**. Exact reviewed head must be recorded externally after publication; a self-referential commit hash is not embedded in the candidate.

The approval covers §§1 and 4–12's read semantics, including the artifact-content interpretation, one-live-attempt/no-protected-replay choice, preparation/outcome separation, C-to-L guard requirement, uncertainty and refresh behavior. It would not certify the missing bindings in §14 or grant another owner's authority. Review must challenge those choices as a coherent positive protocol, not merely count references to requirements.

Draft verification on 2026-09-14: all seven live owner heads and both main refs matched the recorded pins; the reviewed issue body was unchanged. Static checks found all ten issue criteria, twelve named invariants and nineteen case rows, balanced fences/table columns and the required Markdown spacing. `validate_repo_hygiene.py`, `check_generated_currentness.py`, `check_repository_cross_references.py` and `check_repository_steward_guardrails.py` passed without generated-file changes. These are document/repository checks only, not independent protocol review. No database, concurrency, delivery, privacy or production-readiness result is claimed by the worked cases.

Scope stayed within **governed-read transaction integrity and protected disclosure**; adjacent candidate bytes, runtime and active authority are unchanged.

What is next: exact-head review of this proposal, then explicit semantic approval or a bounded revision. Keep every actual binding, acceptance, conformance, promotion, extraction and implementation gate open until its own work is authorized and verified.
