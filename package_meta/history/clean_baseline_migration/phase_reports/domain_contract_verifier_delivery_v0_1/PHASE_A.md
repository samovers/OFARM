# Complete typed AssertionRecord contract and verifier — Phase A v4

Status: proposed canonical, draft/non-default Delivery design. Prepared on
21 October 2026 from the reviewed inventory. This design does not adopt semantic
definitions, implement a verifier or establish a production validation result.

## Problem, outcome and one boundary

The current PR45 component can compare operation intent/result fields but cannot
validate the complete meaning of a pending claim. The selected language is a
complete typed proposition with exact rendered text for every assertion branch,
including claims without an event. A tag, keyword or matching event family
cannot establish that meaning.

The independently usable outcome is one offline command and Python function:
given original intent/result bytes, the pinned domain package and explicit
owner inputs, a caller can reproduce the domain checks and inspect every
failure or missing prerequisite. The consumer is an author or reviewer of a
proposed assertion and its evidence bundle. All three branches remain pending
claims. A successful conditional conformance test does not accept a claim.

The primary trust boundary and intended PR boundary are **AssertionRecord
domain meaning and validation integrity**. The schemas, definitions, complete
protected-effect contract, payload, evaluator, fixtures and mechanical
registration form one capability and remain in this PR. The initial design
commit is not a separately mergeable contract-only prerequisite.

The PR stacks on PR45 at `2110f6d78451b50712264dba87d0b8989f134907`. It neither
replaces PR45 nor changes its limited report into a full verdict. The base
contains the PR41 result/body, PR42 operation/read input, PR43 shared-envelope
and PR44 inactive input components. Their exact bytes and prior meanings remain
inputs. New schemas receive explicit new identities and bindings; silently
mutating a pinned old schema to reinterpret historical inputs is prohibited.

## Authority map and effects

| Owner | Responsibility retained |
| --- | --- |
| Canonical stewards/domain owners | Adopt the exact new body, definition, predicate, contract and schema bindings through the existing source process. Inventory completeness is not adoption. |
| This Delivery | Describe and implement the domain predicates, closed typed language, exact rendering, complete intent/result comparisons, prerequisite graph and domain report. |
| Authorization and input owners | Canonical Party/action/rule, authority extraction, scope eligibility, selected input profiles and action admission. Three domain branches do not enlarge the initial two-action authorization package. |
| Identity, relationship and immutable-resolution owners | Exact existing identities, directed relationships, scope/extent/time coverage and authentic resolved records. Four added subject/context kinds do not add authority anchors or create identities. |
| Measurement, provenance, use and Event Ingress owners | Actual evidence records, meaning/profile bindings, eligible use and event classification/admission. This Delivery compares their domain relevance; it does not manufacture their evidence. |
| Transaction/history owners | Proposed writes, protected uniqueness/absence, correction visibility/context, same-attempt guards, immutable inputs and commit outcome. |
| Profile owners | Local law, code/currentness, thresholds, evidence policies and deterministic calculations. NL calculations remain an explicit dependency. |
| User/repository owners | Publication, source decisions, later runtime approvals and merge under the applicable existing procedures. |

Permitted effects are non-default candidate schemas and contract bytes, an
offline verifier and its deterministic diagnostic output, focused fictional
conformance evidence, documentation and registration necessary for that
capability. Domain-owned reference updates may accompany it only when they
preserve the already accepted authorization extraction and scope semantics.

Non-effects: no result/identity/event creation, material lifecycle write,
accepted fact, authorization decision, receipt, database transaction, current
state, live evidence admission, runtime wiring, policy-bundle activation,
OFARM2 extraction, current/default promotion or production-readiness claim.
No edits to active law, old reference copies, Event Ingress classification,
foreign proof producers, clocks, guards or the shared PR43 envelope are included.
An input/proof change affecting authority or another owner's meaning becomes a
separate prerequisite; it is not folded into this PR to clear review.

## Protected facts and risk containment

