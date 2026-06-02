# OFARM Economic Intelligence Pack Note v0.2

Date: 2026-04-12  
Status: active companion artifact  
Scope: define the first bounded specialization of the Advisory scenario workspace for farm economic intelligence without turning OFARM into ERP, shadow ERP, or fake-current-state

---

## 1. Purpose

This note defines the smallest justified OFARM-native economics posture.

The aim is not to build a finance suite.
The aim is to make economically meaningful decision support native to OFARM where operations and economics are tightly coupled, while keeping authoritative truth, compliance consequences, and ERP semantics properly bounded.

---

## 2. Core stance

### 2.1 Operations and economics are causally coupled
Operational truth is the main causal substrate for bounded farm economics:
- hectares,
- activities,
- hours,
- machinery use,
- fuel use,
- input use,
- yields,
- lot/facility movements where relevant.

### 2.2 Operations and economics are not the same authority class
The fact that operations drive economics does **not** mean all economic outputs should become authoritative core truth.

Economic reasoning often includes:
- estimates,
- scenarios,
- benchmarks,
- proxies,
- allocations,
- imported posted facts from external accounting systems,
- model outputs.

Those must stay explicit and typed.

### 2.3 Economics belongs in Advisory by default
Economic intelligence is native to OFARM as an Advisory-Twin packized capability.
It is not native as a ledger or authoritative financial-close engine.

---

## 3. Hard boundary: not ERP

This pack must not become:
- general ledger,
- accounts payable / accounts receivable,
- payroll,
- tax or VAT engine,
- treasury or bank reconciliation,
- procurement workflow,
- order-management system,
- statutory financial-reporting system,
- inventory-valuation ERP clone,
- second accounting truth store.

If a proposed feature requires ledger completeness or close-process semantics, it belongs outside this pack.

---

## 4. What this pack is for

This pack is for economically meaningful decision support such as:
- crop/system ranking before season commitment,
- incremental change decisions in season,
- own-versus-contract comparisons,
- break-even and downside-threshold framing,
- capacity/bottleneck economics,
- post-harvest routing and storage/processing decisions where data exists,
- pre-gate capital screening.

This pack is **not** for replacing formal accounting or statutory finance.

---

## 5. Data-maturity posture

### 5.1 Scenario 1 — operational/planning data only
Valid support:
- revenue and resource-intensity screening,
- return per scarce operational resource,
- partial-budget style directional comparison with explicit assumptions,
- break-even price or yield thresholds with visible assumption ranges.

Invalid or dangerous claims:
- asserted net profitability,
- whole-farm solvency claims,
- fine-grain field profit using hidden fixed-cost allocation.

### 5.2 Scenario 2 — operational data plus partial or flattened financial inputs
Additional valid support:
- enterprise budgets,
- gross-margin style screening,
- contractor-rate comparisons,
- return-to-resource screens using explicit rate cards,
- more credible break-even thresholds,
- limited post-harvest routing economics where quality, loss, and cost data exist.

Still dangerous:
- pretending flattened year-end totals can be allocated back to field truth without confidence loss,
- presenting allocation-heavy fine-grain profit as if it were observed actual.

### 5.3 Scenario 3 — plus regular ERP/accounting imports
Additional valid support:
- enterprise and farm-level trend analysis,
- cash-flow and debt-service support views,
- stronger capex pre-gate dossiers,
- more disciplined sensitivity analysis using posted external facts.

Still outside scope:
- accounting close,
- ledger reconciliation workflow,
- statutory statements,
- accounting system master authority.

---

## 6. Minimum economic evidence classes

The pack should type economic values at minimum as:
- `ACTUAL_POSTED`
- `ACTUAL_PRELIMINARY`
- `ESTIMATE`
- `BENCHMARK`
- `PROXY`

The pack should also preserve:
- source system or source artifact reference,
- as-of time,
- scope/grain,
- freshness posture,
- whether the value was direct, derived, or allocated.

No economic number shown to the user should float without this posture.

---

## 7. Pack-local object posture

These remain **pack/runtime candidate contracts**, not constitutional-core promotions and not accepted machine contracts yet.

### 7.1 EconomicScenarioSpec
ScenarioSpec specialized for economic use, including:
- decision class,
- target scope and grain,
- economic evidence inputs,
- assumptions and ranges,
- relevant cost and price posture,
- method/model used.

