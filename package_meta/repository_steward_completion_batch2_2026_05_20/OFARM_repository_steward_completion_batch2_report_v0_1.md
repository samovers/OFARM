# OFARM repository-steward completion Batch 2 report

Generated: 2026-05-20T12:00:00+02:00

This patch completes the structural remediation that Batch 1 only quarantined by metadata.

## Key changes

- Physically moved root `reviewed_*` snapshots into `archive/review_holding/OFARM_review_holding_snapshots_2026_05_20.zip`.
- Physically split `04_implementation_and_conformance/` into controlled lane folders.
- Physically renamed 77 implementation/conformance schema copies with `__non_active_copy.json`.
- Added direct `derivedFrom` and `doNotCiteAsIndependentSource` markers to generated duplicate maps.
- Removed legacy snake_case compatibility keys from `folder.status.json` files.
- Updated guardrails to fail if these structural fixes regress.

Active OFARM law was not changed.