Protected facts are the complete alleged meaning, its exact subject/time/extent,
original evidence, intended versus performed posture, pending status and
truthful validation findings. Untrusted inputs include caller JSON, bindings,
source strings, supplied reports, event and measurement content, and claimed
success flags. Hash equality establishes identity of bytes, not their admission.

The verifier trusts only its pinned reviewed package and the specific existing
owner mechanisms used for each input. A caller cannot select a permissive
policy, supply executable predicates, resolve “latest”, use a network fallback
or copy an expected fact from the proposed result. Compromise of a separately
trusted owner is outside this verifier's threat model; its required contract,
schema, context and binding checks are still enforced.

The primary risk is a schema-valid but semantically incomplete or contradicted
claim being presented as validated. Containment is one closed meaning path,
exact rendering and bindings, complete obligation accounting, and fail-closed
handling of unknown semantics or missing admitted inputs. An unknown predicate
is a missing contract capability, not a successful runtime dependency refusal.

## Fixed coverage and semantic invariants

The acceptance denominator is [the reviewed requirement register](reviewed-input/domain/requirements.json),
not an arbitrary count of convenient fixtures. V01 contains 14 structure rows,
V02 27 operation rows, V03 17 compliance rows, V04 12 event rows, V05 17 measured
performance rows and V06 12 relationship rows. V07 maps all 42 requirements to
those 99 definitions. Preserve all 23 original whole-claim meanings, the two
additional offline/FARM examples and original source pins. The second review
amendment versions event-role placement and measurement-source requirements.
The third versions the exact scalar provenance bindings and typed source checks;
all historical examples remain immutable. W05 retains its numeric limit,
threshold, censoring meaning and outcome while its provenance links and exact
rendered text are explicitly versioned.

