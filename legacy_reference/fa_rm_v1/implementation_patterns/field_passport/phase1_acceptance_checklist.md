# Field Compliance Passport — Phase 1 Acceptance Checklist

Codex PR review gate and implementation instructions for hardening the parcel passport before spray-window / plant-health work

_Prepared: 2026-03-07_

## Decision
- Product next capability is still spray-window and plant-health relevance.
- Repo next move is narrower: harden the passport into repo-native source artifacts and one minimal runtime slice first.
- Do not start phase 2 until phase 1 sources, generation, constraints, SQL, runtime contract, and tests are green.

## Observed current state
- Markdown archetypes/templates are the human source of truth; generated FADL/JSON artifacts are derived and should not be hand-edited. `specs/generated/README.md:L6-L24; specs/generated/fadl-manifest.json:L1-L25; AI_ONBOARDING.md`
- The repo already has a tested template projection layer for app-facing workflows on top of archetypes. `specs/v0.8/templates/projections/template-crop-health-visit-ipm-nutrition-v0_8.json:L1-L92; specs/api/v1/server/fastapi/tests/test_template_projection_contracts.py:L54-L93; 20-semantic-core.md`
- The stable semantic backbone already includes Field, CropInstance, EvidenceRecord, EventRecord, and RuleExecutionTrace, with URI-first and append-only semantics. `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L152; 20-semantic-core.md; 90-glossary.md`
- FastAPI runtime code loads validators, report packs/layouts, template projections, and reference ingest profiles directly from specs/. `specs/api/v1/server/fastapi/app/main.py:L135-L165; 30-runtime-architecture.md`
- Build and verification seams already exist for generation, SHACL, DB smoke, and backend tests. `make fadl-generate; make fadl-check; make shacl-test; make db-smoke-v0_8; specs/api/v1/server/fastapi/run-tests.sh; 60-build-run-test-generate.md`
- Static OpenAPI metadata can lag runtime; runtime Pydantic/tests are the more trustworthy contract surface when they disagree. `AI_ONBOARDING.md; 70-implementation-status.md`

## Evidence-backed inference
- The passport should be implemented as new v0.8 source artifacts plus a projection-backed runtime endpoint, not as a parallel subsystem.
- The right acceptance bar is repo-native: markdown sources, generated artifacts, ontology/SHACL/SQL alignment, minimal runtime contract, and passing tests.
- Spray-window and plant-health work should start only after this hardening pass is merged, so the next feature is built on stable contracts rather than draft files.

## Recommended working assumptions
- Use v0.8 for the new field facts, templates, projections, ontology, SHACL, and SQL migrations.
- Keep Field as the semantic root; do not introduce a new canonical top-level “digital twin” entity.
- Phase 1 includes one minimal runtime read slice (GET passport). Phase 2 will add daily evaluation and plant-health/spray-window logic.

## Phase 1 scope

### In scope
- [ ] Six repo-native field fact archetypes under specs/v0.8/archetypes/
- [ ] Two repo-native template markdown sources under specs/v0.8/templates/
- [ ] Two projection JSON contracts under specs/v0.8/templates/projections/ generated from markdown sources
- [ ] Ontology and SHACL additions for any new semantic terms introduced
- [ ] Append-only SQL migrations for the new facts under specs/v0.8/sql/migrations/
- [ ] One minimal runtime endpoint: GET /v1/fields/{fieldUri}/passport
- [ ] Pydantic models, request/response examples, and projection contract tests
- [ ] A concise implementation note / PR summary with evidence paths, commands run, and explicit out-of-scope items

### Explicitly out of scope
- [ ] Full Slovenia field-ops rulepack and daily action evaluation
- [ ] Spray-window logic, disease nowcasting, plant-health ingestion, EO anomaly triage
- [ ] PPP candidate legality checks or nitrate rule computation
- [ ] Report-pack / official PDF rendering for the passport
- [ ] Bulk external data ingestion beyond placeholders or profiles needed for the minimal slice
- [ ] A generic farm dashboard

## Required source artifacts
- [ ] `FIELD.field_authority_link.v1.md`
- [ ] `FIELD.field_geometry_snapshot.v1.md`
- [ ] `FIELD.field_declaration_snapshot.v1.md`
- [ ] `FIELD.field_overlay_fact.v1.md`
- [ ] `FIELD.field_condition_daily.v1.md`
- [ ] `FIELD.field_action_evaluation.v1.md`
- [ ] `template-field-compliance-passport-si-v0_8.md`
- [ ] `template-field-action-check-si-v0_8.md`

## Acceptance checklist
### Semantic source placement
- Required: New source files live in specs/v0.8/ and follow nearby v0.8 markdown grammar; generated outputs come from the generator, not manual edits.
- Reviewer evidence: Diff of new markdown sources; generated manifest diff; note naming and placement rationale.
- Pass condition: No direct hand-edits in specs/generated/ except regenerated outputs.

