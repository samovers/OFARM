# OFARM Pack Merge Semantics RFC v0.1

Date: 2026-04-08  
Status: accepted post-charter RFC  
Scope: formalize what “declared safe merge” means for different pack surface families so pack composition becomes implementable rather than only policy-level

---

## 1. Problem statement

RC2 and the Pack Safety Policy already say:

- packs may be active together
- packs declare touched surfaces
- same-precedence conflicts require:
  - declared safe merge, or
  - hard fail

That is a good policy layer.
It is not yet an implementation-grade contract.

The missing question is:

**What counts as a safe merge for each surface family?**

Without that, “declared safe merge” is still partly hand-waving.

This RFC closes that gap for the first priority surface families:
- vocabulary/code bindings
- evidence policies
- archetypes/templates
- validation rules
- decision rules
- event subtype definitions
- view/passport/document shaping

---

## 2. Core stance

### 2.1 Merge is surface-specific
There is no single generic merge rule that works for every artifact family.

A safe merge for:
- a vocabulary binding
- a template constraint
- an evidence policy
- a decision rule
- a view section

are different things.

### 2.2 Merge must preserve constitutional meaning
A merge is safe only if it preserves:
- semantic clarity
- determinism
- auditability
- precedence discipline
- traceability

If a merge would require hidden interpretation or runtime guesswork, it is not safe.

### 2.3 Default safety bias
If OFARM lacks a declared surface-specific safe merge path, the default remains:
- do not guess
- do not silently merge
- hard fail or require governance

---

## 3. Surface families

This RFC fixes these baseline **PackSurfaceFamily** values:

- **VOCABULARY_BINDINGS**
- **EVIDENCE_POLICY**
- **ARCHETYPE_DEFINITION**
- **TEMPLATE_CONSTRAINT**
- **VALIDATION_RULE**
- **DECISION_RULE**
- **EVENT_SUBTYPE_DEFINITION**
- **VIEW_SHAPING**
- **DOCUMENT_ASSEMBLY_SHAPING**

The family matters because it determines which merge modes are even legal.

---

## 4. Merge modes

This RFC fixes these baseline **PackSurfaceMergeMode** values:

### 4.1 ADDITIVE_UNION
Safe when items are disjoint and may coexist without changing each other’s meaning.

### 4.2 CONSTRAINT_INTERSECTION
Safe when multiple constraints may be applied together by logical narrowing.

### 4.3 STRONGEST_REQUIREMENT
Safe when multiple requirements can be combined by taking the stricter or cumulative requirement set.

### 4.4 ORDERED_COMPOSITION
Safe when composition is explicitly ordered and the order is semantically governed.

### 4.5 IDENTICAL_ONLY
Safe only when the overlapping definition is the same in all relevant meaning-bearing respects.

### 4.6 HARD_FAIL
No safe merge exists for the overlapping case.

---

## 5. Surface-specific merge semantics

### 5.1 VOCABULARY_BINDINGS

#### Safe cases
Use **ADDITIVE_UNION** when:
- the bindings target different concept slots
- the bindings target different code keys without overlap
- the overlapping binding is semantically identical

Use **CONSTRAINT_INTERSECTION** when:
- two packs both narrow the allowed value set for the same slot
- the resulting intersection is non-empty
- the resulting intersection does not contradict higher-precedence constraints

#### Unsafe cases
Use **HARD_FAIL** when:
- the same slot is bound to mutually incompatible mandatory code systems
- the same key is given conflicting exact semantic meaning
- narrowing would produce an empty allowed set
- the system cannot prove semantic compatibility

### 5.2 EVIDENCE_POLICY

#### Safe cases
Use **STRONGEST_REQUIREMENT** when:
- multiple packs require additional evidence for the same action/path
- requirements can be accumulated without contradiction
- one pack narrows sufficiency by adding conditions or stronger proof

This means:
- required evidence sets usually combine cumulatively
- optional evidence remains optional unless another pack upgrades it
- stronger retention or attestation requirements win

#### Unsafe cases
Use **HARD_FAIL** when:
- one pack requires an evidence type that another explicitly prohibits for the same path
- one pack requires a retention/attestation mode that another makes impossible
- sufficiency logic becomes contradictory and no higher-precedence resolution exists

### 5.3 ARCHETYPE_DEFINITION

#### Safe cases
Use **IDENTICAL_ONLY** when:
- the same archetype identifier appears in multiple packs but the definition is materially the same

#### Unsafe cases
Use **HARD_FAIL** when:
- two packs define materially different versions of the same archetype identifier
- one pack attempts to locally rewrite another archetype’s semantic structure
- a merge would create a silent fork of the archetype

Reason:
- archetypes are identity-bearing content artifacts
- they are not meant to be casually merged like config snippets

### 5.4 TEMPLATE_CONSTRAINT

#### Safe cases
Use **CONSTRAINT_INTERSECTION** when:
- packs constrain the same base template or same archetype-derived node set
- constraints are monotone/narrowing
- the resulting template remains structurally valid
- the result does not create impossible or contradictory cardinality/type/binding requirements

Examples:
- both packs make a field required
- both packs narrow allowed values and the intersection remains valid
- one pack adds a stricter max length while another adds a stricter format, if both can hold

