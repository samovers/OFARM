# OFARM conformance seed set v0.1

Date: 2026-04-18  
Status: active supporting implementation artifact  
Scope: initial executable and design fixtures that later conformance work can extend

---

## 1. Purpose

These artifacts are **not** the full minimum conformance baseline.

They are the **starter pack** for the highest-risk seams:
- identity/lifecycle
- pack merge
- pack activation and active-artifact grounding
- authority policy
- current-state materialization
- core query/capability schemas
- horizontal external-standard-readiness contracts
- one integrated vertical slice at design level
- first-wave trace/materialization machine contracts

The authoritative statement of coverage is now:
- `OFARM_conformance_coverage_matrix_v0_1.md`

---

## 2. Fixture classes used in this package

### 2.1 Executable fixtures
Machine-readable artifacts that are actually run or validated.

Current executable fixtures include:
- spike harness JSON fixtures under `ofarm_spike_v0_1/fixtures/`
- QuerySpecification, QueryPlanIR, and Capability Manifest schema/example validation
- runtime graph-pattern equivalence canonicalization over bounded internal query fragments
- runtime-backed query-plan semantic-equivalence checks across bounded execution targets
- runtime-integrated alias-governance and saved-query regression checks over bounded query families
- machine-contract negative mutation validation and package-local cross-file reference consistency checks over the consolidated schema/example set
- runtime-shaped pack-merge legality and deterministic conflict evaluation across all governed merge surface families
- wave-1 schema/example validation for:
  - PackMergeResolutionTrace
  - AuthorizationDecisionTrace
  - MaterializationBasis
  - MaterializationSnapshot
- governance/runtime closure validation for:
  - PackActivationSet
  - ActiveArtifactSet
  - RuntimeProblem
  - PackActivationRequest / PackActivationResult
  - manifest-to-active-artifact-state consistency
  - pack-activation allow / deny / governance-required / scope-separation outcomes
- external-standard-readiness validation for:
  - SemanticSubstrateBundle
  - MappingCoverageStatement / LossMap
  - RuntimeSurfaceContract
  - ConformanceClaimSet
  - Capability Manifest v0.2 draft
  - manifest-to-substrate / claim-set / runtime-surface reference consistency
  - conservative import promotion posture checks

### 2.2 Design fixtures
Narrative or design-level fixtures that document expected behavior but are **not yet** runnable.

Current design fixtures include:
- `OFARM_Pack_Merge_Semantics_Fixtures_v0_1.md`
- `OFARM_spike_failure_case_examples_v0_1.md`
- `ofarm_spike_v0_1/fixtures/vertical_slice.json`

The full rule is documented in:
- `OFARM_executable_vs_prose_fixture_policy_v0_1.md`

---

## 3. Included executable seed families

### Identity/lifecycle
- field boundary revision vs split
- crop-cycle replant after failure
- lot commingling into new cohort identity
- recurring zone revision versus ephemeral advisory mask
- governed zone split into recurring child zones
- relay/intercrop overlap with explicit crop-cycle lineage
- equipment maintenance revision versus replacement asset
- facility restructure revision versus storage/container replacement
- reusable container occupancy continuity versus broken-unit replacement

### Pack merge and activation
- cumulative evidence-policy merge
- conflicting template-constraint hard fail
- activation allowed through declared merge
- activation denied for same-precedence conflict
- activation routed to governance-required
- activation allowed by scope separation
- vocabulary-binding additive union, non-empty intersection, and incompatible mandatory-code-system hard fail
- archetype identical-only coexistence and divergent-definition hard fail
- validation-rule conjunctive intersection and contradiction hard fail
- decision-rule ordered composition allow and unordered competing-key hard fail
- event-subtype disjoint union, ordered enrichment, and top-level-family mismatch hard fail
- PassportView additive/ordered shaping allow and conflicting-slot hard fail
- DocumentAssembly additive/ordered shaping allow and conflicting-attested-slot hard fail

### Profile compatibility and activation-set depth
- approved narrowing profile allowed under higher-precedence baseline
- disjoint recipient-facing view profile allowed as plain compatibility
- lower-precedence weakening attempt denied deterministically
- same-precedence competing output profiles routed to governance
- scope-separated profile coexistence allowed
- time-window-separated seasonal profile coexistence allowed
- missing required pack dependency denied
- declared exclusion denied deterministically

### Capability-manifest grounding
- core deployment manifest matches active artifact state
- partner deployment manifest matches active artifact state
- partner manifest mismatch against active artifact state fails deterministically

