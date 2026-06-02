#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import urllib.parse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REPORT_JSON = REPO / 'REPOSITORY_CROSS_REFERENCE_SCAN.json'
REPORT_MD = REPO / 'REPOSITORY_CROSS_REFERENCE_SCAN.md'
PACKAGE = 'OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized'
NOW = '2026-05-30T23:05:00+02:00'

MD_LINK_RE = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
ANGLE_LINK_RE = re.compile(r'<([^>\s]+\.(?:md|json|py|csv|txt|ttl|rdf|xml|yaml|yml)(?:#[^>\s]+)?)>')
STALE_PACKAGE_RE = re.compile(r'OFARM2_2026-05-(14|15|16)[A-Za-z0-9_\-.]*')
NEXT_PHASE_RE = re.compile(r'\b(next\s+(?:controlled\s+)?phase\s+(?:is|=)|next\s+queued\s+phase)\s*:?\s*\*{0,2}(AAI-)?CP[0-9]', re.I)
CURRENTNESS_WORD_RE = re.compile(r'\b(current|latest|active|endpoint|package|now|governs|authoritative|final)\b', re.I)
HISTORICAL_WORD_RE = re.compile(r'\b(historical|superseded|legacy|review-held|source-context|contextual|archived|prior|older|previous|non-active|not current|not active|lineage|remap|snapshot|package-control)\b', re.I)
TEXT_EXTS = {'.md', '.txt', '.json', '.jsonl', '.py', '.yml', '.yaml', '.csv'}

REPORT_SELF = {'REPOSITORY_CROSS_REFERENCE_SCAN.json', 'REPOSITORY_CROSS_REFERENCE_SCAN.md'}
IGNORED_FILE_TREE_DIRS = {'.git'}


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def text_read(path: Path) -> str | None:
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding='latin-1')
        except Exception:
            return None
    except Exception:
        return None


def clean_target(raw: str) -> str:
    t = raw.strip()
    if t.startswith('<') and '>' in t:
        t = t[1:t.index('>')]
    else:
        m = re.match(r"([^\s]+)\s+(['\"]).*", t)
        if m:
            t = m.group(1)
    return urllib.parse.unquote(t.strip())


def ignore_target(target: str) -> bool:
    low = target.lower()
    if not target or target.startswith('#'):
        return True
    if low.startswith(('http://', 'https://', 'mailto:', 'tel:', 'urn:', 'doi:', 'data:')):
        return True
    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) and not re.match(r'^[A-Za-z]:[\\/]', target):
        return True
    return False


def resolve(src: Path, target: str) -> bool:
    if ignore_target(target):
        return True
    path_part = target.split('#', 1)[0]
    if not path_part:
        return True
    if any(ch in path_part for ch in '*?['):
        return bool(list(src.parent.glob(path_part)) or list(REPO.glob(path_part)))
    candidates = []
    if path_part.startswith('/'):
        candidates.append(REPO / path_part.lstrip('/'))
    else:
        candidates.append(src.parent / path_part)
        candidates.append(REPO / path_part)
    return any(c.exists() for c in candidates)


def in_review_or_context(path: str) -> bool:
    return path.startswith('reviewed_') or path.startswith('archive/review_holding/') or '/source_context/' in path


def in_legacy(path: str) -> bool:
    return path.startswith('legacy_reference/')


def in_historical_package_meta(path: str) -> bool:
    return path.startswith((
        'package_meta/consolidation_',
        'package_meta/preimplementation_final_consolidation_',
        'package_meta/agentic_ai_world_model_consolidation_',
        'package_meta/repository_cleanup_',
        'package_meta/repository_handover_publication_layer_',
        'package_meta/repository_stewardship_currentness_patch_',
        'package_meta/history/',
        'package_meta/ontology_semint_',
    ))


def intentionally_historical_stale_reference(path: str, line: str) -> bool:
    if path in REPORT_SELF:
        return True
    if in_review_or_context(path) or in_legacy(path) or in_historical_package_meta(path):
        return True
    if path == '03_machine_contracts/PATH_REMAPS.json':
        return True
    if '/controlled_promotion/' in path and ('file_manifest' in path.lower() or 'validation_report' in path.lower()):
        return True
    return bool(HISTORICAL_WORD_RE.search(line))


