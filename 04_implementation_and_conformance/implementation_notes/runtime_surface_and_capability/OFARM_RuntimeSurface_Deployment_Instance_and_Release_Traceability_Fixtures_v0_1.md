# OFARM runtime-surface deployment-instance and release traceability fixtures v0.1

Date: 2026-04-19  
Status: active supporting implementation fixture set  
Scope: bounded package-local proof connecting one concrete deployment release bundle to the linked manifest, active-artifact state, discovery response, and local service-description files for that deployment-facing lane

---

## 1. Purpose

These fixtures harden the next deployment-facing runtime-surface seam after the manifest/discovery linkage wave.

The bounded target is:
- keep active currentness unchanged for Capability Manifest and RuntimeSurfaceContract
- prove that one concrete release bundle resolves to the linked manifest / active-artifact / claim-set tuple already in force for the bounded surface-linkage lane
- prove that each declared service-description ref resolves to one local machine-readable document
- keep discovery response publication aligned with governed surface identities and manifest status
- keep `PLANNED` surfaces preview-only even when their docs are locally available for tooling and review

## 2. Positive fixtures

### Release bundle grounding
- one release bundle resolves to the linked manifest draft, active artifact set, and conformance claim set
- the release bundle stays explicitly fixture-only and does not claim live deployment evidence

### Local service-description catalog
- the catalog resolves each declared service-description ref to a concrete local file
- each catalog entry names the governed target surface identity and linked runtime-surface contract

### Discovery publication alignment
- the capability discovery endpoint description resolves to a concrete discovery response document
- the discovery response document points back to the same manifest, deployment scope, and outward surface statuses as the release bundle

### Service-description document alignment
- NGSI-LD export OpenAPI stays `PARTIAL`
- query-facade OpenAPI stays `PLANNED`
- semantic-event-ingress AsyncAPI stays `PLANNED`
- each local document keeps release-label and target-surface linkage explicit

## 3. Negative fixtures

- a release bundle whose manifest ref drifts from the bounded deployment lane should fail
- a catalog entry whose local document advertises a different target surface should fail
- a discovery response document whose manifest ref drifts should fail
- a planned surface whose release posture is marked live should fail

## 4. Expected result

The runner should emit `PASS_WITH_LIMITATIONS` when:
- the linked manifest, active artifact set, claim set, and runtime-surface contracts validate
- the release bundle resolves to those governed artifacts
- each local service-description file resolves and aligns to the correct surface
- the discovery endpoint description resolves to a concrete discovery response document
- planned surfaces remain preview-only
- negative mutations fail as expected

## 5. Limitation boundary

This wave is package-local release-traceability proof only.
It does not fetch live deployment endpoints and does not claim that the local docs are equivalent to production deployment evidence.
