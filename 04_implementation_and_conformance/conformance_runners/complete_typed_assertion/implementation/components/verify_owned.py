"""Run the bounded owned component, not the complete public domain verifier."""
import argparse,collections,copy,hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from domain_owned import OwnedComponent,interval_outcome,composed_outcome,event_literal_errors
from build_owned_inputs import PACKET
HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo-root',type=Path,required=True)
    args=parser.parse_args();component=OwnedComponent(args.repo_root.resolve());checks=[]
    def record(name,category,okay,details=None):
        checks.append({'id':name,'category':category,'passed':bool(okay),**({'details':details} if not okay else {})})
    for name in ['finite-reviewed-forms.schema.json','owned-value-types.schema.json']:
        Draft202012Validator.check_schema(json.loads((HERE/name).read_text()))
        record('schema-meta/'+name,'schema-meta',True)
    document=json.loads((HERE/'independent-cases.json').read_text())
    methods={name:getattr(component,name) for name in ['value_errors','time_errors','quantity_errors','quantity_context_errors','analysis_output_errors','check_explicit_o22','measurement_result_errors','measured_instant_errors','event_time_errors','qualified_nl_errors']}
    methods.update({'interval_outcome':interval_outcome,'composed_outcome':composed_outcome,'event_literal_errors':event_literal_errors})
    seen=set()
    for case in document['cases']:
        if case['id'] in seen:raise ValueError('Duplicate case id: '+case['id'])
        seen.add(case['id'])
        result=methods[case['method']](*case['args'])
        errors=result if isinstance(result,list) else result['errors']
        expected=case['expected'];okay=(not errors)==expected['valid']
        if 'outcome' in expected:okay=okay and result.get('outcome',result.get('value'))==expected['outcome']
        record(case['id'],case['category'],okay,{'expected':expected,'actual':result})
    fixtures=json.loads((HERE/'finite-form-positives.json').read_text())['cases']
    for case in fixtures:
        result=component.check_reviewed_atom(case['row'],case['input'])
        record('finite/'+case['id'],'finite-reviewed-form',not result['errors'],result)
    # One wrong discriminator and one unknown body field per reviewed row.
    # These cover finite scaffolding rejection only, not semantic completeness.
    rows={c['row']:c for c in fixtures}
    for row,case in rows.items():
        mutated=copy.deepcopy(case['input']);mutated['body']['unknownMember']=True
        result=component.check_reviewed_atom(row,mutated)
        record('finite-extra/'+row,'finite-reviewed-form-hostile',bool(result['errors']),result)
        mutated=copy.deepcopy(case['input']);del mutated['scope']['subjectTime']
        result=component.check_reviewed_atom(row,mutated)
        record('finite-missing-time/'+row,'finite-reviewed-form-hostile',bool(result['errors']),result)
    definitions=json.loads((HERE/'definition-construction-map.json').read_text())['definitions']
    requirements=json.loads((HERE/'requirement-construction-map.json').read_text())['requirements']
    meanings=json.loads((HERE/'whole-meaning-source-map.json').read_text())['examples']
    record('coverage/99-distinct-definitions','source-accounting',len(definitions)==99 and len({d['id'] for d in definitions})==99)
    record('coverage/42-distinct-requirements','source-accounting',len(requirements)==42 and len({d['id'] for d in requirements})==42)
    record('coverage/25-whole-meanings','source-accounting',len(meanings)==25 and len({d['id'] for d in meanings})==25 and all(d['sourceBytesUnchanged'] for d in meanings))
    record('coverage/nine-profiles','source-accounting',len(component.contracts['timeProfiles'])==9)
    record('coverage/17-retained-event-profile-cells','source-accounting',sum(c['category']=='17-event-profile-cells' and c['expected']['valid'] for c in document['cases'])==17)
    record('coverage/30-result-time-cells','source-accounting',sum(c['category']=='five-results-by-six-time-roles' for c in document['cases'])==30)
    record('coverage/36-output-profile-facet-cells','source-accounting',sum(c['category']=='O22-profile-facet-output-matrix' for c in document['cases'])==36)
    original_domain=json.loads((args.repo_root/PACKET/'reviewed-input/domain/inventory.json').read_text())
    original_canonical=json.loads((args.repo_root/PACKET/'reviewed-input/canonical/inventory.json').read_text())
    expected_ids={r['id'] for r in original_domain['rows']+original_canonical['rows']}
    record('coverage/exact-source-definition-ids','source-accounting',{r['id'] for r in definitions}==expected_ids)
    obligations=json.loads((HERE/'obligation-retention-map.json').read_text())
    record('coverage/49-retained-duties','source-accounting',len(obligations['duties'])==49 and len({d['id'] for d in obligations['duties']})==49 and obligations['counts']=={'AR':29,'PC':20})
    execution=json.loads((HERE/'execution-map.json').read_text())
    record('coverage/execution-map-denominator','source-accounting',{r['id'] for r in execution['definitions']}==expected_ids and len(execution['requirements'])==42 and execution['counts']['completeSemanticRowEvaluators']==0)
    pins=json.loads((HERE/'source-pins.json').read_text())
    input_files=['independent-cases.json','finite-form-positives.json','owned-value-types.schema.json','finite-reviewed-forms.schema.json','owned-contract-inputs.json','execution-map.json','obligation-retention-map.json','domain_owned.py','build_value_types.py','build_owned_inputs.py','build_owned_cases.py','build_execution_map.py']
    report={'status':'BOUNDED_OWNED_COMPONENT_CHECKS_PASSED' if all(c['passed'] for c in checks) else 'CHECKS_FAILED',
        'primaryTrustBoundary':'AssertionRecord domain meaning and validation integrity','scopeStayedInsideBoundary':True,
        'completePublicVerifierEstablished':False,'completeDefinitionSemanticsEstablished':0,'admittedFactsEstablished':False,
        'sourceHead':pins['sourceHead'] if 'sourceHead' in pins else '389a8f6b6bb2f43435c35f32df769e723d736856',
        'pinnedRepositorySourcesChecked':len(pins['sources']),
        'counts':{'checks':len(checks),'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'independentlyAuthoredCases':len(document['cases']),'finiteReviewedForms':len(fixtures)},
        'categories':dict(collections.Counter(c['category'] for c in checks)),
        'testedInputHashes':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in input_files},
        'checks':checks,
        'next':'Integrate these bounded executable inputs without treating scaffolding or source-accounting counts as complete row semantics; continue the remaining owned rows and exact foreign interfaces.'}
    (HERE/'verification-results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'counts':report['counts'],'failures':[c for c in checks if not c['passed']]}))
    raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
if __name__=='__main__':main()