### Authority
- delegated service-provider execution allowed
- buyer/assert write path denied

### Current-state materialization
- high-consequence pack/context change invalidates current state and requires recomputation
- compliance report recomputation on context drift or output-profile change
- dossier attestation recomputation on attestation-policy or shaping change
- submission filing recomputation on submission-binding change
- explicit refusal on invalidated high-consequence filing paths

### Output taxonomy and publication
- advisory stale live passport serving with warning
- frozen advisory/compliance report assembly with twin-dependent freshness policy
- dossier attestation allow, review, recompute, and deny paths
- submission filing allow, recompute, and refuse paths
- explicit no-attestation and no-filing rule for `PassportView`

### Query equivalence
- same-semantics graph-pattern equivalence after alias resolution, variable renaming, and branch reordering
- explicit non-equivalence for optional edges, anchor shifts, twin shifts, temporal posture shifts, alias-path drift, and relation changes

### Event grammar and promotion safety
- all seven fixed top-level event families exercised at runtime-shaped fixture level
- subtype compatibility allow/block/review outcomes across family-rooted subtype declarations
- runtime-shaped promotion traces for all nine baseline commit classes
- explicit dominant-semantic-consequence handling where linked consequences do not override the primary family

### Schema validation
- QuerySpecification schema validation
- QueryPlanIR schema validation
- Capability Manifest schema validation
- PackMergeResolutionTrace schema validation
- AuthorizationDecisionTrace schema validation
- MaterializationBasis schema validation
- MaterializationSnapshot schema validation
- PackActivationSet schema validation
- ActiveArtifactSet schema validation
- RuntimeProblem schema validation
- PackActivationRequest schema validation
- PackActivationResult schema validation
- SemanticSubstrateBundle schema validation
- MappingCoverageStatement schema validation
- LossMap schema validation
- RuntimeSurfaceContract schema validation
- ConformanceClaimSet schema validation
- Capability Manifest v0.2 draft schema validation

---

## 4. Included design-only seed artifacts

### Vertical slice
- delegated orchard execution followed by current-state recompute and field-passport regeneration

### Prose fixture families
- wider pack merge families beyond the executable subset
- broader failure examples and scenario expansion targets
- richer capability-manifest honesty checks beyond the current active-pack/profile grounding subset

---

## 5. Why this is still useful

This seed set now does five honest things:
- proves the delivered spike package is rerunnable from package-relative inputs
- proves the core query/capability contracts validate
- proves the first trace/materialization contracts are no longer prose-only
- proves the package can evaluate a starter pack-activation seam and manifest-grounding seam without hidden runtime interpretation
- makes the remaining uncovered minimum baseline explicit rather than implied


---

## 6. Update in v0.6

The package now ships the horizontal external-standard-readiness contracts as active substance plus executable support:
- substrate bundle fixture and schema validation
- mapping coverage/loss fixture families for ADAPT, ISOXML, and NGSI-LD examples
- runtime-surface contract fixtures for NGSI-LD export, capability discovery, and a CQL2 query façade
- claim-set and manifest-by-reference consistency checks

This still does **not** close bridge-pack or mapping round-trip work.
It closes the horizontal law and machine-contract seams those later packs depend on.

---

## 7. Wave 9 import/export hardening update

The package now also ships a first executable import/export hardening slice:
- runtime-shaped ADAPT and ISOXML import gate logs that stop at normalized claim/evidence material
- a starter declared-surface round-trip feasibility suite for ADAPT import, ISOXML import, and NGSI-LD export
- output-adapter trace-back records for live passport export, frozen dossier packaging, and frozen submission filing

This still does **not** close same-standard reversible bridge-pack loops or executor-native ingest/export telemetry.
It moves the package from static mapping honesty checks toward boundary-path conformance evidence.

---

## 8. Wave 10 executor telemetry update

The package now also ships a first executor-synthesized ingest/export telemetry slice:
- ADAPT import executor telemetry with claim/evidence-first normalization and review-required accepted-consequence gating
- ISOXML import executor telemetry with material-loss visibility retained in the emitted event stream
- NGSI-LD live passport export telemetry linked back to the declared round-trip and trace-back records
- frozen dossier package adapter telemetry and frozen submission filing adapter telemetry
- blocked submission telemetry showing invalid materialization stops the file path before any output is emitted

