# OFARM partner-output surface governance boundary closure note v0.1

Date: 2026-04-19  
Status: accepted closure companion artifact (colocated with the compiled-output taxonomy and interoperability/runtime-surface RFC family)  
Scope: clarify when partner-facing compiled-output channels remain implementation-local support identities versus when they should be promoted into a governed RuntimeSurfaceContract or equivalent deployment-facing contract lane

---

## Decision

This note closes the next bounded hostile-integrator seam without reopening RC2.1 baseline law, without promoting any new runtime-surface contract family by default, and without forcing every recipient-facing compiled-output channel to become a governed runtime-surface artifact.

For the current package:

- `RuntimeSurfaceContract` remains the default governed family for partner-facing APIs, event feeds, query façades, discovery surfaces, and similarly stable externally consumed boundary lanes
- `PassportView`, `DocumentAssembly`, and `SubmissionAssembly` semantics remain governed primarily by the compiled-output taxonomy, publication request/result boundaries, and output metadata contracts
- recipient-specific compiled-output channels that are only format/rendering/delivery adapters do **not** become governed runtime-surface artifacts merely because they produce JSON, CSV, PDF, or XML
- current package-local partner-output channels may remain explicit implementation-local support identities where the stable semantic meaning is already carried by governed output artifacts and publication traces
- later promotion into a governed `RuntimeSurfaceContract` or equivalent contract lane remains possible, but only through explicit OFARM governance work when the promotion threshold is actually crossed

## Boundary rules

### 1. RuntimeSurfaceContract remains a boundary-contract family, not a universal publication bucket

The accepted interoperability/runtime-surface RFC and Platform RC2.1 already position runtime surfaces around partner-facing API/event/query/discovery boundaries.

That family should not silently expand into a bucket for every buyer dashboard payload, report export, dossier file, or submission package emitted by an implementation.

### 2. Governing meaning for compiled outputs usually lives above the adapter format

For partner-facing compiled outputs, the first governing questions are normally:

- is the result a `PassportView`, `DocumentAssembly`, or `SubmissionAssembly`
- which scope, twin, profile, recipient, and authority path apply
- whether the output is live/recomputable or frozen/attested/filed
- which publication gate outcome, evidence posture, and trace basis justify delivery

If those questions already determine the meaningful behavior, a format adapter identity alone does not require promotion into a governed runtime-surface lane.

### 3. Format or recipient variation alone is not a promotion trigger

The following do **not** by themselves trigger runtime-surface promotion:

- the same governed output being rendered as JSON, CSV, PDF, XML, or another carrier
- recipient-specific shaping of a governed `PassportView`
- export of a governed `DocumentAssembly` to a local delivery channel
- implementation-local file naming, dashboard response shaping, or partner adapter ids

### 4. Promotion threshold for partner-output channels

A partner-output channel should be promoted into a governed `RuntimeSurfaceContract` or equivalent deployment-facing contract lane only when the channel has become a stable external boundary in its own right.

The promotion threshold is crossed only when most of the following are true:

- the channel has a stable externally consumed boundary identity beyond a local adapter name
- the channel publishes or depends on stable service-description, schema, namespace, or protocol-boundary artifacts that matter operationally
- compatibility/versioning promises for that lane must be governed independently of the underlying output artifact family
- delivery/auth/idempotency behavior of the lane must be governed across deployments or packs
- runtime-surface collision or merge analysis materially depends on that lane
- partner integrations rely on that lane as a durable contract rather than as implementation-local output transport

### 5. Current package posture

For the current package lane:

- `NGSI_LD_PARTNER_EXPORT` is already represented by a governed runtime-surface lane through `surface:ngsi-ld-export:v1` and `surface-contract:ngsi-ld-export:v0.2-draft`
- `PARTNER_DASHBOARD_JSON`
- `PARTNER_ADVISORY_CSV`
- `PARTNER_COMPLIANCE_PDF`
- `PARTNER_DOSSIER_JSON`
- `PARTNER_SUBMISSION_XML`

remain explicit implementation-local support output channels in the current package

This means they stay visible and traceable, but they are **not** modeled as governed runtime-surface artifacts in the current release lane.

### 6. Submission channels are the main future-promotion candidate, but not by default

A submission-shaped output may later justify a governed runtime-surface or equivalent contract lane if OFARM adopts a stable filing gateway, schema-bound exchange endpoint, or long-lived delivery namespace that external partners depend on as a contract.

A generated XML payload or file-delivery adapter alone is not enough.

## What this note does not do

This note does not:

- demote or weaken the compiled-output taxonomy
- redefine `PassportView`, `DocumentAssembly`, or `SubmissionAssembly`
- promote dashboard/CSV/PDF/dossier/submission adapters into active runtime-surface contracts by itself
- require every partner-output channel to appear in the Capability Manifest
- create a new constitutional output-channel artifact family
- claim that implementation-local partner-output telemetry becomes active law

## Practical implication

The package can now say all of the following clearly:

- governed runtime surfaces remain bounded to true external boundary lanes
- governed compiled-output meaning still lives in the output taxonomy and publication traces
- current package-local dashboard/CSV/PDF/dossier/submission channels are traceable and explicit without being over-promoted
- future promotion remains possible only where a channel becomes a stable external contract lane rather than a local rendering/delivery adapter
