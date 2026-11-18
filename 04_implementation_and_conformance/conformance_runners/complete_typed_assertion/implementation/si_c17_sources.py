"""Conditional C17 record completeness over independently selected originals.

Fixed SI construction rules supply meanings; neither the claim nor a register
projection supplies field facts. Source admission, live identity and transaction
acceptance are outside this reader. No raw bytes are reconstructed from JSON.
"""
from pathlib import Path
import math
import re

from strict_inputs import parse, sha, digest, same, pointer, InputError, distinct_selected_originals
from domain_reader_occurrences import (reader, selection, origin, observed_shape,
    predicate_value, branch, guard, observe_comparisons, selector_scope)

HERE = Path(__file__).resolve().parent
PINS = {
    'rules.v0_1.json': 'd9302cbff0e27bc325e5b9748016aa59784c609cf0e8c86af199aa3fc2df8773',
    'per-use-source-interpretation.schema.json': '1b26cf8f62e8fe121e76a7edac3cd662f994a579f6cced87ad314d8262b1f78f',
    'source-meaning.schema.json': '863567417e0340a584cac1eafbab27b05a9030cd847b3def8bf2e5524be1d0ad',
    'address-interpretation.schema.json': '8b2640c3d2197b50bfc8b19944934bba9b9fd42495160414aa8febac6450355e',
    'EvidenceRecord.schema.json': 'ee68822ae45e6a013412ef5173810747340c14671f44b593ee6f35ee113f2be6',
}
USE = 'urn:ofarm:si-c17-per-use-source-interpretation:v0.1'
MEANING = 'urn:ofarm:si-c17-source-meaning:v0.1'
ADDRESS = 'urn:ofarm:candidate:si-c17-professional-user-address-interpretation:v0.1'
EXECUTION = 'https://ofarm.dev/schema/executionrecordpayload/v0.1'
CODE = 'https://ofarm.dev/schema/agronomicidentitybinding/v0.1'
OBSERVATION = 'https://ofarm.dev/schema/agronomicobservationcontext/v0.1'
PARTIAL = 'https://ofarm.dev/schema/partialextent/v0.1'
PARTY = 'https://ofarm.dev/schema/party/v0.1'
EVIDENCE = 'https://ofarm.dev/schema/evidencerecord/v0.1'
ABSENT = object()


def register(schemas):
    """Register only the independently reviewed fixed local schema copies."""
    from definition_inputs import register as register_dependencies
    register_dependencies(schemas)
    from referencing import Registry, Resource
    for name, expected in PINS.items():
        raw = (HERE / 'si-c17' / name).read_bytes()
        if sha(raw) != expected:
            raise ValueError('SI_C17_FIXED_RULE_PIN_MISMATCH:' + name)
        value = parse(raw)
        if '$id' not in value:
            continue
        previous = schemas.schemas.get(value['$id'])
        if previous is not None and not same(previous, value):
            raise ValueError('SI_C17_SCHEMA_ID_CONFLICT:' + value['$id'])
        schemas.schemas[value['$id']] = value
    schemas.registry = Registry().with_resources((key, Resource.from_contents(value))
                                                 for key, value in schemas.schemas.items())


