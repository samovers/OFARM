# OFARM Runtime Pack Merge and Surface Legality Fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation fixture set  
Scope: runtime-shaped legality and deterministic-outcome checks for all governed pack-merge surface families

---

## 1. Purpose

These fixtures close the remaining pack-merge conformance cluster by turning the RFC-3 merge-law families into executable runtime-shaped cases.

The target families are:

- VOCABULARY_BINDINGS
- EVIDENCE_POLICY
- ARCHETYPE_DEFINITION
- TEMPLATE_CONSTRAINT
- VALIDATION_RULE
- DECISION_RULE
- EVENT_SUBTYPE_DEFINITION
- VIEW_SHAPING
- DOCUMENT_ASSEMBLY_SHAPING

---

## 2. Positive legality fixtures

### Vocabulary bindings
- disjoint additive union allow
- non-empty narrowing intersection allow

### Evidence policy
- cumulative strongest-requirement allow

### Archetype definition
- identical-only coexistence allow

### Template constraint
- monotone narrowing intersection allow

### Validation rule
- conjunctive validation intersection allow

### Decision rule
- ordered composition allow with higher-precedence primary rule and lower non-conflicting enrichment

### Event subtype definition
- disjoint subtype additive union allow
- same-subtype ordered enrichment allow with stable family identity

### View shaping
- additive PassportView shaping allow
- ordered PassportView composition allow

### Document assembly shaping
- additive DocumentAssembly appendix allow
- ordered frozen-assembly composition allow

---

## 3. Negative legality fixtures

### Vocabulary bindings
- conflicting mandatory code-system binding hard fail

### Evidence policy
- required-versus-prohibited evidence contradiction hard fail

### Archetype definition
- divergent archetype definition hard fail

### Template constraint
- impossible cardinality combination hard fail

### Validation rule
- contradictory validation logic hard fail

### Decision rule
- competing decision key without ordered composition hard fail

### Event subtype definition
- same subtype key attached to different top-level families hard fail

### View shaping
- conflicting live slot semantics hard fail

### Document assembly shaping
- conflicting attested slot/section hard fail

---

## 4. Determinism requirement

Each scenario is evaluated twice at the outcome layer.
The emitted result must remain stable for:

- merge mode
- activation outcome
- compatibility class
- reason code

No scenario may degrade into hidden operator choice or silent partial activation.
