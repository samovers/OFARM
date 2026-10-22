"""Seal the reviewed repair evidence once. Never edit a sealed packet."""
from pathlib import Path
import hashlib,json,shutil,platform
H=Path(__file__).resolve().parent
assert not (H/'DELIVERY_MANIFEST.json').exists(),'Use a sibling repair after sealing.'
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def read(n):return json.loads((H/n).read_bytes())
full=read('conformance-results.json');target=read('targeted-results.json');edge=read('edge-results.json');helper=read('helper-integrity-results.json');api=read('api-only-results.json');oracle=read('runner-oracle-results.json');installed=read('installed-runner-results.json');mutation=read('mutation-coverage-ledger.json')
for result in [full,target,edge,helper,api,oracle,installed]:assert result['cases']==result['matched']
assert (full['cases'],target['cases'],edge['cases'],helper['cases'],api['cases'],oracle['cases'],installed['cases'])==(332,138,31,7,2,2,491)
assert mutation['directNegativeWitnessSites']==112 and mutation['checkSites']==115 and mutation['classifications']=={'PASS_EXPOSED':84,'SPECIFIC_ERROR_CHANGED':28,'SURVIVED_SAME_EXPECTED_ERROR':0,'NO_DIRECT_NEGATIVE_WITNESS':3}
index=read('cases.json');assert len(index['cases'])==491 and all('expectedCodes'in x for x in index['cases'])
for item in index['cases']:
 if item['expected']=='PASS':assert item['expectedCodes']==[]
 else:assert len(item['expectedCodes'])==1
for d in (H/'fixtures').glob('basis-*'):
 source=H/'checks'/(d.name+'-baseline')/'api-report.json';assert json.loads(source.read_bytes())['disposition']=='PASS';(d/'api-report.json').write_bytes(source.read_bytes())
# Reproducible installed copies are omitted; exact input cases and run reports stay.
layout=H/'edge-checks/installed-layout'
if layout.exists():shutil.rmtree(layout)
ledger=read('repair-ledger.json');ledger.update(status='SEALED_FOR_FRESH_REVIEW',resolvedFindings=['F1','F2','F3','F4','F5','P1','P2'],reviewAuthority='AUTHOR_SIDE; no formal two-reviewer gate satisfied',limits=['Selected sharing paths explicitly outside this profile','Full producer profile and complete v0.2 decision package not established','No eligibility, principal trust, CP3 admission, runtime/process attestation or effect permission','Python 3.11 compatibility not tested','Three must() failure branches structurally redundant after earlier checked trace conditions'])
(H/'repair-ledger.json').write_bytes(raw(ledger))
contract=read('contract.json');checks={'baseCases':332,'targetedCases':138,'edgeAndInstalledChecks':31,'helperIntegrityChecks':7,'apiOnlyChecks':2,'runnerOracleChecks':2,'portableInstalledCliCases':491,'mutationCorpusCases':493,'mutationSites':115,'directNegativeWitnessSites':112,'mutationsAcceptingInvalidInput':84,'mutationsChangingExpectedError':28,'redundantFailureBranches':3,'allExpected':True}
delivery=f'''# Canonical authorization evidence repair delivery

This packet addresses F1–F5 and P1/P2 from the current-head review of PR #56. The primary trust/PR boundary remains **canonical authorization decision evidence integrity**; scope stayed inside it. The original owner packet and author-side independent review are unchanged, as verified in `preserved-originals.json`.

The repair binds native source revisions, rejects conflicting versions of one logical source identity, checks every retained tuple and the selected path's ordering against retained PATH_ALLOW claims, loads the actual adjacent helper bytes, retains the missing PR11 output fields and exact extractor bytes, and selects the intent's native schema-version field through its profile. Selected sharing paths get an explicit out-of-profile error; retained sharing paths remain checked. `REPAIR_DESIGN.md` explains each source-backed decision and limitation.

Validation completed:

- 332 full conformance cases, 138 targeted specific-code cases and 31 edge/installation checks passed.
- Seven fresh-process helper-origin/identity probes and two API-only invalid-map checks passed.
- All 491 portable cases have matching actual split installed CLI executions, with exact error-code and applicable detail expectations: 490 from the initial full run and the oversized-wire case from a targeted replay after correcting its CLI-specific error expectation. Runtime and wire bytes did not change. Initial results and correction evidence are preserved. Two deliberately incorrect runner oracles were correctly rejected.
- The 493-case mutation baseline reaches all 115 must() sites. There are direct negative witnesses for 112: removing 84 accepts an invalid input; removing 28 changes the required error. The remaining three failure branches repeat earlier trace guards. They are explicitly classified rather than counted as kills.

These are author-side checks, not a formal two-reviewer gate. They establish conditional evidence integrity only. Eligibility, principal trust, candidate completeness, globally correct canonical selection, live owner origin, CP3 admission, runtime protection and effect permission remain unestablished. No extractor is executed. No runtime, foreign source law, CI activation, merge or publication was performed. Selected SharingGrant support and a real complete producer profile remain outside this narrow draft. Python {platform.python_version()} was tested; Python 3.11 was not.

The integration map keeps runtime code, package contracts, fixtures and verbatim semantic sources in separate existing lanes. New repair history uses a new history directory so the original delivery seal is preserved. `cases.json` is the portable exact-code index. API-only, helper-origin and mutation evidence are separately labelled. Temporary split installation copies were removed after verification; rebuild only in a separate review/install directory using the map.

Next: the coordinator performs a fresh review of these exact sealed bytes, integrates only the reviewed repair into #56 with [skip ci], and leaves consumer integration and all other trust boundaries separate.
'''
(H/'DELIVERY.md').write_text(delivery)
pkg='03_machine_contracts/drafts_non_default/authorization_decision_evidence/canonical_success_path/'
runner='04_implementation_and_conformance/conformance_runners/canonical_success_path/'
fixture='04_implementation_and_conformance/examples_and_fixtures/fixtures/canonical_success_path/'
evidence='package_meta/history/clean_baseline_migration/phase_reports/canonical_success_path_review_repair_01/'
def target_path(name):
 if name in ['verify_success_path.py','path_common.py','run_cases.py']:return runner+name
 if name.startswith('sources/'):return fixture+name
 if name.startswith('schemas/') or name in ['contract.json','source-pins.json','README.md','DESIGN.md','SOURCE_INTERFACE.md','REGISTRATION.md']:return pkg+name
 if name.startswith('checks/'):return fixture+'cases/'+name[len('checks/'):]
 if name.startswith('targeted-checks/'):return fixture+'targeted-cases/'+name[len('targeted-checks/'):]
 if name.startswith('edge-checks/'):return fixture+'edge-cases/'+name[len('edge-checks/'):]
 if name.startswith('fixtures/'):return fixture+'examples/'+name[len('fixtures/'):]
 if name=='cases.json':return fixture+name
 return evidence+name
