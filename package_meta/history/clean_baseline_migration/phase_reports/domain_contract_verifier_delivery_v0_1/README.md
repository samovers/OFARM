# Complete typed-claim contract and verifier Delivery

This packet prepares one canonical OFARM Delivery and its draft PR. The intended
outcome is a callable, deterministic offline verifier for complete typed
AssertionRecord claims across structure, operation and compliance. Its primary
trust boundary is **AssertionRecord domain meaning and validation integrity**.

Start with [PHASE_A.md](PHASE_A.md). This is a design and reviewed-input packet;
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
domain verifier. The candidate's frozen pre-review labels are historical.

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

## Limits

The coverage denominator is the named crop-core and BE/SI/RS/NL source set. It
does not cover every future pack or establish live legal truth. No definition,
schema or source is adopted or promoted by this packet. No owner evidence,
runtime integration, CI activation or merge is established. OFARM2 #392/#396
remain parked and #421 remains separate.

Next: review this Delivery design, then construct the candidate schemas,
contract, verifier and focused controls together in the same draft, keeping
source adoption and actual evidence admission under their existing owners.