This still does **not** provide deployment-collected runtime telemetry or same-standard reversible bridge-pack loops.
It moves the package from replay-shaped boundary logs toward execution-produced import/export evidence.

---

## 9. Wave 11 same-standard bridge-pack update

The package now also ships a first same-standard reversible bridge-pack rehearsal slice:
- draft ADAPT export bridge machine-contract examples paired against the existing ADAPT import posture
- draft ISOXML export bridge machine-contract examples paired against the existing ISOXML import posture
- an updated reverse-pair scan showing draft same-standard reversible eligibility for ADAPT and ISOXML
- declared-subset round-trip records for both draft pairs
- blocked conflict cases for vendor-private ADAPT extensions and high-consequence ISOXML timestamp ambiguity

This still does **not** provide deployment-collected same-standard runtime telemetry or broad production bridge-pack claims.
It does close the declared-surface conformance gap that previously kept same-standard round-trip coverage partial.

---

## 10. Wave 12 same-standard bridge executor update

The package now also ships a first executor-produced same-standard bridge telemetry slice:
- ADAPT declared-subset bridge executor telemetry with re-import equivalence confirmation and explicit draft-surface warnings
- ISOXML declared-subset bridge executor telemetry with the same draft-scoped round-trip confirmation posture
- blocked ADAPT vendor-extension bridge telemetry that retains raw evidence instead of claiming reversible transport
- blocked ISOXML high-consequence timestamp telemetry that stops the reversible bridge claim before any bridge emission
- an updated candidate-pair posture file and an explicit promotion-readiness decision that keeps both same-standard bridge surfaces at `DRAFT`

This still does **not** provide deployment-collected same-standard telemetry or justify promotion beyond draft.
It moves the package from declared-subset bridge rehearsal into executor-produced bridge evidence plus an explicit non-promotion decision.
## 11. Wave 13 partner-variant sample replay update

The package now also ships a bounded same-standard bridge partner-variant sample replay slice:
- anonymized partner deployment sample replays for ADAPT and ISOXML draft bridge pairs
- supported partner-variant success paths for each draft pair
- blocked partner-variant sample paths for the current vendor-extension and high-consequence timestamp conflict families
- partner-variant coverage records tied back to the draft candidate pairs
- an updated promotion assessment that keeps both bridge surfaces at `DRAFT`

This still does **not** provide live field-collected same-standard bridge telemetry.
It moves the package from executor-only bridge proof into stronger partner-variant conformance rehearsal while keeping the non-promotion boundary explicit.


## 12. Wave 14 deployment-intake and broader construct-family update

The package now also ships a bounded same-standard bridge deployment-intake and broader construct-family slice:
- package-local redacted deployment-intake telemetry for ADAPT and ISOXML draft bridge pairs
- broader construct-family sample coverage records for each draft pair
- supported intake samples for supplemental construct families beyond the earlier minimum reversible subsets
- blocked intake samples for unsupported nested vendor-private extensions and timezone-ambiguous high-consequence worker-summary families
- an updated promotion assessment that still keeps both bridge surfaces at `DRAFT`

This still does **not** provide live field-collected same-standard bridge telemetry or full reversible round-trip proof for the supplemental construct families.
It moves the package from partner-variant sample replay into intake-shaped bridge readiness evidence and broader construct-family sample coverage while keeping the non-promotion boundary explicit.



## 13. Wave 15 supplemental-family round-trip and live-field evidence gate update

The package now also ships a bounded same-standard bridge supplemental-family proof slice:
- reversible round-trip records for the supported ADAPT supplemental families
- reversible round-trip records for the supported ISOXML supplemental families
- blocked supplemental-family conflict records that keep nested vendor-private and timezone-ambiguous variants outside reversible claims
- an explicit live-field evidence gate that records the continued absence of live field-collected same-standard bridge telemetry
- an updated promotion assessment that narrows the blocker while still keeping both bridge surfaces at `DRAFT`

This still does **not** provide live field-collected same-standard bridge telemetry or production promotion approval.
It closes the supported supplemental-family reversible-proof gap while keeping the missing live-field evidence explicit rather than implied.

---

## 14. Wave 16 drift-check and materialization trace update

