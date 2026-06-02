# OFARM research — advisory cohort benchmark product normalization v0.1

Date: 2026-04-15
Status: active supporting research
Scope: first-wave product normalization posture for receipt-backed cohort benchmark contributions

---

## 1. Purpose

This memo defines how receipt-backed invoice-line extracts can support benchmarking without pretending that OCR text is already governed product identity.

---

## 2. Normalization chain

Wave 1 should use this chain:
1. receipt/document captured as evidence
2. OCR or parsing used only as helper
3. reviewed invoice-line extract created
4. `ProductNormalizationTrace` created
5. `BenchmarkContribution` derived only if normalization and comparability pass
6. disclosure-controlled benchmark decision evaluated

---

## 3. Required outcomes

A product normalization attempt must end in exactly one of these states:
- `EXACT_PRODUCT`
- `PRODUCT_CLASS`
- `REFUSED`

### EXACT_PRODUCT
Use only when reviewed text, code bindings, packaging/unit semantics, and formulation/treatment markers are stable enough.

### PRODUCT_CLASS
Default fallback when exact product is not reliable enough but a governed product class remains comparable.

### REFUSED
Use when ambiguity or non-comparability would make the benchmark misleading.

---

## 4. Fertilizer posture

For fertilizer, wave 1 should prefer governed product classes such as a formulation class when:
- package sizes differ but normalized quantity is comparable,
- invoice text varies across suppliers,
- exact product branding would over-fragment the cohort.

Refuse when:
- unit cannot be normalized,
- formulation differences break comparability,
- the line merges product with service/freight in a way that prevents safe separation.

---

## 5. Seed posture

For seed, exact product is somewhat more plausible than fertilizer only when:
- the hybrid/variety marker is reviewed,
- treatment status is known,
- package size is normalized,
- the cohort remains large enough after exact normalization.

Otherwise broaden to product class or refuse.

---

## 6. Currency and unit comparability

Wave 1 should refuse when:
- currency is mixed and no governed FX posture exists,
- units are mixed and cannot be normalized,
- package/treatment/formulation differences break comparability,
- tax/freight/discount treatment cannot be separated consistently enough.

---

## 7. Why the trace object should stay separate

`ProductNormalizationTrace` should remain separate from `ImportedFactExtract` because:
- it preserves raw-versus-interpreted discipline,
- it makes ambiguity visible,
- it avoids treating OCR/output text as governed truth,
- it supports exact-product fallback to product-class without mutating the original extract.

---

## 8. Bottom line

The amendment only stays honest if product identity is treated as a reviewed interpretation layer with explicit refusal behavior, not as a silent by-product of receipt parsing.
