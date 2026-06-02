#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from collections import defaultdict
import re
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as e:
    raise SystemExit('jsonschema is required for this validator') from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / '03_machine_contracts'
OUT_DIR = Path(__file__).resolve().parent
RESULTS = OUT_DIR / 'OFARM_machine_contract_validation_results_v0_22.json'
NEGATIVE = OUT_DIR / 'OFARM_machine_contract_negative_validation_records_v0_5.json'
REFERENCE = OUT_DIR / 'OFARM_machine_contract_reference_consistency_records_v0_5.json'


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')


def infer_schema(example_name: str, schema_names: list[str]) -> str | None:
    if '_example_' not in example_name:
        return None
    prefix = example_name.split('_example_')[0]
    candidates = sorted([s for s in schema_names if s.startswith(prefix + '_schema_')])
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    m = re.search(r'_(v\d+_\d+(?:_draft)?)\.json$', example_name)
    if m:
        token = m.group(1)
        for candidate in candidates:
            if token in candidate:
                return candidate
    for candidate in candidates:
        if 'v0_2_draft' in example_name and 'v0_2_draft' in candidate:
            return candidate
    for candidate in candidates:
        if 'v0_1' in candidate:
            return candidate
    return candidates[0]


def path_join(parts: list[Any]) -> str:
    out = []
    for part in parts:
        out.append(str(part))
    return '.'.join(out)


def get_at_path(data: Any, parts: list[Any]) -> Any:
    cur = data
    for part in parts:
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    return cur


def set_at_path(data: Any, parts: list[Any], value: Any) -> None:
    cur = data
    for part in parts[:-1]:
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    last = parts[-1]
    if isinstance(cur, list):
        cur[int(last)] = value
    else:
        cur[last] = value


def del_at_path(data: Any, parts: list[Any]) -> None:
    cur = data
    for part in parts[:-1]:
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    last = parts[-1]
    if isinstance(cur, list):
        del cur[int(last)]
    else:
        del cur[last]


def extract_primary_ids(obj: Any) -> list[tuple[str, str]]:
    ids: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and (key.endswith('Id') or key in ('artifactId', 'id')):
                ids.append((key, value))
    return ids