The package now also ships a bounded current-state explainability hardening slice:
- a drift-check memo that re-reads the original amendment plan and explicitly returns continuation work to a central plan-linked seam
- runtime-produced freshness telemetry covering FRESH reuse, STALE advisory reuse with warning, context-drift recomputation, evidence-update recomputation, explicit invalidation refusal, and high-consequence filing stop paths
- runtime-produced materialization-basis trace records linking start/result basis refs, context refs, snapshot refs, trigger families, and emitted telemetry event ids
- an updated conformance assessment that closes the current-state freshness and materialization-basis trace rows at the package-evidence level

This still does **not** provide deployment-collected materialization telemetry or close authority-derived lineage inheritance and revocation-race follow-on work.
It does move the package back toward the central hardest-design concern that governed current state must remain explainable under runtime trigger pressure.

---

## 15. Wave 17 authority-depth and review-decision update

The package now also ships a bounded authority-depth hardening slice:
- derived-lineage inheritance decision logs for child-lot read allow and write/assert deny
- delegated-scope narrowing and grant-supersession evidence for an exact-only override case
- revocation-race evidence showing final submission filing is denied after a promotion-time recheck
- dossier sharing evidence that allows read but denies write and later denies access after revocation
- an explicit software-agent allow path for low-consequence live-passport assembly under machine-permitted governance
- explicit `REQUIRE_HUMAN_APPROVAL` and `REQUIRE_REVIEW` review records for AI-assisted finalization and delegated attestation-sign attempts

This still does **not** provide deployment-collected authorization telemetry or close every multi-hop delegation and signatory permutation.
It does move the package back toward a central hardest-design seam by closing the missing `DERIVED_LINEAGE_SCOPES` mode and deepening review/revocation authority evidence without changing OFARM law.

---

## 16. Wave 18 identity/lifecycle expansion update

The package now also ships a bounded identity/lifecycle hardening slice:

- runtime-shaped identity-versus-revision proof for recurring zones, crop cycles, equipment, facilities, storage locations, and reusable containers
- executable lineage proof for split, successor, overlap, and replacement outcomes
- durable-versus-ephemeral zone evidence that keeps advisory overlays from minting constitutional identities
- identity/lifecycle-trigger invalidation evidence for zone durability change, crop replant, lifecycle overlap, identity replacement, and lifecycle split

This still does **not** provide deployment-collected lifecycle telemetry or exhaust every possible asset/place/container subfamily.
It does close the central identity/lifecycle conformance gap that remained after the earlier authority and current-state hardening waves.

---

## 17. Wave 19 event-family and promotion safety update

The package now also ships a bounded event-grammar hardening slice:

- executable coverage for all seven fixed top-level event families
- deterministic subtype compatibility allow/block/review outcomes, including an explicit invented-top-level-family block
- runtime-shaped dominant-semantic-consequence evidence showing linked consequences do not silently rewrite the primary family
- runtime-shaped promotion traces across all nine baseline commit classes
- explicit no-shortcut evidence for notes, hypotheses, evidence records, advisory outputs, and governance decisions that try to bypass evidence rules

This still does **not** provide deployment-collected event-ingestion telemetry or close cross-precedence merge legality for conflicting event subtype declarations.
It does close the core conformance seam around OFARM's fixed event grammar and promotion matrix without changing OFARM law.

---

## 18. Wave 20 profile compatibility and activation-set update

The package now also ships a bounded profile-compatibility hardening slice:

- runtime-shaped profile compatibility records across all five constitutional compatibility classes
- deterministic allow/deny/governance outcomes for narrowing, disjoint shaping, weakening denial, scope separation, time-window separation, dependency failure, and declared exclusion
- activation decision logs that explicitly record dependency, exclusion, precedence, and surface-overlap checks
- stronger PackActivationSet depth evidence for multi-scope and multi-time evaluation

This still does **not** provide deployment-collected profile telemetry or full profile-manifest machine contracts.
It does close the previously untouched central conformance seam around profile compatibility while materially deepening activation-set evaluation evidence without changing OFARM law.



---

## 19. Wave 21 alignment-register coverage update

The package now also ships a bounded semantic-governance coverage slice:

- a machine-checked coverage review over all `91` canonical concepts in the harmonized Alignment Register
- per-concept evidence classification across baseline, companion, RFC, machine-contract, and implementation/conformance layers
- explicit exclusion of self-referential matrix/seed/patch artifacts from the coverage scan
- explicit follow-on gap records for the three concepts still evidenced only in the register itself:
  - `Variety / cultivar`
  - `LocalConditionPattern`
  - `PlannedIntervention`

This still does **not** mean every register concept has equal machine-contract or runtime depth.
It does close the previously untouched central conformance seam around alignment-register coverage by making semantic coverage machine-checked rather than implicit.