class _C17:
    def __init__(self, atom, sources, schemas, evidence):
        self.atom, self.sources, self.schemas, self.evidence = atom, sources, schemas, evidence
        self.claim = {'id': 'ATOM:' + atom['atomId'], 'record': atom}
        self.errors, self.missing, self.comparisons, self.ids, self.refs = [], [], [], [], []
        self.fields, self.conditions = {}, {}
        self.use = self.execution = self.product = self.address = self.person = None
        self.supported_use = False
        self.current = 'selection'
        self.field_issues = {}
        self.dependencies = []
        self.rules = parse((HERE / 'si-c17/rules.v0_1.json').read_bytes())

    def need(self, code, path='', *, field=None):
        row = {'role': 'SI_C17_' + code, 'pointer': path, 'field': field or self.current}
        if row not in self.missing:
            self.missing.append(row)
        return None

    def bad(self, code, path='', entry=None):
        row = {'code': 'SI_C17_' + code, 'pointer': path, 'field': self.current}
        if entry is not None:
            row['sourceInputId'] = entry['id']
        self.errors.append(row)
        return False

    def observe_predicate(self, code, outcome, left, right=None, *, depends_on=()):
        """Trace an existing decision without changing ordinary reader output.

        Operands name real original fields, including an observed absence.
        Derived facts such as selected-byte hashes travel through dependencies.
        """
        comparison = {'predicateId': 'SI_C17_' + code,
                      'source': origin(left[0]['id'], left[1]),
                      'disposition': 'PASS' if outcome else 'FAIL'}
        if right is not None:
            comparison['destination'] = origin(right[0]['id'], right[1])
        self.dependencies.extend(observe_comparisons([comparison], depends_on=depends_on) or [])

    def value(self, entry, path):
        if entry is None:
            return ABSENT
        try:
            value = pointer(entry['record'], path)
        except (InputError, ValueError, TypeError, IndexError, KeyError):
            event = guard('SI_C17_FIELD_PRESENT', False, origins=[origin(entry['id'], path)])
            if event is not None: self.dependencies.append(event)
            return ABSENT
        if entry is self.claim:
            guard('SI_C17_CLAIM_READ', True, origins=[origin(entry['id'], path)])
        else:
            predicate_value(entry, path, value, 'SI_C17_READ:' + self.current)
        return value

    def check(self, code, left, right=None, *, okay=None, depends_on=()):
        a = self.value(*left)
        b = self.value(*right) if right else ABSENT
        if a is ABSENT or right and b is ABSENT:
            return self.need('COMPARISON_FIELD_UNAVAILABLE:' + code, left[1])
        result = same(a, b) if okay is None else bool(okay)
        comparison = {'predicateId': 'SI_C17_' + code,
                      'source': {**origin(left[0]['id'], left[1]), 'valueDigest': digest(a)},
                      'disposition': 'PASS' if result else 'FAIL'}
        if right:
            comparison['destination'] = {**origin(right[0]['id'], right[1]), 'valueDigest': digest(b)}
        self.comparisons.append(comparison)
        emitted = observe_comparisons([comparison], depends_on=depends_on)
        self.dependencies.extend(emitted or [])
        if not result:
            self.bad(code, right[1] if right else left[1], right[0] if right else left[0])
        return result

    def select(self, binding, parent, path, schema=None):
        candidates = distinct_selected_originals([v for v in self.sources if same(v['binding'], binding)])
        event = selection('SI_C17_ORIGINAL', self.sources, candidates, binding=binding,
                  origins=[origin(parent['id'], path)], predicate_sites=('SI_C17_READ:' + self.current,))
        if event is not None: self.dependencies.append(event)
        if len(candidates) != 1:
            self.need('EXACT_ORIGINAL', path)
            if len(candidates) > 1:
                self.bad('AMBIGUOUS_ORIGINAL', path, parent)
            return None
        entry = candidates[0]
        self.ids.append(entry['id'])
        self.refs.append({'role': 'SI_C17_SELECTED_ORIGINAL', 'binding': binding, 'pointer': path})
        mapping = entry.get('selectorMapping')
        if not isinstance(mapping, dict):
            return self.need('INDEPENDENT_SELECTOR_MAPPING', path)
        if any(not same(mapping.get(key), entry.get(key)) for key in ('binding', 'rawSha256', 'valueDigest')):
            self.bad('SELECTOR_MAPPING_CONFLICT', path, entry)
            return None
        if entry.get('digestMode', 'JCS_JSON') != 'JCS_JSON':
            return self.need('JSON_ORIGINAL_REQUIRED', path)
        if entry.get('valueDigest') != digest(entry['record']):
            self.bad('CATALOG_VALUE_DIGEST_MISMATCH', path, entry)
            return None
        if 'digest' in binding and binding['digest'] != entry['valueDigest']:
            self.bad('CATALOG_BINDING_DIGEST_MISMATCH', path, entry)
            return None
        if schema and not self.shape(entry, schema):
            return None
        return entry

    def shape(self, entry, schema):
        errors = observed_shape(self.schemas, schema, entry['record'])
        for error in errors:
            self.errors.append({**error, 'field': self.current, 'sourceInputId': entry['id']})
        return not errors

    def id_check(self, entry, key):
        return self.check('SOURCE_ID', (entry, '/' + key), okay=self.value(entry, '/' + key) == entry['binding']['ref'])

    def linked_bindings(self, entry, path):
        values = self.value(entry, path)
        if values is ABSENT:
            return []
        found = []
        for n, binding in enumerate(values):
            selected = self.select(binding, entry, path + '/' + str(n))
            if selected is not None:
                found.append(selected)
        return found

    def read(self, parent, path, *, schema=None, role=None, pattern=None):
        read = self.value(parent, path)
        if read is ABSENT or not isinstance(read, dict):
            return self.need('SOURCE_READ_SELECTION', path)
        if role is not None and read['role'] != role:
            self.bad('SOURCE_READ_ROLE', path + '/role', parent); return None
        if pattern is not None and re.fullmatch(pattern, read['pointer']) is None:
            self.bad('SOURCE_READ_POINTER', path + '/pointer', parent); return None
        entry = self.select(read['binding'], parent, path + '/binding', schema)
        if entry is None:
            return None
        if read['role'] == 'EXECUTION' and self.execution is not None:
            if not same(entry['binding'], self.execution['binding']):
                self.bad('OTHER_EXECUTION_SELECTED', path, parent); return None
        return entry, read['pointer'], self.value(entry, read['pointer'])

    def slot(self, field, role, pattern, schema=None):
        base = '/fieldSelections/' + field + '/reads'
        values = self.value(self.use, base)
        positions = [n for n, read in enumerate(values)
                     if self.value(self.use, base + '/' + str(n) + '/role') == role]
        if len(positions) != 1:
            self.need('UNIQUE_FIELD_SELECTION:' + role, '/fieldSelections/' + field)
            if len(positions) > 1:
                self.bad('AMBIGUOUS_FIELD_SELECTION', '/fieldSelections/' + field, self.use)
            return None
        return self.read(self.use, '/fieldSelections/' + field + '/reads/' + str(positions[0]),
                         schema=schema, role=role, pattern=pattern)

    def meaning(self, entry, kind, *, per_use=True):
        if entry is None or not self.shape(entry, MEANING):
            return False
        if not self.id_check(entry, 'sourceMeaningId'):
            return False
        if not self.check('SOURCE_MEANING_KIND', (entry, '/kind'), okay=entry['record']['kind'] == kind):
            return False
        if per_use:
            self.check('MEANING_RECORD', (entry, '/recordBinding'), (self.use, '/recordBinding'))
            self.check('MEANING_SCOPE', (entry, '/scope'), (self.use, '/scope'))
            if self.execution is not None:
                interval = self.execution['record']['effectiveTimeInterval']
                for key in ('start', 'end', 'timeBasis'):
                    self.check('MEANING_USE_INTERVAL_' + key.upper(), (entry, '/useInterval/' + key),
                               (self.execution, '/effectiveTimeInterval/' + key))
        for key in ('basisBindings', 'contextBindings'):
            if key in entry['record']:
                self.linked_bindings(entry, '/' + key)
        return True

    def meaning_at(self, parent, path, kind, *, per_use=True):
        selected = self.read(parent, path, role=kind, pattern='')
        if selected and self.meaning(selected[0], kind, per_use=per_use):
            return selected[0]
        return None

    def meaning_list(self, parent, path, kind, *, per_use=True):
        values = self.value(parent, path)
        if values is ABSENT or len(values) != 1:
            self.need('UNIQUE_' + kind, path)
            if values is not ABSENT and len(values) > 1:
                self.bad('AMBIGUOUS_' + kind, path, parent)
            return None
        return self.meaning_at(parent, path + '/0', kind, per_use=per_use)

    def literal_basis(self, entry, keys):
        """Supported JSON route: named fields at one selected original root.

        Other document layouts require a separate interpretation; missing paths
        here are not a finding that the actual use record omitted the field.
        """
        bases = self.linked_bindings(entry, '/basisBindings')
        if len(bases) != 1:
            self.need('UNIQUE_LITERAL_BASIS', '/basisBindings'); return
        basis = bases[0]
        for key in keys:
            original = self.value(basis, '/' + key)
            interpreted = self.value(entry, '/' + key)
            if original is ABSENT and interpreted is ABSENT:
                continue
            if original is ABSENT or interpreted is ABSENT:
                self.need('UNSUPPORTED_BASIS_FIELD:' + key, '/' + key)
            else:
                self.check('ORIGINAL_' + key.upper(), (basis, '/' + key), (entry, '/' + key))

    def condition(self, field):
        old = self.current; self.current = field
        dependency_start = len(self.dependencies)
        path = '/conditionalRequirements/' + field
        declaration = self.value(self.use, path)
        self.value(self.use, path + '/disposition')
        self.value(self.use, path + '/basis')
        before = len(self.missing)
        entry = self.meaning_list(self.use, path + '/basis', 'FIELD_APPLICABILITY') if declaration['basis'] else None
        outcome = 'UNKNOWN'
        if entry is not None:
            record = entry['record']
            self.check('CONDITION_FIELD', (entry, '/field'), okay=record['field'] == field)
            if field in ('startHour', 'growthStage') and self.product:
                self.check('CONDITION_PRODUCT', (entry, '/productBinding'), okay=same(record['productBinding'], self.product['binding']))
            for key in ('restrictionAssessment', 'contextAssessment'):
                self.linked_bindings(entry, '/' + key + '/basisBindings')
            a = self.value(entry, '/restrictionAssessment/conclusion')
            b = self.value(entry, '/contextAssessment/conclusion')
            coverage = self.value(entry, '/contextCoverage')
            if 'CONFLICTED' in (a, b): outcome = 'CONFLICTED'
            elif 'REQUIRES_FIELD' in (a, b): outcome = 'REQUIRED'
            elif 'REVIEW_REQUIRED' in (a, b): outcome = 'REVIEW_REQUIRED'
            elif a == b == 'DOES_NOT_REQUIRE_FIELD' and coverage == 'COMPLETE_FOR_SELECTED_USE': outcome = 'NOT_REQUIRED'
            if len(self.missing) > before:
                outcome = 'UNKNOWN'
            self.check('CONDITION_DISPOSITION', (entry, ''), (self.use, path + '/disposition'),
                       okay=outcome == declaration['disposition'] or outcome == 'UNKNOWN' and len(self.missing) > before)
        elif declaration['disposition'] not in ('UNKNOWN', 'REVIEW_REQUIRED', 'SOURCE_UNAVAILABLE'):
            self.need('SUPPORTED_CONDITIONAL_REQUIREMENT', path)
        if declaration['disposition'] == 'CONFLICTED' or outcome == 'CONFLICTED':
            self.observe_predicate('CONFLICTED_REQUIREMENT', False, (self.use, path),
                                   (entry, '') if entry is not None else None,
                                   depends_on=self.dependencies[dependency_start:])
            self.bad('CONFLICTED_REQUIREMENT', path, self.use)
        # Missing relevance evidence does not block an independently valid supplied field.
        deferred = self.missing[before:]; del self.missing[before:]
        self.conditions[field] = {'disposition': outcome, 'remainingRoles': deferred}
        self.current = old
        return outcome

    def text(self, read):
        if read is None: return 'UNRESOLVED'
        if read[2] is ABSENT or read[2] == '': return 'ABSENT'
        if not isinstance(read[2], str):
            self.bad('TEXT_REQUIRED', read[1], read[0]); return 'CONTRADICTORY'
        return 'PRESENT'

    def product_source(self, field, path):
        read = self.slot(field, 'PRODUCT_BINDING', path, CODE)
        if read is None: return None
        entry = read[0]
        self.id_check(entry, 'agronomicIdentityBindingId')
        self.check('PRODUCT_ROLE', (entry, '/bindingRole'), okay=entry['record']['bindingRole'] == 'CROP_PROTECTION_PRODUCT')
        self.check('PRODUCT_EXECUTION_LINK', (entry, '/agronomicIdentityBindingId'),
                   (self.execution, '/agronomicIdentityBindingRefs'),
                   okay=entry['binding']['ref'] in self.execution['record'].get('agronomicIdentityBindingRefs', []))
        if self.product and not same(self.product['binding'], entry['binding']):
            self.bad('PRODUCT_SELECTION_CONFLICT', read[1], entry)
        self.product = entry
        self.binding_qualifications(entry)
        return read

    def binding_qualifications(self, entry):
        # Preserve these source qualifications; VERIFIED is not promotion.
        self.value(entry, '/promotionBoundary')
        period = self.value(entry, '/bindingValue/effectivePeriod')
        if period is ABSENT:
            return
        self.value(entry, '/bindingValue/effectivePeriod/start')
        self.value(entry, '/bindingValue/effectivePeriod/end')
        if entry['record']['bindingRole'] == 'CROP_PROTECTION_PRODUCT':
            # This is recorded authorization information, not a lawful-use test.
            return
        start, end = self.date_time(period.get('start')), self.date_time(period.get('end'))
        use = self.execution['record']['effectiveTimeInterval']
        a, b = self.date_time(use['start']), self.date_time(use['end'])
        if None in (start, end, a, b):
            self.need('BINDING_EFFECTIVE_PERIOD_INTERPRETATION', '/bindingValue/effectivePeriod')
        else:
            self.check('BINDING_EFFECTIVE_PERIOD', (entry, '/bindingValue/effectivePeriod'),
                       (self.execution, '/effectiveTimeInterval'), okay=start <= a <= b <= end)

    def date_time(self, text):
        from time_validation import foreign_seconds
        try:
            return foreign_seconds(text)
        except (ValueError, TypeError, InputError):
            return None

    def time(self, field):
        mapping = self.value(self.use, '/timeMapping')
        role = self.value(self.use, '/timeMapping/role')
        basis = self.value(self.use, '/timeMapping/timeBasis')
        if role != 'EXECUTION_START' or basis != 'EXECUTION_INTERVAL':
            return self.need('UNSUPPORTED_ACTUAL_TIME_LINKAGE', '/timeMapping') or 'UNRESOLVED'
        selected = self.read(self.use, '/timeMapping/source', role='EXECUTION', pattern='/effectiveTimeInterval/start', schema=EXECUTION)
        path = '/effectiveTimeInterval' if field == 'useDate' else '/effectiveTimeInterval/start'
        target = self.slot(field, 'EXECUTION', path, EXECUTION)
        for n in range(len(mapping['linkageBasis'])):
            self.read(self.use, '/timeMapping/linkageBasis/' + str(n), role='EXECUTION', pattern='/effectiveTimeInterval', schema=EXECUTION)
        if selected is None or target is None: return 'UNRESOLVED'
        interval = self.execution['record']['effectiveTimeInterval']
        if self.value(self.execution, '/effectiveTimeInterval/timeBasis') != 'EXECUTION_INTERVAL':
            return self.need('UNSUPPORTED_ACTUAL_TIME_BASIS', '/effectiveTimeInterval/timeBasis') or 'UNRESOLVED'
        if selected[2] is ABSENT: return 'ABSENT'
        start, end = self.date_time(interval['start']), self.date_time(interval['end'])
        if start is None or end is None:
            return self.need('UNSUPPORTED_OR_INVALID_ACTUAL_TIMESTAMP', '/effectiveTimeInterval') or 'UNRESOLVED'
        self.check('EXECUTION_INTERVAL_ORDER', (self.execution, '/effectiveTimeInterval'), okay=start <= end)
        return 'PRESENT'

    def unit(self, field, entry, path):
        mapping = self.value(self.use, '/unitMappings/' + field)
        encoding = self.value(self.use, '/unitMappings/' + field + '/encoding')
        numerator_meaning = self.value(self.use, '/unitMappings/' + field + '/numeratorMeaning')
        self.value(self.use, '/unitMappings/' + field + '/denominatorMeaning')
        if encoding not in ({'HECTARES'} if field == 'treatedArea' else {'COMPOUND_PER_HECTARE', 'SPLIT_PER_HECTARE'}):
            self.need('UNSUPPORTED_UNIT_MEANING', '/unitMappings/' + field); return
        meanings = []
        meaning_dependency_start = len(self.dependencies)
        for n in range(len(mapping['definitionSources'])):
            meaning = self.meaning_at(self.use, '/unitMappings/' + field + '/definitionSources/' + str(n), 'UNIT_MEANING', per_use=False)
            if meaning: meanings.append(meaning)
        meaning_dependencies = self.dependencies[meaning_dependency_start:]
        def match(qpath, upath, expected):
            q, u = self.value(entry, qpath), self.value(entry, upath)
            site = 'SI_C17_UNIT_CANDIDATE:' + upath
            selected = [m for m in meanings
                        if predicate_value(m, '/quantityKindRef', m['record']['quantityKindRef'], site) == q
                        and predicate_value(m, '/unitRef', m['record']['unitRef'], site) == u]
            # This chooses among originals already acquired by meaning_at.
            # A new acquisition here would couple later split-unit matches to it.
            event = guard('SI_C17_UNIT_DEFINITION:' + upath, len(selected) == 1,
                          origins=[origin(entry['id'], qpath), origin(entry['id'], upath),
                                   origin(self.use['id'], '/unitMappings/' + field + '/definitionSources')],
                          depends_on=meaning_dependencies, predicate_sites=(site,))
            if event is not None: self.dependencies.append(event)
            if len(selected) != 1:
                self.need('EXACT_UNIT_DEFINITION', upath)
                if len(selected) > 1:
                    self.observe_predicate('AMBIGUOUS_UNIT_MEANING', False, (entry, upath),
                                           (self.use, '/unitMappings/' + field + '/definitionSources'),
                                           depends_on=[event] if event is not None else [])
                    self.bad('AMBIGUOUS_UNIT_MEANING', upath, entry)
                return
            m = selected[0]
            self.check('UNIT_QUANTITY_KIND', (entry, qpath), (m, '/quantityKindRef'))
            self.check('UNIT_REF', (entry, upath), (m, '/unitRef'))
            self.check('UNIT_MEANING', (m, '/unitMeaning'), okay=m['record']['unitMeaning'] == expected)
        if field == 'treatedArea':
            match(path + '/quantityKindRef', path + '/unitRef', 'HECTARE')
        else:
            numerator = 'KILOGRAM' if numerator_meaning == 'KILOGRAM_PRODUCT' else 'LITRE'
            match(path + '/quantityKindRef', path + '/unitRef', numerator + '_PER_HECTARE' if encoding == 'COMPOUND_PER_HECTARE' else numerator)
            if encoding == 'SPLIT_PER_HECTARE':
                match(path + '/basisQuantityKindRef', path + '/basisUnitRef', 'HECTARE')
                self.check('ONE_HECTARE_BASIS', (entry, path + '/basisValue'), okay=self.value(entry, path + '/basisValue') == 1)

    def quantity(self, field):
        path = r'/actualQuantityParameters/(?:0|[1-9][0-9]*)' if field == 'dose' else '/executionExtent/area'
        read = self.slot(field, 'EXECUTION', path, EXECUTION)
        if read is None: return 'UNRESOLVED'
        entry, at, value = read
        if value is ABSENT: return 'ABSENT'
        number = self.value(entry, at + '/value')
        self.check('NONNEGATIVE_FINITE_QUANTITY', (entry, at + '/value'),
                   okay=isinstance(number, (int, float)) and not isinstance(number, bool)
                   and math.isfinite(number) and number >= 0)
        self.value(entry, at + '/qualifier')
        if field == 'dose':
            self.check('ACTUAL_PRODUCT_DOSE_ROLE', (entry, at), okay=value.get('parameterRole') in ('DOSE', 'RATE') and value.get('materialRole') == 'PRODUCT')
            if self.product:
                self.check('DOSE_PRODUCT', (entry, at + '/materialRef'), (self.product, '/localSubject/subjectRef'))
            else: self.need('SELECTED_PRODUCT_FOR_DOSE', at)
        self.unit(field, entry, at)
        return 'PRESENT'

    def context(self, entry):
        if not self.shape(entry, OBSERVATION): return False
        self.id_check(entry, 'agronomicObservationContextId')
        self.check('OBSERVATION_TARGET', (entry, '/targetScope'), (self.execution, '/executionExtent/targetScope'))
        for key in ('subjectType', 'subjectRef'):
            self.check('OBSERVATION_' + key.upper(), (entry, '/subject/' + key), (self.claim, '/scope/subject/' + key))
        self.value(entry, '/promotionUse')
        time = entry['record']['phenomenonTime']
        if time.get('timeType') != 'INTERVAL' or time.get('timeBasis') != 'OBSERVED_TIME':
            self.need('UNSUPPORTED_OBSERVATION_TIME_LINK', '/phenomenonTime'); return False
        self.check('OBSERVATION_TIME_START', (entry, '/phenomenonTime/intervalStart'), (self.execution, '/effectiveTimeInterval/start'))
        self.check('OBSERVATION_TIME_END', (entry, '/phenomenonTime/intervalEnd'), (self.execution, '/effectiveTimeInterval/end'))
        return True

    def crop(self, field):
        if field == 'growthStage':
            read = self.slot(field, 'OBSERVATION_CONTEXT', '/phenologyStateBinding', OBSERVATION)
            if read is None: return 'UNRESOLVED'
            entry, at, value = read
            if value is ABSENT: return 'ABSENT'
            self.context(entry)
            okay = (value.get('bindingRole') == 'CROP_STAGE' and value.get('schemeRef') == 'scheme:bbch'
                    and value.get('bindingStatus') == 'EXACT' and bool(value.get('code')) and bool(value.get('schemeVersionRef')))
            if not okay:
                self.need('EXACT_BBCH_STAGE_BINDING', at); return 'UNRESOLVED'
            return 'PRESENT'
        reads = self.use['record']['fieldSelections'][field]['reads']
        if any(read['role'] == 'CROP_BINDING' for read in reads):
            read = self.slot(field, 'CROP_BINDING', '/bindingValue', CODE)
            if read is None: return 'UNRESOLVED'
            entry, at, value = read; record = entry['record']
            self.id_check(entry, 'agronomicIdentityBindingId')
            self.check('CROP_BINDING_ROLE', (entry, '/bindingRole'), okay=record['bindingRole'] == 'CROP_SPECIES')
            self.check('CROP_EXECUTION_LINK', (entry, '/agronomicIdentityBindingId'), (self.execution, '/agronomicIdentityBindingRefs'),
                       okay=entry['binding']['ref'] in self.execution['record'].get('agronomicIdentityBindingRefs', []))
            self.check('CROP_SCOPE', (entry, '/localSubject/scopeRef'), (self.execution, '/executionExtent/targetScope/scopeRef'))
            self.binding_qualifications(entry)
            exact_code = (record['externalScheme']['schemeRef'] == 'scheme:eppo' and bool(record['externalScheme'].get('schemeVersion'))
                          and record['bindingState'] == 'VERIFIED' and value.get('mappingRelation') == 'EXACT' and bool(value.get('code')))
            text = value.get('capturedLabel')
        else:
            read = self.slot(field, 'OBSERVATION_CONTEXT', r'/cropBindings/(?:0|[1-9][0-9]*)', OBSERVATION)
            if read is None: return 'UNRESOLVED'
            entry, at, value = read
            if value is ABSENT: return 'ABSENT'
            self.context(entry)
            exact_code = (value.get('bindingRole') == 'CROP_SPECIES' and value.get('schemeRef') == 'scheme:eppo'
                          and value.get('bindingStatus') == 'EXACT' and bool(value.get('code')) and bool(value.get('schemeVersionRef')))
            text = value.get('capturedLabel')
        if not text and not value.get('code'): return 'ABSENT'
        if not exact_code and not text:
            self.need('CROP_TEXT_OR_SUPPORTED_CODE', at); return 'UNRESOLVED'
        if not exact_code and self.conditions['eppoCode']['disposition'] != 'NOT_REQUIRED':
            self.need('EXACT_EPPO_OR_SUPPORTED_EXCLUSION', at); return 'UNRESOLVED'
        return 'PRESENT'

    def exact_pin(self, owner, path):
        pin = self.value(owner, path)
        if pin is ABSENT: return None
        binding = {'ref': pin['ref'], 'revisionRef': pin['revisionRef']}
        dependency_start = len(self.dependencies)
        selected = self.select(binding, owner, path)
        if selected and selected['rawSha256'] != pin['rawSha256']:
            self.observe_predicate('ADDRESS_RAW_PIN_MISMATCH', False, (owner, path + '/rawSha256'),
                                   depends_on=self.dependencies[dependency_start:])
            self.bad('ADDRESS_RAW_PIN_MISMATCH', path + '/rawSha256', owner)
            return None
        return selected

    def identifier_meaning(self, entry, identifier, allowed):
        if not self.meaning(entry, 'IDENTIFIER_SCHEME_MEANING', per_use=False): return False
        value = self.value(*identifier)
        if not isinstance(value, dict) or not isinstance(value.get('value'), str) or not value['value']:
            self.need('IDENTIFIER_VALUE', identifier[1]); return False
        self.check('IDENTIFIER_SCHEME', (entry, '/scheme'), (identifier[0], identifier[1] + '/scheme'))
        self.check('IDENTIFIER_KIND', (entry, '/identifierKind'), okay=entry['record']['identifierKind'] in allowed)
        scope = {'PERSON_IDENTIFIER': 'SINGLE_PERSON_IN_ISSUER_NAMESPACE', 'PROFESSIONAL_USER_TRAINING_CARD': 'SINGLE_PERSON_IN_ISSUER_NAMESPACE',
                 'HOLDING_IDENTIFIER': 'SINGLE_HOLDING_IN_ISSUER_NAMESPACE', 'LEGAL_PERSON_TAX_IDENTIFIER': 'SINGLE_LEGAL_PERSON_IN_ISSUER_NAMESPACE'}
        self.check('IDENTIFIER_NAMESPACE', (entry, '/identityScope'), okay=entry['record']['identityScope'] == scope[entry['record']['identifierKind']])
        return True

    def person_join(self, address):
        join = self.value(self.use, '/personJoin')
        if self.value(self.use, '/personJoin/method') != 'EXACT_IDENTIFIER_SCHEME_VALUE':
            return self.need('PERSON_JOIN_MEANING', '/personJoin')
        party = self.select(join['professionalUser'], self.use, '/personJoin/professionalUser', PARTY)
        link = self.meaning_list(self.use, '/personJoin/useApplicabilityBasis', 'PERSON_USE_LINK')
        scheme = self.meaning_list(self.use, '/personJoin/schemeMeaningSources', 'IDENTIFIER_SCHEME_MEANING', per_use=False)
        source_id = self.read(self.use, '/personJoin/sourceIdentifier', role='SOURCE_PERSON_JSON')
        party_id = self.read(self.use, '/personJoin/partyIdentifier', role='PROFESSIONAL_USER_PARTY', pattern=r'/registeredIdentifiers/(?:0|[1-9][0-9]*)', schema=PARTY)
        if not all(item is not None for item in (party, link, scheme, source_id, party_id)): return None
        self.id_check(party, 'partyId'); self.person = party
        value = link['record']
        for key, expected in [('professionalUserBinding', party['binding']), ('addressInterpretationBinding', address['binding']),
                              ('sourceAssetBinding', source_id[0]['binding']), ('identifierSchemeBinding', scheme['binding'])]:
            self.check('PERSON_LINK_' + key.upper(), (link, '/' + key), okay=same(value[key], expected))
        self.check('PARTY_IDENTIFIER_SOURCE', (self.use, '/personJoin/partyIdentifier/binding'), okay=same(party_id[0]['binding'], party['binding']))
        self.check('PERSON_IDENTIFIER_POINTER', (link, '/sourceIdentifierPointer'), (self.use, '/personJoin/sourceIdentifier/pointer'))
        self.check('PARTY_IDENTIFIER_POINTER', (link, '/partyIdentifierPointer'), (self.use, '/personJoin/partyIdentifier/pointer'))
        self.check('PERSON_IDENTIFIER_SECTION', (link, '/sourceIdentifierPointer'), okay=value['sourceIdentifierPointer'] == value['sourcePersonPointer'] + '/identifier')
        section = self.value(source_id[0], value['sourcePersonPointer'])
        section_valid = isinstance(section, dict) and set(section) == {'personalName', 'address', 'identifier'}
        self.observe_predicate('PERSON_SECTION_SHAPE', section_valid, (source_id[0], value['sourcePersonPointer']))
        if not section_valid:
            self.bad('PERSON_SECTION_SHAPE', value['sourcePersonPointer'], source_id[0]); return None
        for key in ('personalName', 'address'):
            self.check('PERSON_SECTION_' + key.upper(), (source_id[0], value['sourcePersonPointer'] + '/' + key),
                       okay=isinstance(section[key], str) and bool(section[key]))
        sections = join['personSectionBasis']
        if len(sections) != 1:
            self.need('UNIQUE_PERSON_SECTION_BASIS', '/personJoin/personSectionBasis')
        else:
            selected = self.read(self.use, '/personJoin/personSectionBasis/0', role='SOURCE_PERSON_JSON')
            if selected:
                self.check('PERSON_SECTION_SELECTION', (self.use, '/personJoin/personSectionBasis/0'),
                           okay=same(selected[0]['binding'], source_id[0]['binding']) and selected[1] == value['sourcePersonPointer'])
        self.identifier_meaning(scheme, (source_id[0], source_id[1]), ('PERSON_IDENTIFIER', 'PROFESSIONAL_USER_TRAINING_CARD'))
        for key in ('scheme', 'value'):
            self.check('PERSON_EXACT_IDENTIFIER_' + key.upper(),
                       (source_id[0], source_id[1] + '/' + key), (party_id[0], party_id[1] + '/' + key))
        self.check('EXECUTION_PROFESSIONAL_USER', (self.execution, value['executionPartyField']), (party, '/partyId'))
        if value['addressUseApplicability'] == 'UNKNOWN': self.need('ADDRESS_USE_APPLICABILITY', '/addressUseApplicability')
        else: self.check('ADDRESS_USE_APPLICABILITY', (link, '/addressUseApplicability'), okay=value['addressUseApplicability'] == 'APPLIES_TO_SELECTED_USE')
        return party, link, source_id[0], value['sourcePersonPointer']

    def address_field(self, field):
        name = 'sourcePersonText' if field == 'professionalUserName' else 'addressText'
        read = self.slot(field, 'ADDRESS_INTERPRETATION', '/' + name, ADDRESS)
        if read is None: return 'UNRESOLVED'
        address = read[0]; self.address = address; record = address['record']
        self.id_check(address, 'interpretationId')
        if 'revisionRef' not in address['binding']:
            self.need('EXACT_ADDRESS_INTERPRETATION_REVISION', '/' + name)
        party = self.exact_pin(address, '/professionalUser')
        evidence = self.exact_pin(address, '/sourceEvidence')
        self.exact_pin(address, '/extractionProvenance/methodRevision')
        join_entries = [self.exact_pin(address, '/subjectJoinEvidence/' + str(n)) for n in range(len(record['subjectJoinEvidence']))]
        selected = self.slot(field, 'SOURCE_PERSON_JSON', r'.*')
        if selected is None: return 'UNRESOLVED'
        asset, at, value = selected
        asset_ref_matches = self.check('ADDRESS_ASSET_REF', (address, '/rawAsset/ref'), okay=record['rawAsset']['ref'] == asset['binding']['ref'])
        asset_hash_matches = self.check('ADDRESS_ASSET_RAW_HASH', (address, '/rawAsset/rawSha256'),
                                        okay=record['rawAsset']['rawSha256'] == asset['rawSha256'])
        asset_matches = asset_ref_matches and asset_hash_matches
        if self.value(address, '/extractionProvenance/method') != 'STRUCTURED_FIELD_COPY':
            self.need('UNSUPPORTED_ADDRESS_EXTRACTION_METHOD', '/extractionProvenance/method'); return 'UNRESOLVED'
        locator = 'personLocator' if name == 'sourcePersonText' else 'addressLocator'
        if self.value(address, '/' + locator + '/kind') != 'ORIGINAL_JSON_POINTER':
            self.need('ADDRESS_DOCUMENT_LOCATOR', '/' + locator); return 'UNRESOLVED'
        self.check('ADDRESS_ORIGINAL_POINTER', (address, '/' + locator + '/pointer'), (self.use, '/fieldSelections/' + field + '/reads/' +
                   str(next(n for n,r in enumerate(self.use['record']['fieldSelections'][field]['reads']) if r['role'] == 'SOURCE_PERSON_JSON')) + '/pointer'))
        if asset_matches:
            self.check('ADDRESS_LITERAL_COPY', (address, '/' + name), (asset, at))
        else:
            self.need('ADDRESS_ORIGINAL_COPY_DEPENDENCY', '/rawAsset')
        if evidence and self.shape(evidence, EVIDENCE):
            self.id_check(evidence, 'evidenceRecordId')
            self.check('ADDRESS_EVIDENCE_ASSET_REF', (evidence, '/rawAssetRef'), (address, '/rawAsset/ref'))
            self.check('ADDRESS_EVIDENCE_RAW_DIGEST', (evidence, '/rawAssetDigest'), okay=evidence['record'].get('rawAssetDigest') == 'sha256:' + asset['rawSha256'])
            self.check('ADDRESS_STRUCTURED_LINK', (evidence, '/interpretation/structuredRef'), (address, '/interpretationId'))
            self.check('ADDRESS_INTERPRETATION_CLASS', (evidence, '/interpretation/interpretationClass'), okay=evidence['record'].get('interpretation', {}).get('interpretationClass') == 'STRUCTURED_RECORD')
        if field == 'professionalUserAddress':
            declared = self.slot(field, 'ADDRESS_EVIDENCE', '/interpretation/structuredRef', EVIDENCE)
            if declared and evidence:
                self.check('ADDRESS_EVIDENCE_SELECTION', (declared[0], '/evidenceRecordId'), (evidence, '/evidenceRecordId'))
                self.check('ADDRESS_EVIDENCE_REVISION', (address, '/sourceEvidence'),
                           okay=same(declared[0]['binding'], evidence['binding']))
        temporal = record['sourceTemporalBasis']
        if temporal['posture'] == 'SOURCE_DATE_STATED':
            if temporal['locator']['kind'] == 'ORIGINAL_JSON_POINTER' and asset_matches:
                self.check('ADDRESS_SOURCE_DATE_COPY', (address, '/sourceTemporalBasis/dateText'), (asset, temporal['locator']['pointer']))
            elif temporal['locator']['kind'] != 'ORIGINAL_JSON_POINTER':
                self.need('ADDRESS_SOURCE_DATE_DOCUMENT_LOCATOR', '/sourceTemporalBasis/locator')
        joined = self.person_join(address)
        if joined:
            chosen_party, link, chosen_asset, section = joined
            self.check('ADDRESS_PERSON_SELECTION', (address, '/professionalUser/ref'), (chosen_party, '/partyId'))
            if party:
                self.check('ADDRESS_PARTY_REVISION', (address, '/professionalUser'),
                           okay=same(party['binding'], chosen_party['binding']))
            self.check('ADDRESS_SOURCE_PERSON_SELECTION', (link, '/sourceAssetBinding'), okay=same(chosen_asset['binding'], asset['binding']))
            expected_path = section + ('/personalName' if name == 'sourcePersonText' else '/address')
            self.check('ADDRESS_PERSON_SECTION_FIELD', (address, '/' + locator + '/pointer'), okay=at == expected_path)
            if not any(item is not None and same(item['binding'], link['binding']) for item in join_entries):
                # An unavailable exact revision may contain the selected join.
                # Digest equality alone cannot supply its revision selector.
                if any(item is None for item in join_entries):
                    self.need('ADDRESS_JOIN_EVIDENCE_MEMBERSHIP', '/subjectJoinEvidence')
                else:
                    self.bad('ADDRESS_JOIN_EVIDENCE_MEMBERSHIP', '/subjectJoinEvidence', address)
        return self.text(read)

    def field(self, name):
        if name == 'productName': return self.text(self.product_source(name, '/bindingValue/capturedLabel'))
        if name == 'productAuthorization':
            read = self.product_source(name, '/bindingValue')
            selected = self.slot(name, 'PRODUCT_DECISION_SOURCE', '')
            if read is None or selected is None: return 'UNRESOLVED'
            entry, at, value = read; decision = selected[0]
            if not self.meaning(decision, 'PRODUCT_DECISION_RECORD', per_use=False): return 'UNRESOLVED'
            keys = [key for key in ('registrationRef', 'authorisationRef') if value.get(key)]
            if not keys: return 'ABSENT'
            if len(keys) > 1 and value[keys[0]] != value[keys[1]]:
                self.bad('PRODUCT_DECISION_NUMBER_CONFLICT', at, entry)
            self.check('PRODUCT_DECISION_BINDING', (decision, '/productBinding'), okay=same(decision['record']['productBinding'], entry['binding']))
            self.check('PRODUCT_DECISION_NUMBER', (entry, at + '/' + keys[0]), (decision, '/decisionNumber'))
            self.check('PRODUCT_DECISION_NAME', (entry, '/bindingValue/capturedLabel'), (decision, '/productName'))
            self.check('PRODUCT_SCHEME', (entry, '/externalScheme/schemeRef'), (decision, '/schemeMeaning'))
            self.literal_basis(decision, ('decisionNumber', 'productName', 'issued', 'validUntil'))
            if self.value(entry, '/bindingValue/effectivePeriod') is ABSENT:
                self.need('PRODUCT_BINDING_EFFECTIVE_PERIOD', '/bindingValue/effectivePeriod')
            return 'PRESENT'
        if name in ('useDate', 'startHour'): return self.time(name)
        if name in ('dose', 'treatedArea'): return self.quantity(name)
        if name == 'location':
            target = self.slot(name, 'EXECUTION', '/executionExtent/targetScope', EXECUTION)
            reads = self.use['record']['fieldSelections'][name]['reads']
            role = 'LOCATION_IDENTITY' if any(r['role'] == 'LOCATION_IDENTITY' for r in reads) else 'ALTERNATIVE_LOCATION'
            selected = self.slot(name, role, '')
            available = self.meaning_list(self.use, '/iacsAvailability/basis', 'IACS_AVAILABILITY')
            if target is None or selected is None or available is None: return 'UNRESOLVED'
            entry = selected[0]
            if not self.meaning(entry, 'LOCATION_IDENTIFICATION'): return 'UNRESOLVED'
            for e in (entry, available): self.check('LOCATION_TARGET', (e, '/targetScope'), (self.execution, '/executionExtent/targetScope'))
            self.check('IACS_DISPOSITION', (available, '/availability'), (self.use, '/iacsAvailability/disposition'))
            status = available['record']['availability']
            if status not in ('AVAILABLE', 'UNAVAILABLE'):
                if status == 'CONFLICTED': self.bad('CONFLICTED_IACS_AVAILABILITY', '/availability', available)
                self.need('LOCATION_IDENTIFICATION_PRECEDENCE', '/iacsAvailability'); return 'UNRESOLVED'
            self.check('LOCATION_METHOD_PRECEDENCE', (entry, '/method'), okay=entry['record']['method'] == ('IACS_GERK' if status == 'AVAILABLE' else 'ARTICLE_1_2'))
            if status == 'AVAILABLE': self.check('GERK_SCHEME', (entry, '/scheme'), okay=entry['record']['scheme'] == 'SI:GERK')
            self.literal_basis(entry, ('targetScope', 'identifier', 'scheme'))
            return 'PRESENT'
        if name == 'treatedFraction':
            read = self.slot(name, 'EXECUTION', '/executionExtent', EXECUTION)
            if read is None: return 'UNRESOLVED'
            if read[2]['extentClass'] == 'WHOLE_TARGET_SCOPE': return 'ABSENT'
            if read[2]['extentClass'] != 'PARTIAL_TARGET_SCOPE':
                self.need('UNSUPPORTED_FRACTION_MEANING', read[1]); return 'UNRESOLVED'
            extent = self.slot(name, 'PARTIAL_EXTENT', '', PARTIAL)
            if extent is None: return 'UNRESOLVED'
            e = extent[0]
            self.check('PARTIAL_EXTENT_ID', (e, '/partialExtentId'), (self.execution, '/executionExtent/extentRef'))
            self.check('PARTIAL_PARENT_SCOPE', (e, '/parentScope'), (self.execution, '/executionExtent/targetScope'))
            time = e['record']['temporalApplicability']
            if time.get('timeType') != 'INTERVAL' or time.get('timeBasis') != 'EXECUTION_INTERVAL':
                self.need('PARTIAL_EXTENT_TIME_MEANING', '/temporalApplicability')
            else:
                self.check('PARTIAL_TIME_START', (e, '/temporalApplicability/intervalStart'), (self.execution, '/effectiveTimeInterval/start'))
                self.check('PARTIAL_TIME_END', (e, '/temporalApplicability/intervalEnd'), (self.execution, '/effectiveTimeInterval/end'))
            return 'PRESENT'
        if name in ('cropSituation', 'growthStage'): return self.crop(name)
        if name in ('professionalUserName', 'professionalUserAddress'): return self.address_field(name)
        if name == 'holdingOrLegalIdentifier':
            selected = self.slot(name, 'HOLDING_OR_LEGAL_PARTY', r'/registeredIdentifiers/(?:0|[1-9][0-9]*)', PARTY)
            link_read = self.slot(name, 'HOLDING_OR_LEGAL_IDENTITY', '')
            if selected is None or link_read is None: return 'UNRESOLVED'
            party, at, value = selected; link = link_read[0]
            if not self.meaning(link, 'HOLDING_LEGAL_PERSON_LINK'): return 'UNRESOLVED'
            self.id_check(party, 'partyId')
            self.check('HOLDING_OWNER', (link, '/ownerBinding'), okay=same(link['record']['ownerBinding'], party['binding']))
            self.check('HOLDING_IDENTIFIER_POINTER', (link, '/identifierPointer'), okay=link['record']['identifierPointer'] == at)
            self.check('HOLDING_SCOPE', (link, '/recordAnchorScope'), (self.execution, '/anchorScopes'),
                       okay=link['record']['recordAnchorScope'] in self.execution['record']['anchorScopes'])
            scheme = self.select(link['record']['identifierSchemeBinding'], link, '/identifierSchemeBinding')
            if scheme:
                self.identifier_meaning(scheme, (party, at), ('HOLDING_IDENTIFIER', 'LEGAL_PERSON_TAX_IDENTIFIER'))
                if scheme['record'].get('identifierKind') == 'HOLDING_IDENTIFIER':
                    self.check('HOLDING_SCHEME', (scheme, '/scheme'), okay=scheme['record']['scheme'] == 'SI:KMG-MID')
            return 'ABSENT' if value is ABSENT or not value.get('value') else 'PRESENT'
        if name == 'trainingCard':
            selected = self.slot(name, 'PROFESSIONAL_USER_PARTY', r'/registeredIdentifiers/(?:0|[1-9][0-9]*)', PARTY)
            scheme_read = self.slot(name, 'TRAINING_SOURCE', '')
            if selected is None or scheme_read is None: return 'UNRESOLVED'
            party, at, value = selected
            if not self.person: self.need('SELECTED_PROFESSIONAL_USER', at)
            else:
                self.check('TRAINING_CARD_PERSON', (party, '/partyId'), (self.person, '/partyId'))
                self.check('TRAINING_CARD_PARTY_REVISION', (self.use, '/fieldSelections/trainingCard'),
                           okay=same(party['binding'], self.person['binding']))
            scheme = scheme_read[0]
            self.identifier_meaning(scheme, (party, at), ('PROFESSIONAL_USER_TRAINING_CARD',))
            self.check('TRAINING_CARD_SCHEME', (scheme, '/scheme'), okay=scheme['record'].get('scheme') == 'SI:FFS-IZKAZNICA')
            return 'ABSENT' if value is ABSENT or not value.get('value') else 'PRESENT'
        if name == 'equipment':
            selected = self.slot(name, 'EXECUTION', '/equipment', EXECUTION)
            if selected is None: return 'UNRESOLVED'
            if selected[2] is ABSENT or not selected[2].get('equipmentRef'): return 'ABSENT'
            source = self.slot(name, 'EQUIPMENT_SOURCE', '')
            if source is None or not self.meaning(source[0], 'EQUIPMENT_USE_EVIDENCE'): return 'UNRESOLVED'
            self.check('EQUIPMENT_USE_REF', (source[0], '/equipmentRef'), (self.execution, '/equipment/equipmentRef'))
            self.literal_basis(source[0], ('equipmentRef', 'inspectionStickerNumber', 'inspectionValidUntil'))
            return 'PRESENT'
        raise ValueError('Unknown fixed C17 field.')

    def run(self):
        body = self.atom['body']
        rules = self.select(body['requirementsRevision'], self.claim, '/body/requirementsRevision')
        if rules is None: return self.result()
        if rules['rawSha256'] != PINS['rules.v0_1.json'] or not same(rules['record'], self.rules):
            self.bad('UNSUPPORTED_RULE_REVISION', '/body/requirementsRevision', self.claim); return self.result()
        candidates = distinct_selected_originals([entry for entry in self.sources if 'selectorMapping' in entry
            and predicate_value(entry, '', isinstance(entry['record'], dict), 'SI_C17_USE_SELECTION')
            and predicate_value(entry, '/schemaVersion', entry['record'].get('schemaVersion'), 'SI_C17_USE_SELECTION') == 'ofarm.siC17PerUseSourceInterpretation.v0.1'
            and same(predicate_value(entry, '/recordBinding', entry['record'].get('recordBinding'), 'SI_C17_USE_SELECTION'), body['record'])])
        selection('SI_C17_USE_SELECTION', self.sources, candidates,
                  origins=[origin(self.claim['id'], '/definition'), origin(self.claim['id'], '/body/record')])
        if len(candidates) != 1:
            self.need('UNIQUE_PER_USE_INTERPRETATION', '/body/record')
            if len(candidates) > 1: self.bad('AMBIGUOUS_PER_USE_INTERPRETATION', '/body/record', self.claim)
            return self.result()
        self.use = self.select(candidates[0]['binding'], self.claim, '/body/record', USE)
        if self.use is None: return self.result()
        self.id_check(self.use, 'interpretationId')
        self.check('SELECTED_REQUIREMENTS', (self.use, '/requirementsBinding'), (self.claim, '/body/requirementsRevision'))
        self.check('SELECTED_RECORD', (self.use, '/recordBinding'), (self.claim, '/body/record'))
        self.check('SELECTED_SCOPE', (self.use, '/scope'), (self.claim, '/scope'))
        self.execution = self.select(body['record'], self.claim, '/body/record', EXECUTION)
        if self.execution is None: return self.result()
        self.id_check(self.execution, 'executionRecordPayloadId')
        self.check('ACTUAL_USE_TARGET_REF', (self.execution, '/executionExtent/targetScope/scopeRef'), (self.claim, '/scope/subject/subjectRef'))
        self.check('ACTUAL_USE_TARGET_TYPE', (self.execution, '/executionExtent/targetScope/scopeType'), (self.claim, '/scope/subject/subjectType'))
        use_errors, use_missing = len(self.errors), len(self.missing)
        use = self.meaning_list(self.use, '/useType/basis', 'USE_CLASSIFICATION')
        if use:
            self.check('USE_CLASSIFICATION', (use, '/classification'), (self.use, '/useType/classification'))
            self.check('CLAIM_USE_CLASSIFICATION', (use, '/classification'), (self.claim, '/body/useType'))
        if not use or use['record']['classification'] != 'SURFACE_AREA':
            self.need('SUPPORTED_SURFACE_AREA_USE', '/useType')
        self.supported_use = bool(use and use['record']['classification'] == 'SURFACE_AREA'
                                  and len(self.errors) == use_errors and len(self.missing) == use_missing)
        # Product is selected before applicability, whose product link is independent.
        self.current = 'productName'; self.product_source('productName', '/bindingValue/capturedLabel')
        for field in self.use['record']['conditionalRequirements']:
            self.condition(field)
        for rule in self.rules['fieldRules']:
            name = rule['field']; self.current = name; selector_scope(self.atom['atomId'] + ':' + name)
            error_start, missing_start = len(self.errors), len(self.missing)
            allowed = {route['role'] for route in rule['originalRoutes']}
            for n, read in enumerate(self.use['record']['fieldSelections'][name]['reads']):
                if self.value(self.use, '/fieldSelections/' + name + '/reads/' + str(n) + '/role') not in allowed:
                    self.bad('UNSUPPORTED_FIELD_SOURCE_ROLE', '/fieldSelections/' + name + '/reads/' + str(n), self.use)
            roles = [read['role'] for read in self.use['record']['fieldSelections'][name]['reads']]
            alternatives = ({'CROP_BINDING', 'OBSERVATION_CONTEXT'} if name == 'cropSituation'
                            else {'LOCATION_IDENTITY', 'ALTERNATIVE_LOCATION'} if name == 'location' else set())
            if len(alternatives.intersection(roles)) > 1:
                self.bad('AMBIGUOUS_ALTERNATIVE_SOURCE_ROUTE', '/fieldSelections/' + name, self.use)
            state = self.field(name)
            condition = self.conditions.get(name, {'disposition': 'REQUIRED', 'remainingRoles': []})
            if state == 'ABSENT':
                if condition['disposition'] == 'NOT_REQUIRED': state = 'SATISFIED_EXCLUSION'
                elif condition['disposition'] == 'REQUIRED': state = 'MISSING_REQUIRED'
                else:
                    state = 'UNRESOLVED'; self.missing.extend(condition['remainingRoles'])
                    self.need('CONDITIONAL_FIELD_RELEVANCE', '/fieldSelections/' + name)
            elif state == 'PRESENT': state = 'SATISFIED'
            if len(self.missing) > missing_start: state = 'UNRESOLVED'
            if len(self.errors) > error_start or condition['disposition'] == 'CONFLICTED': state = 'CONTRADICTORY'
            self.fields[name] = {'state': state, 'requirement': condition['disposition'],
                                 'sourceRequirement': rule['requirement']}
        return self.result()

    def result(self):
        states = [value['state'] for value in self.fields.values()]
        if self.supported_use and 'MISSING_REQUIRED' in states: outcome = 'INCOMPLETE_FOR_RECORDKEEPING'
        elif len(states) == 15 and all(state in ('SATISFIED', 'SATISFIED_EXCLUSION') for state in states) and not self.errors and not self.missing:
            outcome = 'COMPLETE_FOR_RECORDKEEPING'
        else: outcome = 'INDETERMINATE'
        if self.use is not None and outcome != 'INDETERMINATE':
            self.current = 'outcome'
            outcome_guard = guard('SI_C17_DERIVED_FIELD_AGGREGATION', True, depends_on=self.dependencies)
            self.check('ALLEGED_OUTCOME', (self.use, ''), (self.claim, '/body/allegedOutcome'),
                       okay=outcome == self.atom['body']['allegedOutcome'],
                       depends_on=[outcome_guard] if outcome_guard is not None else [])
        return {'scope': 'CONDITIONAL_SI_C17_RECORD_COMPLETENESS',
                'disposition': 'FAIL' if self.errors else 'NOT_EVALUATED' if self.missing else 'PASS',
                'errors': self.errors, 'remainingRoles': self.missing, 'comparisons': self.comparisons,
                'sourceInputIds': sorted(set(self.ids)), 'requiredReferences': self.refs,
                'conditionalReportedOutcome': outcome, 'fieldResults': self.fields,
                'conditionalRequirements': self.conditions,
                'qualification': 'Bounded agreement under reviewed generic SI rules and supplied independent originals only. No source authentication, live identity, evidence-use admission, current lawful use, C4 acceptance or publication readiness.',
                'liveC4': 'GATED', 'publication': 'GATED'}


@reader('si_c17_sources.py', ['AR_BODY'])
def evaluate(atom, sources, schemas, evidence_bindings):
    register(schemas)
    return _C17(atom, sources, schemas, evidence_bindings).run()
