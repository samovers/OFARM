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
actual pinned report schema before emission.

Errors are separate envelopes with `componentResult: UNAVAILABLE`, an error
layer/code/target and, for schema failures, an exact witness. They do not claim
input digests or successful schema checks. Missing Python libraries produce a
dependency error. Caller argument errors use the standard command-line usage
diagnostic.

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

The committed fixture has 74 controls: 17 MATCH, 26 MISMATCH and 31 expected
UNAVAILABLE outcomes. The repository validation suite includes this invocation
once, alongside its fourteen existing commands. Python's protective digit limit
is preserved; parser value rejection reports `JSON / PARSER_VALUE_REJECTED`
without claiming successful parsing or digests. Mismatch controls complete both
schema/local preflights
and compute fresh digests; stale hashes cannot substitute for the intended
mapping failure. Expected mismatch sets and schema witnesses are explicit in
the fixture, not calculated from the mapping table. Two report-schema controls
deliberately alter a completed report to demonstrate rejection of full-domain
or domain-payload claims; they are report-schema controls, not input failures.

No fictional dependency schemas are used. Fixture values are fictional and
format-valid under actual schemas; positive cases do not prove foreign facts.
This component is integrated above PR44 commit
`898396f9612541ae0305d9d5935890776978f630`. Its manifest pins the shared input
helper bytes from that commit, including the reviewed inactive-input extension.
The operation schema remains the exact PR42 schema; the result schema remains
the exact PR41 schema. Older manifests and source pins retain their original
lineage. This component does not edit those upstream components.

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

Next: review the frozen combined candidate and final suite evidence before the
coordinator releases the separate draft PR above the PR44 input branch.
