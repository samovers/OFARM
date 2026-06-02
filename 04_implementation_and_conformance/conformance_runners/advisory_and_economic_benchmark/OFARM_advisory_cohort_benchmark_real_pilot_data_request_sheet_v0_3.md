# OFARM advisory cohort benchmark real-pilot data request sheet v0.3

## Rule zero

Do **not** ask the tenant cohort for data just because software could theoretically ingest it.
Ask only for what the bounded benchmark pilot requires.

## Needed for fertilizer product-class benchmark

Need:
- 5+ contributing participants or farms
- explicit benchmark contribution share-grant ref per participant
- reviewed extract ref per contribution
- evidence ref per contribution
- normalized fertilizer product-class ref
- optional exact product ref if captured
- normalized quantity
- normalized unit code
- amount in EUR (or one declared currency with conversion basis)
- benchmark window
- request-history record or exported fingerprint log for at least one viewer

Do not ask for:
- raw invoice PDFs in the pilot packet
- line-by-line GL export
- whole-farm accounting export
- payroll, bank details, or tax identifiers
- fixed-cost allocations
- free-form unredacted participant notes

## Needed for seed exact-product benchmark

Need:
- all the above baseline fields
- exact normalized seed product ref
- exact product comparability basis (same pack/seed-count basis)
- 5+ contributions on the same exact normalized product
- dominance still below the disclosure threshold
- request-history state proving the exact slice is still safe

Do not ask for:
- percentile or distribution analytics
- arbitrary time-series slices
- whole product catalog exports if one exact product is enough

## Needed for revocation/recompute test

Need:
- one contribution eligible at first materialization
- one later revocation event or a realistic simulated revocation record
- old materialization ref
- fresh recomputed materialization ref or equivalent recompute completion marker

## Redaction minimum

Replace with stable redacted refs:
- participant ids
- farm ids
- viewer ids
- share-grant ids if the raw id encodes identity
- extract ids if the raw id encodes identity
- evidence ids if the raw id encodes identity

Remove unless indispensable:
- staff names
- counterpart names where coded refs are enough
- government ids
- bank details
- email addresses
- raw receipt payloads