def material_status_for(path: str) -> str:
    if path.startswith('00_active_baseline/'):
        return 'ACTIVE_BASELINE'
    if path.startswith('01_companion_artifacts/'):
        return 'COMPANION_ARTIFACT'
    if path.startswith('02_accepted_rfcs/'):
        return 'ACCEPTED_RFC'
    if path.startswith('03_machine_contracts/'):
        return 'MACHINE_CONTRACT'
    if path.startswith('04_implementation_and_conformance/'):
        return 'IMPLEMENTATION_CONFORMANCE'
    if path.startswith('05_project_handoff_and_prompts/'):
        return 'HANDOFF_PROMPT'
    if path.startswith('06_active_supporting_research/'):
        return 'ACTIVE_SUPPORTING_RESEARCH'
    if path.startswith('07_linked_domain_architectures/'):
        return 'LINKED_DOMAIN_ARCHITECTURE'
    if path.startswith('legacy_reference/'):
        return 'LEGACY_REFERENCE'
    if path.startswith('package_meta/'):
        return 'PACKAGE_METADATA'
    if path.startswith('reviewed_'):
        return 'REVIEW_HOLDING'
    return 'ROOT_PACKAGE_METADATA'


def load_json(rel_path: str):
    return json.loads((REPO / rel_path).read_text(encoding='utf-8'))


