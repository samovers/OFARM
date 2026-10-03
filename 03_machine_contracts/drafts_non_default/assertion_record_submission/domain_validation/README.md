# Offline operation mapping integrity

This draft component compares supplied operation-intent and AssertionRecord
result bytes against the deterministic mappings in PR23. It is directly usable
as a file-based command or Python library. Its primary trust boundary is
**AssertionRecord operation intent-to-result mapping integrity**.

It validates the actual pinned PR42 operation intent schema, PR41 result and
operation body schemas, and their existing local consistency checks. One
manifest table then checks the complete settled copy/derivation/absence surface:
identity, subject, sole anchor, relationship-proof copy, act time/posture/evidence,
subject time, complete body and evidence array, operation posture and performer,
conditional actorship/performer evidence, and correction-binding copy. Existing
schemas retain constants, conditional presence, branch absences and unknown-field
rejection. Source-fixed operation subtype selection is explicit in the table.

Each result is a **subcheck**, not a full AR/PC verdict. Matching proof bytes do
not establish their truth or admission. Authorization Party/rule, relationship
and identity truth, trusted act/time, foreign evidence, prior history, event
compatibility, transaction and admission remain unavailable.

## Use

From the repository root, with Python, jsonschema, referencing and rfc8785:

```sh
python3 04_implementation_and_conformance/conformance_runners/ofarm_assertion_record_domain_mappings_v0_1.py --intent /path/to/intent.json --result /path/to/result.json
```

Exit 0 means all named comparisons match. Exit 1 means at least one comparison
differs. Exit 2 means input, schema, dependency or local consistency checks could
not complete. A completed MATCH or MISMATCH report includes freshly calculated
whole-value digests, exact schema bindings, comparison pointers/digests and
shared evidence references. Every completed report is validated against the
actual pinned report schema before emission. It fixes pointers, evidence forms,
schema bindings, aggregate/reference outcomes, presence/digest membership and
AR traceability. An internal check also compares digest strings with row
outcomes; standard JSON Schema cannot express that cross-property equality.
Neither check authenticates a supplied report or its whole-input digest. Re-run
`verify` with original bytes to substantiate a report.

Each row names its `obligationIds`; `arTraceability` accounts for all 29 PR23
AR IDs through comparison references, schema enforcement, other-action scope
or explicit unavailable reasons. These are explanatory links, not full AR
dispositions. `eventBindingPresent` records supplied binding presence;
`eventAssociation` is UNAVAILABLE when present and NOT_SUPPLIED when absent.
It never emits full-contract N/A or a family/compatibility verdict.

Errors are separate envelopes with `componentResult: UNAVAILABLE`, an error
layer/code/target and, for schema failures, an exact witness. They do not claim
input digests or successful schema checks. Missing Python libraries produce a
dependency error. Missing caller files use `INPUT / FILE_UNAVAILABLE`; missing
manifest/schema/helper files retain `DEPENDENCY / FILE_UNAVAILABLE`. Caller
argument errors use the standard command-line usage diagnostic.

For library use, add the conformance runner directory to the normal Python
import path and call:

```python
from ofarm_assertion_record_domain_mappings_v0_1 import verify, MappingError

report = verify(intent_bytes, result_bytes)
```

`verify` accepts UTF-8 bytes and returns MATCH/MISMATCH, or raises `MappingError`.
`error.as_dict()` provides the same error envelope as the command. Each call
loads fresh pinned dependencies. For multiple comparisons against one immutable
loaded snapshot, use `Component().verify(intent_bytes, result_bytes)`.

## Reproduce component checks

```sh
python3 04_implementation_and_conformance/conformance_runners/ofarm_assertion_record_domain_mappings_v0_1.py
```

The committed fixture has 147 controls: 22 MATCH, 26 MISMATCH and 99 expected
UNAVAILABLE outcomes. Original 74 cases and their outcomes are unchanged. The
added controls cover impossible dates on each input and both inputs, valid leap
dates, hostile reports, event presence, caller file errors and rejection of
another otherwise valid assertion branch. The repository suite includes this
invocation once, alongside its fourteen existing commands.

Python's protective digit limit remains; parser value rejection reports
`JSON / PARSER_VALUE_REJECTED` without successful parsing or digest claims.
Mismatch controls complete schema/local preflights and compute fresh digests.
Expectations are explicitly authored, not calculated from the mapping table.
Original full witnesses are preserved; added schema controls name their target,
instance path and keyword. Report corruption controls test output consistency,
not original-input or foreign-fact truth.

The component registers the pinned PR41 Gregorian calendar check on its own
format checker. Behavior is the same with and without optional
`rfc3339-validator`; that package is not required. February 30, non-leap
February 29 and year zero fail schema preflight rather than producing successful
schema claims or later local-consistency errors.

No fictional dependency schemas are used. Fixture values are fictional and
format-valid under actual schemas; positive cases do not prove foreign facts.
This component is integrated above PR44 commit
`6457009520257f8751ca03caa4b0704cf92160a7`. Its manifest pins the shared input
helper bytes from that commit, including its inactive-input extension.
The operation schema remains the exact PR42 schema; the result schema remains
the exact PR41 schema. Older manifests and source pins retain their original
lineage. These are byte-pinned dependencies, not claims of human review or formal
GitHub approval. This component does not edit those upstream components.

`AR_TYPE.derived_constant` is always MATCH in a completed operation report:
preflight has already constrained the subtype and selected body. A wrong
subtype returns `UNAVAILABLE / SCHEMA`, exit 2, with no comparison rows. It is
rejected, not accepted or represented as a complete PR23 FAIL payload. DESIGN
explains the source/disposition distinction and review limitations.

## Claim limits

`fullDomainValidation` is always `UNAVAILABLE`. The report has no
`overallDisposition` or `protectedEffectContractDigest` and cannot serve as
PR23's complete domain payload or PR43's `domainPayload`. An entirely matching
report does not authorize a write, prove a full AR/PC rule, admit a correction,
establish uniqueness, or create accepted execution/current state. Nothing here
changes runtime, authorization inputs, transaction enforcement or default
selection.

The eventual real payload must adopt PR43's fixed four subject fields, complete
AR/PC dispositions and contract-owned prerequisite graph. The mapping manifest
is a component description, not the complete protected-effect contract. See
[DESIGN.md](DESIGN.md) for source ownership, construction order and limits.

Next: review the correction, integrate the separately reviewed PR44 dependency
at its exact commit, then verify the final stack before publication.