#### Unsafe cases
Use **HARD_FAIL** when:
- constraints operate on incompatible base templates
- structural/cardinality constraints become contradictory
- node typing becomes incompatible
- the result is not machine-validatable

### 5.5 VALIDATION_RULE

#### Safe cases
Use **CONSTRAINT_INTERSECTION** when:
- validation rules can be applied conjunctively
- both rules target the same object path but simply add more checks
- all checks may hold together

This effectively means:
- all relevant validations must pass

#### Unsafe cases
Use **HARD_FAIL** when:
- validations are explicitly contradictory
- one rule requires what another forbids for the same validated state
- the runtime cannot prove a coherent combined validation policy

### 5.6 DECISION_RULE

#### Safe cases
Use **ORDERED_COMPOSITION** only when:
- decision rules are partitioned by distinct decision keys, or
- explicit ordered composition is declared, or
- higher-precedence rule is clearly primary and the lower one only enriches non-conflicting outputs

#### Unsafe cases
Use **HARD_FAIL** when:
- multiple rules compete for the same decision key with no explicit ordered composition
- rule outcomes could diverge materially without a declared arbitration policy
- precedence alone is not enough to explain the decision path

Reason:
- decision logic is not just another list to union
- silent parallel decisioning destroys reproducibility

### 5.7 EVENT_SUBTYPE_DEFINITION

#### Safe cases
Use **ADDITIVE_UNION** when:
- packs define different subtype identifiers under the same top-level family

Use **ORDERED_COMPOSITION** or limited additive enrichment when:
- packs enrich the same subtype with additional attributes/evidence/workflow metadata
- the top-level family remains the same
- no attribute meaning conflicts
- enrichment can be traced by source pack

#### Unsafe cases
Use **HARD_FAIL** when:
- the same subtype is attached to different top-level families
- the same attribute key is given incompatible semantics
- one pack redefines another subtype’s core meaning
- subtype identity or lineage becomes ambiguous

### 5.8 VIEW_SHAPING

#### Safe cases
Use **ADDITIVE_UNION** when:
- packs add disjoint sections, panels, or fields to the same view family

Use **ORDERED_COMPOSITION** when:
- view assembly explicitly supports ordered section composition
- slot ownership stays unambiguous

#### Unsafe cases
Use **HARD_FAIL** when:
- the same output slot or field key is mapped to conflicting semantics
- the same section key is defined incompatibly
- the merge would make the view non-deterministic

### 5.9 DOCUMENT_ASSEMBLY_SHAPING

#### Safe cases
Use **ADDITIVE_UNION** for:
- disjoint required sections or appendices

Use **ORDERED_COMPOSITION** when:
- assembly order is explicitly governed
- section ownership and attestation implications remain clear

#### Unsafe cases
Use **HARD_FAIL** when:
- the same attested slot/section has conflicting definitions
- output purpose becomes ambiguous
- assembly would produce non-deterministic or semantically conflicting frozen outputs

Reason:
- frozen outputs have stronger governance weight than live views
- merge tolerance should therefore be lower

---

## 6. Precedence interaction

### 6.1 Same-precedence rule
Within the same precedence class:
- apply the allowed surface-specific merge mode if declared and safe
- otherwise hard fail

### 6.2 Cross-precedence rule
Across precedence classes:
- higher precedence still wins
- lower precedence may only enrich where its surface-specific merge mode remains safe and non-contradictory
- if not, hard fail rather than silently degrade

### 6.3 Higher precedence is not universal license
Higher precedence does **not** mean a pack may rewrite constitutional law or force an unsafe merge.
Precedence decides conflicts inside allowed surfaces.
It does not legalize forbidden behavior.

---

## 7. PackMergeResolutionTrace

A safe runtime needs a traceable merge decision object.

This RFC introduces **PackMergeResolutionTrace** as the runtime-governed trace of:
- compared packs
- affected PackActivationSet
- surface family
- merge mode applied
- precedence relationship
- resulting outcome
- reason for hard fail or governance requirement where relevant

This does not need to become a giant permanent artifact in every case.
But the platform must be able to produce it when explainability matters.

---

## 8. Minimal conformance expectations

A conforming implementation should be able to determine, for the covered surface families:

- which surface family is being merged
- which merge mode is legal for that family
- whether the overlap is safe, unsafe, or governance-required
- what the resulting merged meaning is, or why hard fail occurs
- what trace explains that merge decision

At minimum, conformance fixtures should include:
- disjoint vocabulary binding union
- conflicting mandatory code-system binding hard fail
- cumulative evidence-policy merge
- required-versus-prohibited evidence hard fail
- identical archetype coexistence
- divergent archetype definition hard fail
- monotone template narrowing merge
- conflicting template cardinality hard fail
- conjunctive validation merge
- conflicting decision rule hard fail
- additive event subtype enrichment
- subtype family mismatch hard fail
- additive PassportView section merge
- conflicting DocumentAssembly slot hard fail

---

## 9. Main patch consequences

This RFC requires:
- Constitution patching in section 6 and conformance direction
- Pack Safety and Compatibility Policy update
- Platform patching in package/runtime merge evaluation and trace
- Alignment Register update for merge-surface concepts
- example merge fixtures

---

## 10. Hard stop question

The RFC succeeds only if the system can answer, for a concrete same-scope pack overlap:

**Which surface family is in conflict, which merge mode is legally allowed here, and why does the runtime merge or hard fail?**
