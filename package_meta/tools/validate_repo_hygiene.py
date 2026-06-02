#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_SHA256_CACHE: dict[str, str] = {}

ALLOWED_MATERIAL_STATUSES = {
    'ACTIVE_BASELINE','COMPANION_ARTIFACT','ACCEPTED_RFC','MACHINE_CONTRACT',
    'IMPLEMENTATION_CONFORMANCE','ACTIVE_SUPPORTING_RESEARCH','HANDOFF_PROMPT',
    'LINKED_DOMAIN_ARCHITECTURE','REVIEW_HOLDING','LEGACY_REFERENCE',
    'ROOT_PACKAGE_METADATA','PACKAGE_METADATA'
}

MANIFEST_SELF_EXCLUSIONS = {'MANIFEST.csv'}
STATUS_SELF_EXCLUSIONS = {'MANIFEST.csv','MATERIAL_STATUS.csv','MATERIAL_STATUS.json'}

ROOT_ALLOWLIST = {
    'README.md','CURRENT_ACTIVE_ENTRYPOINT.md','CURRENT_ACTIVE_ENTRYPOINT.json','CURRENT_DELTA.md',
    'CURRENT_PACKAGE_CHANGELOG.md','PROJECT_AUTHORITY.md','ACTIVE_SUBSTANCE_README.md','AGENT_NAVIGATION.md',
    'STATUS_TAXONOMY.md','STATUS_TAXONOMY.json','TRACEABILITY_INDEX.md','TRACEABILITY_INDEX.json',
    'SOURCE_INPUT_INDEX.md','SOURCE_INPUT_INDEX.json','DECISION_INDEX.md','DECISION_INDEX.json',
    'DEVELOPMENT_HANDOVER.md','AUDIT_STRESS_CHAIN_COVERAGE.md','AUDIT_STRESS_CHAIN_COVERAGE.json','REVIEW_HOLDING_INDEX.md','REVIEW_HOLDING_INDEX.json',
    'REPOSITORY_CROSS_REFERENCE_SCAN.md','REPOSITORY_CROSS_REFERENCE_SCAN.json',
    'MANIFEST.csv','MATERIAL_STATUS.csv','MATERIAL_STATUS.json','REVIEW_HOLDING_INDEX.md','REVIEW_HOLDING_INDEX.json','agent_authority_map.json',
    'AGENTS.md','CLAUDE.md','llms.txt','.gitattributes','LICENSE'
}

