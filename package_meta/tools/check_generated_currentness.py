#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DERIVED_KEYS = {'derivedFrom','doNotCiteAsIndependentSource','derivedIndexPolicy'}
IGNORED_FILE_TREE_DIRS = {'.git'}

def load_json(rel: str):
    return json.loads((REPO / rel).read_text(encoding='utf-8'))

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

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

def strip_generated_and_derived(obj):
    if isinstance(obj, dict):
        return {k: strip_generated_and_derived(v) for k, v in obj.items() if k not in DERIVED_KEYS and k != 'generatedAt'}
    if isinstance(obj, list):
        return [strip_generated_and_derived(v) for v in obj]
    return obj

def status_for(rel: str) -> str:
    name = Path(rel).name
    if name in {'README.md','folder.status.json'} or name.endswith('.status.json'):
        if '/' in rel:
            return 'PACKAGE_METADATA'
    if rel.startswith('00_active_baseline/'): return 'ACTIVE_BASELINE'
    if rel.startswith('01_companion_artifacts/'): return 'COMPANION_ARTIFACT'
    if rel.startswith('02_accepted_rfcs/'): return 'ACCEPTED_RFC'
    if rel.startswith('03_machine_contracts/'): return 'MACHINE_CONTRACT'
    if rel.startswith('04_implementation_and_conformance/'): return 'IMPLEMENTATION_CONFORMANCE'
    if rel.startswith('05_project_handoff_and_prompts/'): return 'HANDOFF_PROMPT'
    if rel.startswith('06_active_supporting_research/'): return 'ACTIVE_SUPPORTING_RESEARCH'
    if rel.startswith('07_linked_domain_architectures/'): return 'LINKED_DOMAIN_ARCHITECTURE'
    if rel.startswith('legacy_reference/'): return 'LEGACY_REFERENCE'
    if rel.startswith('archive/review_holding/'):
        return 'REVIEW_HOLDING' if name.endswith('.zip') else 'PACKAGE_METADATA'
    if rel.startswith('package_meta/'): return 'PACKAGE_METADATA'
    return 'ROOT_PACKAGE_METADATA'

def main() -> int:
    issues: list[str] = []
    files = set(rel_files())
    authority_status_by_path = {rel: status_for(rel) for rel in sorted(files)}
    status_counts = dict(sorted(Counter(authority_status_by_path.values()).items()))
    authority = load_json('package_meta/generated/authority.index.json')
    authority_order = authority.get('authorityOrder', [])
    records_by_status = {status: sorted(path for path, st in authority_status_by_path.items() if st == status) for status in authority_order if any(st == status for st in authority_status_by_path.values())}
    if authority.get('counts') != status_counts:
        issues.append('authority.index.json counts do not match current file tree')
    if authority.get('recordsByStatus') != records_by_status:
        issues.append('authority.index.json recordsByStatus does not match current file tree')
    materials = load_json('package_meta/generated/materials.index.json')
    material_status = load_json('MATERIAL_STATUS.json')
    ms_counts = dict(sorted(Counter(r['status'] for r in material_status.get('records', [])).items()))
    if materials.get('fileCount') != len(files):
        issues.append(f'materials.index.json fileCount mismatch: index={materials.get("fileCount")} actual={len(files)}')
    if materials.get('statusCounts') != ms_counts:
        issues.append('materials.index.json statusCounts do not match MATERIAL_STATUS.json')
    checks = [
        ('03_machine_contracts/CONTRACT_INDEX.json','package_meta/generated/contracts.index.json'),
        ('SOURCE_INPUT_INDEX.json','package_meta/generated/source_inputs.lock.json'),
        ('TRACEABILITY_INDEX.json','package_meta/generated/traceability.index.json'),
    ]
    for src_rel, gen_rel in checks:
        src = strip_generated_and_derived(load_json(src_rel))
        gen = strip_generated_and_derived(load_json(gen_rel))
        if gen != src:
            issues.append(f'generated {gen_rel} does not match {src_rel} ignoring generated/derived metadata')
    example_src = load_json('03_machine_contracts/EXAMPLE_SCHEMA_MAP.json')
    example_gen = load_json('package_meta/generated/schema_example_map.json')
    if example_gen.get('records') != example_src.get('records'):
        issues.append('generated schema_example_map.json records do not match EXAMPLE_SCHEMA_MAP.json')
    if example_gen.get('phase8Validation', {}).get('allMappedExamplesValidate') is not True:
        issues.append('generated schema_example_map.json does not record all mapped examples as validating')
    for gen_rel, source in [
        ('package_meta/generated/contracts.index.json','03_machine_contracts/CONTRACT_INDEX.json'),
        ('package_meta/generated/schema_example_map.json','03_machine_contracts/EXAMPLE_SCHEMA_MAP.json'),
        ('package_meta/generated/traceability.index.json','TRACEABILITY_INDEX.json'),
    ]:
        gen = load_json(gen_rel)
        if gen.get('derivedFrom') != source or gen.get('doNotCiteAsIndependentSource') is not True:
            issues.append(f'{gen_rel} missing derived source marker')
    pmi = load_json('package_meta/PACKAGE_META_INDEX.json')
    package_meta_root = REPO / 'package_meta'
    expected_package_meta = {p.relative_to(REPO).as_posix() for p in package_meta_root.rglob('*') if p.is_file() and p.relative_to(REPO).as_posix() not in {'package_meta/PACKAGE_META_INDEX.json','package_meta/PACKAGE_META_INDEX.md'}}
    indexed_package_meta = {r.get('path') for r in pmi.get('records', [])}
    if indexed_package_meta != expected_package_meta:
        issues.append(f'PACKAGE_META_INDEX.json path set mismatch: missing={sorted(expected_package_meta-indexed_package_meta)[:10]} extra={sorted(indexed_package_meta-expected_package_meta)[:10]}')
    # Hash validation for generated support indexes that contain records.
    for label, index_rel in [('package meta index','package_meta/PACKAGE_META_INDEX.json')]:
        idx = load_json(index_rel)
        for r in idx.get('records', []):
            path = r.get('path')
            if path and (REPO/path).exists() and r.get('sha256') and r['sha256'] != sha256(REPO/path):
                issues.append(f'{label} sha256 mismatch: {path}')
    if issues:
        print('Generated currentness check: FAIL')
        for issue in issues: print(f'- {issue}')
        return 1
    print('Generated currentness check: OK')
    print(f'Checked generated indexes and package metadata in {REPO.name}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
