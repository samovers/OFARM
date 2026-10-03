# Inactive structure and compliance assertion inputs

Status: **draft/non-default, incomplete, non-executable**. This component adds
`EI_STRUCTURE_ASSERTION_V0_2` and `EI_COMPLIANCE_ASSERTION_V0_2` as input
formats for the unchanged full three-branch AssertionRecord submission contract.
It does not add either action to the initial release's admitted set of
`ASSERT_OPERATION_CLAIM` and `RECEIVE_READ_DATA`.

Primary trust boundary: **authorization-input integrity**. The capability is
closed input validation, exact identity extraction and complete-intent hashing.
It creates no authority result, domain verdict, assertion, approval or transaction.

## Exact dependencies and draft choices

The component is built above PR43 at
`546f831f495d60b45e93b55fbaaa601b1374ad7e`.
Its manifest binds actual schema and extractor bytes, the unchanged PR41
AssertionRecord schema and PR42 operation schema, and the current source revisions:

- PR11 `d1178fe07d57accedde5748672602db38346b3e6`, especially sections
  7.2–7.8 and 8.2–8.6.
- PR23 `6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f`, especially sections
  5–8, 11 and 15.

These sources determine the required content and its meaning. The concrete
schema identities, field layout and extraction bytes remain proposed,
reviewable machine materialization. The source owner files are not changed.
File SHA-256 pins exact bytes; RFC 8785 JCS/SHA-256 covers complete JSON values.

The original operation/read schemas, descriptor, manifest, README and fixture
remain unchanged. The new descriptor contains only the two missing profiles,
so each action has one input profile. A future resolved rule must select and
pin that exact schema/extractor pair; the caller cannot choose one.
PR43's historical commit/path/digest pins are retained, not rewritten.

## Input closure

| Profile | Action | Prospective effect-subject kind | PR41 body/time definitions |
| --- | --- | --- | --- |
| EI_STRUCTURE_ASSERTION_V0_2 | ASSERT_STRUCTURE | STRUCTURE_ASSERTION | structureAssertionBody / structureTime |
| EI_COMPLIANCE_ASSERTION_V0_2 | ASSERT_COMPLIANCE | COMPLIANCE_ASSERTION | complianceAssertionBody / complianceTime |

Each input has exactly one `TARGET_SCOPE` with `AUTHORITY_TARGET` posture.
It reuses the pinned operation schema's `/$defs/targetScope`: the ten existing
scope kinds, exact immutable selector, tenant, optional twin and immutable
proof bindings. This reference shares the existing resource shape; it does not
import the operation action's approval or timing semantics.

This intentionally pins the **whole operation-schema file**, not a fragment
digest. Even an unrelated comment-only change to that file invalidates its
exact-byte dependency. A compatible replacement requires explicit review and
repinning of both inactive schemas, their descriptor/fixture/manifest and
downstream consumers such as PR45. No silent digest refresh or schema-owner
restructure is implied. A future shared-shape extraction would be a separately
scoped dependency choice; this correction retains the existing ownership.

The layout places the proposed assertion ID in `effectSubject.subjectRef`
and has no separate top-level result-ID mirror. This is not a universal
prohibition on equal ref strings elsewhere: other subject/evidence/proof/rule
bindings may contain that same string. Only the existing correction comparison
explicitly prohibits it as the superseded assertion ref. Immutable resolution
and prospective-identity truth remain separately owned.
The assertion's typed `subject` is distinct from that future assertion record.
Existing subjects carry one immutable selector; prospective subjects carry
none. The local checker rejects a prospective subject whose kind/ref equals
the existing authority anchor or a typed immutable body context. This proves
no global nonexistence and creates no identity.

Both profiles carry the exact body, corresponding `subjectTime`, evidence,
assertion-act time/posture and conditional act evidence, conditional subject
relationship proofs, and conditional correction binding. The body preserves
the exact claim text; the checker neither interprets its truth nor trims it.
Its `applicability` must equal the complete `subjectTime` object. Each
branch admits only its existing AS_OF, EFFECTIVE_FROM and EFFECTIVE_INTERVAL
profiles; interval endpoints must satisfy `start < end`. Canonical timestamp
strings are preserved without normalization.