| ID | Required invariant and hostile counterexample |
| --- | --- |
| DV01 | All three branches preserve every material qualification and exact rendered text. Changing negation, uncertainty, extent, activity, value, unit, evidence or revision while retaining the old text must fail. A tag beside contradictory prose is insufficient. |
| DV02 | Every ATOM has its exact definition, atom ID, subject/time/extent and complete row body. Missing scope cannot be inherited from a sibling. ALL/ANY/NOT/SEQUENCE/QUALIFIED retain the reviewed algebra; ANY cannot bypass a mandatory gate and missing evidence is not negation. |
| DV03 | All 29 AR and 20 PC duties have contract-owned predicates, explicit foreign-owner dependencies and ordered dispositions. Omission, unknown rules or required NOT_EVALUATED cannot become full PASS; an independent FAIL must survive another missing prerequisite. |
| DV04 | Nine time profiles and 17 eligible event-presence cells remain. INTENDED_WINDOW works without an event and rejects envelope-v0.1 association. A physical interval cannot become an instant because eventTime equals its end. Capture, assertion, result and record times cannot substitute for the required selected time. |
| DV05 | Event cases bind subtype presence/value, full consequence literal, pack/vocabulary revision and body concept; subtype absence differs from null. Family is independently supplied by Event Ingress. Wrong dominant consequence fails even when family and time match. Direct exact subject membership wins at the lowest matching index; only its absence allows the specific relationship proof. The anchor always requires direct exact membership. Technical association presence, envelope, case/selector and ingress-proof data stay outside the rendered body and AssertionRecord; the intent binds the optional envelope and the protected-effect trace binds the complete association verification. |
| DV06 | Performed instants use actual INSTANT MeasurementEvidence /phenomenonTime/instant with exact subjectTime equality and an operation-specific property/result/context/method/use predicate, identically with and without an event. Soil nitrate at the same time cannot establish spraying. Preserve five result kinds and five qualifier meanings plus omission; RESULT_TIME/RECORD_TIME refer to separate evidenced acts, not fallback clock fields. A measured compliance operand also requires its exact measurement binding and value pointer, selected criterion and independently fixed property/context/method/time/unit/bound expectations. Missing, empty or non-object source roles fail completeness before dependent member or alias checks; a placeholder cannot satisfy a required tuple or cause an uncaught type exception. A valid-shaped source of the wrong property fails. Quantity provenance qualifiers must belong to the pinned closed set and match the selected source role; scalar lexical evidence must match its exact resolved source, separately from full censored-result text. |
| DV07 | Fourteen quantity roles and eight material roles retain exact activity, material, role, basis, time and extent. Simultaneous rate/volume/flow/dose values stay separate. WATER at 200 L/ha in the pinned source remains WATER; an applied mixture needs its own OTHER_MATERIAL identity, definition and constituents. Do not infer additive volume or replace missing actual values with planned ones. |
| DV08 | Sampling, analysis and reporting are distinct acts. O22 occurrence/start/progress can bind PENDING_OUTPUT and an expected specification without an actual result; NOT_YET_PRODUCED differs from UNREPORTED. Completion needs the actual matching output, independent provenance and every finish condition. A work-facet measurement does not invent an analysis output. |
| DV09 | Relationships bind exact typed endpoints, direction, applicable time/extent and owner proof. Tenant match, ID similarity, arbitrary inverse or transitive shortcut fails. Retain the nine kinds plus proposed EQUIPMENT, TOOL, STORAGE_LOCATION and CONTAINER, with explicit owned interfaces and unchanged authority anchors. |
| DV10 | Result/body/intent, assertion act, accountable reporter, alleged performer, branch content, correction and absence rules remain exact. A pending material receipt, disposal, reclassification or lot-formation allegation does not perform that identity/lifecycle effect. Historical narrative and lexical evidence remain preserved and unaltered. |
| DV11 | The exact typed evidence-role map requires every relied-on supporting reference to occur with its complete immutable binding in the authoritative slot for its role. Nested assertion-support citations belong in /evidenceBindings; scope proofs and Event Ingress inputs retain their separate owner slots. Unknown roles and missing or wrong-revision members prevent PASS. Assertion-act self-attestation stays outside P and ordinary claim evidence. Actual owner records and their admission must establish every relied-on external fact. Caller valid/admitted flags, a forged rehashed report, a schema stub or an unprotected proposed-write list cannot establish it. DC-01 concerns protected proposed state through commit, not proof of a future durable commit. |
| DV12 | Core meaning is profile-neutral. BE locality, SI record-keeping exclusions, RS production hold and the narrow NL scope remain. A source-bounded inventory is not universal coverage, live legal truth or implemented NL calculation semantics. |

## Callable design and exact rendering

Proposed Python interface:

```python
verify_domain(intent_bytes, result_bytes, *, package, owner_inputs) -> DomainVerification
```

The file-based CLI accepts those same four inputs and calls that single
evaluator. Names are proposed API choices. Strict UTF-8 JSON parsing rejects
duplicate names, malformed values and unsupported canonical values. Schema
references resolve only to the exact local pinned closure. Pin the actual RFC
8785 implementation and its required behavior; ordinary sorted JSON is not
production JCS. Calendar checks cannot depend on an optional installed library.

`package` binds the selected action, intent/result/body schemas, all referenced
schemas, row definitions, typed claim-projection schema and selector map,
protected-effect contract, prerequisite graph and payload schema. These are
one owned semantic package, not a second generic rule registry. `owner_inputs`
is an immutable snapshot of exact independently supplied records, expected
bindings and the existing owner-specific verification/admission evidence.

The rendering rule remains `claimText = "Pending claim: " + JCS(P) + "."`.
P represents the complete alleged domain content, not the metadata that
authenticates this submission act. The exact package fixes its closed selector
map, field presence and array order. All body qualifications, subject and scope,
subject time, alleged performers, quantities/materials, ordinary supporting
evidence and relationship proofs remain covered. Alleged domain activity,
performance facet and subject time remain claim content regardless of whether
the complete intent associates a semantic event.

