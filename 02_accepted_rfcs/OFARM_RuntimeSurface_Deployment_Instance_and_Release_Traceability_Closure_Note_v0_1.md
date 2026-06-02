# OFARM RuntimeSurface deployment-instance and release traceability closure note v0.1

Date: 2026-04-19  
Status: accepted closure companion artifact (colocated with the runtime-surface and Capability Manifest RFC family)  
Scope: clarify bounded package-local deployment-instance and release-bound traceability between a concrete deployment lane and the discovery/service-description artifacts published for that lane

---

## Decision

This note closes the next bounded deployment-facing gap without reopening RC2.1 baseline law, without changing default currentness, and without promoting local service-description files into active semantic/runtime authority.

For bounded release-traceability hardening:

- `OFARM_Capability_Manifest_schema_v0_1.json` remains the default current manifest family.
- `OFARM_RuntimeSurfaceContract_schema_v0_1.json` remains the default current runtime-surface family.
- `OFARM_Capability_Manifest_schema_v0_2_draft.json` and `OFARM_RuntimeSurfaceContract_schema_v0_2_draft.json` may continue to anchor a bounded deployment-facing traceability lane where richer manifest/contract linkage is already in use.
- package-local implementation artifacts may carry a release bundle, a local service-description catalog, a discovery response document, and local service-description files tied to that bundle.
- those implementation artifacts must remain explicitly fixture-only unless replaced later by deployment-emitted evidence.

## Release-traceability rules

### 1. One release bundle should ground one governed deployment lane

A bounded runtime-surface release bundle should resolve at minimum to:

- one manifest artifact
- one `ActiveArtifactSet`
- one `ConformanceClaimSet`
- one deployment scope
- the runtime-surface contracts and surface identities that the release exposes or previews

This keeps deployment-facing publication traceability anchored on governed OFARM artifacts rather than on loose external-doc filenames alone.

### 2. Local service-description catalog entries should resolve to governed surface identities

A local service-description catalog entry should identify at minimum:

- the service-description document id
- the target governed surface identity
- the linked runtime-surface contract ref
- the local publication path used by the bounded release fixture lane
- the release label and surface posture carried by that publication

This allows package-local proof that service-description files are aligned with the governed surface lane they describe.

### 3. Discovery endpoint description may point at a separate discovery response document

A discovery endpoint description may remain a service-description artifact while pointing at a separate discovery response document.

That discovery response document may summarize the manifest and outward runtime surfaces for the same bounded release lane, but it must not outrank the manifest, runtime-surface contracts, or other active OFARM artifacts.

### 4. `PLANNED` surfaces may publish preview-only documents

If a manifest row remains `PLANNED`, the linked release-traceability fixture should keep its publication posture explicitly preview-only.

This prevents documentation polish from silently making a planned surface look live.

### 5. Fixture-only posture must stay explicit

Package-local release-traceability artifacts should self-declare fixture-only posture and should not be counted as live deployment evidence merely because they carry release labels, local publication paths, or machine-readable documents.

## Selective-merge allowance

The repository may selectively merge reviewed preimplementation service-description material into `04_implementation_and_conformance/` when all of the following hold:

- the merged material is adapted to the current active manifest/runtime-surface examples
- it stays under active supporting implementation status
- it is treated as deployment-facing support evidence, not as semantic authority
- any new surface document for a later-added lane is created in the same bounded style

## What this note does not do

This note does not:

- promote local OpenAPI, AsyncAPI, endpoint-description, or discovery-response files to active semantic law
- require live endpoint fetches from a running deployment
- claim that package-local release fixtures are equivalent to production deployment evidence
- change same-standard bridge promotion posture
- reopen RC2.1 architecture

## Practical implication

A package-local hardening lane may now prove all of the following together:

- one concrete deployment release bundle resolves to one governed manifest / claimset / active-artifact tuple
- each declared service-description ref resolves to a concrete local machine-readable document
- discovery response publication remains aligned with the linked manifest and surface statuses
- planned surfaces remain preview-only even when their docs are locally published for tooling and review