Compliance additionally carries nonempty top-level `ruleRevisionBindings`
and `evidencePolicyRevisionBindings`. Their shapes reuse PR41's
`complianceBasis` property definitions. The flat input layout is a proposed
serialization choice; the domain result destinations remain inside
`complianceBasis`. No duplicate input wrapper is accepted. These bindings
identify claimed rules and evidence policies; they prove no compliance fact or
passing evidence policy. A compiled-output reference cannot replace the body.

Offline assertion-act evidence and correction lineage have the existing exact
presence/absence rules. An online timestamp's syntax does not establish trusted
injection. A prior assertion binding's syntax does not establish committed
existence, snapshot visibility or correction compatibility.

Operation-only fields and result-side actor/state fields are absent. No
authority principal, approver, clock cutoff, human-finalization object,
transaction record, result ID mirror or self-digest is admitted. Optional
semantic-event association is only an immutable binding shape; its actual
classification and compatibility remain with the domain/Event Ingress owners.

## One extraction and checking path

The new profiles use the existing operation profile's 25 identity mappings:
one resource and its context, effect-subject identity/proofs/time, optional
purpose and the dedicated scope/sovereignty proofs. Body, lineage, assertion-act
and compliance rule/policy content stay inside the complete hashed intent;
they are not new extracted authority facts.

The existing checker accepts two explicit closed descriptor pairs: the
unchanged operation/read pair or this structure/compliance pair. It has one
strict JSON parser, pinned local schema registry, identity-pointer engine and
JCS digest path. There is no arbitrary profile registry or runtime fallback.
Unknown or altered dependencies, duplicate names, invalid selectors, overlapping
destinations and non-identity transformations reject.

Required schema validation precedes local cross-field checks and extraction.
The new fixture's expected authorization views are independently specified.
Its schema negatives identify their precise rejection witness. Whole-intent
digest controls cover content that may change the proposed effect even when
the extracted authorization view is unchanged.

Every new-fixture `additionalProperties` witness names `unexpectedProperty`.
The checker matches that exact member against the validation error's instance
and governing schema, as well as keyword and complete instance/schema paths;
another unknown member cannot satisfy it. Older witnesses without this optional
field retain their existing matching behavior. The inactive suite requires it
for its unknown-field schema cases and commits controls for all 46 renamed
members, wrong paths/keywords/property names, missing witnesses and missing
unexpected-property names. These controls test the harness, not domain policy.

The descriptor's requirement IDs map explicitly to failure layers/codes:

| Inactive requirement | Failure layer/code |
| --- | --- |
| TIME_ORDER | SCHEMA/SCHEMA for invalid timestamp syntax/calendar; COMPONENT/INTERVAL_ORDER for non-increasing valid endpoints |
| BODY_TIME_EQUALITY | COMPONENT/APPLICABILITY_TIME_EQUALITY for unequal complete body applicability and subjectTime |
| PROSPECTIVE_SUBJECT_NON_COLLISION | COMPONENT/PROSPECTIVE_SUBJECT_IS_ANCHOR or COMPONENT/PROSPECTIVE_SUBJECT_IS_CONTEXT |
| SUBJECT_SCOPE_PROOF | COMPONENT/SUBJECT_SCOPE_PROOF_ABSENCE for an unnecessary proof; COMPONENT/SUBJECT_SCOPE_PROOF_REQUIRED for a missing required proof |
| CORRECTION_SELF_REFERENCE | COMPONENT/CORRECTION_SELF_REFERENCE |

Schema preflight runs first; an empty or malformed present proof array fails
SCHEMA/SCHEMA before those cross-field codes. The unchanged operation
descriptor uses BODY_TIME_EQUALITY for a different, explicit comparison:
when temporalBasis.sourceKind is BODY_TIME, temporalBasis.time must equal
subjectTime, emitting COMPONENT/BODY_TIME_EQUALITY. Requirement IDs are local
to their descriptor and are not interchangeable error codes. No check is weakened.