The complete technical event-association object is outside P: its optional
presence, envelope binding, compatibility-case identifier, envelope time
selector/role and Event Ingress proof are validation context. The exact optional
envelope binding stays at intent `/associatedSemanticEventBinding`; the
protected-effect trace records the resolved association, classification,
indices/proofs, selectors and compatibility findings. Neither the result nor
its exact claimText provides an association destination. The package fixes the
case and allowed selectors from body/profile meaning; a caller hint cannot
choose a permissive rule. No ordinary-evidence alias or added body member may
smuggle these technical roles back into the persisted claim. This excludes
specific owned roles, not domain occurrences, alleged activity, measurement
meaning or a similarly named domain field.

The submission's assertedAt, authorization-selected asserting Party,
assertionActPosture and assertionActEvidenceBinding do not enter P. Removing
these selectors from P does not remove them from the governed assertion: the
complete intent retains its actual act fields and binding, the result retains
its required fields, and verification compares them to their existing owners'
facts. The asserting Party is still resolved by the existing authorization
path; the candidate does not add a caller-selected Party field to that path.
Alleged performer Parties and domain time remain material claim content.

These exclusions apply to exact submission roles and selectors, not to every
similarly named field. Body INITIAL/CORRECTION posture, operation
INTENDED/PERFORMED posture, an alleged reporting act, its domain timestamp and
all measured/qualified times remain material. The act-evidence record or any
alias/descendant that depends on the rendered body cannot be relabelled as
ordinary evidence to recreate self-attestation through another path.

For online submission, the submitting author renders and fixes the complete
claim body before submission. The trusted runtime supplies the top-level
assertedAt before intent validation and hashing, as PR23 requires. It does not
write or rewrite claimText. Later approval, authorization and result mapping
use exactly those body bytes. Invalid text is rejected, not repaired in place.

For offline submission, the author first fixes the complete rendered claim,
subject/scope and ordinary evidence content. The existing act-evidence owner
then authenticates that exact content with its source time and Party/basis.
Only then can the immutable act-evidence digest be calculated and attached at
the complete intent's assertionActEvidenceBinding. The owner-sourced assertedAt
and exact content must match; the act record does not include its own digest or
the later intent digest. No digest-bound record can be included in the content
it authenticates. The owner still governs admission, proof and time trust.

The author must fix an associated envelope's exact resolvable bytes and binding
before hashing and authorizing the complete intent. Independently passing Event
Ingress proof need not be known while claimText is authored. Eligible existing
proof, or proof completed in the validation phase, must be available before the
dependent domain verdict consumes it. The sources provide no pre-submission
production or blanket reuse guarantee. The existing owner must identify the
actual artifact/schema, producer, admission/context/reuse checks and availability
milestone. Proof generation cannot depend on this domain verdict, its later
trace, final assertion effect or receipt. A later CommitIngressResult or
PromotionTrace is not automatically an earlier classification proof. The offline
verifier consumes completed immutable owner inputs; it creates no producer and
rewrites no authorized bytes. See the [canonical event resolution](review-amendment-02/canonical-owner/resolution.md)
for the finite order and source clauses.

The package must classify every immutable reference by an explicit typed role.
Assertion-support citations inside the proposition, qualifiers, quantity sources
and actual output evidence must occur with the same complete binding in
`/evidenceBindings`. Scope/relationship proof and Event Ingress inputs retain
their own exact owner slots; they are not forced into the ordinary assertion
list merely because they are immutable references. The complete validation
trace binds every resolved input across those typed roles. Logical-ref equality
alone is insufficient, and identity/value references do not become evidence
merely by occurring in a proposition. No field-name suffix scan or permissive
unknown-reference fallback may define these sets. The assertion-act
self-attestation is a separate required owner input outside P and ordinary
claim evidence. Every declared evidence member must be resolved, checked and
represented in the validation report. The concrete role map is part of the
versioned amendment and must be materialized in the future closed schemas.

