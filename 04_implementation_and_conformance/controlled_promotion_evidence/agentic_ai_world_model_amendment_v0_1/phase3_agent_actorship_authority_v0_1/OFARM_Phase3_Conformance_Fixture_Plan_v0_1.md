# OFARM Phase 3 Conformance Fixture Plan v0.1

Date: 2026-05-14  
Status: supporting; tests not executed

## Positive fixtures

1. Evidence steward creates a draft evidence attachment within delegated field/crop-cycle scope.
2. Advisory agronomy agent creates a planned-intervention draft in Advisory posture.
3. Sharing agent reads a scoped lot view under a valid SharingGrant and preserves permission-limited result posture.
4. Contractor agent reports operation execution within scope/time as a draft operation claim.

## Negative fixtures

1. Evidence steward attempts `CONTEXT_ACTIVATE_PACK`.
2. Advisory agronomy agent attempts `ASSERT_COMPLIANCE` without human approval.
3. Contractor agent reports operation outside delegated scope.
4. Revoked agent instance attempts to attach evidence.
5. Unapproved model/tool profile attempts high-consequence output preparation.
6. Agent tries to convert its output into generic `AgentOutput` truth.

## Execution posture

Because no implementation exists, these remain fixture definitions and schema examples only. They must not be reported as executed runtime tests.
