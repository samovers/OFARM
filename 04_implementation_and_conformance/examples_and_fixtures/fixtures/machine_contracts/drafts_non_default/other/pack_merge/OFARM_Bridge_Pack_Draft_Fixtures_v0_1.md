# OFARM Bridge Pack Draft Fixtures v0.1

Status: active machine-contract fixture note  
Scope: draft same-standard bridge-pack examples for reversible declared-subset conformance

---

## Purpose

These fixtures add the smallest machine-contract step needed to exercise same-standard reversible bridge-pack conformance without reopening baseline law.
They introduce **draft** export bridge examples for:
- ADAPT payload exchange
- ISOXML file exchange

They are intentionally limited:
- the runtime-surface contracts are `DRAFT`
- the bridge posture is only for a **declared subset**
- these fixtures do **not** make OFARM broadly standard-ready for production bridge-pack claims
- downstream accepted consequence and promotion posture remain governed by normal OFARM authority, evidence, and materialization law

## Included examples

- `OFARM_MappingCoverageStatement_example_adapt_export_bridge_draft_v0_1.json`
- `OFARM_LossMap_example_adapt_export_bridge_draft_v0_1.json`
- `OFARM_RuntimeSurfaceContract_example_adapt_bridge_export_draft_v0_1.json`
- `OFARM_MappingCoverageStatement_example_isoxml_export_bridge_draft_v0_1.json`
- `OFARM_LossMap_example_isoxml_export_bridge_draft_v0_1.json`
- `OFARM_RuntimeSurfaceContract_example_isoxml_bridge_export_draft_v0_1.json`

## Intent

The purpose of these fixtures is to let the implementation/conformance layer test:
- same-standard reverse-pair eligibility
- declared-subset round-trip rehearsal
- loss-aware conflict disclosure

They are not baseline amendments and they are not a claim that OFARM now ships production bridge packs for all external standards.
