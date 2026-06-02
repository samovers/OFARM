# OFARM advisory cohort benchmark hostile test matrix v0.1

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: hostile cases that the advisory cohort benchmark spike must survive before any broader implementation proceeds

---

| Case | Risk | Expected control | Current artifact coverage |
|---|---|---|---|
| Small exact-product cohort | Likely re-identification | `SUPPRESS` or `BROADEN` | disclosure decision examples + runtime disclosure records |
| Dominant contributor | Single participant inference | dominance threshold blocks exposure | disclosure decision examples + validator semantic checks |
| Near-identical repeated narrowing | Differencing attack | differencing guard blocks or requires review | research memo + runtime disclosure records |
| Exact product ambiguous | False comparability | `ProductNormalizationTrace` returns `REFUSED` or `PRODUCT_CLASS` | negative normalization example + validator |
| Mixed unit | False benchmark | refusal for non-normalizable unit | negative normalization/contribution examples + validator |
| Mixed currency without governed FX | False benchmark | refusal for non-comparable currency | negative contribution example + runtime disclosure records |
| Viewer asks for raw rows | tenant-to-tenant leakage | access denied | runtime benchmark sharing boundary records |
| Viewer asks for raw evidence | evidence leakage | access denied | runtime benchmark sharing boundary records |
| Contributor revokes share | stale future use | contribution becomes ineligible for future recompute | runtime benchmark sharing boundary records + validator rule |
| Contribution object drifts into ledger semantics | ERP creep | schema/semantic validation rejects ledger-like keys | negative contribution example + validator |
| Benchmark shows raw peer total spend | overly revealing metric | metric family rejected | negative disclosure example + validator |
| Spend-per-hectare sneaks in | allocation/ERP drift | out of scope in wave 1 | negative contribution/disclosure example + validator |
| Query surface needs group-by/distinct/window | query-law reopening | contribution layer keeps aggregate subset enough | query templates + pre-implementation packet |
| Cached view outlives disclosure safety | stale unsafe reuse | future work: recompute/refusal gate | documented as open limitation |
| Exact product safe, broader class also safe | fallback ambiguity | exact product allowed only when deterministic and safe | positive exact-product bundle |
| Exact product unsafe, broader class safe | wrong refusal | `BROADEN` to product class | runtime disclosure records |
