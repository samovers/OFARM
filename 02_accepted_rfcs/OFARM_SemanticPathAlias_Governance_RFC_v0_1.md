# OFARM SemanticPathAlias Governance RFC v0.1

Date: 2026-04-11  
Status: accepted post-charter RFC  
Scope: formalize governed alias catalogs, explicit alias-resolution traces, and fixture-level cross-target query reproducibility without reopening public query-language design

---

## 1. Problem statement

The active query note and QuerySpecification/QueryPlanIR RFC already say the right high-level thing:
- `SemanticPathAlias` is governed shorthand rather than a hidden second schema
- aliases should be versioned
- stale or ambiguous alias resolution should fail clearly rather than guess
- `QueryPlanIR` should carry resolved alias information rather than hiding it in runtime code

That direction is correct.
What is still missing is the actual closure contract for alias governance.

Without that closure, the package still leaves too much drift-prone room around questions such as:
- where governed alias versions are registered
- how deprecated aliases are allowed to roll forward, if at all
- how alias resolution becomes traceable rather than remaining a hidden runtime convention
- how ambiguity hard-fail is made executable
- how one approved query proves the same canonical alias meaning across more than one execution target

This RFC closes that gap with a narrow query-governance patch.

It does **not** reopen OFARM’s internal-model-first query posture.
It makes the already-required alias-governance layer explicit.

---

## 2. Core stance

### 2.1 Alias governance closes reproducibility risk, not public syntax
This RFC is about governed meaning and reproducibility.
It is **not** a public expert text-language RFC.

The canonical query artifact remains `QuerySpecification`.
The canonical runtime planning artifact remains `QueryPlanIR`.

### 2.2 Governed alias meaning comes from catalogued versions, not runtime convention
A `SemanticPathAlias` used in a query should resolve through a governed alias catalog rather than through undocumented runtime defaults.

This means the platform should be able to explain:
- which catalog governed the alias
- which alias version was requested
- which canonical alias version was ultimately applied
- which semantic target was resolved

### 2.3 High-consequence use should be version-pinned
For high-consequence or approved-query use, alias resolution should be version-pinned.

If the runtime receives an unpinned alias in a high-consequence posture, it should fail clearly rather than infer meaning from ambient convention.

### 2.4 Deprecated aliases may roll forward only through explicit trace
A deprecated alias version may still be accepted when the governing catalog declares an exact canonical successor.

But that rollover must be:
- explicit
- traceable
- warning-bearing
- reproducible

It must not be silent.

### 2.5 Ambiguity and stale alias meaning should hard-fail
If more than one active alias meaning could plausibly satisfy the same query alias reference and the query has not pinned the version precisely enough, the platform should fail clearly.

The runtime should prefer an explainable refusal over guessed meaning.

### 2.6 Cross-target execution must preserve canonical alias meaning
The same approved `QuerySpecification` may compile into more than one `QueryPlanIR`.
That runtime freedom is acceptable only if the canonical resolved alias meaning stays the same across targets.

---

## 3. Formal artifacts produced by this RFC

This RFC creates:

- **OFARM SemanticPathAliasCatalog schema v0.1** (`ofarm.semanticpathaliascatalog.v0.1`)
- **OFARM SemanticPathAliasResolutionTrace schema v0.1** (`ofarm.semanticpathaliasresolutiontrace.v0.1`)

This RFC also introduces executable example payloads for:
- active version-pinned alias resolution
- deprecated alias rollover with explicit canonical successor
- ambiguity hard-fail when an alias is not pinned tightly enough
- two semantically equivalent `QueryPlanIR` variants for the same approved query across different execution targets

---

## 4. What a SemanticPathAliasCatalog means

### 4.1 One catalog = one governed alias registry posture
A `SemanticPathAliasCatalog` is the governed registry of alias versions for a declared artifact/profile posture.

It records which alias versions exist, which are active, which are deprecated, and which canonical semantic targets they resolve to.

