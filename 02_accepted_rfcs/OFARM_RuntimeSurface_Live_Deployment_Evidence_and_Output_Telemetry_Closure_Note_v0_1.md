# OFARM RuntimeSurface live deployment evidence and output telemetry closure note v0.1

Date: 2026-04-19  
Status: accepted closure companion artifact (colocated with the runtime-surface and Capability Manifest RFC family)  
Scope: clarify bounded package-local live deployment evidence capture readiness and partner-output telemetry linkage for runtime-surface release lanes

---

## Decision

This note closes the next bounded deployment-facing gap without reopening RC2.1 baseline law, without changing default currentness, and without claiming that package-local runtime-emitted telemetry already qualifies as live deployment evidence.

For this closure lane:

- the release-bundle and service-description artifacts introduced by the earlier runtime-surface traceability waves remain fixture-only by default
- package-local runtime-emitted publication telemetry and partner-surface trace-back records may be linked to governed release-bundle and runtime-surface artifacts as **support evidence**, but they remain non-qualifying until a real deployment evidence packet exists
- package-local capture templates, intake registries, and linkage summaries may be added so future live deployments do not invent ad hoc evidence packets
- partner-output surfaces that are not yet promoted as governed `RuntimeSurfaceContract` artifacts must remain explicitly implementation-local support identities in this lane

## Live-evidence rules

### 1. Qualifying live deployment evidence must bind to one governed release lane

A qualifying runtime-surface evidence packet should bind at minimum to:

- one release bundle
- one manifest artifact
- one deployment scope
- one active artifact set
- one conformance claim set
- one surface identity or explicitly declared implementation-local partner surface
- the service-description refs and runtime binding actually observed for that lane

This keeps future deployment evidence attached to governed OFARM artifacts rather than to loose endpoint or topic strings alone.

### 2. Preview-only surfaces cannot claim live deployment evidence

If a release-bundle surface remains `PREVIEW_ONLY`, that surface may still have package-local docs, examples, and planned-capture templates, but it must not claim live deployment evidence for the current release lane.

### 3. Partner-output telemetry may use implementation-local adapter identities, but the modeling posture must stay explicit

Partner-output telemetry may aggregate on implementation-local adapter surface ids when a governed runtime-surface contract is not yet present.

In that case the telemetry linkage artifact should state explicitly:

- the implementation-local adapter surface ref
- whether a governed runtime-surface identity exists
- whether the partner surface is already modeled in the current release bundle
- whether the telemetry is support-only pending later runtime-surface promotion or explicit long-term implementation-local treatment

This prevents partner-output telemetry from silently masquerading as an already-governed runtime-surface family.

### 4. Package-local runtime-emitted telemetry remains non-qualifying by default

Package-local runtime-emitted publication telemetry, publication gate-sequence records, partner-surface trace-back records, local service-description catalogs, and release bundles remain **non-qualifying** for live deployment evidence unless they are replaced later by deployment-emitted artifacts that satisfy the capture rules.

### 5. Capture templates and intake registries must self-declare non-qualifying posture

Any package-local capture template, registry, or operator note added for this lane must self-declare all of the following until a real deployment artifact replaces it:

- `templateOnly` or equivalent capture-ready posture
- `qualifiesAsLiveDeploymentEvidence: false`
- explicit replacement-only guidance
- explicit non-claim that the artifact changes bridge promotion or baseline runtime authority by itself

### 6. Live evidence and contract promotion remain separate decisions

Even if future live deployment evidence exists:

- that evidence does not automatically promote a previously unmodeled partner-output surface into active runtime-surface law
- that evidence does not by itself change same-standard bridge posture
- any later contract promotion still requires explicit OFARM governance work

## What this note does not do

This note does not:

- promote partner dashboard, CSV, PDF, dossier, or submission surfaces into active runtime-surface contracts by itself
- claim that current package-local runtime-emitted publication telemetry is equivalent to live deployment evidence
- require live endpoint probing inside the package
- reopen RC2.1 architecture
- change same-standard bridge promotion posture

## Practical implication

A package-local hardening lane may now prove all of the following together:

- the current release-bundle lane is ready to receive future live deployment evidence without ad hoc artifact invention
- release-bound surface evidence eligibility is explicit
- preview-only surfaces stay ineligible for live-evidence claims
- current partner-output telemetry can be linked to the governed release lane where that lane exists and can otherwise remain explicitly implementation-local support evidence
- the package can stay honest about what it has prepared versus what it has actually collected
