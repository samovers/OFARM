
# OFARM Advisory to Execution to Passport Dispute Break Test v0.1

Date: 2026-04-19
Status: active supporting implementation artifact
Scope: hostile composition test for an Advisory-origin recommendation that becomes a governed draft plan, later reviewed execution, and finally a buyer-facing passport dispute path

---

## 1. Purpose

This hostile break test composes the seam most likely to be simplified incorrectly by product teams:
- an Advisory-origin recommendation exists
- the recommendation becomes a proposal-shaped BridgeCandidate
- a governed draft plan is prepared
- later execution is captured and accepted through normal source-truth law
- a buyer-facing PassportView is served
- the dispute path attempts to treat the live passport as if it were an attestable frozen document

The goal is to prove that OFARM:
- does not let Advisory output become authoritative truth directly
- does require fresh Compliance-side materialization before buyer-facing publication
- does preserve the PassportView versus DocumentAssembly boundary even during dispute pressure

---

## 2. Required composed artifacts

This test composes existing active and support artifacts:
- the new active `BridgeCandidate` contract family
- a draft `PlannedIntervention`
- the existing pruning semantic event / assertion / review / accepted-consequence chain
- a fresh Compliance materialization basis/snapshot/result for the buyer-facing lot passport
- buyer sharing, authorization, and publication examples for the live passport
- a denied attestation attempt showing that the live PassportView is not silently upgraded into a frozen document

---

## 3. Expected hostile behavior

The runner must prove all of the following:
- the BridgeCandidate remains Advisory-origin and proposal-only
- the bridge path points at a draft plan, not an executed consequence
- the later accepted execution consequence comes from the reviewed semantic event path, not from the bridge object
- the buyer-facing passport is grounded in fresh Compliance materialization, not the exploratory Advisory materialization
- the live passport may be served under governed sharing and read authorization
- the dispute path may not treat the live passport as an attestable frozen document

---

## 4. Non-goals

This break test does not prove:
- a full scenario-workspace promotion
- deployment telemetry for bridge approvals
- full buyer dispute workflow outside the publication/output boundary
- every future advisory-to-output permutation
