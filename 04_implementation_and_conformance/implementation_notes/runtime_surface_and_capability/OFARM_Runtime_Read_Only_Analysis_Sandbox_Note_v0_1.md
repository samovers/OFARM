# OFARM Runtime Read-Only Analysis Sandbox Note v0.1

Date: 2026-04-24  
Status: active supporting implementation artifact  
Scope: define the smallest implementation boundary for a Code-Interpreter-style analysis sandbox that lets a model write Python and perform bounded computation over governed OFARM reads without mutating authoritative truth or creating hidden stores

---

## 1. Purpose

Some user requests need real computation rather than retrieval alone.
Examples include:
- long-range aggregation over authorized history,
- joins between governed OFARM results and explicit user-provided files,
- charting,
- geospatial transforms,
- ranking and optimization,
- simulation over declared assumptions.

The active OFARM baseline already permits runtime freedom in Advisory-oriented services, but it also forbids bypassing query law, forbids direct truth writes into projections/caches/report stores, and forbids silent promotion of AI output into harder truth.

This note defines the smallest implementation posture for such a sandbox.

It does **not**:
- create a new constitutional artifact family,
- create a second query language,
- legalize direct AI writes to the semantic substrate,
- require every deployment to expose notebook-like or external sandbox surfaces.

---

## 2. Authority basis used

This note is grounded in already-active law and accepted extensions:
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
  - AI mediation rule
  - current-state and high-consequence law
  - twin and bridge law
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
  - projection rule
  - authoritative write rule
  - AI enforcement path
  - twin runtime freedom
- `01_companion_artifacts/OFARM_Query_Architecture_Note_v0_1.md`
- `01_companion_artifacts/OFARM_Platform_Enforcement_Architecture_Memo_v0_1.md`
- `01_companion_artifacts/OFARM_Advisory_Scenario_Workspace_and_Bridge_Note_v0_2.md`
- `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Authority_Policy_Model_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Local_Knowledge_and_Planning_Closure_RFC_v0_1.md`

---

## 3. Core stance

### 3.1 Runtime capability, not truth authority
A code-interpreter-style sandbox is a runtime capability attached to OFARM.
It is not a second truth system and not a bypass around the enforcement chain.

### 3.2 Code-on-results, not code-on-authority
The sandbox may compute over governed read bundles or result slices.
It may not invent its own backend truth path or direct write path.

### 3.3 Advisory by default
Sandbox outputs are exploratory, advisory, or draft by default.
They do not become Compliance truth, accepted consequence, or high-consequence output merely because code produced them.

---

## 4. Entry path

A safe default path is:
1. user request or AI-authored intent,
2. normal OFARM query/materialization resolution,
3. authorization/sharing evaluation,
4. governed execution producing a bounded input bundle,
5. bounded sandbox session over that bundle,
6. answer text, chart, draft advisory artifact, or bridge preparation,
7. if a higher-consequence next step is wanted, re-enter the normal `EnforcementChain`.

The sandbox session should receive bounded refs and/or read-only input mounts rather than privileged direct datastore credentials.

---

## 5. Minimum input-bundle posture

Before code executes, the sandbox should receive or be able to resolve at minimum:
- sandbox session identifier,
- acting party / agent ref where relevant,
- target twin,
- anchor scope,
- evaluation time policy,
- freshness status,
- `ContextSnapshot` ref where interpretation depends on context,
- `MaterializationBasis` / `MaterializationSnapshot` ref or governed query-result ref where relevant,
- authorization/access-decision trace ref,
- pack/profile context where interpretation depends on it,
- declared purpose/use posture,
- durable input refs and/or checksums for replay/debug.

Uploaded user files may join the bundle, but they do not become authoritative OFARM truth merely by entering the sandbox.

---

## 6. Allowed runtime behavior

### 6.1 Allowed operations
The sandbox may:
- run Python or similar bounded tools,
- create temporary files, charts, derived tables, vector tiles, and helper indices inside session scope,
- perform joins between authorized OFARM result bundles and explicit user-provided files,
- run simulation, ranking, optimization, geospatial transforms, and summarization,
- iterate within the same bounded input bundle,
- request additional governed reads, but only by re-entering the normal query/materialization path.

