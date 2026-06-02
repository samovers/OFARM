# OFARM economic intelligence spike backlog v0.1

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: concrete near-term execution backlog for the bounded economics spike

---

## Lane A — Scenario 1 crop/system ranking

### Goal
Prove OFARM can generate useful economic screening from operational/planning data only.

### Tasks
- bind operational-basis refs for field/crop/operation data
- create crop ranking ScenarioSpec fixtures
- create threshold and ranked-alternative result fixtures
- enforce refusal text for profitability claims without finance basis
- test stale/invalid behavior for advisory reuse

### Done in this package
- candidate schema bundle
- positive fixture bundle
- negative fixture bundle
- validation runner

### Still to implement in code
- actual query compilation from QuerySpecification basis refs
- view rendering from result set
- refusal messaging in runtime UI/API

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

### Done in this package
- scenario, extract, result, bridge fixtures
- allocation-basis example

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

### Done in this package
- scenario, extracts, result, bridge fixtures
- negative bridge example showing non-human-gated failure

### Still to implement in code
- dossier assembly generation
- high-consequence freshness recheck before export
- external-appraisal handoff integration stub
