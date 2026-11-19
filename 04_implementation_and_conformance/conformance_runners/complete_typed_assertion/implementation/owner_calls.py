"""Candidate-only owner transport. Full #47 public consumer integration is pending.

An OWNER_REPORT outcome means a concrete checker returned, not that it passed.
Dependency/worker failures never masquerade as owner verdicts. All selections
are local trusted configuration; caller input cannot select code or paths.
"""
import base64
import hashlib
import importlib
import importlib.machinery
import importlib.metadata
import io
import json
import platform
import re
import subprocess
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
SELECTION_SHA256 = '10a810e2b2cc513cbd37ed135f9e2be2d70fc937470dc4bee5075c3101877cf6'
FIELDS = {
    'act': {'act_bytes', 'content_bytes', 'rendered_bytes', 'context_bytes',
            'policy_bytes', 'source_inputs', 'trusted_pins', 'expected_act_selection',
            'intent_profile_bytes', 'schema_bundle'},
    'event': {'proof_bytes', 'envelope_bytes', 'request_bytes', 'context_bytes',
              'profile_bytes', 'trusted_pins', 'expected_proof_binding', 'use_mode'},
    'state': {'proof_bytes', 'selected', 'context_bytes', 'policy_bytes', 'snapshot_bytes', 'records'},
    'authorization': {'evidence_bytes', 'profile_bytes', 'context_bytes', 'source_bytes',
                      'schema_bytes', 'expected_context_sha256'},
    'occupancy': {'request_bytes', 'context_bytes', 'records', 'trusted_pins'},
}
LIBRARY_MODULES = ('rfc8785', 'jsonschema', 'jsonschema_specifications', 'referencing',
                   'attr', 'attrs', 'rpds', 'typing_extensions')
EVALUATION_SELECTION_SCHEMA_SHA256 = 'b0f5ffdc4e97ab745c6e666dcbbeef8ee4485efdb265251904f5447e966b03d9'
EVALUATION_SELECTION_V0_5_SCHEMA_SHA256 = '3928be7c89dc3a4547415b21938f6f79256627171508384270beb968118942b5'
EVALUATION_SELECTION_VERSIONS = {
    'ofarm.assertionDomainEvaluationSelection.v0.4': (
        'https://ofarm.dev/schema/drafts/non-default/assertion-domain/evaluation-selection/v0.4',
        EVALUATION_SELECTION_SCHEMA_SHA256, 'EXACT_REVIEWED_V0_4_SCHEMA_AND_UNIQUENESS'),
    'ofarm.assertionDomainEvaluationSelection.v0.5': (
        'https://ofarm.dev/schema/drafts/non-default/assertion-domain/evaluation-selection/v0.5',
        EVALUATION_SELECTION_V0_5_SCHEMA_SHA256, 'EXACT_REVIEWED_V0_5_SCHEMA_AND_UNIQUENESS'),
}
SELECTION_SCHEMAS = (
    # EvaluationSelection.sourceSelections follows the reviewed payload/v0.1
    # immutableBinding reference into this exact AssertionRecord schema.
    ('https://ofarm.dev/schema/assertionrecord/v0.2',
     'components/revision-02/sources/OFARM/389a8f6b6bb2/03_machine_contracts/drafts_non_default/assertion_record_submission/OFARM_AssertionRecord_schema_v0_2.json',
     '3a7044086a2b0a226109ac00b361332503d77b07efd602b29402662515b67f1e'),
    ('https://ofarm.dev/schema/drafts/non-default/assertion-domain/evaluation-selection/v0.4',
     'schemas/evaluation-selection.schema.json', EVALUATION_SELECTION_SCHEMA_SHA256),
    ('https://ofarm.dev/schema/drafts/non-default/assertion-domain/evaluation-selection/v0.5',
     'schemas/evaluation-selection-v0_5.schema.json', EVALUATION_SELECTION_V0_5_SCHEMA_SHA256),
    ('https://ofarm.dev/schema/drafts/non-default/assertion-domain/immutable-input-closure/v0.3',
     'schemas/immutable-input-closure.schema.json', '133af8f25a06f7eea180875cc33bd20f357f832ecd506de5dbbafb3a549d0b85'),
    ('https://ofarm.dev/schema/drafts/non-default/authorization-finalization-evidence/protected-effect-validation-trace/v0.1',
     'source-contracts/ProtectedEffectValidationTrace.schema.json', 'a5150119555a2faaa0531ae96e650dcefd5cb491fa30fd8ffe337c873f6cdae3'),
    ('https://ofarm.dev/schema/drafts/non-default/assertion-record-domain-validation/payload/v0.1',
     'outer/payload-schema.json', '1a1622fdce7d4437c5d63afbb6888e17a01c89dba8fb363cf7a051ace6493add'),
)
MAX_ORIGINAL_BYTES = 2 * 1024 * 1024
MAX_JSON_DEPTH = 64


