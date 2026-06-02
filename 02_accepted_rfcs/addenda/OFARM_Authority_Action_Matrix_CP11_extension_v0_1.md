# OFARM Authority Action Matrix — CP11 Extension v0.1

Status: accepted addendum; machine contracts remain draft/non-default where applicable.

## New charter-sensitive action classes

| Action class | Default posture | AI/agent posture | Notes |
|---|---|---|---|
| CHARTER_SET_OBJECTIVE_PRIORITY | Human approval required | Not allowed by default | Changes objective hierarchy. |
| CHARTER_APPROVE_TRADEOFF | Human approval required for high consequence | May prepare review package only | Policy approval requires authority trace. |
| CHARTER_APPROVE_EXCEPTION | Human only / human approval required | Not allowed by default | Open-ended exceptions invalid. |
| CHARTER_ACCEPT_BREACH_FINDING | Human approval required | Not allowed by default | Does not automatically create compliance fact. |
| CHARTER_CONTEST_BREACH_FINDING | Authorised party / human process | May prepare evidence package | Contestation must be traceable. |
| CHARTER_RESOLVE_BREACH_FINDING | Human approval required | Not allowed by default | Requires review/authority trace. |
| CHARTER_APPROVE_CLAIM_BASIS | Human approval or policy approval with trace | May prepare candidate only | Required for stronger claims. |
| CHARTER_ATTEST_SUSTAINABILITY_CLAIM | Human/signing authority | Not allowed by default | Attestation-ready/filed states require trace. |
| CHARTER_ACTIVATE_POLICY_PACK | Human approval/governance required | Not allowed by default | Sustainability surfaces may not conflict silently. |
| CHARTER_APPROVE_RISK_BUDGET | Human approval required | Not allowed by default | Does not authorise execution. |
| CHARTER_APPROVE_REGRET_BUDGET | Human approval required | Not allowed by default | Does not authorise experimentation or learning promotion. |

Policy approval is not model confidence, tool success, workflow completion, manifest support, or agent runtime success. It must resolve to an authority-decision trace or equivalent governed decision record.
