"""Bounded nested source occurrences from checked, selected JSON originals.

Only explicit candidate reader rules below are traversed. The selection and
admitted values come from original_inputs.bind_roots, never an offered state
read list. These rows retain obligations and unresolved owner decisions.
Selected parent schemas are checked where the pinned reader requires them;
complete reader recursion and immutable input closure remain open.
"""

from collections import defaultdict
from pathlib import Path
import sys

from strict_inputs import InputError, canonical, digest, parse, pointer as json_pointer, safe_path, same, sha
from event_definition_inputs import CASES, SCHEMAS as EVENT_SCHEMAS
from work_definition_inputs import SCHEMAS as WORK_SCHEMAS
from sample_collection_definitions import SCHEMAS as O10_OUTPUT_SCHEMAS
from analysis_output_definitions import SCHEMAS as O22_OUTPUT_SCHEMAS
from definition_inputs import SCHEMAS as DOMAIN_SCHEMAS
from condition_sources import (condition_reader_kind, resolve_condition_inputs,
                               condition_property_comparisons, condition_linked_reader,
                               condition_scope_checks, evaluate_preoperand,
                               condition_operand_source_request, evaluate_precriterion,
                               condition_criterion_binding_origins, condition_required_unit,
                               condition_activity_quantity_kind, condition_activity_operator,
                               condition_activity_predicate_kind,
                               condition_activity_threshold_decimal,
                               condition_activity_threshold_qualifier)
from criterion_sources import evaluate_traced as evaluate_criterion_traced
from sample_relation_sources import evaluate_traced as evaluate_sample_relation_traced
from sample_collection_sources import resolve_collection_inputs, resolve_collection_analysis
from drying_sources import (resolve_drying_specification, drying_target_parameters,
                            drying_target_has_basis, drying_term_inputs)
from irrigation_sources import irrigation_initial_inputs, irrigation_named_condition_inputs
from sanitation_sources import (sanitation_initial_inputs, sanitation_named_condition_inputs,
                                read_sanitation_duration_unit)
from analysis_output_sources import resolve_analysis_inputs
from observation_acquisition_sources import (resolve_acquisition_inputs,
                                             resolve_acquisition_extent,
                                             acquisition_observation_inputs)
from work_sources import (WORK_CLAIM_VALUE_RULES, WORK_CONDITION_GROUPS,
                          WORK_EXECUTION_STAGES, carrier_meaning_checks,
                          condition_parent_expectations, condition_at_stage, work_performer_pointer,
                          work_time_basis_selection, actual_carrier_comparisons)


HERE = Path(__file__).resolve().parent
WORK_VERSION = 'ofarm.assertionDomainWorkSpecificationDefinition.v0.1'
SAMPLE_OUTPUT_VERSIONS = {
    'O10': 'ofarm.assertionDomainSampleCollectionSpecification.v0.1',
    'O22': 'ofarm.assertionDomainAnalysisOutputSpecification.v0.1',
}
SAMPLE_RELATION_VERSION = 'ofarm.assertionDomainSampleTargetRelationUseDefinition.v0.1'
EVENT_USE_VERSION = 'ofarm.assertionDomainEventUseDefinition.v0.1'
EVENT_VOCABULARY_VERSION = 'ofarm.assertionDomainEventVocabularyDefinition.v0.1'
EVENT_PACK_VERSION = 'ofarm.assertionDomainEventMeaningPackDefinition.v0.1'
REVIEWED_CONDITION_PATH = (
    'package_meta/history/clean_baseline_migration/phase_reports/'
    'domain_contract_verifier_delivery_v0_1/reviewed-input/domain/'
    'work-condition-definitions.json')
REVIEWED_CONDITION_SHA256 = '3334642f506968c8970945bd27be3b569946e5453b75757af31f32e61064dd11'
REVIEWED_CONDITION_COMMIT = '389a8f6b6bb2f43435c35f32df769e723d736856'
OPERATION_CARRIER_SCHEMA_PATH = 'outer/carriers/result.schema.json'
OPERATION_SOURCE_SCHEMAS = {
    'intent': ('https://ofarm.dev/schema/interventionintentpayload/v0.1',
               'interventionIntentPayloadId'),
    'execution': ('https://ofarm.dev/schema/executionrecordpayload/v0.1',
                  'executionRecordPayloadId'),
}


def _binding(value):
    return (isinstance(value, dict)
            and set(value) in ({'ref', 'digest'}, {'ref', 'revisionRef'})
            and all(isinstance(v, str) and v for v in value.values()))


def _candidate_schema_status(schema, value, role):
    """Validate against an exact candidate schema and its pinned local closure."""
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource

        resources = (
            HERE / 'outer/payload-schema.json',
            HERE / 'components/revision-02/sources/OFARM/389a8f6b6bb2'
            / '03_machine_contracts/drafts_non_default/assertion_record_submission'
            / 'OFARM_AssertionRecord_schema_v0_2.json',
            HERE / 'components/revision-02/proposition.schema.json',
            HERE / 'components/revision-02/owned-value-types-amendment.schema.json',
        )
        registry = Registry()
        for path in resources:
            document = parse(path.read_bytes())
            registry = registry.with_resource(document['$id'],
                                              Resource.from_contents(document))
        errors = list(Draft202012Validator(
            schema, registry=registry).iter_errors(value))
        return ('PASS', None) if not errors else ('FAIL', role + '_SOURCE_SCHEMA_INVALID')
    except Exception:
        # An unavailable dependency/schema never enables the next read edge.
        return 'NOT_EVALUATED', role + '_SOURCE_SCHEMA_CHECK_UNAVAILABLE'


def _event_schema_status(kind, value):
    return _candidate_schema_status(EVENT_SCHEMAS[kind], value, 'EVENT')


def _condition_source_schemas():
    """Use the actual reader's pinned schema registry and strict timestamps."""
    component_root = str(HERE / 'components/revision-02')
    if component_root not in sys.path:
        sys.path.insert(0, component_root)
    from runtime_support import Schemas
    from importlib import import_module
    schemas = Schemas()
    schemas.definition_source_modules = {}
    for name in ('definition_inputs', 'work_definition_inputs', 'analysis_output_definitions',
                 'observation_acquisition_definitions', 'sample_collection_definitions',
                 'drying_definitions', 'irrigation_definitions', 'sanitation_definitions'):
        module = import_module(name)
        module.register(schemas)
        schemas.definition_source_modules.update({value['$id']: name + '.py' for value in module.SCHEMAS.values()})
    return schemas


def _specific_activity_status(row_id, value):
    """Check the used claim field against its exact candidate row constant."""
    try:
        schema = parse((HERE / 'components/revision-02/proposition.schema.json').read_bytes())
        field = schema['$defs'][row_id]['properties']['body']['properties'][
            'parameters']['properties']['specificActivity']
        expected = field['const']
        if not isinstance(expected, str):
            return 'NOT_EVALUATED'
        return 'PASS' if isinstance(value, str) and value == expected else 'FAIL'
    except (OSError, InputError, KeyError, TypeError):
        return 'NOT_EVALUATED'


def _operation_carrier_wrapper_status(kind, value):
    """Check the complete declaration against the exact candidate carrier def."""
    try:
        from jsonschema import Draft202012Validator
        document = parse((HERE / OPERATION_CARRIER_SCHEMA_PATH).read_bytes())
        name = ('interventionIntentPayloadBinding' if kind == 'intent'
                else 'executionRecordPayloadBinding')
        schema = {'$schema': document['$schema'], '$defs': document['$defs'],
                  '$ref': '#/$defs/' + name}
        errors = list(Draft202012Validator(schema).iter_errors(value))
        return ('PASS', None) if not errors else (
            'FAIL', 'OPERATION_CARRIER_DECLARATION_SCHEMA_INVALID')
    except Exception:
        return 'NOT_EVALUATED', 'OPERATION_CARRIER_DECLARATION_SCHEMA_UNAVAILABLE'


def _operation_carrier_record_status(kind, value, schemas, pin):
    """Use the sealed component's current pinned source registry and timestamps."""
    try:
        if pin is None or schemas is None:
            return 'NOT_EVALUATED', 'OPERATION_CARRIER_SOURCE_SCHEMA_UNAVAILABLE'
        schema_id = OPERATION_SOURCE_SCHEMAS[kind][0]
        source_schema = parse((HERE / pin['localPath']).read_bytes())
        if schemas.schemas.get(schema_id) != source_schema:
            return 'NOT_EVALUATED', 'OPERATION_CARRIER_SOURCE_SCHEMA_UNAVAILABLE'
        errors = schemas.errors(schema_id, value)
        if any(item['code'] in {'SCHEMA_NOT_IN_PINNED_REGISTRY',
                                'SCHEMA_RESOLUTION_ERROR'} for item in errors):
            return 'NOT_EVALUATED', 'OPERATION_CARRIER_SOURCE_SCHEMA_UNAVAILABLE'
        return ('PASS', None) if not errors else (
            'FAIL', 'OPERATION_CARRIER_SOURCE_SCHEMA_INVALID')
    except Exception:
        return 'NOT_EVALUATED', 'OPERATION_CARRIER_SOURCE_SCHEMA_UNAVAILABLE'


def _operation_carrier_source_schema_pin(kind):
    """Name the current reviewed schema bytes used by the sealed registry."""
    filename = ('OFARM_InterventionIntentPayload_schema_v0_1.json'
                if kind == 'intent' else
                'OFARM_ExecutionRecordPayload_schema_v0_1.json')
    component_root = HERE / 'components/revision-02'
    pins = parse((component_root / 'source-pins.json').read_bytes())['sources']
    matches = [pin for pin in pins
               if pin.get('id') == 'CURRENT:' + filename.removesuffix('.json')]
    if len(matches) != 1:
        return None
    pin = matches[0]
    try:
        raw = safe_path(component_root, pin['localPath']).read_bytes()
    except (OSError, InputError, KeyError, TypeError):
        return None
    if sha(raw) != pin.get('sha256'):
        return None
    try:
        schema = parse(raw)
        schema_id = schema['$id']
        schema_version = schema['properties']['schemaVersion']['const']
    except (InputError, KeyError, TypeError):
        return None
    return {'repository': pin['repository'], 'commit': pin['commit'],
            'originalPath': pin['originalPath'],
            'localPath': 'components/revision-02/' + pin['localPath'],
            'rawSha256': pin['sha256'], 'schemaId': schema_id,
            'schemaVersion': schema_version}


def _reviewed_condition_table():
    """Load the exact reviewed rule input through its candidate source pin."""
    try:
        root = HERE / 'components/revision-02'
        pins = parse((root / 'source-pins.json').read_bytes())['sources']
        selected = [pin for pin in pins
                    if (pin.get('originalPath') == REVIEWED_CONDITION_PATH
                        and pin.get('commit') == REVIEWED_CONDITION_COMMIT
                        and pin.get('repository') == 'samovers/OFARM')]
        if len(selected) != 1:
            return None
        pin = selected[0]
        raw = safe_path(root, pin['localPath']).read_bytes()
        if sha(raw) != pin['sha256'] or sha(raw) != REVIEWED_CONDITION_SHA256:
            return None
        document = parse(raw)
        if not isinstance(document, dict) or not isinstance(document.get('rows'), list):
            return None
        return document['rows']
    except (OSError, InputError, KeyError, TypeError, ValueError):
        return None


def _pointer_token(value):
    return value.replace('~', '~0').replace('/', '~1')


