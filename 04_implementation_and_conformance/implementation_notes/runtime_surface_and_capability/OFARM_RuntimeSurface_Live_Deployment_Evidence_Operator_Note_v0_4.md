# OFARM RuntimeSurface live deployment evidence operator note v0.4

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: operational guidance for turning the runtime-surface live-evidence templates into future deployment-specific artifacts under the current authenticity-gated intake and reviewer-decision lane

Supersedes:
- `OFARM_RuntimeSurface_Live_Deployment_Evidence_Operator_Note_v0_3.md`

---

## Use this note when

- a deployment team wants to replace the package-local live-evidence templates with real deployment artifacts
- a reviewer needs to decide whether a collected artifact is still template-only, still repo-authored rehearsal material, or is eligible to count as governed runtime-surface live evidence
- partner-output telemetry needs to be captured as support evidence alongside the governed runtime-surface lane

## Current target production filenames

Place future real artifacts in:

- `live_evidence_packets/runtime_surface_release_lane/OFARM_runtime_surface_live_deployment_evidence_v*.json`
- `live_evidence_packets/partner_output_channels/OFARM_runtime_surface_partner_output_telemetry_v*.json`

## Required discipline

Do not treat a copied artifact as qualifying evidence unless:

1. `templateOnly` is `false`
2. deployment-specific placeholders are removed
3. `authenticityEnvelope` is present
4. `authenticityEnvelope.repositoryAuthored` is `false`
5. `authenticityEnvelope.attestedByRef`, `attestedAt`, and `artifactDigest` are explicit
6. `qualificationClaim` is present and the `claimKind` matches the lane
7. the artifact binds to one release bundle, one deployment scope, one surface identity or explicit implementation-local adapter surface, and one capture window
8. the artifact points to deployment-emitted or deployment-controlled evidence refs rather than package-local rehearsal files
9. the artifact survives `ofarm_external_evidence_intake_runner_v0_4.py`
10. an accountable reviewer later records a matching disposition through `live_evidence_decisions/` and `ofarm_external_evidence_decision_runner_v0_2.py`

## Required non-claims

Even after a qualifying artifact exists:

- partner-output telemetry still does not promote dashboard, CSV, PDF, dossier, or submission channels into governed runtime-surface law by itself
- a live evidence artifact still does not make `RuntimeSurfaceContract v0.2` the package default by itself
- the artifact still does not outrank active manifests, runtime-surface contracts, or other active OFARM artifacts
