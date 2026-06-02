# OFARM submission-gateway promotion and equivalent contract closure note v0.1

Date: 2026-04-19  
Status: accepted closure companion artifact (colocated with the compiled-output taxonomy and interoperability/runtime-surface RFC family)  
Scope: clarify when a submission-shaped output channel should remain an implementation-local adapter, when it should be promoted into a governed filing boundary, and what shape an equivalent filing-boundary contract would need if OFARM later promotes that seam

---

## Decision

This note closes the next bounded hostile-integrator seam without reopening RC2.1 baseline law, without promoting `PARTNER_SUBMISSION_XML` into a governed runtime-surface lane by default, and without creating a new active machine-contract family in the current package.

For the current package:

- `PARTNER_SUBMISSION_XML` remains an explicit implementation-local support output channel
- the governing meaning for the current successful filing path remains the combination of `SubmissionAssembly`, publication request/result boundaries, evidence-sufficiency policy, authorization traces, and no-edit-in-place correction law
- the package now carries an explicit **promotion threshold** for a future governed submission gateway
- the package also carries a **fixture-only candidate shape** for an equivalent filing-boundary contract lane so future promotion work does not have to restart from scratch

## Why this note exists

The partner-output governance-boundary clarification already said that submission adapters are the strongest future-promotion candidate.

That was directionally correct, but it still left two practical questions open:

1. what exact conditions must be true before an XML submission adapter becomes a governed filing boundary rather than a local delivery adapter
2. whether the ordinary `RuntimeSurfaceContract` lane is sufficient once filing-specific receipt, correction, duplicate, and finality semantics become part of the governed boundary

This note answers both without promoting anything by convenience.

## Promotion threshold for submission gateways

A submission-shaped adapter crosses the promotion threshold only when **all** of the following are materially true:

1. the lane has a stable external boundary identity beyond a local adapter name
2. the partner relies on a stable schema, service-description, namespace, or delivery contract for that lane
3. acceptance, rejection, or receipt semantics are operationally meaningful and must be governed
4. duplicate, retry, replay, or correlation-id behavior must be governed beyond ordinary publication metadata
5. correction, amendment, supersession, or successor-filing behavior must be governed at the lane itself
6. compatibility/version promises for the filing lane matter independently of the underlying `SubmissionAssembly`
7. release-bound service-description and deployment-traceability artifacts must name that filing lane directly

A generated XML file by itself is not enough.

## Lane-choice rule after the threshold is crossed

### 1. Use `RuntimeSurfaceContract` when filing semantics are still generic boundary semantics

If the promoted lane can still be governed adequately by the existing runtime-surface posture plus service-description artifacts, then OFARM should continue using the `RuntimeSurfaceContract` family.

That is the right choice when the important governed behavior is mostly:
- stable boundary identity
- transport/binding identity
- version posture
- auth posture
- delivery semantics
- idempotency posture

### 2. Use an equivalent filing-boundary contract only when filing-specific semantics materially exceed the generic lane

A filing-specific equivalent contract lane is justified only when the promoted boundary must also govern semantics such as:
- mandatory acceptance or rejection receipts
- partner-issued filing ids or correlation ids
- duplicate filing resolution rules
- amendment / correction / successor-filing semantics
- finality signals that matter independently of the underlying frozen output metadata
- explicit linkage from filing-lane behavior back to governed publication request/result and submission-correction chains

In other words, OFARM should not create a new filing-boundary contract family unless the filing lane has become more than a runtime surface plus a frozen output.

## Candidate equivalent-lane shape in the current package

The current package does **not** promote such a lane.

It does, however, ship a fixture-only candidate shape under `04_implementation_and_conformance/` so the package can state what would have to become first-class if promotion happens later.

That candidate shape requires at least:
- stable gateway identity
- underlying governed output kind = `SubmissionAssembly`
- explicit boundary binding / delivery namespace
- partner schema or service-description refs
- receipt / rejection / finality semantics
- duplicate / retry / correlation semantics
- correction / supersession / successor-submission semantics
- explicit refs back to governed publication request/result, evidence sufficiency, and authorization trace artifacts

## Current package posture

The current package now says all of the following clearly:

- `PARTNER_SUBMISSION_XML` is still implementation-local support output transport in this release
- the current package demonstrates successful filing and schema-mismatch refusal paths without claiming a governed filing gateway lane
- future promotion requires more than XML generation; it requires a real governed filing boundary
- if promotion later happens, OFARM already has a fixture-only candidate contract shape and service-description stub to anchor that work

## What this note does not do

This note does not:

- promote `PARTNER_SUBMISSION_XML` into the active RuntimeSurfaceContract lane
- create a new active machine-contract family in `03_machine_contracts/`
- change `SubmissionAssembly` semantics
- weaken publication, evidence, freshness, or authority gates
- treat a filed submission as canonical truth by itself

## Practical implication

The package can now distinguish three states cleanly:

1. **implementation-local submission adapter** — the current package posture  
2. **governed runtime-surface filing lane** — only when a stable submission boundary exists and generic runtime-surface semantics are enough  
3. **equivalent filing-boundary contract lane** — only when filing-specific receipt/correction/finality semantics materially exceed the generic runtime-surface family
