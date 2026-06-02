# OFARM Pack Merge Semantics Fixtures v0.1

Date: 2026-04-08  
Status: example/conformance fixture set  
Scope: illustrative surface-family merge cases for RFC-3

---

## Fixture 1 — disjoint vocabulary binding union
Packs:
- Slovenia regulatory pack
- Organic pack

Surface:
- VOCABULARY_BINDINGS

Case:
- Slovenia pack binds `submissionCategory`
- Organic pack binds `organicInspectionType`

Expected:
- ADDITIVE_UNION
- merged successfully

---

## Fixture 2 — conflicting mandatory code-system binding
Packs:
- Buyer claim pack A
- Buyer claim pack B

Surface:
- VOCABULARY_BINDINGS

Case:
- both bind the same `claimStatus` slot to different mandatory incompatible code systems

Expected:
- HARD_FAIL

---

## Fixture 3 — cumulative evidence-policy merge
Packs:
- Slovenia pack
- Organic pack

Surface:
- EVIDENCE_POLICY

Case:
- Slovenia pack requires subsidy receipt scan
- Organic pack requires segregation cleanout log
- same submission path needs both

Expected:
- STRONGEST_REQUIREMENT
- both evidence requirements apply

---

## Fixture 4 — required-versus-prohibited evidence contradiction
Packs:
- Pack A requires signed PDF evidence for path X
- Pack B prohibits signed PDF evidence for path X

Surface:
- EVIDENCE_POLICY

Expected:
- HARD_FAIL

---

## Fixture 5 — identical archetype coexistence
Packs:
- Orchard pack
- Regional extension pack

Surface:
- ARCHETYPE_DEFINITION

Case:
- both reference the same archetype id with materially identical definition

Expected:
- IDENTICAL_ONLY
- coexistence allowed

---

## Fixture 6 — divergent archetype definition
Packs:
- Pack A
- Pack B

Surface:
- ARCHETYPE_DEFINITION

Case:
- both define the same archetype id differently

Expected:
- HARD_FAIL

---

## Fixture 7 — monotone template narrowing
Packs:
- Organic pack
- Orchard pack

Surface:
- TEMPLATE_CONSTRAINT

Case:
- both constrain the same base template
- one makes field `cleanoutEvidence` required
- another narrows allowed values for `treatmentMethod`
- no contradiction

Expected:
- CONSTRAINT_INTERSECTION

---

## Fixture 8 — conflicting template cardinality
Packs:
- Pack A requires maxCount=1 for node N
- Pack B requires minCount=2 for node N

Surface:
- TEMPLATE_CONSTRAINT

Expected:
- HARD_FAIL

---

## Fixture 9 — conjunctive validation merge
Packs:
- Pack A validates date ordering
- Pack B validates lot reference presence

Surface:
- VALIDATION_RULE

Expected:
- CONSTRAINT_INTERSECTION

---

## Fixture 10 — conflicting decision rules
Packs:
- Pack A decision rule for `eligibilityDecision`
- Pack B different decision rule for same `eligibilityDecision`
- no explicit ordered composition

Surface:
- DECISION_RULE

Expected:
- HARD_FAIL

---

## Fixture 11 — additive event subtype enrichment
Packs:
- Orchard pack
- Organic pack

Surface:
- EVENT_SUBTYPE_DEFINITION

Case:
- both enrich subtype `PruningEvent`
- one adds blossom-thinning attributes
- one adds organic evidence requirements
- same parent family = InterventionEvent
- no semantic conflict

Expected:
- additive enrichment allowed

---

## Fixture 12 — event subtype family mismatch
Packs:
- Pack A defines subtype `FrostProtection`
  under InterventionEvent
- Pack B defines same subtype key under OccurrenceEvent

Surface:
- EVENT_SUBTYPE_DEFINITION

Expected:
- HARD_FAIL

---

## Fixture 13 — additive PassportView shaping
Packs:
- Buyer pack
- Regional benchmark pack

Surface:
- VIEW_SHAPING

Case:
- Buyer pack adds buyer-required lot summary section
- benchmark pack adds optional benchmark panel
- sections are disjoint

Expected:
- ADDITIVE_UNION

---

## Fixture 14 — conflicting DocumentAssembly slot
Packs:
- Submission pack A
- Submission pack B

Surface:
- DOCUMENT_ASSEMBLY_SHAPING

Case:
- both define the same attested slot `declaration.signatory` incompatibly

Expected:
- HARD_FAIL
