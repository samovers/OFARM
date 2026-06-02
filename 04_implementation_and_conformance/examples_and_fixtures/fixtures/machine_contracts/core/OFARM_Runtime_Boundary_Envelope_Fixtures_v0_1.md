# OFARM Runtime Boundary Envelope Fixtures v0.1

Date: 2026-04-11  
Status: active machine-contract fixture note  
Scope: starter examples for the Wave 5 runtime-boundary closure pass

---

## Purpose

These fixtures make the remaining runtime seams more explicit without reopening RC2.1 architecture.

They add typed request/result envelopes for:
- authority decisions
- current-state use/materialization decisions
- query execution entry/results
- publication/export assembly

They also add minimal metadata contracts that keep:
- `PassportView`
- `DocumentAssembly`

machine-distinct at runtime.

---

## Starter authority cases

The authority-boundary examples cover:
- delegated field execution reporting allow
- revocation blocking final submission promotion
- AI-assisted submission preparation requiring human approval
- buyer read-allow versus write-deny under explicit sharing
- software-agent document attestation deny by default

These cases are narrow by design.
They close the next executable seams without claiming full authority-matrix completion.

---

## Starter materialization cases

The materialization-boundary examples cover:
- fresh compliance reuse for a high-consequence path
- stale advisory reuse for exploratory use
- invalid compliance reuse after context drift on an attested-output path

This gives a typed envelope layer above the earlier basis/snapshot closure.

---

## Starter query and publication cases

The query seam adds:
- typed query execution request/result envelopes
- explicit alias-resolution-trace references
- explicit current-state materialization result references

The publication seam adds:
- `PassportViewMetadata`
- `DocumentAssemblyMetadata`
- live passport publication allow
- passport-as-document attestation deny
- governed submission filing allow

---

## Boundary rule preserved

This wave does **not** change OFARM’s model law.

It makes already-decided runtime seams more explicit and more testable:
- authority remains governed by the authority RFC set
- current state remains a governed materialization
- query semantics remain governed by QuerySpecification / QueryPlanIR plus alias law
- publication/export remains traceable and does not collapse PassportView into DocumentAssembly
