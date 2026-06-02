# OFARM 2 Repository Cleanup and Handover Readiness Recommendation

## Research basis and operating principles

The right model for OFARM 2 is not a generic software monorepo. It is a standards-style publication system with a strict authority ladder, where active and accepted artefacts are citable, while drafts, review holdings and legacy context are visible but fenced. That is the same structural idea used by the IETF, where RFCs are the archival publication channel and Internet-Drafts have no formal status and must not be cited for compliance, and by ADR practice, where accepted decisions become immutable and later changes supersede them instead of being silently rewritten. For OFARM 2, the practical implication is simple: status must be encoded in paths, manifests and validators, not just in file names or prose disclaimers. citeturn34view0turn34view1turn35view0turn35view2

For machine contracts, the best pattern is to keep source schemas as discrete schema resources with stable identifiers, and treat bundles as generated transport artefacts rather than edited source. JSON Schema’s own guidance recommends absolute `$id` values, explains that each embedded schema resource in a compound document should be treated as its own resource, and recommends using bundling tools rather than hand-authoring embedded bundles during development. That matters here because it gives you a clean split between source-of-truth schemas and convenience distributions. citeturn9view1turn9view2turn16view1turn16view2

For large semantic packages, HL7 FHIR is a useful comparator. Its package format uses a `package.json` manifest, stores definitional artefacts separately from examples, and uses a rebuildable `.index.json` so tools do not need to open every resource file just to discover what exists. The same FHIR guidance also warns that large packages become hard for tooling to handle, and explicitly suggests splitting out extra collateral such as testing support and examples, or publishing subsets when file counts become significant. That is directly relevant to OFARM 2’s schema, example and conformance sprawl problem. citeturn10view0turn10view1turn10view3

For developer and AI-agent navigability, repository instruction files help, but they are guidance, not enforcement. Codex reads `AGENTS.md` before doing any work and resolves instruction files by walking from the project root to the current working directory; Claude loads repository instructions and path-scoped rules, can import `AGENTS.md` into `CLAUDE.md`, and explicitly notes that long or conflicting instruction files reduce adherence. Anthropic’s documentation also points agents first to an `llms.txt` documentation index for discovery before exploration. The consequence for OFARM 2 is that you should keep one short root instruction source, add path-scoped archive rules, and rely on validators and CI for hard guarantees. citeturn30view0turn30view2turn33view0turn33view1turn36view0turn38view0

## Target folder tree

I would preserve OFARM’s top-level authority separation exactly as given, but standardise the internals so that active material, accepted decisions, supporting implementation, research, review holdings and legacy context are mechanically distinguishable. I would also avoid creating a parallel “docs” or “archive” top level, because that would weaken the authority model instead of clarifying it. The tree below is the minimum shape I would target after cleanup, based on the standards/package patterns above. citeturn34view0turn35view2turn16view2turn10view1turn30view0

```text
OFARM2/
├── README.md
├── AGENTS.md
├── CLAUDE.md                          # contains: @AGENTS.md
├── llms.txt                           # generated, terse navigation
├── .gitattributes
├── .github/
│   ├── CODEOWNERS
│   └── workflows/
│       ├── validate.yml
│       └── generate_indexes.yml
│
├── 00_active_baseline/
│   ├── README.md
│   ├── folder.status.json
│   └── baseline/
│
├── 01_companion_artifacts/
│   ├── README.md
│   ├── folder.status.json
│   └── artifacts/
│
├── 02_accepted_rfcs/
│   ├── README.md
│   ├── folder.status.json
│   ├── accepted/
│   └── superseded/
│
├── 03_machine_contracts/
│   ├── README.md
│   ├── folder.status.json
│   ├── schemas/
│   │   └── <namespace>/<concept>.schema.json
│   └── bundles_generated/
│       └── <namespace>.bundle.schema.json
│
├── 04_implementation_and_conformance/
│   ├── README.md
│   ├── folder.status.json
│   ├── examples/
│   │   └── <namespace>/<concept>/{valid,invalid,roundtrip}/...
│   ├── fixtures/
│   ├── conformance_suites/
│   │   └── <dialect_or_capability>/
│   └── reports_generated/
│
├── 05_project_handoff_and_prompts/
│   ├── README.md
│   ├── folder.status.json
│   ├── prompts/
│   ├── output_schemas/
│   ├── eval_datasets/
│   └── review_runs/
│
├── 06_active_supporting_research/
│   ├── README.md
│   ├── folder.status.json
│   ├── source_inputs/
│   │   ├── manifests/
│   │   └── working_extracts/
│   └── syntheses/
│
├── 07_linked_domain_architectures/
│   ├── README.md
│   ├── folder.status.json
│   └── linked_architectures/
│
├── reviewed_*/
│   ├── README.md
│   ├── folder.status.json
│   └── holding/
│
├── legacy_reference/
│   ├── README.md
│   ├── folder.status.json
│   ├── superseded_material/
│   ├── source_snapshots/
│   │   └── <source>/<yyyymmdd>/{manifest.json,snapshot.tar.zst}
│   └── historical_overlays/
│
└── package_meta/
    ├── package.json
    ├── release.manifest.json
    ├── validators/
    ├── schemas/
    └── generated/
        ├── authority.index.json
        ├── materials.index.json
        ├── contracts.index.json
        ├── schema_example_map.json
        ├── source_inputs.lock.json
        ├── traceability.index.json
        ├── review_runs.index.jsonl
        ├── handover_gate.json
        └── llms-full.txt
```

