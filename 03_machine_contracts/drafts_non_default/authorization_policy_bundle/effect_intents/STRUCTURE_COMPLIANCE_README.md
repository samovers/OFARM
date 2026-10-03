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

The proposed assertion ID appears only in `effectSubject.subjectRef`.
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

