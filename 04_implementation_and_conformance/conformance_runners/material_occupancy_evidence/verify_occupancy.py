"""Opt-in material occupancy evidence comparison; no occupancy or runtime writes.

Call verify(request_bytes, context_bytes, records, trusted_pins=...). All values
are original bytes. records maps selector_key(full_binding) to original bytes.
The contract, context and request hashes must come from independent selection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

CID = 'ofarm.material-occupancy-evidence.v0.1'
PACKAGE = Path(__file__).resolve().parent
LIMIT = 2 * 1024 * 1024
BUNDLE_LIMIT = 16 * 1024 * 1024
SCHEMAS = ['context', 'record', 'request']
SOURCES = ['sources/constitution.md', 'sources/identity-lifecycle.md', 'sources/identity-lifecycle.schema.json', 'sources/container-continuity-example.json']
TIME_RE = re.compile(r'([0-9]{4}-[0-9]{2}-[0-9]{2})T([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(?:\.([0-9]{1,9}))?Z')
QUALIFICATIONS = [
    'MATCHED means exact conditional comparison against independently selected owner context and original source bytes; it does not authenticate that context.',
    'Actual source validity, dispute resolution, inventory completeness, currentness and source-owner authority remain with their owners. This checker preserves and qualifies their selected reported posture.',
    'Supporting event, measurement, identity, unit, extent and lifecycle bytes are retained and bound without replacing their owner validators. No event family or measurement result kind is excluded.',
    'No durable identity, movement, occupancy creation or closure, current-state write, assertion promotion, authorization, runtime protection, CI activation or merge is performed.',
]

class Fault(ValueError):
    pass

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def strict(raw):
    if not isinstance(raw, bytes) or not raw or len(raw) > LIMIT:
        raise Fault('MISSING_NONBYTE_OR_OVERSIZE_INPUT')
    depth, quoted, escaped = 0, False, False
    for byte in raw:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            depth += 1
            if depth > 64:
                raise Fault('JSON_DEPTH_LIMIT')
        elif byte in (93, 125):
            depth -= 1
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Fault('DUPLICATE_JSON_NAME')
            result[key] = value
        return result
    def constant(_):
        raise Fault('NON_JSON_NUMBER')
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Fault('INVALID_UTF8_JSON') from exc

def selector_key(binding):
    """Stable transport map key; never derive or translate an immutable selector."""
    return json.dumps(binding, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def timestamp(value):
    match = TIME_RE.fullmatch(value) if isinstance(value, str) else None
    if not match:
        raise Fault('NONCANONICAL_TIMESTAMP')
    day = datetime.strptime(match[1], '%Y-%m-%d').toordinal()
    return (((day * 24 + int(match[2])) * 60 + int(match[3])) * 60 + int(match[4])) * 10**9 + int((match[5] or '').ljust(9, '0'))

def binding_keys(value):
    if isinstance(value, dict):
        if set(value) in ({'ref', 'digest'}, {'ref', 'revisionRef'}):
            yield selector_key(value)
        else:
            for child in value.values():
                yield from binding_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from binding_keys(child)

def window(value):
    if value['mode'] == 'AS_OF':
        at = timestamp(value['at'])
        return at, True, at, True
    start, end = timestamp(value['start']), timestamp(value['end'])
    if end < start or (end == start and not (value['startInclusive'] and value['endInclusive'])):
        raise Fault('EMPTY_OR_REVERSED_APPLICABILITY')
    return start, value['startInclusive'], end, value['endInclusive']

def contains(outer, inner):
    left, li, right, ri = outer
    a, ai, b, bi = inner
    return ((left < a or (left == a and (li or not ai))) and
            (right > b or (right == b and (ri or not bi))))

def temporal_coverage(facts):
    selected = window(facts['applicability'])
    start, end = facts['interval']['start'], facts['interval']['end']
    lower = timestamp(start['at']) if start['posture'] == 'KNOWN' else None
    upper = timestamp(end['at']) if end['posture'] == 'KNOWN' else (timestamp(end['asOf']) if end['posture'] == 'OPEN_AS_OF' else None)
    if lower is not None and upper is not None:
        if upper < lower or (upper == lower and (not start['inclusive'] or (end['posture'] == 'KNOWN' and not end['inclusive']))):
            raise Fault('EMPTY_OR_REVERSED_OCCUPANCY_INTERVAL')
    # Each known boundary constrains applicability independently. An unknown
    # opposite endpoint cannot erase a known contradiction or expired open end.
    if lower is not None and not contains((lower, start['inclusive'], 10**40, True), selected):
        raise Fault('KNOWN_START_EXCLUDES_SOURCE_APPLICABILITY')
    if upper is not None and not contains((-10**40, True, upper, end.get('inclusive', True)), selected):
        raise Fault('KNOWN_END_EXCLUDES_SOURCE_APPLICABILITY' if end['posture'] == 'KNOWN' else 'OPEN_END_OBSERVATION_EXCLUDES_SOURCE_APPLICABILITY')
    # Unknown endpoint posture is retained, never silently converted to infinity.
    if start['posture'] == 'UNKNOWN' or end['posture'] == 'UNKNOWN':
        return False
    lo = lower if lower is not None else -10**40
    hi = upper if upper is not None else 10**40
    return contains((lo, start.get('inclusive', True), hi, end.get('inclusive', True)), selected)

def verify(request_bytes, context_bytes, records, *, trusted_pins, package_root=PACKAGE, source_root=None):
    """Compare original-byte source records with an independently selected context.

    trusted_pins has exactly contractSha256, contextSha256, requestSha256. The
    caller must not copy these from the request/context it is trying to verify.
    The records mapping is data, never a resolver callback or admission flag.
    """
    report = {'schemaVersion': 'ofarm.materialOccupancyVerificationReport.v0.1',
              'status': 'INPUT_ERROR', 'contractId': CID,
              'primaryTrustBoundary': 'Material occupancy source evidence',
              'verificationMode': 'CONDITIONAL_OFFLINE_OWNER_EVIDENCE',
              'runtimeAdmission': 'NOT_ESTABLISHED', 'actualInventoryCompleteness': 'NOT_ESTABLISHED',
              'requestSha256': sha(request_bytes) if isinstance(request_bytes, bytes) else None,
              'contextSha256': sha(context_bytes) if isinstance(context_bytes, bytes) else None,
              'checkedRules': [], 'errors': [], 'episodes': [], 'boundRecords': [],
              'qualifications': QUALIFICATIONS.copy()}
    def error(code, document, detail=None):
        item = {'code': code, 'document': document}
        if detail is not None:
            item['detail'] = detail
        report['errors'].append(item)
    def check(ok, code, document, detail=None):
        if not ok:
            error(code, document, detail)
        return ok
    try:
        import rfc8785
        from jsonschema import Draft202012Validator, FormatChecker
        if version('rfc8785') != '0.1.4' or version('jsonschema') != '4.26.0':
            raise Fault('UNSUPPORTED_LOCAL_DEPENDENCY')
        def digest(value):
            return 'sha256:' + sha(rfc8785.dumps(value))
        if not isinstance(trusted_pins, dict) or set(trusted_pins) != {'contractSha256','contextSha256','requestSha256'} or any(not isinstance(v, str) or not re.fullmatch('[0-9a-f]{64}', v) for v in trusted_pins.values()):
            raise Fault('INVALID_INDEPENDENT_PINS')
        raw_contract = (Path(package_root) / 'contract.json').read_bytes()
        if not check(sha(raw_contract) == trusted_pins['contractSha256'], 'CONTRACT_PIN_MISMATCH', 'contract'):
            return report
        contract = strict(raw_contract)
        if not isinstance(contract, dict) or contract.get('contractId') != CID or contract.get('interpretation') != 'CONDITIONAL_SELECTED_SOURCE_EVIDENCE_ONLY':
            raise Fault('UNSUPPORTED_CONTRACT')
        if not check(contract.get('contractDigest') == digest({k:v for k,v in contract.items() if k != 'contractDigest'}), 'CONTRACT_SELF_DIGEST_MISMATCH', 'contract'):
            return report
        if set(contract.get('schemas', {})) != set(SCHEMAS) or set(contract.get('sources', {})) != set(SOURCES) or set(contract.get('checker', {})) != {'verify_occupancy.py'}:
            raise Fault('PACKAGE_CLOSURE_MISMATCH')
        if not check(sha(Path(__file__).read_bytes()) == contract['checker']['verify_occupancy.py'], 'CHECKER_PIN_MISMATCH', 'checker'):
            return report
        fmt = FormatChecker()
        @fmt.checks('occupancy-timestamp', raises=(ValueError, TypeError))
        def valid_time(value):
            if not isinstance(value, str):
                return True
            timestamp(value)
            return True
        validators = {}
        for name in SCHEMAS:
            raw = (Path(package_root) / 'schemas' / (name + '.schema.json')).read_bytes()
            if not check(sha(raw) == contract['schemas'][name], 'SCHEMA_PIN_MISMATCH', name):
                return report
            schema = strict(raw)
            # Every schema in this owner interface is inline; no network resolution.
            def closed(value):
                if isinstance(value, dict):
                    return all(k not in ('$ref','$dynamicRef','$recursiveRef') and closed(v) for k,v in value.items())
                return all(closed(v) for v in value) if isinstance(value, list) else True
            if not closed(schema):
                raise Fault('NONLOCAL_SCHEMA_REFERENCE')
            Draft202012Validator.check_schema(schema)
            validators[name] = Draft202012Validator(schema, format_checker=fmt)
        if source_root is None:
            source_root = package_root
        for name in SOURCES:
            if not check(sha((Path(source_root) / name).read_bytes()) == contract['sources'][name], 'SEMANTIC_SOURCE_PIN_MISMATCH', name):
                return report
        report['checkedRules'].append('PINNED_EXACT_PACKAGE_AND_SOURCE_CLOSURE')
        if not check(sha(context_bytes) == trusted_pins['contextSha256'], 'CONTEXT_PIN_MISMATCH', 'context') or not check(sha(request_bytes) == trusted_pins['requestSha256'], 'REQUEST_PIN_MISMATCH', 'request'):
            return report
        context, request = strict(context_bytes), strict(request_bytes)
        for name, value in [('context', context), ('request', request)]:
            errors = list(validators[name].iter_errors(value))
            if errors:
                error('SCHEMA_MISMATCH', name, [{'path': list(e.absolute_path), 'rule': e.validator} for e in errors[:20]])
        if report['errors']:
            return report
        report['checkedRules'].append('STRICT_JSON_AND_CLOSED_SCHEMAS')
        fixed_at = timestamp(context['fixedAt'])
        if not check(digest(context['selection']) == digest(request['selection']), 'SELECTION_MISMATCH', 'request'):
            return report
        selected_window = window(context['selection']['applicability'])
        selected_keys = [selector_key(b) for b in context['episodeBindings']]
        request_keys = [selector_key(e['binding']) for e in request['episodes']]
        if not check(len(selected_keys) == len(set(selected_keys)), 'DUPLICATE_SELECTED_EPISODE', 'context') or not check(selected_keys == request_keys, 'EPISODE_SET_OR_ORDER_MISMATCH', 'request'):
            return report
        if not isinstance(records, dict) or any(not isinstance(k, str) or not isinstance(v, bytes) for k,v in records.items()):
            raise Fault('INVALID_ORIGINAL_BYTE_RECORD_MAP')
        if len(records) > 2048 or sum(map(len, records.values())) > BUNDLE_LIMIT:
            raise Fault('RECORD_BUNDLE_LIMIT')
        entries = context['records']
        keys = [selector_key(e['binding']) for e in entries]
        if not check(len(keys) == len(set(keys)), 'DUPLICATE_SOURCE_SELECTOR', 'context') or not check(set(keys) == set(records), 'ORIGINAL_RECORD_SET_MISMATCH', 'records'):
            return report
        if not check([selector_key(e['binding']) for e in entries if e['role'] == 'EPISODE'] == selected_keys, 'OWNER_EPISODE_MANIFEST_MISMATCH', 'context'):
            return report
        parsed = {}
        for entry, key in zip(entries, keys):
            raw = records[key]
            if not raw or len(raw) > LIMIT:
                raise Fault('EMPTY_OR_OVERSIZE_RECORD')
            if not check(sha(raw) == entry['bytesSha256'], 'ORIGINAL_BYTES_MISMATCH', key):
                continue
            if entry['digestMode'] == 'JCS_JSON':
                parsed[key] = strict(raw)
                actual_digest = digest(parsed[key])
            else:
                actual_digest = 'sha256:' + sha(raw)
            check(actual_digest == entry['valueDigest'], 'SELECTED_VALUE_DIGEST_MISMATCH', key)
            if 'digest' in entry['binding']:
                check(entry['binding']['digest'] == actual_digest, 'IMMUTABLE_BINDING_DIGEST_MISMATCH', key)
            if entry['role'] == 'EPISODE':
                check(entry['digestMode'] == 'JCS_JSON', 'EPISODE_REQUIRES_JSON_SOURCE', key)
            report['boundRecords'].append(entry.copy())
        if report['errors']:
            return report
        report['checkedRules'].append('EXACT_ORIGINAL_BYTES_AND_FULL_IMMUTABLE_SELECTORS')
        required = set(binding_keys(context['selection'])) | set(binding_keys(context['ownerIdentity'])) | set(selected_keys)
        for item in request['episodes']:
            key = selector_key(item['binding'])
            source = parsed[key]
            errors = list(validators['record'].iter_errors(source))
            if errors:
                error('OCCUPANCY_SOURCE_SCHEMA_MISMATCH', key, [{'path': list(e.absolute_path), 'rule': e.validator} for e in errors[:20]])
                continue
            facts = source['facts']
            required.update(binding_keys(facts))
            check(facts['occupant']['binding']['ref'] != facts['place']['binding']['ref'], 'OCCUPANT_AND_PLACE_IDENTITY_NOT_DISTINCT', key)
            check(digest(facts) == digest(item['expectedFacts']), 'OCCUPANCY_FACTS_MISMATCH', key)
            check(digest(facts['place']) == digest(context['selection']['place']), 'SELECTED_PLACE_MISMATCH', key)
            check(contains(window(facts['applicability']), selected_window), 'SOURCE_APPLICABILITY_MISMATCH', key)
            if facts['interval']['end']['posture'] == 'OPEN_AS_OF':
                check(timestamp(facts['interval']['end']['asOf']) <= fixed_at, 'OPEN_POSTURE_AFTER_CONTEXT', key)
            posture = facts['sourcePosture']
            check(timestamp(posture['assessedAt']) <= fixed_at, 'POSTURE_AFTER_CONTEXT', key)
            if posture['revision'] == 'SUPERSEDED':
                check(bool(posture['supersededBy']), 'MISSING_SUPERSESSION_EVIDENCE', key)
            else:
                check(not posture['supersededBy'], 'CONTRADICTORY_SUPERSESSION_EVIDENCE', key)
            temporal = temporal_coverage(facts)
            unresolved = facts['interval']['start']['posture'] == 'UNKNOWN' or facts['interval']['end']['posture'] == 'UNKNOWN'
            if not unresolved:
                check(temporal, 'OCCUPANCY_INTERVAL_DOES_NOT_COVER_SOURCE_APPLICABILITY', key)
            posture_ok = posture['validity'] == 'VALID' and posture['dispute'] == 'UNDISPUTED' and posture['revision'] in ('CURRENT','HISTORICAL_APPLICABLE')
            amount_known = facts['occupiedQuantity']['posture'] == 'REPORTED' or facts['occupiedCohort']['posture'] == 'IDENTIFIED'
            report['episodes'].append({'binding': item['binding'], 'facts': facts, 'temporalCoverage': 'SUPPORTED' if temporal else 'UNRESOLVED', 'selectedPostureSupportsUnqualifiedClaim': posture_ok and temporal and amount_known and facts['relevantExtent']['posture'] != 'UNRESOLVED'})
        if not check(required == set(keys), 'REFERENCED_SOURCE_CLOSURE_MISMATCH', 'context', {'missing': sorted(required - set(keys)), 'unexpected': sorted(set(keys) - required)}):
            report['episodes'] = []
            return report
        report['checkedRules'].extend(['COMPLETE_SELECTED_EPISODE_INVENTORY', 'EXACT_ENDPOINT_DIRECTION_INTERVAL_AMOUNT_UNIT_EXTENT_AND_POSTURE', 'COMPLETE_OWNED_REFERENCE_CLOSURE', 'PRESERVE_REPEATED_AND_OVERLAPPING_EPISODES'])
        report['status'] = 'MISMATCH' if report['errors'] else 'MATCHED_SELECTED_OCCUPANCY_EVIDENCE'
    except (ImportError, OSError, ValueError, TypeError, KeyError, OverflowError, RecursionError) as exc:
        error(str(exc) if isinstance(exc, Fault) else type(exc).__name__, 'input-or-package')
    if report['errors']:
        # No partial successful output may be mistaken for an accepted whole set.
        report['episodes'] = []
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', required=True, type=Path)
    parser.add_argument('--context', required=True, type=Path)
    parser.add_argument('--record-map', required=True, type=Path, help='JSON list of {binding,path}; paths relative to this map')
    parser.add_argument('--trusted-pins', required=True, type=Path)
    parser.add_argument('--package-root', type=Path, default=PACKAGE)
    parser.add_argument('--source-root', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    try:
        rows = strict(args.record_map.read_bytes())
        if not isinstance(rows, list) or any(not isinstance(row, dict) or set(row) != {'binding','path'} for row in rows):
            raise Fault('INVALID_RECORD_FILE_MAP')
        mapping = {}
        for row in rows:
            key = selector_key(row['binding'])
            if key in mapping:
                raise Fault('DUPLICATE_RECORD_FILE_SELECTOR')
            path = (args.record_map.parent / row['path']).resolve()
            if not path.is_relative_to(args.record_map.parent.resolve()):
                raise Fault('RECORD_FILE_PATH_ESCAPE')
            mapping[key] = path.read_bytes()
        report = verify(args.request.read_bytes(), args.context.read_bytes(), mapping, trusted_pins=strict(args.trusted_pins.read_bytes()), package_root=args.package_root, source_root=args.source_root)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        report = {'status':'INPUT_ERROR', 'errors':[{'code':str(exc) if isinstance(exc, Fault) else type(exc).__name__, 'document':'cli'}]}
    raw = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(raw)
    else:
        sys.stdout.write(raw)
    return 0 if report['status'] == 'MATCHED_SELECTED_OCCUPANCY_EVIDENCE' else 1

if __name__ == '__main__':
    raise SystemExit(main())
