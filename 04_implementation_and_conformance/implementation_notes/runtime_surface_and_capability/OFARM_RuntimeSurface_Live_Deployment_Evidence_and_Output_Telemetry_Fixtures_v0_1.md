# OFARM RuntimeSurface live deployment evidence and output telemetry fixtures v0.1

Date: 2026-04-19  
Status: active supporting implementation artifact  
Scope: bounded capture-ready fixture family for runtime-surface live deployment evidence and partner-output telemetry linkage

---

## Purpose

This wave performs the next narrow move after runtime-surface release traceability.
It does **not** invent fake live deployment evidence.
It prepares the package to receive future deployment evidence cleanly while explicitly linking the already-present package-local publication telemetry to the governed release lane where possible.

## Included artifacts

- `OFARM_runtime_surface_live_deployment_evidence_capture_template_v0_1.json`
- `OFARM_runtime_surface_partner_output_telemetry_capture_template_v0_1.json`
- `OFARM_RuntimeSurface_Live_Deployment_Evidence_Operator_Note_v0_1.md`
- `OFARM_runtime_surface_live_deployment_evidence_registry_v0_1.json`
- `OFARM_runtime_surface_partner_output_telemetry_linkage_v0_1.json` (superseded later by the governance-boundary-aligned `v0.2` summary)
- `ofarm_runtime_surface_live_deployment_evidence_runner_v0_1.py`
- `OFARM_runtime_surface_live_deployment_evidence_results_v0_1.json`

## What this wave does

- prepares one stable capture shape for future live deployment evidence tied to the current release-bundle lane
- prepares one stable capture shape for future partner-output telemetry tied to release-bound trace-back and publication events
- explicitly separates **capture-ready** artifacts from **qualifying evidence**
- links the current package-local runtime-emitted publication telemetry and partner-surface trace-back records into one bounded summary so the package can say exactly what it has and what it still lacks
- keeps preview-only runtime surfaces ineligible for live-evidence claims
- keeps unmodeled partner-output surfaces explicit instead of silently treating them as already-governed runtime-surface contracts
- hands current partner-output channels forward to the later governance-boundary decision lane rather than forcing automatic promotion

## What this wave does not do

- it does **not** create real live deployment evidence
- it does **not** claim that the package-local release bundle, service-description catalog, or runtime-emitted publication telemetry already qualify as live deployment evidence
- it does **not** promote partner-output surfaces into active runtime-surface contracts
- it does **not** change same-standard bridge posture

## Current bounded truth

Within the current release lane:

- `surface:capability-discovery:v1` and `surface:ngsi-ld-export:v1` are live-posture surfaces in the package-local release bundle
- `surface:cql2-query-facade:v1` and `surface:semantic-event-ingress:v1` remain preview-only in that lane
- only the NGSI-LD partner surface is already linked to a governed runtime-surface contract in the current runtime-surface draft example set
- the dashboard, advisory CSV, compliance PDF, dossier JSON, and submission XML partner surfaces remain implementation-local support identities in the existing package-local publication telemetry lane

## Conversion rule

Keep the two capture files at their template filenames while the repository remains in pre-live-evidence posture.
Only copy a template to a deployment-pattern evidence filename after a real deployment artifact exists.
When that happens:

1. copy the template to the deployment-specific filename  
2. set `templateOnly` to `false`  
3. set `qualifiesAsLiveDeploymentEvidence` only if the collection actually satisfies the closure-note rules  
4. replace every placeholder with deployment-emitted ids, timestamps, and evidence refs  
5. rerun the runtime-surface live deployment evidence runner  

## Qualification rule

For a later artifact to count as qualifying live deployment evidence for this lane, it must satisfy all of the following:

- the evidence is emitted or collected from a real deployment instance rather than being a package-local fixture or replay
- the evidence binds to one governed release bundle and one surface lane
- the evidence records the actual service-description and runtime binding observed
- the evidence is attributable to a runtime principal, operator, or deployment-controlled collector
- the evidence clearly distinguishes governed runtime-surface identities from implementation-local partner-output identities

## Non-qualifying material in the current package

The following remain non-qualifying by design:

- `OFARM_runtime_surface_deployment_release_bundle_example_core_surface_linkage_v0_1.json`
- `service_descriptions/core_surface_linkage_release_v0_1/service_description_catalog_v0_2.json`
- `OFARM_runtime_deployment_emitted_publication_telemetry_v0_1.json`
- `OFARM_runtime_partner_surface_publication_trace_back_records_v0_1.json`
- `OFARM_runtime_deployment_emitted_publication_gate_sequence_records_v0_1.json`

## Current package posture

The package now has:

- a capture-ready lane for future runtime-surface live deployment evidence
- a capture-ready lane for future partner-output telemetry evidence
- one bounded linkage summary for the already-present package-local runtime-emitted publication telemetry
- a later governance-boundary lane that can turn “explicit but unmodeled” partner surfaces into an actual keep-local versus promote decision

The package still does **not** have qualifying live deployment evidence for this lane.
