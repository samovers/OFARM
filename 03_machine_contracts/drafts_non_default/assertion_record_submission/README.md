# AssertionRecord v0.2 submission component

Status: **draft/non-default, non-executable**. This component proposes the
pending AssertionRecord carrier and its structure, operation and compliance
bodies. AssertionRecord v0.1 remains current/default and its historical examples
remain unchanged. The new bytes require review; approved source prose does not
automatically approve their concrete wire choices.

Primary trust boundary: assertion-domain record integrity. The component adds
record formats and fictional checks within that boundary. It does not implement
the complete protected-effect contract, authorization or a runtime producer.

## Owned formats

The manifest pins the actual schema bytes and canonical JSON digest, four
definition pointers and the six approved source revisions. Byte SHA-256 names
the file; the RFC 8785 JCS digest names its JSON value. The manifest is component
metadata, not an authorization-policy manifest or executable release profile.

| Definition | Owned content | Source |
| --- | --- | --- |
| `assertionRecord` | Closed pending result, subject and sole authority anchor, assertion act, time, evidence and conditional operation/compliance/correction members | #23 §§5–6 |
| `structureAssertionBody` | Typed structural claim and retained context | #23 §§5.1–5.2, 6.4 |
| `operationClaimBody` | Intended or performed operation claim; reporting Party remains distinct from claimed performer | #23 §§5.1–5.3, 6.4 |
| `complianceAssertionBody` | Typed compliance claim with retained context | #23 §§5.1–5.2, 5.4, 6.4 |

The three body names are schema review keys, not extra caller-supplied tags.
Covering all three domain branches does not select all three actions for an
executable release. Every produced carrier remains `PENDING_REVIEW`; a claim is
neither accepted truth nor proof that an intended operation was performed.

One authority anchor must not erase domain context. Operation/field/crop-cycle
and lot/field relationships remain expressible through the typed subject,
closed body context and immutable relationship-proof bindings. A binding's
syntax cannot establish the relationship's truth or completeness. Existing
subject bindings select exactly one revision reference or content digest;
prospective subjects carry neither selector and create no identity.

The source delegates concrete body forms, context roles and exact time-source
selectors to this materialization. Those proposed choices are stated in the
schema and remain reviewable draft choices. They do not extend the source's
action, authority or accepted-effect vocabulary. Operation payload bindings are
optional; valid non-payload claims must remain representable.

The proposed `claimText` is required inside each closed body. It preserves the
exact human statement; it is not an executable rule or result-level notes field.
The schema types the enclosing branch and its context/time fields. It does not
machine-validate the prose's structural, operational or compliance meaning, or
prove that every context mentioned in the statement was encoded. This is an
explicit draft choice for review, not a claim of semantic closure.

| Concrete choice | Meaning and limit |
| --- | --- |
| Nine named subject/context kinds | Preserve FARM, SITE, FIELD, ZONE, CROP_CYCLE, LOT, FACILITY, OPERATION and INPUT; exclude the unregistered catch-all OTHER. |
| `contextBindings` | Zero entries by absence or one or more ordered role-typed bindings, each with immutable proof bindings; no arbitrary maximum or role singleton. |
| Structure/compliance `applicability` | The body supplies the exact corresponding `subjectTime` object; comparison preserves the original strings. |
| Operation `temporalBasis` | Body time for intended windows/performed intervals, or exact existing payload endpoint selectors. Performed instants use existing MeasurementEvidence `/phenomenonTime/instant`, never its result time. |
| Payload/evidence schema bindings | Pin the existing schema ID, version and byte digest. Actual immutable source resolution and semantic compatibility remain separate. |
| `allegesSoftwareAgentPerformance` | A claim allegation, false for intended operations; performed claims alleging agent performance require actorship bindings. It establishes no authority. |

Event association is absent from the carrier. Its separately admitted envelope,
family, compatibility checks and trace bindings belong to the later complete
protected-effect contract.

## Integrity and time limits

Use UTF-8, RFC 8785 JCS and SHA-256 for component-owned body/result values.
The complete object is hashed; the carrier gains no invented self-digest field.
Duplicate JSON names must be rejected before constructing an object model.
Foreign immutable references remain owner dependencies even when their digest
spelling or fictional bytes can be checked locally.

The nine subject-time profiles preserve the claimed domain instant, start or
half-open interval. Canonical UTC spelling and exact nanosecond ordering are
local format checks. Assertion time, payload capture time and server receipt
time cannot silently replace the named domain time. An offline evidence binding
does not establish a trusted clock or an admitted assertion-act producer.

Correction shape names one immutable prior assertion. Actual committed prior
existence, snapshot visibility, governance/twin compatibility and resolved
subject/anchor identity remain checks for the separately bound contract. This
component does not update a prior record or create a ReviewDecision.

## Reproduce the checks

From the repository root with the existing validation dependencies:

```sh
python3 -m pip install 'jsonschema>=4.22,<5' 'rfc8785==0.1.4'
python3 04_implementation_and_conformance/conformance_runners/ofarm_assertion_record_submission_v0_2.py
python3 package_meta/tools/run_repository_validation_suite.py
```

The new runner uses the actual schema and the existing RFC 8785 implementation.
Its fixtures are fictional and its checks concern shape, component-owned
digests and selected cross-field consistency. Full-suite execution also retains
the transaction component's existing checks. No database is needed.

The case bundle has 49 positive and 440 rejection cases: 375 schema, 27 local
component, 31 integrity, six strict-JSON and one canonical-domain rejection.
It exercises all four definition pointers and all nine time profiles. Foreign
payload selectors are checked as shapes bound to existing schema hashes;
the runner deliberately does not resolve foreign records or claim their time
and content equality. PR #40 retains its 32 positive and 132 rejection cases.

Actual authorization intent schemas, the shared validation-trace envelope,
immutable resolution, authority, clock provenance, prior-record snapshot proof,
Event Ingress classification, transaction atomicity and runtime activation
remain separately owned prerequisites. Neither these fixtures nor a green
repository suite closes them. OFARM2 #392/#396 remains parked.

Next: review these exact proposed bytes and tests, then complete the separately
owned binding prerequisites before any promotion or runtime implementation.