def collect_resolvable_refs(example_name: str, obj: Any, id_index: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    def walk(node: Any, path: list[Any]) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                next_path = path + [key]
                if key.endswith('Ref') and isinstance(value, str):
                    if value in id_index:
                        records.append({
                            'sourceFile': example_name,
                            'refPath': path_join(next_path),
                            'refField': key,
                            'refValue': value,
                            'targets': id_index[value],
                        })
                elif key.endswith('Refs') and isinstance(value, list):
                    for idx, item in enumerate(value):
                        if isinstance(item, str) and item in id_index:
                            records.append({
                                'sourceFile': example_name,
                                'refPath': path_join(next_path + [idx]),
                                'refField': key,
                                'refValue': item,
                                'targets': id_index[item],
                            })
                walk(value, next_path)
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                walk(item, path + [idx])

    walk(obj, [])
    return records


def choose_negative_mutation(schema: dict[str, Any], example: dict[str, Any]) -> dict[str, Any]:
    required = schema.get('required', [])
    for field in required:
        if field in example:
            mutated = copy.deepcopy(example)
            del mutated[field]
            return {
                'mutation': 'remove_required_field',
                'field': field,
                'data': mutated,
            }

    props = schema.get('properties', {})
    for field, prop in props.items():
        if field in example and isinstance(example[field], str):
            if 'const' in prop:
                mutated = copy.deepcopy(example)
                mutated[field] = '__INVALID_CONST__'
                return {
                    'mutation': 'break_const',
                    'field': field,
                    'data': mutated,
                }
            if 'enum' in prop:
                mutated = copy.deepcopy(example)
                mutated[field] = '__INVALID_ENUM__'
                return {
                    'mutation': 'break_enum',
                    'field': field,
                    'data': mutated,
                }

    if schema.get('additionalProperties') is False:
        mutated = copy.deepcopy(example)
        mutated['wave28UnexpectedField'] = True
        return {
            'mutation': 'inject_additional_property',
            'field': 'wave28UnexpectedField',
            'data': mutated,
        }

    mutated = copy.deepcopy(example)
    mutated['wave28FallbackInvalidation'] = {'unexpected': True}
    return {
        'mutation': 'fallback_inject_property',
        'field': 'wave28FallbackInvalidation',
        'data': mutated,
    }


def main() -> int:
    schema_names = sorted(p.name for p in MC.glob('*_schema_*.json'))
    example_names = sorted(p.name for p in MC.glob('*_example_*.json'))

    schemas: dict[str, dict[str, Any]] = {}
    examples: dict[str, Any] = {}

    result: dict[str, Any] = {
        'metadata': {
            'runner': Path(__file__).name,
            'scope': 'schema validity, positive example validation, negative mutation validation, and package-local cross-file reference consistency',
            'note': 'Cross-file reference consistency is limited to refs that resolve to package-local example primary ids. Externally anchored refs are informational and not treated as failures here.',
        },
        'schemaChecks': {},
        'positiveExampleValidation': {},
        'negativeValidationSummary': {},
        'referenceConsistencySummary': {},
        'overall': 'PASS',
    }

    # Schemas
    for schema_name in schema_names:
        try:
            schema = load_json(MC / schema_name)
            jsonschema.Draft202012Validator.check_schema(schema)
            schemas[schema_name] = schema
            result['schemaChecks'][schema_name] = 'PASS'
        except Exception as exc:  # pragma: no cover - diagnostic path
            result['schemaChecks'][schema_name] = f'FAIL: {exc}'
            result['overall'] = 'FAIL'

    # Positive examples
    examples_by_schema: dict[str, list[str]] = defaultdict(list)
    for example_name in example_names:
        schema_name = infer_schema(example_name, schema_names)
        key = f'{example_name} :: {schema_name or "NO_MATCH"}'
        try:
            if schema_name is None:
                raise ValueError('could not infer matching schema')
            data = load_json(MC / example_name)
            jsonschema.validate(data, schemas[schema_name])
            result['positiveExampleValidation'][key] = 'PASS'
            examples[example_name] = data
            examples_by_schema[schema_name].append(example_name)
        except Exception as exc:
            result['positiveExampleValidation'][key] = f'FAIL: {exc}'
            result['overall'] = 'FAIL'

    # Negative validations
    negative_records: list[dict[str, Any]] = []
    for schema_name in schema_names:
        if schema_name not in examples_by_schema:
            negative_records.append({
                'schemaName': schema_name,
                'status': 'SKIP',
                'reason': 'no matching example available for mutation',
            })
            continue
        example_name = sorted(examples_by_schema[schema_name])[0]
        example = examples[example_name]
        schema = schemas[schema_name]
        mutation = choose_negative_mutation(schema, example)
        record = {
            'schemaName': schema_name,
            'exampleName': example_name,
            'mutationType': mutation['mutation'],
            'mutatedField': mutation['field'],
        }
        try:
            jsonschema.validate(mutation['data'], schema)
            record['status'] = 'UNEXPECTED_PASS'
            record['detail'] = 'mutated example still validated successfully'
            result['overall'] = 'FAIL'
        except Exception as exc:
            record['status'] = 'EXPECTED_FAIL'
            record['detail'] = str(exc).splitlines()[0]
        negative_records.append(record)

    # Cross-file reference consistency
    id_index: dict[str, list[dict[str, str]]] = defaultdict(list)
    for example_name, obj in examples.items():
        for field_name, value in extract_primary_ids(obj):
            id_index[value].append({
                'targetFile': example_name,
                'idField': field_name,
                'idValue': value,
            })

    positive_reference_records: list[dict[str, Any]] = []
    all_resolvable: list[dict[str, Any]] = []
    for example_name, obj in examples.items():
        all_resolvable.extend(collect_resolvable_refs(example_name, obj, id_index))

    for item in all_resolvable:
        status = 'UNIQUE_TARGET_PASS' if len(item['targets']) == 1 else 'VARIANT_TARGET_PASS'
        positive_reference_records.append({
            'caseId': f"ref::{item['sourceFile']}::{item['refPath']}",
            'sourceFile': item['sourceFile'],
            'refPath': item['refPath'],
            'refField': item['refField'],
            'refValue': item['refValue'],
            'targetCount': len(item['targets']),
            'targets': item['targets'],
            'status': status,
        })

    # Broken-reference negatives against a bounded sample of unique-target refs.
    broken_reference_records: list[dict[str, Any]] = []
    unique_positive = [r for r in positive_reference_records if r['targetCount'] == 1]
    selected_broken = unique_positive[:20]
    for idx, case in enumerate(selected_broken, start=1):
        source_obj = copy.deepcopy(examples[case['sourceFile']])
        parts: list[Any] = []
        for part in case['refPath'].split('.'):
            if part.isdigit():
                parts.append(int(part))
            else:
                parts.append(part)
        original_value = get_at_path(source_obj, parts)
        bad_value = f'missing::{original_value}'
        set_at_path(source_obj, parts, bad_value)
        mutated_records = collect_resolvable_refs(case['sourceFile'], source_obj, id_index)
        still_resolves = any(r['refPath'] == case['refPath'] and r['refValue'] == bad_value for r in mutated_records)
        broken_reference_records.append({
            'caseId': f'broken-ref::{idx:02d}',
            'sourceFile': case['sourceFile'],
            'refPath': case['refPath'],
            'originalValue': original_value,
            'mutatedValue': bad_value,
            'status': 'EXPECTED_FAIL' if not still_resolves else 'UNEXPECTED_PASS',
        })
        if still_resolves:
            result['overall'] = 'FAIL'

    negative_summary = {
        'casesChecked': len(negative_records),
        'expectedFailCount': sum(1 for r in negative_records if r['status'] == 'EXPECTED_FAIL'),
        'unexpectedPassCount': sum(1 for r in negative_records if r['status'] == 'UNEXPECTED_PASS'),
        'skippedCount': sum(1 for r in negative_records if r['status'] == 'SKIP'),
    }
    reference_summary = {
        'packageLocalResolvableRefChecks': len(positive_reference_records),
        'uniqueTargetPassCount': sum(1 for r in positive_reference_records if r['status'] == 'UNIQUE_TARGET_PASS'),
        'variantTargetPassCount': sum(1 for r in positive_reference_records if r['status'] == 'VARIANT_TARGET_PASS'),
        'brokenReferenceCasesChecked': len(broken_reference_records),
        'brokenReferenceExpectedFailCount': sum(1 for r in broken_reference_records if r['status'] == 'EXPECTED_FAIL'),
        'brokenReferenceUnexpectedPassCount': sum(1 for r in broken_reference_records if r['status'] == 'UNEXPECTED_PASS'),
        'packageLocalResolvableRefScopeNote': 'Only refs whose current values resolve to primary ids in package-local example artifacts are checked here.',
    }
    result['negativeValidationSummary'] = negative_summary
    result['referenceConsistencySummary'] = reference_summary
    result['summary'] = {
        'schemasValidated': len(result['schemaChecks']),
        'positiveExamplesValidated': len(result['positiveExampleValidation']),
        'negativeCasesChecked': negative_summary['casesChecked'],
        'packageLocalResolvableRefsChecked': reference_summary['packageLocalResolvableRefChecks'],
        'brokenReferenceCasesChecked': reference_summary['brokenReferenceCasesChecked'],
    }

    dump_json(NEGATIVE, {
        'runner': Path(__file__).name,
        'records': negative_records,
        'summary': negative_summary,
    })
    dump_json(REFERENCE, {
        'runner': Path(__file__).name,
        'positiveReferenceRecords': positive_reference_records,
        'brokenReferenceRecords': broken_reference_records,
        'summary': reference_summary,
    })
    dump_json(RESULTS, result)

    print(RESULTS)
    print(result['overall'])
    return 0 if result['overall'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