Typed completeness precedes citation closure. A row that requires a measured
operand or qualification must name its exact immutable source, value pointer
and criterion/context before membership is tested; deleting that citation is
not a valid empty set. The governing criterion and existing owner contracts
independently establish the expected property, subject/extent and relationship,
method/use constraints, time, units, censoring/LOQ and bounds. Compare the
selected source value and original lexical evidence to those expectations,
retaining uncertainty rather than replacing a censored value with zero. Neither
the measurement itself nor caller-supplied matching flags may choose the
expectations. The second amendment audits analogous measured compliance roles;
its exact selectors and completeness rules remain construction inputs for the
new closed schemas, not a new evidence-admission mechanism. The third amendment
requires actual objects for measured sources, rate sources and owner-required
qualifications, validates the existing closed bindings and pointers, and guards
dependent access. A missing role and a role with the wrong JSON type both
produce explicit errors; neither becomes an empty successful citation set.

A quantity provenance qualifier describes its selected source role. LAB_RESULT
alone does not establish machine reporting. The W05 candidate explicitly models
a fictional human transcription of the laboratory LOQ and a separately authored
fictional human criterion; both quantities retain HUMAN_REPORTED under those
exact source roles. Neither a statutory label limit nor machine reporting is
inferred. The scalar source record links the exact measurement and selected
detection-limit value; its immutable binding is ordinary claim evidence. The
criterion record stays an exact definition/owner input. Real source schemas,
producer facts and admission remain with the existing owners.

Compare the claim qualifier with the closed source-backed qualifier set and the
resolved source role. Compare the LOQ scalar lexical text with the selected
scalar source field, retaining the full measurement result lexical text in its
separate field. The text "< 2 mg/kg" expresses the censored result and is not the
scalar lexical value "2". No hard-coded claim literal, silent normalization or
matching caller-controlled qualifier establishes that linkage. The criterion
owner record independently fixes the threshold, operator and provenance; the
claim cannot choose those expected values.

Compare each resolved scalar source with its independently selected exact digest,
not only a digest supplied beside that record. A different lexical source revision
requires a distinct binding and independently pinned bytes. Select required source
roles from the definition/use profile before reading claimant discriminators; a
changed result tag cannot remove scalar-source obligations. The finite W05
profile and its r2/H03 contexts are fictional non-adopted check inputs, not a
new runtime authority or a reduction of supported result branches.

All historical input and review bytes remain immutable. Corrected examples
explicitly supersede the historical rendering/projection as construction input,
retain all existing domain meanings and preserve a before/after source map.
They remain fictional candidate material, not adopted schemas or admitted proof.

The concrete versioned projection, typed reference-role table, corrected
examples, offline evidence construction and source mappings are specified in
[the third review amendment](review-amendment-03/INTEGRATION.md), which inherits
the pinned second amendment without changing its historical files. The original
and earlier amended renderings remain historical evidence. They are superseded as construction examples by
the newest version, not silently rewritten or accepted as executable positives.
No trimming, Unicode normalization, arbitrary notes field or post-authorization
translation is permitted. The complete authorized body is copied unchanged into
the pending result.

## Evaluation, report and hash order

1. Authenticate the local package bytes against the explicit expected pins;
   resolve its complete schema/definition closure and parse original inputs.
2. Validate each actual schema, branch and selected body, then compute complete
   input/result digests and the exact rendering comparison. Reuse compatible
   strict parsing, JCS and copy mechanics from PR45; do not treat MATCH as a
   domain verdict or preserve a second competing full validator.
3. Resolve each exact owner slot and check its schema, immutable binding,
   expected subject/action/scope/time or attempt context, and its actual
   owner-specific admission mechanism. A generic callback returning a Boolean
   is not that mechanism.
4. Evaluate every available independent atom, relationship, event, measurement,
   AR and PC predicate. Apply the contract-enumerated prerequisite graph to
   dependent leaves only; preserve all other failures and evidence.
