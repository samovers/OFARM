# OFARM Authorization Evidence Retention and Proof Strength v0.1

Date: 2026-09-07

Status: non-authoritative Phase A candidate; review and semantic approval pending

Issue: [samovers/OFARM#14](https://github.com/samovers/OFARM/issues/14); authorization parent [#10](https://github.com/samovers/OFARM/issues/10)

Inspected canonical main: `71ca724a8b6ec23f1655b086a6f549496d10a47f`

Downstream: [OFARM2#353](https://github.com/samovers/OFARM2/issues/353) / [draft PR #359](https://github.com/samovers/OFARM2/pull/359); this candidate alone does not unblock implementation.

## 1. Decision requested

Approve or amend these proposed retention and evidence claims, not a storage implementation:

1. Use one separately governed, immutable `AuthorizationEvidenceRetentionPolicy v0.1` family for exact approval-display and governed-read payload bytes. Do not stretch the current agent-trace retention schema into this different contract.
2. Keep the original receipt and its selected proof posture immutable. Report current byte availability and integrity separately, with an observation time and evidence for the claim.
3. Fresh human approval requires retained exact display bytes and the complete renderer/display bindings. It cannot fall back to digest-only approval. Direct human action and `NOT_REQUIRED` do not gain a synthetic approval challenge.
4. Governed reads retain PR #11's two postures, `RETAINED_BYTES` and `DIGEST_ONLY`. The latter supports comparison with independently supplied candidate bytes, not reconstruction from a digest or a claim that retained bytes exist.
5. Require explicit retention clocks, compatible minimum and maximum constraints, encryption and custody profiles, and governed deletion/redaction rules. Neither an arbitrary default duration nor a privacy-conflicting retention promise is admissible.
6. Governed deletion concerns separately stored content only where the governing obligations permit it. It cannot rewrite immutable receipts, policy bindings, disclosure history, or the evidence needed for safe retry, reconciliation and conflict detection.
7. Record later availability, redaction and deletion evidence through a bounded support profile in the already proposed authorization evidence package, subject to carrier/classification review. Do not invent a new event family, operation ledger, deletion authority, or public error registry.

These are choices for review. This file creates no accepted law, current/default contract, approval record, merge authority, provider capability, or runtime readiness.

## 2. Primary trust boundary and intended PR boundary

The primary trust boundary is **authorization evidence retention and custody / proof strength**: what exact bytes must be kept, under which policy, and what the surviving evidence can truthfully establish.

The intended PR changes only this candidate file in the historical phase-report lane. It does not change active baseline files, accepted RFCs, companion policies, schemas, indexes, another candidate PR, or OFARM2 code.

| Responsibility | Owner | Limit here |
|---|---|---|
| Evidence retention duration, permitted byte handling, custody requirements and proof limits | Issue #14, this candidate | Define policy requirements and evidence semantics only |
| Authorization outcomes, eligibility, grants, purpose/sovereignty checks and safe response projection | Active authority law and pinned PR #11 | Retention does not grant access, select an authority path, or rewrite a decision |
| Approval challenge, human act, finalization, guards, single use, retry and reconciliation | Pinned PR #20; PR #26 for `NOT_REQUIRED` | Consume their obligations; no new transaction, cancellation or repair protocol |
| Protected-effect result, domain history and promotion | Each separately governed domain contract and active Event Grammar | No deletion of domain truth or automatic promotion from custody evidence |
| Governed-read release and external transport | PR #11 section 18.5 and separate issue #13 | No new disclosure point, streaming support, delivery guarantee or receiver acknowledgement |
| Storage, encryption operations, key issuance/rotation and custodian implementation | Later separately authorized implementation boundaries | No provider, algorithm suite, database role, migration, worker or key operation selected here |
| Acceptance, conformance, currentness and OFARM2 extraction | PR #11 section 24 and issue #21 | No gate passes merely because this candidate exists or receives Phase A approval |

If closure requires changing another owner's semantics, stop before editing that boundary and propose a linked prerequisite or follow-up. A later implementation must likewise declare its own single primary trust boundary.

## 3. Governing sources and exact dependency pins

Apply `PROJECT_AUTHORITY.md`: active baseline outranks accepted RFCs, then companion artifacts, then machine contracts. The draft candidates below are planning dependencies, not accepted law. Active file references in this section are pinned to the inspected canonical main above.

| Source | Constraint used here |
|---|---|
| `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`, sections 7.8, 7.15-7.17 and 10 | Explicit authority, farm sovereignty, prospective revocation, immutable history and preserved evidence/provenance |
| `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`, sections 14.11, 14.14 and 14.15 | Revocation cannot erase history; durable evidence basis and authorization trace remain required |
| `02_accepted_rfcs/OFARM_Performance_and_Explainable_Current_State_Evidence_RFC_v0_1.md`, section 9 | Tier-2 reconstruction and applicable Tier-3 retention obligations remain independent; compact hashes are not a waiver |
| `02_accepted_rfcs/OFARM_AI_Facing_Result_Qualification_and_Trace_Surface_RFC_v0_1.md`, sections 2, 4 and 7 | Qualify missing, denied and redacted evidence honestly; public codes belong to the existing CP2 process |
| `01_companion_artifacts/OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md`, sections 6-10 | Purpose-limited sharing, separately governed authority and prospective revocation |
| `01_companion_artifacts/OFARM_Evidence_Sufficiency_and_Attestation_Policy_v0_1.md`, sections 2 and 6 | Raw/linked original, normalized interpretation and provenance; a frozen output reference alone is not complete evidence |
| `01_companion_artifacts/OFARM_Agent_Tool_Manifest_and_Capability_Honesty_Policy_v0_1.md` | Retention promises must be runtime-verifiable; descriptions and schema checks do not prove operational custody |
| `01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`, sections 3.6, 6.6, 8 and 10 | Supporting evidentiary statements fit `EvidenceEvent` / `evidence record`; they do not create hard truth or new authority |
| [PR #11](https://github.com/samovers/OFARM/pull/11), head `03a21f669ee04f96d444e14f00ae7212cab04803` | Sections 16, 17.2, 18.3, 18.5 and 24: policy-byte availability, existing evidence package, exact displays/payloads, immutable receipts and delivery stages |
| [PR #20](https://github.com/samovers/OFARM/pull/20), head `98f8c4fafbae42c8f7fd931f43f53adcb4733713` | Sections 6.2, 8, 11, 17 and 18: display lifecycle, no unsafe forgetting, and separately owned retention/custody policy |
| [PR #26](https://github.com/samovers/OFARM/pull/26), head `e042efa2911b2ef0a61603b8e0adaa6911c03ac0` | Sections 12 and 14.2: no synthetic approval, no loss of required retry/reconciliation inputs, and no reusable operation tuple after bulk expiry |

The three pinned candidates are respectively `authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md`, `governed_human_approval_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`, and `not_required_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`, all under `package_meta/history/clean_baseline_migration/phase_reports/` at their stated commits. They are not copied into this PR. A changed dependency head requires inspection and renewed binding review, not an automatic switch to “latest”.

## 4. Existing contract inventory and smallest extension

The current/default status of the following schemas was checked through both `03_machine_contracts/CONTRACT_INDEX.json` and `03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json`, not inferred from filenames.

| Current contract | Existing capability | Remaining gap |
|---|---|---|
| `03_machine_contracts/schemas/agent_manifest/OFARM_AgentTraceRetentionPolicy_schema_v0_1.json` | Minimum trace-retention class, required trace events, blocked-action trace and runtime-verifiable promises | No exact approval/payload binding, retention clock, proof posture, deletion evidence or encryption/custody requirements |
| `03_machine_contracts/schemas/agent_manifest/OFARM_RedactionAndPermissionLimitedResultPolicy_schema_v0_1.json` | Qualified permission-limited results, non-leaking redaction, share-policy recheck posture and response behavior | No storage-retention horizon, original-byte proof, or governed erasure evidence |
| `03_machine_contracts/schemas/authority/OFARM_DataSovereigntyBoundary_schema_v0_1.json` | Owning authority, scope, effective interval, sharing/intelligence posture and stronger-rule refs | Not a byte-retention schedule or custody implementation contract |
| Accepted evidence-sufficiency and trace rules | Retain or regenerate the appropriate evidence basis for consequential use | Do not specify exact approval-display or serialized-disclosure custody |
| Pinned PR #11 | Exact display/read bindings and `RETAINED_BYTES` / `DIGEST_ONLY` semantics | Deliberately delegates duration, encryption, deletion/redaction and custody to #14 |

Raw-file SHA-256 values for the three current schemas, in table order:

- `aed069d355f74c3379e35f27cadbfc9700166123f017f33da791a651bac179d7`
- `95dbda4e9a9ad192667af1ca12303d9bc9ea2d4304a0c8c39f82eb097ab2dafe`
- `197f171d3eb21fe9b954556e8c02c3b1a4e57721ee074ae801e0ec234937f858`

The minimum proposed extension is one dedicated policy family, consumed through the already required policy ref/digest in approval and read evidence, plus one bounded later-disposition support profile. Existing agent-trace classes stay unchanged and continue to apply where selected. In particular, `EPHEMERAL_DEBUG_ONLY` cannot authorize ephemeral approval evidence or waive a consequential trace obligation.

## 5. Separate the historical promise from present proof

An immutable evidence record states what was bound at the owning operation. A later observation states what an authorized verifier could establish at a particular time. Neither replaces the other.

| Available evidence at verification time | Truthful claim | Forbidden claim |
|---|---|---|
| Exact retained original bytes retrieved and checked against the bound digest, with the required identity/media/profile bindings verified | These original bound bytes are byte-reconstructible at this observation time | The human understood or assented, the action was authorized, or the recipient received them, solely because the bytes exist |
| `DIGEST_ONLY` receipt plus independently supplied candidate bytes checked under the original digest profile | These candidate bytes match, or do not match, the recorded digest | OFARM reconstructed the payload from the receipt, retained it, or independently proved its provenance |
| Digest only, with no candidate bytes available | The record preserves a digest commitment | A byte comparison has passed or the original content can be recovered from the digest |
| Originally retained bytes now deleted, inaccessible through lost keys, or unavailable | Original retention posture remains historical; present reconstruction is not established | Rewrite the original posture to `DIGEST_ONLY`, hide the loss, or fabricate replacement bytes |
| Retrieval forbidden to this requester | This requester is not permitted to inspect the bytes; use a safe qualified response | The bytes do not exist, were deleted, or are available to no authorized verifier |
| Redacted derivative or newly rendered/serialized content only | A separately identified derivative or new output exists | It is the original display or payload, even if its meaning appears equivalent |
| Retrieved bytes or binding metadata fail integrity checks | Integrity mismatch for the specific verified object/binding | Successful reconstruction, an in-place repair, or a silently updated digest |

“Byte-reconstructible” means retrieval of the exact captured byte sequence with matching digest and bound format/profile identity. It does not promise a working historical renderer, a pixel-identical browser environment, or reconstruction of the entire authorization decision from payload bytes alone. Those stronger claims require their own retained dependencies and evidence. A missing policy or provenance dependency must be reported even when the content bytes themselves match.

An availability observation is not a permanent certificate. Its scope, trusted observation time, verifier identity, digest profile, retrieval/integrity evidence, and limitations must accompany the claim. A failed retrieval is not proof of deletion. A digest is neither encryption nor anonymization; even identifiers and hashes may expose sensitive facts or enable guessing.

## 6. Separately governed retention policy

### 6.1 Required policy content

`AuthorizationEvidenceRetentionPolicy v0.1` is a proposed family, not an existing schema or an executable profile. Its later closed schema must require these semantic groups:

| Group | Required meaning |
|---|---|
| Immutable identity | Policy ID, version and digest-profile binding; consuming evidence addresses the finalized policy by exact content ref/digest, and those bytes remain retrievable under their applicable evidence obligations |
| Governance basis | Issuing/accountable authority and exact admission/governance basis refs; scope and effective interval; no self-asserted authority merely because a document hashes correctly |
| Applicability | Tenant/twin, sovereignty boundary, purpose, applicable data and evidence classes, recipient/use restrictions where relevant, and stronger governing constraints |
| Evidence-specific posture | Approval-display retention is mandatory; governed-read payload posture is exactly `RETAINED_BYTES` or `DIGEST_ONLY` as selected by the trusted policy |
| Time and obligations | Trusted clock and start-event basis, explicit duration/cutoff rules, minimum required retention, maximum permitted retention or explicit governed absence of a cap, and applicable holds/retry/reconciliation obligations |
| Permitted handling | Whether exact bulk bytes may be retained; separate treatment of immutable proof metadata, transient buffers, originals, derivatives, replicas, backups and indexes |
| Encryption and custody | Exact approved encryption and custody profile refs/digests; responsible custody boundary; access/decryption purpose; key-availability, recovery, compromise and erasure-evidence requirements |
| Disposition | Conditions and independently authorized basis for deletion/redaction, required copy-scope evidence, and the safe proof/availability claim after completion, partial failure or uncertainty |
| Conformance | Evidence required to substantiate the selected promise, including retrieval/integrity checks and the later disposition record; no silent optional downgrade |

Policy parameters are governed data. This candidate selects no universal number of days, legal retention schedule, encryption algorithm, storage provider or key custodian. Actual policy instances must contain explicit values and exact approved profiles before use; generic prose, unresolved refs and placeholder digests cannot pass binding review.

The consuming ref/digest is assigned over finalized policy bytes under the bound digest profile. The policy does not embed its own full-byte digest or a future receipt/disposition digest. This avoids a self-referential construction requirement.

### 6.2 Selection and binding

The trusted policy owner resolves the applicable admitted immutable policy using the owning operation's snapshot and complete purpose, tenant, sovereignty, evidence-class and data constraints. The caller cannot supply a more permissive policy, a “do not log” flag, an alternate digest, or a weaker payload posture.

The operation evidence binds that policy's ID/version/ref/digest, the selected evidence class and posture, the exact scope/governance inputs, and the resolved retention schedule or its immutable evidence ref/digest. These facts are incorporated into the existing owner-defined approval or read evidence, not a parallel decision ledger.

The owning protocol guards relevant policy and byte-availability facts through its existing commit boundary. This candidate adds no new transaction or source of trusted time. Policy resolution, integrity or capability failure prevents the use from claiming conforming evidence; the owner applies its existing fail-closed behavior. Do not turn a custody failure into an invented authorization outcome or new public reason code.

Changed policy creates a new immutable policy version. It cannot rewrite a historical policy binding, claimed posture, receipt or disclosure time. Current stronger restrictions may constrain later access or disposition, but require their own exact governed basis and linked evidence. “Use the latest policy” is not sufficient authority to erase an earlier obligation.

## 7. Approval-display profile

For `FRESH_HUMAN_APPROVAL_REQUIRED`, retain the actual immutable human-visible representation for the intended natural person before the challenge is persisted, as PR #11 and PR #20 require. Bind:

- content-addressed `humanVisibleRepresentationRef` and exact byte digest;
- media type;
- renderer identifier, version and digest;
- display-policy ref/digest;
- locale and timezone;
- selected retention-policy ID/version/ref/digest and the applicable schedule binding; and
- the existing challenge, effect-intent, intended-person and later explicit-act bindings owned by those protocols.

The digest covers the captured representation bytes, not an encrypted storage envelope or a fresh render of current data. Every component needed to constitute that representation must be in the immutable captured byte set under the display owner's contract; a mutable external asset is not captured evidence. If that contract cannot identify the complete representation, stop for its owner rather than inventing a new display format here.

Retain enough dependencies to verify the exact media/renderer/display-policy identity; never claim semantic or visual reproduction from a current renderer substituted for the bound version. Byte reconstruction and runnable historical rendering are distinct claims.

The original display must remain retrievable over the required approval-evidence period and while the owning challenge, finalization, retry or reconciliation obligation requires it. Missing, changed, digest-invalid or policy-incompatible bytes/metadata before finalization cannot be replaced by a digest-only approval. The owning protocol's existing non-`ALLOW` and lifecycle rules apply; retention work does not issue a new challenge or revive an old act.

A later permitted deletion leaves the challenge, approval, person/intent bindings, original display digest, metadata and policy identity intact, with separately recorded present proof limits. It does not retroactively erase a valid historical act or authorize another consumption. Unexpected loss is a retention conformance failure, not a silent downgrade.

`DIRECT_HUMAN_ACTION_REQUIRED` and `NOT_REQUIRED` retain their owning act/transaction evidence. This profile does not create a separate human display, approval or challenge requirement for those modes, nor weaken any domain-owned assertion-act evidence.

## 8. Governed-read payload profile

The governed-read receipt continues to bind the exact buffered payload disclosed by PR #11's protocol, including:

- payload digest and media type;
- serializer identifier, version and digest;
- serialization-policy ref/digest;
- selected `payloadEvidencePosture`;
- retention-policy ID/version/ref/digest and applicable schedule binding; and
- for `RETAINED_BYTES`, the content-addressed exact payload ref.

The existing target/origin revisions, query/plan, coverage, redaction, CP2 qualification, authority, decision-consumption and completion/failure bindings remain required. This list supplements rather than replaces them. The original disclosure time and historical disclosure fact remain owned by the read protocol.

With `RETAINED_BYTES`, the exact staged payload and required bindings must satisfy the retention promise before the owner's atomic evidence commit and single disclosure point. A pointer to absent bytes, a future upload promise or an unverified storage acknowledgement is insufficient. Encryption does not change which plaintext/application-payload bytes the receipt digest denotes.

With `DIGEST_ONLY`, no durable copy of the payload is promised or retained by this profile. The exact buffer must still exist long enough to hash and execute the owning read protocol. The policy must separately permit that necessary transient processing and govern its cleanup, including crash dumps, logs and caches; “digest only” does not authorize an undocumented persistent copy elsewhere. If privacy prohibits even that processing, the read is ineligible, not an excuse to invent unobservable bytes.

The selected `DIGEST_ONLY` posture must also be compatible with required immutable receipt, coverage, decision and trace retention. It never waives the accepted Tier-2/Tier-3 rules or evidence-sufficiency requirements for the underlying consequential use. If compatible minimization cannot preserve the required proof without prohibited retention, the operation cannot proceed under this profile; report the policy conflict to its owner.

Later deletion of a retained payload leaves `payloadEvidencePosture = RETAINED_BYTES` in the original receipt and records current loss of reconstruction separately. A later candidate match against a `DIGEST_ONLY` receipt does not upgrade that receipt to `RETAINED_BYTES`. If those candidate bytes are subsequently retained, that is a separate, currently authorized capture with its own provenance and retention basis, not proof that OFARM retained the original disclosure.

No retention or availability record proves that bytes reached a recipient. Preserve the owning protocol's actual release/completion/failure evidence and timestamps; do not infer release from a committed pre-release receipt or custody check. This candidate changes neither read linearization nor external transport/acknowledgement semantics.

## 9. Duration, conflict and no-unsafe-forgetting rules

### 9.1 Explicit clocks and compatible bounds

Each policy class must define its trusted start event and deterministic duration/cutoff calculation. The bound evidence identifies the actual start event/time and resolved cutoffs. Calendar arithmetic, timezone treatment and inclusive/exclusive edges must be fixed by the materialized profile; “keep for a while”, local machine time and an unbound locale default are invalid.

For exact bulk bytes, distinguish:

1. the minimum interval during which exact retrieval is required;
2. the latest time through which retention is permitted, or an explicit governed statement that no maximum is imposed;
3. additional live obligations, such as a pending challenge, unresolved transaction, retryable intent, high-consequence reconstruction or a separately authorized hold; and
4. the immutable proof-record and policy-dependency obligations, which are not the bulk-byte clock.

Where a schedule depends on a later owner-defined terminal event, its rule and the pending obligation are bound from capture; absence or uncertainty of that event is not expiry. When the event becomes authoritative, append the exact resolved schedule evidence without changing the original record. An unresolved obligation prevents a claim that deletion is permitted, but does not confer authority to violate a maximum-retention constraint.

Admission requires a compatible policy and a credible, verifiable capability to meet its bounds and the owning lifecycle. A known minimum/maximum conflict, an unresolved governing constraint, or a profile unable to honor a maximum while its operation remains pending blocks new use. Do not automatically choose “longest retention wins”, “privacy always overrides”, or a weaker proof posture.

If a new conflict arises after capture, stop affected new uses and expose the conflict through the authorized governance/incident path. Preserve truthful evidence and apply only already authorized restriction/disposition actions. This candidate supplies neither a blanket retention extension nor an erasure waiver; changing the conflicting obligations requires the respective authority owners. Unknown or delayed cleanup cannot be reported as compliant deletion.

### 9.2 Immutable history is not an expiring bulk object

The separately stored display/payload byte object can have a governed lifecycle. The receipt, original digest, disclosure time, proof posture, policy binding and historical fact cannot be edited or deleted by that lifecycle. Policy bytes and other basis bytes needed for retained decision reconstruction remain retrievable for the applicable decision-evidence period under PR #11 section 16 and active trace law.

For PR #20 and PR #26 operations, retention must preserve the exact owner-required retry/reconciliation inputs while those obligations remain. After eligible bulk removal, the immutable binding or required tombstone continues to prevent unsafe tuple reuse and preserves the owner-defined intent, mode, result, receipt and consumption bindings. No deletion job can mark an operation unused, reopen a terminal operation, release consumed approval/decision authority, or recreate a missing success set.

These requirements also constrain data placement before capture. A layout that embeds prohibited bulk content in an immutable receipt and later proposes to redact that receipt is not conforming. Use permitted minimization and separately governed byte references without losing required proof; if the constraints cannot coexist, stop before capture/disclosure. Digest-only payload treatment is not permission to drop or rewrite sensitive immutable metadata after the fact. Any proposal to change canonical history-retention law is a separate boundary, not a #14 cleanup fix.

## 10. Encryption, custody and later inspection

Retained protected bytes require an exact governed encryption profile covering persistence, replicas, backups and the permitted retrieval path, plus an exact custody profile specifying which independently authorized principals/services may obtain plaintext for which purposes. Encryption profile selection is not an implicit grant of decryption or read authority.

The retention contract must require:

- integrity binding between the exact original byte digest and the governed storage representation; a separate ciphertext digest cannot replace the original payload/display digest;
- key/decryption availability and governed recovery sufficient for every required byte-reconstruction interval, without placing secrets in receipts or retention evidence;
- separation of tenant, purpose and custody scopes; content-address equality or deduplication cannot bridge access grants or another tenant's deletion obligations;
- verifiable treatment of keys, wrapping keys and recoverable copies for any claimed cryptographic erasure; deleting one key handle is not proof that plaintext, backup keys or replicas are gone;
- truthful compromise, loss, failed recovery and unavailable-key evidence, without automatic reissuance, re-signing or repair authority; and
- retention of verification dependencies where a signature/attestation is separately required, without inventing a new signing requirement.

This candidate does not choose a cipher, KMS, storage layout, credential verifier, custodian, key generation/rotation process or worker. Those operations require their own approved contracts and implementation evidence. It only forbids a retained-byte promise whose required decryption capability is knowingly absent or scheduled to expire too early.

Later inspection remains a new authorized use. A receipt ID, object ref, digest or old approval is not a bearer read credential. Full decision traces still require the separately authorized `AUTHORIZATION_TRACE` read and CP2-safe projection described by PR #11. Apply current scope, purpose, sovereignty and redaction rules without claiming permission-denied bytes are missing.

Do not expose a hash-comparison, existence, count, error or metadata oracle to an unauthorized requester. Proof-strength reporting must not reveal protected payload facts through diagnostics. This candidate's internal descriptions do not register public response codes.

## 11. Deletion, redaction and later disposition evidence

### 11.1 Permitted object and authority

A disposition targets exact governed content refs/digests and a declared custody/copy scope. It requires both an applicable retention-policy basis and independently valid authority for the requested action. Policy applicability, byte possession or a storage-administrator identity alone is not deletion authority.

Before destructive work, the owner must establish that the requested handling is compatible with the relevant minimum/maximum bounds, current stronger restrictions, holds, immutable-history rules and live protocol obligations. Concurrent change in a relevant obligation must be covered by the later implementation's guard and evidence. This candidate specifies that safety requirement, not a locking algorithm or new authority action.

Redaction creates a separately identified derivative with its own digest, provenance link, redaction-policy binding, permitted-use scope and retention obligations. It never changes the original digest or substitutes the derivative as exact original evidence. Deletion of the original, if permitted, is separately recorded. A redacted response is not proof that every original copy was erased.

### 11.2 Honest completion claims

Distinguish a requested/authorized disposition, started work, verified completion for a named scope, partial failure and an unresolved outcome. These are proposed internal evidence meanings, not a new runtime state machine or public reason vocabulary.

“Deletion completed” requires verified coverage of every copy and recovery route in the declared scope under the bound deletion/custody profile. A queued task, successful API response, cache eviction or one missing object is insufficient. If a backup remains recoverable until later expiry, record that fact and the residual retention obligation; do not claim complete erasure. If a profile permits scoped cryptographic erasure, label exactly that method and scope rather than claiming physical removal everywhere.

Recipient-controlled copies and independently governed stores cannot be included in a completion claim without evidence and authority for them. No deletion claim promises global recall of a past disclosure. A policy requiring a wider erasure guarantee than the admitted custody boundary can substantiate is not satisfied by narrowing the reported scope afterward.

### 11.3 Append-only support record

The proposed `AUTHORIZATION_EVIDENCE_DISPOSITION_V0_1` support profile records:

- its immutable evidence identity and the exact original challenge/approval/read-receipt or prior support-record ref/digest being described;
- the target original content ref where one exists, original digest, media/profile identity and original retention-policy binding;
- current applicable policy, disposition-authority and constraint/hold basis refs/digests, without substituting them for the original policy;
- whether it describes availability/integrity, redaction or deletion; the requested/attempted/completed/partial/unknown meaning appropriate to that claim;
- trusted actor/observer identity and times, exact copy/custody scope, evidence refs/digests for the checks performed, and unresolved limitations;
- original-byte availability and integrity observations separately from the receipt's immutable proof posture; and
- a derivative ref/digest and its own policy/provenance binding when redaction or a separately authorized recapture produced new content.

The later closed schema must distinguish observations from authorized disposition attempts and require the appropriate conditional evidence for each. An unavailable-byte observation must not require fabricated deletion authority or claim a deletion occurred. A requested deletion must not carry completion evidence as if it had already executed.

Use existing `EvidenceEvent` / `evidence record` classification for this support statement only. The policy-admission or deletion-authorizing governance act remains separately owned; this supporting record cannot itself enact one. If the bounded statement does not fit that carrier/classification, stop for a separate Event Grammar or evidence-carrier prerequisite.

All references are constructible: the original receipt binds the already finalized policy/content, not a future disposition digest; later support records bind finalized original records and any finalized predecessor. Corrections append linked evidence and preserve prior statements. No circular future-digest reference, mutable status row or duplicate operation ledger can become the historical proof.

## 12. Future machine package and delivery gates

| Unit | Minimum proposed materialization | Explicit limit |
|---|---|---|
| `AuthorizationEvidenceRetentionPolicy v0.1` | One closed non-default policy family, exact digest/profile rules, admitted instance examples and negative cases | Does not modify current AgentTraceRetentionPolicy, DataSovereigntyBoundary or role/grant families |
| Approval display and governed-read receipt profiles | Required policy/schedule bindings and the conditional claims in sections 7-8 within the PR #11 / #20 evidence package | No new approval mode, read receipt namespace, consumption rule or disclosure point |
| `AUTHORIZATION_EVIDENCE_DISPOSITION_V0_1` | One tagged support profile, preferably within proposed `AuthorizationFinalizationEvidence v0.2`, with exact conditional fields and classification proof | That package is still proposed; schema-fit review is required, not presumed from the name |
| Qualification of later inspection | Bind safe current availability/proof limits through the owning CP2-compatible surface | No private public-code registry or unauthorized evidence endpoint |

The retention-policy family is separately governed policy content referenced by the existing authorization evidence packages, not a fifth top-level authorization bundle or a replacement policy/source registry.

Exact schemas, field selectors, digest constructions, canonical time arithmetic, approved encryption/custody/deletion profiles, sample policy values and executable tests do not exist in this PR. They are materialization gates, not optional runtime choices. A schema/profile review must reject ambiguous clocks, opaque policy precedence, incompatible bounds, missing dependencies and unsupported custody claims before executable use.

Preserve PR #11 section 24's order: adjacent semantic contracts; separate policy-bundle draft; separate source-bundle draft; bounded evidence drafts; exact cross-binding review and accepted law; hostile conformance; explicit current/default promotion; byte-identical OFARM2 extraction; separately authorized runtime work. The retention policy and evidence must have real immutable bytes before a consumer claims their exact bindings. No placeholder can stand in for an absent profile.

This Phase A file is the whole PR boundary. Later non-default materialization remains design/contract work; actual byte storage, encryption/key operations and runtime integration require their own single-boundary PRs. Existing missing domain contracts, the complete authorization manifest, CP2 integration and OFARM2 readiness gates remain open independently.

## 13. Positive and hostile case specifications

These are design cases for later production-reachable conformance, not implemented or executed tests. The eventual harness must exercise the owning capture/read/inspection/disposition path and inspect authoritative evidence, actual byte access and relevant copy/key behavior. Mocked acknowledgements alone cannot establish custody.

| Case | Stimulus | Required observable result |
|---|---|---|
| `ER-T01` | Fresh-approval display is captured, retained and bound before challenge persistence; all owning gates pass | Exact content, person/intent, renderer/media/display-policy, locale/timezone and retention bindings remain verifiable through finalization |
| `ER-T02` | Governed read selects `RETAINED_BYTES` under compatible policy and custody | Exact committed payload ref/bytes and receipt bindings; later authorized retrieval matches the original digest |
| `ER-T03` | Trusted policy selects `DIGEST_ONLY`; later candidate bytes match or mismatch | Correct comparison under the original digest profile; never claim reconstruction or original retention |
| `ER-T04` | `DIGEST_ONLY` receipt is presented without candidate bytes | No successful byte-comparison or reconstruction claim |
| `ER-T05` | Display bytes are missing or changed before finalization | Owner's non-`ALLOW`/lifecycle behavior; no digest-only substitution or synthetic approval |
| `ER-T06` | Renderer, display policy, locale/timezone or bound metadata drifts | Reject substitution; a fresh current render is not the original proof |
| `ER-T07` | Payload is reserialized with another serializer/version/policy or encoding | New bytes do not replace the original payload/digest; report exact comparison, not semantic equivalence |
| `ER-T08` | Returned retained bytes fail their digest or storage-to-original binding | Integrity failure; no successful reconstruction, digest rewrite or hidden repair |
| `ER-T09` | Valid governed deletion removes a retained payload after all applicable obligations permit it | Original receipt, digest, time and `RETAINED_BYTES` posture unchanged; scoped deletion evidence and no present reconstruction claim |
| `ER-T10` | Exact bytes or decryption keys disappear before a required retention interval ends | Retention conformance failure; no silent downgrade or claimed compliant deletion; owning retry/reconciliation safety preserved |
| `ER-T11` | Privacy forbids a durable payload copy but permits transient processing and required immutable metadata/trace | Trusted `DIGEST_ONLY` may be selected if every other owner requirement is met; logs/caches/backups do not retain an undeclared payload copy |
| `ER-T12` | Privacy also forbids required display bytes, transient processing, or unavoidable immutable proof metadata | No conforming capture/disclosure; explicit policy conflict, not dropped evidence or overwritten history |
| `ER-T13` | Caller selects a weaker policy/posture, unknown policy version, mutable ref or placeholder digest | No conforming admission or protected disclosure based on that substitute |
| `ER-T14` | Maximum retention conflicts with a minimum, pending lifecycle, hold or consequential trace obligation | Block new use; no automatic precedence or expiry. A later-arising conflict is escalated without fabricated permission or compliance |
| `ER-T15` | Cleanup reaches a cutoff edge, clock disagreement, or unknown terminal event | Apply the exact materialized time rule; uncertainty is not expiry or deletion permission |
| `ER-T16` | Full trace/decision basis is discarded because the payload is `DIGEST_ONLY` | Fail independent trace/evidence obligations; payload posture is no waiver |
| `ER-T17` | Byte expiry would erase retry intent, reconciliation inputs, consumption or an operation-binding tombstone | Required owner evidence remains; no tuple reuse, new effect, revived approval or guessed receipt |
| `ER-T18` | A requester lacks current evidence-read authority but possesses the digest or receipt ID | No protected bytes, existence oracle or comparison oracle; qualified denial is not a deletion claim |
| `ER-T19` | Redaction creates a derivative, or later candidate bytes are recaptured | Separate content/digest/policy/provenance; original receipt and posture remain unchanged |
| `ER-T20` | Deletion API reports success while a replica, backup key or recoverable copy remains | Partial/scoped evidence with residual limitations; no complete erasure claim |
| `ER-T21` | Deletion acknowledgement is lost, retrieval fails, or work is merely queued | Unknown/requested/observed-unavailable as supported; no fabricated completion |
| `ER-T22` | Equal content hashes occur in different tenants/custody scopes | No cross-scope access, unauthorized comparison, key sharing or unsupported deletion claim |
| `ER-T23` | A later policy is stricter or an original policy dependency disappears | Original bindings stay immutable; current restrictions need governed basis; lost reconstruction dependencies are reported |
| `ER-T24` | Custody evidence is used to infer human assent, authorization, actual release, recipient receipt or global recall | Reject each unsupported stronger claim; retain the owning protocol's independent evidence |
| `ER-T25` | A storage administrator or policy author requests deletion without current independently valid authority | No destructive action based solely on possession, policy authorship or administrative access |
| `ER-T26` | Proposed evidence layout embeds privacy-prohibited bulk bytes in an immutable receipt | Reject the layout before capture; no later receipt-redaction workaround |
| `ER-T27` | A disposition record claims completion before its target or evidence is finalized | Reject impossible/forward-digest bindings and claim/evidence mismatch; retain constructible append-only history |
| `ER-T28` | A direct-human or `NOT_REQUIRED` operation uses the retention policy | Preserve its existing act/transaction requirements; create no fresh-approval challenge |

| Issue #14 acceptance criterion | Candidate sections | Principal cases |
|---|---|---|
| Exact human-visible approval bytes and metadata | 6-7 | T01, T05-T06 |
| Retained versus digest-only read proof | 5, 8 | T02-T04, T09-T10 |
| Exact payload, serializer and policy bindings | 6, 8 | T02, T07-T08, T13 |
| Immutable receipt/digest/disclosure history after deletion or redaction | 8-9, 11 | T09, T17, T19, T24, T26 |
| Duration, encryption, deletion, redaction and custody requirements without a provider | 6, 9-12 | T10-T12, T14-T15, T20-T23, T25 |
| Hostile drift, loss, false reconstruction, digest mismatch and privacy prohibition | 13 | T04-T16, T18-T27 |

`Tnn` abbreviates `ER-Tnn`. Later implementation must add invariant-to-code-to-test traceability in its own PR. This table is not executable coverage or evidence that any custody promise has been met.

## 14. Steward approval card and next step

Decision ID: `OFARM-ISSUE14-AUTHORIZATION-EVIDENCE-RETENTION-PROOF-STRENGTH-001`

Version: `1`

Requested approval: these Phase A semantics at the exact reviewed commit, not schema acceptance, storage/key operations, merge, currentness or OFARM2 implementation.

| Decision | Proposed answer |
|---|---|
| One dedicated immutable retention-policy family; unchanged current trace/sovereignty schemas? | Yes |
| Mandatory retained display bytes for fresh approval; no digest-only approval fallback or synthetic challenge? | Yes |
| Preserve the original two read postures while separating current availability and integrity? | Yes |
| Require explicit, compatible time/privacy/lifecycle constraints and exact governed custody profiles? | Yes; an unresolved conflict is not runtime discretion |
| Preserve immutable receipts, original policy/digest/time/posture and no-unsafe-forgetting evidence after eligible bulk deletion? | Yes |
| One bounded append-only disposition support profile in the existing proposed evidence package, subject to carrier/classification review? | Yes; no new governance authority, event family or ledger |
| Leave provider, key operations, runtime, acceptance and promotion to separately approved stages? | Yes |

Scope confirmation: this candidate stays within **authorization evidence retention and custody / proof strength**. No other trust boundary or approved candidate is edited. Repository structural checks can establish package hygiene, not semantic approval or runtime retention compliance; the historical candidate lane is excluded from several package-index checks.

What is next: review the candidate's proof limits, policy conflicts, immutable-history protections and future evidence-carrier fit before requesting exact-head Phase A semantic approval.
