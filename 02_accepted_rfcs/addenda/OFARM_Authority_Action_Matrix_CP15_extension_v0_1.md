# OFARM Authority Action Matrix — CP15 extension v0.1

Status: CP15 final amendment accepted/merged addendum  
Date: 2026-05-30

CP15 adds the following authority action classes. All are default-deny unless explicit scoped authority exists.

| Action class | Default posture | Notes |
|---|---|---|
| SOFTWARE_GENERATE_ARTIFACT | agent-assisted allowed if scoped | Generates accepted/merged only. |
| SOFTWARE_APPROVE_GENERATED_ARTIFACT | human approval required | Approval does not deploy. |
| SOFTWARE_APPROVE_SEMANTIC_MAPPING | human/review required | Mapping loss/coverage must be reviewed. |
| SOFTWARE_ACCEPT_SECURITY_WAIVER | human/security-governance required | Requires expiry and scope. |
| SOFTWARE_APPROVE_DEPLOYMENT_CANDIDATE | human/review required | Requires build/SBOM/security/conformance evidence. |
| SOFTWARE_AUTHORIZE_DEPLOYMENT | human/policy approval required | Creates deployment authority only within scope/time. |
| SOFTWARE_PROMOTE_RELEASE | human/policy approval required | Requires accepted/merged, authorization, release, canary/rollback where applicable. |
| SOFTWARE_BIND_RUNTIME_SURFACE | human/policy approval required | Binds release to runtime surface. |
| SOFTWARE_ROLLBACK_RELEASE | policy/human emergency allowed | Must create rollback event trace. |
| SOFTWARE_ACCEPT_DEPLOYMENT_RECEIPT | review required | Receipt is evidence only. |
| SOFTWARE_RECORD_DEPLOYMENT_INCIDENT | machine/human report allowed | Review determines consequence. |
| MODEL_APPROVE_DEPLOYMENT_CANDIDATE | human/review required | CP13/CP14 gates required where applicable. |
| PROMPT_POLICY_APPROVE_HIGH_CONSEQUENCE_CHANGE | human/review required | No agent-only approval by default. |

Successful tool execution, build completion, scan completion, canary pass, or runtime receipt is not authority.