REQUIRED_FILES = [
    'README.md','CURRENT_ACTIVE_ENTRYPOINT.md','CURRENT_ACTIVE_ENTRYPOINT.json','CURRENT_DELTA.md',
    'CURRENT_PACKAGE_CHANGELOG.md','PROJECT_AUTHORITY.md','ACTIVE_SUBSTANCE_README.md','AGENT_NAVIGATION.md',
    'AGENTS.md','CLAUDE.md','llms.txt','.gitattributes','.claude/rules/archive.md',
    'STATUS_TAXONOMY.md','STATUS_TAXONOMY.json','TRACEABILITY_INDEX.md','TRACEABILITY_INDEX.json',
    'SOURCE_INPUT_INDEX.md','SOURCE_INPUT_INDEX.json','DECISION_INDEX.md','DECISION_INDEX.json',
    'DEVELOPMENT_HANDOVER.md','AUDIT_STRESS_CHAIN_COVERAGE.md','AUDIT_STRESS_CHAIN_COVERAGE.json','REVIEW_HOLDING_INDEX.md','REVIEW_HOLDING_INDEX.json',
    'REPOSITORY_CROSS_REFERENCE_SCAN.md','REPOSITORY_CROSS_REFERENCE_SCAN.json',
    '03_machine_contracts/README.md','03_machine_contracts/folder.status.json','03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json',
    '03_machine_contracts/CONTRACT_INDEX.json','03_machine_contracts/EXAMPLE_SCHEMA_MAP.json',
    '03_machine_contracts/DRAFT_NON_DEFAULT_INDEX.json','03_machine_contracts/PATH_REMAPS.json',
    '04_implementation_and_conformance/README.md','04_implementation_and_conformance/folder.status.json','04_implementation_and_conformance/IMPLEMENTATION_LANE_INDEX.json',
    '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/README.md',
    '04_implementation_and_conformance/examples_and_fixtures/examples/EXAMPLE_INDEX.json','04_implementation_and_conformance/examples_and_fixtures/examples/EXAMPLE_INDEX.md',
    '04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/README.md',
    '04_implementation_and_conformance/examples_and_fixtures/fixtures/FIXTURE_INDEX.json','04_implementation_and_conformance/examples_and_fixtures/fixtures/FIXTURE_INDEX.md',
    '05_project_handoff_and_prompts/README.md','05_project_handoff_and_prompts/folder.status.json',
    '05_project_handoff_and_prompts/HANDOFF_PROMPT_INDEX.json','05_project_handoff_and_prompts/HANDOFF_PROMPT_INDEX.md',
    '05_project_handoff_and_prompts/prompts/README.md','05_project_handoff_and_prompts/prompts/folder.status.json',
    '05_project_handoff_and_prompts/prompts/REVIEWER_PROMPT_INDEX.json','05_project_handoff_and_prompts/prompts/REVIEWER_PROMPT_INDEX.md',
    '05_project_handoff_and_prompts/output_schemas/farm_review_output_schema.json',
    '05_project_handoff_and_prompts/output_schemas/README.md','05_project_handoff_and_prompts/output_schemas/folder.status.json',
    '05_project_handoff_and_prompts/eval_datasets/README.md','05_project_handoff_and_prompts/eval_datasets/folder.status.json',
    '05_project_handoff_and_prompts/review_runs/README.md','05_project_handoff_and_prompts/review_runs/folder.status.json',
    '05_project_handoff_and_prompts/reports_and_maps/README.md','05_project_handoff_and_prompts/reports_and_maps/folder.status.json',
    '05_project_handoff_and_prompts/prompts/OFARM_Standalone_Reviewer_Prompt_Repository_Steward_v0_1.md',
    '06_active_supporting_research/README.md','06_active_supporting_research/folder.status.json',
    '06_active_supporting_research/RESEARCH_INDEX.json','06_active_supporting_research/RESEARCH_INDEX.md',
    '06_active_supporting_research/source_inputs/deep-research-report-repository-cleanup-and-handover-readiness-2026-05-15.md',
    'legacy_reference/README.md','legacy_reference/README_READ_ONLY.md','legacy_reference/AGENTS.override.md','legacy_reference/folder.status.json',
    'legacy_reference/LEGACY_REFERENCE_INDEX.json','legacy_reference/LEGACY_REFERENCE_INDEX.md',
    'package_meta/README.md','package_meta/folder.status.json','package_meta/package.json','package_meta/release.manifest.json',
    'package_meta/PACKAGE_META_INDEX.json','package_meta/PACKAGE_META_INDEX.md',
    'package_meta/generated/README.md','package_meta/generated/folder.status.json',
    'package_meta/tools/README.md','package_meta/tools/folder.status.json',
    'package_meta/tools/check_generated_currentness.py','package_meta/tools/check_repository_cross_references.py',
    'package_meta/schemas/README.md','package_meta/schemas/folder.status.json',
    'package_meta/generated/authority.index.json','package_meta/generated/materials.index.json',
    'package_meta/generated/contracts.index.json','package_meta/generated/schema_example_map.json',
    'package_meta/generated/source_inputs.lock.json','package_meta/generated/traceability.index.json',
    'package_meta/generated/review_runs.index.jsonl','package_meta/generated/handover_gate.json',
    'package_meta/REPOSITORY_STEWARD_CHECKLIST.md','package_meta/tools/validate_repo_hygiene.py',
    'package_meta/final_validation_2026_05_19/README.md',
    'package_meta/final_validation_2026_05_19/folder.status.json',
    'package_meta/final_validation_2026_05_19/OFARM_phase15_final_validation_report_v0_1.json',
    'package_meta/final_validation_2026_05_19/OFARM_phase15_final_validation_report_v0_1.md',
    'package_meta/final_validation_2026_05_19/OFARM_repository_currentness_cleanup_report_v0_1.json',
    'package_meta/final_validation_2026_05_19/OFARM_repository_currentness_cleanup_report_v0_1.md',
    'package_meta/final_validation_2026_05_19/OFARM_unresolved_debt_register_v0_1.json',
    'package_meta/final_validation_2026_05_19/OFARM_unresolved_debt_register_v0_1.md',
    'package_meta/final_validation_2026_05_19/OFARM_final_release_notes_v0_1.md',
    'package_meta/final_validation_2026_05_19/README.md',
    'package_meta/final_validation_2026_05_19/folder.status.json',
    'package_meta/final_validation_2026_05_19/OFARM_phase15_final_validation_report_v0_1.json',
    'package_meta/final_validation_2026_05_19/OFARM_phase15_final_validation_report_v0_1.md',
    'package_meta/final_validation_2026_05_19/OFARM_repository_currentness_cleanup_report_v0_1.json',
    'package_meta/final_validation_2026_05_19/OFARM_repository_currentness_cleanup_report_v0_1.md',
    'package_meta/final_validation_2026_05_19/OFARM_unresolved_debt_register_v0_1.json',
    'package_meta/final_validation_2026_05_19/OFARM_unresolved_debt_register_v0_1.md',
    'package_meta/final_validation_2026_05_19/OFARM_final_release_notes_v0_1.md',
    'package_meta/final_validation_2026_05_19/README.md',
    'package_meta/final_validation_2026_05_19/folder.status.json',
    'package_meta/final_validation_2026_05_19/OFARM_phase15_final_validation_report_v0_1.json',
    'package_meta/final_validation_2026_05_19/OFARM_phase15_final_validation_report_v0_1.md',
    'package_meta/final_validation_2026_05_19/OFARM_repository_currentness_cleanup_report_v0_1.json',
    'package_meta/final_validation_2026_05_19/OFARM_repository_currentness_cleanup_report_v0_1.md',
    'package_meta/final_validation_2026_05_19/OFARM_unresolved_debt_register_v0_1.json',
    'package_meta/final_validation_2026_05_19/OFARM_unresolved_debt_register_v0_1.md',
    'package_meta/final_validation_2026_05_19/OFARM_final_release_notes_v0_1.md',
]

REQUIRED_FILES = list(dict.fromkeys(REQUIRED_FILES))

DISALLOWED_ROOT_PATTERNS = [
    re.compile(r'^PATCH_APPLY_GUIDE.*\.md$'),
    re.compile(r'.*PACKAGE_README.*\.md$'),
    re.compile(r'^FARM_OWNER_CONSOLIDATED_ADDENDUM_README\.md$'),
    re.compile(r'^CONSOLIDATED_PACKAGE_README_.*\.md$'),
    re.compile(r'^PROJECT_PROMPT\.md$'),
    re.compile(r'^MIGRATION_INVENTORY\.md$')
]

TOP_LEVEL_STATUS_REQUIRED = [
    '00_active_baseline','01_companion_artifacts','02_accepted_rfcs','03_machine_contracts',
    '04_implementation_and_conformance','05_project_handoff_and_prompts','06_active_supporting_research',
    '07_linked_domain_architectures','legacy_reference','package_meta'
]

IGNORED_FILE_TREE_DIRS = {'.git'}


def sha256(path: Path) -> str:
    rel = path.relative_to(REPO).as_posix() if path.is_absolute() else path.as_posix()
    if rel in _SHA256_CACHE:
        return _SHA256_CACHE[rel]
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    value = h.hexdigest()
    _SHA256_CACHE[rel] = value
    return value

def rel_files() -> list[str]:
    files: list[str] = []
    for p in REPO.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(REPO)
        if any(part in IGNORED_FILE_TREE_DIRS for part in rel.parts):
            continue
        files.append(rel.as_posix())
    return sorted(files)

def load_json(rel: str):
    return json.loads((REPO/rel).read_text(encoding='utf-8'))

