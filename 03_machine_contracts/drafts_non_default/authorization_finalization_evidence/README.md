# NOT_REQUIRED transaction evidence component

Status: **draft/non-default, non-executable**. This is a transaction-evidence
component of the proposed `AuthorizationFinalizationEvidence v0.2` family. It
does not complete the selected release, promote any contract or change OFARM law.

Primary trust boundary: immutable transaction evidence integrity. The component
describes the approved `ASSERT_OPERATION_CLAIM` use, including unsuccessful and
uncertain attempts. It adds no evaluator, transaction coordinator, clock service,
database schema, disclosure path or withdrawal permission.

## Files and profile ownership

The component manifest identifies the exact schema bytes and canonical digest,
all seven definition pointers, six immutable source inputs and outstanding owner
dependencies. Its file SHA-256 and JCS digest are deliberately different: one
identifies the checked-in bytes; the other identifies their canonical JSON value.
The manifest is not an authorization-policy manifest or complete runtime profile.

| Definition | Truth claim and source |
| --- | --- |
| `callerSubmissionProjection` | Complete caller object for retry comparison, #26 §5.3. Auxiliary definition; not a root evidence record. Unknown caller members are retained for later domain-owner validation, not discarded here. |
| `operationBinding` | One immutable admitted operation and original intent, #26 §§5–6. Exact approved shape, including required null when representation does not apply. |
| `modeEvidence` | Current rule selected NOT_REQUIRED for this attempt, #26 §7.3. This record supplies no authority or human approval. |
| `transactionAttempt` | Ordered attempt, reached stages and truthful outcome, #26 §§8–12. No-effect has exactly one consequence; unresolved has none. |
| `decisionConsumption` | Single use only with complete atomic success, #11 §§18.2/18.8 and #26 §13.3. The receipt forward reference is ID-only. |
| `governedEffectReceipt` | Exact success membership, #26 §9.4. A receipt's syntax or outcome label does not prove commit or admissibility. |
| `reconciliationEvidence` | Later append-only observation/resolution, #26 §10.3. It never repairs or rewrites the earlier set. |

Six disjoint root branches use their `schemaVersion` as the discriminator. The
manifest's profile tags are metadata; they are not extra payload wrappers.
All closed record objects reject unknown members. The caller's intent stays an
opaque complete object because validating its domain content is another owner's
job. This exception cannot introduce an extra top-level transaction field.

The existing EvidenceEvent / evidence-record classification is retained only if
the evidence is separately admitted to OFARM authority. None of these profiles
creates domain truth, a ReviewDecision, accepted state or an external effect.
Other actions and human/read/filing modes are outside this component, with their
release-closure dispositions recorded in the manifest.

## Integrity and wire choices for review

Use RFC 8785 JCS, UTF-8 and SHA-256. Reject duplicate JSON names before creating
the object model and reject values outside the canonicalizer's input domain.
The manifest names each exact top-level self-digest member and provisional
sentinel. Validate the provisional record, remove only that member, hash the
remaining complete object, insert the digest and validate the final record.
Caller projection has no self-digest exclusion. No nested field is excluded.

The operation-binding wire shape is unchanged from #26 §5.5. For the other
profiles, `operation`, `attempt` and typed binding subobjects factor the approved
semantic fields into explicit closed structures. These new schema bytes and
field names are draft materialization for review, not retrospectively approved
machine formats. Shared decision consumption uses a component-specific tag; its
schema-defined integrity excludes only `decisionConsumptionDigest`, with sentinel
`ofarm:pending-decision-consumption-digest`. It does not change the authorization
bundle's owning projection or define consumption for other modes.

The operation binding's immutable carrier reference is distinct from its
`logicalOperationId` (#26 §13.1). It is assigned outside that closed payload;
the manifest does not invent an extra operation-binding ID member. Fictional
record wrappers label the carrier reference separately and are not evidence fields.

Finalize operation/mode and their inputs, then consumption → attempt → receipt.
Consumption and attempt name the preallocated future receipt by ID only. Receipt
self-membership has only role and ID; every other membership digest points to
already finalized bytes. A no-effect attempt uses the corresponding ID-only
self-entry and contains neither consumption nor a success receipt. An embedded
admitted-result binding is covered by its containing attempt; later references
use that attempt's digest and `/admittedProtectedResultBinding`.

The selected branch carries the original attempt context and matching checkpoint
in consumption, attempt and receipt. T must be before full original D, including
the original 30-second deadline. Success records have no physical commit or
consumption timestamp, including null or a renamed T. A truthful checkpoint may
survive in no-effect evidence after a later abort. It grants no retry entitlement.
Later observations point back to unchanged records. Contradictory admitted time
evidence can accompany existing quarantine; it cannot be silently erased to make
a success check pass. Quarantine is not a fourth transaction outcome.

These formats do not establish elapsed-clock provenance, the evaluator's full D,
complete guards, original-context continuity, status truth, observation admission
or TERMINATE handling through actual commit. Those real owner bindings remain
required. The approved time-policy object is not a complete transaction profile.

## Reproduce the fixture checks

From the repository root, using a local Python environment:

```sh
python3 -m pip install 'jsonschema>=4.22,<5' 'rfc8785==0.1.4'
python3 04_implementation_and_conformance/conformance_runners/ofarm_not_required_transaction_evidence_v0_1.py
python3 package_meta/tools/run_repository_validation_suite.py
```

The fixture runner is part of the existing repository suite and hosted workflow.
It uses the [RFC 8785 library](https://github.com/trailofbits/rfc8785.py) rather than
a new canonicalizer. It checks schema validity, fictional record shapes, owned
digests, digest construction, membership and selected cross-record/time relations.
Negative relation cases recompute record digests and update digest references so
they fail for the intended inconsistency rather than stale hashes.

Every external fixture record is synthetic. Checking its bytes/digest is not
validation under an unmaterialized authorization, domain, guard, status or clock
contract. Each positive set is a separate scenario, not one database history.
The checker neither executes the full lifecycle nor produces production-admissible
evidence. No real clocks, PostgreSQL, authority grants or private records are used.

Next: review these exact draft bytes and tests, then complete the separately
owned prerequisites and binding stages in #26 §21 before any promotion or runtime
implementation. The source approvals remain unchanged and OFARM2 #396 stays parked.