---

## 20. Wave 22 graph-pattern equivalence update

The package now also ships a bounded query-equivalence hardening slice:

- runtime-shaped canonicalization for same-semantics internal query graphs after alias-version resolution
- positive equivalence coverage for variable renaming, predicate reordering, alias-version path equivalence, branch reordering, lineage branches, and operation/evidence branches
- explicit non-equivalence coverage for optional-versus-required edges, anchor shifts, twin shifts, temporal shifts, alias-path drift, and relation changes
- a distinct boundary between graph-pattern equivalence and execution-target plan equivalence

This still does **not** provide full QuerySpecification executor integration, saved-query regression, or deployment-produced alias telemetry.
It does close the previously untouched central conformance seam around same-semantics graph-pattern equivalence without changing OFARM law.

---

## 21. Wave 23 query-plan target-equivalence update

The package now also ships a bounded cross-target query-planner hardening slice:

- runtime-backed QueryPlanIR semantic-equivalence checks across `CURRENT_STATE_MATERIALIZATION`, `READ_MODEL`, `SEARCH_INDEX`, and `SEMANTIC_GRAPH`
- canonical semantics fingerprints plus per-target execution/result digests over shared bounded data sets
- positive equivalence coverage for field-passport, lot-lineage, evidence-backed operation, frozen submission, advisory-zone, and note-search query families
- explicit blocked coverage for:
  - compliance queries sent to a target without a valid freshness gate
  - targets that silently drop a required query filter and therefore drift semantically

This still does **not** provide live deployment-produced query execution telemetry or full saved-query regression at deployment scale.
It does close the remaining direct central conformance seam around runtime-backed query-plan semantic equivalence across execution targets without changing OFARM law.

---

## 22. Wave 24 alias-runtime and saved-query regression update

The package now also ships a bounded alias-governance hardening slice at runtime:

- runtime-integrated alias resolution during saved-query load and query compilation
- saved-query baseline-versus-runtime semantics fingerprint comparison across catalog upgrades
- bounded result-digest regression across allowed execution targets after alias resolution
- positive coverage for:
  - direct pinned stability
  - backward-compatible pinned stability
  - deprecated successor rollover with explicit trace
  - repin-notice success where semantics stay unchanged
- explicit blocked coverage for:
  - ambiguous unpinned alias resolution
  - high-consequence saved query with missing alias version
  - alias-path upgrade that would silently drift semantics

This still does **not** provide deployment-produced alias telemetry or full deployment-scale saved-query replay.
It does close the remaining central alias-governance seam around runtime-integrated alias stability and saved-query regression without changing OFARM law.

---

## 23. Wave 25 pack-merge legality and conflict update

The package now also ships a bounded pack-merge conformance hardening slice:

- runtime-shaped legality and deterministic-outcome coverage for all nine governed merge surface families:
  - `VOCABULARY_BINDINGS`
  - `EVIDENCE_POLICY`
  - `ARCHETYPE_DEFINITION`
  - `TEMPLATE_CONSTRAINT`
  - `VALIDATION_RULE`
  - `DECISION_RULE`
  - `EVENT_SUBTYPE_DEFINITION`
  - `VIEW_SHAPING`
  - `DOCUMENT_ASSEMBLY_SHAPING`
- explicit safe-merge coverage for additive union, constraint intersection, strongest requirement, identical-only coexistence, and ordered composition where the RFC allows them
- explicit unsafe coverage for incompatible mandatory bindings, contradictory evidence policies, divergent archetypes, impossible template/validation combinations, competing decision rules, event-family mismatch, conflicting live-view slots, and conflicting attested frozen-output sections
- repeated deterministic evaluation showing stable merge mode, activation outcome, compatibility class, and reason code on every scenario

This still does **not** provide deployment-produced pack-activation telemetry or new machine-contract schema families.
It does close the remaining central conformance seam around pack-merge legality, conflict determinism, and executable surface-family coverage without changing OFARM law.

---

## 24. Wave 26 authority action-class and sharing-boundary update

The package now also ships a bounded authority/output hardening slice:

- runtime-shaped decision coverage for all 20 Authority Action Matrix classes
- explicit coverage for all 4 baseline authorization outcomes:
  - `ALLOW`
  - `DENY`
  - `REQUIRE_REVIEW`
  - `REQUIRE_HUMAN_APPROVAL`