### 4.2 Minimum entry expectations
At minimum, a catalog entry should make explicit:
- alias name
- alias version reference
- alias status
- root concept
- governed path reference
- semantic target kind
- resolved semantic target reference
- semantic equivalence group
- governing artifact references

### 4.3 Deprecated alias versions remain real historical objects
A deprecated alias version should not be erased.

If a system must explain how an older approved query was interpreted, the deprecated version still needs to be traceable, together with any declared canonical successor.

### 4.4 Catalogs do not replace the semantic substrate
A catalog is not a second ontology and not a hidden schema store.
It is a governed registry that points into already-governed semantic meaning.

---

## 5. What a SemanticPathAliasResolutionTrace means

### 5.1 ResolutionTrace is the explanation object for alias binding
A `SemanticPathAliasResolutionTrace` records how a query alias reference was resolved, warned, or refused.

It is the minimum machine-readable explanation object for:
- requested alias version
- matched catalog entry
- canonical alias version used
- resolved semantic target
- warnings or failure posture

### 5.2 Success cases
For a successful resolution, the trace should make clear:
- which catalog governed the binding
- whether the resolution was direct or via deprecated rollover
- the canonical alias version ultimately used
- the semantic equivalence group preserved

### 5.3 Failure cases
For a failure, the trace should still make the refusal explainable.

At minimum, the trace should be able to record:
- ambiguity failure
- version-pin-required failure
- path mismatch failure
- alias-not-found failure

### 5.4 Relation to QueryPlanIR
`QueryPlanIR.resolvedPathAliases` remains the runtime planning contract.

A `SemanticPathAliasResolutionTrace` does not replace it.
Instead, the trace makes the governed alias-binding decision explainable and reproducible, while `QueryPlanIR` remains the execution-planning artifact that should reflect that canonical binding.

---

## 6. Version pinning, deprecation, and ambiguity rules

### 6.1 Version pinning
For approved/high-consequence query use:
- the query should carry an `aliasVersionRef`
- the runtime should resolve that exact alias version or fail clearly

### 6.2 Deprecated rollover
A deprecated alias version may resolve to an exact canonical successor only when:
- the catalog declares that successor
- the runtime records the rollover explicitly
- the warning posture is retained in the trace

### 6.3 Ambiguity hard-fail
If an alias request is not pinned tightly enough and more than one active meaning remains plausible, the runtime should emit an ambiguity failure instead of selecting one candidate implicitly.

### 6.4 No silent alias migration
The platform must not silently rewrite historical approved queries as though they had always used the newest alias version.
If migration is desired, it should produce a new governed query artifact or an explicit trace of canonical successor binding.

---

## 7. Conformance posture

This RFC is intentionally a closure artifact.
It should be implemented with:
- machine-validatable alias catalog and alias-resolution-trace schemas
- grounded example payloads for active, deprecated, and ambiguous cases
- fixture-level checks confirming:
  - version-pinned resolution stays stable
  - deprecated rollover remains explicit
  - ambiguity hard-fails
  - two execution-target plans preserve the same canonical alias meaning

This wave is intentionally narrow.
It does **not** claim:
- a public expert query language
- full saved-query migration workflows
- full executor-backed equivalence over all future query patterns

Those remain later work.

---

## 8. Non-goals and safety guardrails

### 8.1 No public syntax freeze
This RFC must not be used to back-door a public query-language standard.

### 8.2 No hidden runtime alias conventions
Runtime code, index layout, or adapter defaults must not redefine canonical alias meaning outside the governed catalog and trace layer.

### 8.3 No alias blobs as substitute for model law
The catalog must point into governed semantic meaning; it must not become a free-floating alternate schema.

### 8.4 No fake equivalence claims
Cross-target equivalence claims must remain bounded and explicit.
A fixture-level equivalence result in this wave does not prove every future executor path is equivalent.