### Backbone reuse
- Required: Changes reuse Field, CropInstance, EvidenceRecord, EventRecord, RuleExecutionTrace; no competing parcel root is introduced.
- Reviewer evidence: Spec diff and implementation note showing relation to existing RM terms.
- Pass condition: Model extends the current RM instead of bypassing it.

### Authority separation
- Required: GERK / cadastre / farm-operational / derived compliance geometries remain separate snapshots; no silent polygon collapse.
- Reviewer evidence: Archetype fields and sample passport payload show multiple geometry roles plus complianceGeometryRef.
- Pass condition: Authority choice is explicit and versioned.

### Append-only discipline
- Required: SQL tables and runtime behavior preserve append-only facts; no mutable current-passport table and no update/delete semantics for source facts.
- Reviewer evidence: Migration diff and persistence logic summary.
- Pass condition: Source facts are persisted as records; the passport is a projection.

### Provenance and freshness
- Required: Imported facts carry sourceSystem, sourceId, sourceVersion, effective/valid dates, and evidence/trace references where relevant.
- Reviewer evidence: Sample payload and field list.
- Pass condition: Reviewer can trace every computed passport section back to source facts.

### Ontology / SHACL alignment
- Required: New terms are represented in ontology/constraints where needed, consistent with existing v0.8 archetype patterns.
- Reviewer evidence: Ontology diff; SHACL diff; shacl-test output.
- Pass condition: No new semantic term exists only in runtime code.

### Generation integrity
- Required: Generator produces FADL/JSON for the new markdown sources and manifest entries are updated.
- Reviewer evidence: Output of make fadl-generate and make fadl-check.
- Pass condition: Generated artifacts match source definitions.

### Runtime contract
- Required: GET /v1/fields/{fieldUri}/passport exists with typed Pydantic models and examples. If persistence is off, the API must degrade honestly rather than fabricate complete data.
- Reviewer evidence: Endpoint diff; model diff; example JSON; test output.
- Pass condition: Runtime behavior is explicit about partial/unknown data.

### Projection contract tests
- Required: Projection contract coverage extends to the new passport projection, using the existing projection test pattern.
- Reviewer evidence: New/updated tests under specs/api/v1/server/fastapi/tests/.
- Pass condition: Projection schema and vocabulary alignment are enforced.

### API metadata caution
- Required: Do not treat static OpenAPI as the authoritative source when it conflicts with runtime models.
- Reviewer evidence: PR note explicitly states whether static OpenAPI was updated and why.
- Pass condition: Runtime Pydantic/tests remain the review anchor.

### Build and smoke tests
- Required: All required commands run cleanly for the changed slice.
- Reviewer evidence: Command transcript or summarized outputs.
- Pass condition: All phase 1 gates are green.

### Out-of-scope discipline
- Required: The PR does not drift into spray-window, disease nowcasting, nitrate engine, or report-pack work.
- Reviewer evidence: PR summary lists non-goals.
- Pass condition: Phase 1 remains mergeable and reviewable.

## Required commands
- [ ] `make fadl-generate`
- [ ] `make fadl-check`
- [ ] `make shacl-test`
- [ ] `make db-smoke-v0_8`
- [ ] `specs/api/v1/server/fastapi/run-tests.sh`

## Codex execution order
1. Inspect the nearest real v0.8 archetype/template markdown files and mirror their grammar exactly before introducing new source files.
2. Add the six field fact archetypes and the two template markdown files under specs/v0.8/.
3. Add or extend ontology/SHACL/SQL assets for the new field facts; preserve append-only behavior.
4. Run the generator and confirm manifest entries/output paths are created for the new sources.
5. Add Pydantic models, endpoint wiring, request/response examples, and one minimal GET passport runtime slice.
6. Add or extend tests for projection contracts, runtime contract behavior, and any persistence or capability gating touched.
7. Run the required commands, capture the results, and prepare a short PR summary with evidence paths and out-of-scope notes.

## PR evidence pack
- [ ] One-paragraph implementation summary
- [ ] Touched-file inventory by layer: specs, generated artifacts, runtime, tests, docs
- [ ] Exact commands run and whether each passed
- [ ] One example passport response JSON
- [ ] One note on persistence-disabled behavior
- [ ] One note on what is intentionally deferred to phase 2

## Exit gate to start phase 2
- [ ] All phase 1 gates above are green in CI or reproducible locally.
- [ ] Reviewer can trace model → generated artifacts → runtime contract → tests without repo archaeology.
- [ ] The PR remains parcel-passport hardening only.
- [ ] Only after merge should Codex start the spray-window and plant-health engine.

## Reviewer stop conditions
- Stop review and request revision if generated artifacts were hand-edited.
- Stop review if the PR invents a new top-level parcel or digital-twin root instead of extending `Field`.
- Stop review if authority boundaries between official and farm-operational geometries are collapsed.
- Stop review if persistence-disabled behavior fabricates complete passport content without explicit warnings or `unknown` state.
- Stop review if phase 2 logic (spray-window, plant-health, nitrate engine, PPP legality) is mixed into this PR.