The most important structural choice is this one: keep **schemas** in `03_machine_contracts`, but keep **examples, fixtures and conformance suites** in `04_implementation_and_conformance`. FHIR packages often place examples adjacent to definitional artefacts, but OFARM’s stricter authority separation argues for a cleaner split: tier 03 should hold the current contracts themselves, while tier 04 holds material that proves or illustrates them. That makes authority unambiguous for both humans and tooling, and generated maps can reconnect the two without mixing them physically. JSON Schema’s official test suite is useful here as a pattern: versioned tests live in dedicated directories and are organised structurally rather than as ad hoc examples sprinkled around the source. citeturn10view0turn10view3turn15view0

The minimal package root after cleanup should contain only the authority folders, `package_meta`, the root navigation files (`README.md`, `AGENTS.md`, `CLAUDE.md`, `llms.txt`), and repository governance files (`.github/`, `.gitattributes`, licence if applicable). Loose exports, one-off inventories, duplicated status summaries, stray prompts, temporary research captures, and generated reports should not sit at root. They should either move into the authority folders that own them, into `package_meta/generated`, into `05_project_handoff_and_prompts`, into `06_active_supporting_research`, or into `legacy_reference`. citeturn30view0turn36view0turn32view0

A practical disposition by current area is below.

| Current area | Cleanup action |
|---|---|
| `00_active_baseline/` | Keep in place. Add `folder.status.json`, stable internal anchors, and explicitly mark downward references as supportive only. |
| `01_companion_artifacts/` | Keep in place. Remove drafts and snapshots. Keep only current normative support artefacts. |
| `02_accepted_rfcs/` | Split into `accepted/` and `superseded/`. Accepted RFCs become immutable; later changes are new RFCs linked by `supersedes`. |
| `03_machine_contracts/` | Keep only source schemas and generated bundles. Move examples/fixtures/reports out to tier 04. |
| `04_implementation_and_conformance/` | Mirror the schema namespace tree here for examples and fixtures; keep conformance suites and generated results here, not in active contract folders. |
| `05_project_handoff_and_prompts/` | Normalise into `prompts/`, `output_schemas/`, `eval_datasets/`, `review_runs/`. No free-floating reviewer notes. |
| `06_active_supporting_research/` | Keep only actively used source inputs and syntheses. Anything purely historical moves to `legacy_reference/`. |
| `07_linked_domain_architectures/` | Keep as context-only. Indexable, but never citable as active authority. |
| `reviewed_*` | Preserve, but standardise each to `README.md` + `folder.status.json` + `holding/`, with explicit non-authoritative flags. |
| `legacy_reference/` | Preserve, but make it archival: superseded material, source snapshots, historical overlays, and no active default navigation. |
| `package_meta/` | Expand into the single place for package manifest, validator schemas, generated indexes and release metadata. |

