# OFARM RC2.1 cross-RFC harmonization report v0.1

Date: 2026-04-08  
Status: completed  
Scope: integrate accepted post-charter RFCs into one cleaner baseline pair without reopening the architecture

---

## 1. Purpose

The accepted post-charter RFCs were created as focused closures for six narrow gaps:

- RFC-1 Identity and lifecycle semantics
- RFC-6 Current-state materialization operational policy
- RFC-2 QuerySpecification and QueryPlanIR schemas
- RFC-3 Pack merge semantics by surface
- RFC-4 Authority action matrix and policy model
- RFC-5 Capability Manifest schema and registry relation

Those RFCs were intentionally produced as separate artifacts for reasoning quality.
RC2.1 is the first harmonized baseline that treats them as one integrated system again.

---

## 2. Main harmonization decisions

### 2.1 Constitution versus Platform split remains intact
The harmonization keeps the split real:

- **Constitution RC2.1** = model law and artifact constitution
- **Platform RC2.1** = runtime law and execution architecture

RFC-5 remained mostly Platform-only on purpose.
Capability Manifest is treated as runtime self-description, not constitutional semantic-core law.

### 2.2 Alignment Register remains at v0.13
The Alignment Register already integrated the semantic consequences of:
- RFC-1
- RFC-6
- RFC-2
- RFC-3
- RFC-4

RFC-5 did not change constitutional semantic-core meaning, so the register remains at **v0.13** in the RC2.1 baseline.

### 2.3 Companion artifact set is now stable enough to name directly
RC2.1 baseline depends on the following companion artifacts:

- OFARM Identity and Lifecycle RFC v0.1
- OFARM Current-State Materialization RFC v0.1
- OFARM QuerySpecification Schema RFC v0.1
- OFARM Pack Merge Semantics RFC v0.1
- OFARM Authority Policy Model RFC v0.1
- OFARM Authority Action Matrix v0.1
- OFARM Alignment Register v0.13
- OFARM Event Grammar and Commit Matrix v0.1
- OFARM Pack Safety and Compatibility Policy v0.2
- OFARM Authority, Delegation, and Data Sovereignty Policy v0.2
- OFARM Query Architecture Note v0.1
- OFARM Compiled Output and Passport Taxonomy Note v0.1
- OFARM Capability Manifest RFC v0.1
- OFARM Capability Manifest schema v0.1

### 2.4 RC2.1 is a baseline, not another rewrite
This harmonization pass did not reopen:
- semantic-layer philosophy
- truth philosophy
- twin philosophy
- pack philosophy
- output taxonomy philosophy

It only:
- integrated accepted RFC outcomes
- normalized titles/status markers
- checked cross-document consistency
- preserved the model/runtime boundary

---

## 3. What changed between RC2 and RC2.1

### Constitution-side additions now integrated
RC2.1 Constitution now includes:
- durable identity / identity revision / time-bounded state distinction
- explicit lifecycle rules for fields, zones, crop cycles, lots, equipment/facilities/containers
- MaterializationBasis / MaterializationSnapshot / freshness-state law
- action-based authority model with AuthorityActionClass and ScopeInheritanceMode
- stronger pack merge law by surface family and merge mode
- stronger query-law formalization around QuerySpecification / QueryPlanIR relationship
- stronger conformance expectations tied to those RFCs

### Platform-side additions now integrated
RC2.1 Platform now includes:
- stronger materialization/runtime freshness handling
- QuerySpecification and QueryPlanIR validation expectations
- stronger pack surface-family merge evaluation and trace requirements
- action-based authorization/runtime decision model
- formal Capability Manifest runtime contract and registry relation

---

## 4. What was intentionally left out of Constitution RC2.1

The following remain primarily runtime-level and are not elevated into constitutional semantic-core law:

- Capability Manifest structure
- manifest registry relation fields
- deployment/tenant runtime self-description details
- manifest-to-active-artifact-set consistency mechanics

That is intentional.
Those belong to OFARM Platform.

---

## 5. Result

Produced:
- OFARM Reference Model and Artifact Constitution (RC2.1)
- OFARM Platform Runtime and Product Architecture (RC2.1)

These should now be treated as the harmonized post-charter baseline pair for the next stages:
- reference implementation spike
- final hostile review after gap closure