mapping=[]
for f in sorted(H.rglob('*')):
 if not f.is_file() or f.name in ['integration-map.json','DELIVERY_MANIFEST.json']:continue
 name=str(f.relative_to(H));b=f.read_bytes();mapping.append({'source':name,'destination':target_path(name),'sha256':sha(b),'bytes':len(b)})
assert len({x['destination'] for x in mapping})==len(mapping)
mapvalue={'status':'EXACT_PROPOSED_REPAIR_INTEGRATION_MAP','primaryTrustBoundary':'Canonical authorization decision evidence integrity','scopeStayedInsideBoundary':True,'packageRoot':pkg.rstrip('/'),'checkerRoot':runner.rstrip('/'),'sourceRoot':fixture.rstrip('/'),'selfDestination':evidence+'integration-map.json','manifestDestination':evidence+'DELIVERY_MANIFEST.json','mappings':mapping,'previousCandidateSeal':ledger['previousSeal'],'next':'Fresh author-side independent review, then coordinator integrates only these bytes into PR #56; no default CI activation.'}
(H/'integration-map.json').write_bytes(raw(mapvalue))
files=[]
for f in sorted(H.rglob('*')):
 if f.is_file() and f.name!='DELIVERY_MANIFEST.json':
  b=f.read_bytes();files.append({'path':str(f.relative_to(H)),'sha256':sha(b),'bytes':len(b)})
manifest={'status':'SEALED_REPAIR_FOR_FRESH_REVIEW','primaryTrustBoundary':'Canonical authorization decision evidence integrity','scopeStayedInsideBoundary':True,'previousCandidateSeal':ledger['previousSeal'],'contractRawSha256':sha((H/'contract.json').read_bytes()),'contractDigest':contract['contractDigest'],'integrationMapSha256':sha((H/'integration-map.json').read_bytes()),'checks':checks,'files':files,'next':'Fresh review of exact sealed bytes; coordinator owns integration/publication with CI inactive.'}
(H/'DELIVERY_MANIFEST.json').write_bytes(raw(manifest));print(json.dumps({'sealSha256':sha((H/'DELIVERY_MANIFEST.json').read_bytes()),'contractSha256':manifest['contractRawSha256'],'contractDigest':contract['contractDigest'],'integrationMapSha256':manifest['integrationMapSha256'],'sealedFiles':len(files),'mappedFiles':len(mapping),'checks':checks},indent=2))