def derive(bound, requirements, uses):
    """Add exact operation/work/sample/event positions and explicit frontiers.

    The reader modules are candidate rules pinned by the #47 package. A field
    is traversed only after its source original is byte-matched, JSON-admitted
    and exactly nominated. Parent shapes and stopping guards follow the pinned
    reader; identity contradictions remain visible where that reader continues.
    Each child retains its actual parent original input ID and JSON pointer.
    """
    by_ref = bound['pinsByRef']
    by_id = bound['pinsById']
    results = bound['inventoryResults']
    admitted = bound['admittedJson']
    selected_index = {pin['inputId']: index
                      for index, pin in enumerate(bound['selection']['originalSelections'])}
    rule_hashes = {name: sha((HERE / name).read_bytes()) for name in
                   ('work_sources.py', 'condition_sources.py', 'criterion_sources.py', 'sample_relation_sources.py',
                    'analysis_output_sources.py', 'observation_acquisition_sources.py',
                    'sample_collection_sources.py', 'drying_sources.py',
                    'irrigation_sources.py', 'sanitation_sources.py',
                    'event_definition_inputs.py', 'source_derivation.py',
                    'components/revision-02/operation_adapters.py',
                    'condition_property_resolution.py')}
    definition_registry_raw = (HERE / 'domain-definitions.json').read_bytes()
    canonical_cases = [row for row in parse(definition_registry_raw)['definitions']
                       if row['id'] in CASES]
    nominations = defaultdict(list)
    for row in requirements:
        if (row['id'].startswith('selected-source:') and row['disposition'] == 'PASS'
                and len(row['inputIds']) == 1):
            nominations[canonical(row['selectedBinding'])].append(row)
        elif (row.get('kind') == 'CANDIDATE_CLAIM_SOURCE_OCCURRENCE'
              and row.get('structuralSelection') == 'PASS'
              and len(row['inputIds']) == 1):
            nominations[canonical(row['selectedBinding'])].append(row)
    rows, frontiers, expanded, event_roots, carrier_selections = [], [], [], [], []
    carrier_schema_cache = {'attempted': False, 'schemas': None}
    actual_carrier_cache = {'attempted': False, 'adapter': None}
    condition_schema_cache = {'attempted': False, 'schemas': None}
    carrier_schema_pins = {}

    def carrier_schema_pin(kind):
        if kind not in carrier_schema_pins:
            carrier_schema_pins[kind] = _operation_carrier_source_schema_pin(kind)
        return carrier_schema_pins[kind]

    def carrier_schema_status(kind, value, pin):
        if not carrier_schema_cache['attempted']:
            carrier_schema_cache['attempted'] = True
            try:
                component_root = str(HERE / 'components/revision-02')
                if component_root not in sys.path:
                    sys.path.insert(0, component_root)
                from runtime_support import Schemas
                carrier_schema_cache['schemas'] = Schemas()
            except Exception:
                carrier_schema_cache['schemas'] = None
        return _operation_carrier_record_status(
            kind, value, carrier_schema_cache['schemas'], pin)

    def frontier(role, input_id, pointer, reason, triggering_id=None):
        frontiers.append({'role': role, 'origin': {'inputRole': input_id,
                                                  'pointer': pointer},
                          'reason': reason,
                          **({'triggeringRequirementId': triggering_id}
                             if triggering_id is not None else {})})

    def selected_record(binding, role, origin_id, pointer, triggering_id, *, object_only=True):
        """Return only an exactly nominated, matched JCS original value."""
        if not _binding(binding):
            frontier(role, origin_id, pointer, 'MALFORMED_SOURCE_BINDING', triggering_id)
            return None
        pin = by_ref.get(binding['ref'])
        if pin is None:
            frontier(role, origin_id, pointer, 'SELECTED_ORIGINAL_MISSING', triggering_id)
            return None
        iid = pin['inputId']
        if pin['digestMode'] != 'JCS_JSON':
            frontier(role, origin_id, pointer, 'RAW_BYTES_OPAQUE', triggering_id)
            return None
        if results[iid]['status'] != 'MATCHED':
            frontier(role, origin_id, pointer, 'SELECTED_ORIGINAL_NOT_MATCHED', triggering_id)
            return None
        if binding != {'ref': pin['ref'], 'digest': pin['wholeJcsDigest']}:
            read_row = next((row for row in requirements if row['id'] == triggering_id), {})
            fact = next((row for row in requirements
                         if row['id'] == read_row.get('conditionPropertyResolutionId')), None)
            if (fact is not None and fact['disposition'] == 'PASS'
                    and read_row['origin'] == {'inputRole': origin_id, 'pointer': pointer}
                    and read_row['role'] == role and pointer == '/propertyBinding'
                    and role in {'WORK_CONDITION_PROPERTY_DEFINITION', 'CRITERION_OBSERVED_PROPERTY_DEFINITION'}):
                from condition_property_resolution import resolve_method
                resolved = resolve_method(bound, origin_id, binding)
                if (resolved and resolved['disposition'] == 'PASS'
                        and resolved['propertyInputId'] == iid
                        and same({key: value for key, value in resolved.items() if key != 'entry'},
                                 fact['sourceResolution'])):
                    return iid, admitted[iid]
            frontier(role, origin_id, pointer,
                     'SOURCE_DIGEST_OR_REVISION_RULE_PENDING', triggering_id)
            return None
        if not any(iid in row['inputIds'] for row in nominations[canonical(binding)]):
            frontier(role, origin_id, pointer,
                     'EXACT_INDEPENDENT_SOURCE_NOMINATION_MISSING', triggering_id)
            return None
        value = admitted.get(iid)
        if iid not in admitted or object_only and not isinstance(value, dict):
            frontier(role, origin_id, pointer, 'ADMITTED_JSON_OBJECT_UNAVAILABLE', triggering_id)
            return None
        return iid, value

    def emit(parent_id, origin_id, pointer, binding, role, module, rule_name,
             finding_id='AR_BODY', *, allow_unpinned=False,
             unpinned_reason='SOURCE_USE_RULE_PENDING',
             additional_dependencies=(), edge_class='REQUIRED_ORIGINAL_READ',
             condition_property=False):
        resolution = resolution_id = None
        if (condition_property and pointer == '/propertyBinding'
                and role in {'WORK_CONDITION_PROPERTY_DEFINITION', 'CRITERION_OBSERVED_PROPERTY_DEFINITION'}
                and isinstance(binding, dict) and 'revisionRef' in binding):
            from condition_property_resolution import resolve_method
            resolution = resolve_method(bound, origin_id, binding)
            if resolution is not None:
                resolution_id = 'nested-source:' + str(len(rows))
                source_nominations = [item['id'] for item in requirements
                    if item['id'].startswith('selected-source:') and item.get('selectedBinding') == binding]
                resolution_dependencies = list(dict.fromkeys([parent_id, *additional_dependencies,
                    *('selected-original:' + str(selected_index[iid]) for iid in resolution['inputIds']),
                    *source_nominations]))
                resolution_rule = {'module': 'condition_property_resolution.py',
                    'moduleRawSha256': rule_hashes['condition_property_resolution.py'],
                    'rule': 'EXPLICIT_CONDITION_PROPERTY_REVISION', 'sourcePointer': pointer,
                    'coreManifestRawSha256': resolution['coreManifestRawSha256']}
                fact = {'id': resolution_id, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
                    'role': 'CONDITION_PROPERTY_REVISION_RESOLUTION', 'edgeClass': 'COMPARISON_VALUE',
                    'origin': {'inputRole': origin_id, 'pointer': pointer},
                    'rule': resolution_rule, 'selectedBinding': binding,
                    'inputIds': resolution['inputIds'], 'dependsOn': resolution_dependencies,
                    'findingIds': [finding_id], 'disposition': resolution['disposition'],
                    'structuralSelection': resolution['disposition'],
                    'observations': resolution['observations'],
                    'sourceResolution': {key: value for key, value in resolution.items() if key != 'entry'},
                    'diagnostics': resolution['diagnostics'], 'qualification': resolution['qualification']}
                requirements.append(fact)
                rows.append({'requirementId': resolution_id, 'useId': None,
                    'origin': fact['origin'], 'rule': resolution_rule, 'role': fact['role'],
                    'edgeClass': 'COMPARISON_VALUE', 'selectedBinding': binding,
                    'selectedInputId': resolution['propertyInputId'], 'selectedOriginal': None,
                    'dependsOn': resolution_dependencies, 'disposition': resolution['disposition']})
        index = len(rows)
        rid = 'nested-source:' + str(index)
        valid = _binding(binding)
        pin = by_ref.get(binding['ref']) if valid else None
        iid = pin['inputId'] if pin is not None else None
        nomination_rows = nominations[canonical(binding)] if valid else []
        matching_nominations = [row for row in nomination_rows
                                if iid is not None and iid in row['inputIds']]
        dependencies = [parent_id, *additional_dependencies]
        if resolution_id is not None:
            dependencies.append(resolution_id)
        if iid is not None:
            dependencies.append('selected-original:' + str(selected_index[iid]))
        # A sourceSelections nomination is a separate exact mapping. Direct
        # claim occurrences are already represented by the parent dependency.
        dependencies.extend(row['id'] for row in matching_nominations
                            if row['id'].startswith('selected-source:'))
        if not valid:
            structural, reason = 'FAIL', 'MALFORMED_NESTED_SOURCE_BINDING'
        elif pin is None:
            structural, reason = ('NOT_EVALUATED' if allow_unpinned else 'FAIL'), \
                                 (unpinned_reason if allow_unpinned
                                  else 'NESTED_ORIGINAL_NOT_IN_INDEPENDENT_SELECTION')
        elif results[iid]['status'] == 'MISMATCH':
            structural, reason = 'FAIL', 'NESTED_SELECTED_ORIGINAL_MISMATCH'
        elif results[iid]['status'] == 'NOT_EVALUATED':
            structural, reason = 'NOT_EVALUATED', 'NESTED_SELECTED_ORIGINAL_UNAVAILABLE'
        elif pin['digestMode'] == 'RAW_BYTES':
            structural, reason = 'NOT_EVALUATED', 'RAW_BYTES_SOURCE_USE_RULE_PENDING'
        elif resolution is not None:
            structural = 'PASS' if resolution['disposition'] == 'PASS' else 'NOT_EVALUATED'
            reason = ('MATCHED_CONTEXTUAL_CONDITION_PROPERTY_ORIGINAL' if structural == 'PASS'
                      else 'CONDITION_PROPERTY_RESOLUTION_' + resolution['disposition'])
        elif binding != {'ref': pin['ref'], 'digest': pin['wholeJcsDigest']}:
            structural, reason = 'NOT_EVALUATED', 'SOURCE_DIGEST_OR_REVISION_RULE_PENDING'
        elif not matching_nominations:
            structural, reason = 'NOT_EVALUATED', 'EXACT_SOURCE_NOMINATION_PENDING'
        else:
            structural, reason = 'PASS', 'MATCHED_SELECTED_JSON_ORIGINAL_ONLY'
        if edge_class != 'REQUIRED_ORIGINAL_READ' and structural == 'FAIL':
            # A comparison value or conditional position cannot establish an
            # independent read failure before its applicability rule does.
            structural = 'NOT_EVALUATED'
            reason = 'NON_REQUIRED_POSITION_' + reason
            frontier(role, origin_id, pointer, reason, rid)
        disposition = 'FAIL' if structural == 'FAIL' else 'NOT_EVALUATED'
        rule = {'module': module, 'moduleRawSha256': rule_hashes[module],
                'rule': rule_name, 'sourcePointer': pointer}
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': role, 'edgeClass': edge_class,
               'origin': {'inputRole': origin_id, 'pointer': pointer},
               'rule': rule, 'selectedBinding': binding,
               'inputIds': [iid] if iid is not None else [],
               'dependsOn': dependencies, 'findingIds': [finding_id],
               'structuralSelection': structural, 'disposition': disposition,
               'diagnostics': [{'code': reason}],
               'qualification': 'Exact candidate reader field occurrence only; owner selector, admission, revision and protected treatment remain open.'}
        if resolution_id is not None:
            row['conditionPropertyResolutionId'] = resolution_id
        requirements.append(row)
        use_id = None
        if iid is not None and edge_class == 'REQUIRED_ORIGINAL_READ':
            use_id = 'nested-source-use:' + str(index)
            uses.append({'id': use_id, 'requirementId': rid, 'inputId': iid,
                         'classification': 'OWNER_SOURCE_USE_AND_TREATMENT_PENDING',
                         'ownerSelectorsStatus': 'NOT_EVALUATED',
                         'treatment': {'kind': 'NOT_EVALUATED',
                                       'reason': 'OWNER_SOURCE_USE_RULE_PENDING'}})
        rows.append({'requirementId': rid, 'useId': use_id,
                     'origin': row['origin'], 'rule': rule, 'role': role,
                     'edgeClass': edge_class,
                     'selectedBinding': binding, 'selectedInputId': iid,
                     'selectedOriginal': ({'ref': pin['ref'],
                                           'digestMode': pin['digestMode'],
                                           'rawSha256': pin['rawSha256'],
                                           'byteLength': pin['byteLength'],
                                           'inventoryStatus': results[iid]['status']}
                                          if pin is not None else None),
                     'dependsOn': dependencies, 'disposition': disposition})
        return row

    def emit_comparison(parent_id, origin_id, pointer, binding, role, case_selection,
                        additional_dependencies=()):
        """Retain a source value position without claiming another original read."""
        index = len(rows)
        rid = 'nested-source:' + str(index)
        rule = {'module': 'event_definition_inputs.py',
                'moduleRawSha256': rule_hashes['event_definition_inputs.py'],
                'rule': 'event_membership_comparison', 'sourcePointer': pointer,
                'caseSelection': case_selection}
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': role, 'edgeClass': 'COMPARISON_VALUE',
               'origin': {'inputRole': origin_id, 'pointer': pointer},
               'rule': rule, 'selectedBinding': binding, 'inputIds': [],
               'dependsOn': [parent_id, *additional_dependencies],
               'findingIds': ['AR_EVENT_ASSOCIATION'],
               'sourceUseApplicability': 'COMPARISON_VALUE_ONLY',
               'structuralSelection': 'NOT_EVALUATED',
               'disposition': 'NOT_EVALUATED',
               'diagnostics': [{'code': 'COMPARISON_VALUE_NO_ADDITIONAL_ORIGINAL_READ'}],
               'qualification': 'Exact membership value position only; it selects no additional original or owner use.'}
        requirements.append(row)
        rows.append({'requirementId': rid, 'useId': None, 'origin': row['origin'],
                     'rule': rule, 'role': role, 'edgeClass': 'COMPARISON_VALUE',
                     'selectedBinding': binding,
                     'selectedInputId': None, 'selectedOriginal': None,
                     'dependsOn': row['dependsOn'],
                     'disposition': row['disposition']})
        if not _binding(binding):
            frontier(role, origin_id, pointer, 'MALFORMED_COMPARISON_BINDING', rid)
        return row

    def emit_reader_guard(parent_id, origin, binding, module, fact, dependencies, observations):
        """Retain an actual reader's applicability fact without another read."""
        rid = 'nested-source:' + str(len(rows))
        rule = {'module': module, 'moduleRawSha256': rule_hashes[module],
                'rule': fact['rule'], 'sourcePointer': origin['pointer']}
        dependencies = list(dict.fromkeys([parent_id, *dependencies]))
        disposition = 'PASS' if fact['satisfied'] else 'NOT_EVALUATED'
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': 'READER_APPLICABILITY:' + fact['rule'], 'edgeClass': 'CONDITIONAL',
               'origin': origin, 'rule': rule, 'selectedBinding': binding,
               'inputIds': list(dict.fromkeys(item['inputRole'] for item in observations)),
               'dependsOn': dependencies, 'findingIds': ['AR_BODY'], 'observations': observations,
               'readerGuard': fact, 'guardSatisfied': fact['satisfied'],
               'dependencyUse': ('READER_DIAGNOSTIC_STATE' if fact.get('stateProvenance')
                                 else 'READ_APPLICABILITY_OPERANDS'),
               'structuralSelection': disposition, 'disposition': disposition,
               'diagnostics': [], 'qualification': 'Actual reader applicability only. A false guard does not create a failed read or assert source-use admission.'}
        requirements.append(row)
        rows.append({'requirementId': rid, 'useId': None, 'origin': origin, 'rule': rule,
                     'role': row['role'], 'edgeClass': 'CONDITIONAL', 'selectedBinding': binding,
                     'selectedInputId': None, 'selectedOriginal': None,
                     'dependsOn': dependencies, 'disposition': disposition})
        return row

    def source_shape_failure(parent_id, origin_id, binding, role, reader_module,
                             schema_module, reason, *, finding_id='AR_BODY',
                             additional_dependencies=(), source_pointer=''):
        """Attach a matched parent schema contradiction to AR, never PC read."""
        index = len(rows)
        rid = 'nested-source:' + str(index)
        rule = {'module': reader_module,
                'moduleRawSha256': rule_hashes[reader_module],
                'rule': 'selected_parent_source_schema', 'sourcePointer': source_pointer,
                'schemaModule': schema_module,
                'schemaModuleRawSha256': sha((HERE / schema_module).read_bytes())}
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': role, 'edgeClass': 'SOURCE_SHAPE',
               'origin': {'inputRole': origin_id, 'pointer': source_pointer},
               'rule': rule, 'selectedBinding': binding, 'inputIds': [origin_id],
               'dependsOn': list(dict.fromkeys((parent_id, *additional_dependencies,
                             'selected-original:' + str(selected_index[origin_id])))),
               'findingIds': [finding_id], 'structuralSelection': 'FAIL',
               'disposition': 'FAIL', 'diagnostics': [{'code': reason}],
               'qualification': 'Matched selected parent fails its pinned domain source schema; no child read follows.'}
        requirements.append(row)
        rows.append({'requirementId': rid, 'useId': None, 'origin': row['origin'],
                     'rule': rule, 'role': role, 'edgeClass': 'SOURCE_SHAPE',
                     'selectedBinding': binding, 'selectedInputId': origin_id,
                     'selectedOriginal': {'ref': by_id[origin_id]['ref'],
                                          'digestMode': by_id[origin_id]['digestMode'],
                                          'rawSha256': by_id[origin_id]['rawSha256'],
                                          'byteLength': by_id[origin_id]['byteLength'],
                                          'inventoryStatus': results[origin_id]['status']},
                     'dependsOn': row['dependsOn'], 'disposition': 'FAIL'})
        frontier(role, origin_id, '', reason, rid)
        return row

    def work_condition_fact(parent, condition_id, field, actual, expected,
                            work_id, expected_pointer=None):
        """Compare one pre-carrier field at its two actual source positions."""
        index = len(rows)
        rid = 'nested-source:' + str(index)
        pointer = '/' + field
        equal = actual == expected
        code = ('WORK_DEFINITION_IDENTITY_MISMATCH' if field == 'definitionId'
                else 'WORK_CONDITION_' + field.upper() + '_MISMATCH')
        rule = {'module': 'work_sources.py',
                'moduleRawSha256': rule_hashes['work_sources.py'],
                'rule': 'work_definition_condition_pre_carrier_comparison',
                'sourcePointer': pointer,
                **({'expectedSourcePointer': expected_pointer} if expected_pointer else
                   {'expectedStageFromArray': expected})}
        observations = [{'side': 'ACTUAL', 'inputRole': condition_id,
                         'pointer': pointer, 'valueDigest': digest(actual)}]
        if expected_pointer is not None:
            observations.append({'side': 'EXPECTED', 'inputRole': work_id,
                                 'pointer': expected_pointer,
                                 'valueDigest': digest(expected)})
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': 'WORK_CONDITION_' + field.upper() + '_COMPARISON',
               'edgeClass': 'COMPARISON_VALUE',
               'origin': {'inputRole': condition_id, 'pointer': pointer},
               'rule': rule, 'selectedBinding': parent['selectedBinding'],
               'inputIds': [condition_id, work_id] if expected_pointer else [condition_id],
               'dependsOn': [parent['id']], 'findingIds': ['AR_BODY'],
               'observations': observations,
               'structuralSelection': 'PASS' if equal else 'FAIL',
               'disposition': 'PASS' if equal else 'FAIL',
               'diagnostics': [] if equal else [{'code': code}],
               'qualification': 'Local pre-carrier condition comparison only; canonical meaning, active stage and descendants remain unresolved.'}
        requirements.append(row)
        pin = by_id[condition_id]
        rows.append({'requirementId': rid, 'useId': None,
                     'origin': row['origin'], 'rule': rule, 'role': row['role'],
                     'edgeClass': 'COMPARISON_VALUE',
                     'selectedBinding': parent['selectedBinding'],
                     'selectedInputId': condition_id,
                     'selectedOriginal': {'ref': pin['ref'],
                                          'digestMode': pin['digestMode'],
                                          'rawSha256': pin['rawSha256'],
                                          'byteLength': pin['byteLength'],
                                          'inventoryStatus': results[condition_id]['status']},
                     'dependsOn': row['dependsOn'], 'disposition': row['disposition']})
        return equal

    def work_canonical_fact(parent_id, binding, role, origin, actual, expected,
                            equal, code, observations, *, static_rule=False,
                            rule_details=None):
        """Retain one exact pre-carrier reader comparison without a new use."""
        index = len(rows)
        rid = 'nested-source:' + str(index)
        rule = {'module': 'work_sources.py',
                'moduleRawSha256': rule_hashes['work_sources.py'],
                'rule': code, 'sourcePointer': origin['pointer']}
        if rule_details:
            rule.update(rule_details)
        if static_rule:
            rule['reviewedRule'] = {
                'originalPath': REVIEWED_CONDITION_PATH,
                'commit': REVIEWED_CONDITION_COMMIT,
                'rawSha256': REVIEWED_CONDITION_SHA256}
        input_ids = list(dict.fromkeys(
            observation['inputRole'] for observation in observations
            if observation.get('side') != 'PINNED_RULE'
            and observation.get('inputRole') in by_id))
        dependencies = [parent_id]
        for iid in input_ids:
            selected_dependency = 'selected-original:' + str(selected_index[iid])
            if selected_dependency not in dependencies:
                dependencies.append(selected_dependency)
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': role, 'edgeClass': 'COMPARISON_VALUE',
               'origin': origin, 'rule': rule, 'selectedBinding': binding,
               'inputIds': input_ids, 'dependsOn': dependencies,
               'findingIds': ['AR_BODY'], 'observations': observations,
               'actualValueDigest': digest(actual),
               'expectedValueDigest': digest(expected),
               'structuralSelection': 'PASS' if equal else 'FAIL',
               'disposition': 'PASS' if equal else 'FAIL',
               'diagnostics': [] if equal else [{'code': code}],
               'qualification': 'Local pre-carrier work reader comparison only; carrier, owner use and complete closure remain open.'}
        requirements.append(row)
        origin_pin = by_id.get(origin['inputRole'])
        origin_iid = origin['inputRole'] if origin_pin is not None else None
        rows.append({'requirementId': rid, 'useId': None,
                     'origin': origin, 'rule': rule, 'role': role,
                     'edgeClass': 'COMPARISON_VALUE',
                     'selectedBinding': binding,
                     'selectedInputId': origin_iid,
                     'selectedOriginal': ({'ref': origin_pin['ref'],
                                           'digestMode': origin_pin['digestMode'],
                                           'rawSha256': origin_pin['rawSha256'],
                                           'byteLength': origin_pin['byteLength'],
                                           'inventoryStatus': results[origin_iid]['status']}
                                          if origin_pin is not None else None),
                     'dependsOn': dependencies, 'disposition': row['disposition']})
        return row

    def work_claim_value_fact(parent_id, binding, role, code,
                              claim_id, claim_pointer, claim_value,
                              work_id, work_pointer, work_value,
                              *, claim_present=True):
        """Compare exact claim/work operands, retaining a truly absent claim."""
        work_observation = {'side': 'WORK', 'inputRole': work_id,
                            'pointer': work_pointer,
                            'valueDigest': digest(work_value)}
        if claim_present:
            claim_observation = {'side': 'CLAIM', 'inputRole': claim_id,
                                 'pointer': claim_pointer,
                                 'valueDigest': digest(claim_value)}
            origin = {'inputRole': claim_id, 'pointer': claim_pointer}
            actual, expected = claim_value, work_value
            observations = [claim_observation, work_observation]
        else:
            origin = {'inputRole': work_id, 'pointer': work_pointer}
            actual, expected = None, work_value
            observations = [work_observation]
        return work_canonical_fact(
            parent_id, binding, role, origin, actual, expected,
            same(actual, expected), code, observations,
            rule_details={'claimPointer': claim_pointer,
                          'claimPointerPresent': claim_present,
                          **({'actualProjection': 'ABSENT_SELECTED_GET_RETURNS_NULL'}
                             if not claim_present else {}),
                          'expectedWorkPointer': work_pointer})

    def carrier_identity_fact(parent, carrier, declaration_pointer, intent_id,
                              kind):
        """Compare the selected source's ID to its actual declaration ref."""
        field = OPERATION_SOURCE_SCHEMAS[kind][1]
        iid = carrier['inputId']
        actual = carrier['record'][field]
        expected = carrier['binding']['ref']
        equal = same(actual, expected)
        rid = 'nested-source:' + str(len(rows))
        rule = {'module': 'components/revision-02/operation_adapters.py',
                'moduleRawSha256': rule_hashes[
                    'components/revision-02/operation_adapters.py'],
                'rule': 'SOURCE_ID_BINDING_MISMATCH',
                'selectionRuleModule': 'source_derivation.py',
                'selectionRuleRawSha256': rule_hashes['source_derivation.py'],
                'sourcePointer': '/' + field,
                'declarationPointer': declaration_pointer,
                'sourceSchemaId': OPERATION_SOURCE_SCHEMAS[kind][0]}
        observations = [
            {'side': 'CARRIER', 'inputRole': iid, 'pointer': '/' + field,
             'valueDigest': digest(actual)},
            {'side': 'DECLARATION', 'inputRole': intent_id,
             'pointer': declaration_pointer + '/ref',
             'valueDigest': digest(expected)}]
        dependencies = [parent['id'],
                        'selected-original:' + str(selected_index[iid])]
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': 'OPERATION_CARRIER_PAYLOAD_ID_COMPARISON',
               'edgeClass': 'COMPARISON_VALUE',
               'origin': {'inputRole': iid, 'pointer': '/' + field},
               'rule': rule, 'selectedBinding': carrier['binding'],
               'inputIds': [iid, intent_id], 'dependsOn': dependencies,
               'findingIds': ['AR_BODY'], 'observations': observations,
               'actualValueDigest': digest(actual),
               'expectedValueDigest': digest(expected),
               'structuralSelection': 'PASS' if equal else 'FAIL',
               'disposition': 'PASS' if equal else 'FAIL',
               'diagnostics': [] if equal else [
                   {'code': 'SOURCE_ID_BINDING_MISMATCH'}],
               'qualification': 'Selected operation carrier ID comparison only; source use, subject relation and further carrier checks remain open.'}
        requirements.append(row)
        pin = carrier['pin']
        rows.append({'requirementId': rid, 'useId': None,
                     'origin': row['origin'], 'rule': rule, 'role': row['role'],
                     'edgeClass': 'COMPARISON_VALUE',
                     'selectedBinding': carrier['binding'],
                     'selectedInputId': iid,
                     'selectedOriginal': {'ref': pin['ref'],
                                          'digestMode': pin['digestMode'],
                                          'rawSha256': pin['rawSha256'],
                                          'byteLength': pin['byteLength'],
                                          'inventoryStatus': results[iid]['status']},
                     'dependsOn': dependencies,
                     'disposition': row['disposition']})
        return row

    def work_carrier_fact(work_parent, carrier_selection, work_id, intent_id,
                          role, code, actual, expected, actual_origin,
                          expected_pointer, *, actual_present=True,
                          projected_source_pointer=None):
        """Compare one exact selected carrier/work value without another read."""
        carrier = carrier_selection['selectedCandidate']
        carrier_id = carrier['inputId']
        rid = 'nested-source:' + str(len(rows))
        origin = (actual_origin if actual_present else
                  {'inputRole': work_id, 'pointer': expected_pointer})
        observations = []
        if actual_present:
            observations.append({'side': 'ACTUAL', **actual_origin,
                                 'valueDigest': digest(actual)})
        observations.append({'side': 'EXPECTED', 'inputRole': work_id,
                             'pointer': expected_pointer,
                             'valueDigest': digest(expected)})
        dependencies = list(dict.fromkeys((
            work_parent['id'], carrier_selection['identityRequirementId'],
            'selected-original:' + str(selected_index[work_id]),
            'selected-original:' + str(selected_index[carrier_id]))))
        if actual_origin['inputRole'] == intent_id:
            dependencies.append('root:effectIntent')
        rule = {'module': 'work_sources.py',
                'moduleRawSha256': rule_hashes['work_sources.py'],
                'rule': code, 'sourcePointer': actual_origin['pointer'],
                'expectedWorkPointer': expected_pointer,
                'atomPointer': carrier_selection['atomPointer']}
        if role == 'WORK_SPECIFIC_ACTIVITY_COMPARISON':
            rule['claimValueSchemaPath'] = \
                'components/revision-02/proposition.schema.json'
            rule['claimValueSchemaRawSha256'] = sha(
                (HERE / rule['claimValueSchemaPath']).read_bytes())
        if not actual_present:
            rule['actualProjection'] = 'ABSENT_OPTIONAL_FIELD_AS_NULL'
            rule['projectedSourcePointer'] = projected_source_pointer
        equal = same(actual, expected)
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': role, 'edgeClass': 'COMPARISON_VALUE',
               'origin': origin, 'rule': rule,
               'selectedBinding': carrier['binding'],
               'workBinding': work_parent['selectedBinding'],
               'inputIds': list(dict.fromkeys((carrier_id, work_id,
                                              actual_origin['inputRole']))),
               'dependsOn': dependencies, 'findingIds': ['AR_BODY'],
               'observations': observations,
               'actualValueDigest': digest(actual),
               'expectedValueDigest': digest(expected),
               'structuralSelection': 'PASS' if equal else 'FAIL',
               'disposition': 'PASS' if equal else 'FAIL',
               'diagnostics': [] if equal else [{'code': code}],
               'qualification': 'Selected operation carrier/work meaning comparison only; owner admission, performer, time and condition evidence remain open.'}
        requirements.append(row)
        origin_pin = by_id.get(origin['inputRole'])
        rows.append({'requirementId': rid, 'useId': None,
                     'origin': origin, 'rule': rule, 'role': role,
                     'edgeClass': 'COMPARISON_VALUE',
                     'selectedBinding': carrier['binding'],
                     'selectedInputId': origin['inputRole'],
                     'selectedOriginal': ({'ref': origin_pin['ref'],
                                           'digestMode': origin_pin['digestMode'],
                                           'rawSha256': origin_pin['rawSha256'],
                                           'byteLength': origin_pin['byteLength'],
                                           'inventoryStatus': results[origin['inputRole']]['status']}
                                          if origin_pin is not None else None),
                     'dependsOn': dependencies, 'disposition': row['disposition']})
        return row

    def operation_actual_comparisons(selection, atom, intent_id):
        """Capture the sealed adapter's actual predicates from exact originals."""
        if not actual_carrier_cache['attempted']:
            actual_carrier_cache['attempted'] = True
            try:
                component_root = str(HERE / 'components/revision-02')
                if component_root not in sys.path:
                    sys.path.insert(0, component_root)
                from operation_adapters import OperationAdapters
                actual_carrier_cache['adapter'] = OperationAdapters()
            except Exception:
                pass
        adapter = actual_carrier_cache['adapter']
        carrier = selection['selectedCandidate']
        carrier_id = carrier['inputId']
        atom_pointer = selection['atomPointer']
        source = admitted[carrier_id]
        try:
            checked = (actual_carrier_comparisons(
                adapter, atom['definition'].split(':')[-1], atom, selection['kind'],
                {'binding': carrier['binding'], 'record': source}) if adapter is not None else
                {'status': 'NOT_EVALUATED', 'reason': 'OPERATION_ADAPTER_UNAVAILABLE'})
        except Exception:
            checked = {'status': 'NOT_EVALUATED', 'reason': 'OPERATION_ADAPTER_COMPARISON_UNAVAILABLE'}
        if checked['status'] != 'CHECKED':
            frontier('OPERATION_CARRIER_ACTUAL_COMPARISONS', intent_id, atom_pointer,
                     checked['reason'], selection['identityRequirementId'])
            return
        from original_operand import select_operand

        def rebind(operand):
            value = dict(operand)
            if value['inputRole'] == 'OPERATION_SOURCE':
                value['inputRole'] = carrier_id
            elif value['inputRole'] == 'ATOM:' + atom['atomId']:
                value['inputRole'] = intent_id
                for key in ('pointer', 'ancestorPointer'):
                    if key in value:
                        value[key] = atom_pointer + value[key]
            else:
                raise InputError('Unexpected operation comparison operand role.')
            return value

        def retain(item, role, *, result_kind='COMPARISON', disposition=None):
            available = item.get('operandAvailability', item)
            operands = {side: rebind(available[side])
                        for side in ('source', 'destination') if side in available}
            observations = []
            for side, operand in operands.items():
                pointer = operand.get('ancestorPointer', operand['pointer'])
                value_digest = operand.get('ancestorValueDigest', operand.get('valueDigest'))
                if value_digest is None:
                    continue
                assert digest(json_pointer(admitted[operand['inputRole']], pointer)) == value_digest
                observations.append({'side': side.upper() + ('_ANCESTOR' if 'ancestorPointer' in operand else ''),
                                     'inputRole': operand['inputRole'], 'pointer': pointer,
                                     'valueDigest': value_digest})
            if not observations:
                frontier(role, intent_id, atom_pointer, 'ORIGINAL_COMPARISON_OPERANDS_UNAVAILABLE',
                         selection['identityRequirementId'])
                return
            status = disposition or item.get('disposition', 'NOT_EVALUATED')
            origin = {key: observations[0][key] for key in ('inputRole', 'pointer')}
            rid = 'nested-source:' + str(len(rows))
            dependencies = [selection['atomRequirementId'], selection['identityRequirementId'],
                            'selected-original:' + str(selected_index[carrier_id]), 'root:effectIntent']
            rule = {'module': 'components/revision-02/operation_adapters.py',
                    'moduleRawSha256': rule_hashes['components/revision-02/operation_adapters.py'],
                    'rule': item['code'], 'readerComparisonPointer': item['pointer'],
                    'atomPointer': atom_pointer,
                    'performerSelectorModule': 'work_sources.py',
                    'performerSelectorRawSha256': rule_hashes['work_sources.py']}
            edge_class = 'COMPARISON_VALUE' if result_kind != 'REQUIRED_INTERPRETATION' else 'CONDITIONAL'
            row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
                   'role': role, 'edgeClass': edge_class, 'origin': origin, 'rule': rule,
                   'selectedBinding': carrier['binding'], 'inputIds': [carrier_id, intent_id],
                   'dependsOn': dependencies, 'findingIds': ['AR_BODY'],
                   'observations': observations, 'operands': operands,
                   'readerResultKind': result_kind, 'structuralSelection': status,
                   'disposition': status,
                   'diagnostics': [] if status == 'PASS' else [{'code': item['code']}],
                   'qualification': 'Existing carrier reference or instant predicate only. Equal party refs do not prove immutable party identity or performer authority; source use and time-basis interpretation remain separate.'}
            if role == 'WORK_CARRIER_PERFORMER_REF_COMPARISON':
                row['selectedPerformerPointer'] = checked['performerPointer']
                row['comparisonScope'] = 'PARTY_REFERENCE_ONLY'
            if 'equal' in item:
                row['equal'] = item['equal']
            requirements.append(row)
            pin = by_id[origin['inputRole']]
            rows.append({'requirementId': rid, 'useId': None, 'origin': origin, 'rule': rule,
                         'role': role, 'edgeClass': edge_class, 'selectedBinding': carrier['binding'],
                         'selectedInputId': origin['inputRole'],
                         'selectedOriginal': {'ref': pin['ref'], 'digestMode': pin['digestMode'],
                                              'rawSha256': pin['rawSha256'], 'byteLength': pin['byteLength'],
                                              'inventoryStatus': results[origin['inputRole']]['status']},
                         'dependsOn': dependencies, 'disposition': status})
            if status == 'NOT_EVALUATED':
                frontier(role, origin['inputRole'], origin['pointer'], item['code'], rid)

        for comparison in checked['comparisons']:
            retain(comparison, 'WORK_CARRIER_PERFORMER_REF_COMPARISON'
                   if comparison['code'] == 'SOURCE_PERFORMER_REF_MISMATCH' else
                   'WORK_CARRIER_PROFILE_TIME_COMPARISON')
        for missing in checked['remainingRoles']:
            if missing['role'] == 'SOURCE_PROFILE_TIME_INSTANT_INTERPRETATION':
                operand = select_operand(source, missing['pointer'].removeprefix('/source/record'),
                                         'OPERATION_SOURCE')
                role = 'WORK_CARRIER_TIME_INSTANT_INTERPRETATION'
            else:
                operand = select_operand(atom, missing['pointer'].removeprefix('/atom'),
                                         'ATOM:' + atom['atomId'])
                role = 'WORK_CARRIER_TIME_PROFILE_INTERPRETATION'
            retain({'code': missing['role'], 'pointer': missing['pointer'], 'source': operand},
                   role, result_kind='REQUIRED_INTERPRETATION', disposition='NOT_EVALUATED')
        for error in checked['errors']:
            operand = select_operand(source, error['pointer'].removeprefix('/source/record'),
                                     'OPERATION_SOURCE')
            retain({**error, 'source': operand}, 'WORK_CARRIER_PROFILE_TIME_COMPARISON',
                   result_kind='READER_ERROR', disposition='FAIL')

    def work_active_stage(work_parent, carrier_selection, work_id, intent_id,
                          atom_pointer, claim_body, condition_positions):
        """Record the reader's stage array choice, not condition satisfaction."""
        kind = carrier_selection['kind']
        facet = claim_body.get('performanceFacet')
        facet_pointer = atom_pointer + '/body/performanceFacet'
        facet_present = 'performanceFacet' in claim_body
        if not isinstance(facet, str) or facet not in {*WORK_EXECUTION_STAGES, 'OCCURRENCE'}:
            stage, selection_status = None, 'PERFORMANCE_FACET_UNAVAILABLE'
            frontier('WORK_CONDITION_ACTIVE_STAGE', intent_id,
                     facet_pointer, selection_status,
                     work_parent['id'])
        elif kind == 'intent':
            stage, selection_status = None, 'NO_EXECUTION_STAGE_FOR_INTENDED'
        elif facet == 'OCCURRENCE':
            stage, selection_status = None, 'NO_ACTIVE_STAGE_FOR_OCCURRENCE'
        else:
            stage, selection_status = WORK_EXECUTION_STAGES[facet], 'SELECTED_STAGE_ONLY'
        chosen_positions = (condition_positions.get(stage, []) if stage else [])
        rid = 'nested-source:' + str(len(rows))
        dependencies = list(dict.fromkeys([
            work_parent['id'], carrier_selection['identityRequirementId'],
            *[requirement_id for item in chosen_positions
              for requirement_id in (
                  item['readRequirementId'],
                  *item['preCarrierComparisonRequirementIds'],
                  *([item['canonicalMeaningRequirementId']]
                    if 'canonicalMeaningRequirementId' in item else []),
                  *([item['sourceShapeRequirementId']]
                    if 'sourceShapeRequirementId' in item else []))]]))
        rule = {'module': 'work_sources.py',
                'moduleRawSha256': rule_hashes['work_sources.py'],
                'rule': 'execution_active_condition_stage_selection',
                'sourcePointer': (facet_pointer if facet_present else
                                  atom_pointer + '/body'),
                'claimFacetPointerPresent': facet_present,
                'claimFacetPointer': facet_pointer,
                'workArray': next((field for field, _claim, group_stage, _prefix
                                   in WORK_CONDITION_GROUPS
                                   if group_stage == stage), None)}
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': 'WORK_EXECUTION_ACTIVE_STAGE_SELECTION',
               'edgeClass': 'CONDITIONAL',
               'origin': {'inputRole': intent_id,
                          'pointer': rule['sourcePointer']},
               'rule': rule,
               'selectedBinding': carrier_selection['selectedCandidate']['binding'],
               'workBinding': work_parent['selectedBinding'],
               'inputIds': [intent_id, work_id],
               'dependsOn': dependencies, 'findingIds': ['AR_BODY'],
               'claimFacet': facet, 'selectedStage': stage,
               'stageSelectionStatus': selection_status,
               'selectedConditionPositions': chosen_positions,
               'structuralSelection': ('NOT_EVALUATED' if selection_status ==
                                       'PERFORMANCE_FACET_UNAVAILABLE' else 'PASS'),
               'disposition': 'NOT_EVALUATED',
               'diagnostics': ([{'code': selection_status}] if selection_status ==
                               'PERFORMANCE_FACET_UNAVAILABLE' else []),
               'qualification': 'Exact stage-array selection only. Condition parents may be blocked; no criterion, measurement, method, property or condition satisfaction is inferred.'}
        requirements.append(row)
        rows.append({'requirementId': rid, 'useId': None,
                     'origin': row['origin'], 'rule': rule, 'role': row['role'],
                     'edgeClass': 'CONDITIONAL',
                     'selectedBinding': row['selectedBinding'],
                     'selectedInputId': intent_id,
                     'selectedOriginal': {'ref': by_id[intent_id]['ref'],
                                          'digestMode': by_id[intent_id]['digestMode'],
                                          'rawSha256': by_id[intent_id]['rawSha256'],
                                          'byteLength': by_id[intent_id]['byteLength'],
                                          'inventoryStatus': results[intent_id]['status']},
                     'dependsOn': dependencies,
                     'disposition': 'NOT_EVALUATED'})
        return row

    def condition_property_facts(stage, position, resolved, origins, intent_id, atom_pointer):
        """Retain the existing property-link predicates, not later read reachability."""
        condition_id = position['selectedInputId']
        condition = admitted[condition_id]
        property_record = resolved[3]
        property_id, property_read, _ = origins[id(property_record)]
        work_id = position['origin']['inputRole']
        work = admitted[work_id]
        atom = json_pointer(admitted[intent_id], atom_pointer)
        claim_work = atom.get('body', {}).get('workSpecification', {})
        if isinstance(property_record.get('workConditionMeaning'), dict) and (
                not isinstance(claim_work, dict)
                or not all(_binding(claim_work.get(key)) for key in ('binding', 'procedure'))):
            frontier('WORK_CONDITION_PROPERTY_SEMANTICS', intent_id,
                     atom_pointer + '/body/workSpecification',
                     'CONDITION_PROPERTY_CLAIM_BINDING_OPERANDS_UNAVAILABLE', property_read)
            return
        selection_pointer = position['origin']['pointer'] + '/definitionBinding'
        selection_origin = {'inputRole': work_id, 'pointer': selection_pointer}
        checks = condition_property_comparisons(condition, property_record, atom,
            condition_binding=position['selectedBinding'], work_specification_binding=stage['workBinding'],
            procedure_binding=work['procedure'])
        position['propertyMeaningRequirementIds'] = []
        for check in checks:
            source_pointer = check['sourcePointer'] if check['sourcePresent'] else ''
            source = {'inputRole': property_id, 'pointer': source_pointer}
            destination = (selection_origin if check['destinationKind'] == 'conditionSelection' else
                {'inputRole': intent_id, 'pointer': atom_pointer + check['destinationPointer']}
                if check['destinationKind'] == 'claim' else
                {'inputRole': condition_id, 'pointer': check['destinationPointer']})
            observations = [
                {'side': 'PROPERTY' if check['sourcePresent'] else 'PROPERTY_ANCESTOR', **source,
                 'valueDigest': digest(json_pointer(property_record, source_pointer))},
                {'side': 'EXPECTED', **destination, 'valueDigest': digest(check['expected'])}]
            if check.get('usesSelectedBindings'):
                # The aggregate predicate uses the selected work definition's
                # procedure; its individual procedure predicate uses the claim.
                for side, iid, path in (
                    ('CONDITION_SELECTION', work_id, selection_pointer),
                    ('WORK_SELECTION', intent_id, atom_pointer + '/body/workSpecification/binding'),
                    ('SELECTED_WORK_PROCEDURE', work_id, '/procedure')):
                    observations.append({'side': side, 'inputRole': iid, 'pointer': path,
                                         'valueDigest': digest(json_pointer(admitted[iid], path))})
            fact = work_canonical_fact(property_read, position['selectedBinding'],
                'WORK_CONDITION_PROPERTY_MEANING_COMPARISON', source,
                check['actual'], check['expected'], check['equal'], check['code'], observations,
                rule_details={'module': 'condition_sources.py',
                              'moduleRawSha256': rule_hashes['condition_sources.py'],
                              'readerRule': 'condition_property_comparisons',
                              'readerComparisonPointer': check['path'],
                              'sourcePointerPresent': check['sourcePresent'],
                              'atomPointer': atom_pointer,
                              **({'predicate': 'MEANING_EQUALS_SELECTED_CONDITION_WORK_AND_PROCEDURE'}
                                 if check.get('usesSelectedBindings') else {})})
            fact['dependsOn'][:] = list(dict.fromkeys([
                *fact['dependsOn'], stage['id'], position['readRequirementId'],
                *position['initialInputRequirementIds'],
                *position['preCarrierComparisonRequirementIds']]))
            fact['qualification'] = 'Local property-link predicate only; later semantic guards, condition satisfaction and source-use admission remain open.'
            if not check['sourcePresent']:
                from original_operand import select_operand
                fact.pop('actualValueDigest', None)
                fact['operands'] = {'source': select_operand(property_record, check['sourcePointer'], property_id),
                                    'destination': select_operand(condition, '', condition_id)}
            position['propertyMeaningRequirementIds'].append(fact['id'])

    def condition_fixed_method_facts(stage, position, resolved, origins, atom_pointer):
        """Observe the two existing fixed-method fields after their real initial reads."""
        condition_id = position['selectedInputId']
        condition = admitted[condition_id]
        method = resolved[1]
        method_id, method_read, _prefix = origins[id(method)]
        for field, rule, role, code, requirement_key, qualification in (
            ('unit', condition_required_unit, 'WORK_CONDITION_FIXED_UNIT_COMPARISON',
             'WORK_CONDITION_REQUIRED_UNIT_MISMATCH', 'fixedUnitRequirementIds',
             'Existing fixed-unit predicate only; the selected method field and condition branch controls are originals. Other condition checks and source-use admission remain separate.'),
            ('quantityKind', condition_activity_quantity_kind, 'WORK_CONDITION_FIXED_QUANTITY_KIND_COMPARISON',
             'WORK_CONDITION_REQUIRED_QUANTITY_KIND_MISMATCH', 'fixedQuantityKindRequirementIds',
             'Existing activity/O08 fixed quantity-kind predicate only; the selected method field and condition branch controls are originals. Other condition checks and source-use admission remain separate.')):
            position[requirement_key] = []
            expected = rule(condition)
            if expected is None:
                continue
            pointer = '/quantityContext/' + field
            actual = method['quantityContext'][field]
            observations = [
                {'side': 'ORIGINAL', 'inputRole': method_id, 'pointer': pointer,
                 'valueDigest': digest(actual)},
                *({'side': 'CONTROL', 'inputRole': condition_id, 'pointer': '/' + control,
                   'valueDigest': digest(condition[control])} for control in ('stage', 'activityRow'))]
            fact = work_canonical_fact(method_read, position['selectedBinding'], role,
                {'inputRole': method_id, 'pointer': pointer},
                actual, expected, same(actual, expected), code, observations,
                rule_details={'module': 'condition_sources.py',
                    'moduleRawSha256': rule_hashes['condition_sources.py'],
                    'readerRule': rule.__name__, 'readerComparisonPointer': '/method' + pointer,
                    'atomPointer': atom_pointer})
            fact['dependsOn'][:] = list(dict.fromkeys([*fact['dependsOn'], stage['id'],
                position['readRequirementId'], *position['initialInputRequirementIds'],
                *position['preCarrierComparisonRequirementIds']]))
            fact['expectedValueSource'] = 'PINNED_READER_RULE'
            fact['qualification'] = qualification
            position[requirement_key].append(fact['id'])

    def condition_fixed_predicate_kind_fact(stage, position, atom_pointer):
        """Observe the fixed canonical kind separately from property-link equality."""
        position['fixedPredicateKindRequirementIds'] = []
        condition_id = position['selectedInputId']
        condition = admitted[condition_id]
        expected = condition_activity_predicate_kind(condition)
        if expected is None:
            return
        actual = condition['predicateKind']
        observations = [
            {'side': 'ORIGINAL', 'inputRole': condition_id, 'pointer': '/predicateKind',
             'valueDigest': digest(actual)},
            *({'side': 'CONTROL', 'inputRole': condition_id, 'pointer': '/' + control,
               'valueDigest': digest(condition[control])} for control in ('stage', 'activityRow'))]
        fact = work_canonical_fact(position['readRequirementId'], position['selectedBinding'],
            'WORK_CONDITION_FIXED_PREDICATE_KIND_COMPARISON',
            {'inputRole': condition_id, 'pointer': '/predicateKind'},
            actual, expected, same(actual, expected),
            'WORK_CONDITION_PREDICATE_KIND_MISMATCH', observations,
            rule_details={'module': 'condition_sources.py',
                'moduleRawSha256': rule_hashes['condition_sources.py'],
                'readerRule': 'condition_activity_predicate_kind',
                'readerComparisonPointer': '/condition/predicateKind', 'atomPointer': atom_pointer})
        fact['dependsOn'][:] = list(dict.fromkeys([*fact['dependsOn'], stage['id'],
            *position['initialInputRequirementIds'], *position['preCarrierComparisonRequirementIds']]))
        fact['expectedValueSource'] = 'PINNED_READER_RULE'
        fact['qualification'] = 'Existing activity/O08 fixed canonical predicate only; selected condition scalar and branch controls are originals. Property-link equality and source-use admission remain separate.'
        position['fixedPredicateKindRequirementIds'].append(fact['id'])

    def condition_fixed_operator_fact(stage, position, resolved, origins, atom_pointer):
        """Observe the existing activity/O08 operator on its selected criterion."""
        position['fixedOperatorRequirementIds'] = []
        condition_id = position['selectedInputId']
        condition = admitted[condition_id]
        expected = condition_activity_operator(condition)
        if expected is None:
            return
        criterion = resolved[0]
        criterion_id, criterion_read, _prefix = origins[id(criterion)]
        actual = criterion['operator']
        observations = [
            {'side': 'ORIGINAL', 'inputRole': criterion_id, 'pointer': '/operator',
             'valueDigest': digest(actual)},
            *({'side': 'CONTROL', 'inputRole': condition_id, 'pointer': '/' + control,
               'valueDigest': digest(condition[control])} for control in ('stage', 'activityRow'))]
        fact = work_canonical_fact(criterion_read, position['selectedBinding'],
            'WORK_CONDITION_FIXED_OPERATOR_COMPARISON',
            {'inputRole': criterion_id, 'pointer': '/operator'},
            actual, expected, same(actual, expected),
            'WORK_CONDITION_REQUIRED_OPERATOR_MISMATCH', observations,
            rule_details={'module': 'condition_sources.py',
                'moduleRawSha256': rule_hashes['condition_sources.py'],
                'readerRule': 'condition_activity_operator',
                'readerComparisonPointer': '/criterion/operator', 'atomPointer': atom_pointer})
        fact['dependsOn'][:] = list(dict.fromkeys([*fact['dependsOn'], stage['id'],
            position['readRequirementId'], *position['initialInputRequirementIds'],
            *position['preCarrierComparisonRequirementIds']]))
        fact['expectedValueSource'] = 'PINNED_READER_RULE'
        fact['qualification'] = 'Existing activity/O08 fixed-operator predicate only; criterion scalar and condition branch controls are originals. Other condition checks and source-use admission remain separate.'
        position['fixedOperatorRequirementIds'].append(fact['id'])

    def condition_fixed_threshold_decimal_fact(stage, position, resolved, origins, atom_pointer):
        """Observe the existing decimal comparison, retaining genuine scalar absence."""
        from original_operand import select_operand
        position['fixedThresholdDecimalRequirementIds'] = []
        condition_id = position['selectedInputId']
        condition = admitted[condition_id]
        expected = condition_activity_threshold_decimal(condition)
        if expected is None:
            return
        criterion = resolved[0]
        criterion_id, criterion_read, _prefix = origins[id(criterion)]
        actual = criterion['threshold'].get('decimal')
        operand = select_operand(criterion, '/threshold/decimal', criterion_id)
        present = 'valueDigest' in operand
        source_pointer = operand['pointer'] if present else operand['ancestorPointer']
        observations = [
            {'side': 'ORIGINAL' if present else 'ORIGINAL_ANCESTOR',
             'inputRole': criterion_id, 'pointer': source_pointer,
             'valueDigest': operand['valueDigest'] if present else operand['ancestorValueDigest']},
            *({'side': 'CONTROL', 'inputRole': condition_id, 'pointer': '/' + control,
               'valueDigest': digest(condition[control])} for control in ('stage', 'activityRow'))]
        fact = work_canonical_fact(criterion_read, position['selectedBinding'],
            'WORK_CONDITION_FIXED_THRESHOLD_DECIMAL_COMPARISON',
            {'inputRole': criterion_id, 'pointer': source_pointer},
            actual, expected, same(actual, expected),
            'WORK_CONDITION_REQUIRED_THRESHOLD_MISMATCH', observations,
            rule_details={'module': 'condition_sources.py',
                'moduleRawSha256': rule_hashes['condition_sources.py'],
                'readerRule': 'condition_activity_threshold_decimal',
                'readerComparisonPointer': '/criterion/threshold/decimal',
                'sourcePointerPresent': present, 'atomPointer': atom_pointer})
        fact['dependsOn'][:] = list(dict.fromkeys([*fact['dependsOn'], stage['id'],
            position['readRequirementId'], *position['initialInputRequirementIds'],
            *position['preCarrierComparisonRequirementIds']]))
        fact['operands'] = {'source': operand}
        if not present:
            fact.pop('actualValueDigest', None)
        fact['expectedValueSource'] = 'PINNED_READER_RULE'
        fact['qualification'] = 'Existing activity/O08 fixed decimal predicate only; absent decimal is witnessed at its original ancestor. Other threshold checks and source-use admission remain separate.'
        position['fixedThresholdDecimalRequirementIds'].append(fact['id'])

    def condition_fixed_threshold_qualifier_fact(stage, position, resolved, origins, atom_pointer):
        """Observe the existing qualifier comparison, retaining genuine scalar absence."""
        from original_operand import select_operand
        position['fixedThresholdQualifierRequirementIds'] = []
        condition_id = position['selectedInputId']
        condition = admitted[condition_id]
        expected = condition_activity_threshold_qualifier(condition)
        if expected is None:
            return
        criterion = resolved[0]
        criterion_id, criterion_read, _prefix = origins[id(criterion)]
        actual = criterion['threshold'].get('qualifier')
        operand = select_operand(criterion, '/threshold/qualifier', criterion_id)
        present = 'valueDigest' in operand
        source_pointer = operand['pointer'] if present else operand['ancestorPointer']
        observations = [
            {'side': 'ORIGINAL' if present else 'ORIGINAL_ANCESTOR',
             'inputRole': criterion_id, 'pointer': source_pointer,
             'valueDigest': operand['valueDigest'] if present else operand['ancestorValueDigest']},
            *({'side': 'CONTROL', 'inputRole': condition_id, 'pointer': '/' + control,
               'valueDigest': digest(condition[control])} for control in ('stage', 'activityRow'))]
        fact = work_canonical_fact(criterion_read, position['selectedBinding'],
            'WORK_CONDITION_FIXED_THRESHOLD_QUALIFIER_COMPARISON',
            {'inputRole': criterion_id, 'pointer': source_pointer},
            actual, expected, same(actual, expected),
            'WORK_CONDITION_REQUIRED_THRESHOLD_QUALIFIER_MISMATCH', observations,
            rule_details={'module': 'condition_sources.py',
                'moduleRawSha256': rule_hashes['condition_sources.py'],
                'readerRule': 'condition_activity_threshold_qualifier',
                'readerComparisonPointer': '/criterion/threshold/qualifier',
                'sourcePointerPresent': present, 'atomPointer': atom_pointer})
        fact['dependsOn'][:] = list(dict.fromkeys([*fact['dependsOn'], stage['id'],
            position['readRequirementId'], *position['initialInputRequirementIds'],
            *position['preCarrierComparisonRequirementIds']]))
        fact['operands'] = {'source': operand}
        if not present:
            fact.pop('actualValueDigest', None)
        fact['expectedValueSource'] = 'PINNED_READER_RULE'
        fact['qualification'] = 'Existing activity/O08 fixed qualifier predicate only; absent qualifier is witnessed at its original ancestor. Other threshold checks and source-use admission remain separate.'
        position['fixedThresholdQualifierRequirementIds'].append(fact['id'])

    def condition_scope_facts(stage, position, resolved, origins, intent_id, atom_pointer):
        """Retain shared common predicates without opening the operand gate."""
        from original_operand import select_operand
        condition_id = position['selectedInputId']
        atom = json_pointer(admitted[intent_id], atom_pointer)
        condition = admitted[condition_id]
        method, measurement = resolved[1:3]
        records = {'condition': condition, 'claim': atom,
                   'method': method, 'measurement': measurement}
        original_ids = {'condition': condition_id, 'claim': intent_id,
                        'method': origins[id(method)][0],
                        'measurement': origins[id(measurement)][0]}
        position['commonScopeRequirementIds'] = []
        try:
            checks = condition_scope_checks(condition, atom, method, measurement)
        except (InputError, KeyError, ValueError, TypeError, ImportError):
            frontier('WORK_CONDITION_COMMON_SCOPE', condition_id, '',
                     'COMMON_CONDITION_OPERANDS_OR_INTERPRETATION_UNAVAILABLE', stage['id'])
            return
        for check in checks:
            operands, observations = [], []
            for index, selected in enumerate(check['operands']):
                kind = selected['recordKind']
                operand = select_operand(records[kind], selected['pointer'], original_ids[kind])
                if kind == 'claim':
                    for key in ('pointer', 'ancestorPointer'):
                        if key in operand:
                            operand[key] = atom_pointer + operand[key]
                operands.append(operand)
                pointer = operand.get('ancestorPointer', operand['pointer'])
                value_digest = operand.get('ancestorValueDigest', operand.get('valueDigest'))
                observations.append({'operandIndex': index, 'recordKind': kind,
                    'inputRole': operand['inputRole'], 'pointer': pointer,
                    'valueDigest': value_digest})
            status = ('PASS' if check['equal'] else 'FAIL') if check['kind'] == 'COMPARE' else (
                'FAIL' if check['kind'] == 'ERROR' else 'NOT_EVALUATED')
            code = check.get('code', check.get('role'))
            origin = {key: observations[0][key] for key in ('inputRole', 'pointer')}
            rid = 'nested-source:' + str(len(rows))
            dependencies = list(dict.fromkeys([stage['id'], position['readRequirementId'],
                                               *position['initialInputRequirementIds']]))
            rule = {'module': 'condition_sources.py', 'moduleRawSha256': rule_hashes['condition_sources.py'],
                    'readerRule': 'condition_scope_checks', 'rule': code,
                    'readerComparisonPointer': check['path'], 'atomPointer': atom_pointer}
            role = 'WORK_CONDITION_COMMON_SCOPE_' + (
                'COMPARISON' if check['kind'] == 'COMPARE' else
                'READER_ERROR' if check['kind'] == 'ERROR' else 'INTERPRETATION')
            edge_class = 'CONDITIONAL' if check['kind'] == 'MISSING' else 'COMPARISON_VALUE'
            row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
                   'role': role, 'edgeClass': edge_class, 'origin': origin, 'rule': rule,
                   'selectedBinding': position['selectedBinding'],
                   'inputIds': list(dict.fromkeys(item['inputRole'] for item in operands)),
                   'dependsOn': dependencies, 'findingIds': ['AR_BODY'],
                   'observations': observations, 'operands': operands,
                   'readerResultKind': check['kind'], 'structuralSelection': status,
                   'disposition': status, 'diagnostics': [] if status == 'PASS' else [{'code': code}],
                   'qualification': 'Existing common target, extent and time predicate only; full pre-operand errors, condition satisfaction and source-use admission remain open.'}
            if check['kind'] == 'COMPARE':
                row.update(equal=check['equal'], actualValueDigest=digest(check['actual']),
                           expectedValueDigest=digest(check['expected']),
                           expectedValueSource='ORIGINAL' if check['destination'] is not None else 'PINNED_READER_RULE')
            requirements.append(row)
            pin = by_id[origin['inputRole']]
            rows.append({'requirementId': rid, 'useId': None, 'origin': origin, 'rule': rule,
                         'role': role, 'edgeClass': edge_class,
                         'selectedBinding': row['selectedBinding'], 'selectedInputId': origin['inputRole'],
                         'selectedOriginal': {'ref': pin['ref'], 'digestMode': pin['digestMode'],
                                             'rawSha256': pin['rawSha256'], 'byteLength': pin['byteLength'],
                                             'inventoryStatus': results[origin['inputRole']]['status']},
                         'dependsOn': dependencies, 'disposition': status})
            position['commonScopeRequirementIds'].append(rid)
            if status == 'NOT_EVALUATED':
                frontier(role, origin['inputRole'], origin['pointer'], code, rid)

    def condition_preoperand_gate(stage, position, intent_id, atom_pointer):
        """Replay the actual prefix over its observed, independently selected reads."""
        by_requirement = {row['id']: row for row in requirements}
        trace_ids = [*position['initialInputRequirementIds'], *position.get('rowSourceRequirementIds', [])]
        trace = [by_requirement[rid] for rid in trace_ids]
        condition_id = position['selectedInputId']
        condition = admitted[condition_id]
        work_id = position['origin']['inputRole']
        work = admitted[work_id]
        atom = json_pointer(admitted[intent_id], atom_pointer)
        catalog = {}
        catalog_unavailable = False
        # Include the current condition for origin lookup, but do not invent a
        # second read of it in the evaluator's prefix reference sequence.
        for read_row in [by_requirement[position['readRequirementId']], *trace]:
            if read_row['structuralSelection'] != 'PASS':
                continue
            source = selected_record(read_row['selectedBinding'], read_row['role'],
                read_row['origin']['inputRole'], read_row['origin']['pointer'], read_row['id'])
            if source is None:
                catalog_unavailable = True
                continue
            iid, record = source
            if iid in catalog and catalog[iid]['binding'] != read_row['selectedBinding']:
                catalog_unavailable = True
                continue
            catalog[iid] = {'id': iid, 'binding': read_row['selectedBinding'], 'record': record}
        schemas = condition_schema_cache['schemas']
        if schemas is None and not condition_schema_cache['attempted']:
            condition_schema_cache['attempted'] = True
            try:
                schemas = condition_schema_cache['schemas'] = _condition_source_schemas()
            except Exception:
                pass
        checked, report, reason = None, None, None
        if catalog_unavailable or schemas is None:
            reason = 'PREOPERAND_ORIGINAL_OR_SCHEMA_UNAVAILABLE'
        else:
            try:
                checked = evaluate_preoperand(condition, atom, list(catalog.values()), schemas,
                    condition_binding=position['selectedBinding'],
                    condition_binding_origin={'inputRole': work_id,
                        'pointer': position['origin']['pointer'] + '/definitionBinding'},
                    work_specification_binding=stage['workBinding'], procedure_binding=work['procedure'])
                report = checked['report']
                if report is None or checked['readerKind'] != 'CRITERION_MEASUREMENT':
                    reason = 'PREOPERAND_GENERIC_READER_UNAVAILABLE'
                elif any(error.get('code') in {'SCHEMA_NOT_IN_PINNED_REGISTRY', 'SCHEMA_RESOLUTION_ERROR'}
                         for error in report['errors']):
                    reason = 'PREOPERAND_SOURCE_SCHEMA_UNAVAILABLE'
            except (InputError, KeyError, ValueError, TypeError, ImportError, AttributeError):
                reason = 'PREOPERAND_READER_INTERPRETATION_UNAVAILABLE'
        expected_refs = [{'role': row['role'], 'binding': row['selectedBinding']} for row in trace]
        expected_ids = sorted({row['inputIds'][0] for row in trace
                               if row['structuralSelection'] == 'PASS' and row['inputIds']})
        actual_refs = ([{'role': item['role'], 'binding': item['binding']}
                        for item in report['requiredReferences']] if report is not None else None)
        reconciled = (reason is None and actual_refs == expected_refs
                      and report['sourceInputIds'] == expected_ids)
        if reason is None and not reconciled:
            reason = 'PREOPERAND_READ_TRACE_MISMATCH'
        if not reconciled:
            gate_state, disposition = 'UNRESOLVED', 'NOT_EVALUATED'
        elif not checked['reachedOperandBoundary']:
            gate_state = 'INITIAL_INPUTS_NOT_RESOLVED'
            disposition = 'FAIL' if report['errors'] else 'NOT_EVALUATED'
            reason = 'PREOPERAND_INITIAL_INPUTS_NOT_RESOLVED'
        elif report['errors']:
            gate_state, disposition, reason = 'BLOCKED_BY_READER_ERRORS', 'FAIL', 'PREOPERAND_READER_ERRORS'
        else:
            gate_state, disposition, reason = 'NO_PREOPERAND_ERRORS', 'NOT_EVALUATED', 'PREOPERAND_GATE_REACHED_WITHOUT_ERRORS'
        dependencies = list(dict.fromkeys([stage['id'], position['readRequirementId'], *trace_ids,
            *position.get('propertyMeaningRequirementIds', []), *position.get('fixedUnitRequirementIds', []),
            *position.get('fixedQuantityKindRequirementIds', []),
            *position.get('fixedOperatorRequirementIds', []),
            *position.get('fixedPredicateKindRequirementIds', []),
            *position.get('fixedThresholdDecimalRequirementIds', []),
            *position.get('fixedThresholdQualifierRequirementIds', []),
            *position.get('commonScopeRequirementIds', [])]))
        observations = [{'inputRole': intent_id, 'pointer': atom_pointer, 'valueDigest': digest(atom)}]
        for iid in dict.fromkeys([work_id, condition_id, *catalog]):
            observations.append({'inputRole': iid, 'pointer': '', 'valueDigest': digest(admitted[iid])})
        rule_names = ('condition_sources.py', 'activity_condition_meanings.py', 'completion_count_meanings.py',
                      'irrigation_sources.py', 'sanitation_sources.py', 'drying_sources.py',
                      'sample_collection_sources.py', 'components/revision-02/time_validation.py')
        rule = {'module': 'condition_sources.py', 'moduleRawSha256': rule_hashes['condition_sources.py'],
                'readerRule': 'evaluate_preoperand', 'atomPointer': atom_pointer,
                'semanticModuleRawSha256': {name: sha((HERE / name).read_bytes()) for name in rule_names}}
        rid = 'nested-source:' + str(len(rows))
        origin = {'inputRole': condition_id, 'pointer': ''}
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': 'WORK_CONDITION_PREOPERAND_GATE', 'edgeClass': 'CONDITIONAL',
               'origin': origin, 'rule': rule, 'selectedBinding': position['selectedBinding'],
               'inputIds': list(dict.fromkeys(item['inputRole'] for item in observations)),
               'dependsOn': dependencies, 'findingIds': ['AR_BODY'], 'observations': observations,
               'gateState': gate_state, 'readTraceReconciled': reconciled,
               'readRequirementIds': trace_ids, 'catalogInputIds': list(catalog),
               'reachedOperandBoundary': checked['reachedOperandBoundary'] if checked else False,
               'readerReport': report,
               'readerReportProvenance': 'DERIVED_DIAGNOSTICS_NOT_ORIGINAL_OBSERVATIONS',
               'claimOriginBinding': {'readerInputRole': 'ATOM:' + atom['atomId'],
                                      'inputRole': intent_id, 'pointer': atom_pointer},
               'resolvedInputIds': checked['resolvedInputIds'] if checked else None,
               'structuralSelection': disposition, 'disposition': disposition,
               'diagnostics': [{'code': reason}],
               'qualification': 'Existing generic reader prefix only. No condition satisfaction, source-use admission, complete read closure or publication readiness is established.'}
        requirements.append(row)
        pin = by_id[condition_id]
        rows.append({'requirementId': rid, 'useId': None, 'origin': origin, 'rule': rule,
                     'role': row['role'], 'edgeClass': 'CONDITIONAL', 'selectedBinding': row['selectedBinding'],
                     'selectedInputId': condition_id,
                     'selectedOriginal': {'ref': pin['ref'], 'digestMode': pin['digestMode'],
                                         'rawSha256': pin['rawSha256'], 'byteLength': pin['byteLength'],
                                         'inventoryStatus': results[condition_id]['status']},
                     'dependsOn': dependencies, 'disposition': disposition})
        position['preOperandGateRequirementId'] = rid
        position['preOperandGateState'] = gate_state
        if gate_state != 'NO_PREOPERAND_ERRORS':
            frontier('WORK_CONDITION_OPERAND_READS', condition_id, '', reason, rid)
        return row, catalog, schemas

    def condition_operand_continuation(stage, position, resolved, prefix, read, intent_id, atom_pointer):
        """Collect the selected operand original and replay actual C04 construction."""
        gate, prior_catalog, schemas = prefix
        if (not gate['readTraceReconciled'] or not gate['reachedOperandBoundary']
                or gate['gateState'] != 'NO_PREOPERAND_ERRORS' or resolved is None):
            return
        condition_id = position['selectedInputId']
        condition = admitted[condition_id]
        work_id = position['origin']['inputRole']
        work = admitted[work_id]
        atom = json_pointer(admitted[intent_id], atom_pointer)
        method, measurement = resolved[1:3]
        method_id = gate['resolvedInputIds']['method']
        measurement_id = gate['resolvedInputIds']['measurement']
        request, reason = None, None
        guards = [{'inputRole': measurement_id, 'pointer': '/result/resultKind',
                   'valueDigest': digest(measurement['result']['resultKind'])}]
        before = len(position['initialInputRequirementIds'])
        try:
            request = condition_operand_source_request(method, measurement)
            if request is not None:
                if request['role'] == 'WORK_CONDITION_ORIGINAL_SCALAR':
                    guards.append({'inputRole': method_id, 'pointer': '/scalarSource/parameterIndex',
                                   'valueDigest': digest(method['scalarSource']['parameterIndex'])})
                read(method, request['pointer'], request['schemaId'], request['role'], (method, measurement))
        except (InputError, KeyError, ValueError, TypeError, ImportError, AttributeError):
            reason = 'OPERAND_SOURCE_SELECTION_OR_INTERPRETATION_UNAVAILABLE'
        operand_ids = position['initialInputRequirementIds'][before:]
        del position['initialInputRequirementIds'][before:]
        position['operandInputRequirementIds'] = operand_ids
        by_requirement = {item['id']: item for item in requirements}
        catalog = dict(prior_catalog)
        for rid in operand_ids:
            selected = by_requirement[rid]
            selected['guardObservations'] = guards
            if selected['structuralSelection'] != 'PASS':
                continue
            source = selected_record(selected['selectedBinding'], selected['role'], method_id,
                                     request['pointer'], rid)
            if source is None:
                reason = 'OPERAND_SELECTED_ORIGINAL_UNAVAILABLE'
                continue
            iid, record = source
            if iid in catalog and catalog[iid]['binding'] != selected['selectedBinding']:
                reason = 'OPERAND_ORIGINAL_BINDING_CONFLICT'
                continue
            catalog[iid] = {'id': iid, 'binding': selected['selectedBinding'], 'record': record}
        trace_ids = [*gate['readRequirementIds'], *operand_ids]
        trace = [by_requirement[rid] for rid in trace_ids]
        checked, report = None, None
        if reason is None:
            try:
                checked = evaluate_precriterion(condition, atom, list(catalog.values()), schemas,
                    condition_binding=position['selectedBinding'],
                    condition_binding_origin={'inputRole': work_id,
                        'pointer': position['origin']['pointer'] + '/definitionBinding'},
                    work_specification_binding=stage['workBinding'], procedure_binding=work['procedure'])
                report = checked['report']
                if report is None or checked['readerKind'] != 'CRITERION_MEASUREMENT':
                    reason = 'PRECRITERION_GENERIC_READER_UNAVAILABLE'
                elif any(error.get('code') in {'SCHEMA_NOT_IN_PINNED_REGISTRY', 'SCHEMA_RESOLUTION_ERROR'}
                         for error in report['errors']):
                    reason = 'PRECRITERION_SCHEMA_UNAVAILABLE'
            except (InputError, KeyError, ValueError, TypeError, ImportError, AttributeError):
                reason = 'PRECRITERION_READER_INTERPRETATION_UNAVAILABLE'
        expected_refs = [{'role': item['role'], 'binding': item['selectedBinding']} for item in trace]
        expected_ids = sorted({item['inputIds'][0] for item in trace
                               if item['structuralSelection'] == 'PASS' and item['inputIds']})
        actual_refs = ([{'role': item['role'], 'binding': item['binding']}
                        for item in report['requiredReferences']] if report is not None else None)
        reconciled = (reason is None and actual_refs == expected_refs
                      and report['sourceInputIds'] == expected_ids)
        if reason is None and not reconciled:
            reason = 'PRECRITERION_READ_TRACE_MISMATCH'
        if not reconciled:
            state, disposition = 'UNRESOLVED', 'NOT_EVALUATED'
        else:
            # Interval/domain errors do not add a gate before criterion entry.
            state = 'CRITERION_ENTRY_REACHED' if checked['reachedCriterionEntry'] else 'CONSTRUCTION_STOPPED'
            disposition = 'FAIL' if report['errors'] else 'NOT_EVALUATED'
            reason = 'RECURSIVE_CRITERION_READS_PENDING' if checked['reachedCriterionEntry'] else 'DERIVED_CRITERION_CONSTRUCTION_STOPPED'
        observations = [*gate['observations'], *guards]
        for iid in (key for key in catalog if key not in prior_catalog):
            observations.append({'inputRole': iid, 'pointer': '', 'valueDigest': digest(admitted[iid])})
        rid = 'nested-source:' + str(len(rows))
        dependencies = list(dict.fromkeys([gate['id'], *trace_ids]))
        rule = {'module': 'condition_sources.py', 'moduleRawSha256': rule_hashes['condition_sources.py'],
                'readerRule': 'evaluate_precriterion', 'atomPointer': atom_pointer,
                'sourceSelector': 'condition_operand_source_request',
                'semanticModuleRawSha256': gate['rule']['semanticModuleRawSha256']}
        criterion_schema_id = 'https://ofarm.dev/schema/drafts/non-default/assertion-domain/proposition/v0.1'
        criterion_schema = schemas.schemas.get(criterion_schema_id)
        rule['derivedCriterionSchema'] = {'id': criterion_schema_id, 'definition': 'C04',
            'documentValueDigest': digest(criterion_schema) if criterion_schema is not None else None}
        origin = {'inputRole': condition_id, 'pointer': ''}
        derived = checked['derivedCriterion'] if checked is not None else None
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': 'WORK_CONDITION_PRECRITERION_GATE', 'edgeClass': 'CONDITIONAL',
               'origin': origin, 'rule': rule, 'selectedBinding': position['selectedBinding'],
               'inputIds': list(dict.fromkeys(item['inputRole'] for item in observations)),
               'dependsOn': dependencies, 'findingIds': ['AR_BODY'], 'observations': observations,
               'gateState': state, 'readTraceReconciled': reconciled,
               'preOperandGateRequirementId': gate['id'], 'readRequirementIds': trace_ids,
               'operandInputRequirementIds': operand_ids, 'catalogInputIds': list(catalog),
               'operandSourceRequest': request, 'guardObservations': guards,
               'reachedCriterionEntry': bool(checked and checked['reachedCriterionEntry']),
               'readerReport': report, 'readerReportProvenance': 'DERIVED_DIAGNOSTICS_NOT_ORIGINAL_OBSERVATIONS',
               'claimOriginBinding': gate['claimOriginBinding'],
               'derivedCriterion': derived, 'derivedCriterionDigest': digest(derived) if derived is not None else None,
               'derivedCriterionProvenance': 'CONSTRUCTED_FROM_SELECTED_INPUTS_NOT_AN_ORIGINAL',
               'criterionSchemaErrors': checked['criterionSchemaErrors'] if checked is not None else None,
               'structuralSelection': disposition, 'disposition': disposition,
               'diagnostics': [{'code': reason}],
               'qualification': 'Actual operand-source read and derived C04 construction only. Criterion entry is not criterion satisfaction, source admission or complete read closure.'}
        requirements.append(row)
        pin = by_id[condition_id]
        rows.append({'requirementId': rid, 'useId': None, 'origin': origin, 'rule': rule,
                     'role': row['role'], 'edgeClass': 'CONDITIONAL', 'selectedBinding': row['selectedBinding'],
                     'selectedInputId': condition_id,
                     'selectedOriginal': {'ref': pin['ref'], 'digestMode': pin['digestMode'],
                                         'rawSha256': pin['rawSha256'], 'byteLength': pin['byteLength'],
                                         'inventoryStatus': results[condition_id]['status']},
                     'dependsOn': dependencies, 'disposition': disposition})
        position['preCriterionGateRequirementId'] = rid
        position['preCriterionGateState'] = state
        if reconciled and state == 'CRITERION_ENTRY_REACHED':
            condition_criterion_continuation(stage, position, resolved, row, schemas,
                                             gate['resolvedInputIds'])
        else:
            frontier('WORK_CONDITION_CRITERION_READS', condition_id, '', reason, rid)

    def condition_criterion_continuation(stage, position, resolved, entry, schemas, initial_ids,
                                        *, submitted_atom=None, submitted_pointer=None):
        """Record the real criterion reader's ordered reads and original selectors."""
        if (submitted_atom is None and (not entry['readTraceReconciled'] or entry['gateState'] != 'CRITERION_ENTRY_REACHED'
                or not entry['reachedCriterionEntry'] or entry['derivedCriterion'] is None)):
            return
        condition_id = position['selectedInputId']
        condition = admitted[condition_id]
        is_submitted = submitted_atom is not None
        criterion_atom = submitted_atom if is_submitted else entry['derivedCriterion']
        if is_submitted:
            method = measurement = None
            original_ids = {}
        else:
            method, measurement = resolved[1:3]
            original_ids = {'condition': condition_id, 'method': initial_ids['method'],
                           'measurement': initial_ids['measurement']}
        catalog, reason, checked, report = {}, None, None, None
        trace_ids, shape_ids = [], []
        position['criterionReadRequirementIds'] = trace_ids
        # Make available only the same independently nominated, byte-matched
        # JSON values accepted by selected_record. The reader checks object
        # shape only for values it consumes. Supplying a catalog is
        # not a read; only actual resolve events below become occurrences.
        for iid, pin in by_id.items():
            if pin['digestMode'] != 'JCS_JSON' or results[iid]['status'] != 'MATCHED':
                continue
            binding = {'ref': pin['ref'], 'digest': pin['wholeJcsDigest']}
            if not any(iid in item['inputIds'] for item in nominations[canonical(binding)]):
                continue
            selected = selected_record(binding, 'WORK_CONDITION_CRITERION_CATALOG',
                                       condition_id, '', entry['id'], object_only=False)
            if selected is None:
                reason = 'CRITERION_CATALOG_ORIGINAL_UNAVAILABLE'
                continue
            selected_id, record = selected
            catalog[selected_id] = {'id': selected_id, 'binding': binding, 'record': record,
                                   'rawSha256': pin['rawSha256'], 'valueDigest': pin['wholeJcsDigest']}
        source_map = {}
        if reason is None:
            try:
                if not is_submitted:
                    source_map = condition_criterion_binding_origins(condition, method, measurement)
                from condition_property_resolution import catalog as property_catalog
                scoped_catalog = (list(catalog.values()) if is_submitted else
                                  property_catalog(list(catalog.values()), bound, method_id=initial_ids['method']))
                checked = evaluate_criterion_traced(criterion_atom, scoped_catalog, schemas,
                                                    claim_origin='ACTUAL_ATOM' if is_submitted else None)
                report = checked['report']
            except (InputError, KeyError, ValueError, TypeError, ImportError, AttributeError):
                reason = 'CRITERION_READER_INTERPRETATION_UNAVAILABLE'
        available_parents = {}
        observations = list(entry['observations'])
        guard_rows = {}
        guard_facts = {fact['id']: fact for fact in checked.get('guards', [])} if checked else {}
        if checked is not None and len(guard_facts) != len(checked.get('guards', [])):
            reason = 'CRITERION_DUPLICATE_GUARD_ID'

        def original_guard_operand(operand):
            if operand['kind'] == 'ORIGINAL':
                iid, path = operand['inputRole'], operand['pointer']
                if iid not in available_parents:
                    raise ValueError('Guard source was not returned by an earlier valid read.')
            elif operand['kind'] == 'ACTUAL_ATOM' and is_submitted:
                iid, path = condition_id, submitted_pointer + operand['pointer']
            elif operand['kind'] == 'DERIVED_CRITERION' and not is_submitted:
                mapped = source_map[operand['pointer']]
                iid, path = original_ids[mapped['recordKind']], mapped['pointer']
                if not same(json_pointer(criterion_atom, operand['pointer']), json_pointer(admitted[iid], path)):
                    raise ValueError('Derived guard operand differs from its original.')
            else:
                raise ValueError('Guard origin does not belong to this criterion invocation.')
            return {'inputRole': iid, 'pointer': path, 'valueDigest': digest(json_pointer(admitted[iid], path))}

        def retain_guard(gid):
            if gid in guard_rows: return guard_rows[gid]
            fact = guard_facts[gid]
            if type(fact['satisfied']) is not bool:
                raise ValueError('Reader guard result is not boolean.')
            indices = fact['readIndices']
            if any(type(index) is not int or index < 0 or index >= len(trace_ids) for index in indices):
                raise ValueError('Reader guard depends on an unavailable read occurrence.')
            guard_observations = [original_guard_operand(operand) for operand in fact['operands']]
            origin = guard_observations[0] if guard_observations else {'inputRole': condition_id,
                'pointer': submitted_pointer if is_submitted else ''}
            origin = {key: origin[key] for key in ('inputRole', 'pointer')}
            row = emit_reader_guard(entry['id'], origin, position['selectedBinding'], 'criterion_sources.py',
                                    fact, [trace_ids[index] for index in indices], guard_observations)
            guard_rows[gid] = row
            observations.extend(guard_observations)
            return row

        if checked is not None:
            for index, event in enumerate(checked['reads']):
                try:
                    binding = event['binding']
                    reader_origin = event['bindingOrigin']
                    guards = []
                    if reader_origin['kind'] == 'DERIVED_CRITERION':
                        selected_origin = source_map[reader_origin['pointer']]
                        origin_id = original_ids[selected_origin['recordKind']]
                        pointer = selected_origin['pointer']
                        parent_read = entry['id']
                        for guard in selected_origin.get('guards', []):
                            iid = original_ids[guard['recordKind']]
                            guards.append({'inputRole': iid, 'pointer': guard['pointer'],
                                           'valueDigest': digest(json_pointer(admitted[iid], guard['pointer']))})
                        if not same(json_pointer(criterion_atom, reader_origin['pointer']), binding):
                            raise ValueError('Derived selector does not match the actual request.')
                    elif reader_origin['kind'] == 'ORIGINAL':
                        origin_id, pointer = reader_origin['inputRole'], reader_origin['pointer']
                        # A recursive parent must have been returned by an
                        # earlier actual read with a valid source shape.
                        parent_read = available_parents[origin_id]
                    elif reader_origin['kind'] == 'ACTUAL_ATOM' and is_submitted:
                        origin_id, pointer = condition_id, submitted_pointer + reader_origin['pointer']
                        parent_read = entry['id']
                    else:
                        raise ValueError('A constructed criterion is not submitted atom bytes.')
                    if not same(json_pointer(admitted[origin_id], pointer), binding):
                        raise ValueError('Original selector does not match the actual request.')
                    matches = [item for item in catalog.values() if same(item['binding'], binding)]
                    if (not is_submitted and event['role'] == 'CRITERION_OBSERVED_PROPERTY_DEFINITION'
                            and pointer == '/propertyBinding' and origin_id == initial_ids['method']
                            and isinstance(binding, dict) and 'revisionRef' in binding):
                        from condition_property_resolution import ConditionSources
                        if isinstance(scoped_catalog, ConditionSources):
                            matches = scoped_catalog.property_for(admitted[origin_id], recursive=True)
                    selected_id = matches[0]['id'] if len(matches) == 1 else None
                    if event['matchCount'] != len(matches) or event['selectedInputId'] != selected_id:
                        raise ValueError('Reader selection disagrees with the admitted catalog.')
                    schema_id = event['schemaId']
                    shape = schemas.errors(schema_id, matches[0]['record']) if selected_id is not None else None
                    if event['schemaErrors'] != shape:
                        raise ValueError('Reader shape result disagrees with the selected original.')
                    read_guards = [retain_guard(gid) for gid in event['guardIds']]
                    if any(not guard['guardSatisfied'] for guard in read_guards):
                        raise ValueError('A read followed an unsatisfied actual reader guard.')
                except (InputError, KeyError, ValueError, TypeError, AttributeError):
                    reason = 'CRITERION_READ_PROVENANCE_OR_SELECTION_MISMATCH'
                    break
                row = emit(parent_read, origin_id, pointer, binding, event['role'],
                           'criterion_sources.py', 'evaluate_traced',
                           condition_property=not is_submitted and origin_id == initial_ids['method'],
                           additional_dependencies=(entry['id'], *[guard['id'] for guard in read_guards]))
                row['rule'].update(readerRule='evaluate_traced', sourceSchemaId=schema_id)
                schema = schemas.schemas.get(schema_id)
                if schema is not None:
                    row['rule']['sourceSchemaDigest'] = digest(schema)
                row.update(criterionReadIndex=index, readerBindingOrigin=reader_origin,
                           readerPrefixReadRequirementIds=list(trace_ids), guardObservations=guards,
                           readerSchemaErrors=shape, readerGuardRequirementIds=[guard['id'] for guard in read_guards])
                trace_ids.append(row['id'])
                expanded.append(origin_id)
                observations.extend([{'inputRole': origin_id, 'pointer': pointer,
                                      'valueDigest': digest(binding)}, *guards])
                if selected_id is not None:
                    observations.append({'inputRole': selected_id, 'pointer': '',
                                         'valueDigest': digest(admitted[selected_id])})
                if schema is None or (shape is not None and any(item.get('code') in
                        {'SCHEMA_NOT_IN_PINNED_REGISTRY', 'SCHEMA_RESOLUTION_ERROR'} for item in shape)):
                    reason = 'CRITERION_SOURCE_SCHEMA_UNAVAILABLE'
                    frontier(event['role'], origin_id, pointer, reason, row['id'])
                elif shape:
                    schema_module = schemas.definition_source_modules.get(
                        schema_id, 'components/revision-02/runtime_support.py')
                    failed = source_shape_failure(row['id'], selected_id, binding,
                        event['role'] + '_SOURCE_SHAPE', 'criterion_sources.py', schema_module,
                        'CRITERION_INPUT_SOURCE_SCHEMA_INVALID', additional_dependencies=(entry['id'],))
                    failed['rule'].update(sourceSchemaId=schema_id, sourceSchemaDigest=digest(schema))
                    shape_ids.append(failed['id'])
                elif selected_id is not None:
                    available_parents[selected_id] = row['id']
                if row['structuralSelection'] != 'PASS':
                    frontier(event['role'], origin_id, pointer,
                             'CRITERION_INPUT_SELECTION_UNRESOLVED', row['id'])
            if reason is None:
                try:
                    for gid in guard_facts: retain_guard(gid)
                except (InputError, KeyError, ValueError, TypeError, AttributeError):
                    reason = 'CRITERION_GUARD_PROVENANCE_OR_DEPENDENCY_MISMATCH'
        by_requirement = {item['id']: item for item in requirements}
        trace = [by_requirement[rid] for rid in trace_ids]
        expected_refs = [{'role': item['role'], 'binding': item['selectedBinding']} for item in trace]
        expected_ids = sorted({item['inputIds'][0] for item in trace
                               if item['structuralSelection'] == 'PASS' and item['inputIds']})
        actual_refs = ([{'role': item['role'], 'binding': item['binding']}
                        for item in report['requiredReferences']] if report is not None else None)
        reconciled = (reason is None and actual_refs == expected_refs
                      and report['sourceInputIds'] == expected_ids
                      and len(checked['reads']) == len(trace))
        if reason is None and not reconciled:
            reason = 'CRITERION_READ_TRACE_MISMATCH'
        state = 'READ_TRACE_RECONCILED' if reconciled else 'UNRESOLVED'
        disposition = 'FAIL' if reconciled and report['errors'] else 'NOT_EVALUATED'
        if reason is None:
            reason = 'CRITERION_READER_TRACE_RECONCILED_SOURCE_USE_PENDING'
        rid = 'nested-source:' + str(len(rows))
        origin = {'inputRole': condition_id, 'pointer': ''}
        rule = {'module': 'criterion_sources.py', 'moduleRawSha256': rule_hashes['criterion_sources.py'],
                'readerRule': 'evaluate_traced', 'claimOrigin': 'ACTUAL_ATOM' if is_submitted else None,
                **({} if is_submitted else {'derivedOriginRule': 'condition_criterion_binding_origins',
                   'derivedOriginModuleRawSha256': rule_hashes['condition_sources.py']}),
                'semanticModuleRawSha256': {name: sha((HERE / name).read_bytes()) for name in (
                    'definition_inputs.py', 'completion_count_meanings.py', 'extent_temporal.py',
                    'strict_inputs.py', 'components/revision-02/runtime_support.py',
                    'components/revision-02/time_validation.py', 'components/revision-02/meaning_comparisons.py')}}
        dependencies = list(dict.fromkeys([entry['id'], *trace_ids, *shape_ids,
                                          *[guard['id'] for guard in guard_rows.values()]]))
        blocked_reads = [item['id'] for item in trace
                         if item['structuralSelection'] != 'PASS' or item.get('readerSchemaErrors')]
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': 'SUBMITTED_CRITERION_TRACE' if is_submitted else 'WORK_CONDITION_CRITERION_TRACE', 'edgeClass': 'CONDITIONAL',
               'origin': origin, 'rule': rule, 'selectedBinding': position['selectedBinding'],
               'inputIds': list(dict.fromkeys(item['inputRole'] for item in observations)),
               'dependsOn': dependencies, 'findingIds': ['AR_BODY'], 'observations': observations,
               'traceState': state, 'readTraceReconciled': reconciled,
               'preCriterionGateRequirementId': None if is_submitted else entry['id'], 'readRequirementIds': trace_ids,
               'guardRequirementIds': [guard['id'] for guard in guard_rows.values()],
               'readerReport': report, 'readerReadTrace': checked['reads'] if checked is not None else None,
               'readerReportProvenance': 'DERIVED_DIAGNOSTICS_NOT_ORIGINAL_OBSERVATIONS',
               **({'actualAtomOrigin': {'inputRole': condition_id, 'pointer': submitted_pointer}}
                  if is_submitted else {'derivedCriterionDigest': entry['derivedCriterionDigest'],
                     'derivedCriterionProvenance': 'CONSTRUCTED_FROM_SELECTED_INPUTS_NOT_AN_ORIGINAL'}),
               'readerCoverage': {'reader': 'criterion_sources.evaluate', 'useRequirementId': entry['id'],
                   'status': ('UNRESOLVED' if not reconciled else 'BLOCKED_SOURCE_PATH' if blocked_reads else 'ACTUAL_PATH_RECONCILED'),
                   'blockedReadRequirementIds': blocked_reads,
                   'knownReadInputsResolved': reconciled and not blocked_reads,
                   'semanticDisposition': report['disposition'] if report is not None else 'NOT_EVALUATED'},
               'structuralSelection': disposition, 'disposition': disposition,
               'diagnostics': [{'code': reason}],
               'qualification': 'Actual recursive criterion read occurrences only. Derived diagnostics create no protected-read use; source-use admission, complete domain closure and publication remain open.'}
        requirements.append(row)
        pin = by_id[condition_id]
        rows.append({'requirementId': rid, 'useId': None, 'origin': origin, 'rule': rule,
                     'role': row['role'], 'edgeClass': 'CONDITIONAL', 'selectedBinding': row['selectedBinding'],
                     'selectedInputId': condition_id,
                     'selectedOriginal': {'ref': pin['ref'], 'digestMode': pin['digestMode'],
                                         'rawSha256': pin['rawSha256'], 'byteLength': pin['byteLength'],
                                         'inventoryStatus': results[condition_id]['status']},
                     'dependsOn': dependencies, 'disposition': disposition})
        position['criterionTraceRequirementId'] = rid
        position['criterionTraceState'] = state
        frontier('WORK_CONDITION_CRITERION_SOURCE_USE', condition_id, '', reason, rid)

    def sample_relation_continuation(parent, intent_id, atom_pointer, atom):
        """Use the original sample reader's exact selectors and continuation."""
        catalog, reason, checked = {}, None, None
        trace_ids, shape_ids, guard_rows, available_parents = [], [], {}, {}
        selector_read_ids = []
        observations = [{'inputRole': intent_id, 'pointer': atom_pointer, 'valueDigest': digest(atom)}]
        if not condition_schema_cache['attempted']:
            condition_schema_cache['attempted'] = True
            try: condition_schema_cache['schemas'] = _condition_source_schemas()
            except (ValueError, ImportError, AttributeError): pass
        schemas = condition_schema_cache['schemas']
        for iid, pin in by_id.items():
            if pin['digestMode'] != 'JCS_JSON' or results[iid]['status'] != 'MATCHED': continue
            binding = {'ref': pin['ref'], 'digest': pin['wholeJcsDigest']}
            if not any(iid in item['inputIds'] for item in nominations[canonical(binding)]): continue
            original = selected_record(binding, 'SAMPLE_RELATION_CATALOG', intent_id, atom_pointer,
                                       parent['id'], object_only=False)
            if original is not None:
                catalog[iid] = {'id': iid, 'binding': binding, 'record': original[1],
                                'rawSha256': pin['rawSha256'], 'valueDigest': pin['wholeJcsDigest']}
        try:
            if schemas is None: raise ValueError('Sample reader schemas unavailable.')
            checked = evaluate_sample_relation_traced(atom, list(catalog.values()), schemas)
        except (InputError, ValueError, KeyError, TypeError, ImportError, AttributeError):
            reason = 'SAMPLE_RELATION_READER_OR_SCHEMA_UNAVAILABLE'

        def actual_origin(value):
            if value['kind'] == 'ACTUAL_ATOM':
                return intent_id, atom_pointer + value['pointer'], parent['id']
            if value['kind'] == 'ORIGINAL':
                return value['inputRole'], value['pointer'], available_parents[value['inputRole']]
            raise ValueError('Sample reader origin is not an actual original.')

        guard_facts = {fact['id']: fact for fact in checked['guards']} if checked else {}
        def retain_guard(gid):
            if gid in guard_rows: return guard_rows[gid]
            fact = guard_facts[gid]
            if type(fact['satisfied']) is not bool: raise ValueError('Guard result must be boolean.')
            if any(type(index) is not int or not 0 <= index < len(trace_ids) for index in fact['readIndices']):
                raise ValueError('Guard read dependency is not earlier in the actual trace.')
            operands = []
            for operand in fact['operands']:
                iid, path, _parent = actual_origin(operand)
                operands.append({'inputRole': iid, 'pointer': path, 'valueDigest': digest(json_pointer(admitted[iid], path))})
            selector_dependencies = []
            for candidate in fact.get('selectionReads', []):
                iid, path, origin_parent = actual_origin(candidate['bindingOrigin'])
                selected_id = candidate['selectedInputId']
                selected = catalog[selected_id]
                if (not same(json_pointer(admitted[iid], path), candidate['binding'])
                        or not same(selected['binding'], candidate['binding'])
                        or digest(json_pointer(selected['record'], candidate['sourcePointer'])) != candidate['sourceValueDigest']):
                    raise ValueError('Sample selector inspection differs from its independently selected original.')
                observed = {'inputRole': selected_id, 'pointer': candidate['sourcePointer'],
                            'valueDigest': candidate['sourceValueDigest']}
                selected_row = emit(origin_parent, iid, path, candidate['binding'],
                    'SAMPLE_TARGET_RELATION_CANDIDATE', 'sample_relation_sources.py',
                    'evaluate_traced.selectionReads', additional_dependencies=(parent['id'],))
                if selected_row['structuralSelection'] != 'PASS':
                    raise ValueError('Sample selector inspection is not an independently selected original.')
                selected_row.update(observations=[observed], selectorInspection=candidate,
                                    sourceReadAttempted=True)
                selector_read_ids.append(selected_row['id'])
                selector_dependencies.append(selected_row['id'])
                operands.append(observed)
            origin = ({key: operands[0][key] for key in ('inputRole', 'pointer')} if operands
                      else {'inputRole': intent_id, 'pointer': atom_pointer})
            row = emit_reader_guard(parent['id'], origin, parent['selectedBinding'], 'sample_relation_sources.py',
                                    fact, [*[trace_ids[index] for index in fact['readIndices']],
                                           *selector_dependencies], operands)
            guard_rows[gid] = row
            observations.extend(operands)
            return row

        if checked is not None:
            try:
                if len(guard_facts) != len(checked['guards']): raise ValueError('Duplicate sample guard ID.')
                for index, event in enumerate(checked['reads']):
                    iid, path, original_parent = actual_origin(event['bindingOrigin'])
                    if not same(json_pointer(admitted[iid], path), event['binding']):
                        raise ValueError('Sample selector differs from its original.')
                    guards = [retain_guard(gid) for gid in event['guardIds']]
                    attempted = event['attempted']
                    if attempted and any(not item['guardSatisfied'] for item in guards):
                        raise ValueError('A sample read followed a false guard.')
                    if not attempted and all(item['guardSatisfied'] for item in guards):
                        raise ValueError('An unattempted sample read has no false guard.')
                    matches = [item for item in catalog.values() if same(item['binding'], event['binding'])] if attempted else []
                    selected = matches[0] if len(matches) == 1 else None
                    shape = schemas.errors(event['schemaId'], selected['record']) if selected is not None else None
                    if (event['matchCount'] != (len(matches) if attempted else None)
                            or event['selectedInputId'] != (selected['id'] if selected else None)
                            or event['schemaErrors'] != shape):
                        raise ValueError('Sample read selection/shape does not reconcile.')
                    row = emit(original_parent, iid, path, event['binding'], event['role'],
                        'sample_relation_sources.py', 'evaluate_traced',
                        additional_dependencies=(parent['id'], *[item['id'] for item in guards]),
                        edge_class='REQUIRED_ORIGINAL_READ' if attempted else 'CONDITIONAL')
                    row.update(readerReadIndex=index, readerGuardRequirementIds=[item['id'] for item in guards],
                               readerSchemaErrors=shape, sourceReadAttempted=attempted,
                               readerReportedReference=event['reportedReference'])
                    schema = schemas.schemas.get(event['schemaId'])
                    row['rule']['sourceSchemaId'] = event['schemaId']
                    if schema is not None:
                        row['rule']['sourceSchemaDigest'] = digest(schema)
                    trace_ids.append(row['id']); expanded.append(iid)
                    observations.append({'inputRole': iid, 'pointer': path, 'valueDigest': digest(event['binding'])})
                    if selected is not None:
                        observations.append({'inputRole': selected['id'], 'pointer': '', 'valueDigest': digest(selected['record'])})
                        if schema is None or (shape is not None and any(item.get('code') in
                                {'SCHEMA_NOT_IN_PINNED_REGISTRY', 'SCHEMA_RESOLUTION_ERROR'} for item in shape)):
                            reason = 'SAMPLE_RELATION_SOURCE_SCHEMA_UNAVAILABLE'
                            frontier(event['role'], iid, path, reason, row['id'])
                        elif shape:
                            failure_role = ('SAMPLE_OUTPUT_SOURCE_SHAPE' if event['role'] == 'SAMPLE_TARGET_OPERATION_OUTPUT_SPECIFICATION'
                                            else 'SAMPLE_RELATION_SOURCE_SHAPE' if event['role'] == 'SAMPLE_TARGET_RELATION_USE'
                                            else event['role'] + '_SOURCE_SHAPE')
                            failure = source_shape_failure(row['id'], selected['id'], event['binding'],
                                failure_role, 'sample_relation_sources.py',
                                schemas.definition_source_modules.get(event['schemaId'], 'components/revision-02/runtime_support.py'),
                                'SAMPLE_RELATION_SOURCE_SCHEMA_INVALID')
                            shape_ids.append(failure['id'])
                        else: available_parents[selected['id']] = row['id']
                for gid in guard_facts: retain_guard(gid)
            except (InputError, ValueError, KeyError, TypeError, AttributeError):
                reason = 'SAMPLE_RELATION_TRACE_OR_GUARD_MISMATCH'
        report = checked['report'] if checked is not None else None
        expected_refs = ([{'role': event['role'], 'binding': event['binding']} for event in checked['reads']
                          if event['reportedReference']] if checked else None)
        actual_refs = ([{'role': item['role'], 'binding': item['binding']} for item in report['requiredReferences']]
                       if report is not None else None)
        expected_ids = sorted({event['selectedInputId'] for event in checked['reads']
                               if event['selectedInputId'] is not None}) if checked else None
        reconciled = (reason is None and expected_refs == actual_refs and expected_ids == report['sourceInputIds']
                      and len(trace_ids) == len(checked['reads']) and len(guard_rows) == len(checked['guards']))
        if not reconciled and reason is None: reason = 'SAMPLE_RELATION_REPORT_TRACE_MISMATCH'
        rid = 'nested-source:' + str(len(rows))
        dependencies = list(dict.fromkeys([parent['id'], *trace_ids, *selector_read_ids, *shape_ids,
                                          *[item['id'] for item in guard_rows.values()]]))
        disposition = 'FAIL' if reconciled and report['errors'] else 'NOT_EVALUATED'
        blocked_reads = ([index for index, event in enumerate(checked['reads'])
                          if event['attempted'] and (event['selectedInputId'] is None or event['schemaErrors'])]
                         if checked else None)
        origin = {'inputRole': intent_id, 'pointer': atom_pointer}
        rule = {'module': 'sample_relation_sources.py', 'moduleRawSha256': rule_hashes['sample_relation_sources.py'],
                'rule': 'evaluate_traced', 'sourcePointer': atom_pointer}
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE', 'role': 'SAMPLE_RELATION_READER_TRACE',
               'edgeClass': 'CONDITIONAL', 'origin': origin, 'rule': rule,
               'selectedBinding': parent['selectedBinding'], 'inputIds': list(dict.fromkeys(item['inputRole'] for item in observations)),
               'dependsOn': dependencies, 'findingIds': ['AR_BODY'], 'observations': observations,
               'readTraceReconciled': reconciled, 'readRequirementIds': trace_ids,
               'selectorReadRequirementIds': selector_read_ids,
               'guardRequirementIds': [item['id'] for item in guard_rows.values()],
               'readerReport': report, 'readerReadTrace': checked['reads'] if checked else None,
               'readerReportProvenance': 'DERIVED_DIAGNOSTICS_NOT_ORIGINAL_OBSERVATIONS',
               'readerCoverage': {'reader': 'sample_relation_sources.evaluate', 'useRequirementId': parent['id'],
                   'status': ('UNRESOLVED' if not reconciled else 'BLOCKED_SOURCE_PATH' if blocked_reads else 'ACTUAL_PATH_RECONCILED'),
                   'semanticDisposition': report['disposition'] if report else 'NOT_EVALUATED',
                   'blockedReadIndices': blocked_reads,
                   'conditionalReadIndices': [index for index, event in enumerate(checked['reads'])
                                             if not event['attempted']] if checked else None},
               'structuralSelection': disposition, 'disposition': disposition,
               'diagnostics': [{'code': reason or 'SAMPLE_RELATION_TRACE_RECONCILED_SOURCE_USE_PENDING'}],
               'qualification': 'Actual sample support reader path and diagnostics only; endpoint identity, evidence eligibility, custody, geometry and representativeness remain separate.'}
        requirements.append(row)
        rows.append({'requirementId': rid, 'useId': None, 'origin': origin, 'rule': rule,
                     'role': row['role'], 'edgeClass': 'CONDITIONAL', 'selectedBinding': parent['selectedBinding'],
                     'selectedInputId': None, 'selectedOriginal': None, 'dependsOn': dependencies, 'disposition': disposition})
        frontier('SAMPLE_RELATION_SOURCE_USE', intent_id, atom_pointer,
                 reason or 'SAMPLE_RELATION_SOURCE_USE_PENDING', rid)

    def condition_initial_inputs(stage, condition_positions, intent_id, atom_pointer):
        """Collect actual initial reads without evaluating condition semantics."""
        if stage['selectedStage'] is None:
            return
        stage['readerConditionPositions'] = []
        positions = [position for _field, _claim, group, _prefix in WORK_CONDITION_GROUPS
                     for position in condition_positions.get(group, [])]
        for position in positions:
            condition_id = position.get('selectedInputId')
            condition = admitted.get(condition_id)
            if (position.get('readStructuralSelection') != 'PASS'
                    or 'sourceShapeRequirementId' in position
                    or not isinstance(condition, dict)):
                if position['stageFromWorkArray'] == stage['selectedStage']:
                    frontier('WORK_CONDITION_INITIAL_INPUTS',
                             position['origin']['inputRole'], position['origin']['pointer'],
                             'CONDITION_ORIGINAL_OR_SHAPE_UNAVAILABLE', stage['id'])
                continue
            # A missing schema dependency must not turn a partly inspected
            # parent into permission to descend. Other local value failures
            # still retain independently known reads from a valid parent.
            parent_status, parent_reason = _candidate_schema_status(
                WORK_SCHEMAS['workCondition'], condition, 'WORK_CONDITION')
            if parent_status != 'PASS':
                frontier('WORK_CONDITION_INITIAL_INPUTS', condition_id, '',
                         parent_reason, stage['id'])
                continue
            if not condition_at_stage(condition, stage['selectedStage']):
                if position['stageFromWorkArray'] == stage['selectedStage']:
                    frontier('WORK_CONDITION_INITIAL_INPUTS', condition_id, '/stage',
                             'CONDITION_STAGE_CONTRADICTS_SELECTED_WORK_ARRAY', stage['id'])
                continue
            reader = condition_reader_kind(condition)
            stage['readerConditionPositions'].append(position)
            stage['dependsOn'][:] = list(dict.fromkeys([
                *stage['dependsOn'], position['readRequirementId'],
                *position['preCarrierComparisonRequirementIds'],
                *([position['canonicalMeaningRequirementId']]
                  if 'canonicalMeaningRequirementId' in position else [])]))
            position['readerKind'] = reader
            position['initialInputRequirementIds'] = []
            position['initialInputsStatus'] = 'NOT_EVALUATED'
            module, reader_rule = {
                'CRITERION_MEASUREMENT': ('condition_sources.py', 'resolve_condition_inputs'),
                'ANALYSIS_OUTPUT': ('analysis_output_sources.py', 'resolve_analysis_inputs'),
                'OBSERVATION_ACQUISITION': ('observation_acquisition_sources.py', 'resolve_acquisition_inputs'),
            }[reader]
            origins = {id(condition): (condition_id, position['readRequirementId'], '')}
            identities = {}
            dependencies = [stage['id'], *position['preCarrierComparisonRequirementIds']]
            if 'canonicalMeaningRequirementId' in position:
                dependencies.append(position['canonicalMeaningRequirementId'])

            def read(parent_record, path, schema_id, role, prerequisites, identity=None):
                origin_id, parent_read, prefix = origins[id(parent_record)]
                pointer = prefix + path
                binding = json_pointer(parent_record, path)
                row = emit(parent_read, origin_id, pointer, binding, role,
                           module, reader_rule,
                           condition_property=reader == 'CRITERION_MEASUREMENT' and role == 'WORK_CONDITION_PROPERTY_DEFINITION',
                           additional_dependencies=(*dependencies,
                               *(origins[id(item)][1] for item in prerequisites),
                               *(identities[id(item)] for item in prerequisites if id(item) in identities)))
                row['rule']['sourceSchemaId'] = schema_id
                position['initialInputRequirementIds'].append(row['id'])
                expanded.append(origin_id)
                if row['structuralSelection'] != 'PASS':
                    frontier(role, origin_id, pointer,
                             'CONDITION_INPUT_SELECTION_UNRESOLVED', row['id'])
                    return None
                selected = selected_record(binding, role, origin_id, pointer, row['id'])
                if selected is None:
                    return None
                input_id, record = selected
                if not condition_schema_cache['attempted']:
                    condition_schema_cache['attempted'] = True
                    try:
                        condition_schema_cache['schemas'] = _condition_source_schemas()
                    except Exception:
                        condition_schema_cache['schemas'] = None
                schemas = condition_schema_cache['schemas']
                if schemas is None:
                    frontier(role, input_id, '', 'CONDITION_INPUT_SCHEMA_UNAVAILABLE', row['id'])
                    return None
                errors = schemas.errors(schema_id, record)
                if any(item['code'] in {'SCHEMA_NOT_IN_PINNED_REGISTRY',
                                        'SCHEMA_RESOLUTION_ERROR'} for item in errors):
                    frontier(role, input_id, '', 'CONDITION_INPUT_SCHEMA_UNAVAILABLE', row['id'])
                    return None
                row['rule']['sourceSchemaDigest'] = digest(schemas.schemas[schema_id])
                if errors:
                    schema_module = schemas.definition_source_modules.get(
                        schema_id, 'components/revision-02/runtime_support.py')
                    shape = source_shape_failure(
                        row['id'], input_id, binding, role + '_SOURCE_SHAPE',
                        module, schema_module,
                        'CONDITION_INPUT_SOURCE_SCHEMA_INVALID',
                        additional_dependencies=dependencies)
                    shape['rule']['sourceSchemaId'] = schema_id
                    shape['rule']['sourceSchemaDigest'] = row['rule']['sourceSchemaDigest']
                    return None
                if identity is not None:
                    actual, expected = record[identity], binding['ref']
                    code = ('SAMPLE_COLLECTION_SOURCE_IDENTITY_MISMATCH' if module == 'sample_collection_sources.py' else
                            'ANALYSIS_SOURCE_IDENTITY_MISMATCH' if reader == 'ANALYSIS_OUTPUT'
                            else 'OBSERVATION_ACQUISITION_SOURCE_IDENTITY_MISMATCH')
                    fact = work_canonical_fact(row['id'], binding,
                        ('O10_COLLECTION_SOURCE_IDENTITY_COMPARISON' if module == 'sample_collection_sources.py' else
                         'O22_INITIAL_SOURCE_IDENTITY_COMPARISON' if reader == 'ANALYSIS_OUTPUT' else
                         'O09_INITIAL_SOURCE_IDENTITY_COMPARISON' if reader_rule == 'resolve_acquisition_inputs' else
                         'O09_REQUIRED_SOURCE_IDENTITY_COMPARISON'),
                        {'inputRole': input_id, 'pointer': '/' + identity}, actual, expected,
                        same(actual, expected), code,
                        [{'side': 'ORIGINAL', 'inputRole': input_id, 'pointer': '/' + identity, 'valueDigest': digest(actual)},
                         {'side': 'BINDING', 'inputRole': origin_id, 'pointer': pointer + '/ref', 'valueDigest': digest(expected)}],
                        rule_details={'module': module, 'moduleRawSha256': rule_hashes[module], 'readerRule': reader_rule})
                    fact['qualification'] = 'Local original identity comparison only; source-use admission and condition semantics remain open.'
                    identities[id(record)] = fact['id']
                    if not same(actual, expected):
                        frontier(role, input_id, '/' + identity, code, fact['id'])
                        return None
                origins[id(record)] = (input_id, row['id'], '')
                return record

            if reader == 'CRITERION_MEASUREMENT':
                resolved = resolve_condition_inputs(condition, lambda parent, field, schema, role, prerequisites:
                    read(parent, '/' + field, schema, role, prerequisites))
                if resolved is not None:
                    condition_property_facts(stage, position, resolved, origins, intent_id, atom_pointer)
                    condition_fixed_predicate_kind_fact(stage, position, atom_pointer)
                    condition_fixed_method_facts(stage, position, resolved, origins, atom_pointer)
                    condition_fixed_operator_fact(stage, position, resolved, origins, atom_pointer)
                    condition_fixed_threshold_decimal_fact(stage, position, resolved, origins, atom_pointer)
                    condition_fixed_threshold_qualifier_fact(stage, position, resolved, origins, atom_pointer)
                    linked = condition_linked_reader(condition)
                    if linked is not None:
                        atom = json_pointer(admitted[intent_id], atom_pointer)
                        proposition_schema = parse((HERE / 'components/revision-02/proposition.schema.json').read_bytes())
                        claim_schema = {'$ref': proposition_schema['$id'] + '#/$defs/' + condition['activityRow'] + '/properties/body'}
                        claim_status, claim_reason = _candidate_schema_status(claim_schema, atom.get('body'), 'ROW_CONDITION_CLAIM')
                        position['rowSourceReader'] = linked
                        position['rowSourceRequirementIds'] = []
                        position['rowSourceStatus'] = 'NOT_EVALUATED'
                        if claim_status != 'PASS':
                            frontier('WORK_CONDITION_ROW_READER', intent_id, atom_pointer, claim_reason, stage['id'])
                        else:
                            origins[id(atom)] = (intent_id, stage['id'], atom_pointer)
                            initial_count = len(position['initialInputRequirementIds'])
                            dependencies.extend(position['initialInputRequirementIds'])
                            module = {'SAMPLE_COLLECTION': 'sample_collection_sources.py', 'DRYING': 'drying_sources.py',
                                      'IRRIGATION': 'irrigation_sources.py', 'SANITATION': 'sanitation_sources.py'}[linked]
                            def row_need(role, path):
                                if path.startswith('/condition/'):
                                    source, iid, prefix, path = condition, condition_id, '', path[len('/condition'):]
                                else:
                                    source, iid, prefix = atom, intent_id, atom_pointer
                                while path:
                                    try:
                                        json_pointer(source, path); break
                                    except InputError: path = path.rsplit('/', 1)[0]
                                frontier(role, iid, prefix + path, 'ROW_CONDITION_READ_GUARD_UNRESOLVED', stage['id'])
                            matched = False
                            if linked == 'SAMPLE_COLLECTION':
                                def collection_read(parent, path, schema, role, identity, prerequisites):
                                    record = read(parent, path, schema, role, prerequisites, identity)
                                    return None if record is None else {'id': origins[id(record)][0], 'record': record}
                                reader_rule = 'resolve_collection_inputs'
                                collected = resolve_collection_inputs(atom, collection_read, row_need, lambda spec: None)
                                if collected is not None:
                                    _spec, entry, context = collected
                                    before_analysis = len(position['initialInputRequirementIds'])
                                    reader_rule = 'resolve_collection_analysis'
                                    analytic = resolve_collection_analysis(atom, entry, context, collection_read)
                                    matched = len(position['initialInputRequirementIds']) == before_analysis or analytic is not None
                            elif linked == 'DRYING':
                                reader_rule = 'resolve_drying_specification'
                                spec = resolve_drying_specification(condition, read, row_need)
                                if spec is not None:
                                    targets = drying_target_parameters(atom)
                                    guards = [
                                        {'inputRole': intent_id, 'pointer': atom_pointer + path,
                                         'valueDigest': digest(json_pointer(atom, path))}
                                        for path in ('/body/parameters/targetMoisture/quantityParameterId', '/body/quantityParameters')]
                                    if len(targets) != 1:
                                        row_need('DRYING_TARGET_PARAMETER_NOT_UNIQUE', '/body/quantityParameters')
                                    else:
                                        target_index, target = targets[0]
                                        position['dryingTargetParameterIndex'] = target_index
                                        for leaf in ('value/state', 'basis/presence'):
                                            path = '/body/quantityParameters/' + str(target_index) + '/' + leaf
                                            guards.append({'inputRole': intent_id, 'pointer': atom_pointer + path,
                                                           'valueDigest': digest(json_pointer(atom, path))})
                                        if not drying_target_has_basis(target):
                                            row_need('DRYING_STATED_TARGET_AND_MASS_BASIS', '/body/quantityParameters/' + str(target_index))
                                        else:
                                            reader_rule = 'drying_term_inputs'
                                            matched = True
                                            for _role, _field, _expected, term in drying_term_inputs(resolved[1], spec, read):
                                                matched = term is not None and matched
                                    position['rowSourceGuardObservations'] = guards
                            else:
                                initial_reader, named_reader = ((irrigation_initial_inputs, irrigation_named_condition_inputs)
                                    if linked == 'IRRIGATION' else (sanitation_initial_inputs, sanitation_named_condition_inputs))
                                reader_rule = initial_reader.__name__
                                selected = list(initial_reader(condition, atom, read))
                                if len(selected) == 2 and all(value is not None for value in selected):
                                    spec, selected_work = selected
                                    matched = True
                                    reader_rule = named_reader.__name__
                                    position['namedConditionSelections'] = []
                                    for named_role, matches, named in named_reader(spec, selected_work, read):
                                        position['namedConditionSelections'].append({
                                            'role': named_role, 'matchingWorkIndices': [index for index, _item in matches],
                                            'specificationConditionIdOrigin': {'inputRole': origins[id(spec)][0], 'pointer': '/' + named_role + '/conditionId'},
                                            'workArrayOrigin': {'inputRole': origins[id(selected_work)][0], 'pointer': '/finishConditions'}})
                                        matched = named is not None and matched
                                        if len(matches) != 1:
                                            frontier('WORK_CONDITION_NAMED_SOURCE', origins[id(selected_work)][0], '/finishConditions',
                                                     'NAMED_CONDITION_WORK_MEMBERSHIP_NOT_UNIQUE', stage['id'])
                                    if linked == 'SANITATION':
                                        reader_rule = 'read_sanitation_duration_unit'
                                        before_unit = len(position['initialInputRequirementIds'])
                                        unit = read_sanitation_duration_unit(condition, resolved[1], spec, selected_work, read)
                                        if len(position['initialInputRequirementIds']) > before_unit:
                                            matched = unit is not None and matched
                            position['rowSourceRequirementIds'] = position['initialInputRequirementIds'][initial_count:]
                            del position['initialInputRequirementIds'][initial_count:]
                            position['rowSourceStatus'] = 'MATCHED_APPLICABLE_ORIGINALS_ONLY' if matched else 'NOT_EVALUATED'
                    condition_scope_facts(stage, position, resolved, origins, intent_id, atom_pointer)
                prefix = condition_preoperand_gate(stage, position, intent_id, atom_pointer)
                module, reader_rule = 'condition_sources.py', 'condition_operand_source_request'
                dependencies.extend([prefix[0]['id'], *position['initialInputRequirementIds']])
                condition_operand_continuation(stage, position, resolved, prefix, read, intent_id, atom_pointer)
            else:
                atom = json_pointer(admitted[intent_id], atom_pointer)
                try:
                    proposition_schema = parse((HERE / 'components/revision-02/proposition.schema.json').read_bytes())
                    claim_schema = {'$ref': proposition_schema['$id'] + '#/$defs/' + condition['activityRow'] + '/properties/body'}
                    claim_status, claim_reason = _candidate_schema_status(claim_schema, atom.get('body'), 'SPECIAL_CONDITION_CLAIM')
                except (OSError, InputError, KeyError, TypeError):
                    claim_status, claim_reason = 'NOT_EVALUATED', 'SPECIAL_CONDITION_CLAIM_SCHEMA_UNAVAILABLE'
                if claim_status != 'PASS':
                    frontier('WORK_CONDITION_SPECIAL_READER', intent_id, atom_pointer,
                             claim_reason, stage['id'])
                    continue
                origins[id(atom)] = (intent_id, stage['id'], atom_pointer)
                def initial_read(parent, path, schema, role, identity, prerequisites):
                    record = read(parent, path, schema, role, prerequisites, identity)
                    return None if record is None else {'id': origins[id(record)][0], 'record': record}
                def unresolved(code, path):
                    if path.startswith('/condition/'):
                        source, iid, prefix, path = condition, condition_id, '', path[len('/condition'):]
                    else:
                        source, iid, prefix = atom, intent_id, atom_pointer
                    # An absent optional field has an existing parent origin.
                    while path:
                        try:
                            json_pointer(source, path)
                            break
                        except InputError:
                            path = path.rsplit('/', 1)[0]
                    frontier('WORK_CONDITION_SPECIAL_READER', iid, prefix + path, code, stage['id'])
                if reader == 'ANALYSIS_OUTPUT':
                    resolved = resolve_analysis_inputs(condition, atom, initial_read, unresolved, unresolved, lambda spec: None)
                else:
                    resolved = resolve_acquisition_inputs(condition, {'id': condition_id, 'record': condition},
                        initial_read, unresolved, unresolved, lambda spec: None)
                    if resolved is not None:
                        specification, context = resolved
                        initial_count = len(position['initialInputRequirementIds'])
                        reader_rule = 'resolve_acquisition_extent'
                        partial = resolve_acquisition_extent(atom, context, initial_read)
                        partial_attempted = len(position['initialInputRequirementIds']) > initial_count
                        matched = not partial_attempted or partial is not None
                        reader_rule = 'acquisition_observation_inputs'
                        for _index, _required, observation in acquisition_observation_inputs(
                                specification, context, initial_read):
                            matched = observation is not None and matched
                        position['partialExtentReadAttempted'] = partial_attempted
                        position['continuationInputRequirementIds'] = position['initialInputRequirementIds'][initial_count:]
                        del position['initialInputRequirementIds'][initial_count:]
                        position['continuationInputsStatus'] = ('MATCHED_APPLICABLE_ORIGINALS_ONLY'
                                                               if matched else 'NOT_EVALUATED')
            position['initialInputsStatus'] = ('MATCHED_SCHEMA_VALID_ORIGINALS_ONLY'
                                               if resolved is not None else 'NOT_EVALUATED')
            frontier('WORK_CONDITION_SEMANTICS', condition_id, '',
                     ('CONDITION_SEMANTICS_AND_CRITERION_DESCENDANTS_PENDING' if reader == 'CRITERION_MEASUREMENT'
                      else 'OBSERVATION_ACQUISITION_SEMANTICS_PENDING' if reader == 'OBSERVATION_ACQUISITION'
                      else reader + '_SEMANTICS_AND_LATER_READS_PENDING'), stage['id'])

    def work_carrier_support_fact(work_parent, carrier_selection, work_id,
                                  role, rule_name, origin_pointer, observations,
                                  supported, details, remaining_role, reason):
        """Record a source support rule, not party/time equality or authority."""
        carrier = carrier_selection['selectedCandidate']
        carrier_id = carrier['inputId']
        rid = 'nested-source:' + str(len(rows))
        disposition = 'PASS' if supported else 'NOT_EVALUATED'
        origin = {'inputRole': carrier_id, 'pointer': origin_pointer}
        dependencies = list(dict.fromkeys((
            work_parent['id'], carrier_selection['identityRequirementId'],
            'selected-original:' + str(selected_index[work_id]),
            'selected-original:' + str(selected_index[carrier_id]))))
        rule = {'module': 'work_sources.py',
                'moduleRawSha256': rule_hashes['work_sources.py'],
                'rule': rule_name, 'atomPointer': carrier_selection['atomPointer']}
        row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
               'role': role, 'edgeClass': 'CONDITIONAL', 'origin': origin,
               'rule': rule, 'selectedBinding': carrier['binding'],
               'workBinding': work_parent['selectedBinding'],
               'inputIds': [carrier_id, work_id], 'dependsOn': dependencies,
               'findingIds': ['AR_BODY'], 'observations': observations,
               'structuralSelection': disposition, 'disposition': disposition,
               'diagnostics': [] if supported else [{'code': reason}],
               **details,
               'qualification': 'Source-declared basis or performer-role selection only; actor-party equality, temporal comparisons, source admission and condition satisfaction remain separate.'}
        requirements.append(row)
        pin = by_id[carrier_id]
        rows.append({'requirementId': rid, 'useId': None,
                     'origin': origin, 'rule': rule, 'role': role,
                     'edgeClass': 'CONDITIONAL', 'selectedBinding': carrier['binding'],
                     'selectedInputId': carrier_id,
                     'selectedOriginal': {'ref': pin['ref'],
                                          'digestMode': pin['digestMode'],
                                          'rawSha256': pin['rawSha256'],
                                          'byteLength': pin['byteLength'],
                                          'inventoryStatus': results[carrier_id]['status']},
                     'dependsOn': dependencies, 'disposition': disposition})
        if not supported:
            frontier(remaining_role, carrier_id, origin_pointer, reason, rid)
        return row

    def work_carrier_support(work_parent, carrier_selection, work_id, source):
        """Use only the already selected, schema-valid original carrier."""
        carrier_id = carrier_selection['selectedInputId']
        basis = work_time_basis_selection(carrier_selection['kind'], source)
        origin_pointer = (basis['sourcePointer'] if basis['present'] else
                          basis['parentPointer'])
        observed = json_pointer(source, origin_pointer)
        work_carrier_support_fact(
            work_parent, carrier_selection, work_id,
            'WORK_CARRIER_TIME_BASIS_INTERPRETATION',
            'selected_payload_time_basis_interpretation', origin_pointer,
            [{'side': 'SOURCE' if basis['present'] else 'SOURCE_PARENT',
              'inputRole': carrier_id, 'pointer': origin_pointer,
              'valueDigest': digest(observed)}],
            basis['supported'],
            {'timeBasis': basis['value'], 'timeBasisPointer': basis['sourcePointer'],
             'timeBasisPointerPresent': basis['present'],
             'allowedTimeBases': basis['allowedValues']},
            'EXACT_SELECTED_WORK_TIME_BASIS',
            'SELECTED_WORK_TIME_BASIS_UNAVAILABLE')
        if carrier_selection['kind'] != 'execution':
            return
        actor = source['actor']
        role_present = 'roleAtCapture' in actor
        capture_role = actor.get('roleAtCapture')
        expected_pointer = work_performer_pointer(capture_role)
        field = expected_pointer.rsplit('/', 1)[1] if expected_pointer else None
        pointer_present = field is not None and field in actor
        selected_pointer = expected_pointer if pointer_present else None
        role_pointer = '/actor/roleAtCapture'
        origin_pointer = role_pointer if role_present else '/actor'
        observations = [
            {'side': 'SOURCE' if role_present else 'SOURCE_PARENT',
             'inputRole': carrier_id, 'pointer': origin_pointer,
             'valueDigest': digest(json_pointer(source, origin_pointer))}]
        if selected_pointer is not None:
            observations.append({'side': 'SELECTED_PERFORMER_FIELD',
                                 'inputRole': carrier_id, 'pointer': selected_pointer,
                                 'valueDigest': digest(json_pointer(source, selected_pointer))})
        work_carrier_support_fact(
            work_parent, carrier_selection, work_id,
            'WORK_EXECUTION_PERFORMER_ROLE_SELECTION',
            'physical_performer_role_source_selection', origin_pointer,
            observations, selected_pointer is not None,
            {'roleAtCapture': capture_role, 'roleAtCapturePointer': role_pointer,
             'roleAtCapturePointerPresent': role_present,
             'expectedPerformerPointer': expected_pointer,
             'performerPointerPresent': pointer_present,
             'selectedPerformerPointer': selected_pointer},
            'EXACT_PHYSICAL_PERFORMER_ROLE_SOURCE',
            'PHYSICAL_PERFORMER_ROLE_UNAVAILABLE' if expected_pointer is None else
            'PHYSICAL_PERFORMER_POINTER_UNAVAILABLE')

    # The carrier reader makes its choice from the atom and the complete outer
    # declaration array before work-specification resolution. The claim-root
    # and proposition occurrence are independent of any offered #51 read list.
    intent_root = bound['roots']['effectIntent']
    if intent_root['disposition'] == 'PASS':
        intent_id = intent_root['inputId']
        intent = admitted[intent_id]
        assertion_body = intent.get('assertionBody')
        direct_carriers = {row['origin']['pointer']: row for row in requirements
                           if (row.get('kind') == 'CANDIDATE_CLAIM_SOURCE_OCCURRENCE'
                               and row['role'] in {'INTERVENTION_INTENT_PAYLOAD',
                                                   'EXECUTION_RECORD_PAYLOAD'})}
        schema_raw = (HERE / OPERATION_CARRIER_SCHEMA_PATH).read_bytes()
        for atom_row in [row for row in requirements
                         if (row.get('kind') == 'CANDIDATE_PROPOSITION_OCCURRENCE'
                             and row['role'] == 'PROPOSITION_ATOM'
                             and row['disposition'] == 'PASS'
                             and isinstance(row.get('definitionRowId'), str)
                             and row['definitionRowId'].startswith('O'))]:
            atom_pointer = atom_row['origin']['pointer']
            try:
                atom = json_pointer(intent, atom_pointer)
                body = atom['body']
                posture = body['claimPosture']
                activity_binding = body['activityInstance']
                activity_ref = activity_binding['ref']
                if (not _binding(activity_binding)
                        or not isinstance(activity_ref, str) or not activity_ref
                        or posture not in {'INTENDED', 'PERFORMED'}):
                    raise ValueError('Operation posture or activity instance is malformed.')
            except (InputError, KeyError, TypeError, ValueError, IndexError):
                frontier('OPERATION_CARRIER_ATOM', intent_id, atom_pointer,
                         'EXACT_OPERATION_ATOM_BODY_UNAVAILABLE', atom_row['id'])
                carrier_selections.append({'atomPointer': atom_pointer,
                                           'atomRequirementId': atom_row['id'],
                                           'kind': None, 'selectedInputId': None,
                                           'status': 'NOT_EVALUATED',
                                           'reason': 'EXACT_OPERATION_ATOM_BODY_UNAVAILABLE',
                                           'declarations': []})
                continue
            kind = 'intent' if posture == 'INTENDED' else 'execution'
            field = ('interventionIntentPayloadBindings' if kind == 'intent'
                     else 'executionRecordPayloadBindings')
            outer_pointer = '/assertionBody/' + field
            declarations = (assertion_body.get(field)
                            if isinstance(assertion_body, dict) else None)
            if not isinstance(declarations, list):
                frontier('OPERATION_CARRIER_DECLARATIONS', intent_id, outer_pointer,
                         'EXACT_OPERATION_CARRIER_DECLARATION_ARRAY_UNAVAILABLE',
                         atom_row['id'])
                carrier_selections.append({'atomPointer': atom_pointer,
                                           'atomRequirementId': atom_row['id'],
                                           'sourceKind': kind, 'kind': kind,
                                           'selectedInputId': None,
                                           'activityInstanceRef': activity_ref,
                                           'status': 'NOT_EVALUATED',
                                           'reason': 'DECLARATION_ARRAY_UNAVAILABLE',
                                           'declarations': []})
                continue
            candidates, declaration_rows, unresolved = [], [], False
            for position, wrapper in enumerate(declarations):
                pointer = outer_pointer + '/' + str(position)
                direct = direct_carriers.get(pointer)
                wrapper_status, wrapper_reason = _operation_carrier_wrapper_status(
                    kind, wrapper)
                binding = ({key: wrapper[key]
                            for key in ('ref', 'revisionRef', 'digest') if key in wrapper}
                           if isinstance(wrapper, dict) else None)
                valid_binding = _binding(binding)
                pin = by_ref.get(binding['ref']) if valid_binding else None
                iid = pin['inputId'] if pin is not None else None
                reason = wrapper_reason
                status = wrapper_status
                record = None
                if status == 'PASS':
                    current_schema_pin = carrier_schema_pin(kind)
                    if current_schema_pin is None:
                        status, reason = ('NOT_EVALUATED',
                                          'CURRENT_CARRIER_SOURCE_SCHEMA_PIN_UNAVAILABLE')
                    elif (wrapper['schemaRef'] != current_schema_pin['schemaId']
                          or wrapper['schemaVersion'] != current_schema_pin['schemaVersion']
                          or wrapper['schemaDigest'] !=
                          'sha256:' + current_schema_pin['rawSha256']):
                        status, reason = ('NOT_EVALUATED',
                                          'DECLARATION_SCHEMA_METADATA_CURRENT_PIN_MISMATCH')
                    elif direct is None or direct['role'] != (
                            'INTERVENTION_INTENT_PAYLOAD' if kind == 'intent'
                            else 'EXECUTION_RECORD_PAYLOAD'):
                        status, reason = ('NOT_EVALUATED',
                                          'EXACT_DIRECT_CARRIER_DECLARATION_UNAVAILABLE')
                    elif direct.get('structuralSelection') != 'PASS':
                        status, reason = ('NOT_EVALUATED',
                                          'DIRECT_CARRIER_ORIGINAL_SELECTION_NOT_PASS')
                    elif pin is None:
                        status, reason = ('NOT_EVALUATED',
                                          'CARRIER_ORIGINAL_NOT_SELECTED')
                    elif results[iid]['status'] != 'MATCHED':
                        status, reason = ('NOT_EVALUATED',
                                          'CARRIER_ORIGINAL_INVENTORY_NOT_MATCHED')
                    elif pin['digestMode'] != 'JCS_JSON':
                        status, reason = ('NOT_EVALUATED', 'RAW_BYTES_CARRIER_OPAQUE')
                    elif binding != {'ref': pin['ref'],
                                     'digest': pin['wholeJcsDigest']}:
                        status, reason = ('NOT_EVALUATED',
                                          'CARRIER_DIGEST_OR_REVISION_RESOLUTION_PENDING')
                    else:
                        record = admitted.get(iid)
                        if not isinstance(record, dict):
                            status, reason = ('NOT_EVALUATED',
                                              'ADMITTED_CARRIER_OBJECT_UNAVAILABLE')
                        else:
                            status, reason = carrier_schema_status(
                                kind, record, current_schema_pin)
                if status != 'PASS':
                    unresolved = True
                    frontier('OPERATION_CARRIER_DECLARATION', intent_id, pointer,
                             reason, atom_row['id'])
                index = len(rows)
                rid = 'nested-source:' + str(index)
                dependencies = [atom_row['id']]
                if direct is not None:
                    dependencies.append(direct['id'])
                if iid is not None:
                    dependencies.append('selected-original:' + str(selected_index[iid]))
                rule = {'module': 'source_derivation.py',
                        'moduleRawSha256': rule_hashes['source_derivation.py'],
                        'rule': 'operation_carrier_declaration_candidate',
                        'sourcePointer': pointer,
                        'wrapperSchemaPath': OPERATION_CARRIER_SCHEMA_PATH,
                        'wrapperSchemaRawSha256': sha(schema_raw),
                        'sourceSchemaId': OPERATION_SOURCE_SCHEMAS[kind][0],
                        'sourceSchemaPin': carrier_schema_pin(kind)}
                source_shape_invalid = (status == 'FAIL' and
                                        reason == 'OPERATION_CARRIER_SOURCE_SCHEMA_INVALID')
                edge_class = 'COMPARISON_VALUE'
                row = {'id': rid, 'kind': 'CANDIDATE_NESTED_SOURCE_OCCURRENCE',
                       'role': 'OPERATION_CARRIER_DECLARATION',
                       'edgeClass': edge_class,
                       'origin': {'inputRole': intent_id, 'pointer': pointer},
                       'rule': rule, 'selectedBinding': binding,
                       'inputIds': list(dict.fromkeys([intent_id, *([iid] if iid else [])])),
                       'dependsOn': dependencies, 'findingIds': ['AR_BODY'],
                       'sourceKind': kind, 'atomPointer': atom_pointer,
                       'activityInstanceRef': activity_ref,
                       'declarationValueDigest': digest(wrapper),
                       'structuralSelection': ('NOT_EVALUATED' if source_shape_invalid
                                               else status),
                       'disposition': ('FAIL' if status == 'FAIL' and
                                       not source_shape_invalid else 'NOT_EVALUATED'),
                       'diagnostics': [] if status == 'PASS' else [{'code': reason}],
                       'qualification': 'Exact declaration position and candidate source shape only; no owner admission, protected treatment or complete carrier comparison.'}
                requirements.append(row)
                selected_original = ({'ref': pin['ref'],
                                      'digestMode': pin['digestMode'],
                                      'rawSha256': pin['rawSha256'],
                                      'byteLength': pin['byteLength'],
                                      'inventoryStatus': results[iid]['status']}
                                     if pin is not None else None)
                rows.append({'requirementId': rid, 'useId': None,
                             'origin': row['origin'], 'rule': rule,
                             'role': row['role'], 'edgeClass': edge_class,
                             'selectedBinding': binding, 'selectedInputId': iid,
                             'selectedOriginal': selected_original,
                             'dependsOn': dependencies,
                             'disposition': row['disposition']})
                declaration_rows.append({'pointer': pointer, 'requirementId': rid,
                                         'directRequirementId': (direct['id'] if direct else None),
                                         'selectedInputId': iid,
                                         'selectedOriginal': selected_original,
                                         'structuralSelection': row['structuralSelection'],
                                         **({'reason': reason} if reason else {})})
                if source_shape_invalid:
                    schema_pin = carrier_schema_pin(kind)
                    if schema_pin is not None:
                        shape = source_shape_failure(
                            rid, iid, binding, 'OPERATION_CARRIER_SOURCE_SHAPE',
                            'source_derivation.py', schema_pin['localPath'],
                            reason)
                        shape['rule']['sourceSchemaId'] = OPERATION_SOURCE_SCHEMAS[kind][0]
                        shape['rule']['sourceSchemaPin'] = schema_pin
                        rows[-1]['rule'] = shape['rule']
                        declaration_rows[-1]['sourceShapeRequirementId'] = shape['id']
                if status == 'PASS':
                    candidates.append({'inputId': iid, 'binding': binding,
                                       'record': record, 'pin': pin,
                                       'requirementId': rid, 'requirementRow': row,
                                       'subjectMatch': same(
                                           record['subject'],
                                           {'subjectType': 'OPERATION',
                                            'subjectRef': activity_ref})})
            distinct = {}
            for candidate in candidates:
                key = (canonical(candidate['binding']),
                       candidate['pin']['rawSha256'],
                       candidate['pin']['wholeJcsDigest'])
                distinct.setdefault(key, []).append(candidate)
            unique = [members[0] for members in distinct.values()]
            matching = [candidate for candidate in unique if candidate['subjectMatch']]
            viable = matching if matching else unique
            selected = viable[0] if not unresolved and len(viable) == 1 else None
            if selected is None:
                selection_reason = ('DECLARATIONS_UNRESOLVED' if unresolved else
                                    'NO_DECLARED_CARRIER' if not declarations else
                                    'AMBIGUOUS_DECLARED_CARRIER')
                frontier('UNIQUE_DECLARED_OPERATION_PAYLOAD_FOR_ACTIVITY',
                         intent_id, outer_pointer, selection_reason, atom_row['id'])
                carrier_selections.append({
                    'atomPointer': atom_pointer, 'atomRequirementId': atom_row['id'],
                    'sourceKind': kind, 'kind': kind,
                    'selectedInputId': None,
                    'activityInstanceRef': activity_ref,
                    'status': 'NOT_EVALUATED', 'reason': selection_reason,
                    'declarations': declaration_rows,
                    'distinctResolvedCandidateCount': len(unique)})
                continue
            selected_members = next(members for members in distinct.values()
                                    if selected in members)
            selected_info = {'atomPointer': atom_pointer,
                             'atomRequirementId': atom_row['id'],
                             'sourceKind': kind, 'kind': kind,
                             'selectedInputId': selected['inputId'],
                             'activityInstanceRef': activity_ref,
                             'status': 'SELECTED_CANDIDATE',
                             'declarations': declaration_rows,
                             'distinctResolvedCandidateCount': len(unique),
                             'selectedCandidate': {
                                 'inputId': selected['inputId'],
                                 'binding': selected['binding'],
                                 'selectedOriginal': {
                                     'ref': selected['pin']['ref'],
                                     'digestMode': selected['pin']['digestMode'],
                                     'rawSha256': selected['pin']['rawSha256'],
                                     'byteLength': selected['pin']['byteLength'],
                                     'inventoryStatus': results[selected['inputId']]['status']},
                                 'subjectExactActivityMatch': selected['subjectMatch'],
                                 'declarationRequirementIds': [
                                     member['requirementId'] for member in selected_members]}}
            carrier_selections.append(selected_info)
            declaration_pointer = next(
                row['pointer'] for row in declaration_rows
                if row['requirementId'] == selected['requirementId'])
            identity_fact = carrier_identity_fact(
                selected['requirementRow'], selected, declaration_pointer,
                intent_id, kind)
            selected_info['identityRequirementId'] = identity_fact['id']
            selected_info['identityDisposition'] = identity_fact['disposition']
            if identity_fact['disposition'] == 'FAIL':
                frontier('OPERATION_CARRIER_IDENTITY', selected['inputId'],
                         '/' + OPERATION_SOURCE_SCHEMAS[kind][1],
                         'SOURCE_ID_BINDING_MISMATCH', identity_fact['id'])
                continue
            operation_actual_comparisons(selected_info, atom, intent_id)
            if not selected['subjectMatch']:
                frontier('OPERATION_CARRIER_SUBJECT_RELATION',
                         selected['inputId'], '/subject',
                         'EXACT_SOURCE_SUBJECT_TO_ACTIVITY_INSTANCE_PENDING',
                         selected['requirementId'])
            for role, reason in (
                    ('OPERATION_CARRIER_OWNER_USE', 'OWNER_ADMISSION_AND_PROTECTED_TREATMENT_PENDING'),
                    ('OPERATION_CARRIER_ACTIVE_STAGE', 'ACTIVE_STAGE_OR_CONDITION_EVIDENCE_PENDING'),
                    ('OPERATION_CARRIER_DESCENDANTS', 'CARRIER_COMPARISONS_AND_DESCENDANTS_PENDING')):
                frontier(role, selected['inputId'], '', reason,
                         selected['requirementId'])

    direct = [row for row in requirements
              if row.get('kind') == 'CANDIDATE_CLAIM_SOURCE_OCCURRENCE']
    for parent in direct:
        rule = parent['rule']
        row_id = rule.get('definitionRef', '').split(':')[-1]
        if rule.get('group') == 'ROW_BODY_FIELD' and row_id == 'C04' and rule['selector'] == 'criterion':
            intent_id = bound['roots']['effectIntent']['inputId']
            atom_pointer = rule['atomPointer']
            try:
                atom = json_pointer(admitted[intent_id], atom_pointer)
                if not condition_schema_cache['attempted']:
                    condition_schema_cache['attempted'] = True
                    condition_schema_cache['schemas'] = _condition_source_schemas()
                schemas = condition_schema_cache['schemas']
                if schemas is None: raise ValueError('Criterion schemas unavailable.')
                shape = schemas.errors('https://ofarm.dev/schema/drafts/non-default/assertion-domain/proposition/v0.1', atom, 'C04')
                if shape:
                    if any(item.get('code') in {'SCHEMA_NOT_IN_PINNED_REGISTRY', 'SCHEMA_RESOLUTION_ERROR'} for item in shape):
                        raise ValueError('Criterion schema resolution unavailable.')
                    source_shape_failure(parent['id'], intent_id, bound['selection']['effectIntent'],
                        'SUBMITTED_C04_SHAPE', 'criterion_sources.py', 'components/revision-02/runtime_support.py',
                        'SUBMITTED_C04_SCHEMA_INVALID', source_pointer=atom_pointer)
                else:
                    position = {'selectedInputId': intent_id, 'selectedBinding': bound['selection']['effectIntent']}
                    entry = {'id': parent['id'], 'observations': [{'inputRole': intent_id,
                        'pointer': atom_pointer, 'valueDigest': digest(atom)}]}
                    condition_criterion_continuation(None, position, None, entry, schemas, None,
                                                    submitted_atom=atom, submitted_pointer=atom_pointer)
            except (InputError, KeyError, ValueError, TypeError, ImportError, AttributeError):
                frontier('SUBMITTED_C04_READER', intent_id, atom_pointer,
                         'SUBMITTED_C04_READER_OR_SCHEMA_UNAVAILABLE', parent['id'])
        if (rule.get('group') == 'ROW_BODY_FIELD' and row_id in SAMPLE_OUTPUT_VERSIONS
                and rule['selector'] == 'workSpecification/outputSpecification'):
            intent_id = bound['roots']['effectIntent']['inputId']
            atom_pointer = rule['atomPointer']
            try:
                atom = json_pointer(admitted[intent_id], atom_pointer)
                sample_relation_continuation(parent, intent_id, atom_pointer, atom)
            except (InputError, KeyError, ValueError, TypeError, ImportError, AttributeError):
                frontier('SAMPLE_RELATION_READER', intent_id, atom_pointer,
                         'SAMPLE_RELATION_READER_OR_SCHEMA_UNAVAILABLE', parent['id'])
            continue
        iid = parent['inputIds'][0] if parent['inputIds'] else None
        if iid is None or parent.get('structuralSelection') != 'PASS':
            continue
        if any(row['id'] in parent['dependsOn'] and row['disposition'] == 'FAIL'
               for row in requirements
               if row.get('kind') == 'CANDIDATE_PROPOSITION_OCCURRENCE'):
            continue
        if rule.get('group') != 'ROW_BODY_FIELD':
            continue
        if rule['selector'] == 'workSpecification/binding' and row_id.startswith('O'):
            source = selected_record(parent['selectedBinding'], 'SELECTED_WORK_SPECIFICATION',
                                     bound['roots']['effectIntent']['inputId'],
                                     parent['origin']['pointer'], parent['id'])
            if source is None:
                continue
            source_id, record = source
            schema_status, schema_reason = _candidate_schema_status(
                WORK_SCHEMAS['work'], record, 'WORK')
            if schema_status == 'FAIL':
                source_shape_failure(parent['id'], source_id,
                                     parent['selectedBinding'],
                                     'WORK_SPECIFICATION_SOURCE_SHAPE',
                                     'work_sources.py', 'work_definition_inputs.py',
                                     schema_reason)
                continue
            if schema_status != 'PASS':
                frontier('SELECTED_WORK_SPECIFICATION', source_id, '',
                         schema_reason, parent['id'])
                continue
            intent_id = bound['roots']['effectIntent']['inputId']
            binding_pointer = parent['origin']['pointer']
            identity_fact = work_canonical_fact(
                parent['id'], parent['selectedBinding'],
                'WORK_SPECIFICATION_DEFINITION_ID_COMPARISON',
                {'inputRole': source_id, 'pointer': '/definitionId'},
                record['definitionId'], parent['selectedBinding']['ref'],
                same(record['definitionId'], parent['selectedBinding']['ref']),
                'WORK_DEFINITION_IDENTITY_MISMATCH',
                [{'side': 'WORK', 'inputRole': source_id,
                  'pointer': '/definitionId',
                  'valueDigest': digest(record['definitionId'])},
                 {'side': 'CLAIM', 'inputRole': intent_id,
                  'pointer': binding_pointer + '/ref',
                  'valueDigest': digest(parent['selectedBinding']['ref'])}])
            row_fact = work_canonical_fact(
                parent['id'], parent['selectedBinding'],
                'WORK_SPECIFICATION_ACTIVITY_ROW_COMPARISON',
                {'inputRole': source_id, 'pointer': '/activityRow'},
                record['activityRow'], row_id, same(record['activityRow'], row_id),
                'WORK_DEFINITION_ROW_MISMATCH',
                [{'side': 'WORK', 'inputRole': source_id,
                  'pointer': '/activityRow',
                  'valueDigest': digest(record['activityRow'])}],
                rule_details={'expectedRowFromDefinitionRef': row_id,
                              'claimDefinitionPointer': rule.get('atomPointer', '') + '/definition'})
            # The work evaluator records these contradictions but continues
            # through the schema-valid definition's selected condition reads.
            work_comparison_ids = (identity_fact['id'], row_fact['id'])
            expanded.append(source_id)
            atom_pointer = rule.get('atomPointer')
            claim_work = None
            claim_body = None
            try:
                atom = json_pointer(admitted[intent_id], atom_pointer)
                selected_work = atom['body']['workSpecification']
                if (atom.get('definition') == rule.get('definitionRef')
                        and isinstance(selected_work, dict)
                        and selected_work.get('binding') == parent['selectedBinding']):
                    claim_work = selected_work
                    claim_body = atom['body']
            except (InputError, KeyError, TypeError, AttributeError):
                pass
            if claim_work is None:
                frontier('WORK_CONDITION_SELECTED_IDS', intent_id,
                         atom_pointer or '', 'EXACT_CLAIM_WORK_SPECIFICATION_UNAVAILABLE',
                         parent['id'])
            else:
                for code, role, container, key in WORK_CLAIM_VALUE_RULES:
                    claim_source = (claim_work if container == 'workSpecification'
                                    else claim_body)
                    claim_pointer = (atom_pointer + '/body/' +
                                     ('workSpecification/'
                                      if container == 'workSpecification' else '') + key)
                    if isinstance(claim_source, dict) and key in claim_source:
                        work_claim_value_fact(
                            parent['id'], parent['selectedBinding'], role, code,
                            intent_id, claim_pointer, claim_source[key],
                            source_id, '/' + key, record[key])
                    else:
                        frontier(role, intent_id, claim_pointer,
                                 'CLAIM_WORK_COMPARISON_OPERAND_UNAVAILABLE', parent['id'])
                output_pointer = atom_pointer + '/body/workSpecification/outputSpecification'
                work_claim_value_fact(
                    parent['id'], parent['selectedBinding'],
                    'WORK_OUTPUT_SPECIFICATION_COMPARISON',
                    'WORK_OUTPUT_SPECIFICATION_MISMATCH', intent_id,
                    output_pointer, claim_work.get('outputSpecification'),
                    source_id, '/outputSpecification', record['outputSpecification'],
                    claim_present='outputSpecification' in claim_work)
                if claim_body.get('claimPosture') == 'INTENDED':
                    performer_pointer = atom_pointer + '/body/performedBy'
                    if 'performedBy' in claim_body:
                        work_claim_value_fact(
                            parent['id'], parent['selectedBinding'],
                            'INTENDED_WORK_PERFORMER_COMPARISON',
                            'INTENDED_WORK_PERFORMER_MISMATCH',
                            intent_id, performer_pointer, claim_body['performedBy'],
                            source_id, '/intendedPerformer', record['intendedPerformer'])
                    else:
                        frontier('INTENDED_WORK_PERFORMER', intent_id,
                                 performer_pointer,
                                 'CLAIM_WORK_COMPARISON_OPERAND_UNAVAILABLE', parent['id'])
                elif claim_body.get('claimPosture') != 'PERFORMED':
                    frontier('WORK_CLAIM_POSTURE', intent_id,
                             atom_pointer + '/body/claimPosture',
                             'CLAIM_WORK_POSTURE_UNAVAILABLE', parent['id'])
            carrier_selection = next((item for item in carrier_selections
                                      if (item['atomPointer'] == atom_pointer
                                          and item['status'] == 'SELECTED_CANDIDATE'
                                          and item.get('identityDisposition') == 'PASS')),
                                     None)
            carrier_record = (admitted.get(carrier_selection['selectedInputId'])
                              if carrier_selection is not None else None)
            if carrier_selection is not None and claim_body is not None \
                    and isinstance(carrier_record, dict):
                carrier_id = carrier_selection['selectedInputId']
                kind = carrier_selection['kind']
                work_carrier_support(parent, carrier_selection, source_id,
                                     carrier_record)
                action_key = 'intendedAction' if kind == 'intent' else 'actualAction'
                action = carrier_record.get(action_key)
                meaning = record['carrierMeaning']
                if isinstance(action, dict) and isinstance(meaning, dict):
                    parameters = claim_body.get('parameters')
                    checks = carrier_meaning_checks(
                        kind, carrier_record, meaning,
                        parameters if isinstance(parameters, dict) else {})
                    for code, actual, expected, _path, scope, pointer, expected_pointer, present in checks:
                        if scope == 'claim':
                            shape = _specific_activity_status(
                                row_id, actual)
                            if shape != 'PASS':
                                frontier('WORK_SPECIFIC_ACTIVITY', intent_id,
                                         atom_pointer + pointer,
                                         'CLAIM_SPECIFIC_ACTIVITY_INVALID_FOR_PINNED_ROW'
                                         if shape == 'FAIL' else
                                         'CLAIM_SPECIFIC_ACTIVITY_ROW_SCHEMA_UNAVAILABLE',
                                         parent['id'])
                                continue
                        work_carrier_fact(
                            parent, carrier_selection, source_id, intent_id,
                            code.replace('_MISMATCH', '_COMPARISON'), code,
                            actual, expected,
                            {'inputRole': intent_id if scope == 'claim' else carrier_id,
                             'pointer': atom_pointer + pointer if scope == 'claim' else pointer},
                            expected_pointer, actual_present=present,
                            projected_source_pointer=pointer)
                    if not isinstance(parameters, dict):
                        frontier('WORK_SPECIFIC_ACTIVITY', intent_id,
                                 atom_pointer + '/body/parameters',
                                 'CLAIM_PARAMETERS_UNAVAILABLE', parent['id'])
                else:
                    frontier('WORK_CARRIER_MEANING', source_id,
                             '/carrierMeaning',
                             'SCHEMA_VALID_CARRIER_ACTION_OR_WORK_MEANING_UNAVAILABLE',
                             parent['id'])
            elif carrier_selection is not None:
                frontier('WORK_CARRIER_MEANING', intent_id, atom_pointer or '',
                         'EXACT_CLAIM_WORK_OR_SELECTED_CARRIER_UNAVAILABLE',
                         parent['id'])
            reviewed_rows = _reviewed_condition_table()
            reviewed_matches = ([(index, item) for index, item in enumerate(reviewed_rows)
                                 if isinstance(item, dict) and item.get('activityRow') == row_id]
                                if reviewed_rows is not None else [])
            reviewed_rule = reviewed_matches[0] if len(reviewed_matches) == 1 else None
            if reviewed_rule is None:
                frontier('WORK_CONDITION_CANONICAL_MEANING', source_id, '',
                         'PINNED_CANONICAL_CONDITION_RULE_UNAVAILABLE', parent['id'])
            condition_positions = {}
            for field, claim_field, stage, canonical_prefix in WORK_CONDITION_GROUPS:
                group = record.get(field)
                if not isinstance(group, list):
                    frontier('WORK_CONDITION_GROUP', source_id, '/' + field,
                             'SOURCE_FIELD_SHAPE_UNAVAILABLE', parent['id'])
                    continue
                work_ids = [item['conditionId'] for item in group]
                work_observations = [
                    {'side': 'WORK', 'inputRole': source_id,
                     'pointer': '/' + field + '/' + str(pos) + '/conditionId',
                     'valueDigest': digest(item['conditionId'])}
                    for pos, item in enumerate(group)]
                canonical_id = canonical_prefix + row_id
                work_canonical_fact(
                    parent['id'], parent['selectedBinding'],
                    'WORK_CANONICAL_CONDITION_ID',
                    {'inputRole': source_id, 'pointer': '/' + field},
                    work_ids, canonical_id, canonical_id in work_ids,
                    'REQUIRED_CANONICAL_WORK_CONDITION_OMITTED',
                    work_observations)
                work_canonical_fact(
                    parent['id'], parent['selectedBinding'],
                    'WORK_DISTINCT_CONDITION_IDS',
                    {'inputRole': source_id, 'pointer': '/' + field},
                    work_ids, 'DISTINCT_CONDITION_IDS',
                    len(set(work_ids)) == len(work_ids),
                    'DUPLICATE_WORK_CONDITION_ID', work_observations)
                claim_pointer = (atom_pointer + '/body/workSpecification/' + claim_field
                                 if isinstance(atom_pointer, str) else '')
                claim_ids = claim_work.get(claim_field) if claim_work is not None else None
                if (isinstance(claim_ids, list)
                        and all(isinstance(value, str) for value in claim_ids)):
                    work_canonical_fact(
                        parent['id'], parent['selectedBinding'],
                        'WORK_SELECTED_CONDITION_SET',
                        {'inputRole': intent_id, 'pointer': claim_pointer},
                        claim_ids, work_ids, claim_ids == work_ids,
                        'WORK_CONDITION_SET_MISMATCH',
                        [{'side': 'CLAIM', 'inputRole': intent_id,
                          'pointer': claim_pointer, 'valueDigest': digest(claim_ids)},
                         *work_observations])
                    for pos, expected_id in enumerate(work_ids[:len(claim_ids)]):
                        work_canonical_fact(
                            parent['id'], parent['selectedBinding'],
                            'WORK_SELECTED_CONDITION_ID',
                            {'inputRole': intent_id,
                             'pointer': claim_pointer + '/' + str(pos)},
                            claim_ids[pos], expected_id,
                            claim_ids[pos] == expected_id,
                            'WORK_SELECTED_CONDITION_ID_MISMATCH',
                            [{'side': 'CLAIM', 'inputRole': intent_id,
                              'pointer': claim_pointer + '/' + str(pos),
                              'valueDigest': digest(claim_ids[pos])},
                             work_observations[pos]])
                else:
                    frontier('WORK_CONDITION_SELECTED_IDS', intent_id,
                             claim_pointer, 'CLAIM_CONDITION_ID_ARRAY_UNAVAILABLE',
                             parent['id'])
                for pos, item in enumerate(group):
                    pointer = '/' + field + '/' + str(pos) + '/definitionBinding'
                    binding = item.get('definitionBinding') if isinstance(item, dict) else None
                    condition_id = item.get('conditionId') if isinstance(item, dict) else None
                    position = {'origin': {'inputRole': source_id,
                                           'pointer': '/' + field + '/' + str(pos)},
                                'stageFromWorkArray': stage,
                                'conditionId': condition_id,
                                'selectedBinding': binding,
                                'parentValidation': 'NOT_EVALUATED',
                                'preCarrierComparisonRequirementIds': []}
                    condition_positions.setdefault(stage, []).append(position)
                    selected_condition = emit(
                        parent['id'], source_id, pointer, binding,
                        'CONDITION:' + condition_id if isinstance(condition_id, str)
                        else 'WORK_CONDITION_UNNAMED',
                        'work_sources.py', 'work_definition_condition_resolve',
                        additional_dependencies=work_comparison_ids)
                    position['readRequirementId'] = selected_condition['id']
                    position['readStructuralSelection'] = selected_condition[
                        'structuralSelection']
                    position['selectedInputId'] = (selected_condition['inputIds'][0]
                                                   if selected_condition['inputIds'] else None)
                    if selected_condition['structuralSelection'] != 'PASS':
                        continue
                    source_condition = selected_record(
                        binding, 'SELECTED_WORK_CONDITION', source_id,
                        pointer, selected_condition['id'])
                    if source_condition is None:
                        continue
                    selected_condition_id, condition = source_condition
                    schema_status, schema_reason = _candidate_schema_status(
                        WORK_SCHEMAS['workCondition'], condition, 'WORK_CONDITION')
                    if schema_status == 'FAIL':
                        shape = source_shape_failure(
                            selected_condition['id'], selected_condition_id,
                            binding, 'WORK_CONDITION_SOURCE_SHAPE',
                            'work_sources.py', 'work_definition_inputs.py',
                            schema_reason)
                        position['parentValidation'] = 'FAIL'
                        position['sourceShapeRequirementId'] = shape['id']
                        continue
                    if schema_status != 'PASS':
                        frontier('SELECTED_WORK_CONDITION', selected_condition_id,
                                 '', schema_reason, selected_condition['id'])
                        continue
                    comparisons = (
                        ('definitionId', binding['ref'], pointer + '/ref'),
                        *condition_parent_expectations(
                            condition_id, row_id, stage,
                            '/' + field + '/' + str(pos)),
                    )
                    comparison_start = len(requirements)
                    matched = [work_condition_fact(
                        selected_condition, selected_condition_id, name,
                        condition[name], expected, source_id, expected_pointer)
                        for name, expected, expected_pointer in comparisons]
                    position['preCarrierComparisonRequirementIds'] = [
                        row['id'] for row in requirements[comparison_start:]]
                    meaning_matched = True
                    meaning_evaluated = False
                    if reviewed_rule is not None:
                        reviewed_index, reviewed_row = reviewed_rule
                        meanings = reviewed_row.get('conditionDefinitions')
                        if (isinstance(meanings, dict)
                                and item['conditionId'] in meanings
                                and isinstance(meanings[item['conditionId']], str)):
                            meaning_pointer = ('/rows/' + str(reviewed_index)
                                               + '/conditionDefinitions/'
                                               + _pointer_token(item['conditionId']))
                            expected_meaning = meanings[item['conditionId']]
                            meaning_matched = condition['meaning'] == expected_meaning
                            meaning_fact = work_canonical_fact(
                                selected_condition['id'], binding,
                                'WORK_CONDITION_CANONICAL_MEANING_COMPARISON',
                                {'inputRole': selected_condition_id,
                                 'pointer': '/meaning'},
                                condition['meaning'], expected_meaning,
                                meaning_matched,
                                'REVIEWED_WORK_CONDITION_MEANING_CHANGED',
                                [{'side': 'CONDITION',
                                  'inputRole': selected_condition_id,
                                  'pointer': '/meaning',
                                  'valueDigest': digest(condition['meaning'])},
                                 {'side': 'PINNED_RULE',
                                  'ruleInput': REVIEWED_CONDITION_PATH,
                                  'pointer': meaning_pointer,
                                  'rawSha256': REVIEWED_CONDITION_SHA256,
                                  'valueDigest': digest(expected_meaning)}],
                                static_rule=True)
                            position['canonicalMeaningRequirementId'] = meaning_fact['id']
                            meaning_evaluated = True
                        else:
                            frontier('WORK_CONDITION_NONCANONICAL_MEANING',
                                     selected_condition_id, '/meaning',
                                     'NONCANONICAL_CONDITION_MEANING_RULE_PENDING',
                                     selected_condition['id'])
                    position['parentValidation'] = (
                        'FAIL' if not all(matched) or not meaning_matched else
                        'PASS' if meaning_evaluated else 'NOT_EVALUATED')
                    if all(matched) and meaning_matched:
                        expanded.append(selected_condition_id)
                    else:
                        frontier('SELECTED_WORK_CONDITION', selected_condition_id,
                                 '', 'WORK_CONDITION_PRE_CARRIER_COMPARISON_FAILED',
                                 selected_condition['id'])
            stage_fact = (work_active_stage(
                parent, carrier_selection, source_id, intent_id,
                atom_pointer, claim_body, condition_positions)
                if carrier_selection is not None and claim_body is not None
                else None)
            if stage_fact is not None and stage_fact['selectedStage'] is not None:
                condition_initial_inputs(stage_fact, condition_positions, intent_id, atom_pointer)
                frontier('WORK_CONDITION_ACTIVE_STAGE', source_id, '',
                         'SELECTED_STAGE_CONDITION_EVIDENCE_PENDING', stage_fact['id'])
            elif stage_fact is None:
                frontier('WORK_CONDITION_ACTIVE_STAGE', source_id, '',
                         'INDEPENDENT_EXECUTION_CARRIER_AND_STAGE_PENDING',
                         parent['id'])
            frontier('WORK_CONDITION_DESCENDANTS', source_id, '',
                     'CRITERION_MEASUREMENT_METHOD_PROPERTY_RULES_PENDING'
                     if stage_fact is None else 'CONDITION_SEMANTICS_AND_LATER_READER_RULES_PENDING',
                     parent['id'])
    event_claims = [row for row in direct if row['role'] == 'SEMANTIC_EVENT']
    selected_sources = [row for row in requirements
                        if row['id'].startswith('selected-source:')
                        and row['disposition'] == 'PASS' and len(row['inputIds']) == 1]
    for event_claim in event_claims:
        if (event_claim.get('structuralSelection') != 'PASS'
                or len(event_claim['inputIds']) != 1):
            frontier('INDEPENDENT_EVENT_USE_DEFINITION',
                     bound['roots']['effectIntent']['inputId'],
                     event_claim['origin']['pointer'],
                     'SEMANTIC_EVENT_CLAIM_ORIGINAL_NOT_SELECTED', event_claim['id'])
            continue
        candidates = {}
        for selected in selected_sources:
            iid = selected['inputIds'][0]
            value = admitted.get(iid)
            if (isinstance(value, dict) and value.get('schemaVersion') == EVENT_USE_VERSION
                    and value.get('envelopeBinding') == event_claim['selectedBinding']):
                # Repeated exact nominations are distinct provenance, not
                # distinct EventUse originals. A second selected original
                # still makes the independent event-use choice ambiguous.
                if iid not in candidates:
                    candidates[iid] = (selected, value, [])
                candidates[iid][2].append(selected['id'])
        if len(candidates) != 1:
            frontier('INDEPENDENT_EVENT_USE_DEFINITION',
                     bound['roots']['effectIntent']['inputId'],
                     event_claim['origin']['pointer'],
                     'UNIQUE_NOMINATED_EVENT_USE_DEFINITION_UNAVAILABLE',
                     event_claim['id'])
            continue
        use_id, (selected, event_use, nomination_ids) = next(iter(candidates.items()))
        event_schema, event_schema_reason = _event_schema_status('eventUse', event_use)
        if event_schema == 'FAIL':
            source_shape_failure(
                selected['id'], use_id, selected['selectedBinding'],
                'EVENT_USE_SOURCE_SHAPE', 'event_definition_inputs.py',
                'event_definition_inputs.py', event_schema_reason,
                finding_id='AR_EVENT_ASSOCIATION',
                additional_dependencies=(event_claim['id'], *nomination_ids[1:]))
            continue
        if event_schema != 'PASS':
            frontier('EVENT_USE_SCHEMA', use_id, '', event_schema_reason,
                     selected['id'])
            continue
        if event_use.get('definitionId') != selected['selectedBinding']['ref']:
            frontier('INDEPENDENT_EVENT_USE_DEFINITION', use_id, '',
                     'EVENT_USE_DEFINITION_IDENTITY_UNVERIFIED', selected['id'])
            continue
        event_roots.append({'inputId': use_id,
                            'eventClaimRequirementId': event_claim['id'],
                            'nominationRequirementId': nomination_ids[0],
                            'nominationRequirementIds': nomination_ids})
        expanded.append(use_id)
        case_binding = event_use.get('canonicalCaseBinding')
        matching_cases = [case for case in canonical_cases
                          if case_binding == {'ref': case['definitionRef'],
                                              'digest': digest(case)}]
        case_selection = None
        if len(matching_cases) == 1:
            case_selection = {'kind': 'PINNED_CANONICAL_CASE',
                              'id': matching_cases[0]['id'],
                              'definitionRegistryRawSha256': sha(definition_registry_raw)}
        elif not matching_cases:
            extension_source = selected_record(
                case_binding, 'EVENT_EXTENSION_CASE', use_id,
                '/canonicalCaseBinding', selected['id'])
            if extension_source is not None:
                extension_id, extension = extension_source
                extension_schema, extension_reason = _event_schema_status(
                    'eventExtension', extension)
                if extension_schema == 'FAIL':
                    source_shape_failure(
                        selected['id'], extension_id, case_binding,
                        'EVENT_EXTENSION_SOURCE_SHAPE',
                        'event_definition_inputs.py', 'event_definition_inputs.py',
                        extension_reason, finding_id='AR_EVENT_ASSOCIATION',
                        additional_dependencies=(
                            event_claim['id'], *nomination_ids[1:],
                            *(row['id'] for row in nominations[canonical(case_binding)]
                              if extension_id in row['inputIds']
                              and row['id'].startswith('selected-source:'))))
                    continue
                if (extension_schema == 'PASS'
                        and extension.get('definitionId') == case_binding['ref']
                        and extension.get('subtypePresence') == event_use['subtypePresence']
                        and (extension['subtypePresence'] == 'PRESENT')
                        == (isinstance(extension.get('eventSubtypeId'), str)
                            and bool(extension['eventSubtypeId']))):
                    case_selection = {
                        'kind': 'SELECTED_TYPED_EXTENSION', 'id': 'V04-extension',
                        'inputId': extension_id, 'ref': case_binding['ref'],
                        'rawSha256': by_id[extension_id]['rawSha256']}
                    expanded.append(extension_id)
                else:
                    frontier('EVENT_EXTENSION_CASE', extension_id, '',
                             extension_reason or 'EVENT_EXTENSION_IDENTITY_OR_SUBTYPE_UNVERIFIED',
                             selected['id'])
        case_ready = case_selection is not None
        event_children = {}
        for field, role in [('canonicalCaseBinding', 'EXACT_EVENT_CASE_DEFINITION'),
                            ('vocabularyDefinitionBinding', 'EXACT_EVENT_VOCABULARY_DEFINITION'),
                            ('packDefinitionBinding', 'EXACT_EVENT_MEANING_PACK_DEFINITION')]:
            event_children[field] = emit(
                selected['id'], use_id, '/' + field, event_use.get(field), role,
                'event_definition_inputs.py', 'event_use_resolve',
                'AR_EVENT_ASSOCIATION',
                allow_unpinned=field == 'canonicalCaseBinding',
                unpinned_reason='LOCAL_OR_EXTENSION_CASE_RULE_PENDING',
                additional_dependencies=(event_claim['id'], *nomination_ids[1:],
                                         *([event_children['canonicalCaseBinding']['id']]
                                           if field != 'canonicalCaseBinding' and case_ready
                                           else [])),
                edge_class=('REQUIRED_ORIGINAL_READ'
                            if (case_ready and
                                (field != 'canonicalCaseBinding' or
                                 case_selection['kind'] == 'SELECTED_TYPED_EXTENSION'))
                            else 'CONDITIONAL'))
        if 'observationMeasurementBinding' in event_use:
            emit(selected['id'], use_id, '/observationMeasurementBinding',
                 event_use['observationMeasurementBinding'],
                 'EVENT_OBSERVATION_MEASUREMENT_CONDITIONAL',
                 'event_definition_inputs.py',
                 'stand_count_observation_measurement_selection',
                 'AR_EVENT_ASSOCIATION', allow_unpinned=True,
                 unpinned_reason='CASE_SPECIFIC_MEASUREMENT_APPLICABILITY_PENDING',
                 additional_dependencies=(event_claim['id'], *nomination_ids[1:]),
                 edge_class='CONDITIONAL')
            frontier('EVENT_OBSERVATION_MEASUREMENT', use_id,
                     '/observationMeasurementBinding',
                     'CASE_SPECIFIC_MEASUREMENT_APPLICABILITY_PENDING', selected['id'])
        frontier('EVENT_DEFINITION_RECURSIVE_RULES', use_id, '',
                 'COMPLETE_EVENT_CASE_AND_OWNER_RULES_PENDING', selected['id'])
        if not case_ready:
            frontier('EVENT_EXTENSION_CASE', use_id, '/canonicalCaseBinding',
                     'TYPED_EVENT_EXTENSION_SELECTION_AND_RULE_PENDING',
                     event_children['canonicalCaseBinding']['id'])
            continue
        for field, version, role in (
                ('vocabularyDefinitionBinding', EVENT_VOCABULARY_VERSION,
                 'EVENT_VOCABULARY_MEMBERSHIP'),
                ('packDefinitionBinding', EVENT_PACK_VERSION,
                 'EVENT_PACK_MEMBERSHIP')):
            parent = event_children[field]
            if parent['structuralSelection'] != 'PASS':
                frontier(role, use_id, '/' + field,
                         'SELECTED_EVENT_DEFINITION_ORIGINAL_UNAVAILABLE', parent['id'])
                continue
            selected_definition = selected_record(
                event_use.get(field), role, use_id, '/' + field, parent['id'])
            if selected_definition is None:
                continue
            definition_id, definition = selected_definition
            source_schema, source_schema_reason = _event_schema_status(
                'eventVocabulary' if field == 'vocabularyDefinitionBinding'
                else 'eventPack', definition)
            if source_schema == 'FAIL':
                source_shape_failure(
                    parent['id'], definition_id, event_use[field],
                    role + '_SOURCE_SHAPE', 'event_definition_inputs.py',
                    'event_definition_inputs.py', source_schema_reason,
                    finding_id='AR_EVENT_ASSOCIATION')
                continue
            if source_schema != 'PASS':
                frontier(role, definition_id, '', source_schema_reason, parent['id'])
                continue
            if (definition.get('schemaVersion') != version
                    or definition.get('definitionId') != event_use[field]['ref']):
                frontier(role, definition_id, '',
                         'EVENT_DEFINITION_VERSION_OR_IDENTITY_UNVERIFIED', parent['id'])
                continue
            members = definition.get('caseBindings')
            if not isinstance(members, list) or not members:
                frontier(role, definition_id, '/caseBindings',
                         'EVENT_CASE_MEMBERSHIP_SET_UNAVAILABLE', parent['id'])
                continue
            expanded.append(definition_id)
            for index, member in enumerate(members):
                emit_comparison(parent['id'], definition_id,
                                '/caseBindings/' + str(index), member,
                                role + '_VALUE', case_selection,
                                additional_dependencies=(
                                    event_children['canonicalCaseBinding']['id'],))
            if field == 'packDefinitionBinding':
                emit_comparison(parent['id'], definition_id,
                                '/vocabularyDefinitionBinding',
                                definition.get('vocabularyDefinitionBinding'),
                                'EVENT_PACK_VOCABULARY_MEMBERSHIP_VALUE', case_selection,
                                additional_dependencies=(
                                    event_children['vocabularyDefinitionBinding']['id'],))

    return {'status': 'PARTIAL', 'knownOccurrenceCount': len(rows),
            'occurrences': rows, 'expandedInputIds': list(dict.fromkeys(expanded)),
            'selectedEventUseRoots': event_roots,
            'operationCarrierSelections': carrier_selections,
            'frontier': frontiers,
            'qualification': 'Exact operation carrier candidates, selected work conditions, sample relations and event-use fields only. Active stage, further carrier comparisons, owner use and complete protected obligations remain open.'}
