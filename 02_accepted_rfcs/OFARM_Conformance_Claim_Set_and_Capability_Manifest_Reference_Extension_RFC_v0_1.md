# OFARM Conformance Claim Set and Capability Manifest Reference Extension RFC v0.1

Date: 2026-04-10  
Status: accepted RFC extension  
Scope: formalize a separate `ConformanceClaimSet` contract and extend Capability Manifest references without turning the manifest into a second ontology

---

## 1. Problem statement

The active Capability Manifest RFC already made the correct high-level move:
- keep the manifest machine-readable
- keep it comparable
- keep it narrow
- ground it in registry relation and active artifact state

That posture is correct.
The remaining gap is:
- the minimal conformance block is too small for comparable standard-readiness claims across deployments
- detailed claims do not yet have a first-class contract
- the Alignment Register is the wrong place to store deployment-facing conformance taxonomy
- runtime surfaces and substrate/profile claims need a reference path that does not bloat the top-level manifest

This RFC closes that gap.

---

## 2. Core stance

### 2.1 Conformance taxonomy is separate from the Alignment Register
The Alignment Register remains a semantic-core artifact.
Deployment or pack conformance claims belong in a dedicated `ConformanceClaimSet` contract.

This RFC fixes four first-order claim families:
- `SEMANTIC_SUBSTRATE`
- `PROFILE`
- `MAPPING`
- `RUNTIME_SURFACE`

### 2.2 Capability Manifest stays narrow by reference
The Capability Manifest should keep its current top-level shape.
It may add references to:
- a `SemanticSubstrateBundle`
- a `ConformanceClaimSet`
- governed runtime surface contracts
- coverage/loss artifacts for declared mapping surfaces

That preserves the “contract, not ontology blob” rule.

### 2.3 Claims must be grounded in active state and tests
A meaningful conformance claim should be traceable to:
- the active artifact state
- the relevant profile or mapping artifact
- one or more declared test suites where verification is claimed

---

## 3. Formal artifacts produced by this RFC

This RFC defines:
- **OFARM ConformanceClaimSet schema v0.1** (`ofarm.conformanceclaimset.v0.1`)
- **OFARM ConformanceClaimSet example partner deployment v0.1**
- **OFARM Capability Manifest schema v0.2 draft**
- **OFARM Capability Manifest example core deployment v0.2 draft**

---

## 4. ConformanceClaimSet schema decisions

### 4.1 Mandatory top-level fields
A valid `ConformanceClaimSet` should include at minimum:
- `schemaVersion`
- `claimSetId`
- `subjectRef`
- `generatedAt`
- `activeArtifactSetRef`
- `claims`

### 4.2 Claim entries
Each claim entry should identify at minimum:
- `claimId`
- `claimFamily`
- `targetRef`
- `status`

Optional references may include:
- `conformanceClassRef`
- `testSuiteRefs`
- `profileRefs`
- `evidenceRefs`

This is enough to compare two deployments without turning conformance into free text.

---

## 5. Capability Manifest v0.2 draft patch decisions

### 5.1 Registry relation stays the grounding core
The existing registry relation remains mandatory.
The draft adds optional references for:
- `semanticSubstrateBundleRef`
- `conformanceClaimSetRef`

These do not replace `activeArtifactSetRef`.
They extend it.

### 5.2 Pack-surface support expands narrowly
The draft updates `supportedSurfaceFamilies` so the manifest can declare support for:
- `IMPORT_EXPORT_MAPPING`
- `RUNTIME_SURFACE_CONTRACT`

### 5.3 Declared surfaces stay compact but become more usable
The draft keeps `importExportSupport.declaredSurfaces` as the surface declaration array.
It adds optional references for:
- `contractRef`
- `coverageStatementRef`
- `lossMapRef`
- `serviceDescriptionRefs`

That is enough to make declared surfaces actionable without turning the manifest into a registry dump.

### 5.4 Discovery support is referenced, not embedded
The draft allows discovery surfaces to be declared through the same surface array.
This keeps `.well-known` or equivalent discovery posture explicit without adding a second discovery subsystem to the manifest.

---

## 6. Comparison meaning

With this extension, tools can compare deployments on questions such as:
- do these deployments depend on the same substrate bundle
- do they claim the same external profile conformance family
- do they expose the same mapping/runtime surfaces
- are those claims merely declared, or backed by named test suites

This is the missing comparison layer that the minimal v0.1 conformance block cannot yet provide by itself.

---

## 7. Main patch consequences

If promoted, this RFC implies:
- no Alignment Register expansion for runtime/deployment conformance claims
- a narrow Platform patch to mention referenced substrate/claim-set support
- a new Capability Manifest draft schema version rather than an unbounded v0.1 expansion
- better comparability of external-standard-readiness claims across deployments

---

## 8. Hard stop question

Should OFARM broaden Capability Manifest content every time a new interoperability claim appears, or should it keep the manifest narrow and reference detailed claim sets?

This RFC’s answer is:
- keep the manifest narrow
- reference the detailed claim sets
- keep comparison grounded in active state and tests