### 6.2 Infrastructure defaults
The default runtime posture should be:
- OFARM source inputs mounted read-only,
- writable scratch limited to a session-local workspace,
- network disabled by default or reduced to a tight allowlist,
- no standing high-authority credentials inside the sandbox,
- bounded session lifetime with scratch cleanup/garbage collection.

---

## 7. Prohibited behavior

The sandbox must not:
- write directly to the assertion/history substrate,
- write directly to current-state materialization,
- write directly to projections, caches, report stores, search indexes, or pack/context activation state,
- bypass `QuerySpecification` / `QueryPlanIR` with raw SQL, graph-console access, or ad hoc datastore access,
- hold standing credentials for output approval, attestation, filing, review acceptance, or pack governance actions,
- read outside explicit receive/use + sharing authority,
- treat notebook/session state as authoritative memory,
- silently publish or file results as passports, submissions, or attested outputs.

---

## 8. Persistence and saved outputs

Session state is ephemeral by default.

When a deployment chooses to keep outputs, it should persist only deliberately and into explicit homes, for example:
- `ScenarioResultSet` or other implementation-local advisory objects,
- `BridgeCandidate` when proposing a governed next step,
- `ReportAssembly` or `DossierAssembly` when freezing a packet through the normal path,
- `LocalArtifact` support records only when the retained object is truly local-support material and the chosen `artifactKind` is legitimate.

The platform should not retain opaque notebook/session state as a hidden truth cache.

---

## 9. Freshness, bridge, and high-consequence handling

Exploratory advisory sessions may use stale Advisory-side materialization when clearly marked.

The moment the request crosses into:
- compliance assertion,
- output approval/attestation/filing,
- accepted operational consequence,
- or any other high-consequence use,

the sandbox must stop treating its current working state as sufficient.
The runtime must recompute, refuse, or route to explicit review under the stricter Compliance-Twin freshness and basis rules.

A sandbox may prepare a `BridgeCandidate` or draft artifact.
It may not complete the bridge by itself unless a separately authorized and legally valid non-human path exists.

---

## 10. Provenance and replay

Every meaningful sandbox run should emit or retain at minimum:
- `sandboxSessionId`,
- model/module identifier and version where AI authored or executed steps,
- container/runtime image identifier,
- code hash or notebook/script hash,
- `generatedAt`,
- durable input refs and checksums,
- authorization/access trace ref,
- query/materialization/context refs,
- network posture,
- declared purpose,
- retained output refs where anything was saved.

This keeps explanation and audit anchored even when the computation itself is exploratory.

---

## 11. Refusal and downgrade behavior

The sandbox should refuse or downgrade when:
- no governed input bundle exists,
- access is not authorized,
- freshness is insufficient for the declared consequence,
- the requested action is human-only by default,
- the user is asking for direct state mutation rather than advisory analysis,
- provenance of imported or user-supplied data is unclear for a claimed compliance use.

Appropriate downgrade paths include:
- answer only from currently authorized Advisory data with clear marking,
- prepare a `BridgeCandidate` or review request,
- ask the normal runtime to produce a fresh input bundle,
- save only bounded local/advisory artifacts rather than attempting publication.

---

## 12. Conformance targets for a first implementation

A first implementation should prove at minimum:
1. the sandbox input bundle contains twin, scope, time, freshness, and authorization-trace refs,
2. OFARM source data is mounted read-only and scratch writes stay session-local,
3. extra data fetches re-enter governed query execution rather than bypassing it,
4. exploratory Advisory use may tolerate stale Advisory materialization with explicit marking,
5. a Compliance-targeted or filing-targeted request forces recomputation, refusal, or human review,
6. sandbox outputs cannot directly approve, attest, file, or mutate current state,
7. retained outputs carry provenance and do not become hidden truth stores,
8. network-disabled and allowlisted modes are both explicit and auditable when supported.

---

## 13. External-surface rule

The sandbox need not appear as a stable external partner surface.
If a deployment later exposes it as an external API or stable operator surface, declare that boundary through the normal `RuntimeSurfaceContract` / `Capability Manifest` lane rather than leaving it implicit.

---

## 14. Stop rule

Do not promote a general sandbox artifact family into active law merely because one deployment wants notebook-like UX.
The boundary, provenance, and bridge behavior matter now.
Broader standardization should remain evidence-triggered.