def validate_condition_property_revision_sources(selection):
    """Validate v0.5 references inside the already pinned inventory worker."""
    if 'conditionPropertyRevisionSources' not in selection:
        return
    if selection.get('schemaVersion') != 'ofarm.assertionDomainEvaluationSelection.v0.5':
        raise ValueError('Condition property revision sources require evaluation selection v0.5.')
    selected = selection['conditionPropertyRevisionSources']
    if (type(selected) is not dict or set(selected) != {'ruleInputId', 'mapInputId'}
            or any(type(value) is not str or not value for value in selected.values())
            or selected['ruleInputId'] == selected['mapInputId']):
        raise ValueError('Condition property revision sources require distinct nonempty rule and map input IDs.')
    originals = selection.get('originalSelections')
    if type(originals) is not list:
        raise ValueError('Condition property revision sources require selected originals.')
    for iid in selected.values():
        matches = [pin for pin in originals if type(pin) is dict and pin.get('inputId') == iid]
        if len(matches) != 1 or matches[0].get('digestMode') != 'JCS_JSON':
            raise ValueError('Condition property revision source must name one selected JCS_JSON original: ' + iid)


class IntegrityError(RuntimeError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def wire_bytes(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8')


def evidence(raw):
    raw = raw or b''
    return {'rawSha256': sha(raw), 'byteLength': len(raw),
            'originalBytesBase64': base64.b64encode(raw).decode('ascii')}


def encode(value):
    if isinstance(value, bytes):
        return {'originalBytesBase64': base64.b64encode(value).decode('ascii')}
    if isinstance(value, dict):
        if 'originalBytesBase64' in value or not all(isinstance(k, str) for k in value):
            raise ValueError('Reserved byte transport member or non-string key in caller value.')
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [encode(v) for v in value]
    if value is None or type(value) in (str, int, float, bool):
        return value
    raise ValueError('Unsupported transport value type.')


def decode(value):
    if isinstance(value, dict):
        if set(value) == {'originalBytesBase64'}:
            return base64.b64decode(value['originalBytesBase64'], validate=True)
        if 'originalBytesBase64' in value:
            raise ValueError('Ambiguous byte transport.')
        return {k: decode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [decode(v) for v in value]
    return value


def load_selection():
    raw = (HERE / 'dependency-selection.json').read_bytes()
    if sha(raw) != SELECTION_SHA256:
        raise IntegrityError('DEPENDENCY_SELECTION_BYTES_MISMATCH')
    selection = json.loads(raw)
    # Location is transport metadata. The interpreter, library and owner closures
    # retain independent byte pins before launch and again inside the worker.
    groups = [(selection['interpreter'], ('path', 'stdlibRoot', 'extensionRoot', 'stdlibManifestPath')),
              (selection['libraries'], ('root', 'manifestPath'))]
    groups.extend((owner, ('root', 'checkerRoot', 'sourceRoot', 'contractRoot', 'manifestPath'))
                  for owner in selection['owners'].values())
    for entry, keys in groups:
        for key in keys:
            entry[key] = str((HERE.parent / entry[key]).resolve())
    return selection


def closure(root, manifest_path, manifest_sha256, *, excluded_root=None):
    """Verify the complete inventory, including data/metadata and extra files."""
    raw = Path(manifest_path).read_bytes()
    if sha(raw) != manifest_sha256:
        raise IntegrityError('CLOSURE_MANIFEST_BYTES_MISMATCH: ' + str(manifest_path))
    manifest = json.loads(raw)
    root = Path(root).resolve()
    files = manifest['files']
    if manifest['fileCount'] != len(files):
        raise IntegrityError('CLOSURE_COUNT_MISMATCH')
    inventory = {}
    relative_names = set()
    for pin in files:
        relative = PurePosixPath(pin['path'])
        if relative.is_absolute() or '..' in relative.parts or '\\' in pin['path']:
            raise IntegrityError('UNSAFE_CLOSURE_PATH')
        path = root / pin['path']
        resolved = path.resolve()
        if not resolved.is_relative_to(root) or resolved in inventory or pin['path'] in relative_names:
            raise IntegrityError('ESCAPING_OR_DUPLICATE_CLOSURE_PATH')
        value = path.read_bytes()
        if len(value) != pin['byteLength'] or sha(value) != pin['rawSha256']:
            raise IntegrityError('DEPENDENCY_FILE_BYTES_MISMATCH: ' + str(path))
        inventory[resolved] = pin
        relative_names.add(pin['path'])
    actual = set()
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if excluded_root and relative.parts[0] == excluded_root:
            continue
        if path.is_file() or path.is_symlink():
            actual.add(relative.as_posix())
    if actual != relative_names:
        raise IntegrityError('CLOSURE_FILE_SET_MISMATCH: ' + str(root))
    return inventory


def verify_dependencies(selection):
    selected = selection['interpreter']
    executable = Path(selected['path'])
    if sha(executable.read_bytes()) != selected['rawSha256']:
        raise IntegrityError('INTERPRETER_BYTES_MISMATCH')
    standard = closure(selected['stdlibRoot'], selected['stdlibManifestPath'],
                       selected['stdlibManifestRawSha256'], excluded_root='site-packages')
    library = selection['libraries']
    libraries = closure(library['root'], library['manifestPath'], library['manifestRawSha256'])
    owners = {}
    for kind, owner in selection['owners'].items():
        owners[kind] = closure(owner['root'], owner['manifestPath'], owner['manifestRawSha256'])
        if len(owners[kind]) != owner['fileCount']:
            raise IntegrityError('OWNER_CLOSURE_COUNT_MISMATCH: ' + kind)
    if set(owners) != set(FIELDS):
        raise IntegrityError('OWNER_SELECTION_SET_MISMATCH')
    return standard, libraries, owners


def selected_owner_root(kind):
    """Return exact external contract/schema root after checking all owner bytes."""
    if kind not in FIELDS:
        raise ValueError('Unknown selected owner.')
    selection = load_selection()
    verify_dependencies(selection)
    return Path(selection['owners'][kind]['contractRoot'])


def candidate_closure(expected_manifest_sha256):
    """Verify every candidate file before importing domain implementation."""
    manifest_path = HERE / 'candidate-manifest.json'
    if manifest_path.is_symlink():
        raise IntegrityError('CANDIDATE_MANIFEST_SYMLINK')
    raw = manifest_path.read_bytes()
    if sha(raw) != expected_manifest_sha256:
        raise IntegrityError('CANDIDATE_MANIFEST_BYTES_MISMATCH')
    manifest = _strict_json(raw)
    if manifest.get('implementationCompleteness') != 'INCOMPLETE' or type(manifest.get('members')) is not list:
        raise IntegrityError('INVALID_CANDIDATE_MANIFEST')
    inventory = {}
    names = set()
    for pin in manifest['members']:
        name = pin['path']
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name or name in names:
            raise IntegrityError('UNSAFE_OR_DUPLICATE_CANDIDATE_MEMBER')
        source = HERE / name
        path = source.resolve()
        if source.is_symlink() or not path.is_relative_to(HERE) or not path.is_file():
            raise IntegrityError('INVALID_CANDIDATE_MEMBER: ' + name)
        value = path.read_bytes()
        if sha(value) != pin['rawSha256'] or len(value) != pin['byteLength']:
            raise IntegrityError('CANDIDATE_MEMBER_BYTES_MISMATCH: ' + name)
        inventory[path] = pin
        names.add(name)
    actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() or p.is_symlink()}
    if actual - {'candidate-manifest.json'} != names:
        raise IntegrityError('CANDIDATE_FILE_SET_MISMATCH')
    return inventory


def verify_interpreter(selection):
    selected = selection['interpreter']
    if (Path(sys.executable).resolve() != Path(selected['path']) or sys.version != selected['version']
            or sys.implementation.name != selected['implementation']
            or sys.implementation.cache_tag != selected['cacheTag']
            or platform.system() != selected['platform'] or platform.machine() != selected['machine']):
        raise IntegrityError('RUNNING_INTERPRETER_IDENTITY_MISMATCH')
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        raise IntegrityError('ISOLATED_WORKER_FLAGS_REQUIRED')


def install_import_guard(selection, kind, inventories, candidate_inventory=None):
    standard, libraries, owners = inventories
    owner = selection['owners'].get(kind)
    inventory = standard | libraries | (owners[kind] if owner else {}) | (candidate_inventory or {})
    owner_code = ({Path(owner['root']).resolve() / name for name in owner['executableFiles']}
                  if owner else set())
    executable_paths = {path for path in standard | libraries | (candidate_inventory or {})
                        if path.suffix == '.py' or any(str(path).endswith(s) for s in importlib.machinery.EXTENSION_SUFFIXES)}
    executable_paths |= owner_code

    def verify_origin(path):
        resolved = Path(path).resolve()
        if resolved not in executable_paths:
            raise IntegrityError('UNPINNED_IMPORT_ORIGIN: ' + str(path))
        raw = resolved.read_bytes()
        pin = inventory[resolved]
        if len(raw) != pin['byteLength'] or sha(raw) != pin['rawSha256']:
            raise IntegrityError('IMPORTED_FILE_BYTES_MISMATCH: ' + str(path))
        return raw

    class VerifiedSourceLoader(importlib.machinery.SourceFileLoader):
        def get_code(self, fullname):
            # Compile the exact bytes verified here; never read an ambient pyc.
            return self.source_to_code(verify_origin(self.path), self.path)

    class VerifiedExtensionLoader(importlib.machinery.ExtensionFileLoader):
        def create_module(self, spec):
            verify_origin(spec.origin)
            return super().create_module(spec)

        def exec_module(self, module):
            verify_origin(self.path)
            return super().exec_module(module)

    class VerifiedFinder:
        @classmethod
        def find_distributions(cls, context=None):
            selected_context = importlib.metadata.DistributionFinder.Context(
                name=getattr(context, 'name', None), path=[selection['libraries']['root']])
            return importlib.metadata.MetadataPathFinder.find_distributions(selected_context)

        @classmethod
        def find_spec(cls, fullname, path=None, target=None):
            spec = importlib.machinery.PathFinder.find_spec(fullname, path, target)
            if spec is not None:
                if spec.origin is None:
                    raise IntegrityError('UNSELECTED_NAMESPACE_IMPORT: ' + fullname)
                verify_origin(spec.origin)
            return spec

    selected = selection['interpreter']
    sys.path[:] = [selected['stdlibRoot'], selected['extensionRoot'], selection['libraries']['root']]
    if owner:
        sys.path.append(owner['checkerRoot'])
    if kind == 'domain':
        sys.path.append(str(HERE))
    sys.path_hooks[:] = [importlib.machinery.FileFinder.path_hook(
        (VerifiedSourceLoader, importlib.machinery.SOURCE_SUFFIXES),
        (VerifiedExtensionLoader, importlib.machinery.EXTENSION_SUFFIXES))]
    sys.path_importer_cache.clear()
    sys.meta_path[:] = [importlib.machinery.BuiltinImporter, importlib.machinery.FrozenImporter, VerifiedFinder]

    def audit():
        result = []
        for name, module in list(sys.modules.items()):
            if module is None or name == '__main__':
                continue
            spec = getattr(module, '__spec__', None)
            origin = getattr(spec, 'origin', None)
            if origin in ('built-in', 'frozen'):
                continue
            if not origin:
                # Some stdlib-created aliases lack specs. They must be aliases
                # of modules with a pinned file, or file-free stdlib objects.
                origin = getattr(module, '__file__', None)
                if not origin:
                    continue
            raw = verify_origin(origin)
            result.append({'module': name, 'path': str(Path(origin).resolve()), 'rawSha256': sha(raw)})
        return sorted(result, key=lambda p: p['module'])

    return audit


def _failure(status, kind, error, **details):
    return {'schemaVersion': 'fixture.ownerInvocation.v0.1', 'status': status, 'owner': kind,
            'ownerReport': None, 'error': str(error), **details}


def _launch(request):
    """Private fixed-policy launch: caller data cannot supply command/env/root."""
    kind = request['kind']
    started = time.monotonic()
    try:
        selection = load_selection()
        verify_dependencies(selection)
    except (IntegrityError, OSError, ValueError, KeyError) as exc:
        return _failure('DEPENDENCY_INTEGRITY_ERROR', kind, exc)
    selected = selection['interpreter']
    command = [selected['path'], *selected['flags'], str(HERE / 'owner_calls.py'), '--worker']
    raw_request = wire_bytes(request)
    timeout = selection['workerPolicy']['timeoutSeconds']
    common = {'dependencySelectionRawSha256': SELECTION_SHA256,
              'requestRawSha256': sha(raw_request), 'requestByteLength': len(raw_request),
              'command': command, 'timeoutSeconds': timeout}
    try:
        process = subprocess.run(command, input=raw_request, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 timeout=timeout, check=False, cwd=HERE, env=selected['environment'])
    except subprocess.TimeoutExpired as exc:
        status = 'DOMAIN_EXECUTION_TIMEOUT' if kind == 'domain' else 'OWNER_EXECUTION_TIMEOUT'
        return _failure(status, kind, 'Selected worker deadline exceeded.',
                        **common, elapsedSeconds=time.monotonic() - started,
                        stdout=evidence(exc.stdout), stderr=evidence(exc.stderr))
    except OSError as exc:
        return _failure('DOMAIN_EXECUTION_ERROR' if kind == 'domain' else 'OWNER_EXECUTION_ERROR', kind, exc, **common)
    transport = common | {'elapsedSeconds': time.monotonic() - started,
                          'returnCode': process.returncode,
                          'stdout': evidence(process.stdout), 'stderr': evidence(process.stderr)}
    if process.returncode != 0:
        return _failure('DOMAIN_EXECUTION_ERROR' if kind == 'domain' else 'OWNER_EXECUTION_ERROR',
                        kind, 'Worker exited unsuccessfully.', **transport)
    try:
        response = json.loads(process.stdout)
        if not isinstance(response, dict) or response.get('owner') != kind or response.get('schemaVersion') != 'fixture.ownerInvocation.v0.1':
            raise ValueError('Invalid worker envelope.')
    except (UnicodeError, ValueError) as exc:
        return _failure('DOMAIN_PROTOCOL_ERROR' if kind == 'domain' else 'OWNER_PROTOCOL_ERROR', kind, exc, **transport)
    return response | {'transport': transport}


def invoke_owner(kind, inputs, original_intent_bytes=None):
    """Foundation API. Returns transport status plus the unchanged owner report."""
    if kind not in FIELDS or type(inputs) is not dict or set(inputs) != FIELDS[kind]:
        return _failure('INVOCATION_INPUT_ERROR', kind, 'Wrong fields for selected concrete owner API.')
    kwargs = dict(inputs)
    if kind == 'act':
        kwargs['intent_bytes'] = original_intent_bytes
    try:
        request = {'kind': kind, 'operation': 'invoke', 'inputs': encode(kwargs)}
        wire_bytes(request)
    except (ValueError, TypeError, RecursionError) as exc:
        return _failure('INVOCATION_INPUT_ERROR', kind, exc)
    return _launch(request)


def preflight(kind):
    """Imports and audits one checker without evaluating a claim."""
    if kind not in FIELDS:
        return _failure('INVOCATION_INPUT_ERROR', kind, 'Unknown owner.')
    return _launch({'kind': kind, 'operation': 'preflight'})


def verify_original_inventory(selection_bytes, trusted_selection_sha256, originals):
    """Check selected original bytes without accepting claim or source meaning.

    The caller must obtain trusted_selection_sha256 independently of the claim.
    Full evaluation-selection schema validation and requirement derivation are
    separate gates; this result alone never authorizes a domain PASS.
    """
    if (type(selection_bytes) is not bytes or type(trusted_selection_sha256) is not str
            or not re.fullmatch(r'[0-9a-f]{64}', trusted_selection_sha256)
            or type(originals) is not dict or not all(type(k) is str and type(v) is bytes
                                                    for k, v in originals.items())):
        return _failure('INVOCATION_INPUT_ERROR', 'domain', 'Invalid original-inventory input types.')
    request = {'kind': 'domain', 'operation': 'originals',
               'selectionBytes': encode(selection_bytes),
               'trustedSelectionRawSha256': trusted_selection_sha256,
               'originals': encode(originals)}
    return _launch(request)


def verify_original_inventory_in_worker(selection_bytes, trusted_selection_sha256, originals):
    """Use the same verifier inside an already pinned isolated domain worker.

    The outer worker has verified the candidate/dependencies and installed the
    import guard. This avoids a second dependency scan and subprocess for an
    owned byte-inventory operation; no foreign owner checker runs here.
    """
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        return _failure('DEPENDENCY_INTEGRITY_ERROR', 'domain', 'Guarded domain worker flags required.')
    if (type(selection_bytes) is not bytes or type(trusted_selection_sha256) is not str
            or not re.fullmatch(r'[0-9a-f]{64}', trusted_selection_sha256)
            or type(originals) is not dict or not all(type(k) is str and type(v) is bytes
                                                    for k, v in originals.items())):
        return _failure('INVOCATION_INPUT_ERROR', 'domain', 'Invalid original-inventory input types.')
    request = {'selectionBytes': encode(selection_bytes),
               'trustedSelectionRawSha256': trusted_selection_sha256,
               'originals': encode(originals)}
    try:
        result = _original_inventory(request)
    except (ValueError, TypeError, KeyError, UnicodeError, OverflowError) as exc:
        return _failure('INVOCATION_INPUT_ERROR', 'domain', exc)
    return {'schemaVersion': 'fixture.ownerInvocation.v0.1', 'owner': 'domain',
            'status': 'ORIGINAL_INVENTORY', 'ownerReport': None, **result}


def verify_source_selector(candidate_manifest_sha256, context_bytes, context_pin, entry_pointer,
                           source_bytes, source_pin, storage_spec):
    """Run one bounded domain-owned selector comparison in the pinned worker.

    The caller must independently derive the pins, pointer and storage read;
    this operation cannot supply the missing production requirement graph.
    """
    if type(candidate_manifest_sha256) is not str or not re.fullmatch(r'[0-9a-f]{64}', candidate_manifest_sha256):
        return _failure('INVOCATION_INPUT_ERROR', 'domain', 'Invalid candidate manifest pin.')
    try:
        request = {'kind': 'domain', 'operation': 'source_selector',
                   'package': {'manifestRawSha256': candidate_manifest_sha256},
                   'contextBytes': encode(context_bytes), 'contextPin': encode(context_pin),
                   'entryPointer': entry_pointer, 'sourceBytes': encode(source_bytes),
                   'sourcePin': encode(source_pin), 'storageSpec': encode(storage_spec)}
        wire_bytes(request)
    except (ValueError, TypeError, RecursionError) as exc:
        return _failure('INVOCATION_INPUT_ERROR', 'domain', exc)
    return _launch(request)


def evaluate_domain(original_intent_bytes, original_result_bytes, *, package, owner_inputs):
    """Public offline consumer transport; returns a real domain report or error."""
    if (type(original_intent_bytes) is not bytes or type(original_result_bytes) is not bytes
            or type(package) is not dict or type(owner_inputs) is not dict
            or type(package.get('manifestRawSha256')) is not str
            or not re.fullmatch(r'[0-9a-f]{64}', package['manifestRawSha256'])
            or package.get('root') != str(HERE)):
        return _failure('INVOCATION_INPUT_ERROR', 'domain', 'Invalid candidate invocation or package pin.')
    try:
        request = {'kind': 'domain', 'operation': 'evaluate',
                   'intentBytes': encode(original_intent_bytes),
                   'resultBytes': encode(original_result_bytes),
                   'package': package, 'ownerInputs': encode(owner_inputs)}
        wire_bytes(request)
    except (ValueError, TypeError, RecursionError) as exc:
        return _failure('INVOCATION_INPUT_ERROR', 'domain', exc)
    return _launch(request)


def _strict_json(raw):
    if type(raw) is not bytes or len(raw) > MAX_ORIGINAL_BYTES:
        raise ValueError('JSON input exceeds the selected 2 MiB per-input bound.')
    depth = 0
    quoted = escaped = False
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
            if depth > MAX_JSON_DEPTH:
                raise ValueError('JSON nesting exceeds 64 levels.')
        elif byte in (93, 125):
            depth -= 1
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON number')))


def _validate_selection_schema(value):
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012

    def reject_unselected(uri):
        raise ValueError('Unselected schema reference: ' + uri)

    registry = Registry(retrieve=reject_unselected)
    version = value.get('schemaVersion') if type(value) is dict else None
    if version not in EVALUATION_SELECTION_VERSIONS:
        raise ValueError('Unsupported evaluation-selection version.')
    selected_uri, selected_schema_hash, selected_label = EVALUATION_SELECTION_VERSIONS[version]
    schema = None
    for uri, relative, expected_sha in SELECTION_SCHEMAS:
        if (relative in ('schemas/evaluation-selection.schema.json', 'schemas/evaluation-selection-v0_5.schema.json')
                and uri != selected_uri):
            continue
        raw = (HERE / relative).read_bytes()
        if sha(raw) != expected_sha:
            raise IntegrityError('SELECTED_SCHEMA_BYTES_MISMATCH: ' + relative)
        document = _strict_json(raw)
        if '$id' in document and document['$id'] != uri:
            raise IntegrityError('SELECTED_SCHEMA_ID_MISMATCH: ' + relative)
        Draft202012Validator.check_schema(document)
        registry = registry.with_resource(uri, Resource.from_contents(document, default_specification=DRAFT202012))
        if uri == selected_uri:
            schema = document
    errors = list(Draft202012Validator(schema, registry=registry).iter_errors(value))
    if errors:
        first = min(errors, key=lambda error: (list(map(str, error.absolute_path)), error.message))
        raise ValueError('Selection schema mismatch at /' + '/'.join(map(str, first.absolute_path)) + ': ' + first.message)
    return selected_schema_hash, selected_label


def _original_inventory(request):
    rfc8785 = importlib.import_module('rfc8785')
    selected_bytes = decode(request['selectionBytes'])
    trusted_hash = request['trustedSelectionRawSha256']
    originals = decode(request['originals'])
    if type(selected_bytes) is not bytes or type(originals) is not dict:
        raise ValueError('Malformed original byte transport.')
    if sha(selected_bytes) != trusted_hash:
        raise ValueError('Independently pinned selection bytes differ.')
    selection = _strict_json(selected_bytes)
    if (type(selection) is not dict
            or selection.get('schemaVersion') not in EVALUATION_SELECTION_VERSIONS
            or not isinstance(selection.get('selectionId'), str) or not selection['selectionId']
            or type(selection.get('originalSelections')) is not list
            or not selection['originalSelections']):
        raise ValueError('Invalid evaluation-selection inventory header.')
    required_fields = {'schemaVersion', 'selectionId', 'effectIntent', 'authorizationResult',
                       'currentActionRuleBinding', 'originalSelections'}
    optional_fields = {'sourceSelections'}
    if selection['schemaVersion'] == 'ofarm.assertionDomainEvaluationSelection.v0.5':
        optional_fields.add('conditionPropertyRevisionSources')
    if not required_fields <= set(selection) or set(selection) - required_fields - optional_fields:
        raise ValueError('Unexpected evaluation-selection fields.')
    selection_schema_hash, selection_label = _validate_selection_schema(selection)
    seen_ids, seen_refs = set(), set()
    inventory, admitted_json = [], {}
    for pin in selection['originalSelections']:
        if type(pin) is not dict:
            raise ValueError('Original selection is not an object.')
        mode = pin.get('digestMode')
        expected = ({'inputId', 'ref', 'digestMode', 'rawSha256', 'byteLength', 'wholeJcsDigest'}
                    if mode == 'JCS_JSON' else
                    {'inputId', 'ref', 'digestMode', 'rawSha256', 'byteLength'} if mode == 'RAW_BYTES' else None)
        if expected is None or set(pin) != expected:
            raise ValueError('Invalid mode-specific original selection.')
        iid, ref = pin['inputId'], pin['ref']
        if (type(iid) is not str or not iid or type(ref) is not str or not ref
                or iid in seen_ids or ref in seen_refs
                or type(pin['rawSha256']) is not str or not re.fullmatch(r'[0-9a-f]{64}', pin['rawSha256'])
                or type(pin['byteLength']) is not int or pin['byteLength'] < 0):
            raise ValueError('Invalid or duplicate original identity/pin.')
        if mode == 'JCS_JSON' and (type(pin['wholeJcsDigest']) is not str
                                    or not re.fullmatch(r'sha256:[0-9a-f]{64}', pin['wholeJcsDigest'])):
            raise ValueError('Invalid whole-value JCS pin.')
        if pin['byteLength'] > MAX_ORIGINAL_BYTES:
            raise ValueError('Selected original exceeds the reviewed per-input bound.')
        seen_ids.add(iid)
        seen_refs.add(ref)
        raw = originals.get(iid)
        if raw is None:
            result = {'status': 'NOT_EVALUATED', 'reason': 'ORIGINAL_UNAVAILABLE'}
        elif type(raw) is not bytes:
            raise ValueError('Original transport is not bytes.')
        else:
            if len(raw) > MAX_ORIGINAL_BYTES:
                raise ValueError('Original transport exceeds the reviewed per-input bound.')
            observed = {'observedRawSha256': sha(raw), 'byteLength': len(raw)}
            if observed['observedRawSha256'] != pin['rawSha256'] or len(raw) != pin['byteLength']:
                result = {'status': 'MISMATCH', **observed, 'reason': 'PIN_MISMATCH'}
            elif mode == 'RAW_BYTES':
                result = {'status': 'MATCHED', **observed}
            else:
                try:
                    value = _strict_json(raw)
                    actual_jcs = 'sha256:' + sha(rfc8785.dumps(value))
                except (UnicodeError, ValueError, OverflowError, TypeError):
                    result = {'status': 'MISMATCH', **observed, 'reason': 'INVALID_JSON'}
                else:
                    if actual_jcs != pin['wholeJcsDigest']:
                        result = {'status': 'MISMATCH', **observed, 'reason': 'PIN_MISMATCH'}
                    else:
                        result = {'status': 'MATCHED', **observed}
                        admitted_json[iid] = value
        inventory.append({'inputId': iid, 'result': result})
    if set(originals) - seen_ids:
        raise ValueError('Unselected original transport bytes.')
    validate_condition_property_revision_sources(selection)
    return {'selectionBinding': {'rawSha256': trusted_hash,
                                 'wholeJcsDigest': 'sha256:' + sha(rfc8785.dumps(selection))},
            'inventory': inventory, 'admittedJson': admitted_json,
            'selectionShapeValidated': selection_label,
            'selectionSchemaRawSha256': selection_schema_hash,
            'qualification': 'Selection shape and original bytes checked; source admission and domain graph remain separate.'}


def worker():
    kind = None
    operation = None
    out, err = io.StringIO(), io.StringIO()
    try:
        request = json.load(sys.stdin)
        kind = request['kind']
        operation = request.get('operation')
        if not ((kind in FIELDS and operation in ('preflight', 'invoke'))
                or (kind == 'domain' and operation in ('originals', 'evaluate', 'source_selector'))):
            raise ValueError('Unknown worker operation.')
        fields = ({'kind', 'operation'} if operation == 'preflight' else
                  {'kind', 'operation', 'inputs'} if operation == 'invoke' else
                  {'kind', 'operation', 'selectionBytes', 'trustedSelectionRawSha256', 'originals'}
                  if operation == 'originals' else
                  {'kind', 'operation', 'contextBytes', 'contextPin', 'entryPointer',
                   'sourceBytes', 'sourcePin', 'storageSpec', 'package'}
                  if operation == 'source_selector' else
                  {'kind', 'operation', 'intentBytes', 'resultBytes', 'package', 'ownerInputs'})
        if set(request) != fields:
            raise ValueError('Unexpected worker fields.')
        selection = load_selection()
        verify_interpreter(selection)
        inventories = verify_dependencies(selection)
        candidate_inventory = (candidate_closure(request['package']['manifestRawSha256'])
                               if operation in ('evaluate', 'source_selector') else None)
        audit = install_import_guard(selection, kind, inventories, candidate_inventory)
        with redirect_stdout(out), redirect_stderr(err):
            for module in LIBRARY_MODULES:
                importlib.import_module(module)
            for distribution, expected in selection['libraries']['distributions'].items():
                if importlib.metadata.version(distribution) != expected:
                    raise IntegrityError('DISTRIBUTION_VERSION_MISMATCH: ' + distribution)
            before = audit()
            if operation == 'originals':
                result = {'schemaVersion': 'fixture.ownerInvocation.v0.1', 'owner': kind,
                          'status': 'ORIGINAL_INVENTORY', 'ownerReport': None,
                          'importsBeforeChecker': before, **_original_inventory(request),
                          'importsAfterChecker': audit()}
            elif operation == 'source_selector':
                comparator = importlib.import_module('source_selector').compare
                comparison = comparator(decode(request['contextBytes']), decode(request['contextPin']),
                                        request['entryPointer'], decode(request['sourceBytes']),
                                        decode(request['sourcePin']), decode(request['storageSpec']))
                result = {'schemaVersion': 'fixture.ownerInvocation.v0.1', 'owner': kind,
                          'status': 'SOURCE_SELECTOR_COMPARISON', 'ownerReport': None,
                          'sourceSelectorComparison': comparison,
                          'importsBeforeChecker': before, 'importsAfterChecker': audit()}
            elif operation == 'evaluate':
                evaluator = importlib.import_module('verify_domain').verify_domain
                report = evaluator(decode(request['intentBytes']), decode(request['resultBytes']),
                                   package=request['package'], owner_inputs=decode(request['ownerInputs']))
                result = {'schemaVersion': 'fixture.ownerInvocation.v0.1', 'owner': kind,
                          'status': 'DOMAIN_REPORT', 'ownerReport': None, 'domainReport': report,
                          'importsBeforeChecker': before, 'importsAfterChecker': audit()}
            else:
                owner = selection['owners'][kind]
                checker = getattr(importlib.import_module(owner['module']), owner['function'])
                result = {'schemaVersion': 'fixture.ownerInvocation.v0.1', 'owner': kind,
                          'status': 'PREFLIGHT_OK', 'ownerReport': None, 'importsBeforeChecker': audit(),
                          'ownerPackageManifestRawSha256': owner['manifestRawSha256']}
            if operation == 'invoke':
                kwargs = decode(request['inputs'])
                expected_fields = FIELDS[kind] | ({'intent_bytes'} if kind == 'act' else set())
                if type(kwargs) is not dict or set(kwargs) != expected_fields:
                    raise ValueError('Wrong concrete worker API fields.')
                roots = ({'contract_root': Path(owner['contractRoot']), 'source_root': Path(owner['sourceRoot'])}
                         if kind == 'authorization' else {'package_root': Path(owner['contractRoot'])})
                if kind in ('state', 'event', 'occupancy'):
                    roots['source_root'] = Path(owner['sourceRoot'])
                report = checker(**kwargs, **roots)
                # This serialization is precisely identified; it is not claimed
                # to be an original owner-authored on-disk report artifact.
                serialized = wire_bytes(report)
                result.update(status='OWNER_REPORT', ownerReport=report,
                              ownerReportSerialization=evidence(serialized),
                              importsAfterChecker=audit())
        result['ownerStdout'] = evidence(out.getvalue().encode())
        result['ownerStderr'] = evidence(err.getvalue().encode())
    except IntegrityError as exc:
        result = _failure('DEPENDENCY_INTEGRITY_ERROR', kind, exc,
                          ownerStdout=evidence(out.getvalue().encode()), ownerStderr=evidence(err.getvalue().encode()))
    except Exception as exc:
        status = ('INVOCATION_INPUT_ERROR' if kind == 'domain' and operation == 'originals'
                  and isinstance(exc, (ValueError, TypeError, KeyError)) else
                  'DOMAIN_EXECUTION_ERROR' if kind == 'domain' else 'OWNER_EXECUTION_ERROR')
        result = _failure(status, kind, type(exc).__name__ + ': ' + str(exc),
                          ownerStdout=evidence(out.getvalue().encode()), ownerStderr=evidence(err.getvalue().encode()))
    sys.stdout.buffer.write(wire_bytes(result))


if __name__ == '__main__':
    if sys.argv[1:] != ['--worker']:
        raise SystemExit('Private worker; use invoke_owner or preflight from the candidate harness.')
    worker()
