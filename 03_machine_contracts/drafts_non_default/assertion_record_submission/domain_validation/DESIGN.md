# Deterministic operation mapping component

Primary trust boundary: **AssertionRecord operation intent-to-result mapping
integrity**. One separate draft PR owns the offline verifier, mapping table,
report schema, focused controls and mechanical integration. Full domain
evaluation, authorization inputs/context, transactions, persistence and runtime
admission remain outside it.

## Source and capability

PR23 at `6c5c6eb754baecfa38b7e364fc3d0318ae1ad89f`, §§5.1–5.6, 7.2 and 8.1–8.3,
fixes the deterministic operation copy, derivation and absence surface. The
component uses actual PR41 `bfd15b98c48f70e679824005c62adf4241dd8b22` and PR42
`471cb1ef20ffde56b1437949975a4c6c86c59dd5` schema bytes; PR43
`546f831f495d60b45e93b55fbaaa601b1374ad7e` fixes the future payload interface.
The final integration base is PR44
`6457009520257f8751ca03caa4b0704cf92160a7`, on
`contracts/inactive-assertion-inputs-v0-2`. The new manifest pins the shared input
helper from that exact commit. Its byte-pinned inactive-input extension is an
upstream dependency; this operation comparator still selects only
`EI_OPERATION_ASSERTION_V0_2`. Actual intent/result schema bytes remain those of
PR42/PR41. Older component manifests and source pins retain their historical
lineage.

The concrete problem is that separately valid intent/result objects can disagree
even if their own hashes and a relabelled shared trace are consistent. This
callable tool compares those supplied objects now; it is independently usable
without constructing a runtime path or claiming missing owner proofs.

## One source for each check

`ASSERTION_RECORD_DOMAIN_MAPPING_manifest_v0_1.json` owns the declarative
cross-document table. The runner verifies its exact hash before reading it.
The manifest pins schema and helper file bytes. Prior helper code executes only
after byte verification, with its standalone test main disabled. It supplies
strict JSON/pointer handling, a pinned local schema registry and existing local
consistency checks. No network or latest lookup is permitted.

Schemas own constants, required members, conditional presence and branch
absences. The evaluator does not duplicate that rule logic. Its source-fixed
`AR_TYPE.derived_constant` uses PR23's selected operation row. The authorization
effect token `OPERATION_ASSERTION`, result subtype `OPERATION_CLAIM_ASSERTION`
and commit-class token `OPERATION_CLAIM` are distinct values, not free aliases.

PR23 section 13 says an incorrect subtype fails the owning contract. This
component has no complete contract/payload; it rejects the input before
comparisons, returning UNAVAILABLE / SCHEMA and exit 2. The original
`wrong_result_subtype` case preserves its exact witness. A second case supplies
an otherwise valid structure record and proves rejection by the selected
operation-body preflight. No completed report can contain AR_TYPE MISMATCH;
the report schema fixes that row to MATCH and its exact constant digest. This
documents the rejection layer without weakening preflight or claiming a full
domain FAIL payload. An error/UNAVAILABLE must never be treated as admission.
No source conflict requiring new domain meaning was found in this limited
classification repair.

`AR_ID.copy` compares `/effectSubject/subjectRef` with `/assertionRecordId`.
`AR_EFFECT_SUBJECT.kind_and_id` reuses that comparison and the already validated
input subject-kind constant. No separate proposed-ID input exists.
`AR_BODY.copy` compares the whole `/assertionBody`; the operation-payload coverage
row refers to that evidence rather than running another partial comparison.

Other rows copy the complete subject, sole `/resources/0/scope` to the sole
result anchor, relationship-proof array, assertion time/posture/evidence,
subjectTime, evidence array, operation posture/performer, conditional arrays
and correction binding. Optional-copy rows require symmetric presence or
absence. Required-copy rows cannot match two absent values.

Equality uses complete RFC8785 JCS/SHA-256 values, with no member exclusions.
Object order may differ. Strings, Unicode values and array order do not change.
No normalization, sorting, trimming, schema repair or generated expected truth
occurs. Input bytes decode into fresh objects and are never mutated.

## Report and errors

Schema validation of intent, complete result and selected operation body precedes
all reported comparisons. Existing local checks enforce interval order, local
prospective collisions, proof presence relative to local subject/anchor
equality, correction self-reference and BODY_TIME equality. Those checks retain
their original limited meanings; they do not establish foreign facts.

The component registers PR41's existing `timestamp_ns` calendar check as
`date-time` before constructing all validators. Reusing the helper without its
standalone main must not omit this registration. Impossible dates fail schema
preflight on both sides with or without optional `rfc3339-validator`. No new
qualifier rule or timestamp normalization is introduced.

Malformed JSON, non-interoperable canonical values, missing/changed dependencies,
schema failures and local consistency failures produce distinct stable error
layers/codes. The error envelope contains no claimed input/result digests or
completed preflight. Schema errors identify target, instance path, schema path
and keyword (`falseSchema` for a boolean-false schema).

After successful preflight, the report includes every table row, exact compared
pointers/value digests or shared evidence references, fresh whole input/result
digests and schema-file bindings. Its own pinned schema checks the closed
report, row order/IDs, literal pointers/references, required evidence by mode,
exact schema bindings, presence/digest membership, finite reference-outcome
relationships, aggregate and unavailable full-domain posture before emission.
The internal report check additionally rejects MATCH with unequal compared
digests and MISMATCH with equal digests. Draft 2020-12 cannot compare arbitrary
sibling strings or recompute input hashes. This output check is not an external
report-admission API; a consistently forged standalone report is not evidence
of its claimed original bytes. `verify` computes actual input/result digests.
MATCH means only all named subchecks match; MISMATCH preserves the same clear
preflight evidence and names every disagreement.