5. Emit and internally validate one deterministic report with all 49 ordered
   AR/PC findings, atom/definition findings, selectors, compared digests,
   resolved-input bindings, exact text and explicit qualifications.

A complete domain payload carries the PR43 interface for both PASS and FAIL:
`proposedResultDigest`, `effectIntentDigest`, `protectedEffectContractDigest`
and the complete `selectedActionBodySchemaBinding`. It also materializes PR23
§11.2's remaining domain-owned subject/context, resolved-evidence and disposition
requirements. Every required duty must pass for overall PASS. NOT_APPLICABLE
requires a declared absent/inapplicable case; NOT_EVALUATED names a failed
contract prerequisite and prevents PASS. Internal proposition
TRUE/FALSE/INDETERMINATE results do not replace mandatory gates.

Malformed or unavailable package/schema/contract inputs produce a structured
input/dependency error, without pretending a completed payload exists. Once
the contract and relevant input identities are materialized, a missing or failed
admissible prerequisite yields the complete non-PASS findings required by that
contract; independent contradictions remain visible. Diagnostics and exit codes
must distinguish completed conditional conformance, completed failure and
unavailable evaluation. Fictional test assumptions are explicit report metadata,
outside any purported admission claim; no runtime consumer is installed here.

Schema digests hash exact file bytes. Intent, result and payload digests hash
whole RFC8785 values. The contract hashes its whole value excluding exactly its
own top-level contractDigest. Freeze schemas, then the contract, then payload,
then the separate shared trace. The contract binds a payload schema, never a
future payload digest. No cycle through the later receipt, trace, commit status
or physical time is permitted. Recomputing or relabelling a supplied report is
not verification: reproduce it from original inputs.

## Evidence dependencies and completion floor

| Slot | Concrete interface that must be closed in construction | Boundary retained |
| --- | --- | --- |
| Actor/authorization | Expected accountable Party through its existing authorization path, exact selected action/rule, actual trusted online or admitted offline assertion-act evidence. Keep submission metadata outside P; compare intent/result and actual owner facts without rewriting the body. | Authorization, input and act/time owners. |
| Identity/relationships | Exact endpoint-kind schemas and bindings, direction, interval/instant/extent coverage and admitted relation proof; actual interfaces for four proposed kinds. | Existing identity/resolution/relationship owners. |
| Measurement | Actual property/result/method/context/provenance/use schema and binding closure; actual work-facet evidence distinct from analysis output; measured criterion source/pointer and independently bound applicability expectations. | Measurement and evidence-use owners. |
| Event | Exact envelope fixed in the intent before hash/authorization; independently passing ingress proof completed before the domain verdict; concrete producer/schema/admission/reuse/timing interface without a later-verdict dependency; full meaning/subject/time predicates and trace-only association. | Event Ingress retains primary-family classification. |
| Profile | Exact rule/evidence-policy/code/currentness/threshold/calculation definitions and revisions. | Local profile owners, including the unclosed NL deterministic calculation contract. |
| History/proposed state | Actual protected proposed writes, uniqueness/absence and immutable-input facts; prior correction creation/context/visibility; same-attempt guard evidence. | Transaction/history owners; unchanged DC-01 guarantee. |

Each slot names its owning contract, actual schema revision and bytes, verified
context and existing admission mechanism. There is no new generic certificate,
parallel evidence ledger or successful fake producer. A missing exact interface
is a named dependency and keeps the relevant completion criterion open. If it
requires changes in another boundary, create separate prerequisite work before
editing there. Do not silently drop its supported domain case.

Offline candidate conformance can execute complete fictional owner records
under clearly stated test assumptions and prove every owned predicate's
behavior. It cannot establish those assumptions as real admitted facts. Before
calling the verifier implementation complete, its interfaces must be concrete
and executable, with successful and hostile cases through the public entry
point; a generic stub or permanent UNAVAILABLE branch is insufficient. Before
claiming an admitted positive, the existing owners must supply actual admitted
records. Before claiming governed end-to-end conformance, PR23 §18 and PR11
§24.2 require their separately approved runtime paths and evidence. These are
different claims and must have separate reported status.

