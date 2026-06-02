# OFARM economic intelligence Lane C — Scenario 3 execution note v0.1

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: concrete execution note for Lane C (capex pre-gate screening) using Scenario-3-style bounded accounting/ERP fact extracts

---

## 1. Purpose

Lane C exists to prove that OFARM can support a **pre-gate capital screen** for a post-harvest line without pretending to perform a full investment appraisal, a lender underwriting packet, or a native ERP workflow.

This lane is intentionally narrow:
- target twin = Advisory only
- output class = DossierAssembly-oriented internal packet only
- basis = operational history + bounded fact extracts + explicit assumptions
- decision type = pre-gate screening for whether full appraisal is justified
- no ledger semantics
- no financing-grade claim
- no automatic go/no-go approval
- no SubmissionAssembly path from this lane

## 2. Minimum data basis

Lane C may use:
- Scenario-1 operational history and facility/throughput basis
- posted settlement and energy-cost summaries
- preliminary financing-term summaries
- explicit downside and working-capital assumptions

This lane still does **not** justify:
- full NPV/IRR/payback claims,
- financing approval,
- lender-ready packet generation,
- statutory accounting semantics,
- crop-margin-only capex shortcuts.

## 3. What this lane is allowed to answer

Allowed answers are screening questions such as:
- is throughput scale likely sufficient to justify paying for fuller appraisal,
- does downside utilization stay above the declared floor,
- is quality fit high enough that the line is not obviously mismatched to the crop stream,
- do existing market channels and working-capital assumptions look non-absurd,
- should the farm prepare an internal pre-gate dossier and escalate outward.

## 4. What this lane must refuse

This lane must refuse or downgrade all of the following:
- approval language,
- NPV / IRR / payback / bankability claims,
- lender-ready or financing-ready wording,
- stale dossier export for high-consequence use,
- any claim that crop-level economics alone justifies the investment.

## 5. Lane C execution method

1. Bind operational basis for throughput, quality fit, loss, and facility hours.
2. Import only bounded finance extracts needed for the screening question.
3. Declare downside and working-capital assumptions explicitly.
4. Compute base and downside eligible-throughput utilization.
5. Screen quality fit, market access, energy intensity, and working-capital pressure.
6. Emit a `DOSSIER_PREP` result set with explicit insufficiency language.
7. Emit a human-gated `BridgeCandidate` only for an internal DossierAssembly preparation step.
8. Require full external appraisal before any approval or financing path.

## 6. Required refusal text

Any user-facing result produced from Lane C must contain language equivalent to:

> Screening only. Not financing truth. Full external appraisal required before approval or lender use.

## 7. Deliverables in this lane package

- sample Scenario-3 capex pre-gate dataset
- evaluator script
- generated example result set
- generated summary note
- positive lane-c screening contract examples
- negative financing-grade claim example
- updated top-level economics validator with Lane-C honesty checks
- validator results

## 8. Promotion consequence

Lane C passing does **not** justify baseline or RFC promotion.
It only shows that the bounded native Advisory seam can support a dossier-shaped pre-gate screen without collapsing into full appraisal or ERP semantics.
