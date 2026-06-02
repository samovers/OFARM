# Deep Research Prompt — OFARM AI-Agent-Ready Platform Implementation Context

Use this prompt before finalizing Phases 4–7 of the AI-Agent-Ready Platform Implementation Amendment.

```text
You are preparing research support for an OFARM 2 amendment.

Research goal:
Identify best current practices for making a semantic reference model and runtime platform ready for implementation by AI coding agents and for later application-building by AI agents, without weakening OFARM’s existing model/runtime law.

OFARM context:
OFARM is a crop-farming semantic reference model and platform architecture. It has:
- assertion/history-first canonical truth
- governed current-state materialization
- one semantic substrate with Compliance Twin and Advisory Twin
- explicit commit classes and promotion law
- explicit authority, delegation, revocation, sharing, and data-sovereignty law
- QuerySpecification and QueryPlanIR
- PassportView and DocumentAssembly taxonomy
- pack/profile compatibility and merge law
- Capability Manifest
- machine contracts and conformance fixtures

Active baseline law wins over research. Do not recommend rewriting OFARM into CRUD. Do not let projections become truth stores. Do not let AI outputs become governance decisions. Do not let packs mutate core meaning. Do not treat FMIS or external imports as accepted truth without governed promotion.

Research questions:
1. What contract-first API practices best support AI coding agents building a complex platform?
2. How should public/internal API and schema boundaries be documented so agents do not copy internals?
3. What patterns from OpenAPI, AsyncAPI, JSON Schema, FHIR CapabilityStatement, FHIR OperationOutcome, Kubernetes API discovery/OpenAPI, OPA/Rego policy traces, MCP-style tool manifests, or similar systems are relevant?
4. How should platform capabilities be exposed to agents so they know what they can call, what requires approval, and what is forbidden?
5. How should high-consequence operations implement dry-run, preflight, explain, and trace retrieval?
6. What error/reason-code registry structure best supports safe AI and SDK behavior?
7. What SDK/codegen practices reduce hallucinated API behavior?
8. What conformance tests catch AI-agent implementation shortcuts?
9. What offline sync, idempotency, retry, duplicate import, and conflict-resolution practices are relevant for farm/mobile/contractor workflows?
10. What unit-conversion, quantity-calculation, formula governance, and rounding practices are relevant for agricultural application platforms?
11. How should source-fidelity, loss maps, unresolved identity, and candidate-only imports be represented for FMIS/machinery/sensor adapters?
12. How should apps safely display stale, disputed, permission-limited, redacted, or evidence-insufficient results?

Required output:
Return a structured research report with these sections:

A. Executive summary
B. Patterns directly applicable to OFARM
C. Patterns that should be rejected because they would weaken OFARM
D. Recommended amendment artifacts
E. Recommended machine contracts
F. Recommended public API surfaces
G. Recommended SDK/codegen structure
H. Recommended conformance tests
I. Recommended agent-readiness gate
J. Source matrix with citations

For each recommendation, classify it as:
- baseline law implication
- accepted RFC extension
- companion artifact
- machine contract
- implementation/conformance artifact
- research-only note

Also include:
- risks
- smallest controlled patch
- affected OFARM files or folders
- whether external evidence is required before promotion

Important constraints:
- Do not recommend broad redesign.
- Do not import external standards as hidden OFARM law.
- Do not use legacy FA_RM/FARM_RM terminology unless explicitly marked historical.
- Do not make livestock semantics part of the current crop-farming release.
- Do not promote farm-owner draft contracts to default law without live/owner evidence.
- Treat FMIS shadow import as candidate-only unless governed evidence and promotion support stronger status.
```

