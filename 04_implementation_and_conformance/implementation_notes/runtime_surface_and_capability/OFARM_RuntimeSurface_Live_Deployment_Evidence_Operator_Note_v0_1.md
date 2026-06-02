# OFARM RuntimeSurface live deployment evidence operator note v0.1

Date: 2026-04-19  
Status: active supporting implementation artifact  
Scope: operational guidance for converting the runtime-surface evidence templates into real deployment evidence artifacts later

---

## Use this note when

- a deployment team wants to replace the package-local templates with real evidence
- a reviewer needs to decide whether a collected artifact is still template-only or is eligible to count as live deployment evidence
- a partner-output telemetry lane needs to be tied back to the governed release bundle without overstating what is modeled today

## Required discipline

Do not change a template into a qualifying evidence artifact unless all placeholders are replaced with deployment-emitted values and the artifact can be traced back to:

- one release bundle
- one deployment scope
- one surface identity or explicitly declared implementation-local adapter surface
- one capture window
- one attributable collector or runtime principal

## Required non-claims

Even after a template is replaced with a real deployment artifact:

- the artifact still does not promote a partner-output surface into active runtime-surface law by itself
- the artifact still does not change same-standard bridge promotion posture by itself
- the artifact still does not outrank the manifest, runtime-surface contract, or other active OFARM artifacts

## Review checklist

Before accepting a later artifact as qualifying live deployment evidence, check all of the following:

1. `templateOnly` is `false`  
2. `qualifiesAsLiveDeploymentEvidence` is justified by the actual collection method  
3. the release-bundle ref, manifest ref, and deployment scope all resolve  
4. the runtime binding matches the observed surface  
5. the evidence refs are deployment-emitted or deployment-controlled rather than package-local replay files  
6. any implementation-local partner surface is labeled as such rather than silently treated as a governed runtime-surface contract
