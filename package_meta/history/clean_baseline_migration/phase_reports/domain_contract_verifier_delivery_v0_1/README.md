# Complete typed-claim contract and verifier Delivery

This packet prepares one canonical OFARM Delivery and its draft PR. The intended
outcome is a callable, deterministic offline verifier for complete typed
AssertionRecord claims across structure, operation and compliance. Its primary
trust boundary is **AssertionRecord domain meaning and validation integrity**.

Start with [PHASE_A.md](PHASE_A.md) and the [third review amendment](review-amendment-03/INTEGRATION.md). This is a design and reviewed-input packet;
the new schemas, protected-effect contract and verifier are not implemented.
They belong in this same PR. Existing candidate code inherited from PR45 does
not establish completion of the new capability.

The intended base is `contracts/operation-domain-mappings-v0-1` at
`2110f6d78451b50712264dba87d0b8989f134907`. Canonical main at preparation was
`4a3d88ea6eff4b3f8a2c521dc621595cbfd1657b`. The stack keeps the existing
PR41–45 capabilities outside this Delivery's diff. Base changes require affected
dependency and diff verification; stacking transfers no approval or readiness.

## Reviewed input custody

[INPUT_MANIFEST.json](INPUT_MANIFEST.json) binds the included files to their
original source bytes. All 48 members of the original frozen-03 snapshot were
verified before copying. Its manifest SHA-256 is
`7aa1ff8ef084a88808717b93f23b83c06c5bc74801ae46cfae6d7fadb92384fc`.

The fifteen substantive domain/canonical JSON files are byte-identical copies.
They preserve all 99 definitions, 42 requirements and 23 whole-claim examples.
The final [inventory review](inventory-review/review-03.json) closes candidate
completeness with zero Blockers; its [verification record](inventory-review/verification-03.json)
records 946 passing checks, including 42 focused cases. These prior recorded
checks concern inventory, rendering and provenance; they did not run the future
domain verifier. The candidate's frozen pre-review labels are historical. The original example
renderings are also historical after the review amendment: the corrected
projection and examples are separately versioned construction inputs, preserving
all 23 domain meanings and all event/measurement coverage.

Only two provenance copies have transport changes: absolute workstation paths
in the final review and the independent requirement-source pins were replaced
with portable references. Findings, definitions, source revisions and hashes
were preserved. The manifest records both original and copied hashes and the
exact transformation. The original snapshot manifest and seven-input register
remain exact historical records; their source-relative paths describe that
original snapshot, including unbundled historical files. They are not a claim
that every historical builder or earlier review is installed here.

Historical builders, repair scripts and old review rounds are deliberately not
installed as new verifier code. The input copies are evidence for this design,
not a second editable vocabulary authority. Construction will produce one
owned definition package with an explicit mapping to these frozen rows.

## Review amendments

The public reviews of PR47 at `e93cad876645799789956311ea091e82064cf981`
identified online rendering ownership, offline self-attestation cycles, nested
evidence membership and example-coverage gaps. The amendment records their
resolution, the work owners' source reasoning and review of the exact pinned
dependency heads. It is candidate design work, not human semantic adoption.

The first corrected claim projection excludes the metadata authenticating this
assertion act. That metadata stays fully governed by its existing owner fields
and checks. Domain supporting evidence, complete event/measurement meaning and
exact body copying remain required. The historical originals and INPUT_MANIFEST
are unchanged. The [L01 resolution](review-amendment/source-pin-resolution.json)
selects the byte-identical frozen coordination copy rather than its changed
working path; the earlier 946-check report remains historical evidence.

The focused amendment checks establish rendering, custody and design-example
behavior only. The registered repository suite remains a regression check of
inherited components; it does not validate this packet or execute a new full
domain verifier.

The next review at `8e86208f96756b8f271f490696e6aa7cf23605fe` closed those
findings and identified B2 (technical event association rendered into the
record) and F4 (a measured criterion operand without a source binding). The
[second amendment](review-amendment-02/README.md) removes the complete technical
association object from the projection while preserving the optional intent
binding, every event compatibility obligation and trace evidence. It also
requires explicit measurement source/pointer and independently pinned criterion
expectations before citation membership can pass. Domain and Event Ingress
owner responsibilities remain unchanged.

Every original input and first-amendment file remains byte-identical. Earlier
projections/examples and check results are historical construction evidence,
superseded as current construction inputs by the newest amendment. The first AMENDMENT_MANIFEST's two
relatedDesignFiles hashes resolve at its exact source commit `8e86208`, where
that Phase A/README version lives; they do not describe the current documents.
The second manifest records that earlier historical selection; its own related
design hashes resolve at `1a2583d`. The [third integration record](review-amendment-03/INTEGRATION.md) and manifest
bind the current design documents and record both historical source commits. Historical checks must
not be presented as validation of the latest construction inputs.

The reviews at `1a2583d24aa7d280e257e2d54d1c7c3708b623b6` accepted B2, F4 and
the bounded F5 commit-class correction, and identified two follow-ups: unchecked
quantity provenance/lexical meaning (F6), and malformed required source objects
that could pass or raise an exception. The [third amendment](review-amendment-03/INTEGRATION.md)
adds explicit scalar-source and criterion-owner bindings, compares closed
qualifiers and selected lexical values, and returns structured errors for
malformed measured sources, rate sources and required qualifications.

W05 explicitly models a human transcription of a lab report and an independently
authored fictional human criterion. A lab result does not automatically mean
machine-reported, and a fictional criterion does not establish a statutory label
limit. The limit, threshold, censoring and INDETERMINATE outcome remain unchanged;
new source links and exact text are versioned. The 24 other whole-claim examples
and all earlier packet files remain unchanged. Current checks must exercise the
corrected examples together with all inherited event and measurement controls.

A fresh local review at `37d680d` found two residual gaps in the first amendment-03
checkpoint: an unenforced independent quantity-source digest and result-tag-driven
scalar guards. The [bounded owner correction](review-amendment-03/review-repair-01/FIX01_DECISION.md)
adds exact source pins, profile-selected required roles and 532 regression controls.
All 25 candidate examples remain byte-identical to that checkpoint. Current
validation and custody are described in the integration record; the original
owner README, reports and manifest remain historical records of `37d680d`.

## Limits

The coverage denominator is the named crop-core and BE/SI/RS/NL source set. It
does not cover every future pack or establish live legal truth. No definition,
schema or source is adopted or promoted by this packet. No owner evidence,
runtime integration, CI activation or merge is established. OFARM2 #392/#396
remain parked and #421 remains separate.

Next: review this Delivery design, then construct the candidate schemas,
contract, verifier and focused controls together in the same draft, keeping
source adoption and actual evidence admission under their existing owners.
