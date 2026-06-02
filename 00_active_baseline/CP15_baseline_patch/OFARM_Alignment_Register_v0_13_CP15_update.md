# OFARM Alignment Register v0.13 — CP15 update

Status: final CP15 amendment candidate alignment addendum  
Date: 2026-05-30

## CP15 concept additions

CP15 adds the following OFARM-owned or OFARM-governed delivery concepts to the alignment register as candidate baseline concepts upon acceptance:

| Concept | Area | Alignment status | External role | Preferred OFARM term | Reason |
|---|---|---|---|---|---|
| SoftwareDeliveryBoundary | Delivery governance | OFARM_OWNED | External CI/CD/MLOps tools are runtime surfaces only | SoftwareDeliveryBoundary | Defines CP15 non-bypass boundary for software/model delivery. |
| GeneratedSoftwareArtifact | Agentic delivery | OFARM_OWNED | Generated code tools are provenance sources only | GeneratedSoftwareArtifact | Prevents generated code becoming deployment authority. |
| GeneratedPatchArtifact | Agentic delivery | OFARM_OWNED | Patch systems are evidence/provenance only | GeneratedPatchArtifact | Separates generated patch from accepted release. |
| GeneratedAdapterArtifact | Integration delivery | OFARM_OWNED | Adapter frameworks are external surfaces only | GeneratedAdapterArtifact | Enforces CP12/CP14 gates for mission and intelligence adapters. |
| GeneratedWorkflowArtifact | Runtime workflow | OFARM_OWNED | Workflow engines are runtime surfaces only | GeneratedWorkflowArtifact | Prevents generated workflow from becoming runtime authority. |
| GeneratedPromptOrPolicyArtifact | Policy/prompt delivery | OFARM_OWNED | Prompt/policy generators are provenance sources only | GeneratedPromptOrPolicyArtifact | Prevents high-consequence policy changes without review. |
| SemanticMappingCandidate | Semantic mapping | OFARM_OWNED | Mapping standards/tools are anchors only | SemanticMappingCandidate | Requires loss/coverage review before deployment. |
| BuildProvenance | Supply chain | OFARM_OWNED | Build tools are evidence sources only | BuildProvenance | Records build identity without granting authority. |
| SBOMReference | Supply chain | OFARM_OWNED | SBOM standards are evidence formats | SBOMReference | Connects dependencies to deployment gate. |
| DependencyRiskAssessment | Supply chain risk | OFARM_OWNED | External vuln data are evidence sources | DependencyRiskAssessment | Blocks critical/unknown risk without review. |
| StaticAnalysisResult | Security quality | OFARM_OWNED | External scanners are evidence sources | StaticAnalysisResult | Scan success is not deployment authority. |
| SecurityScanResult | Security quality | OFARM_OWNED | External scanners are evidence sources | SecurityScanResult | Blocks critical findings without authority/waiver. |
| SecurityFindingWaiver | Security governance | OFARM_OWNED | External waiver workflows are context only | SecurityFindingWaiver | Waivers require scope, expiry, and authority. |
| ConformanceTestPlan | Conformance | OFARM_OWNED | Test frameworks are runtime tools only | ConformanceTestPlan | Defines intended conformance coverage. |
| ConformanceRunReceipt | Conformance | OFARM_OWNED | Test runners are evidence sources | ConformanceRunReceipt | Run success is evidence, not deployment authority. |
| DeploymentCandidate | Deployment governance | OFARM_OWNED | Deployment tools are runtime surfaces | DeploymentCandidate | Candidate state is not deployment authority. |
| DeploymentPlan | Deployment governance | OFARM_OWNED | CI/CD plans are external execution plans | DeploymentPlan | Captures environment, gates, rollback, canary, blast radius. |
| DeploymentAuthorization | Authority | OFARM_OWNED | External approval systems are traces only | DeploymentAuthorization | Deployment requires explicit authority trace. |
| DeploymentPromotionDecision | Promotion | OFARM_OWNED | Release tools are evidence/runtime surfaces | DeploymentPromotionDecision | Promotion remains governed and non-automatic. |
| ReleaseBundle | Release | OFARM_OWNED | Registries are distribution surfaces | ReleaseBundle | Bundle release requires signature, SBOM, conformance, candidate consistency. |
| RuntimeSurfaceReleaseBinding | Runtime surface | OFARM_OWNED | Runtime systems are deployment surfaces | RuntimeSurfaceReleaseBinding | Binding is explicit and scoped. |
| CanaryPlan | Runtime release | OFARM_OWNED | Canary tooling is runtime instrumentation | CanaryPlan | Canary is bounded and non-production by default. |
| CanaryResult | Runtime release | OFARM_OWNED | Telemetry tools are evidence sources | CanaryResult | Canary pass is not production readiness. |
| RollbackPlan | Runtime safety | OFARM_OWNED | Rollback tools are execution mechanisms | RollbackPlan | Readiness requires evidence and freshness. |
| RollbackEvent | Runtime safety | OFARM_OWNED | Runtime events are evidence inputs | RollbackEvent | Rollback occurrence is a governed event. |
| RuntimeDeploymentReceipt | Runtime deployment | OFARM_OWNED | Runtime receipt is evidence only | RuntimeDeploymentReceipt | Receipt is not production readiness. |
| ModelDeploymentCandidate | Model delivery | OFARM_OWNED | Model registries are external surfaces | ModelDeploymentCandidate | Model evaluation is not deployment authority. |
| ModelEvaluationEvidence | Model evidence | OFARM_OWNED | Model cards/evals are evidence formats | ModelEvaluationEvidence | Requires bias/quality/fit handling. |
| SoftwareSupplyChainIncident | Incident | OFARM_OWNED | External incident systems are evidence sources | SoftwareSupplyChainIncident | Supply-chain incidents affect deployment gates. |
| DeploymentIncident | Incident | OFARM_OWNED | Runtime incident tools are evidence sources | DeploymentIncident | Incidents block/qualify deployment paths. |
| DeploymentOutputQualification | Output qualification | OFARM_OWNED | Output displays are surfaces only | DeploymentOutputQualification | Prevents deployment outputs from overclaiming authority/readiness. |

## CP15 non-promotions

CP15 does not promote CP11, CP12, CP13, CP14, or CP15 draft/non-default machine contracts to current/default.
