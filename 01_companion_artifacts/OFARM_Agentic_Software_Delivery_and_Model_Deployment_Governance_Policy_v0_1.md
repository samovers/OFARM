# OFARM Agentic Software Delivery and Model Deployment Governance Policy v0.1

Status: companion policy candidate for CP15  
Date: 2026-05-30

## Purpose

This companion policy explains how CP15 should be interpreted by implementers and AI agents.

## Interpretation rules

1. Generated software is a proposed artifact, not deployment authority.
2. Generated adapters and mappings must prove semantic coverage/loss and applicable CP11/CP12/CP13/CP14 gates before deployment.
3. Build, test, scan, conformance, canary, telemetry, and runtime receipt are evidence inputs, not governance success.
4. Security waivers must be scoped, expiring, authority-backed, and visible to deployment decisions.
5. Model evaluation evidence does not authorise model deployment.
6. CP13 learning outputs and CP14 model-improvement signals may inform model candidates but do not deploy them.
7. Deployment outputs must disclose draft/non-default posture, limitations, blocked uses, authority, rollback, canary, and incident state.

## Display guidance

Deployment-facing surfaces should distinguish:

```text
candidate
planned
authorised
promoted
bound to runtime surface
canarying
receipt observed
rolled back
incident blocked
```

No display should collapse these into a single “deployed/ready” badge unless CP15 evidence and authority gates allow that disposition.
