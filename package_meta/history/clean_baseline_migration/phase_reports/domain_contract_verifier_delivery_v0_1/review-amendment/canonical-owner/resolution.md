# PR47 canonical-owner resolution proposal

21 October 2026. **Use the proposed domain-only rendering projection for both
submission postures.** The submitting author, or a source-side tool preparing
the author's claim, renders the body. The trusted online runtime supplies the
submission timestamp; the authorization path selects the asserting Party.
Neither becomes a new author of `claimText`.

Primary boundary: **AssertionRecord domain meaning and validation integrity**.
This is a local amendment proposal for the existing PR47 Delivery, not semantic
adoption, independent-review clearance, publication or implementation approval.
It interprets the pinned sources without changing them. Transaction timing,
authorization eligibility, evidence admission, runtime, CI activation and merge
remain with their existing owners. #392/#396 remain parked.

The reviewed input is PR47 `e93cad876645799789956311ea091e82064cf981`, stacked on
PR45 `2110f6d78451b50712264dba87d0b8989f134907`. This response addresses
[review 5595943440](https://github.com/samovers/OFARM/pull/47#pullrequestreview-5595943440)
and B1/F1/F2/P1 in
[comment 6309968029](https://github.com/samovers/OFARM/pull/47#issuecomment-6309968029).
F3's base-review assessment is assigned separately and is not repeated here.

## Source decision and exact ownership

PR23 at `6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f` supplies the deciding rules:

- [§6.1, lines 313–320](https://github.com/samovers/OFARM/blob/6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md#L313-L320): the canonical authorization path's `authoritySubjectPartyRef` alone supplies `assertedByPartyRef`; the caller, approver and alleged performer cannot replace it.
- [§6.2, lines 326–341](https://github.com/samovers/OFARM/blob/6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md#L326-L341): the complete intent binds the act fields; online time is trusted-runtime supplied; offline evidence authenticates exact Party/basis, subject/scope/body/evidence and source time under the existing trust policy. The evidence does not claim the later intent digest.
- [§8.1, lines 498–504](https://github.com/samovers/OFARM/blob/6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md#L498-L504): reporter mapping and exact copying of act fields, complete body and complete evidence array remain mandatory.
- [§11.1–11.2, lines 602–629](https://github.com/samovers/OFARM/blob/6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md#L602-L629): complete intent/result/schema/contract bindings, resolved evidence digests, selectors and all AR/PC dispositions remain in the trace.

The inspected PR41 carrier and PR42/PR44 intent schemas agree. All three intents
have the three act fields and no `assertedByPartyRef` property. Reporter is a
result field derived from authorization. The act-evidence binding is required
offline and absent online. The three body definitions retain `claimText` inside
the exactly copied body. Exact file paths, commits and hashes are in
[source-checks.json](source-checks.json).

## Projection correction

Retain `claimText = "Pending claim: " + JCS(P) + "."`. Amend the historical
[Phase A lines 129–153](https://github.com/samovers/OFARM/blob/e93cad876645799789956311ea091e82064cf981/package_meta/history/clean_baseline_migration/phase_reports/domain_contract_verifier_delivery_v0_1/PHASE_A.md#L129-L153)
so the package's closed selector map has these explicit rules:

| Content | Rendering and binding rule |
| --- | --- |
| Submission `/assertedAt` | Exclude from P for **both** postures. Bind the real owner-sourced value in the complete intent and result and verify its provenance and exact mapping. |
| Authorization-selected `assertedByPartyRef` | Exclude from P. Keep its authorization-result source and exact result mapping. Do not add a caller-selected reporter property to the intent. |
| `/assertionActPosture` | Exclude from P, retain and validate in the full intent/result. |
| `/assertionActEvidenceBinding` | Exclude from P. Require and resolve offline; prohibit online. Retain its exact full-record and trace bindings. It cannot re-enter P through an ordinary-evidence alias or wrapper that recreates self-attestation. |
| `/assertionBody/assertionPosture` | **Keep** INITIAL/CORRECTION in P. This is not the excluded submission-act posture. |
| Operation `/claimPosture`, alleged performer and domain time | **Keep** their full meaning. INTENDED/PERFORMED, performedByPartyRef, subject time and measurement/event selectors remain distinct from reporter and submission time. |
| Remaining domain content | Keep selected action, typed subject, sole anchor, complete body qualifications, context and relationship bindings, ordinary assertion evidence, payloads, correction lineage, compliance basis and applicable event information. Presence and array order remain material. |

The exclusions identify roles and exact selectors; they are not a recursive
deletion of any field named `assertedAt`, `posture` or `Party`. Times and Parties
that belong to the claimed domain occurrence remain claim content. The complete
intent/result still cover the excluded submission fields under their existing
owners. No new hash exclusion is introduced.

## Finite construction order

**Online:** the author/preparer fixes the domain content and renders its exact
body first. The trusted runtime observing authenticated submission supplies the
top-level `assertedAt` before intent validation and hashing. The act-evidence
field is absent. The verifier reproduces the expected rendering for comparison;
it rejects inconsistent text and never repairs the submitted body. Fresh
approval and authorization, where required, bind that completed intent.

**Offline:** use this explicit order:

1. Fix the exact domain claim, subject/scope, ordinary evidence and other
   required pre-existing bindings. Render the complete body from P.
2. The existing act-evidence owner authenticates that exact submitted content,
   the actual Party or represented-Party basis, source timestamp and governed
   time-trust context. Seal the evidence record only after those facts exist.
3. Resolve its immutable revision or calculate its digest from the final
   record, then attach that binding and its exact source timestamp to the
   unchanged submission content with VERIFIED_OFFLINE_SUBMISSION. Validate and
   hash the complete intent. The evidence record includes neither its own
   digest nor the later intent digest.
4. The existing authorization owner selects the canonical Party. Validate its
   correspondence to the independently evidenced Party/basis; construct the
   pending result with that reporter and the unchanged body, act and evidence
   fields. Approval time is not substituted for assertion time.
5. Evaluate the complete proposed intent/result and required owner inputs.
   Bind the resulting domain payload and separate trace in the existing order.
   Earlier records cannot depend on these later digests or the later receipt.

Thus the dependency is **domain content → rendered body → offline act evidence
→ evidence binding → complete intent → authorization/result/domain payload →
trace**. A revision placeholder cannot substitute for a missing immutable
record. Ordinary domain evidence must also exist independently of this act's
self-attestation; changing its label does not make a cyclic construction valid.

Existing offline evidence that attests different text cannot be retrofitted by
rewriting the historical body or evidence. The applicable owner must supply
evidence of the actual required act/content. Fictional candidate tests may model
that input explicitly; they cannot establish real evidence admission.

## Two distinct evidence closures

**Ordinary assertion-support closure:** `/evidenceBindings` is the authoritative
array for ordinary evidence relied on by the proposition, including nested
qualifiers, quantity source evidence, measurement support and actual output
records when used as assertion support. The candidate's exact schema/predicate
selector table must identify those roles. Every selected support citation must
have the same complete immutable binding in that array. Check logical identity,
kind and immutable selector, then resolve and record the actual digest. Equal
logical refs alone do not suffice. Different aliases are not presumed equal.
Preserve the whole submitted array and validate every declared evidence member.

**Complete trace closure:** bind every resolved input by its actual role and
selector, including subject/context identities, scope/relationship proofs,
payloads, prior assertions, rules/policies, Event Ingress and offline act evidence.
These remain separately typed slots. PR23 §§5.2/7.3/11.2 do not require forcing
all of them into `/evidenceBindings`. A scope proof remains in
`subjectScopeProofBindings` or the body's `relationshipProofBindings`; Event
Ingress remains separately validated and trace-bound. If a proposition also
uses a record as ordinary assertion support, that support citation must satisfy
the first rule without replacing its other role-specific checks.

The selector table is part of the one domain package, not a new generic evidence
registry. Do not infer roles by field-name suffixes or treat an identity, unit,
definition or value reference as proof merely because it is present. Missing
required evidence blocks overall PASS; a named dependency failure cannot hide
another independent failure. No assertion support may escape the trace.

I directly confirmed the five cited omissions in W02/W07/W08. W07's
`route-evidence:fictional` is not its cited `Skal-or-RVO-route:fictional`. The
domain owner's broader audit reports 40 omitted support citations across 12
examples, including quantity sources and actual outputs; that assessment owns
the complete repair set. The five checked here are not a completeness claim.

## Superseding examples and required checks

Keep frozen originals and their hashes unchanged. Version the amended
projection/examples and record a before/after map for all 23 meanings. Preserve
every domain qualification, all nine profiles and 17 eligible event cells,
measurement support with and without events, and early-analysis pending versus
actual-output distinctions. Fix the domain owner's complete evidence-closure
set; do not delete qualifications to make the array match. The historical
examples remain evidence of the earlier rendering, not construction fixtures
for the amended rule.

The concrete candidate needs an exact selector mapping from example vocabulary
to the new intent/body schemas; `subject.kind` is not implicitly the current
schema's `subjectType`. Add an existing-kind structure positive and a complete
digest-bound offline positive. At the public verifier entry point, exercise
changed attested body, wrong evidence digest, mismatched Party/basis/time,
omitted support, substituted revision, and attempted self-attestation inclusion.
The online positive must show runtime-supplied time without body rewriting.
These are construction acceptance requirements, not tests reported as run here.

## L01 source-pin correction

Confirmed P1 exactly. The historical packet pin expects 3,770 bytes and SHA-256
`5c41b79832e5edd687736faae58bf912acc3552011dfc55c5f073317bce81f62`.
The live coordination file is now 5,110 bytes with SHA-256
`9a97051a1c1aaa11c0240ae3ec68b70cc1dd7fb9622ac2df7d711ebf88955c21`.
The **frozen** file still matches the expected bytes and hash:
`plans/claim-language-coverage-20261020/inventory-02/frozen-03/coordination.md`.

Use that frozen path in the versioned amendment's resolution map, or include
its exact bytes with an explicit custody entry. Preserve the old pin record
and frozen manifest as historical inputs; do not overwrite their evidence or
change L01's expected digest to fit the live file. The new mapping must name
what it supersedes and bind its own actual bytes. This repairs a locator, not
semantic authority. The earlier 946-check result is historical; I did not rerun
the inventory suite or claim a new green result.

## Completed verification and limits

Read both PR47 reviews, the coordinator proposal and exact PR23/source-schema
objects. Verified source hashes and the L01 mismatch/frozen match; directly
checked the reported W02/W07/W08 bindings. A separate read-only reviewer checked
the act ownership and finite order and agreed with excluding assertion time in
both postures and keeping reporter result-only. This is same-agent-team advice,
not independent-review clearance.

Only this owner response and its source-check record were written. No PR47
worktree, source-owner or frozen file was edited. Other owners are amending the
working packet concurrently; their work was preserved. No verifier, repository,
runtime or database tests ran, and no publication, CI or merge action occurred.
Scope stayed inside the named boundary. Formal review clearance awaits the
concrete amended design and examples.

Next: integrate this ownership/order and the domain owner's complete selector
and evidence repairs into the versioned amendment, check the new exact fixtures,
then obtain fresh review without changing the pinned source authorities.
