# OFARM economic intelligence spike execution runbook v0.1

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: execution runbook for the bounded OFARM economics spike after package consolidation and hard-checking

---

## 1. Purpose

This runbook exists to stop the economics amendment from drifting into either:
- architecture theatre, or
- stealth ERP implementation.

The spike is allowed to prove value.
The spike is not allowed to quietly change OFARM law.

---

## 2. Working posture

Use the consolidated checked candidate as the single working tree.
Treat economics as:
- native in Advisory,
- non-authoritative by default,
- companion + implementation only,
- blocked from RFC and machine-contract promotion until the promotion gate passes.

---

## 3. Non-negotiable constraints

The spike must preserve all of the following:
- one semantic substrate
- two logical twins
- no direct Advisory-to-Compliance mutation
- no authoritative writes into projections, marts, caches, or report stores
- no second query model
- no ledger semantics
- no "economic current state"
- no "economic passport" family

---

## 4. Ordered execution

### Phase 0 — Freeze and instrument

Do once before feature work:
1. Freeze the consolidated checked candidate as the only working tree.
2. Mark earlier economics waves as superseded lineage only.
3. Keep the three economics/scenario notes in `01_companion_artifacts/`.
4. Keep contracts/examples/runners in `04_implementation_and_conformance/` only.
5. Wire logging/trace capture for:
   - basis refs
   - target twin
   - freshness status
   - output family
   - bridge candidate review state

Exit condition:
- one working tree,
- one backlog,
- one gate,
- one hostile matrix.

### Phase 1 — Lane A (Scenario 1 crop/system ranking)

Objective:
Prove operational-only economics can produce useful screening without fake profitability.

Required implementation:
- bind operational basis refs to field/crop/activity history
- create scenario input surface using only Scenario-1-confirmed inputs
- emit ranked alternatives / thresholds / constraint ratios
- emit explicit refusal language when users ask for profitability beyond the evidence basis
- show freshness state and basis trace

Required hostile checks:
- no profitability labels
- no current-state labels
- no hidden query fields inside scenario spec

Exit condition:
- users can compare alternatives directionally,
- the system refuses fake precision,
- the result stays clearly Advisory.

### Phase 2 — Lane B (Scenario 2 own-vs-contractor / bottleneck economics)

Objective:
Prove partial or flattened finance can support bounded operational economics without becoming accounting truth.

Required implementation:
- import bounded contractor/input-price extracts
- declare allocation basis where allocation exists
- render a report-oriented decision packet
- preserve source extract provenance
- preserve non-ledger posture

Required hostile checks:
- reject account hierarchy / journal-like fields
- reject payable/receivable workflow semantics
- reject scenario result reuse as current-state truth

Exit condition:
- a user can evaluate own-vs-contract or bottleneck decisions,
- imported finance stays extract-shaped,
- no ERP behavior appears.

### Phase 3 — Lane C (Scenario 3 capex pre-gate dossier)

Objective:
Prove OFARM can support pre-gate screening for capacity/post-harvest investment without pretending to do full appraisal.

Required implementation:
- import bounded settlement/energy/financing-term extracts
- generate capacity / throughput / sensitivity outputs
- shape a DossierAssembly-oriented package
- force human review and explicit external-appraisal escalation
- recheck freshness before dossier export

Required hostile checks:
- no auto-promotion to harder truth
- no stale export for high-consequence use
- no claim that crop-level economics alone justifies capex

Exit condition:
- OFARM can generate a pre-gate dossier,
- the dossier is clearly advisory/screening-grade,
- the system demands external appraisal when needed.

---

## 5. Required evidence captured during the spike

For every lane collect:
- the governing QuerySpecification / query basis refs
- target twin and output family
- basis trace sample
- freshness state sample
- one positive example
- one negative/refusal example
- one hostile test result
- one explicit statement of what remains outside OFARM

---

## 6. Weekly review questions

At the end of each spike cycle ask:
1. Did a second query model appear?
2. Did any output start behaving like current-state truth?
3. Did imported finance start drifting toward ledger semantics?
4. Did any bridge path become too easy or semi-automatic?
5. Did the UI burden become finance-entry-heavy before delivering value?
6. Did any output family drift toward an "economic passport" catch-all?

If the answer to any question is yes, cut back before writing more artifacts.

---

## 7. Promotion rule

Only consider promotion after all three lanes have:
- passed the hard acceptance gate,
- survived the hostile matrix,
- stayed inside current OFARM truth/twin/query/output law,
- and shown deployment-shaped evidence rather than only package-local fixtures.

Until then:
- no RFC promotion,
- no machine-contract promotion,
- no baseline patch,
- no Alignment Register patch.

---

## 8. What success looks like

A successful spike proves exactly this:
- economics can be native in Advisory,
- operations remain the authoritative substrate,
- imported finance can inform decisions without becoming accounting truth,
- scenario outputs remain traceable, freshness-aware, and proposal-shaped,
- and OFARM still does not become ERP.
