# OFARM Agent Actorship and Authority Fixtures v0.1

Status: implementation/conformance fixture set for AAI-CP3.

## Positive fixture

A compliance-steward software-agent instance prepares a preflight review for field 17. The action has:

- an accountable farm-operator sponsor;
- a software-agent profile;
- a deployed agent instance;
- a model/tool profile basis;
- a sponsor-bound actorship binding;
- an authority snapshot;
- a revocation-state check;
- an authorization decision trace;
- a result-qualification reference.

The final filing action remains blocked until human approval.

## Negative fixtures

The following cases fail CP3 conformance:

1. Missing sponsor reference.
2. Model, tool, manifest, prompt, API key, or session identity treated as authority.
3. Revoked authority still used by the agent.
4. Silent delegation through context, memory, or handoff.
5. Human-only action class attempted by an agent.
6. Public-operation success reported as governance success.

These fixtures intentionally do not claim agent-run/handoff readiness or two-agent compatibility.
