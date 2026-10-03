# Protected-effect validation-trace envelope

This proposed non-default component belongs to the existing
AuthorizationFinalizationEvidence family. Its primary trust boundary is shared
validation-evidence integrity. It supplies a common trace envelope and a finite
local integrity checker; it does not establish that domain validation occurred.

The component is stacked above the proposed operation-claim and data-read intent
component in PR #42. Prior transaction, assertion and intent component bytes and
their manifests remain unchanged. Nothing here selects a current/default schema
or creates a new event family. An admitted trace retains the existing
EvidenceEvent / evidence-record classification.

## Ownership and limits

The shared envelope binds immutable identity, authorization, intent, result and
protected-effect contract selectors to an externally schema-bound payload. PASS
and FAIL are carried dispositions. A shape-valid PASS is not proof that the
domain mappings, prerequisites or postconditions were evaluated successfully.
Those meanings remain with the protected-effect contract and payload owners.

Real closed domain payload schemas and the complete protected-effect contract
remain unavailable. Explicitly fictional schemas and records used by the checker
only demonstrate finite integrity controls; they cannot replace missing
production artifacts. No network lookup, wildcard schema or successful fallback
may stand in for an unavailable binding.

PR40's existing trace reference and trace/disposition wrapper can be checked
against their actual preserved schema. Its complete admitted-result binding
requires the real AssertionRecord protected-effect contract identity and bytes,
which remain unavailable. Matching field names or a fictional contract do not
establish that complete binding.

Open dependencies retain their existing owners: temporal admission, prospective
global identity, source history, twin applicability, all three assertion branches,
domain payload/mapping rules, full authorization-policy binding and real
clock/guard/status producers. OFARM2 #392/#396 remains parked. This component
does not establish complete release closure, runtime permission or production
readiness.

## Exact bytes and digest order

The component manifest pins the envelope schema and design, the three accepted
source revisions selected for this component, and seven unchanged prior
artifacts. A schema digest hashes its exact UTF-8 file bytes. A trace or payload
digest hashes RFC 8785 canonical JSON of the complete value, excluding nothing.
The implementation uses pinned `rfc8785==0.1.4`; ordinary sorted JSON is not a
substitute.

Finalize and verify the foreign bindings, then the payload, then the trace.
The trace's ref/digest stays outside its value, so no self-digest or future
receipt reference is needed. Later transaction evidence can bind the finalized
trace under the existing transaction protocol. Earlier traces are not rewritten.

The proposed wire choices include one result per trace, exact full selectors,
an external closed payload exposing `/overallDisposition`, and an external
content-addressed trace reference. [DESIGN.md](DESIGN.md) explains the source
mapping, exact construction, non-schema checks and owner dependencies.

## Local verification

The independent runner is registered once in the existing repository suite.
It uses real pinned local schemas and explicitly fictional foreign records.
It compares all bindings to independently supplied expected context, checks the
payload's schema/digest/copied verdict, and verifies the complete trace hash.
Missing real foreign bytes remain unavailable, including for a FAIL trace.

From the repository root with the existing validation dependencies:

```sh
python3 -m pip install 'jsonschema>=4.22,<5' 'rfc8785==0.1.4'
python3 04_implementation_and_conformance/conformance_runners/ofarm_protected_effect_validation_trace_envelope_v0_1.py
python3 package_meta/tools/run_repository_validation_suite.py
```

The runner passes 19 accepted controls and 217 expected rejections: 93 schema,
51 binding, 43 integrity, 14 unavailable-dependency, 14 strict-JSON and two
canonicalization cases. All 93 schema rejections require the intended target and
exact error witness. The repository suite retains its twelve prior checks and
adds this runner as its thirteenth.

No database, clock, transaction or runtime test result is claimed by these
fictional controls.

Next: complete combined verification and review the proposed envelope and its
explicit wire choices before any separately governed binding or runtime use.
