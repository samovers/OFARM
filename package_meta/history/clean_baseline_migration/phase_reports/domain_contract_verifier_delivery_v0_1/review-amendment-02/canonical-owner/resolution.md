# PR47 B2 — canonical and Event Ingress owner resolution

21 October 2026. **Accept B2. Remove the complete technical event-association
object from the rendered projection.** Keep its immutable envelope binding in
the intent and its validation inputs/results in the protected-effect trace.
Keep the actual alleged domain occurrence, qualifications and measurement basis
in the body. This resolves the conflict without changing PR23.

Primary boundary: **AssertionRecord domain meaning and validation integrity**.
This local source-owner proposal addresses
[comment 6310698661](https://github.com/samovers/OFARM/pull/47#issuecomment-6310698661)
at `8e86208f96756b8f271f490696e6aa7cf23605fe`, with PR45 base
`2110f6d78451b50712264dba87d0b8989f134907`. It is not source adoption,
independent-review clearance or permission to implement an ingress producer.
F4's measurement-operand repair stays with the domain owner.

My amendment-01 statement that “applicable event information” stays in P was
too broad for these association roles. This response supersedes that placement,
while retaining the prior act-metadata exclusion and evidence-closure rules.
Preserve the earlier response and examples as historical bytes.

## Deciding source clauses

The exact PR23 source is `6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f`:

- [§1 item 8, line 42](https://github.com/samovers/OFARM/blob/6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md#L42): consume the immutable envelope and independently validated family; record the association only in the protected-effect trace.
- [§7.3, lines 461–480](https://github.com/samovers/OFARM/blob/6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md#L461-L480): the optional intent binding selects the envelope; the separate Event Ingress gate supplies classification; body-schema rules select compatibility predicates and time pointers. The trace retains the association and proof. No binding means legitimate event-association NOT_APPLICABLE, not a claim that no world event occurred.
- [§11.2, lines 612–629](https://github.com/samovers/OFARM/blob/6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f/package_meta/history/clean_baseline_migration/phase_reports/assertion_record_submission_protected_effect_contract_rfc_candidate_v0_1.md#L612-L629): bind envelope/proof digests, family comparison, selected indices/proofs and all compatibility comparisons; missing required prerequisites prevent overall PASS.

The accepted [Event Ingress RFC §§4–5](https://github.com/samovers/OFARM/blob/2110f6d78451b50712264dba87d0b8989f134907/02_accepted_rfcs/OFARM_Event_Ingress_and_Promotion_Boundary_Closure_RFC_v0_1.md#L80-L133)
keeps envelopes, requests, results and promotion traces separate from assertion
records. [Platform §3.1–3.4](https://github.com/samovers/OFARM/blob/2110f6d78451b50712264dba87d0b8989f134907/00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md#L78-L111)
places relevant ingress, authority and validation gates on the path; it does
not promise pre-submission evidence production. The
[Event Grammar §4](https://github.com/samovers/OFARM/blob/2110f6d78451b50712264dba87d0b8989f134907/01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md#L123-L134)
selects family by dominant semantic consequence, not assertion subtype.

PR41's closed result has no association destination. PR42/PR44's three intents
have optional `/associatedSemanticEventBinding`, pointing to the immutable
binding definition, and no ingress-proof input property. PR45's
[mapping design, lines 129–144](https://github.com/samovers/OFARM/blob/2110f6d78451b50712264dba87d0b8989f134907/03_machine_contracts/drafts_non_default/assertion_record_submission/domain_validation/DESIGN.md#L129-L144)
explicitly leaves actual Event Ingress/domain compatibility evidence to its
owners and provides no result-copy destination. Encoding the association in
`claimText` would defeat that separation even though a JSON string is allowed.

## Exact role placement

| Current association member | Proposed placement |
| --- | --- |
| `envelope` | Outside P and every AssertionRecord destination. Map the exact envelope ref plus revision or digest to intent `/associatedSemanticEventBinding`. Resolve and bind the full envelope digest in the protected-effect trace. |
| `presence` | Derive from presence/absence of that intent field. It may remain outside P as fixture bookkeeping, with exact equality to the actual intent branch. Do not add a second wire flag. Trace an evaluated association or legitimate NOT_APPLICABLE. Remove ABSENT objects from P too. |
| `caseDefinition` | The current ID selects an event-compatibility case. Keep it in the exact versioned domain package and record the selected predicate/definition binding in validation evidence. Select it from the closed body/profile rules; a caller hint cannot select a permissive case. Do not persist this association-case selector through claimText. |
| `timeSelector`, and W04's `timeRole` | Exact envelope selector(s) and their semantic interpretation belong to the body-schema/package's compatibility rule and trace comparison. They are not caller-selected fields or copied result data. Keep the independently claimed `subjectTime` and its actual domain/evidence source in P. |
| `ingressEvidence` | Separately supplied Event Ingress owner input, resolved and admitted before the dependent domain check can pass. Bind its real ref/digest and compared envelope/classification/commit-class context in the protected-effect trace. No P, result, ordinary assertion-evidence alias or new intent property. |

Remove the technical `/association` member from the projection contract and
closed root list, then move fixture association inputs outside `claimContent`.
Use separate intent-context and verification-context slots; their fixture names
do not create a new canonical wire format. Update the selector map and evidence
role map together. Unknown projection members remain errors, not silently
discarded data. This is role-based exclusion, not a string/name scrubber.

Preserve domain meaning independently. W04 already alleges PRUNE, COMPLETED,
the qualified extent, performer and measured performance instant. W22 already
alleges analysis work IN_PROGRESS and NOT_YET_PRODUCED output, with its own
measurement basis. Those stay in the proposition. Their association-case IDs
remain available to the compatibility evaluator. A genuinely additional domain
qualification must have an explicit body definition; it cannot be hidden in
an association-case ID and then lost during this correction.

The envelope's optional presence need not change the claim text when the alleged
domain content is otherwise identical. It still changes the complete intent
and its digest and changes the trace obligations. No association is added,
removed or replaced after authorization to make a failing check pass.

## What must exist before hashing, and what may come later

**Before the complete intent is hashed and authorized:** fix the selected
action/record commit class, exact body and subject/scope/time/evidence content,
and either absence of association or the exact immutable envelope binding.
The envelope's bytes, including its declared family and time values, must be
fixed and resolvable; no future placeholder or mutable latest lookup suffices.
The expected versioned projection/body package fixes the allowed compatibility
cases and selectors. Later verification must check the actual selected package
against that binding, not invent a more permissive rule. Existing online/offline
act-field ownership and any exact-intent human approval stay unchanged.

**Before event-association validation and overall domain PASS:** obtain actual
separately passing Event Ingress evidence for that envelope digest, its dominant
consequence classification and this assertion's fixed commit class. Compare the
authoritative family to the already fixed envelope field. A disagreement fails;
it does not permit rewriting the envelope, intent or body.

The sources define those dependencies, **not a producer scheduling guarantee**:

- Pre-existing proof may be usable if it actually exists and the ingress owner's
  admission, context and any reuse rules permit this exact use. The cited
  sources do not establish blanket reuse or guarantee such proof before the
  assertion is submitted.
- Producing the separate classification evidence in the validation phase is
  consistent with these dependencies, provided it completes before the domain
  verdict consumes it and does not depend on that verdict or a later artifact.
  This is a permissible construction order, not evidence that a current producer
  implements it. The domain verifier consumes a completed immutable owner-input
  snapshot; it does not manufacture or amend ingress evidence.
- An eventual `CommitIngressResult` or `PromotionTrace` is not automatically
  that earlier proof. Their active schemas describe processing/final outcomes,
  gate sequences and source-truth links. They do not by themselves close PR23's
  exact immutable classification-proof, admission and reuse interface. If the
  proposed evidence can only be finalized after this domain verdict or effect,
  using it as the verdict's prerequisite is a cycle. Do not predeclare its
  digest, falsify completion or reinterpret a late result as earlier evidence.

The existing ingress owner must identify the actual evidence artifact/schema,
producer and admission checks; how it binds the exact envelope digest,
classification and required commit class; and its availability milestone and
dependency inputs. Its generation must not require this domain payload/trace,
the final assertion effect or this attempt's later receipt. A missing concrete
interface remains an explicit dependency for an admitted positive, not a new
producer invented by this PR. Candidate fictional conformance can demonstrate
both early-proof and validation-phase-proof ordering under stated assumptions.
It cannot claim either scheduling arrangement is deployed.

## Finite construction order

1. Fix the immutable domain/body package and actual submission content. For an
   associated path, obtain exact immutable envelope bytes from their existing
   owner and fix the intent binding; otherwise leave that binding absent.
2. Render the author's complete domain body without association metadata. For
   offline submission, obtain and seal the actual act evidence under PR23 §6.2;
   for online submission, let the trusted runtime supply assertedAt. Preserve
   those sources' existing content-binding rules without adding a new act rule.
3. Validate/hash the complete intent, including its optional envelope binding.
   Perform the existing exact-intent approval and authorization steps as required.
   Construct the proposed pending result with its unchanged body and no event
   association destination.
4. Consume eligible pre-existing ingress proof, or receive independently produced
   proof in the existing validation phase. Only the ingress owner classifies
   the envelope. Supply the actual completed proof to domain verification.
5. Check PR23 §7.3's schema, family equality, subject/anchor membership or allowed
   proof, exact time selectors and subtype/dominant-context compatibility.
   Record all independent failures; a missing prerequisite blocks PASS.
6. Bind those inputs, predicate results and selected indices in the domain
   payload/protected-effect trace. Later transaction/ingress final records remain
   separately owned; this sequence grants no runtime or commit authority.

No edge runs from the claim text to an ingress-proof digest, or from the
ingress proof back to the domain verdict consuming it. For the selected
operation checkpoint branch, PR23 §6.5 still places domain validation before T;
this correction does not move the gate or borrow later transaction evidence.

## Preservation and verification obligations

Version the new projection, examples and source map; retain all prior bytes.
Re-render W04/W22 and examples whose rendered ABSENT object is removed. Preserve
all nine time profiles and 17 eligible event/profile cells, all event-family
and subtype compatibility obligations, lowest direct-match indices before proof
fallback, and the INTENDED_WINDOW/envelope-v0.1 prohibition. Keep measured-instant
support with and without an associated event: its source remains
`/phenomenonTime/instant`, never an envelope pointer substituted for measurement.

The amended construction checks should show: no technical association roles
in P or copied claimText; exact intent-to-envelope binding; missing/wrong-digest
or wrong-commit-class ingress proof cannot pass; family divergence cannot be
repaired; package-disallowed time selectors fail; event-present and absent
paths retain their proper trace dispositions; and validation-phase evidence
does not require changing the already hashed intent/body. A proof depending on
this domain result or later receipt must be rejected as an unavailable cyclic
input. The separate domain owner retains the F4 operand-source checks.

Read-only inspection confirmed both reported reference leaks at `8e86208`.
Among 25 examples, two have PRESENT association, 18 have ABSENT and five omit
the object. Checked all three intent shapes and the result's closed field list.
The Event Ingress RFC, Event Grammar, Platform source and four ingress schemas
are byte-identical at PR23, PR45 and this reviewed PR47 head. Exact hashes and
checks are in [source-checks.json](source-checks.json).

Only this response and its source-check record were written. No shared worktree,
source authority or historical fixture was changed; no runtime/database tests,
repository suite, publication, CI or merge action ran. Scope stayed inside the
named boundary. No agent or chat was spawned or messaged.

Next: integrate this placement and explicit ingress-interface dependency with
the domain owner's F4 repair, verify the versioned examples, and obtain fresh
review of the exact amended head.
