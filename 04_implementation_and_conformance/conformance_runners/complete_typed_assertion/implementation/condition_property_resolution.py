"""Contextual consumer of the separately adopted generic property source rule.

This module never adds revision aliases to a shared source catalog. Only the
two fixed condition-reader seams can request the exact selected method field.
"""
from pathlib import Path
from types import ModuleType

from strict_inputs import InputError, digest, parse, sha

HERE = Path(__file__).resolve().parent
CORE_SHA256 = '701df5c64f306bde008a56f39f5b0148f11c6f9c64a99a7e626c635939fb1376'
VERSION = 'ofarm.assertionDomainEvaluationSelection.v0.5'
ROLES = {'WORK_CONDITION_PROPERTY_DEFINITION', 'CRITERION_OBSERVED_PROPERTY_DEFINITION'}


def _checker():
    root = HERE / 'condition-property-source'
    raw = (root / 'core-manifest.json').read_bytes()
    if sha(raw) != CORE_SHA256:
        raise InputError('CONDITION_PROPERTY_CORE_MANIFEST_MISMATCH')
    manifest = parse(raw)
    verified = {}
    for item in manifest['members']:
        data = (root / item['path']).read_bytes()
        if sha(data) != item['rawSha256'] or len(data) != item['byteLength']:
            raise InputError('CONDITION_PROPERTY_CORE_MEMBER_MISMATCH')
        verified[item['path']] = data
    # The adopted pure checker imports this utility by its original module name.
    # Require the exact same bytes in the enclosing consumer; no new alias may
    # silently supply a different JSON/JCS interpretation.
    if (HERE / 'strict_inputs.py').read_bytes() != verified['strict_inputs.py']:
        raise InputError('CONDITION_PROPERTY_JSON_DEPENDENCY_MISMATCH')
    # Execute the bytes just verified; a path loader could reread a changed
    # file or a cached bytecode file after the manifest check.
    path = root / 'resolve_property.py'
    module = ModuleType('_ofarm_condition_property_core')
    module.__file__ = str(path)
    exec(compile(verified['resolve_property.py'], str(path), 'exec'), module.__dict__)
    return module.resolve


def enabled(bound):
    return (bound['selection'].get('schemaVersion') == VERSION
            and 'conditionPropertyRevisionSources' in bound['selection'])


def _pin(value, with_ref=False):
    keys = ('rawSha256', 'byteLength', 'wholeJcsDigest')
    return {key: value[key] for key in ((*keys, 'ref') if with_ref else keys)}


def resolve_method(bound, method_id, binding):
    """Recheck selected rule/map/method/property facts for one actual field.

    No returned PASS can replace the caller's parent schema, actual-read or
    condition-use guards. The caller supplies method_id from that occurrence.
    """
    if not enabled(bound):
        return None
    choice = bound['selection']['conditionPropertyRevisionSources']
    by_id, by_ref = bound['pinsById'], bound['pinsByRef']
    method_pin = by_id.get(method_id)
    method = bound['admittedJson'].get(method_id)
    if (method_pin is None or method_pin['digestMode'] != 'JCS_JSON'
            or not isinstance(method, dict) or method.get('propertyBinding') != binding
            or type(binding) is not dict or set(binding) != {'ref', 'revisionRef'}):
        return None
    rule_id, map_id = choice['ruleInputId'], choice['mapInputId']
    property_pin = by_ref.get(binding['ref'])
    property_id = property_pin['inputId'] if property_pin else None
    raw = bound.get('originalBytes', {})
    report = _checker()(rule_bytes=raw.get(rule_id), rule_pin=_pin(by_id[rule_id]),
                        map_bytes=raw.get(map_id), map_pin=_pin(by_id[map_id]),
                        method_bytes=raw.get(method_id), method_pin=_pin(method_pin, True),
                        property_bytes=raw.get(property_id))
    errors, missing = [], []
    input_ids = list(dict.fromkeys([rule_id, map_id, method_id] + ([property_id] if property_id else [])))
    for iid in input_ids:
        status = bound['inventoryResults'][iid]['status']
        if status == 'MISMATCH':
            errors.append({'code': 'CONDITION_PROPERTY_SELECTED_ORIGINAL_MISMATCH', 'inputId': iid})
        elif status != 'MATCHED':
            missing.append({'code': 'CONDITION_PROPERTY_SELECTED_ORIGINAL_UNAVAILABLE', 'inputId': iid})
    nominations = [row for row in bound['selection'].get('sourceSelections', []) if row['binding'] == binding]
    if property_pin is None:
        errors.append({'code': 'CONDITION_PROPERTY_NOT_IN_INDEPENDENT_SELECTION'})
    elif property_pin['digestMode'] != 'JCS_JSON':
        errors.append({'code': 'CONDITION_PROPERTY_JSON_MODE_REQUIRED'})
    elif len(nominations) != 1:
        missing.append({'code': 'CONDITION_PROPERTY_EXACT_NOMINATION_PENDING'})
    elif (nominations[0]['rawSha256'] != property_pin['rawSha256']
          or nominations[0]['valueDigest'] != property_pin['wholeJcsDigest']):
        errors.append({'code': 'CONDITION_PROPERTY_NOMINATION_CONTRADICTION'})
    # Map contradictions are independent of whether the target bytes arrived.
    mapping = bound['admittedJson'].get(map_id)
    matches = []
    if isinstance(mapping, dict) and isinstance(mapping.get('entries'), list):
        matches = [(n, row) for n, row in enumerate(mapping['entries'])
                   if isinstance(row, dict) and row.get('binding') == binding]
    if property_pin is not None and property_pin['digestMode'] == 'JCS_JSON' and len(matches) == 1:
        entry = matches[0][1]
        if any(entry.get(key) != property_pin[key] for key in ('rawSha256', 'byteLength', 'wholeJcsDigest')):
            errors.append({'code': 'CONDITION_PROPERTY_MAP_INVENTORY_CONTRADICTION'})
    status = ('FAIL' if errors or report['disposition'] == 'FAIL' else
              'NOT_EVALUATED' if missing or report['disposition'] != 'PASS' else 'PASS')
    observations = []
    for iid in input_ids:
        if iid in bound['admittedJson']:
            observations.append({'inputRole': iid, 'pointer': '',
                                 'valueDigest': digest(bound['admittedJson'][iid])})
    observations.append({'inputRole': method_id, 'pointer': '/propertyBinding', 'valueDigest': digest(binding)})
    if len(matches) == 1:
        observations.append({'inputRole': map_id, 'pointer': '/entries/' + str(matches[0][0]),
                             'valueDigest': digest(matches[0][1])})
    answer = {'disposition': status, 'diagnostics': report['diagnostics'] + errors + missing,
              'methodInputId': method_id, 'propertyInputId': property_id, 'selectedBinding': binding,
              'ruleInputId': rule_id, 'mapInputId': map_id, 'inputIds': input_ids,
              'selectionRawSha256': bound['selectionRawSha256'],
              'selectionPointer': '/conditionPropertyRevisionSources',
              'selectionValueDigest': digest(choice), 'observations': observations,
              'coreManifestRawSha256': CORE_SHA256,
              'mapEntryPointer': '/entries/' + str(matches[0][0]) if len(matches) == 1 else None,
              'qualification': 'Contextual generic property source selection only; no source-use admission or domain acceptance.'}
    if status == 'PASS':
        if property_id not in bound['admittedJson'] or report.get('selection') is None:
            raise InputError('CONDITION_PROPERTY_RESOLUTION_WITHOUT_ORIGINAL')
        answer['entry'] = {'id': property_id, 'binding': binding,
                           'record': bound['admittedJson'][property_id],
                           'rawSha256': property_pin['rawSha256'],
                           'valueDigest': property_pin['wholeJcsDigest'],
                           'digestMode': 'JCS_JSON', 'byteLength': property_pin['byteLength'],
                           'claimRoles': [], 'selectorMapping': dict(nominations[0])}
    return answer