def validate_rows_have_current_hash(rows: list[dict], issues: list[str], label: str) -> None:
    for row in rows:
        rel = row.get('path')
        if not rel:
            issues.append(f'{label} row missing path: {row}')
            continue
        p = REPO / rel
        if not p.exists():
            continue
        if 'bytes' in row and str(p.stat().st_size) != str(row['bytes']):
            issues.append(f'{label} bytes mismatch for {rel}: row={row["bytes"]} actual={p.stat().st_size}')
        if 'sha256' in row and row['sha256'] != sha256(p):
            issues.append(f'{label} sha256 mismatch for {rel}')

def main() -> int:
    issues: list[str] = []
    files = rel_files()
    file_set = set(files)

    if any(Path(f).name == '.DS_Store' for f in files): issues.append('forbidden .DS_Store residue present')
    if any('__MACOSX' in f for f in files): issues.append('forbidden __MACOSX residue present')
    if any('__pycache__' in f for f in files): issues.append('forbidden __pycache__ residue present')
    if any(f.endswith('.pyc') for f in files): issues.append('forbidden .pyc residue present')

    root_files = {p.name for p in REPO.iterdir() if p.is_file()}
    unexpected = sorted(root_files - ROOT_ALLOWLIST)
    if unexpected: issues.append(f'unexpected root files: {unexpected}')
    for name in root_files:
        if any(pat.match(name) for pat in DISALLOWED_ROOT_PATTERNS):
            issues.append(f'obsolete root overlay still at root: {name}')

    for rel in REQUIRED_FILES:
        if rel not in file_set: issues.append(f'missing required file: {rel}')

    for d in TOP_LEVEL_STATUS_REQUIRED:
        if (REPO/d).exists() and not (REPO/d/'folder.status.json').exists():
            issues.append(f'top-level folder missing folder.status.json: {d}')

    claude = (REPO/'CLAUDE.md').read_text(encoding='utf-8') if (REPO/'CLAUDE.md').exists() else ''
    if '@AGENTS.md' not in claude: issues.append('CLAUDE.md does not import @AGENTS.md')
    if not (REPO/'.claude/rules/archive.md').exists(): issues.append('missing .claude/rules/archive.md')

    with (REPO/'MANIFEST.csv').open(newline='', encoding='utf-8') as f:
        manifest = list(csv.DictReader(f))
    manifest_paths = {row['path'] for row in manifest}
    expected_manifest = file_set - MANIFEST_SELF_EXCLUSIONS
    if manifest_paths != expected_manifest:
        issues.append(f'manifest path set mismatch: missing={sorted(expected_manifest-manifest_paths)[:10]} extra={sorted(manifest_paths-expected_manifest)[:10]}')
    validate_rows_have_current_hash(manifest, issues, 'manifest')

    with (REPO/'MATERIAL_STATUS.csv').open(newline='', encoding='utf-8') as f:
        status_rows = list(csv.DictReader(f))
    status_map = {row['path']: row for row in status_rows}
    status_json = load_json('MATERIAL_STATUS.json')
    status_json_map = {row['path']: row for row in status_json.get('records', [])}
    expected_status = file_set - STATUS_SELF_EXCLUSIONS
    if set(status_map) != expected_status:
        issues.append(f'status csv path set mismatch: missing={sorted(expected_status-set(status_map))[:10]} extra={sorted(set(status_map)-expected_status)[:10]}')
    if set(status_json_map) != expected_status:
        issues.append(f'status json path set mismatch: missing={sorted(expected_status-set(status_json_map))[:10]} extra={sorted(set(status_json_map)-expected_status)[:10]}')
    for row in status_rows:
        if row.get('status') not in ALLOWED_MATERIAL_STATUSES:
            issues.append(f'invalid material status {row.get("status")} for {row.get("path")}')
    validate_rows_have_current_hash(status_rows, issues, 'status csv')
    validate_rows_have_current_hash(list(status_json_map.values()), issues, 'status json')
    for rel, row in status_map.items():
        if rel in status_json_map and row.get('status') != status_json_map[rel].get('status'):
            issues.append(f'status csv/json disagree for {rel}')

    agent = load_json('agent_authority_map.json')
    if agent.get('date') != '2026-05-20': issues.append('agent_authority_map.json date is stale')
    if '"review_holding/"' in json.dumps(agent): issues.append('agent_authority_map.json contains stale review_holding/ pseudo-folder')
    current = load_json('CURRENT_ACTIVE_ENTRYPOINT.json')
    if not current.get('repositoryCleanupApplied'): issues.append('CURRENT_ACTIVE_ENTRYPOINT.json does not record repository cleanup')
    if not current.get('repositoryHandoverPublicationLayerApplied'): issues.append('CURRENT_ACTIVE_ENTRYPOINT.json does not record publication layer')

    reviewed_roots = sorted(REPO.glob('reviewed_*'))
    if reviewed_roots:
        issues.append(f'reviewed_* folders remain in root after archive move: {[d.name for d in reviewed_roots]}')
    if not (REPO/'REVIEW_HOLDING_INDEX.json').exists():
        issues.append('missing root REVIEW_HOLDING_INDEX.json')
    else:
        rhi = load_json('REVIEW_HOLDING_INDEX.json')
        archive_rel = rhi.get('archivePath')
        if not archive_rel or not (REPO/archive_rel).exists():
            issues.append('REVIEW_HOLDING_INDEX.json archivePath does not exist')
        if rhi.get('activeLaw') is not False or rhi.get('doesNotOverrideActiveBaseline') is not True:
            issues.append('REVIEW_HOLDING_INDEX.json does not preserve review-holding-only authority flags')
        if rhi.get('latestControlledPromotion') not in {'AAI-CP10','CP12','CP13','CP14','CP15'}:
            issues.append('REVIEW_HOLDING_INDEX.json does not identify acceptable historical/current controlled promotion')
        if rhi.get('activeSchemaSameBasenameCopiesVisibleInRepository') != 0:
            issues.append('REVIEW_HOLDING_INDEX.json does not record zero visible active-schema basename copies')
        if rhi.get('archivePath') and (REPO/rhi['archivePath']).exists() and rhi.get('archiveSha256') != sha256(REPO/rhi['archivePath']):
            issues.append('REVIEW_HOLDING_INDEX.json archive sha256 drift')


    if not (REPO/'REPOSITORY_CROSS_REFERENCE_SCAN.json').exists():
        issues.append('missing root REPOSITORY_CROSS_REFERENCE_SCAN.json')
    else:
        rx = load_json('REPOSITORY_CROSS_REFERENCE_SCAN.json')
        if rx.get('status') != 'PASS':
            issues.append('REPOSITORY_CROSS_REFERENCE_SCAN.json status is not PASS')
        if rx.get('activeLaw') is not False or rx.get('doesNotOverrideActiveBaseline') is not True:
            issues.append('REPOSITORY_CROSS_REFERENCE_SCAN.json does not preserve non-active authority flags')
        if rx.get('summary', {}).get('fileCount') != len(files):
            issues.append('REPOSITORY_CROSS_REFERENCE_SCAN.json fileCount does not match current file tree')
        if rx.get('summary', {}).get('actionableBrokenMarkdownLinks') != 0:
            issues.append('REPOSITORY_CROSS_REFERENCE_SCAN.json records actionable broken markdown links')
        if rx.get('summary', {}).get('actionableStaleCurrentnessReferences') != 0:
            issues.append('REPOSITORY_CROSS_REFERENCE_SCAN.json records actionable stale currentness references')
        if rx.get('summary', {}).get('schemaCopyIndexCoverageIssues') != 0:
            issues.append('REPOSITORY_CROSS_REFERENCE_SCAN.json records schema-copy index coverage issues')
        if not (REPO/'REPOSITORY_CROSS_REFERENCE_SCAN.md').exists():
            issues.append('missing root REPOSITORY_CROSS_REFERENCE_SCAN.md')

    if (REPO/'03_machine_contracts/examples').exists(): issues.append('03_machine_contracts/examples should be moved to tier 04')
    if (REPO/'03_machine_contracts/fixtures').exists(): issues.append('03_machine_contracts/fixtures should be moved to tier 04')
    if (REPO/'03_machine_contracts/drafts_non_default/examples').exists(): issues.append('draft examples still under 03_machine_contracts')

    contract_index = load_json('03_machine_contracts/CONTRACT_INDEX.json')
    indexed = {r['path'] for r in contract_index.get('records', [])}
    exempt = {
        '03_machine_contracts/README.md','03_machine_contracts/folder.status.json','03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.md',
        '03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json','03_machine_contracts/CONTRACT_INDEX.md',
        '03_machine_contracts/CONTRACT_INDEX.json','03_machine_contracts/EXAMPLE_SCHEMA_MAP.md',
        '03_machine_contracts/EXAMPLE_SCHEMA_MAP.json','03_machine_contracts/DRAFT_NON_DEFAULT_INDEX.md',
        '03_machine_contracts/DRAFT_NON_DEFAULT_INDEX.json','03_machine_contracts/PATH_REMAPS.json'
    }
    machine_files = {f for f in files if f.startswith('03_machine_contracts/') and not f.endswith('/README.md')}
    missing_idx = sorted(machine_files - indexed - exempt)
    if missing_idx: issues.append(f'machine contract files missing from CONTRACT_INDEX.json: {missing_idx[:20]}')
    draft_index = load_json('03_machine_contracts/DRAFT_NON_DEFAULT_INDEX.json')
    draft_indexed = {r['path'] for r in draft_index.get('records', [])}
    draft_files = {f for f in files if (f.startswith('03_machine_contracts/') or f.startswith('04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/') or f.startswith('04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/')) and 'draft' in Path(f).name.lower() and Path(f).name not in {'DRAFT_NON_DEFAULT_INDEX.json','DRAFT_NON_DEFAULT_INDEX.md'}}
    missing_drafts = sorted(draft_files - draft_indexed)
    if missing_drafts: issues.append(f'draft files missing from DRAFT_NON_DEFAULT_INDEX.json: {missing_drafts[:20]}')
    exmap = load_json('03_machine_contracts/EXAMPLE_SCHEMA_MAP.json')
    mapped_examples = {r['examplePath'] for r in exmap.get('records', [])}
    example_files = {f for f in files if f.startswith('04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/') and '_example_' in Path(f).name.lower() and f.endswith('.json')}
    missing_examples = sorted(example_files - mapped_examples)
    if missing_examples: issues.append(f'contract examples missing from EXAMPLE_SCHEMA_MAP.json: {missing_examples[:20]}')
    for r in exmap.get('records', []):
        if not (REPO/r.get('examplePath','')).exists(): issues.append(f'EXAMPLE_SCHEMA_MAP example path missing: {r.get("examplePath")}')
        es = r.get('expectedSchema')
        if es and not (REPO/es).exists(): issues.append(f'EXAMPLE_SCHEMA_MAP expected schema missing: {es}')
    family = load_json('03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json')
    current_defaults = {fam.get('currentDefaultSchema') for fam in family.get('families', []) if fam.get('currentDefaultSchema')}
    bad_defaults = sorted([p for p in current_defaults if p and 'draft' in Path(p).name.lower()])
    if bad_defaults: issues.append(f'draft schemas marked as current defaults: {bad_defaults}')
    for p in current_defaults:
        if p and not (REPO/p).exists(): issues.append(f'current default schema path missing: {p}')
    for fam in family.get('families', []):
        for p in fam.get('examples', []):
            if not str(p).startswith('04_implementation_and_conformance/'):
                issues.append(f'currentness map example outside tier 04 implementation/conformance: {p}')
            if not (REPO/p).exists(): issues.append(f'currentness map example path missing: {p}')



    # Phase 8 example and fixture local coverage.
    for base_rel, index_rel in [
        ('04_implementation_and_conformance/examples_and_fixtures/examples', '04_implementation_and_conformance/examples_and_fixtures/examples/EXAMPLE_INDEX.json'),
        ('04_implementation_and_conformance/examples_and_fixtures/fixtures', '04_implementation_and_conformance/examples_and_fixtures/fixtures/FIXTURE_INDEX.json'),
    ]:
        base_path = REPO / base_rel
        if base_path.exists():
            for d in [base_path] + [p for p in base_path.rglob('*') if p.is_dir()]:
                if not (d / 'README.md').exists():
                    issues.append(f'example/fixture directory missing README.md: {d.relative_to(REPO).as_posix()}')
                if not (d / 'folder.status.json').exists():
                    issues.append(f'example/fixture directory missing folder.status.json: {d.relative_to(REPO).as_posix()}')
        if not (REPO / index_rel).exists():
            issues.append(f'missing example/fixture index: {index_rel}')
    if (REPO / '04_implementation_and_conformance/examples_and_fixtures/examples/EXAMPLE_INDEX.json').exists():
        ex_idx = load_json('04_implementation_and_conformance/examples_and_fixtures/examples/EXAMPLE_INDEX.json')
        if not ex_idx.get('validationSummary', {}).get('allMappedExamplesValidate'):
            issues.append('EXAMPLE_INDEX.json does not record all mapped examples as validating')
        mapped_in_index = {r.get('examplePath') for r in ex_idx.get('records', [])}
        if mapped_in_index != mapped_examples:
            issues.append('EXAMPLE_INDEX.json records do not match EXAMPLE_SCHEMA_MAP.json records')
    if (REPO / '04_implementation_and_conformance/examples_and_fixtures/fixtures/FIXTURE_INDEX.json').exists():
        fx_idx = load_json('04_implementation_and_conformance/examples_and_fixtures/fixtures/FIXTURE_INDEX.json')
        if not fx_idx.get('referenceValidation', {}).get('allDeclaredJsonFixtureReferencesResolve'):
            issues.append('FIXTURE_INDEX.json has unresolved declared fixture/example refs')

    impl_root_files = {p.name for p in (REPO/'04_implementation_and_conformance').iterdir() if p.is_file()}
    impl_allowed = {
        'README.md','IMPLEMENTATION_LANE_INDEX.json','IMPLEMENTATION_LANE_INDEX.md','folder.status.json',
        'IMPLEMENTATION_SUBFOLDER_INDEX.json','IMPLEMENTATION_SUBFOLDER_INDEX.md',
        'NON_ACTIVE_SCHEMA_COPY_INDEX.json','NON_ACTIVE_SCHEMA_COPY_INDEX.md'
    }
    if impl_root_files - impl_allowed: issues.append(f'implementation root has unlaned files: {sorted(impl_root_files-impl_allowed)[:20]}')
    impl_allowed_dirs = {'examples_and_fixtures','conformance_runners','controlled_promotion_evidence','implementation_notes','service_and_sdk_candidates','pilot_material','historical_archive','spikes_incubation'}
    impl_root_dirs = {p.name for p in (REPO/'04_implementation_and_conformance').iterdir() if p.is_dir()}
    if impl_root_dirs != impl_allowed_dirs: issues.append(f'implementation root dirs are not controlled lanes: {sorted(impl_root_dirs)}')

    # 05 root should be clean: README and folder.status only.
    handoff_root_files = {p.name for p in (REPO/'05_project_handoff_and_prompts').iterdir() if p.is_file()}
    handoff_allowed = {'README.md','folder.status.json','HANDOFF_PROMPT_INDEX.json','HANDOFF_PROMPT_INDEX.md'}
    if handoff_root_files - handoff_allowed: issues.append(f'handoff root has unlaned files: {sorted(handoff_root_files-handoff_allowed)[:20]}')

    rp = load_json('05_project_handoff_and_prompts/prompts/REVIEWER_PROMPT_INDEX.json')
    if rp.get('package') != current.get('package'):
        issues.append('REVIEWER_PROMPT_INDEX.json package does not match current package')
    if rp.get('activeLaw') is not False or rp.get('doesNotOverrideActiveBaseline') is not True:
        issues.append('REVIEWER_PROMPT_INDEX.json does not preserve supporting-only authority flags')
    for sr in rp.get('schemaRecords', []):
        if not (REPO/sr['path']).exists(): issues.append(f'reviewer schema missing: {sr["path"]}')
        elif 'sha256' in sr and sr['sha256'] != sha256(REPO/sr['path']): issues.append(f'reviewer schema hash drift: {sr["path"]}')
    for pr in rp.get('promptRecords', []):
        if not (REPO/pr['path']).exists(): issues.append(f'reviewer prompt missing: {pr["path"]}')
        elif 'sha256' in pr and pr['sha256'] != sha256(REPO/pr['path']): issues.append(f'reviewer prompt hash drift: {pr["path"]}')

    handoff_root = REPO / '05_project_handoff_and_prompts'
    if handoff_root.exists():
        for d in [handoff_root] + [x for x in handoff_root.rglob('*') if x.is_dir()]:
            if not (d / 'README.md').exists():
                issues.append(f'handoff directory missing README.md: {d.relative_to(REPO).as_posix()}')
            if not (d / 'folder.status.json').exists():
                issues.append(f'handoff directory missing folder.status.json: {d.relative_to(REPO).as_posix()}')
        hidx = load_json('05_project_handoff_and_prompts/HANDOFF_PROMPT_INDEX.json')
        expected_handoff = {
            x.relative_to(REPO).as_posix()
            for x in handoff_root.rglob('*')
            if x.is_file() and x.relative_to(REPO).as_posix() not in {
                '05_project_handoff_and_prompts/HANDOFF_PROMPT_INDEX.json',
                '05_project_handoff_and_prompts/HANDOFF_PROMPT_INDEX.md'
            }
        }
        indexed_handoff = {r.get('path') for r in hidx.get('records', [])}
        if indexed_handoff != expected_handoff:
            issues.append(f'HANDOFF_PROMPT_INDEX.json path set mismatch: missing={sorted(expected_handoff-indexed_handoff)[:10]} extra={sorted(indexed_handoff-expected_handoff)[:10]}')
        if hidx.get('activeLaw') is not False or hidx.get('doesNotOverrideActiveBaseline') is not True:
            issues.append('HANDOFF_PROMPT_INDEX.json does not preserve supporting-only authority flags')
        validate_rows_have_current_hash(hidx.get('records', []), issues, 'handoff prompt index')
        if hidx.get('package') != current.get('package'):
            issues.append('HANDOFF_PROMPT_INDEX.json package does not match current package')
        if hidx.get('latestControlledPromotion') not in {'AAI-CP10','CP12','CP13','CP14','CP15'}:
            issues.append('HANDOFF_PROMPT_INDEX.json does not identify acceptable historical/current controlled promotion')

    ti = load_json('TRACEABILITY_INDEX.json')
    for item in ti.get('items', []):
        for key in ['authority','rfc','schemas','examplesOrConformance']:
            for p in item.get(key, []):
                if p and not (REPO/p).exists(): issues.append(f'TRACEABILITY_INDEX path missing: {p}')
    si = load_json('SOURCE_INPUT_INDEX.json')
    for row in si.get('records', []):
        if not (REPO/row['path']).exists(): issues.append(f'SOURCE_INPUT_INDEX path missing: {row["path"]}')
    validate_rows_have_current_hash(si.get('records', []), issues, 'source input index')
    for group in si.get('duplicateChecksumGroups', []):
        h = group.get('sha256')
        for p in group.get('paths', []):
            if (REPO/p).exists() and sha256(REPO/p) != h:
                issues.append(f'SOURCE_INPUT_INDEX duplicate checksum drift: {p}')


    # Phase 9 active supporting research local coverage.
    research_root = REPO / '06_active_supporting_research'
    if research_root.exists():
        for d in [research_root] + [p for p in research_root.rglob('*') if p.is_dir()]:
            if not (d / 'README.md').exists():
                issues.append(f'research directory missing README.md: {d.relative_to(REPO).as_posix()}')
            if not (d / 'folder.status.json').exists():
                issues.append(f'research directory missing folder.status.json: {d.relative_to(REPO).as_posix()}')
        if not (research_root / 'RESEARCH_INDEX.json').exists():
            issues.append('missing research index: 06_active_supporting_research/RESEARCH_INDEX.json')
        else:
            research_index = load_json('06_active_supporting_research/RESEARCH_INDEX.json')
            expected_research = {
                p.relative_to(REPO).as_posix()
                for p in research_root.rglob('*')
                if p.is_file()
                and p.relative_to(REPO).as_posix() not in {
                    '06_active_supporting_research/RESEARCH_INDEX.json',
                    '06_active_supporting_research/RESEARCH_INDEX.md'
                }
            }
            indexed_research = {r.get('path') for r in research_index.get('records', [])}
            if indexed_research != expected_research:
                issues.append(f'RESEARCH_INDEX.json path set mismatch: missing={sorted(expected_research-indexed_research)[:10]} extra={sorted(indexed_research-expected_research)[:10]}')
            if research_index.get('activeLaw') is not False or research_index.get('doesNotOverrideActiveBaseline') is not True:
                issues.append('RESEARCH_INDEX.json does not preserve supporting-only authority flags')
            validate_rows_have_current_hash(research_index.get('records', []), issues, 'research index')


    # Phase 12 legacy reference local coverage.
    legacy_root = REPO / 'legacy_reference'
    if legacy_root.exists():
        if not (legacy_root / 'LEGACY_REFERENCE_INDEX.json').exists():
            issues.append('missing legacy reference index: legacy_reference/LEGACY_REFERENCE_INDEX.json')
        for d in [legacy_root] + [p for p in legacy_root.rglob('*') if p.is_dir()]:
            if not (d / 'README.md').exists():
                issues.append(f'legacy reference directory missing README.md: {d.relative_to(REPO).as_posix()}')
            if not (d / 'folder.status.json').exists():
                issues.append(f'legacy reference directory missing folder.status.json: {d.relative_to(REPO).as_posix()}')
        if (legacy_root / 'LEGACY_REFERENCE_INDEX.json').exists():
            legacy_index = load_json('legacy_reference/LEGACY_REFERENCE_INDEX.json')
            expected_legacy = {
                p.relative_to(REPO).as_posix()
                for p in legacy_root.rglob('*')
                if p.is_file()
                and p.relative_to(REPO).as_posix() not in {
                    'legacy_reference/LEGACY_REFERENCE_INDEX.json',
                    'legacy_reference/LEGACY_REFERENCE_INDEX.md'
                }
            }
            indexed_legacy = {r.get('path') for r in legacy_index.get('records', [])}
            if indexed_legacy != expected_legacy:
                issues.append(f'LEGACY_REFERENCE_INDEX.json path set mismatch: missing={sorted(expected_legacy-indexed_legacy)[:10]} extra={sorted(indexed_legacy-expected_legacy)[:10]}')
            if legacy_index.get('activeLaw') is not False or legacy_index.get('doesNotOverrideActiveBaseline') is not True or legacy_index.get('readOnlyContextualReference') is not True:
                issues.append('LEGACY_REFERENCE_INDEX.json does not preserve read-only legacy authority flags')
            if legacy_index.get('latestControlledPromotion') not in {'AAI-CP10','CP12','CP13','CP14','CP15'}:
                issues.append('LEGACY_REFERENCE_INDEX.json does not identify acceptable historical/current controlled promotion')
            validate_rows_have_current_hash(legacy_index.get('records', []), issues, 'legacy reference index')
            directory_records = legacy_index.get('directoryRecords', [])
            if not all(r.get('hasReadme') and r.get('hasFolderStatus') for r in directory_records):
                issues.append('LEGACY_REFERENCE_INDEX.json does not record full legacy directory README/status coverage')
            active_schema_names = {p.name for p in (REPO/'03_machine_contracts'/'schemas').rglob('*.json')}
            actual_schema_basename_copies = {
                p.relative_to(REPO).as_posix()
                for p in legacy_root.rglob('*.json')
                if p.name in active_schema_names
            }
            indexed_schema_basename_copies = {r.get('legacyPath') for r in legacy_index.get('activeSchemaBasenameCopies', [])}
            if indexed_schema_basename_copies != actual_schema_basename_copies:
                issues.append(f'LEGACY_REFERENCE_INDEX.json active-schema basename copy mismatch: missing={sorted(actual_schema_basename_copies-indexed_schema_basename_copies)[:10]} extra={sorted(indexed_schema_basename_copies-actual_schema_basename_copies)[:10]}')

    # Phase 13 package metadata and generated-currentness coverage.
    def status_for_current_file(rel: str) -> str:
        name = Path(rel).name
        if name in {'README.md','folder.status.json'} or name.endswith('.status.json'):
            if '/' in rel:
                return 'PACKAGE_METADATA'
        if rel.startswith('00_active_baseline/'):
            return 'ACTIVE_BASELINE'
        if rel.startswith('01_companion_artifacts/'):
            return 'COMPANION_ARTIFACT'
        if rel.startswith('02_accepted_rfcs/'):
            return 'ACCEPTED_RFC'
        if rel.startswith('03_machine_contracts/'):
            return 'MACHINE_CONTRACT'
        if rel.startswith('04_implementation_and_conformance/'):
            return 'IMPLEMENTATION_CONFORMANCE'
        if rel.startswith('05_project_handoff_and_prompts/'):
            return 'HANDOFF_PROMPT'
        if rel.startswith('06_active_supporting_research/'):
            return 'ACTIVE_SUPPORTING_RESEARCH'
        if rel.startswith('07_linked_domain_architectures/'):
            return 'LINKED_DOMAIN_ARCHITECTURE'
        if rel.startswith('legacy_reference/'):
            return 'LEGACY_REFERENCE'
        if rel.startswith('archive/review_holding/'):
            return 'REVIEW_HOLDING' if Path(rel).name.endswith('.zip') else 'PACKAGE_METADATA'
        if rel.startswith('package_meta/'):
            return 'PACKAGE_METADATA'
        if rel.startswith('reviewed_'):
            return 'REVIEW_HOLDING'
        return 'ROOT_PACKAGE_METADATA'

    package_meta_root = REPO / 'package_meta'
    if package_meta_root.exists():
        for d in [package_meta_root] + [p for p in package_meta_root.rglob('*') if p.is_dir()]:
            if not (d / 'README.md').exists():
                issues.append(f'package_meta directory missing README.md: {d.relative_to(REPO).as_posix()}')
            if not (d / 'folder.status.json').exists():
                issues.append(f'package_meta directory missing folder.status.json: {d.relative_to(REPO).as_posix()}')
        if not (package_meta_root / 'PACKAGE_META_INDEX.json').exists():
            issues.append('missing package metadata index: package_meta/PACKAGE_META_INDEX.json')
        else:
            pmi = load_json('package_meta/PACKAGE_META_INDEX.json')
            expected_pm = {
                p.relative_to(REPO).as_posix()
                for p in package_meta_root.rglob('*')
                if p.is_file()
                and p.relative_to(REPO).as_posix() not in {
                    'package_meta/PACKAGE_META_INDEX.json',
                    'package_meta/PACKAGE_META_INDEX.md'
                }
            }
            indexed_pm = {r.get('path') for r in pmi.get('records', [])}
            if indexed_pm != expected_pm:
                issues.append(f'PACKAGE_META_INDEX.json path set mismatch: missing={sorted(expected_pm-indexed_pm)[:10]} extra={sorted(indexed_pm-expected_pm)[:10]}')
            if pmi.get('activeLaw') is not False or pmi.get('doesNotOverrideActiveBaseline') is not True:
                issues.append('PACKAGE_META_INDEX.json does not preserve package-metadata-only authority flags')
            if pmi.get('latestControlledPromotion') not in {'AAI-CP10','CP12','CP13','CP14','CP15'}:
                issues.append('PACKAGE_META_INDEX.json does not identify acceptable historical/current controlled promotion')
            validate_rows_have_current_hash(pmi.get('records', []), issues, 'package meta index')
            if not all(r.get('hasReadme') and r.get('hasFolderStatus') for r in pmi.get('directoryRecords', [])):
                issues.append('PACKAGE_META_INDEX.json does not record full package_meta directory README/status coverage')
            for wr in pmi.get('workflowRecords', []):
                path = wr.get('path')
                if path == '.github/workflows/validate.yml' and not wr.get('runsRepositoryValidationSuiteWrapper'):
                    issues.append('validate.yml does not run repository validation suite wrapper')
                if path == '.github/workflows/validate_generated_currentness.yml' and not wr.get('runsGeneratedCurrentnessChecker'):
                    issues.append('validate_generated_currentness.yml does not run generated currentness checker')
        validate_wf = REPO / '.github' / 'workflows' / 'validate.yml'
        gen_wf = REPO / '.github' / 'workflows' / 'validate_generated_currentness.yml'
        if validate_wf.exists() and 'package_meta/tools/run_repository_validation_suite.py' not in validate_wf.read_text(encoding='utf-8'):
            issues.append('validate.yml does not call repository validation suite wrapper')
        if gen_wf.exists():
            gen_text = gen_wf.read_text(encoding='utf-8')
            if 'package_meta/tools/check_generated_currentness.py' not in gen_text:
                issues.append('validate_generated_currentness.yml missing generated currentness checker')
            if 'validate_repo_hygiene.py' in gen_text or 'check_repository_cross_references.py' in gen_text:
                issues.append('validate_generated_currentness.yml duplicates broader validation workflow')

    authority_status_by_path = {rel: status_for_current_file(rel) for rel in files}
    authority_expected_counts = dict(sorted(Counter(authority_status_by_path.values()).items()))
    authority_expected_records = {
        status: sorted(path for path, st in authority_status_by_path.items() if st == status)
        for status in load_json('package_meta/generated/authority.index.json').get('authorityOrder', [])
        if any(st == status for st in authority_status_by_path.values())
    }
    authority_index = load_json('package_meta/generated/authority.index.json')
    if authority_index.get('counts') != authority_expected_counts:
        issues.append('generated authority.index.json counts do not match current file tree')
    if authority_index.get('recordsByStatus') != authority_expected_records:
        issues.append('generated authority.index.json recordsByStatus does not match current file tree')
    materials_index = load_json('package_meta/generated/materials.index.json')
    material_status = load_json('MATERIAL_STATUS.json')
    material_status_counts = dict(sorted(Counter(r['status'] for r in material_status.get('records', [])).items()))
    if materials_index.get('fileCount') != len(files):
        issues.append(f'generated materials.index.json fileCount mismatch: index={materials_index.get("fileCount")} actual={len(files)}')
    if materials_index.get('statusCounts') != material_status_counts:
        issues.append('generated materials.index.json statusCounts do not match MATERIAL_STATUS.json')
    def _strip_generated_metadata(obj):
        if isinstance(obj, dict):
            return {k: _strip_generated_metadata(v) for k, v in obj.items() if k not in {'generatedAt','derivedFrom','doNotCiteAsIndependentSource','derivedIndexPolicy'}}
        if isinstance(obj, list):
            return [_strip_generated_metadata(v) for v in obj]
        return obj
    if _strip_generated_metadata(load_json('package_meta/generated/contracts.index.json')) != _strip_generated_metadata(load_json('03_machine_contracts/CONTRACT_INDEX.json')):
        issues.append('generated contracts.index.json does not match 03_machine_contracts/CONTRACT_INDEX.json ignoring derived metadata')
    generated_schema_example_map = load_json('package_meta/generated/schema_example_map.json')
    if generated_schema_example_map.get('records') != load_json('03_machine_contracts/EXAMPLE_SCHEMA_MAP.json').get('records'):
        issues.append('generated schema_example_map.json records do not match EXAMPLE_SCHEMA_MAP.json')
    if generated_schema_example_map.get('phase8Validation', {}).get('allMappedExamplesValidate') is not True:
        issues.append('generated schema_example_map.json does not record all mapped examples as validating')
    if load_json('package_meta/generated/source_inputs.lock.json') != load_json('SOURCE_INPUT_INDEX.json'):
        issues.append('generated source_inputs.lock.json does not match SOURCE_INPUT_INDEX.json')
    trace_src = load_json('TRACEABILITY_INDEX.json')
    trace_gen = load_json('package_meta/generated/traceability.index.json')
    if _strip_generated_metadata(trace_gen) != _strip_generated_metadata(trace_src):
        issues.append('generated traceability.index.json does not match TRACEABILITY_INDEX.json ignoring generated/derived metadata')

    # Generated index path sets.
    gen_required = [
        'package_meta/generated/authority.index.json','package_meta/generated/materials.index.json',
        'package_meta/generated/contracts.index.json','package_meta/generated/schema_example_map.json',
        'package_meta/generated/source_inputs.lock.json','package_meta/generated/traceability.index.json',
        'package_meta/generated/handover_gate.json'
    ]
    for rel in gen_required:
        if rel not in file_set: issues.append(f'missing generated index: {rel}')
    hg = load_json('package_meta/generated/handover_gate.json')
    if not hg.get('gate_pass'): issues.append('handover gate does not pass')
    if hg.get('blocking_failures'): issues.append(f'handover gate has blockers: {hg.get("blocking_failures")}')
    if hg.get('packageMetaCurrentnessValidation', {}).get('status') != 'PASS':
        issues.append('handover gate does not record package metadata currentness validation as PASS')
    if 'package_meta/tools/check_generated_currentness.py' != hg.get('generatedCurrentnessChecker'):
        issues.append('handover gate does not point to generated currentness checker')
    if hg.get('repositoryCrossReferenceScan', {}).get('status') != 'PASS':
        issues.append('handover gate does not record repository cross-reference scan as PASS')
    if 'package_meta/tools/check_repository_cross_references.py' != hg.get('repositoryCrossReferenceChecker'):
        issues.append('handover gate does not point to repository cross-reference checker')


    final_validation_rel = 'package_meta/final_validation_2026_05_19/OFARM_phase15_final_validation_report_v0_1.json'
    if final_validation_rel in file_set:
        final_validation = load_json(final_validation_rel)
        if final_validation.get('status') != 'PASS':
            issues.append('final validation report status is not PASS')
        if final_validation.get('activeLaw') is not False or final_validation.get('doesNotOverrideActiveBaseline') is not True:
            issues.append('final validation report does not preserve package-metadata-only authority flags')
        if final_validation.get('latestControlledPromotion') not in {'AAI-CP10','CP12','CP13','CP14','CP15'}:
            issues.append('final validation report does not identify acceptable historical/current controlled promotion')
    debt_rel = 'package_meta/final_validation_2026_05_19/OFARM_unresolved_debt_register_v0_1.json'
    if debt_rel in file_set:
        debt_register = load_json(debt_rel)
        if debt_register.get('activeLaw') is not False or debt_register.get('doesNotOverrideActiveBaseline') is not True:
            issues.append('unresolved debt register does not preserve package-metadata-only authority flags')
        if not debt_register.get('records'):
            issues.append('unresolved debt register has no records')
    if str(len(files)) not in hg.get('repositoryHygieneStdout', ''):
        issues.append('handover gate repositoryHygieneStdout does not include current file count')

    path_pattern = re.compile(r'`([^`]+\.(?:md|json|csv|py|txt))`')
    high_value = ['README.md','CURRENT_ACTIVE_ENTRYPOINT.md','AGENTS.md','DEVELOPMENT_HANDOVER.md','REVIEW_HOLDING_INDEX.md','03_machine_contracts/README.md','04_implementation_and_conformance/README.md','05_project_handoff_and_prompts/README.md','06_active_supporting_research/README.md','legacy_reference/README.md','legacy_reference/README_READ_ONLY.md','legacy_reference/LEGACY_REFERENCE_INDEX.md','package_meta/README.md','package_meta/PACKAGE_META_INDEX.md','package_meta/generated/README.md','package_meta/tools/README.md','package_meta/REPOSITORY_STEWARD_CHECKLIST.md']
    for rel in high_value:
        text = (REPO/rel).read_text(encoding='utf-8')
        base = (REPO/rel).parent
        for m in path_pattern.finditer(text):
            target = m.group(1)
            if target.startswith('http') or target.startswith('ofarm.') or ' ' in target: continue
            candidates = []
            if rel.count('/') > 0: candidates.append((base / target).resolve())
            candidates.append((REPO / target).resolve())
            if not any(c.exists() for c in candidates) and not target.endswith('/'):
                issues.append(f'linked path in {rel} not found: {target}')

    if issues:
        print('Repository hygiene check: FAIL')
        for issue in issues:
            print(f'- {issue}')
        return 1
    print('Repository hygiene check: OK')
    print(f'Checked {len(files)} files in {REPO.name}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