The report never uses full AR/PC PASS or dependency-bound `NOT_EVALUATED` as a
substitute for missing semantics. PR23 §11.2 owns those complete payload
dispositions and their enumerated prerequisite graph. There is no
`overallDisposition`, contract-digest placeholder, authorization flag, or
user-selectable fallback policy.

The manifest's `arTraceability` lists every source AR ID once, including
other-action obligations, without domain dispositions. Rows also name source
obligation IDs. The report schema pins this explanatory map and the permitted
links. Schema-only enforcement and unavailable semantics can coexist for one
obligation. Event binding presence is visible, but compatibility remains
unavailable; absence is NOT_SUPPLIED rather than full-contract NOT_APPLICABLE.
This inventory cannot make the complete future domain payload mechanical.

The manifest lists fields deliberately not copied: resource tenant context,
authorization-resource proofs, prospective effect-subject proofs and the event
binding. The result's assertedByPartyRef cannot supply its own authority source.
PR23 sections 5.6, 6.1 and 7.3 own those distinctions. Such a field can change
the complete input digest while copy rows still MATCH; its separately owned
semantics remain unavailable.

## Remaining owner obligations

Copying relationship proof is not validating the relationship. Copying act/time
fields is not trusted online injection or offline evidence admission. Copying
correction lineage proves no prior committed visibility, creation context,
boundary/twin or target compatibility. Performer evidence remains
`NOT_EVALUATED_BY_AUTHORIZATION`. The real canonical authorization Party and
selected rule are unavailable; the result cannot supply its own expected
assertor. Event association has no result copy destination and requires actual
Event Ingress and domain compatibility evidence.

All 20 PC semantic obligations and full AR semantic closure remain unavailable.
In particular, validated committed bytes, immutable inputs, no unbound effects,
no current-state effect, atomic transaction handoff and global uniqueness need
their actual execution/storage owners. PR23's pre-T temporal comparison never
invents future receipt/attempt or physical-time evidence.

Three body definitions exist, but inactive structure/compliance input closure
and the complete domain contract are separately owned. This operation-only
component does not claim that all three actions are materialized or admitted.
The complete fixed contract ID is not assigned to this component manifest.

## Future F1 interface and delivery

A later complete real payload must require `proposedResultDigest`,
`effectIntentDigest`, `protectedEffectContractDigest` and the complete
`selectedActionBodySchemaBinding` for both PASS and FAIL, under PR43. Freeze
schemas first, then the real contract (excluding exactly its own top-level
`contractDigest` for its hash), owner inputs, complete payload, shared trace,
and later transaction evidence. The contract binds the payload schema, not a
future payload digest. This comparison report cannot impersonate that payload.

The focused committed controls exercise schema-valid unequal inputs, complete
body/string/array identity, optional presence in both directions, actual schema
witnesses, dependency byte failures and explicit claim limits. A matching
different-assertor control demonstrates that the tool does not invent authority.
Report corruption controls test closed evidence forms, finite relationships
and internal compared-digest consistency. They do not prove original bytes or
foreign facts. All original 74 controls remain unchanged; added expectations
are explicit and are not derived from the mapping table.

## Dependency and review provenance

Commit, byte-count and SHA-256 pins are inspectable provenance, not approval.
The [pinned PR44 helper](https://github.com/samovers/OFARM/blob/6457009520257f8751ca03caa4b0704cf92160a7/04_implementation_and_conformance/conformance_runners/ofarm_authorization_effect_intents_v0_2.py)
and [pinned PR43 future envelope interface](https://github.com/samovers/OFARM/blob/546f831f495d60b45e93b55fbaaa601b1374ad7e/03_machine_contracts/drafts_non_default/authorization_finalization_evidence/protected_effect_validation/OFARM_ProtectedEffectValidationTrace_envelope_schema_v0_1.json)
can be inspected at their exact commits. No claim is made that either head has
independent human review or formal GitHub approval. Local AI checks are neither
and are not needed to reproduce the committed fixture. No unrelated local
review histories are exported as public evidence.

The [available PR45 author-account discussion](https://github.com/samovers/OFARM/pull/45#issuecomment-5971339050)
reports B1, F1–F4 and P1. Its detailed F1/F2 sections and part of F3 are missing
from the posted body. Report counterexamples used for this correction were
independently derived from the existing component contract and output; they
are not recovered reviewer examples. The repair covers those supported
invariants, not an unseen exhaustive list. The [PR44 author-account discussion](https://github.com/samovers/OFARM/pull/44#issuecomment-5971345212)
also does not establish independent human approval. Unsupported descriptions
of dependencies as “reviewed” have been replaced by exact pinned provenance.

This non-default offline component needs no runtime construction exception.
Any OFARM2 runtime use remains subject to PR11 §24.2, PR23 §18 and a separately
approved Phase A/candidate-consumption mechanism with complete reviewed inputs.
Current/default promotion, commit/push/PR publication and merge are not inferred
from a component PASS. The coordinator controls the held publication steps.

Next: independently review the correction, integrate the separately reviewed
PR44 dependency, then verify the final stack before coordinator publication.
