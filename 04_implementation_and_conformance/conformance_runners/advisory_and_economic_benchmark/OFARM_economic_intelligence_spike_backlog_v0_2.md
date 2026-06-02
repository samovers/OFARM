# OFARM economic intelligence spike backlog v0.2

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: concrete near-term execution backlog for the bounded economics spike after the first executable Lane A pass

---

## Lane A — Scenario 1 crop/system ranking

### Goal
Prove OFARM can generate useful economic screening from operational/planning data only.

### Completed in this pass
- sample Scenario-1 dataset added
- executable evaluator added
- generated summary and results added
- positive scenario/result/bridge bundle added
- negative profitability-claim example added
- validator extended with Scenario-1 honesty checks
- validation rerun and stored

### Still to implement in code
- actual query compilation from QuerySpecification basis refs
- ViewModule rendering from result set
- freshness/refusal behavior in runtime UI/API
- explicit bottleneck declaration capture in the scenario authoring flow

---

## Lane B — Scenario 2 own-versus-contractor / bottleneck economics

### Goal
Prove partial/flattened finance can support a bounded operational decision without becoming accounting truth.

### Tasks
- import contractor-rate extract fixture
- import input-price extract fixture
- define allocation-basis declaration example
- generate comparison ReportAssembly-ready result set
- verify that imported facts remain extract-shaped and non-ledger

### Still to implement in code
- import-mapping plumbing from external source to ImportedFactExtract
- report assembly shaper for decision packet
- trace-back surface for allocation basis visibility

---

## Lane C — Scenario 3 capex pre-gate dossier

### Goal
Prove OFARM can support pre-gate screening for post-harvest capacity investment without pretending to do full appraisal or financing truth.

### Tasks
- import settlement / energy / financing-term extracts
- define capacity and sensitivity result sets
- generate DossierAssembly-oriented bridge candidate
- enforce requirement for human review and external appraisal escalation

### Still to implement in code
- dossier assembly generation
- high-consequence freshness recheck before export
- external-appraisal handoff integration stub
