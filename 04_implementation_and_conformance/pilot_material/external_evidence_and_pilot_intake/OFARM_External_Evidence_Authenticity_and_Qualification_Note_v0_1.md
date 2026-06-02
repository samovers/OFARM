# OFARM external evidence authenticity and qualification note v0.1

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: bounded authenticity and qualification rules for real external evidence so repo-authored rehearsal artifacts cannot be mistaken for qualifying pilot proof

---

## Why this note exists

The package already had:
- a live evidence intake lane
- a pilot handoff kit
- a rehearsal lane
- a reviewer-side decision lane

The remaining ambiguity was narrower.
A production-shaped JSON could still look reviewable even when it was only a repo-authored rehearsal packet or a copied template with cleaned placeholders.

This note closes that ambiguity.
A packet must now carry an explicit authenticity envelope and a bounded qualification claim before it can count as live external evidence.

## Separate the three questions

1. **shape** — is the artifact in the correct lane and structurally complete enough?
2. **authenticity** — is the artifact attributable to a real deployment or accountable production approval rather than a repo-authored rehearsal packet?
3. **qualification** — what narrow claim is the artifact allowed to support?

A packet can satisfy shape while still failing authenticity.
A packet can satisfy authenticity while still supporting only a narrow support-evidence claim.

## Required authenticity envelope

Each real artifact in `live_evidence_packets/` should now carry an `authenticityEnvelope` with at least:
- `captureMode`
- `repositoryAuthored`
- `redactionApplied`
- `attestedByRef`
- `attestedAt`
- `artifactDigest`
- `sourceRealityClass`

Minimum meaning:
- `repositoryAuthored` must be `false` for any artifact that is later counted positively
- `sourceRealityClass` must describe a real deployment, real live-field run, or accountable production approval, not rehearsal
- `artifactDigest` must identify the deployment-controlled or operator-controlled artifact being reviewed
- `attestedByRef` and `attestedAt` must make the capture accountable

## Required qualification claim

Each real artifact in `live_evidence_packets/` should now carry a `qualificationClaim` with:
- `claimKind`
- `claimScopeRef`
- `nonClaims`

Use the narrowest valid `claimKind` for the lane:
- `GOVERNED_RUNTIME_SURFACE_LIVE_DEPLOYMENT_EVIDENCE`
- `PARTNER_OUTPUT_SUPPORT_TELEMETRY`
- `LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY`
- `DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE`
- `PRODUCTION_PROMOTION_APPROVAL_RECORD`

`nonClaims` is required so future reviewers do not silently widen what a packet proves.

## Rehearsal boundary

Rehearsal packets under `pilot_intake_rehearsal/` stay useful for shape inspection.
They are now expected to mark themselves explicitly as repo-authored and non-qualifying.
Copying a rehearsal packet into `live_evidence_packets/` without creating a real deployment artifact must not pass the intake gate.

## Reviewer consequence

A positive reviewer decision now requires more than a file in the right folder.
For any positive decision, the reviewer should be able to confirm at minimum:
- the reviewed artifact has an authenticity envelope
- `repositoryAuthored` is `false`
- the decision record repeats the artifact digest and claim kind accurately
- the positive decision does not exceed the artifact's explicit `claimKind` and `nonClaims`

## Non-claims

This note does **not**:
- fabricate pilot proof
- make `RuntimeSurfaceContract v0.2` the default
- promote implementation-local partner-output channels into governed runtime-surface law
- promote same-standard bridge draft pairs without the full real evidence class set