Run the existing and new input suites from the repository root:

```sh
python3 04_implementation_and_conformance/conformance_runners/ofarm_authorization_effect_intents_v0_2.py
python3 04_implementation_and_conformance/conformance_runners/ofarm_authorization_effect_intents_v0_2.py --cases 04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/OFARM_StructureComplianceEffectIntent_cases_v0_2.json
python3 package_meta/tools/run_repository_validation_suite.py
```

Use the repository's existing jsonschema, referencing and RFC 8785 dependencies.
The existing 620 input cases and sixty read-kind/form pairs remain intact.
The new suite uses fictional inputs and the actual pinned schemas. Its inventory
is recorded in the new component manifest. These checks need no database.

## Remaining owner obligations

Optional twin encoding does not decide applicability. Immutable resolution,
truthful prospective identity, tenant/scope relationships, trusted online or
offline assertion-act evidence, correction snapshot/context proof and optional
event subtype/time/dominant-context compatibility remain separately owned.
Operation foreign time qualifiers and their absent-value meaning are unchanged.

**Event/body closure — DC-02 remains unapproved.** PR23 section 7.3 requires
body-owned exact envelope time selectors and a predicate relating the exact
claim to `eventSubtypeId` and `dominantSemanticConsequence`. The pinned PR41
structure/compliance bodies supply neither the required selector definitions
nor that compatibility predicate. For AS_OF, the body must fix one allowed
eventTime/observationTime/decisionTime/effectiveFrom selector; EFFECTIVE_FROM
uses effectiveFrom, and EFFECTIVE_INTERVAL uses effectiveFrom/effectiveUntil,
all under `/timeSemantics/`, with exact subject-time equality. Event Ingress
family equality and schema-valid bindings cannot supply the missing guarantee.
Presence therefore has no complete domain compatibility PASS through this input
component; absence alone legitimately makes event association not applicable.
The optional binding remains allowed here exactly as before.

The separately proposed DC-02 absence-only initial contract would require an
explicit source-owner narrowing; it is not adopted here. Its full-event
alternative requires separately approved body-owned claim meaning, fixed time
selectors, subtype/dominant-context predicates and subject-relationship proofs,
materialized in new immutable body/contract versions before mechanical input
repinning. A family allowlist, caller Boolean or a new body language added by
this input correction cannot close that gap. Both routes remain source-owner
choices; no event allowance changes in this PR.

**Subject kinds and claim whitespace remain pending source-owner choices.**
Both profiles inherit PR41's shared subject kinds: FARM, SITE, FIELD, ZONE,
CROP_CYCLE, LOT, FACILITY, OPERATION and INPUT. This includes INPUT and OPERATION
for structure/compliance; it is inherited syntax, not a demonstrated
action-specific suitability decision. PR23 section 5.2 assigns closure of
permitted subject kinds to the action-bound body schema. The domain/body owner
must explicitly confirm or revise the branch-specific set before semantic
closure. Likewise `claimText` has minLength 1, so whitespace-only strings pass
shape validation and are preserved exactly. Whether to require meaningful
non-whitespace content needs the source owner's rule; this PR neither trims
claims nor narrows the shared body schema.

The domain owner must bind all three intent/body profiles into the unchanged
full protected-effect contract and supply the actual AR_*/PC_* payload.
PR43's declared payload-subject comparisons remain available, but copied labels
and digests do not prove truthful domain evaluation.

Structure and compliance retain fresh-human-approval semantics if later
admitted. They do not inherit the operation action's NOT_REQUIRED checkpoint.
Complete authorization rules, compliance evidence-policy evaluation, transaction
protocols, source/history closure and all applicable approval and construction
gates remain required. No current/default selection, source issuance, public
endpoint or runtime capability changes. OFARM2 #392/#396 stays parked.

Next: review and freeze these exact inactive input bindings, then consume them
in the separately owned full three-branch domain contract and payload.