def scan() -> dict:
    files = []
    for p in REPO.rglob('*'):
        if not p.is_file():
            continue
        relative = p.relative_to(REPO)
        if any(part in IGNORED_FILE_TREE_DIRS for part in relative.parts):
            continue
        files.append(p)
    files = sorted(files)
    rels = [rel(p) for p in files]
    file_set = set(rels)

    json_parse_errors = []
    for p in files:
        if p.suffix.lower() == '.json':
            try:
                json.loads(p.read_text(encoding='utf-8'))
            except Exception as exc:
                json_parse_errors.append({'path': rel(p), 'error': str(exc)})

    markdown_total = 0
    markdown_checked = 0
    broken_links = []
    for p in files:
        if p.suffix.lower() not in {'.md', '.txt'}:
            continue
        txt = text_read(p)
        if txt is None:
            continue
        source = rel(p)
        for lineno, line in enumerate(txt.splitlines(), 1):
            for match in list(MD_LINK_RE.finditer(line)) + list(ANGLE_LINK_RE.finditer(line)):
                target = clean_target(match.group(1))
                markdown_total += 1
                if ignore_target(target) or target.startswith('#'):
                    continue
                markdown_checked += 1
                if not resolve(p, target):
                    broken_links.append({
                        'path': source,
                        'line': lineno,
                        'target': target,
                        'actionability': 'non_actionable_review_or_legacy_snapshot' if (in_review_or_context(source) or in_legacy(source)) else 'actionable_current_repository_link',
                    })

    stale_refs = []
    actionable_stale = []
    next_phase = []
    for p in files:
        if p.name in REPORT_SELF or p.suffix.lower() not in TEXT_EXTS:
            continue
        txt = text_read(p)
        if txt is None:
            continue
        source = rel(p)
        for lineno, line in enumerate(txt.splitlines(), 1):
            for match in STALE_PACKAGE_RE.finditer(line):
                record = {'path': source, 'line': lineno, 'match': match.group(0), 'text': line.strip()[:240]}
                stale_refs.append(record)
                if CURRENTNESS_WORD_RE.search(line) and not intentionally_historical_stale_reference(source, line):
                    actionable_stale.append(record)
            if NEXT_PHASE_RE.search(line) and not intentionally_historical_stale_reference(source, line):
                next_phase.append({'path': source, 'line': lineno, 'text': line.strip()[:240]})

    hashes_by_path = {}
    if (REPO / 'MANIFEST.csv').exists():
        with (REPO / 'MANIFEST.csv').open(newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                hashes_by_path[row['path']] = row.get('sha256') or sha256(REPO / row['path'])
    for p in files:
        rp = rel(p)
        hashes_by_path.setdefault(rp, sha256(p))

    by_basename = defaultdict(list)
    by_hash = defaultdict(list)
    for rp in rels:
        by_basename[Path(rp).name].append(rp)
        by_hash[hashes_by_path[rp]].append(rp)

    duplicate_basename_groups = {k: v for k, v in by_basename.items() if len(v) > 1}
    duplicate_hash_groups = {k: v for k, v in by_hash.items() if len(v) > 1}

    active_schema_names = {p.name for p in (REPO / '03_machine_contracts' / 'schemas').rglob('*.json')}
    same_basename_schema_copies = sorted(
        rp for rp in rels
        if rp.endswith('.json')
        and Path(rp).name in active_schema_names
        and not rp.startswith('03_machine_contracts/schemas/')
    )
    implementation_copies = [p for p in same_basename_schema_copies if p.startswith('04_implementation_and_conformance/')]
    review_copies = [p for p in same_basename_schema_copies if p.startswith('reviewed_')]
    legacy_copies = [p for p in same_basename_schema_copies if p.startswith('legacy_reference/')]
    other_copies = [p for p in same_basename_schema_copies if p not in set(implementation_copies + review_copies + legacy_copies)]

    indexed_impl = set()
    if (REPO / '04_implementation_and_conformance/NON_ACTIVE_SCHEMA_COPY_INDEX.json').exists():
        indexed_impl = {r.get('path') for r in load_json('04_implementation_and_conformance/NON_ACTIVE_SCHEMA_COPY_INDEX.json').get('records', [])}
    indexed_review = set()
    if (REPO / 'REVIEW_HOLDING_INDEX.json').exists():
        indexed_review = {r.get('path') for r in load_json('REVIEW_HOLDING_INDEX.json').get('sameBasenameActiveSchemaCopies', [])}
    indexed_legacy = set()
    if (REPO / 'legacy_reference/LEGACY_REFERENCE_INDEX.json').exists():
        indexed_legacy = {r.get('legacyPath') for r in load_json('legacy_reference/LEGACY_REFERENCE_INDEX.json').get('activeSchemaBasenameCopies', [])}

    index_coverage_issues = []
    if set(implementation_copies) != indexed_impl:
        index_coverage_issues.append({
            'index': '04_implementation_and_conformance/NON_ACTIVE_SCHEMA_COPY_INDEX.json',
            'missing': sorted(set(implementation_copies) - indexed_impl)[:20],
            'extra': sorted(indexed_impl - set(implementation_copies))[:20],
        })
    if set(review_copies) != indexed_review:
        index_coverage_issues.append({
            'index': 'REVIEW_HOLDING_INDEX.json',
            'missing': sorted(set(review_copies) - indexed_review)[:20],
            'extra': sorted(indexed_review - set(review_copies))[:20],
        })
    if set(legacy_copies) != indexed_legacy:
        index_coverage_issues.append({
            'index': 'legacy_reference/LEGACY_REFERENCE_INDEX.json',
            'missing': sorted(set(legacy_copies) - indexed_legacy)[:20],
            'extra': sorted(indexed_legacy - set(legacy_copies))[:20],
        })

    manifest_errors = []
    if (REPO / 'MANIFEST.csv').exists():
        with (REPO / 'MANIFEST.csv').open(newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        manifest_paths = {row['path'] for row in rows}
        expected = file_set - {'MANIFEST.csv'}
        if manifest_paths != expected:
            manifest_errors.append({
                'kind': 'path_set_mismatch',
                'missing_count': len(expected - manifest_paths),
                'extra_count': len(manifest_paths - expected),
                'missing': sorted(expected - manifest_paths)[:20],
                'extra': sorted(manifest_paths - expected)[:20],
            })

    actionable_broken = [b for b in broken_links if b['actionability'] == 'actionable_current_repository_link']
    status = 'PASS' if not any([json_parse_errors, actionable_broken, actionable_stale, next_phase, index_coverage_issues, manifest_errors, other_copies]) else 'FAIL'

    return {
        'schemaVersion': 'ofarm.repositoryCrossReferenceScan.v0.1',
        'generatedAt': NOW,
        'package': PACKAGE,
        'latestControlledPromotion': 'CP15',
        'activeLaw': False,
        'doesNotOverrideActiveBaseline': True,
        'scope': 'Full repository link, stale-reference, duplicate-basename, schema-copy, and cross-index scan. This scan supports repository stewardship only and does not create active OFARM law.',
        'status': status,
        'summary': {
            'fileCount': len(files),
            'jsonParseErrors': len(json_parse_errors),
            'markdownTargetsTotal': markdown_total,
            'markdownTargetsChecked': markdown_checked,
            'brokenMarkdownLinksTotal': len(broken_links),
            'actionableBrokenMarkdownLinks': len(actionable_broken),
            'nonActionableReviewOrLegacySnapshotBrokenMarkdownLinks': len(broken_links) - len(actionable_broken),
            'stalePackageReferencesTotal': len(stale_refs),
            'actionableStaleCurrentnessReferences': len(actionable_stale),
            'nextPhasePhraseCandidates': len(next_phase),
            'duplicateBasenameGroups': len(duplicate_basename_groups),
            'duplicateContentHashGroups': len(duplicate_hash_groups),
            'activeSchemaSameBasenameCopiesOutsideActiveSchemas': len(same_basename_schema_copies),
            'implementationSchemaCopiesIndexed': len(implementation_copies),
            'reviewHoldingSchemaCopiesIndexed': len(review_copies),
            'legacySchemaCopiesIndexed': len(legacy_copies),
            'otherSchemaCopies': len(other_copies),
            'schemaCopyIndexCoverageIssues': len(index_coverage_issues),
            'manifestErrorGroups': len(manifest_errors),
        },
        'actionableFindings': {
            'brokenMarkdownLinks': actionable_broken[:200],
            'staleCurrentnessReferences': actionable_stale[:200],
            'nextPhasePhraseCandidates': next_phase[:200],
            'schemaCopyIndexCoverageIssues': index_coverage_issues,
            'otherActiveSchemaBasenameCopies': other_copies[:200],
            'manifestErrors': manifest_errors,
            'jsonParseErrors': json_parse_errors[:200],
        },
        'nonActionableSnapshotFindings': {
            'brokenMarkdownLinksPreservedInReviewOrLegacySnapshots': len(broken_links) - len(actionable_broken),
            'note': 'Broken links in review-held/source-context and legacy snapshots are recorded as snapshot defects but are not patched so copied historical material remains intact.',
            'sample': [b for b in broken_links if b['actionability'] != 'actionable_current_repository_link'][:25],
        },
        'duplicateSummary': {
            'duplicateBasenameGroups': len(duplicate_basename_groups),
            'duplicateContentHashGroups': len(duplicate_hash_groups),
            'topDuplicateBasenames': [
                {'basename': name, 'count': len(paths), 'samplePaths': paths[:8]}
                for name, paths in sorted(duplicate_basename_groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:25]
            ],
            'schemaCopyCoverage': {
                'implementationConformanceCopies': len(implementation_copies),
                'implementationConformanceIndex': '04_implementation_and_conformance/NON_ACTIVE_SCHEMA_COPY_INDEX.json',
                'reviewHoldingCopies': len(review_copies),
                'reviewHoldingIndex': 'REVIEW_HOLDING_INDEX.json',
                'legacyReferenceCopies': len(legacy_copies),
                'legacyReferenceIndex': 'legacy_reference/LEGACY_REFERENCE_INDEX.json',
                'unindexedOtherCopies': other_copies[:50],
            },
        },
        'staleReferenceSummary': {
            'byTopLevel': dict(sorted(Counter((r['path'].split('/', 1)[0] if '/' in r['path'] else '.') for r in stale_refs).items())),
            'actionableCurrentnessReferences': actionable_stale[:50],
            'interpretation': 'Older package names remain valid inside historical package-control records, controlled-promotion phase manifests, path-remap lineage, review-held snapshots, and legacy contextual reference. Actionable stale currentness references must be zero.',
        },
        'checks': {
            'jsonParses': len(json_parse_errors) == 0,
            'noActionableBrokenMarkdownLinks': len(actionable_broken) == 0,
            'noActionableStaleCurrentnessReferences': len(actionable_stale) == 0,
            'noActionableNextPhasePhrases': len(next_phase) == 0,
            'schemaCopyIndexesCoverKnownCopies': len(index_coverage_issues) == 0,
            'noUnexpectedActiveSchemaBasenameCopies': len(other_copies) == 0,
            'manifestPathSetCurrent': len(manifest_errors) == 0,
        },
    }


def write_report(report: dict) -> None:
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=False) + '\n', encoding='utf-8')
    s = report['summary']
    lines = [
        '# Repository cross-reference scan',
        '',
        f"Package: `{report['package']}`",
        '',
        f"Status: **{report['status']}**",
        '',
        'This scan supports repository stewardship only. It does not create active OFARM law and does not override the active baseline, accepted RFCs, companion artifacts, or machine contracts.',
        '',
        '## Summary',
        '',
        f"- Files scanned: {s['fileCount']}",
        f"- JSON parse errors: {s['jsonParseErrors']}",
        f"- Markdown targets checked: {s['markdownTargetsChecked']}",
        f"- Actionable broken markdown links: {s['actionableBrokenMarkdownLinks']}",
        f"- Broken links preserved in review/legacy snapshots: {s['nonActionableReviewOrLegacySnapshotBrokenMarkdownLinks']}",
        f"- Actionable stale currentness references: {s['actionableStaleCurrentnessReferences']}",
        f"- Next-phase phrase candidates: {s['nextPhasePhraseCandidates']}",
        f"- Duplicate basename groups: {s['duplicateBasenameGroups']}",
        f"- Duplicate content-hash groups: {s['duplicateContentHashGroups']}",
        f"- Active-schema same-basename copies outside active schema folders: {s['activeSchemaSameBasenameCopiesOutsideActiveSchemas']}",
        f"- Schema-copy index coverage issues: {s['schemaCopyIndexCoverageIssues']}",
        f"- Manifest error groups: {s['manifestErrorGroups']}",
        '',
        '## Interpretation',
        '',
        '- Broken markdown links inside reviewed/source-context and legacy snapshots are recorded, but not patched, to preserve copied historical material.',
        '- Same-basename schema copies outside `03_machine_contracts/schemas/` are acceptable only when they are indexed as non-active implementation, review-holding, or legacy copies.',
        '- Older package names are acceptable in historical package-control records, controlled-promotion phase manifests, path-remap lineage, review-held snapshots, and legacy context.',
        '',
        '## Actionable finding status',
        '',
    ]
    for key, value in report['checks'].items():
        lines.append(f"- {key}: {'PASS' if value else 'FAIL'}")
    lines.append('')
    REPORT_MD.write_text('\n'.join(lines), encoding='utf-8')