This disposition follows the same broad pattern found in RFC/ADR lifecycles, JSON Schema source-vs-bundle practice, and FHIR package indexing: authoritative sources are stable and sparse; support material is separated; archival material is preserved but clearly non-current. citeturn34view0turn35view0turn16view2turn10view1

## Generated indexes and metadata

The core cleanup move is to stop relying on people to “remember what is current” and instead generate that fact. FHIR’s `.index.json` is explicit that the index exists so tools do not need to load every resource, and that the index contains no independent information and can be rebuilt from source at any time. OFARM 2 should copy that philosophy: generated indexes should be rebuildable, deterministic, and treated as outputs, not manually curated source. For provenance and retention, the checksum rationale from SPDX is also directly useful: checksums detect change and can serve as a high-likelihood unique identifier for a particular file state. citeturn10view1turn19view1turn19view3

I would generate the following minimum set.

| File | Purpose | Minimum fields |
|---|---|---|
| `package_meta/generated/authority.index.json` | Single source for “what is authoritative now” | `authority_rank`, `canonical_id`, `title`, `path`, `kind`, `current`, `supporting_paths`, `citation_allowed` |
| `package_meta/generated/materials.index.json` | Catalogue of every tracked artefact | `path`, `folder_class`, `kind`, `authority_rank`, `lifecycle_status`, `current`, `generated`, `search_default`, `release_export`, `checksum` |
| `package_meta/generated/contracts.index.json` | Contract currentness and replacement chain | `schema_id`, `concept_id`, `path`, `dialect`, `version`, `current`, `supersedes`, `superseded_by`, `bundle_path`, `authority_basis` |
| `package_meta/generated/schema_example_map.json` | Link current schemas to supporting examples and fixtures | `schema_id`, `example_path`, `fixture_kind`, `expected_validity`, `roundtrip_role`, `last_verified_at` |
| `package_meta/generated/source_inputs.lock.json` | Provenance and checksum lock for copied source-context material | `source_id`, `origin_uri`, `retrieved_at`, `local_path`, `checksum`, `transform_chain`, `active_or_legacy` |
| `package_meta/generated/traceability.index.json` | Concept traceability across the package | `concept_id`, `baseline_anchor`, `companion_ids`, `rfc_ids`, `schema_ids`, `example_ids`, `conformance_ids`, `research_input_ids` |
| `package_meta/generated/review_runs.index.jsonl` | Reproducible review manifest | `run_id`, `prompt_path`, `output_schema_path`, `dataset_path`, `source_commit`, `source_checksums`, `model`, `parameters`, `output_path`, `verdict` |
| `package_meta/generated/handover_gate.json` | Machine gate used by CI and reviewer prompts | `gate_pass`, `blocking_failures`, `warnings`, `coverage`, `generated_at`, `source_commit` |
| `llms.txt` and `package_meta/generated/llms-full.txt` | AI-agent navigation surface | links to root README, authority index, current package manifest, archive index, validator entrypoints |

Two small hand-maintained metadata files should drive nearly all of that generation. First, each top-level folder should have a tiny `folder.status.json` declaring `authority_rank`, `folder_class`, `citation_allowed`, `search_default`, `release_export`, and allowed reference directions. Second, artefacts whose status is not derivable from content alone—especially accepted RFCs, baseline documents and special manifests—should expose a canonical identifier and lifecycle metadata either in-file or as a sidecar. Everything else should be generated. That is the cleanest source-of-truth hygiene: the policy is declared once, and the indexes are rebuilt from it. citeturn35view2turn10view1turn19view1

For AI agents, the root `AGENTS.md` should be short and procedural, not encyclopaedic. It should point first to `package_meta/generated/authority.index.json`, then to `traceability.index.json`, then to the validator command, and it should explicitly mark `reviewed_*` and `legacy_reference` as non-authoritative unless the task is explicitly historical. `CLAUDE.md` should simply import `AGENTS.md` and add Claude-specific notes only if needed. That aligns with Codex’s layered `AGENTS.md` discovery and Anthropic’s explicit guidance to import `AGENTS.md` into `CLAUDE.md` when both tools are used. citeturn30view0turn30view2turn36view0turn33view0

## Validation and clean gate