- broader context-governance coverage across `CONTEXT_INSTALL_PACK`, `CONTEXT_ACTIVATE_PACK`, and `CONTEXT_DEACTIVATE_PACK`
- broader sign/attest/output coverage across `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY`, `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY`, and `OUTPUT_FILE_SUBMISSION_ASSEMBLY`
- explicit sharing-boundary coverage across `PassportView`, `DocumentAssembly`, and `SubmissionAssembly`
- no-implicit-access proof for:
  - compiled-output sharing without write/assert authority
  - compiled-output sharing without attestation authority
  - compiled-output sharing without underlying raw-evidence access
  - cross-farm role presence without explicit sharing grant
  - multi-party revocation where one grantee is denied while another remains allowed

This still does **not** provide deployment-collected authorization/share telemetry or new authorization machine-contract schema families.
It does close the remaining central authority/output conformance seams around action-class decision breadth and no-implicit-access sharing boundaries without changing OFARM law.


---

## 25. Wave 27 materialization/publication policy update

The package now also ships a bounded materialization/publication hardening slice:

- runtime-shaped invalidation breadth across output-profile, attestation-policy, publication-shaping, signatory-scope, and submission-binding change triggers
- high-consequence recompute, review, deny, and refuse paths across compliance reports, dossier attestation, attested reports, and submission filing
- explicit Compliance-versus-Advisory twin-policy comparisons across live passports, frozen reports, alerts, dossier attestation, and filing paths
- runtime-produced evidence sufficiency and attestation/publication decision records with signatory and file-authority checks
- explicit compiled-output taxonomy coverage across live `PassportView`, frozen `DocumentAssembly` families, and `SubmissionAssembly`
- publication trace-back linkage from final output outcomes back to basis, snapshot, context, and evidence-decision refs

This still does **not** provide deployment-collected publication telemetry or partner-specific publication adapters.
It does close the remaining central runtime seam around materialization/publication policy without changing OFARM law.

## 9. Wave 28 machine-contract hardening update

The package now also closes the remaining baseline machine-contract validation gap:
- `OFARM_machine_contract_validation_results_v0_9.json` extends the positive schema/example suite with bounded negative mutations and package-local cross-file reference checks
- `OFARM_machine_contract_negative_validation_records_v0_1.json` records expected-fail validation for one bounded negative mutation per shipped schema family
- `OFARM_machine_contract_reference_consistency_records_v0_1.json` records package-local resolvable reference integrity and injected broken-reference failures

This does **not** claim that every external or deployment-anchored ref in the package is locally resolvable.
It closes the baseline validation row by proving the shipped contract set now has positive validation, negative validation, and package-local cross-file integrity coverage.

---

## 20. Wave 30 deployment-shaped publication sequencing and trace-back update

The package now also ships a final package-internal closure slice for the two last runtime/conformance partials:
- runtime-emitted partner-surface publication gate sequencing across live passport, advisory report, compliance report, dossier, and submission families
- multi-action review-chain emission for human-approval and governance-review paths
- partner-surface publication trace-back across NGSI-LD, dashboard JSON, CSV/PDF report, dossier JSON, and submission XML paths
- blocked external-surface conflict paths for review-pending, schema-mismatch, recipient-profile-conflict, and revocation-recheck outcomes

This closes:
- enforcement-gate sequencing tests
- projection trace-back tests

It still does **not** count as live field bridge-promotion evidence, and it does **not** change the hold-at-draft posture for same-standard bridge pairs.

---

## 26. Wave 31 dispute-path and alignment-gap closure update

The package now also ships a bounded dispute/audit hardening slice:

- runtime-shaped end-to-end late-evidence successor-path fixtures from `PlannedIntervention` through execution claim, accepted consequence, frozen dossier/submission, and successor corrected outputs
- explicit no-edit-in-place proof for frozen outputs and filed submissions
- delayed-sync contractor revocation-recheck fixtures that preserve historical actor lineage while blocking auto-promotion after delegation revocation
- refreshed alignment-register coverage that now runs against the standalone package, excludes self-generated coverage bookkeeping artifacts, and closes the earlier low-cost gaps for:
  - `Variety / cultivar`
  - `LocalConditionPattern`
  - `PlannedIntervention`

This still does **not** provide deployment-collected delayed-sync telemetry or a full product-grade delayed-sync engine.
It does close the remaining high-value package-internal dispute-path seam and the last low-cost alignment coverage seam without changing OFARM law.

