# OFARM Advisory Scenario and Economic Output Taxonomy Addendum v0.2

Date: 2026-04-12  
Status: active companion artifact  
Scope: prevent scenario and economics outputs from corrupting the existing PassportView / DocumentAssembly taxonomy

---

## 1. Purpose

The active compiled-output taxonomy already separates:
- live/recomputable PassportViews,
- frozen DocumentAssemblies,
- ReportAssembly / DossierAssembly / SubmissionAssembly subfamilies.

Economics and scenario work creates a drift risk:
- live scenario views start being called “passports”,
- frozen economic summaries start being called “passports”,
- lender or capex packets start being treated as generic reports without dossier semantics.

This addendum shuts that down.

---

## 2. Core stance

### 2.1 “Economic passport” is not a top-level family
OFARM should not create a blanket “economic passport” family.

Economics outputs are usually:
- assumption-bearing,
- comparative,
- decision-oriented,
- or frozen purpose packets.

That does not fit the stable scope-summary role of PassportView.

### 2.2 Scenario comparison is a view concern first
Live comparison of scenarios should normally be realized as:
- QuerySpecifications,
- one or more ViewModules,
- optionally a saved scenario-comparison view.

It should not be forced into PassportView merely because it is shareable.

### 2.3 Frozen economic/advisory outputs are usually documents
When scenario or economics output is frozen for a purpose, it should normally be a DocumentAssembly subtype.

---

## 3. Recommended mapping

### 3.1 Live scenario workspace output
Use:
- ViewModule,
- saved view,
- result profile.

Typical examples:
- crop/system ranking comparison,
- break-even threshold view,
- constraint/capacity scenario comparison,
- downside-sensitivity view.

### 3.2 Concise scope-centric operational intensity summary
Use:
- PassportView only if the output is primarily a concise scope summary
- and not primarily a scenario comparison or decision packet.

### 3.3 Frozen seasonal or tactical economics summary
Use:
- ReportAssembly.

### 3.4 Capex pre-gate, lender, or investment-screen packet
Use:
- DossierAssembly where evidence, assumptions, downside cases, and insufficiency markers matter.

### 3.5 Formal filing or external delivery packet
Use:
- SubmissionAssembly where a governed filing/delivery process is the purpose.

---

## 4. Hard anti-drift rules

1. A live scenario comparison must not be relabeled as PassportView merely because it is portable.
2. A frozen decision packet must not stay a view just because it was first explored live.
3. A lender/capex packet should not be flattened into generic “report” if dossier semantics are materially present.
4. “Economic passport” and “scenario passport” should be treated as anti-pattern vocabulary.

---

## 5. Why this addendum is safe to promote early

This addendum does not reopen architecture.
It simply protects an already-decided taxonomy boundary from immediate economics-driven drift.

That makes it a good candidate for earlier companion-artifact adoption than the contract layer below it.
