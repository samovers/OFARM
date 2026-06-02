# OFARM research — advisory cohort benchmark capability v0.1

Date: 2026-04-15
Status: active supporting research
Scope: narrowed capability framing after critical evaluation for the advisory cohort spend benchmark seam

---

## 1. Purpose

This memo replaces the loose idea of “show me what other anonymized tenants spent” with a bounded OFARM capability shape that fits the active baseline and the critical evaluation.

The capability is a **disclosure-controlled Advisory benchmark view**, not direct tenant-to-tenant spend visibility.

---

## 2. Working capability statement

A tenant/farm user may view a disclosure-controlled Advisory benchmark for a governed fertilizer or seed product class, or an exact normalized product only when normalization and cohort-safety rules pass, based on explicitly opted-in reviewed contribution artifacts derived from receipt-backed invoice-line extracts. The user never receives raw tenant rows or raw evidence through this capability.

---

## 3. First-wave user outcome

Wave 1 should expose only a small benchmark card/view with fields such as:
- average price per normalized unit
- quantity band
- optional position band relative to the cohort
- product/product-class basis
- evidence posture
- freshness posture
- contributor-count band or hidden contributor posture

The user outcome is therefore a **benchmark explanation surface**, not a cross-tenant ledger summary.

---

## 4. Mandatory boundaries

The capability must remain:
- Advisory only
- explicit-share only
- query/view first
- cohort-level only
- disclosure-controlled
- evidence-postured
- revocable for future use
- traceable to reviewed extracts and normalization decisions

The capability must not become:
- raw row-level peer visibility
- farm-to-farm compliance truth exposure
- a second query language
- a second truth store
- a procurement/accounting subsystem
- a new passport family

---

## 5. Mandatory share topology

Wave 1 requires a two-leg share path.

### Leg 1 — contributor to benchmark operator/service
The contributor grants the benchmark operator/service read/use of reviewed extract and normalization-basis artifacts strictly for benchmark contribution generation.

### Leg 2 — benchmark operator/service to viewer
The viewer receives only the benchmark card/view/report under `RECEIVE_READ_DATA` authority. Raw evidence and raw contribution rows remain denied.

### Revocation
Contributor revocation blocks future contribution use and future recompute. Already issued frozen reports remain governed by prospective revocation law.

---

## 6. Wave-1 metric family

Wave 1 should be limited to the following user-visible metrics:
- `AVG_UNIT_PRICE`
- `QUANTITY_BAND`
- optional `POSITION_BAND`

Wave 1 is explicitly **not** the place for:
- raw peer total spend
- spend per hectare
- exact contributor counts
- min/max exposure
- percentiles/distributions

---

## 7. Product identity posture

Wave 1 defaults to **product-class benchmarking**.
Exact product is allowed only when:
- normalization is reviewed and deterministic enough,
- unit/currency comparability passes,
- cohort size passes,
- dominance checks pass,
- differencing risk is clear.

If exact product is not safe, the system must broaden to product class or refuse.

---

## 8. File impact

### Affected baseline files
None.

### Change type
- supporting research implication
- implementation/conformance implication

### Next controlled patch
`04_implementation_and_conformance/` experimental spike only.

---

## 9. Bottom line

The amended capability is worth pursuing only as a small **Advisory cohort benchmark seam**. Any pressure to turn it into raw anonymized spend visibility should be treated as a cut-back trigger.
