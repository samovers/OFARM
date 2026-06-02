# OFARM Phase 7 — Request Lifecycle State Model v0.1

## Candidate lifecycle states

- `OPEN`
- `IN_PROGRESS`
- `SATISFIED_PENDING_REVIEW`
- `SATISFIED_ACCEPTED`
- `WAIVED_BY_REVIEW`
- `EXPIRED`
- `SUPERSEDED`
- `REJECTED`
- `DUPLICATE_COLLAPSED`
- `BLOCKED_INVALID`

## Lifecycle constraints

- `SATISFIED_ACCEPTED` requires an acceptable satisfaction trace and, where required, human or governed review.
- `WAIVED_BY_REVIEW` requires a review basis and does not imply the missing evidence existed.
- `EXPIRED` does not imply the risk disappeared.
- `DUPLICATE_COLLAPSED` must preserve references to collapsed requests.
- `BLOCKED_INVALID` must identify the invalid blocker, missing basis, or noise-control reason.