Before handover, OFARM 2 needs a validator suite that checks authority hygiene, not semantic truth. JSON Schema’s own ecosystem provides two good anchors here: schemas should carry proper identifiers and dialect declarations, and conformance checks should look like explicit test suites rather than “some examples that happen to exist”. The JSON Schema Test Suite also makes a critical distinction that OFARM should adopt: tests and examples are there to verify specified behaviour, and validators should guarantee that test files are valid JSON and that supplied schemas validate as schemas under the corresponding specification. On the governance side, GitHub branch protection and CODEOWNERS give you the enforcement layer for repository stewardship. citeturn16view2turn15view0turn13view0turn13view2turn13view3turn13view5

I would make the validator suite enforce at least the following.

| Check family | Validator rule | Hand‑over failure condition |
|---|---|---|
| Authority isolation | Every tracked file resolves to exactly one folder class and lifecycle status. Active/accepted material may not cite `reviewed_*` or `legacy_reference` except through explicitly marked historical references. | Any illegal cross-authority reference |
| Canonical currentness | For each declared contract ID or decision ID, there is exactly one current artefact unless a manifest explicitly declares a parallel active set. | Duplicate current artefacts or missing supersession links |
| Accepted RFC hygiene | Accepted RFCs are immutable; replaced items sit in `superseded/` with `superseded_by` links. | Edited accepted artefact without replacement chain |
| Schema identity | Every source schema has root `$schema`, absolute `$id`, unique `schema_id`, and resolvable refs. | Missing or duplicate identifiers; broken refs |
| Compound/bundle integrity | Bundles are regenerated from source and compared bit-for-bit or semantically against checked-in bundle outputs. | Hand-edited or stale bundle |
| Example and fixture coverage | Every current schema has at least one linked valid example; invalid examples fail as expected; roundtrip fixtures, if declared, behave as expected. | Missing links or unexpected validation result |
| Conformance suite quality | Conformance files are valid JSON, classified by dialect/capability, and mapped to their target schemas/contracts. | Orphaned or malformed conformance material |
| Provenance lock | Every copied source input and overlay has an origin, retrieval date and checksum lock entry. | Missing provenance or checksum |
| Generated artefact freshness | All generated indexes, reports and navigation files are reproducible from the current commit. | Dirty regeneration or stale generated output |
| Documentation freshness | Root README, folder READMEs, AGENTS/CLAUDE files and package manifest agree with generated indexes. | Mismatch between prose and index |
| Agent guardrails | One canonical root instruction source exists; `CLAUDE.md` imports `AGENTS.md`; archive/review path rules exist; no stray competing instruction files are in active use. | Conflicting instruction sources or missing archive rules |
| Governance | CODEOWNERS covers authoritative paths; protected branch requires status checks and appropriate reviews. | Unowned authoritative paths or missing branch protections |

The clean gate in the reviewer prompt should therefore stop using fixed issue counts. OpenAI’s current evaluation guidance is explicit that evaluation should be continuous, automated where possible, and tied to specific objective, dataset and metrics rather than vague “seems fine” judgements. The right replacement for “there are fewer than N issues left” is “the machine gate passes and no blocking category is red”. In practice, the reviewer prompt should read `package_meta/generated/handover_gate.json` and fail the review whenever `gate_pass` is false, any `blocking_failures` remain, or any must-have coverage metric falls below target. Open issues can still exist, but only as triaged warnings, not as blockers disguised by a low count. citeturn27view0turn24view2turn24view3turn23view0turn13view3

A useful replacement clause for the steward prompt is:

> Assess handover readiness against `package_meta/generated/handover_gate.json`. Do **not** score readiness by raw issue count. Report `pass`, `blockers`, `warnings`, `missing_evidence`, and `required_moves`. Fail if any blocker exists in authority separation, currentness, contract validation, schema/example mapping, provenance locking, generated index freshness, or agent navigation guardrails.

That turns review into a repeatable gate, not an impressionistic sweep. citeturn23view0turn24view2turn27view0

## Archive and reproducible review policy

Copied source-context snapshots and historical overlays should be retained in two stages. If a copied input is still actively informing work, keep it under `06_active_supporting_research/source_inputs/` with a manifest and checksum entry. Once it becomes historical rather than active, move the raw payload into `legacy_reference/source_snapshots/` or `legacy_reference/historical_overlays/`, keep a small manifest next to it, and index it in `source_inputs.lock.json`. To prevent that material polluting developer handover packages, tag those paths with `export-ignore` so they do not enter generated archives; keep only their manifests and archive index visible by default. SPDX gives the rationale for the checksum lock, and Git gives the mechanism for excluding these archival payloads from export packages. citeturn19view1turn19view3turn32view0turn32view1