def normalized(obj):
    if isinstance(obj, dict):
        return {k: normalized(v) for k, v in obj.items() if k != 'generatedAt'}
    if isinstance(obj, list):
        return [normalized(v) for v in obj]
    return obj


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true', help='write REPOSITORY_CROSS_REFERENCE_SCAN.json and .md')
    args = parser.parse_args()
    report = scan()
    if args.write:
        write_report(report)
        print(f"Repository cross-reference scan written: {report['status']}")
        return 0 if report['status'] == 'PASS' else 1
    issues = []
    if not REPORT_JSON.exists() or not REPORT_MD.exists():
        issues.append('missing REPOSITORY_CROSS_REFERENCE_SCAN.json or .md')
    else:
        existing = json.loads(REPORT_JSON.read_text(encoding='utf-8'))
        if normalized(existing) != normalized(report):
            issues.append('REPOSITORY_CROSS_REFERENCE_SCAN.json is not current with repository scan')
        if existing.get('status') != 'PASS':
            issues.append('REPOSITORY_CROSS_REFERENCE_SCAN.json status is not PASS')
    if report['status'] != 'PASS':
        issues.append('fresh repository cross-reference scan has actionable findings')
    if issues:
        print('Repository cross-reference check: FAIL')
        for issue in issues:
            print(f'- {issue}')
        return 1
    print('Repository cross-reference check: OK')
    print(f"Checked cross-references in {REPO.name}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
