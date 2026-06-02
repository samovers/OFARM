# CP9 fixture plan

## Positive fixtures

- One bundle covering eleven farmer-value scenario families.
- Display snapshots for daily brief, request, and buyer share preview.
- Dispute reconstruction timeline.
- Sharing/revocation examples.

## Negative fixtures

- Hidden stale advisory daily brief.
- Request spam without burden, relevance, or dedupe.
- Redaction leak in summary text.
- Offline capture labelled accepted before sync review.
- Incomplete dispute reconstruction timeline.
- Premature farmer UX readiness claim.

## Runner checks

The runner checks that positive scenarios preserve visible qualification, request-layer weakness, offline/sync labels, sharing/revocation checks, advisory world-model boundaries, dispute timeline completeness, and no readiness claims. It checks that negative fixtures are detected.