Reviewer prompts and their outputs should be stored as reproducible workflows, not as ad hoc markdown notes. Each reusable review should therefore live as a tuple: `prompt.md`, `output.schema.json`, optional `eval.dataset.jsonl`, and immutable `review_runs/<timestamp-or-run-id>/` folders containing the source commit, source checksums, model identifier, parameters, raw output and normalised verdict. OpenAI’s current structured output guidance supports strict JSON Schema-constrained outputs, and its eval guidance already models runs as prompt templates plus datasets with explicit schemas. That is a near-perfect fit for repository stewardship reviews. citeturn23view0turn23view1turn24view2turn24view3turn27view0

For AI-agent fence lines, I would do three things. First, keep one root `AGENTS.md` as the cross-tool instruction source. Second, keep `CLAUDE.md` as a thin import wrapper around it. Third, add path-specific archive rules: a `.claude/rules/archive.md` scoped to `legacy_reference/**` and `reviewed_*/**`, and, where useful, an `AGENTS.override.md` inside those trees saying “historical only; never cite as active source”. That works because Codex discovers layered `AGENTS` files along the path to the working directory, while Claude supports path-scoped rules and warns that conflicting instructions reduce reliability. citeturn30view0turn30view2turn36view0turn33view0turn33view1

## Developer handover and risks

A developer handover checklist should be short enough to follow and strict enough to stop blind repository spelunking. I would require the following sequence on day one: open `README.md`; open `AGENTS.md`; open `package_meta/generated/authority.index.json`; run the validator; use `traceability.index.json` to move from concept to baseline/RFC/schema/example/conformance; and treat `reviewed_*`, `legacy_reference`, `05_project_handoff_and_prompts`, and `07_linked_domain_architectures` as non-authoritative unless the task explicitly calls for them. In agent-driven work, launch the agent from repo root when possible, not from an archive subtree, because both Codex and Claude resolve instructions by path and can load more local guidance when run deep in the tree. citeturn30view2turn36view2turn33view0turn13view3

The main risks and the structural mitigations are these.

| Risk | Why it happens | Structural mitigation |
|---|---|---|
| AI agent chooses a stale file with the right name | Duplicate or near-duplicate filenames exist across active, review and legacy areas | Enforce unique canonical IDs, generate `authority.index.json`, and fail validation on ambiguous “current” matches |
| Review output is mistaken for source of truth | Review notes sit beside active material or use similar names | Keep all reviews under `05/review_runs` or `reviewed_*`, mark them non-citable, and ban active references to them |
| Bundles drift away from source schemas | Bundled files are hand-edited or treated as peers of source schemas | Keep bundles under `*_generated`, regenerate in CI, and fail on diff |
| Archive payload dominates search/navigation | Historical text is stored unpacked and linked from active entry points | Move raw payloads to `legacy_reference`, compress snapshots where appropriate, exclude from export packages, and keep only one archive entry point |
| Agent instructions become contradictory | Multiple instruction files accumulate over time | Keep one root `AGENTS.md`, import it into `CLAUDE.md`, and periodically prune path rules; validator fails on competing instruction sources |
| Accepted decisions are rewritten in place | No immutable accepted/superseded lifecycle exists | Keep accepted RFCs immutable and require explicit supersession |
| Handover quality is judged by issue count | Low counts can hide severity and coverage gaps | Replace counts with `handover_gate.json` and category-based blockers |

The underlying pattern behind those mitigations is consistent across the sources: accepted artefacts should be immutable and superseded explicitly; generated indexes should be rebuildable; instruction files help but do not enforce behaviour; and branch protection plus status checks should enforce the repository’s actual safety rail. OFARM 2 should therefore preserve its semantic law exactly as-is, but convert repository hygiene into a combination of structural fences, generated maps and failing validation. That is the shortest path to a clean development handover without flattening the authority model or losing review and legacy context. citeturn35view2turn10view1turn38view0turn13view3turn13view5