class ConditionSources(list):
    """Ordinary catalog with an explicit property-only, per-method read seam."""
    def __init__(self, entries, bound, allowed_method_id=None, require_existing=False):
        # A legacy protected catalog may already contain property revision
        # aliases. Retain them privately for original ordinary IDs, but do not
        # expose them through list iteration to another field or reader.
        prior = getattr(entries, '_property_aliases', [])
        property_bindings = [entry['record'].get('propertyBinding') for entry in entries
            if isinstance(entry.get('record'), dict)
            and entry['record'].get('schemaVersion') == 'ofarm.assertionDomainMeasurementUseDefinition.v0.1']
        aliases = [entry for entry in entries
                   if 'revisionRef' in entry.get('binding', {})
                   and (entry['binding'] in property_bindings
                        or isinstance(entry.get('record'), dict)
                        and entry['record'].get('category') == 'OBSERVED_PROPERTY')]
        super().__init__(entry for entry in entries if not any(entry is alias for alias in aliases))
        self._property_aliases = [*prior, *aliases]
        self.bound = bound
        self.allowed_method_id = allowed_method_id
        self.require_existing = require_existing

    def method_id(self, method):
        entries = [entry for entry in self if entry['record'] is method]
        if not entries:
            return None
        identities = set()
        for entry in entries:
            pin = self.bound['pinsByRef'].get(entry['binding']['ref'])
            if (pin is None or pin['digestMode'] != 'JCS_JSON'
                    or self.bound['inventoryResults'][pin['inputId']]['status'] != 'MATCHED'
                    or entry.get('rawSha256') != pin['rawSha256']
                    or digest(method) != pin['wholeJcsDigest']):
                return None
            identities.add(pin['inputId'])
        return next(iter(identities)) if len(identities) == 1 else None

    def property_for(self, method, *, recursive=False):
        iid = self.method_id(method)
        if iid is None or recursive and iid != self.allowed_method_id:
            return []
        binding = method.get('propertyBinding')
        resolved = resolve_method(self.bound, iid, binding)
        if not resolved or resolved['disposition'] != 'PASS':
            return []
        chosen = resolved['entry']
        aliases = [entry for entry in self._property_aliases
                   if entry['binding'] == binding and entry.get('rawSha256') == chosen['rawSha256']
                   and entry.get('valueDigest') == chosen['valueDigest']
                   and digest(entry['record']) == chosen['valueDigest']]
        if len(aliases) > 1 or self.require_existing and not aliases:
            return []
        return [aliases[0] if aliases else chosen]

    def for_method(self, method):
        return ConditionSources(self, self.bound, self.method_id(method), self.require_existing)


def catalog(entries, bound, *, method_id=None, require_existing=False):
    return (ConditionSources(entries, bound, method_id, require_existing)
            if bound['selection'].get('schemaVersion') == VERSION else entries)
