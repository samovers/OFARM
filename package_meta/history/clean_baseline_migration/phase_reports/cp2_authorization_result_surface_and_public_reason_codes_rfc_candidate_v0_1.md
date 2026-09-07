# OFARM CP2 Authorization-Result Surface and Public Reason Codes v0.1

Date: 2026-09-07

Status: non-authoritative Phase A candidate; review and semantic approval pending

Issue: [samovers/OFARM#30](https://github.com/samovers/OFARM/issues/30); authorization parent [#10](https://github.com/samovers/OFARM/issues/10); adjacent-contract predecessor of [#21](https://github.com/samovers/OFARM/issues/21).

Inspected canonical main: `71ca724a8b6ec23f1655b086a6f549496d10a47f`.

Downstream: [OFARM2#353](https://github.com/samovers/OFARM2/issues/353) / [draft PR #359](https://github.com/samovers/OFARM2/pull/359). This candidate alone does not unblock implementation.

## 1. Decision requested

Approve or amend the following public-response choices, not an implementation:

1. Add one conditional `AUTHORIZATION_RESULT` branch to a proposed `ResultQualificationEnvelope v0.2`. Keep the six existing surface meanings intact. Do not create a separate top-level authorization-response family or disguise a refusal as a query, preflight or domain result.
2. Preserve PR #11 section 18.7's five proposed public codes and their exact mappings. Use the existing CP2 reason-code registry process, not a private authorization vocabulary.
3. Propose one additional public code, `AUTHORIZATION_RESULT_UNAVAILABLE`, because those five codes cannot truthfully describe runtime/persistence failure or an unconfirmed commit. Distinguish these conditions through typed qualification, not a new authorization outcome.
4. Publish a committed refusal only from verified, committed owner evidence. Prepared evidence is not a public decision. An invalid request, unavailable result or unconfirmed commit carries no public authorization outcome.
5. Embed the applicable public registry definitions so retryability and safe handling remain machine-readable. None of these codes permits automatic resubmission. Later retry eligibility remains entirely with the owning transaction contract.
6. Expose only a safe primary category, disclosure qualification and permitted references. Keep full trace access separate. A receipt, reference or digest never grants read permission or proves present byte availability.
7. For committed refusal evidence, carry the owner's governed source-history qualification, including material corrections, disputes and supersession. Preserve the original outcome and source time; distinguish unavailable or withheld qualification from a verified absence of such limitations.

These are proposals for review. No code is registered, no contract is promoted, and no authorization, transaction, retention or runtime rule changes merely because this file exists or receives Phase A approval.

## 2. Primary trust boundary and PR boundary

The primary trust boundary is **public authorization-result qualification and diagnostic information disclosure**: what an application, person or agent may be told about a result, and what that message can establish.

The intended PR changes only this file in the historical phase-report lane. It does not edit active baseline files, accepted RFCs, companion policies, schemas, indexes, another candidate PR or OFARM2 code.

| Responsibility | Owner | Limit in this candidate |
|---|---|---|
| Public result fields, safe messages and registered code meanings | Existing CP2 process and issue #30 | Define a projection, not another authorization evaluator |
| Authorization outcome, canonical reason ranking, eligibility and approval path | Active authority law and pinned PR #11 | Consume the selected outcome; do not recompute it from public details |
| Corrections and qualifications of authorization evidence | Existing evidence governance and pinned PR #11 section 17.2 | Consume the owner's linked-history qualification; create no correction authority, history store or replacement decision |
| Refusal durability, protected effects, retry, single use and reconciliation | Pinned PR #11, PR #20 and PR #26 as applicable | Report verified facts; do not select a transaction outcome or retry consequence |
| Trace, target and retained-byte access | Separately authorized governed read | Current authorization is still required for each read; no bearer authority from a reference |
| Retention, deletion, custody and proof strength | Pinned PR #29 and its governing sources | Preserve distinctions; do not change policy, storage or verification protocols |
| Acceptance, current/default selection and OFARM2 extraction | PR #11 section 24 and issue #21 | A candidate, example or passing schema check does not satisfy these gates |

If a required mapping conflicts with another owner's meaning, stop before changing that boundary. Propose a linked amendment or prerequisite; do not append an authorization, transaction or custody fix to this PR.

## 3. Governing sources and exact pins

Apply `PROJECT_AUTHORITY.md`: active baseline outranks accepted RFCs, then companion artifacts, then machine contracts. The draft candidates below are planning dependencies, not accepted law. Active paths refer to the inspected main commit above.

| Source | Constraint used here |
|---|---|
| `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`, AAI-C.1 and AAI-C.1.1 | Public/tool success is not authority or truth; material qualifications must remain visible and machine-readable |
| `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`, AAI-P.1-P.3 and AAI-P.6-P.6.1 | Governed public surfaces, enforcement before success, no preflight effects, and faithful release qualification |
| `02_accepted_rfcs/OFARM_AI_Facing_Result_Qualification_and_Trace_Surface_RFC_v0_1.md` | Existing CP2 carrier ownership, applicable result limitations, separately governed trace access and registered public problems |
| `02_accepted_rfcs/OFARM_RuntimeProblem_Reason_Code_Registry_RFC_v0_1.md` | Governed code meanings and metadata; unregistered codes, missing retryability and unsafe messages fail conformance |
| [PR #11](https://github.com/samovers/OFARM/pull/11), head `03a21f669ee04f96d444e14f00ae7212cab04803` | Sections 17.2, 18.5, 18.7 and 24: immutable evidence with new linked corrections/failures, authorized reads, committed refusal bundles, five public mappings and separate CP2 acceptance |
| [PR #20](https://github.com/samovers/OFARM/pull/20), head `98f8c4fafbae42c8f7fd931f43f53adcb4733713` | Human transaction authority, display rules, single use, retry and reconciliation; no synthetic challenge for direct human action |
| [PR #26](https://github.com/samovers/OFARM/pull/26), head `e042efa2911b2ef0a61603b8e0adaa6911c03ac0` | Sections 10-12 and 14: independently verified effect/evidence commits, terminal versus retryable consequences and authorized lookup |
| [PR #29](https://github.com/samovers/OFARM/pull/29), head `8e0994cae5610ac9c0d2652e02c8a8a2dd7b45c5` | Original proof posture versus present availability; missing, denied, corrupt, redacted and digest-only evidence are different facts |

The pinned candidate files, under `package_meta/history/clean_baseline_migration/phase_reports/` at those commits, are respectively `authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md`, `governed_human_approval_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`, `not_required_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`, and `authorization_evidence_retention_and_proof_strength_rfc_candidate_v0_1.md`. They are not copied or amended here. A changed dependency head requires renewed inspection and binding review, not an automatic switch to latest.

## 4. Current CP2 inventory and compatibility decision

Both `03_machine_contracts/CONTRACT_INDEX.json` and `03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json` identify the seven schema families below as current/default v0.1, with zero non-default variants for each at the inspected commit. This is a contract-selection observation, not a runtime-readiness claim.

| Existing carrier | Inspected path | Capability and gap |
|---|---|---|
| Result qualification | `03_machine_contracts/schemas/runtime_surface/OFARM_ResultQualificationEnvelope_schema_v0_1.json` | Closed object with permission, absence, blocked-use, trace and display fields. Its six surfaces omit authorization results; domain-oriented required fields cannot honestly describe every invalid-ingress or runtime failure |
| Public reason registry | `03_machine_contracts/schemas/runtime_surface/OFARM_RuntimeProblemReasonCodeRegistry_schema_v0_1.json` | Complete public code metadata and existing families; its code pattern is extensible without changing this schema |
| Runtime problem | `03_machine_contracts/schemas/core/OFARM_RuntimeProblem_schema_v0_1.json` | Suitable closed problem object; code syntax alone does not establish registration, safe text or retryability |
| Trace retrieval | `03_machine_contracts/schemas/runtime_surface/OFARM_TraceRetrievalResult_schema_v0_1.json` | AUTHORIZATION traces and AVAILABLE / PARTIALLY_REDACTED / REDACTED / NOT_FOUND / ACCESS_DENIED. It has no general storage-unavailable or integrity-failure status |
| Preflight | `03_machine_contracts/schemas/runtime_surface/OFARM_PreflightResult_schema_v0_1.json` | Explicit non-effect preview, with its own decision vocabulary. Not a substitute for a committed authorization refusal |
| Public operation description | `03_machine_contracts/schemas/runtime_surface/OFARM_PublicOperationDescriptor_schema_v0_1.json` | Existing result-schema and reason-code references can bind a later operation-specific reply contract; no new descriptor fields are needed here |
| Public read-model envelope | `03_machine_contracts/schemas/runtime_surface/OFARM_PublicReadModelEnvelope_schema_v0_1.json` | Owns query/read/output payloads and embeds a v0.1 qualification definition. It does not automatically accept a new authorization branch |

Raw-file SHA-256 anchors for the three directly reused or extended carriers:

| Carrier | SHA-256 |
|---|---|
| ResultQualificationEnvelope v0.1 | `a6fa2ac6029b01aa5536d563dab099e8adc224e696bfd468e9bd0ab90b5eeb52` |
| RuntimeProblemReasonCodeRegistry v0.1 | `62191e9a983b5cb60468404c4c26b0e4ad7ec6298902f2c497caeea6850b57c3` |
| RuntimeProblem v0.1 | `873dbeda2932d48a54e5d08d22f4031c6a86b44712a3cec85f1c1008f4d6e95b` |

The linked CP2 core registry example is `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/runtime_surface/OFARM_RuntimeProblemReasonCodeRegistry_example_cp2_core_v0_1.json`. It contains only `EVIDENCE_INSUFFICIENT`, `MATERIALIZATION_STALE` and `PERMISSION_REDACTED`. Its `ACTIVE` value does not by itself register additional codes. The accepted RFC's examples also include `AUTHORITY_DENIED` and `HUMAN_APPROVAL_REQUIRED`. These are not silent aliases for PR #11's spellings. In particular, an example permission message that says restricted information exists cannot justify revealing a hidden target's existence in this profile.

The smallest proposed change is a new branch in the existing qualification family, plus a constrained public profile and governed registry entries. Keep RuntimeProblem v0.1 and the registry schema v0.1 unchanged. Keep the other four existing surface/consumer schemas unchanged in this candidate; later consumer bindings must explicitly negotiate v0.2. A legacy PublicReadModelEnvelope cannot embed this branch through its copied v0.1 definition. An authorization refusal is returned or linked as the authorization qualification, not relabelled QUERY_RESULT or inserted into a successful read payload.

This is versioned compatibility, not wire compatibility with a v0.1-only client. The six legacy surface branches retain their existing fields, enums and requiredness in v0.2, apart from the explicit version literal. Existing v0.1 payloads and consumers remain on v0.1 until separately migrated. Only the new branch has the distinct field applicability below.

## 5. Proposed authorization qualification shape

All names and constraints in this section are proposed future machine materialization, not files created by this PR. The authorization branch is closed. It uses `schemaVersion = ofarm.resultqualificationenvelope.v0.2` and `surfaceClass = AUTHORIZATION_RESULT`.

### 5.1 Root fields and their meaning

Required root fields are `schemaVersion`, `qualificationId`, `qualifiedAt`, `asOf`, `surfaceClass`, `truthPosture`, `permissionClass`, `dataAbsentReason`, `highConsequenceUseAllowed`, `allowedUseClasses`, `blockedUseClasses`, `traceRefs`, `displayHints`, and `authorizationResponse`. Reuse the corresponding v0.1 scalar/array shapes and enums, with the tighter rules here. Do not permit arbitrary extension objects or free-text `notes`.

| Field | Authorization-branch rule |
|---|---|
| `qualificationId` | Opaque reply identifier minted by the trusted producer, not a target ID, hash of a hidden identifier, receipt or read credential |
| `qualifiedAt` | Trusted time this outward projection was formed; not a claimed transaction commit time |
| `asOf` | Time of the source result or trusted failure observation being qualified. A recorded refusal keeps its original result time, not the current lookup time |
| `truthPosture` | `CANONICAL_HISTORY_DIRECT` only for a verified committed refusal; otherwise `UNKNOWN_OR_MIXED`. The former describes the source basis, not a claim that these projected bytes were themselves stored |
| `permissionClass`, `dataAbsentReason` | Qualify this reply's explanation/disclosure scope under section 7; never assert the existence or absence of the protected target |
| `highConsequenceUseAllowed` | Always `false`: this response cannot authorize a protected effect, attest compliance or promote a domain fact |
| `allowedUseClasses` | Non-empty unique subset of `ADVISORY_DISPLAY`, `INFORMATIONAL_DASHBOARD`, `FARMER_WORKFLOW_HINT`, `EXPORT_API_PAYLOAD`, restricted to the already authorized reply and audience |
| `blockedUseClasses` | Exact complement within the existing use-class enum. Always includes `COMPLIANCE_REVIEW`, `COMPLIANCE_OUTPUT_INPUT` and `HIGH_CONSEQUENCE_DECISION`; a separate authorized full-evidence read can have its own uses |
| `traceRefs` | Unique safe references permitted for this audience; otherwise empty. A reference is not trace availability, read authority or evidence of target existence |
| `displayHints` | Required safe label, primary message and forbidden labels; optional next-action label. Constrained templates in sections 6 and 8, not caller-authored text |

`EXPORT_API_PAYLOAD` permits serialization of this qualified reply to its authorized recipient, not export of target data or redistribution to a new audience. Allowed and blocked lists must be disjoint and complete; no empty blocked list or positive-use escape hatch is valid.

The authorization branch does not carry the domain-material fields `twinScope`, `authorityLevel`, `candidateStatus`, `stalenessClass`, `evidenceSufficiency`, source/domain result references, or domain promotion fields. Filling inapplicable fields with FRESH, SUFFICIENT or NOT_EVALUATED could invent facts. This exclusion does not apply to material qualifications of the authorization evidence itself: the conditional `sourceHistoryQualification` below reuses CP2's existing `disputeStatus` meanings for that evidence. The selected authorization outcome, source time, source-history qualification, response confirmation and disclosure limits carry the applicable meaning. A successful or permission-filtered governed read still carries all qualifications required by its own CP2 surface; it cannot use this branch to omit them.

### 5.2 Closed `authorizationResponse` member

| Field | Required shape and rule |
|---|---|
| `requestCorrelationId` | Required opaque string using the existing reference syntax; binds the response to the present call without exposing hidden request fields |
| `responseKind` | Required enum: `COMMITTED_REFUSAL`, `INGRESS_REJECTION`, `RESULT_UNAVAILABLE`, `COMMIT_UNCONFIRMED` |
| `replyMode` | Required enum: `CURRENT_ATTEMPT` or `RECORDED_RESULT`; the latter is legal only for an authorized, verified historical committed-refusal lookup |
| `authorizationOutcome` | Required: exactly `DENY`, `REQUIRE_REVIEW` or `REQUIRE_HUMAN_APPROVAL` for COMMITTED_REFUSAL; JSON null otherwise. Null means no authoritative outcome is surfaced in this reply, not that no historical record could exist |
| `sourceHistoryQualification` | Required closed object for COMMITTED_REFUSAL in either replyMode; forbidden for all other response kinds. Section 5.4 defines its availability, observation point and conditional existing CP2 disputeStatus |
| `registryRef` | Required immutable reference to the governed public registry revision; not an authorization policy/basis identifier |
| `registrySha256` | Required lowercase 64-hex SHA-256 of that registry's complete raw UTF-8 file bytes, with no normalization or self-digest field. Exact admission provenance is also required; a matching digest alone grants no authority |
| `reasonCodeDefinitions` | Required ordered array of the existing registry schema's complete reason-code entry objects, one per problem in the same order; exact value matches to the pinned registry, no locally edited messages or metadata |
| `problems` | Required array of one primary RuntimeProblem v0.1, optionally followed by one DETAILS_REDACTED problem. No duplicates, third problem, private code or changed severity |
| `traceStatus` | Required enum from section 7.2; an observation of permitted trace access, not a new trace store or operation state machine |
| `traceObservedAt` | Required date-time for an actual trace observation, otherwise null for NOT_REQUESTED or NOT_APPLICABLE; cannot be fabricated from a timeout |
| `recordedResultRef` | Optional existing owner-issued safe result reference, only for RECORDED_RESULT with current permission to disclose the reference. It grants no future access and requires no new alias store |

The profile imports the exact RuntimeProblem v0.1 definition; it does not copy the more permissive embedded PublicReadModelEnvelope variant. Each `problemId` is an opaque producer-generated identifier satisfying that core schema. `title` is the fixed label in section 6. `detail` is the registry's `safeUserMessage`; optional `suggestedRemediation`, if present, is the registry's exact `requiredRemediation`. `pointerRefs` and `relatedRefs` are absent in this profile. Trace links have one governed location, `traceRefs`, not a second unfiltered route in a problem object.

### 5.3 Source binding without a new evidence record

Before serialization, the trusted projection consumes the owning operation's exact request/attempt or authorized historical-result binding, its verified source outcome or failure observation, relevant commit confirmation, current disclosure decision and admitted profile/registry version. For committed source evidence, it also consumes the evidence owner's governed linked-history qualification and its observation point, or the trusted reason that qualification is unavailable or withheld. These are internal inputs, not caller-supplied assertions and not a new persistent authority record. The binding uses the existing owner evidence; this candidate does not add a receipt writer or require a second commit of the public explanation.

A conformance harness must show that the emitted outcome, times, mode, source-history qualification and permitted references all came from that same source binding. Mixing one tenant's outcome with another request, substituting a cached result or another record's history qualification, or accepting a fabricated commit flag fails even if the JSON is valid. Public identifiers alone are not the proof. Any later producer unable to obtain the necessary trusted bindings must not claim this profile or repair the gap with placeholders. Section 5.4 permits an explicit unavailable history qualification only when the original refusal itself is independently established and its qualified disclosure remains permitted.

### 5.4 Conditional source-history qualification

`sourceHistoryQualification` has exactly three required fields: `availability`, `asOf`, and `disputeStatus`. It qualifies the committed authorization evidence, not the target's domain state or the caller's current permission. It introduces no new authorization outcome or correction process.

| availability | asOf | disputeStatus | Required source and meaning |
|---|---|---|---|
| AVAILABLE | Owner-supplied date-time of the governed history observation point | Exactly one existing CP2 value: NONE, OPEN_DISPUTE, DISPUTED_BASIS, CORRECTED, SUPERSEDED or MIXED | The owner has established the applicable qualification for this exact source evidence, valid at the reply's governed observation point, and permits disclosure of the status and time |
| UNAVAILABLE | JSON null | JSON null | The producer cannot establish the required history qualification from trustworthy owner evidence. This does not mean that the original refusal or correction records are absent |
| WITHHELD | JSON null | JSON null | Current disclosure policy does not permit returning the qualification or its observation point. It does not disclose whether any correction/dispute/supersession exists |

AVAILABLE reuses the exact enum at `ResultQualificationEnvelope v0.1`'s `properties.disputeStatus`; this candidate does not change that enum for existing surfaces. NONE requires the owner's affirmative, complete determination that no applicable material correction/dispute/supersession limitation is present at the governed observation point. An intact original digest, empty visible search, filtered history, stale cache or incomplete lookup cannot establish NONE. The public projector consumes the owner's classification, including MIXED where applicable; it does not discover corrections, rank competing records, or decide what legally corrects or supersedes evidence.

The nested asOf is the history observation point, not the original decision time or a correction's event time. Root asOf remains the original result time; qualifiedAt remains the outward projection time. Use the owner's valid observation point for this response, not an old checkpoint chosen to omit a known material qualification. If that qualification cannot be established at the required point, use UNAVAILABLE, not an invented time or NONE. The underlying source/history bindings stay internal; no correction IDs, counts, payloads or raw history references are added to this object.

WITHHELD takes precedence when the reader may not receive the history-qualification observation, regardless of whether the producer knows its status or availability. This prevents the field from becoming a correction-existence oracle. If only correction details are restricted but the status/time may be disclosed, keep AVAILABLE with the truthful status and add the existing DETAILS_REDACTED and compatible permission/absence posture. WITHHELD likewise requires DETAILS_REDACTED and compatible withholding posture. UNAVAILABLE alone uses the existing UNAVAILABLE absence qualification without claiming an access denial or missing original bytes; if other diagnostics are suppressed, section 7's suppression precedence still applies. Trace availability remains a separate observation.

Every non-NONE status and every UNAVAILABLE/WITHHELD qualification requires the safe display sentence in section 6. Unknown or restricted qualification cannot silently become unqualified history. A reply may retain the independently verified original refusal with this explicit limitation only if its governing disclosure policy permits both the original category and that limited statement. Otherwise exclude the historical lookup from this narrow profile and use the governing lookup's permitted qualified failure; do not reveal the old outcome, invent a new denial, or manufacture a private fallback code.

## 6. Result categories, precedence and display

| Trusted source condition | Response kind / outcome | Primary code | Fixed title / safe label |
|---|---|---|---|
| Complete, verified committed non-ALLOW refusal bundle with DENY | COMMITTED_REFUSAL / DENY | AUTHORIZATION_DENIED | Authorization denied |
| Same, with REQUIRE_REVIEW | COMMITTED_REFUSAL / REQUIRE_REVIEW | AUTHORIZATION_REVIEW_REQUIRED | Review required |
| Same, with REQUIRE_HUMAN_APPROVAL | COMMITTED_REFUSAL / REQUIRE_HUMAN_APPROVAL | HUMAN_ACTION_REQUIRED | Human action required |
| Request rejected at ingress, before an authorization decision | INGRESS_REJECTION / null | REQUEST_INVALID | Request invalid |
| Trusted runtime/persistence failure prevents returning a confirmed authorization result, with no relevant unresolved commit | RESULT_UNAVAILABLE / null | AUTHORIZATION_RESULT_UNAVAILABLE | Authorization result unavailable |
| Any relevant effect or evidence commit needed for this current reply is unresolved | COMMIT_UNCONFIRMED / null | AUTHORIZATION_RESULT_UNAVAILABLE | Commit status unconfirmed |
| Details are suppressed under the disclosure rules | Keep the truthful primary row | Add DETAILS_REDACTED as secondary only | Details not shown |

For a current attempt, unresolved relevant commit evidence takes precedence over presenting a local/prepared refusal or generic failure as settled. COMMIT_UNCONFIRMED is a public confirmation limit, not a rename or recalculation of PR #26's protected-effect outcome `OUTCOME_UNKNOWN`. A proven protected-effect rollback can coexist with an unresolved failure-evidence commit. The operation owner retains both facts; the public message still must not invite a new attempt while required evidence is unsettled.

Prepared non-ALLOW evidence is internal only and cannot be published as COMMITTED_REFUSAL. The owner must first satisfy PR #11's atomic refusal-bundle rule. A genuine separately governed preflight remains PreflightResult with its non-effect semantics; it is not an alternate route for publishing an uncommitted authorization decision. An ALLOW, a protected-effect success receipt, or a domain validation failure after ALLOW is outside this failure profile and stays with its owning qualified surface. No synthetic positive public authorization code is introduced.

A refusal bundle alone does not establish every surrounding operation's no-effect consequence or retry eligibility. RESULT_UNAVAILABLE likewise does not mean rollback, terminal state, absence of older evidence or permission to retry. If the producer cannot truthfully choose a row, it cannot manufacture a durable result. A transport failure may report only the transport's already governed failure; it cannot claim CP2 conformance without a valid registered qualification.

For CURRENT_ATTEMPT, `displayHints.safeLabel` uses the fixed primary label above. For RECORDED_RESULT it is `Recorded authorization result`; the user message begins `Recorded result; not current permission.` followed by the primary safe message. COMMIT_UNCONFIRMED adds the fixed sentence `Commit status is unconfirmed. Do not resubmit while confirmation is pending.` For COMMITTED_REFUSAL in either mode, append the applicable source-history sentence below after the primary safe message. The DETAILS_REDACTED safe message, when that secondary code is present, comes last. No internal value is interpolated; RuntimeProblem titles, details and registry definitions remain unchanged.

| Source-history qualification | Required displayHints.userMessage sentence |
|---|---|
| AVAILABLE / NONE | No additional sentence; do not turn NONE into a current-authorization or complete-evidence claim |
| AVAILABLE / OPEN_DISPUTE | `The recorded authorization evidence has an open dispute.` |
| AVAILABLE / DISPUTED_BASIS | `The recorded authorization basis is disputed.` |
| AVAILABLE / CORRECTED | `The recorded authorization evidence has a linked correction.` |
| AVAILABLE / SUPERSEDED | `The recorded authorization evidence has been superseded.` |
| AVAILABLE / MIXED | `The recorded authorization evidence has material history qualifications.` |
| UNAVAILABLE | `Source-history qualification could not be established.` |
| WITHHELD | `Source-history qualification is not disclosed.` |

These sentences qualify the evidence without replacing the primary category. They do not recompute the historical outcome, reveal correction content or grant retry authority. They are governed qualification-display templates, not new RuntimeProblem codes or changes to the six existing proposed registry entries.

Every `forbiddenLabels` list includes `Authorized`, `Approved`, `Completed`, `Compliance-ready` and `No records found`. Do not convert review-required into approval, human-action-required into a review ticket, or invalid-ingress into a durable denial. Secondary redaction cannot replace or hide the primary category. English templates are specified here; a future localized template set needs the same governed bindings and hostile checks, not arbitrary runtime translation of internal diagnostics.

## 7. Disclosure and trace qualifications

### 7.1 Explanation scope, not target existence

Permission and absence fields refer to the public explanation and diagnostics. They do not describe whether a named farm, grant, person, record or hidden resource exists.

| Situation for this explanation | Permission / absence qualification |
|---|---|
| Complete applicable public explanation, with no diagnostic information suppressed | FULL_DETAIL / NOT_ABSENT |
| Some otherwise applicable explanation is suppressed | PARTIAL_REDACTION / REDACTED, plus DETAILS_REDACTED |
| All additional diagnostic explanation is withheld by authority | WITHHELD_BY_AUTHORITY / PERMISSION_LIMITED, plus DETAILS_REDACTED; the primary safe category remains visible |
| A tenant-boundary reason may itself safely be disclosed under the owning policy | TENANT_BOUNDARY_BLOCKED / PERMISSION_LIMITED, plus DETAILS_REDACTED |
| No such permission evaluation occurred, as with fixed invalid-ingress explanation | NOT_EVALUATED / NOT_APPLICABLE; no target/trace existence claim |
| An authorized explanation source or required source-history qualification is unavailable or cannot be established from trustworthy evidence, without permission suppression | FULL_DETAIL / UNAVAILABLE, with the distinct applicable source-history and trace observations; neither a denied read nor missing original bytes may be inferred |

Never select TENANT_BOUNDARY_BLOCKED merely because an internal check found a foreign tenant. If that distinction would disclose a protected fact, use the generic permitted withholding posture and primary category. FULL_DETAIL is complete detail within this public profile, not permission to read the full internal trace. Deliberately withholding otherwise applicable trace/diagnostic detail requires DETAILS_REDACTED, even though the remaining safe explanation is complete as a message.

When suppression and unavailability coexist, the root absence field describes the suppression and the separately authorized trace observation reports availability only if that fact may be disclosed. Do not erase a known limit through the single root field or expose availability to someone who is not entitled to inspect it. This branch forbids raw `sourceRefs`, redaction inventories and field-path lists. The secondary code and coarse permission posture communicate withholding without leaking hidden fields or their count.

### 7.2 Trace observation

`traceStatus` is one of `NOT_APPLICABLE`, `NOT_REQUESTED`, `AVAILABLE`, `PARTIALLY_REDACTED`, `REDACTED`, `NOT_FOUND`, `ACCESS_DENIED`, `UNAVAILABLE`, or `INTEGRITY_FAILURE`.

- NOT_APPLICABLE means no authorization-decision trace is applicable to this ingress reply. It does not assert that no operational logs exist. INGRESS_REJECTION requires this value; all other response kinds forbid it.
- NOT_REQUESTED means this projection did not perform or receive an authorized trace observation. Empty traceRefs does not mean NOT_FOUND or ACCESS_DENIED.
- AVAILABLE, PARTIALLY_REDACTED, REDACTED, NOT_FOUND and ACCESS_DENIED preserve the existing TraceRetrievalResult meanings, but may be reported only where the current reader may receive that observation. NOT_FOUND is a scoped lookup observation, never proof of rollback, target nonexistence or safe re-execution.
- UNAVAILABLE reports an authorized observation that trace content cannot currently be obtained. INTEGRITY_FAILURE reports an authorized verification failure. Neither is retyped as NOT_FOUND or ACCESS_DENIED to fit the old TraceRetrievalResult schema.
- REDACTED, PARTIALLY_REDACTED and ACCESS_DENIED require the matching permission-limited explanation and DETAILS_REDACTED. Unavailability or integrity failure alone does not assert permission suppression.

NOT_APPLICABLE requires empty traceRefs and null traceObservedAt. Every other actual-observation value requires a trusted observation time and a source binding; NOT_REQUESTED requires null traceObservedAt. Access-denied or fully redacted replies carry no trace reference unless the separately governing disclosure policy explicitly permits the safe reference itself. Availability values do not authorize returning trace content in this envelope. Reference count, order, path, hostname and identifiers must not reveal hidden basis membership. Where no safe reference is permitted, return an empty list and preserve the qualified category.

This is a small qualification enum, not an amendment to TraceRetrievalResult or a new retrieval operation. Reuse the existing trace carrier for results it can honestly express. If a later full-trace endpoint needs additional payload/status semantics, take that change through its own governed consumer binding; never fabricate a v0.1 trace result. This candidate's trace observation says nothing about the availability of separately retained approval-display or governed-read payload bytes.

### 7.3 Forbidden disclosures and rechecks

Never copy internal basis IDs, grant/revocation details, canonical reason ranks, policy content or identifiers, hidden resource existence, raw validation paths, source digests, stack traces, record counts, or caller-supplied strings into messages, remediation, metadata, references or URLs. Escaping, hashing or translating such text does not make it safe. Public registry revision references are public contract identifiers, not authorization-basis identifiers.

Full internal trace retrieval still requires the separate authorized `RECEIVE_READ_DATA` path over AUTHORIZATION_TRACE and applicable CP2 redaction. A permitted link identifies an existing governed read, not a capability token; following it rechecks current caller, scope and policy. It must not become an arbitrary redirect or an unguarded storage URL. A consumer cannot expand a safe explanation by automatically fetching traces with a more privileged identity.

The issuer must refuse a mismatched registry digest, duplicate/unregistered code, unsafe template, unsupported qualification combination or untrusted source binding before release. A replacement runtime-failure reply is possible only through the same admitted safe profile with truthful source facts. No free-form OTHER code, private fallback dictionary or hidden downgrade to an unqualified success response is permitted.

## 8. Complete proposed registry entries and next-action limits

Use the existing RuntimeProblemReasonCodeRegistry v0.1 schema and governance process. The six rows below, together with each named message/meaning/remediation/UI field, define complete proposed entries. Shared values are `retryable: false`, `redactionSensitive: true`, and `relatedTraceTypes: ["AUTHORIZATION"]` for every entry. Trace-type metadata describes relevance, not an assertion that a trace exists for this request.

Here `retryable: false` means this public problem does not permit automatic resubmission of the failed request. It is not the transaction owner's terminal/retryable consequence. A separately authorized later submission may be permitted by that owner, including a same-operation retry where its rules allow one. A consumer must not infer that permission from these codes, remediation text, HTTP status or an enabled button. Conversely, this metadata does not declare every operation permanently terminal.

| Code | Family | Severity | humanReviewRequired |
|---|---|---|---|
| AUTHORIZATION_DENIED | AUTHORITY | ERROR | false |
| AUTHORIZATION_REVIEW_REQUIRED | AUTHORITY | WARNING | true |
| HUMAN_ACTION_REQUIRED | AUTHORITY | WARNING | false |
| REQUEST_INVALID | OTHER | ERROR | false |
| DETAILS_REDACTED | PERMISSION_REDACTION | INFO | false |
| AUTHORIZATION_RESULT_UNAVAILABLE | OTHER | ERROR | false |

`humanReviewRequired: false` for HUMAN_ACTION_REQUIRED does not mean no person is needed. A required human act and a formal review are different obligations; the primary code expresses the former. A false value also does not forbid separately governed operator investigation after a failure.

### AUTHORIZATION_DENIED

- `safeUserMessage`: `This request was denied.`
- `developerMeaning`: `The verified committed authorization result is DENY. No internal denial reason is disclosed by this code.`
- `requiredRemediation`: `Use the authorized access-resolution workflow if available. A later request still needs the owning operation's authorization and retry checks.`
- `safeUiBehavior`: `Show denied, preserve withholding notices, and disable automatic resubmission. Do not imply that the target exists or that a change of credentials will succeed.`

### AUTHORIZATION_REVIEW_REQUIRED

- `safeUserMessage`: `This request requires review before it can proceed.`
- `developerMeaning`: `The verified committed authorization result is REQUIRE_REVIEW; the code is not an approval or a protected effect.`
- `requiredRemediation`: `Use the separately authorized review workflow. Continue only when the operation owner permits a newly checked attempt.`
- `safeUiBehavior`: `Show review required, not approved or human approval completed. A review link is a navigation hint, not permission to execute.`

### HUMAN_ACTION_REQUIRED

- `safeUserMessage`: `This request requires human action before it can proceed.`
- `developerMeaning`: `The verified committed authorization result is REQUIRE_HUMAN_APPROVAL. The governing action and display policy determine which human act is required.`
- `requiredRemediation`: `Open the separately authorized human-action workflow if available. Its owner must establish eligibility, the exact act and any permitted challenge.`
- `safeUiBehavior`: `Show human action required. Do not create a challenge for direct human action, manufacture approval, reuse an old challenge or treat this code as a review decision.`

### REQUEST_INVALID

- `safeUserMessage`: `This request could not be accepted in its current form.`
- `developerMeaning`: `Ingress rejected the request before producing an authorization decision. The code discloses no internal validation location or target lookup result.`
- `requiredRemediation`: `Correct the request using the published input contract. Any subsequent submission remains subject to the owning operation's rules.`
- `safeUiBehavior`: `Show invalid request, not authorization denied or no records found. Do not echo submitted values, hidden fields or internal validator paths.`

### DETAILS_REDACTED

- `safeUserMessage`: `Additional details are not shown in this response.`
- `developerMeaning`: `The public projection suppresses diagnostic information under its disclosure policy. This secondary code does not classify the primary result or confirm a hidden target.`
- `requiredRemediation`: `Continue with the qualified summary, or use a separately authorized detail-read workflow if one is available.`
- `safeUiBehavior`: `Keep the primary category visible and add a withholding notice. Do not reveal the number, identity or existence of protected source records.`

### AUTHORIZATION_RESULT_UNAVAILABLE

- `safeUserMessage`: `A confirmed authorization result could not be returned.`
- `developerMeaning`: `The qualified response reports a runtime or persistence failure, or an unresolved relevant commit. responseKind distinguishes unavailable from unconfirmed; this is not an authorization outcome.`
- `requiredRemediation`: `Use an authorized status or support workflow where available. Do not resubmit while confirmation is pending; later retry eligibility belongs to the operation owner.`
- `safeUiBehavior`: `Show result unavailable or commit status unconfirmed according to responseKind. Do not assert denial, allowance, rollback, durable absence or safe retry.`

This sixth code is a new choice proposed here, not a code previously approved in PR #11. The inspected CP2 schemas, accepted registry RFC and linked core example do not supply a registered entry with this meaning. Reusing REQUEST_INVALID would blame an otherwise valid request; reusing AUTHORIZATION_DENIED would invent a durable decision. One code with explicit responseKind distinguishes failure from uncertainty without inventing two new decision types. OTHER is the existing registry family for this code, not permission to emit an unregistered fallback reason.

Optional `displayHints.nextActionLabel` is one of `Review access options`, `Open review workflow`, `Open human-action workflow`, `Check request format`, `Check status`, or `Contact support`. The operation/disclosure owner must actually provide that safe route; otherwise omit the hint. A label carries no executable command, approval, retry flag or authority transfer. Safe challenge displays/references, when required and permitted, remain in their existing human-action display carrier with matching source bindings; this qualification does not embed or regenerate them. A historical challenge cannot be reopened merely because a recorded refusal is readable.

## 9. Historical lookup and retained-proof limits

RECORDED_RESULT reports an exact historical refusal that the current caller may inspect. It preserves the original outcome and root asOf time, uses the current projection time and current disclosure limits, and displays that it is not current permission. It must also carry section 5.4's source-history qualification and section 6's safe display sentence where applicable. It is not a replay of old public bytes with stale access or history checks. It neither re-executes the request nor reconstructs a missing original decision.

A later linked correction under PR #11 section 17.2 can materially qualify the original authorization evidence without changing its bytes, digest, original outcome or commit. Those intact historical facts do not justify omitting CORRECTED, disputed or superseded posture supplied by the evidence owner. A later authorization decision under changed permissions is not automatically a correction or supersession of the earlier evidence; only the owner's governed qualification may establish that relationship. This response neither rewrites the old refusal nor adjudicates the correction. Restricted correction details do not erase a safely disclosable status; an unavailable or undisclosable qualification follows section 5.4 instead of falling back to NONE.

Verified historical source/commit evidence does not promise that every original diagnostic byte remains available now. If evidence required to establish the refusal itself is missing or untrustworthy, the producer cannot classify it as COMMITTED_REFUSAL. Conversely, loss of optional diagnostic content does not rewrite an independently established historical refusal into a new denial, ingress error or absence claim.

A lookup denied under current authority cannot reveal the old outcome or even confirm the requested receipt exists. If the lookup itself produces a committed refusal, that reply is CURRENT_ATTEMPT and describes the lookup, not the original operation. A timeout, replica miss or incomplete lookup cannot select RECORDED_RESULT, establish rollback or prove a no-effect consequence. A request for current operation status cannot be answered with an old refusal while hiding a relevant unresolved commit; use the owning status facts and section 6's confirmation rule.

This profile does not return original retained bytes, digests, custody identifiers, byte counts or proof-strength payloads. Those remain with the separately authorized evidence-read surface. Where such a surface is linked, preserve PR #29's limits:

| Fact established by the evidence owner | Public meaning that must be preserved |
|---|---|
| Original receipt selected RETAINED_BYTES | Historical retention promise; not proof that original bytes remain available now |
| DIGEST_ONLY | Comparison with independently supplied candidate bytes may be possible through an authorized verifier; no reconstruction, origin proof or read permission from the digest |
| Current bytes missing or unavailable | Present availability limit; not permission denial, original receipt mutation or proof the decision never existed |
| Current access denied | Read was not permitted; do not reveal storage existence or claim the bytes are missing |
| Integrity verification failed | Evidence did not pass verification; do not relabel it as redacted, unavailable or successful original-byte proof |
| Authorized redacted derivative | Qualified derivative, not exact original display/payload bytes and not a replacement for immutable source evidence |

Trace availability in section 7 cannot stand in for these retained-payload facts. No receipt/hash/reference is a credential for probing storage or running equality comparisons against protected content. PR #29's later schedule-resolution carrier clarification and positive append-only schedule case remain with that owner, not this CP2 PR.

## 10. Invariants and specified conformance cases

The following are test specifications, not executed privacy, transaction or runtime evidence. Each later harness must enter through the owning public adapter with trusted owner inputs and adversarial caller input; hand-constructing a valid envelope alone does not prove conformance.

| Invariant | Required property |
|---|---|
| CP2A-I01 | Explicit versioned authorization branch; existing surface semantics remain unchanged |
| CP2A-I02 | Exact outcome/code mapping and source binding; no prepared, fabricated or cross-request durable result |
| CP2A-I03 | One truthful primary category, optional secondary withholding, complete exact registered metadata |
| CP2A-I04 | Honest permission/absence/trace qualification without target-existence or diagnostic leakage |
| CP2A-I05 | No retry, approval, effect or lookup authority from a public message/reference; uncertainty remains visible |
| CP2A-I06 | Original historical outcome, governed source-history qualification, current access and present proof/availability are distinct; material corrections/disputes/supersession cannot be silently omitted |
| CP2A-I07 | No admission/readiness claim from a candidate, example, digest or schema-only pass |

| Case | Entry condition or hostile input | Required observation | Invariants |
|---|---|---|---|
| CP2A-C01 | Verified current DENY bundle | COMMITTED_REFUSAL / DENY / AUTHORIZATION_DENIED; no positive-use permission | I02, I03, I05 |
| CP2A-C02 | Verified REQUIRE_REVIEW bundle | Exact review code and humanReviewRequired true; no approval claim | I02, I03, I05 |
| CP2A-C03 | Verified REQUIRE_HUMAN_APPROVAL requiring fresh approval | Human-action code, separate permitted exact-display workflow; no challenge fabricated from the code | I02, I03, I05 |
| CP2A-C04 | Same outcome for a direct-human-action path | Human-action message without a synthetic challenge or approval token | I02, I05 |
| CP2A-C05 | Malformed request rejected before authorization | REQUEST_INVALID, null outcome, no invented decision/trace; no raw invalid value or validator path | I02, I04 |
| CP2A-C06 | Non-ALLOW evidence prepared but not committed | No COMMITTED_REFUSAL release; owner must finish evidence handling | I02 |
| CP2A-C07 | Conclusive persistence failure, relevant commit facts settled | RESULT_UNAVAILABLE, null outcome; no durable denial, rollback or retry claim inferred from the code | I02, I05 |
| CP2A-C08 | Relevant effect commit unconfirmed | COMMIT_UNCONFIRMED and explicit do-not-resubmit qualification | I02, I05 |
| CP2A-C09 | Effect rollback proven but separate failure-evidence commit unconfirmed | Keep confirmation warning and owner block; do not erase the independently proven effect fact or invent a no-effect consequence | I02, I05 |
| CP2A-C10 | Safe partial explanation with suppressed basis details | Primary code remains; DETAILS_REDACTED and compatible permission/absence fields | I03, I04 |
| CP2A-C11 | Equivalent denied requests to hidden, foreign and inaccessible targets | Same permitted safe category/templates; no differing IDs, counts, tenant hint, links or hidden-existence inference beyond authorized facts | I02, I04 |
| CP2A-C12 | Caller tries to follow a trace reference without current access | Separate governed read refuses safely; no auto-fetch with privileged credentials or old-authority reuse | I04, I05 |
| CP2A-C13 | Authorized trace is available or partially redacted | Exact observed state/time and only permitted safe links; redaction preserves primary category | I03, I04 |
| CP2A-C14 | No trace read occurred versus an authorized scoped NOT_FOUND | NOT_REQUESTED/null time differs from observed NOT_FOUND; neither proves global absence or rollback | I04, I05 |
| CP2A-C15 | Authorized trace unavailable versus integrity failure versus denied read | Three distinct qualified observations; denied reader gains no storage-existence signal | I04, I06 |
| CP2A-C16 | Well-formed but unregistered or near-synonym reason code | Reject, including AUTHORITY_DENIED substituted for this profile's AUTHORIZATION_DENIED | I02, I03 |
| CP2A-C17 | Registered code with changed severity, retry flag, message, digest or duplicate entry | Reject mismatched registry definition; no local fallback vocabulary | I03, I07 |
| CP2A-C18 | Internal values inserted into title/detail/remediation, pointer, URL or correlation ID | Reject unsafe projection, even when escaped, hashed or translated | I04 |
| CP2A-C19 | Redaction alone, wrong outcome/code, null committed outcome, positive outcome, or inconsistent trace time | Reject invalid combinations; do not silently repair into an apparently valid decision | I01, I02, I03, I04 |
| CP2A-C20 | Valid JSON assembled from different tenant/request/receipt bindings or forged commit proof | Trusted binding check rejects before release | I02, I04 |
| CP2A-C21 | Terminal no-effect consequence followed by a UI retry attempt | No revival or same-key authority from code/remediation; owner rule controls | I05 |
| CP2A-C22 | Owner later authorizes a same-operation retry after all required facts settle | Public retryable false did not rewrite the owner's consequence; only independently checked owner permission enables submission | I05 |
| CP2A-C23 | Authorized historical refusal lookup; owner establishes no material history limitation | RECORDED_RESULT, original outcome/root asOf, AVAILABLE / NONE with valid owner observation point, current disclosure checks and recorded-not-current label; no re-execution | I02, I05, I06 |
| CP2A-C24 | Historical receipt access revoked or wrong tenant; lookup timeout or replica miss | No original result/existence leak, recreated refusal or inferred no-effect proof | I04, I05, I06 |
| CP2A-C25 | Linked evidence has lost bytes, failed integrity, a redacted derivative or DIGEST_ONLY | Authorized evidence surface preserves each proof limit; this reply does not assert retained original bytes from a receipt/hash | I04, I06 |
| CP2A-C26 | User supplies a protected receipt/hash and asks for storage/equality probing | No read/comparison credential inferred; separate evidence authorization required | I04, I05, I06 |
| CP2A-C27 | v0.1-only reader or old PublicReadModelEnvelope receives the new branch | Explicit compatibility failure; no query relabelling or silent removal of required qualifications | I01 |
| CP2A-C28 | High-consequence true, overlapping/incomplete use lists, FRESH/SUFFICIENT invented to fill legacy fields, or ALLOW through this branch | Reject; successful/domain results retain their owning surfaces | I01, I04, I05 |
| CP2A-C29 | Registry/example says ACTIVE but lacks governed admission, or profile/source digest is a placeholder | No registered-code or v0.2/runtime readiness claim | I03, I07 |
| CP2A-C30 | Valid ingress reply and valid committed refusal with no permitted trace link | Both remain truthful with empty traceRefs and their distinct trace/decision postures; emptiness is not absence | I02, I04 |
| CP2A-C31 | Authorized retrieval of an intact original DENY bundle after a governed linked correction | Keep original DENY/code/root asOf; AVAILABLE / CORRECTED at the valid history observation point and required correction sentence; no rewritten refusal or retry authority | I02, I05, I06 |
| CP2A-C32 | Same correction, with status/time disclosable but correction details restricted | Preserve CORRECTED and its sentence, add DETAILS_REDACTED and matching permission/absence posture; no correction IDs, content or counts leak | I03, I04, I06 |
| CP2A-C33 | Original refusal may be read but history qualification itself is not disclosable | WITHHELD with null history status/time and safe withholding sentence, not NONE or an existence signal; exclude lookup if even the limited statement is not permitted | I04, I05, I06 |
| CP2A-C34 | Required history unavailable, partial, stale or untrustworthy; attacker substitutes an empty filtered result or old checkpoint | Reject the forged NONE; if the trusted owner cannot establish the qualification, show UNAVAILABLE with null history status/time and explicit uncertainty. No false absence, correction-existence signal or retry permission | I02, I04, I05, I06 |
| CP2A-C35 | Owner supplies OPEN_DISPUTE, DISPUTED_BASIS, SUPERSEDED or MIXED; contrast a new decision caused only by changed permissions | Preserve each governed status and exact safe sentence without changing the original outcome; a new decision alone does not establish correction/supersession | I02, I04, I06 |
| CP2A-C36 | Missing qualification on either committed reply mode, qualification on invalid ingress, wrong-source history, inconsistent null/status/time or omitted required sentence | Reject the invalid projection; no invented classification, time, private code or silent display downgrade | I01, I02, I03, I04, I06 |

All positive COMMITTED_REFUSAL cases, including CURRENT_ATTEMPT cases C01-C04, require the owner's source-history qualification under section 5.4; a fresh commit does not waive that field. C31-C36 add the corrected, restricted, unavailable and invalid-shape variants. Original outcome, root asOf, registered mappings and retry restrictions remain fixed across those variants.

Invariant references `I01` through `I07` in the case table abbreviate `CP2A-I01` through `CP2A-I07`.

| Issue #30 criterion | Design / invariants | Cases or required review evidence |
|---|---|---|
| 1. Inventory and minimal compatible carrier | Sections 4-5; I01 | C27, C28; both currentness sources and pinned schema hashes |
| 2. Preserve five mappings | Sections 6 and 8; I02, I03 | C01-C05, C10, C16, C19 |
| 3. Qualification and persistence distinctions | Sections 5-7 and 9; I02, I04, I06 | C05-C09, C13-C15, C23-C24, C30-C36 |
| 4. Complete codes and safe retry/human handling | Section 8; I03, I05 | C02-C04, C08-C09, C17, C21-C22 |
| 5. Safe projection and separate trace access | Sections 5.4 and 7; I04, I05 | C10-C12, C15, C18, C20, C26, C32-C36 |
| 6. Retention/proof limits | Sections 5.4 and 9; I06 | C15, C23-C26, C31-C36 |
| 7. Reachable positive/hostile specifications | This section; I01-I07 | C01-C36; later adapter harness required, not asserted here |
| 8. Exact later units, bindings and gates | Section 11; I01, I03, I07 | C17, C27, C29; materialization and admission review |
| 9. One boundary and unchanged owners | Sections 2-3 and 12 | One-file diff; owner/pin review, not a runtime test |

## 11. Later materialization units and gates

These are proposed exact future destinations, not existing files or authority created by this PR. Names/placement require the governed contract stage to confirm repository conventions before writing; a placement adjustment cannot change semantics without review.

| Unit | Proposed destination and scope | Owner / gate |
|---|---|---|
| Non-default carrier revision | `03_machine_contracts/drafts_non_default/schemas/runtime_surface/OFARM_ResultQualificationEnvelope_schema_v0_2_draft.json` | CP2 qualification owner; preserve legacy branches and add the closed authorization branch |
| Constrained public profile | `03_machine_contracts/drafts_non_default/runtime_surface/OFARM_AuthorizationResultPublicProfile_v0_1.md` | CP2 public-surface owner; materialize conditional fields, trusted input bindings, permitted messages and disclosure rules from sections 5-9 |
| Governed proposed registry revision | `03_machine_contracts/drafts_non_default/runtime_surface/OFARM_RuntimeProblemReasonCodeRegistry_cp2_authorization_v0_1.json` | Existing CP2 registry owner, using registry schema v0.1. Six complete entries, unique codes, immutable revision; start DRAFT and record actual publication/admission separately |
| Positive qualification fixtures | `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/drafts_non_default/runtime_surface/cp2_authorization_result_v0_1/positive/` | One named `CP2A-Cnn.json` fixture per applicable positive case, plus trusted source-binding inputs; not runtime evidence |
| Hostile qualification fixtures | `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/drafts_non_default/runtime_surface/cp2_authorization_result_v0_1/negative/` | Named `CP2A-Cnn.json` fixtures/variants tied to section 10; schema-negative versus source/projection-negative failures identified explicitly |
| Conformance manifest | `04_implementation_and_conformance/conformance_runners/cp2_authorization_result_v0_1/OFARM_CP2_AuthorizationResult_Conformance_Matrix_v0_1.json` | CP2 conformance owner; exact case IDs, source/profile/registry hashes, expected predicates and honest execution status |
| Static contract checker | `04_implementation_and_conformance/conformance_runners/cp2_authorization_result_v0_1/validate_cp2_authorization_result_contracts_v0_1.py` | Separately authorized contract stage; check schemas, registry identity, messages and cross-bindings. It cannot prove real transaction, access-control or privacy behavior |
| Existing public consumers | Operation-specific result-schema/code references in PublicOperationDescriptor and the applicable adapter profile | Consumer binding review; no new endpoint or broad PublicReadModelEnvelope migration implied |

The registry revision is part of the existing CP2 governed registry process, not a privately authoritative dictionary. Existing unrelated codes and schemas are not renamed or withdrawn. Consumers must have the exact admitted registry bytes and applicable embedded definitions; neither a filename, a registryRef nor an ACTIVE example is enough. Registry metadata must be available with the failure, not depend on an optional network fetch that may hide retryability.

Required cross-binding review covers the exact PR #11 outcome meanings, refusal evidence and section 17.2 linked-history qualifications, PR #20 human display rules, PR #26 independent commit/lookup/retry facts, PR #29 proof limits, the two accepted CP2 RFCs, the unchanged RuntimeProblem and registry schema definitions, and each proposed consumer's version handling. It must check every implication between responseKind, outcome, source-history qualification/observation point, primary code, registry entry, trace observation, absence/disclosure posture, use lists and safe text. The future qualification schema/profile/fixtures must enforce section 5.4's conditional object and null rules, reuse the exact existing disputeStatus enum, and cover C31-C36 without creating a correction writer or history store. If the real source interface cannot supply one of these facts, resolve that with its owner before runtime work; do not insert placeholder hashes, fabricated times or trusted-looking caller flags.

The gates remain separate:

1. Review and explicit semantic approval of this exact Phase A candidate head.
2. Separately authorized non-default machine/profile/registry/fixture materialization with real bytes and cross-binding review. No active contract replacement at this step.
3. Governing CP2 registration and accepted-law/currentness changes through the established controlled process, with conformance evidence appropriate to that stage. A DRAFT registry or schema pass is not registration.
4. PR #11 section 24 and issue #21's remaining policy/source/evidence bindings, acceptance, hostile conformance and explicit promotion requirements. This candidate is one adjacent prerequisite, not closure of the remaining twelve domain-effect gaps or the full promotion chain.
5. Byte-identical governed OFARM2 extraction and separately authorized, single-boundary producer/consumer implementation. Real public adapter tests must demonstrate the production-reachable cases before claiming this capability.

Do not treat this ordered checklist as authority to perform the later steps. Contract admission and runtime readiness are separate claims with different evidence.

## 12. Phase A verification, non-goals and handoff

Phase A verification checks source pins, both currentness inventories, the three anchored schema hashes, complete registry fields, case/invariant/issue traceability, Markdown structure, diff hygiene and the one-file PR boundary. Run the existing cheap repository hygiene, generated-currentness, cross-reference and steward-guardrail checks. Several exclude historical phase reports; their success establishes package hygiene, not semantic correctness, safe disclosure, atomic persistence or runtime conformance.

No active contract, accepted law, authorization evaluator, principal/grant source, domain-effect contract, Event Grammar rule, transaction protocol, receipt writer, provider, retention store, encryption/key operation, trace verifier, API/UI/SDK endpoint, retry worker, deployment, merge or OFARM2 implementation is changed here. Scope is intentionally confined to public qualification and diagnostic disclosure.

Proposed decision ID: `OFARM-ISSUE30-CP2-AUTHORIZATION-RESULT-PUBLIC-REASONS-001`, version `1`. This is a review identifier, not a live approval record. Approval, if later given, must identify the exact reviewed head and the semantic choices in section 1, including the sixth code, branch-specific applicability and source-history qualification rules. It does not supply merge authority, admit bytes, select current/default contracts or approve implementation.

### Revision responding to the first Phase A review

The [review of head 18e426a](https://github.com/samovers/OFARM/pull/31#pullrequestreview-5134303330) identified one P2 gap: a historical refusal could be returned without qualifying a material linked correction to its own authorization evidence. This revision narrows the field exclusion, adds the conditional owner-supplied source-history object and safe display rules, and specifies C31-C36. The original refusal, six public codes, transaction authority and evidence-governance owners are unchanged. This is a proposed resolution for exact-head re-review, not a claim that the reviewer has cleared it or that Phase A is approved.

What is next: re-review the amended one-file Phase A candidate, especially source-history classification, unavailable/withheld qualification and safe display without rewriting the original refusal. Obtain explicit semantic approval before the separately governed contract-materialization stage.
