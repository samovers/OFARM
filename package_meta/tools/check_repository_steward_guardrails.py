#!/usr/bin/env python3
from __future__ import annotations
import json, sys, re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SNAKE_LEGACY_KEYS = {'material_status','active_law','search_default','does_not_override_active_baseline','folder_class','authority_rank','citation_allowed','release_export','current_package','latest_controlled_promotion'}
EXPECTED_FOLDER_STATUS_SCHEMA = 'package_meta/repository_steward_completion_batch2_2026_05_20/FOLDER_STATUS_CANONICAL_SCHEMA_v1_1.json'

def load_json(rel: str):
    return json.loads((REPO / rel).read_text(encoding='utf-8'))

def main() -> int:
    issues: list[str] = []
    canonical_keys = {'folderStatusVersion','canonicalizedAt','path','materialStatus','folderClass','authorityRank','activeLaw','metadataArtifactActiveLaw','doesNotOverrideActiveBaseline','citationAllowed','searchDefault','releaseExport','currentPackage','latestControlledPromotion','artifactRole','activeLawSubject','folderStatusSchema','canonicalFolderStatusFieldsPresent','notes'}
    for p in REPO.rglob('folder.status.json'):
        data = json.loads(p.read_text(encoding='utf-8'))
        missing = canonical_keys - set(data)
        if missing:
            issues.append(f'folder.status missing canonical keys {sorted(missing)}: {p.relative_to(REPO).as_posix()}')
        legacy = SNAKE_LEGACY_KEYS & set(data)
        if legacy:
            issues.append(f'folder.status still has legacy snake_case keys {sorted(legacy)}: {p.relative_to(REPO).as_posix()}')
        if data.get('metadataArtifactActiveLaw') is not False:
            issues.append(f'folder.status must be metadataArtifactActiveLaw=false: {p.relative_to(REPO).as_posix()}')
        schema_rel = data.get('folderStatusSchema')
        if schema_rel != EXPECTED_FOLDER_STATUS_SCHEMA:
            issues.append(f'folder.status has non-current folderStatusSchema {schema_rel!r}: {p.relative_to(REPO).as_posix()}')
        elif not (REPO / schema_rel).exists():
            issues.append(f'folder.status references missing folderStatusSchema {schema_rel}: {p.relative_to(REPO).as_posix()}')
        else:
            try:
                json.loads((REPO / schema_rel).read_text(encoding='utf-8'))
            except Exception as exc:
                issues.append(f'folderStatusSchema is not parseable JSON {schema_rel}: {exc}')
    material = load_json('MATERIAL_STATUS.json')
    for row in material.get('records', []):
        name = Path(row.get('path','')).name
        if name in {'README.md','folder.status.json'} and row.get('path') != 'README.md' and (row.get('activeLaw') is not False or row.get('status') != 'PACKAGE_METADATA'):
            issues.append(f'navigation metadata must be activeLaw=false and PACKAGE_METADATA: {row.get("path")}')
    # Physical review-holding archive: no root reviewed_* dirs.
    if list(REPO.glob('reviewed_*')):
        issues.append('root reviewed_* folders remain default-visible; expected archive/review_holding zip only')
    rhi = load_json('REVIEW_HOLDING_INDEX.json')
    archive = REPO / rhi.get('archivePath','')
    if not archive.exists() or not archive.name.endswith('.zip'):
        issues.append('REVIEW_HOLDING_INDEX.json does not point to existing review-holding archive zip')
    if rhi.get('activeSchemaSameBasenameCopiesVisibleInRepository') != 0:
        issues.append('review-holding index does not record zero visible active-schema basename copies')
    # Active-schema basename copy disambiguation.
    active_schema_names = {p.name for p in (REPO/'03_machine_contracts'/'schemas').rglob('*.json')}
    visible_copies = [p.relative_to(REPO).as_posix() for p in REPO.rglob('*.json') if p.name in active_schema_names and not p.relative_to(REPO).as_posix().startswith('03_machine_contracts/schemas/')]
    if visible_copies:
        issues.append(f'visible active-schema same-basename copies remain: {visible_copies[:20]}')
    nonactive = load_json('04_implementation_and_conformance/NON_ACTIVE_SCHEMA_COPY_INDEX.json')
    if nonactive.get('activeSchemaSameBasenameCopyCount') != 0 or nonactive.get('records') != []:
        issues.append('NON_ACTIVE_SCHEMA_COPY_INDEX.json does not record zero current same-basename implementation copies')
    # 04 physical lane split.
    allowed_impl_top_files = {'README.md','IMPLEMENTATION_LANE_INDEX.json','IMPLEMENTATION_LANE_INDEX.md','IMPLEMENTATION_SUBFOLDER_INDEX.json','IMPLEMENTATION_SUBFOLDER_INDEX.md','NON_ACTIVE_SCHEMA_COPY_INDEX.json','NON_ACTIVE_SCHEMA_COPY_INDEX.md','folder.status.json'}
    allowed_impl_dirs = {'examples_and_fixtures','conformance_runners','controlled_promotion_evidence','implementation_notes','service_and_sdk_candidates','pilot_material','historical_archive','spikes_incubation'}
    top_dirs = {p.name for p in (REPO/'04_implementation_and_conformance').iterdir() if p.is_dir()}
    if top_dirs != allowed_impl_dirs:
        issues.append(f'04 top-level dirs are not the controlled lane set: {sorted(top_dirs)}')
    top_files = {p.name for p in (REPO/'04_implementation_and_conformance').iterdir() if p.is_file()}
    if top_files - allowed_impl_top_files:
        issues.append(f'04 root has unapproved files: {sorted(top_files-allowed_impl_top_files)}')
    # Derived generated indexes must self-mark.
    for gen_rel, source in [('package_meta/generated/contracts.index.json','03_machine_contracts/CONTRACT_INDEX.json'),('package_meta/generated/schema_example_map.json','03_machine_contracts/EXAMPLE_SCHEMA_MAP.json'),('package_meta/generated/traceability.index.json','TRACEABILITY_INDEX.json')]:
        gen = load_json(gen_rel)
        if gen.get('derivedFrom') != source or gen.get('doNotCiteAsIndependentSource') is not True:
            issues.append(f'{gen_rel} missing explicit derivedFrom/doNotCite markers')
    # Workflow behavior must not duplicate full suite in generated-currentness workflow.
    gen_wf = (REPO/'.github/workflows/validate_generated_currentness.yml').read_text(encoding='utf-8')
    if 'validate_repo_hygiene.py' in gen_wf or 'check_repository_cross_references.py' in gen_wf or 'check_repository_steward_guardrails.py' in gen_wf:
        issues.append('validate_generated_currentness.yml still duplicates full validation workflow behavior')
    # Final validation counts must agree with live scan.
    rx = load_json('REPOSITORY_CROSS_REFERENCE_SCAN.json')
    for rel in ['package_meta/final_validation_2026_05_19/OFARM_phase15_final_validation_report_v0_1.json','package_meta/final_validation_2026_05_19/OFARM_repository_currentness_cleanup_report_v0_1.json']:
        doc = load_json(rel)
        cvs = doc.get('crossReferenceSummary') or doc.get('repositoryCrossReferenceSummary') or {}
        for key, value in cvs.items():
            if key in rx.get('summary', {}) and rx['summary'][key] != value:
                issues.append(f'{rel} cross-reference summary diverges for {key}: {value} != {rx["summary"][key]}')
    # Human generated-view currentness checks.
    # Traceability markdown statuses must match canonical TRACEABILITY_INDEX.json.
    trace_json = load_json('TRACEABILITY_INDEX.json')
    expected_trace_status = {(item.get('concept') or item.get('title') or item.get('id')): (item.get('status') or 'unspecified') for item in trace_json.get('items', [])}
    md = (REPO/'TRACEABILITY_INDEX.md').read_text(encoding='utf-8')
    seen_trace_concepts = set()
    for line in md.splitlines():
        if not line.startswith('| ') or line.startswith('| Concept ') or line.startswith('|---'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 2:
            continue
        concept = cells[0].replace('\\|','|')
        status = cells[1].strip().strip('`')
        if not status:
            issues.append(f'TRACEABILITY_INDEX.md contains blank status for concept: {concept}')
        elif concept in expected_trace_status and status != expected_trace_status[concept]:
            issues.append(f'TRACEABILITY_INDEX.md status mismatch for {concept}: {status!r} != {expected_trace_status[concept]!r}')
        seen_trace_concepts.add(concept)
    missing_trace = set(expected_trace_status) - seen_trace_concepts
    if missing_trace:
        issues.append(f'TRACEABILITY_INDEX.md missing canonical trace concepts: {sorted(missing_trace)}')

    # CURRENT_SOURCE_INPUTS.md summary counts and live-lane paths must match SOURCE_INPUT_INDEX.json.
    source_index = load_json('SOURCE_INPUT_INDEX.json')
    source_md = (REPO/'06_active_supporting_research/CURRENT_SOURCE_INPUTS.md').read_text(encoding='utf-8')
    expected_source_count = len(source_index.get('records', []))
    expected_duplicate_count = len(source_index.get('duplicateChecksumGroups', []))
    if f'Full source-input records: {expected_source_count}' not in source_md:
        issues.append('CURRENT_SOURCE_INPUTS.md full source-input record count does not match SOURCE_INPUT_INDEX.json')
    if f'Duplicate checksum groups: {expected_duplicate_count}' not in source_md:
        issues.append('CURRENT_SOURCE_INPUTS.md duplicate checksum group count does not match SOURCE_INPUT_INDEX.json')
    for row in source_index.get('records', []):
        path = row.get('path', '')
        if path.startswith('06_active_supporting_research/source_inputs/') and f'`{path}`' not in source_md:
            issues.append(f'CURRENT_SOURCE_INPUTS.md missing live source-input lane path: {path}')

    # Batch 2.1 currentness pointers must make Batch 2/2.1 current and Batch 1 historical.
    b21 = 'package_meta/repository_steward_completion_batch2_1_2026_05_20'
    current_json = load_json('CURRENT_ACTIVE_ENTRYPOINT.json')
    if 'reviewed_*' in current_json.get('readOrder', []):
        issues.append('CURRENT_ACTIVE_ENTRYPOINT.json still lists reviewed_* in current readOrder')
    if 'archive/review_holding/' not in current_json.get('readOrder', []):
        issues.append('CURRENT_ACTIVE_ENTRYPOINT.json does not list archive/review_holding/ as review-holding location')
    if current_json.get('repositoryStewardCompletionBatch21Report') != f'package_meta/repository_steward_completion_batch2_1_2026_05_20/OFARM_repository_steward_completion_batch2_1_currentness_patch_v0_1.json':
        issues.append('CURRENT_ACTIVE_ENTRYPOINT.json missing Batch 2.1 currentness report pointer')
    if current_json.get('validationSuite') != f'package_meta/repository_steward_completion_batch2_1_2026_05_20/VALIDATION_SUITE.md':
        issues.append('CURRENT_ACTIVE_ENTRYPOINT.json validationSuite does not point to Batch 2.1')
    for rel in ['README.md','CURRENT_ACTIVE_ENTRYPOINT.md','AGENTS.md','DEVELOPMENT_HANDOVER.md','llms.txt','package_meta/tools/README.md','package_meta/validators/README.md']:
        txt = (REPO/rel).read_text(encoding='utf-8')
        if b21 not in txt:
            issues.append(f'{rel} does not reference Batch 2.1 currentness control surface')
    if '- `reviewed_*/`' in (REPO/'README.md').read_text(encoding='utf-8') or '- reviewed_*/' in (REPO/'llms.txt').read_text(encoding='utf-8'):
        issues.append('root README/llms still list reviewed_* as default visible supporting context')
    b1 = load_json('package_meta/repository_steward_remediation_2026_05_20/OFARM_repository_steward_remediation_report_v0_1.json')
    if 'package_meta/repository_steward_completion_batch2_2026_05_20/OFARM_repository_steward_completion_batch2_report_v0_1.json' not in b1.get('supersededBy', []):
        issues.append('Batch 1 remediation report is not marked superseded by Batch 2')
    if 'package_meta/repository_steward_completion_batch2_1_2026_05_20/OFARM_repository_steward_completion_batch2_1_currentness_patch_v0_1.json' not in b1.get('supersededBy', []):
        issues.append('Batch 1 remediation report is not marked superseded/amended by Batch 2.1')
    debt = load_json('package_meta/final_validation_2026_05_19/OFARM_unresolved_debt_register_v0_1.json')
    for rec in debt.get('records', []):
        if rec.get('id') == 'REP-DEBT-002' and rec.get('status') != 'closed_by_repository_steward_completion_batch2':
            issues.append('REP-DEBT-002 still claims same-basename schema-copy debt remains open')

    if issues:
        print('Repository steward guardrail check: FAIL')
        for issue in issues: print(f'- {issue}')
        return 1
    print('Repository steward guardrail check: OK')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
