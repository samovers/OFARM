# runtime_surface_release_lane — evidence drop zone

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: canonical location for future qualifying live deployment evidence tied to the governed runtime-surface release lane

---

## Allowed future production filenames

- `OFARM_runtime_surface_live_deployment_evidence_v*.json`

## Use this folder when

- a real deployment emits evidence for one governed runtime surface in the release lane
- the deployment team can bind the evidence to one release bundle, one deployment scope, one surface identity, and one observation window
- the artifact can honestly carry an `authenticityEnvelope` with `repositoryAuthored: false`

## Do not claim

- that a file here promotes `RuntimeSurfaceContract v0.2` to the package default
- that a file here promotes implementation-local partner-output channels into governed runtime-surface law
- that package-local rehearsal files count as live deployment evidence

## Required follow-up

After adding a real evidence artifact here, run:
- `../../ofarm_external_evidence_intake_runner_v0_4.py`

If the artifact is structurally and authentically reviewable, place a matching accountable decision record under:
- `../../live_evidence_decisions/runtime_surface_release_lane/`

Then run:
- `../../ofarm_external_evidence_decision_runner_v0_2.py`
