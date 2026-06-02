# OFARM Event Grammar — CP15 extension v0.1

Status: CP15 final amendment accepted/merged addendum  
Date: 2026-05-30

CP15 event families include:

| Event family | Typical commit class | Notes |
|---|---|---|
| GeneratedArtifactRecorded | generated/proposed artifact | Not deployment authority. |
| BuildProvenanceRecorded | evidence record | Build success is evidence only. |
| SBOMRecorded | evidence record | Subject to dependency risk assessment. |
| StaticAnalysisRecorded | evidence record | Findings may block deployment. |
| SecurityScanRecorded | evidence record | Findings may block deployment. |
| SecurityWaiverApproved | governance decision | Scope/expiry required. |
| ConformanceRunRecorded | evidence record | Conformance success is not authority. |
| DeploymentCandidateProposed | advisory/proposed delivery state | Requires review. |
| DeploymentPlanApproved | governance decision | Does not deploy by itself. |
| DeploymentAuthorized | authority decision | Scoped/time-bounded. |
| DeploymentPromoted | governance decision | Requires chain evidence. |
| RuntimeSurfaceBound | runtime binding event | Binding is scoped. |
| CanaryResultRecorded | evidence record | Canary pass is not production readiness. |
| RollbackExecuted | runtime event | Creates rollback evidence. |
| RuntimeDeploymentReceiptRecorded | evidence record | Receipt is not readiness. |
| DeploymentIncidentRecorded | incident record | May block/qualify deployments. |
| SoftwareSupplyChainIncidentRecorded | incident record | May block/qualify deployments. |

No CP15 event auto-promotes to current/default schema, Compliance Twin fact, mission authority, or production readiness.