## Verification and implementation footprint

Expected areas are the non-default assertion submission/domain-validation lane,
corresponding action/body schema references, its conformance runner/fixtures and
required indexes/manifests. No Kernel or other runtime code is included. Exact
new filenames and versions are construction details; their semantics, reference
closure and ownership must satisfy this design before source adoption.

Construction must map every one of the 42 requirements and 99 definitions to
its owning schema/predicate and independently authored public-entry-point tests.
Exercise all 49 obligations, nine profiles, 17 eligible event/profile cells,
all result/qualifier branches, all 23 preserved whole meanings, the added
offline and existing-kind structure examples, and the DV01–DV12 hostile cases.
Exercise digest-bound offline evidence with changed-body and wrong-digest
negatives, reject missing/wrong-revision nested evidence, and show online act
metadata never rewrites or enters the exact claim text. Exercise event-present
and absent paths with association verification outside the body, altered
envelope bindings, missing/mismatched ingress proof and a cyclic late-proof
dependency. Exercise required measured-citation omission and a wrong-property
source that otherwise has valid binding membership and value shape. Reject
string, array, number, Boolean, null, empty and missing required source objects,
including nested rate sources and required qualifications, with structured
errors. Exercise unknown and source-inconsistent provenance qualifiers, missing
source bindings and lexical mismatches. A positive with a different owner-supplied
scalar lexical form must demonstrate source comparison rather than a fixed
literal. Preserve the separate full measurement lexical field. Include
successful measured-instant cases with and without events,
early-analysis pending-output cases and actual-result completion. Test each
contract prerequisite edge, missing required leaf, independent failure,
forged-report subject/digest substitution, unknown recursive object member and
render-before-hash mutation. Counts alone do not establish semantic coverage.

Run the canonical registered local suite and provenance/currentness checks at
the final candidate. Preserve or explicitly version old input/component behavior
and independently inspect the mapping; do not generate expected semantic
outcomes from the implementation. Local design checks, candidate conformance,
admitted evidence and production-reachable tests must be reported separately.
CI activation and merge remain separate actions.

## Simplicity, provisional posture and decisions

One definition package and one evaluator own each domain fact and predicate.
The frozen input copies are audit evidence, not mutable second definitions.
Reuse compatible parser/render/mapping helpers and existing evidence envelopes;
delete any superseded path introduced within this capability. Existing PR45's
limited standalone comparator remains separately useful and must not be
misrepresented as the new complete validator.

The simpler rendering-only or copy-only alternative cannot check wrong
phenomenon, quantity identity, work completion or missing foreign proof. A
general policy engine adds no necessary capability here. A small direct
dispatcher over exact definition IDs and an explicit prerequisite graph serves
the actual three branches without inventing a second rule-admission system.

The posture is provisional, non-default and offline. It is acceptable before
deployment because it creates no live authority or writes and exposes every
assumption and dependency. A source contradiction, lost required meaning,
unrepresentable owner interface, hash cycle or another authority change requires
revising the design or a separate prerequisite. The upgrade path is the existing
canonical adoption/bundle/conformance/promotion/extraction sequence, not implicit
runtime activation after tests pass.

No OFARM2 decision-card sentence is imposed on canonical offline preparation.
The current request authorizes this preparation. Canonical source adoption of
the exact new meanings and bindings remains necessary; it is not supplied by
inventory review, code or a generic implementation approval. Stronger exact-action
requirements in PR23 §18 and PR11 §24.2 apply when those later actions are reached.
Keep the already approved sequence and unchanged DC-01 technical clearance;
neither is reopened here. OFARM2 #392/#396 remain parked; #421 remains separate.

Next: review this concrete design and its exact input packet, then construct the
single non-default contract/verifier capability in this same draft. Source
adoption, actual owner evidence, runtime construction, CI activation and merge
retain their separate decisions.