### 7.2 EconomicSignal
Typed economic input or derived output carrying:
- evidence class,
- provenance,
- freshness,
- direct-versus-allocated flag,
- optional uncertainty band.

### 7.3 ImportedFactExtract
Used for bounded external inputs such as:
- invoice-line summary,
- settlement summary,
- contractor-rate summary,
- payroll summary by labor class,
- energy-cost summary,
- debt-service summary.

ImportedFactExtract remains non-ledger by design.

### 7.4 AllocationBasisDeclaration
Required whenever the pack allocates cost or value across scope.
If no acceptable basis exists, the pack should refuse to imply a fine-grain truth claim.

### 7.5 EconomicScenarioResultSet
Carries:
- ranked alternatives or scenario comparison,
- key metrics used,
- main driver explanation,
- uncertainty and sensitivity posture,
- refusal or caution flags where basis is too weak.

---

## 8. Allowed economic method posture

### 8.1 Strongly supported as bounded Advisory methods
- partial budgets / relevant-cost comparisons,
- break-even price and break-even yield framing,
- return per scarce resource or bottleneck unit,
- contractor-versus-own comparisons using explicit assumptions,
- enterprise-budget style planning in Scenario 2+,
- rolling forecast comparison in Advisory,
- capex pre-gate screening with explicit downside cases.

### 8.2 Allowed only with visible caution and basis disclosure
- gross margin,
- contribution margin,
- activity-based allocation for improvement analysis,
- benchmark comparison,
- trend analysis on partial-finance data.

### 8.3 Must not be presented as fine-grain observed truth
- fully allocated field profitability unless the allocation basis is visible and clearly advisory,
- whole-farm finance ratios pushed down to field truth.

### 8.4 Should remain mostly external or at least connector-fed
- full NPV/IRR investment models using rich financing structure,
- statutory or lender-grade cash-flow models,
- debt covenant monitoring that depends on authoritative accounting posture.

The pack may help stage or summarize these.
It should not claim to replace the systems or models that own them.

---

## 9. Guardrails tightened after hostile review

### 9.1 No second query model inside the economics pack
EconomicScenarioSpec may not smuggle in hidden retrieval semantics.
It references governed queries/basis objects rather than redefining query law.

### 9.2 No fake current state
Scenario results are advisory results, not farm “economic current state.”
Any UI or cache pattern that makes them behave like stable current-state truth should be treated as a conformance failure.

### 9.3 No soft autopilot bridge
Economic bridge candidates remain proposal-shaped and human-gated.
The pack must resist convenience workflows that effectively auto-promote scenario outputs into governed decisions.

### 9.4 No accounting growth inside ImportedFactExtract
Account hierarchies, posting correction workflow, reconciliation states, and close-process semantics are out.

---

## 10. Minimum view and output set

Recommended first-wave ViewModules and DocumentAssemblies:

### 10.1 ViewModules
- `CropSystemRankingViewModule`
- `IncrementalChangeViewModule`
- `BreakEvenThresholdViewModule`
- `CapacityReturnViewModule`
- `PostHarvestRoutingViewModule`
- `WholeFarmAdvisoryTrendViewModule`

### 10.2 Frozen outputs
- `EconomicScenarioReportAssembly`
- `CapexPreGateDossierAssembly`

PassportView should be used only where the result is a concise scope summary rather than a decision packet.
An “economic passport” must not become a blanket family.

---

## 11. Import posture

External accounting or ERP payloads should normally land as:
- ImportedFactExtracts,
- evidence links,
- draft material where a governed bridge is needed.

Imported finance may support:
- better scenarios,
- trend updates,
- tighter break-even ranges,
- cash-flow and debt-service advisory outputs,
- stronger capex screening dossiers.

Imported finance may **not** imply automatically:
- field-level profit fact,
- accepted compliance fact,
- authoritative current state,
- or ERP ownership transfer into OFARM.

---

## 12. Promotion posture

This pack note is small enough for companion-artifact discussion because it narrows the economics scope and names the anti-ERP boundary.

The contract layer under it remains experimental until spike + conformance evidence proves it deserves RFC/machine-contract promotion.
