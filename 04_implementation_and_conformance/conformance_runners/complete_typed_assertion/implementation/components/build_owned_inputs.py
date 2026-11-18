"""Build finite reviewed-form scaffolding and an exact 99-definition construction map.
This owns claim-language typing, not foreign evidence schemas or admission.
"""
import argparse,copy,hashlib,json,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent
HEAD='389a8f6b6bb2f43435c35f32df769e723d736856'
PACKET='package_meta/history/clean_baseline_migration/phase_reports/domain_contract_verifier_delivery_v0_1'
BASE_PATH='03_machine_contracts/drafts_non_default/assertion_record_submission/OFARM_AssertionRecord_schema_v0_2.json'
BASE_ID='https://ofarm.dev/schema/assertionrecord/v0.2'
SCHEMA_ID='https://ofarm.dev/schema/drafts/non-default/assertion-domain/finite-reviewed-forms/v0.1'
DEFINITION_PREFIX='candidate:assertion-domain-construction:2026-10-21:'

def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def converted(x):
    if isinstance(x,dict):
        if set(x)=={'fixtureLogicalRef','fixtureRevision','admittedRuntimeBinding'}:
            if x['admittedRuntimeBinding'] is not False:raise ValueError('Unexpected source admission claim')
            return {'ref':x['fixtureLogicalRef'],'revisionRef':x['fixtureRevision']}
        result={k:converted(v) for k,v in x.items()}
        if result.get('form')=='ATOM':result['definition']=DEFINITION_PREFIX+x['definition'].split('#')[-1]
        return result
    if isinstance(x,list):return [converted(v) for v in x]
    return x

def atoms(x,path=''):
    if isinstance(x,dict):
        if x.get('form')=='ATOM':yield path,x
        for k,v in x.items():yield from atoms(v,path+'/'+k)
    elif isinstance(x,list):
        for i,v in enumerate(x):yield from atoms(v,path+'/'+str(i))

def obj(properties,required=None):return {'type':'object','additionalProperties':False,'properties':properties,'required':list(properties) if required is None else required}
def union(parts):
    unique={json.dumps(x,sort_keys=True):x for x in parts}
    values=list(unique.values());return values[0] if len(values)==1 else {'anyOf':values}

def shape(values,path=''):
    """Closed shape union from pinned reviewed forms; no object fallback.
    Values remain variable. Row discriminators and semantic rules are added below.
    Empty arrays use a declared element type, never an unconstrained object.
    """
    if all(isinstance(v,dict) and set(v) in [{'ref','revisionRef'},{'ref','digest'}] for v in values):return {'$ref':BASE_ID+'#/$defs/immutableBinding'}
    groups={}
    for v in values:
        kind='null' if v is None else 'boolean' if type(v)is bool else 'integer' if type(v)is int else 'number' if type(v)is float else 'string' if isinstance(v,str) else 'array' if isinstance(v,list) else 'object'
        groups.setdefault(kind,[]).append(v)
    result=[]
    for kind,vs in groups.items():
        if kind=='object':
            # Different member sets are explicit closed alternatives, not optional open bags.
            variants={}
            for v in vs:variants.setdefault(tuple(sorted(v)),[]).append(v)
            for keys,records in variants.items():result.append(obj({k:shape([v[k] for v in records],path+'/'+k) for k in keys}))
        elif kind=='array':
            elements=[x for v in vs for x in v]
            if elements:items=shape(elements,path+'/*')
            elif path.endswith('/quantityParameters'):items={'$ref':'#/$defs/quantityParameter'}
            elif path.endswith(('/predecessors','/evidenceBindings','/resources','/sourceBindings')):items={'$ref':BASE_ID+'#/$defs/immutableBinding'}
            else:items={'type':'string','minLength':1}
            result.append({'type':'array','items':items})
        elif kind=='string':
            s={'type':'string'}
            if path.endswith('/decimal'):s['pattern']=r'^-?(0|[1-9][0-9]*)(\.[0-9]+)?$'
            result.append(s)
        else:result.append({'type':kind})
    return union(result)

def object_nodes(s):
    if s.get('type')=='object':yield s
    for branch in s.get('anyOf',[]):yield from object_nodes(branch)

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo-root',type=Path,required=True);a=p.parse_args();repo=a.repo_root.resolve();inputpins={}
    def read(path):
        raw=(repo/path).read_bytes();expected=subprocess.check_output(['git','show',HEAD+':'+path],cwd=repo)
        if raw!=expected:raise ValueError('Source differs from exact reviewed head: '+path)
        inputpins[path]={'path':path,'commit':HEAD,'sha256':sha(raw)}
        return json.loads(raw)
    def rd(path):return read(PACKET+'/'+path)
    inventory=rd('reviewed-input/domain/inventory.json');canonical=rd('reviewed-input/canonical/inventory.json');requirements=rd('reviewed-input/domain/requirements.json');quantity=rd('reviewed-input/domain/quantity-contract.json');profiles=rd('reviewed-input/domain/operation-profile-contract.json');atom_contract=rd('reviewed-input/domain/atom-contract.json');work=rd('reviewed-input/domain/work-condition-definitions.json');occurrences=rd('reviewed-input/domain/occurrence-definitions.json');bundle=rd('review-amendment-03/candidate-examples-v4.json');roles=rd('review-amendment-02/compliance-role-cases-v3.json');base=read(BASE_PATH)
    evidence_roles=rd('review-amendment-03/evidence-selectors-v4.json');measured_roles=rd('review-amendment-03/measurement-role-contract-v4.json');event_cases=rd('review-amendment-02/event-compatibility-package-v3.json')
    samples={r['id']:[{'source':'reviewed-input/domain/inventory.json','pointer':'/rows/'+str(i)+'/typedRepresentation','atom':converted(r['typedRepresentation'])}] for i,r in enumerate(inventory['rows'])}
    # Explicitly supersede the old incomplete C04 form with the reviewed v4 source form.
    samples['C04']=[]
    whole_trace=[]
    for i,e in enumerate(bundle['examples']):
        extracted=[]
        for path,at in atoms(e['claimContent']):
            row=at['definition'].split('#')[-1]
            if row not in samples:raise ValueError(('unknown example row',row))
            item={'source':'review-amendment-03/candidate-examples-v4.json','pointer':'/examples/'+str(i)+'/claimContent'+path,'atom':converted(at),'wholeExampleId':e['id']};samples[row].append(item);extracted.append(row)
        whole_trace.append({'id':e['id'],'sourceIndex':i,'rows':extracted,'originalContentDigest':e['claimContentDigest'],'originalTextDigest':e['renderedTextSha256'],'sourceBytesUnchanged':True})
    rolecases={r['id']:r for r in roles['cases']}
    for row,rolecase in [('C03','C03_ROLE_COMPLETE'),('C06','C06_ROLE_COMPLETE')]:
        for item in samples[row]:item['atom']['body']=converted(rolecases[rolecase]['body'])
    for row,rolecase in [('C03','C03_REQUIRED_QUALIFICATION_COMPLETE'),('C09','C09_ROLE_COMPLETE')]:
        item=copy.deepcopy(samples[row][0]);item['atom']['body']=converted(rolecases[rolecase]['body']);item['source']='review-amendment-02/compliance-role-cases-v3.json';item['pointer']='/cases/'+str(roles['cases'].index(rolecases[rolecase]))+'/body';samples[row].append(item)
    # Explicit C06 source variants from the reviewed role contract.
    item=copy.deepcopy(samples['C06'][0]);ms=converted(rolecases['C03_ROLE_COMPLETE']['body']['measurementSource']);item['atom']['body']['rateSource']={'sourceKind':'MEASUREMENT_EVIDENCE','sourceBinding':ms['measurementBinding'],'valuePointer':ms['resultPointer'],'measurementSource':ms};samples['C06'].append(item)
    item=copy.deepcopy(samples['C06'][0]);item['atom']['body']['rateSource']['sourceKind']='OPERATION_PARAMETER';samples['C06'].append(item)
    # Explicit shared contracts are authored independently of example inference.
    value_id='https://ofarm.dev/schema/drafts/non-default/assertion-domain/owned-value-types/v0.1'
    defs={'quantityParameter':{'$ref':value_id+'#/$defs/quantityParameter'}}
    schemas={};positives=[];mapping=[]
    prerequisite_keys=['OWNER_IDENTITY_RELATION','OWNER_MEASUREMENT_USE','OWNER_PROTECTED_STATE']
    for i,row in enumerate(inventory['rows']):
        key=row['id'];variants=samples[key];body=shape([s['atom']['body'] for s in variants],'/body')
        for node in object_nodes(body):
            for field,value in row['atomContract']['bodyDiscriminators'].items():node['properties'][field]={'const':value}
            if key.startswith('O'):
                node['properties']['quantityParameters']={'type':'array','items':{'$ref':'#/$defs/quantityParameter'}}
                node['properties']['claimPosture']={'enum':['INTENDED','PERFORMED']}
                node['properties']['performanceFacet']={'enum':['OCCURRENCE','STARTED','IN_PROGRESS','COMPLETED']}
                for params in object_nodes(node['properties']['parameters']):
                    for field,value in row['parameterContract'].get('discriminators',{}).items():params['properties'][field]={'const':value}
                    if key=='O22':params['properties']['producedResult']={'$ref':value_id+'#/$defs/analysisOutput'}
            if key=='C09':node['properties']['evidencePosture']={'enum':['MEASURED'] if 'measurementSource' in node['properties'] else ['MODELLED','ESTIMATED','DISPUTED']}
        subject=obj({'kind':{'enum':row['subjectKinds']},'binding':{'$ref':BASE_ID+'#/$defs/immutableBinding'}})
        extent=obj({'posture':{'enum':['FULL_TARGET_SCOPE','PARTIAL_TARGET_SCOPE']},'binding':{'$ref':BASE_ID+'#/$defs/immutableBinding'}})
        time={'oneOf':[{'$ref':BASE_ID+'#/$defs/'+k} for k in row['subjectTimeProfiles']]}
        atom=obj({'form':{'const':'ATOM'},'atomId':{'type':'string','minLength':1},'definition':{'const':DEFINITION_PREFIX+key},'scope':obj({'subject':subject,'subjectTime':time,'extent':extent}),'body':body})
        defs[key]=atom;schemas[key]={'$ref':'#/$defs/'+key}
        for j,item in enumerate(variants):positives.append({'id':key+'_SHAPE_'+str(j+1),'row':key,'source':item['source'],'pointer':item['pointer'],'input':item['atom'],'expectedShape':'VALID','expectationAuthority':'Reviewed source form plus explicit amendment role requirements; authored before evaluator execution.','foreignAdmission':'NOT_ESTABLISHED'})
        needs=['OWNER_IDENTITY_RELATION']
        if key.startswith('O') or key in ['C01','C03','C04','C06','C09','C10']:needs+=['OWNER_MEASUREMENT_USE']
        mapping.append({'id':key,'group':row['inventory'],'kind':'CLAIM_ATOM','definition':DEFINITION_PREFIX+key,'scaffoldSchemaPointer':'#/$defs/'+key,'source':{'path':PACKET+'/reviewed-input/domain/inventory.json','pointer':'/rows/'+str(i),'sourceDefinition':row['conceptRevision']},'requiredFields':row['atomContract'],'parameterContract':row.get('parameterContract'),'domainPredicates':[{'id':key+'.meaning.'+str(j+1),'specification':v,'status':'SOURCE_SPECIFICATION_REQUIRES_ROW_IMPLEMENTATION_OR_EXACT_OWNER_INPUT'} for j,v in enumerate(row['evidencePredicates'])],'independentPositive':row['qualifiedPositive'],'independentHostile':row['contradiction'],'requirements':row.get('requirementIds',[]),'exactOwnerPrerequisites':needs,'sourceBindings':row['sources'],'executionScope':'CLOSED_REVIEWED_ATOM_SHAPES_AND_NAMED_INTRINSIC_CHECKS_ONLY; no complete row-semantic or owner-admission PASS'})
    for i,row in enumerate(canonical['rows']):
        group=row['group'];needs=['OWNER_EVENT_CLASSIFICATION','OWNER_IDENTITY_RELATION'] if group=='V04' else ['OWNER_MEASUREMENT_USE','OWNER_IDENTITY_RELATION'] if group=='V05' else ['OWNER_IDENTITY_RELATION']
        mapping.append({'id':row['id'],'group':group,'kind':{'V04':'EVENT_COMPATIBILITY_DEFINITION','V05':'MEASUREMENT_INTERPRETATION','V06':'RELATIONSHIP_DEFINITION'}[group],'source':{'path':PACKET+'/reviewed-input/canonical/inventory.json','pointer':'/rows/'+str(i)},'definition':row['revision']+'#'+row['id'],'typedConstructionSpecification':row['typedRepresentation'],'domainPredicates':[{'id':row['id']+'.meaning.'+str(j+1),'specification':v,'status':'SOURCE_SPECIFICATION_REQUIRES_ROW_IMPLEMENTATION_OR_EXACT_OWNER_INPUT'} for j,v in enumerate(row['predicates'])],'independentPositive':row['positiveExample'],'independentHostile':row['nearMissExample'],'requirements':row.get('requirementChecks',[]),'exactOwnerPrerequisites':needs,'sourceBindings':row['sourceBindings'],'executionScope':'NAMED_PURE_EVENT_TIME_RESULT_COMPARISONS_WHERE_LISTED; remaining owner-dependent predicates are specifications, not unavailable verifier branches'})
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':SCHEMA_ID,'title':'Finite reviewed-form AssertionRecord scaffolding v0.1','$comment':'Finite example-derived scaffolding only; not complete row contracts. Valid unexemplified optional forms may not fit; primitive strings do not establish allowed semantic enums. References use the exact existing immutableBinding schema. Source example fixture markers are removed by an explicit traced spelling conversion; this does not establish immutable resolution or admission. Foreign source records retain their actual schemas. Complete explicit row contracts remain owned construction work.','oneOf':list(schemas.values()),'$defs':defs}
    reqmap=[]
    for r in requirements['requirements']:
        ids=list(dict.fromkeys(r['mappedCandidateRows']+r.get('canonicalContributionRows',[])));assert all(any(m['id']==n for m in mapping) for n in ids)
        reqmap.append({**r,'constructionDefinitionIds':ids,'executionStatus':'ACCOUNTED_FOR; exact executable subchecks and remaining specifications are listed in execution-map.json'})
    put('finite-reviewed-forms.schema.json',schema);put('finite-form-positives.json',{'status':'UNADOPTED_SOURCE_GROUNDED_CONSTRUCTION_FIXTURES','cases':positives})
    put('definition-construction-map.json',{'status':'OWNED_COMPONENT_CONSTRUCTION_INPUTS_NOT_COMPLETE_VERIFIER','sourceHead':HEAD,'definitions':mapping,'counts':{'definitions':len(mapping),'finiteReviewedFormSchemas':len(schemas),'eventDefinitions':12,'measurementDefinitions':17,'relationshipDefinitions':12},'next':'Use exact executable subchecks and close the explicitly retained owner-interface and semantic construction requirements.'})
    put('requirement-construction-map.json',{'sourceHead':HEAD,'requirements':reqmap,'count':len(reqmap),'next':'Keep all 42 requirements in the complete verifier acceptance denominator.'})
    put('whole-meaning-source-map.json',{'sourceHead':HEAD,'count':len(whole_trace),'examples':whole_trace,'conversion':{'fixtureBinding':'Exact {fixtureLogicalRef,fixtureRevision,admittedRuntimeBinding:false} becomes the existing immutable selector {ref,revisionRef}. The old bytes remain source evidence; no admission is inferred.','definition':'Explicit new candidate construction identity per atom; no historical rewrite.'},'next':'Preserve every complete original meaning when integrating new caller schemas and projection.'})
    put('owned-contract-inputs.json',{'sourceHead':HEAD,'quantity':quantity,'operationProfiles':profiles,'atomAlgebra':atom_contract,'workConditions':work,'occurrenceDefinitions':occurrences,'typedEvidenceRoles':evidence_roles,'measurementRoles':measured_roles,'eventCases':event_cases,'timeProfiles':inventory['currentProposedTimeProfiles'],'preservedInvariants':inventory['preservedInvariants'],'next':'Consume named source-defined rules without inventing admission or omitted profile semantics.'})
    old=json.loads((O/'source-pins.json').read_text());merged={s['path']:s for s in old['sources']};merged.update(inputpins);old['sources']=list(merged.values());old['next']='Verify this exact source closure before construction checks.';put('source-pins.json',old)
    print(json.dumps({'definitions':len(mapping),'requirements':len(reqmap),'finiteReviewedFormSchemas':len(schemas),'shapeFixtures':len(positives),'wholeExamples':len(whole_trace),'sourcePins':len(merged)}))
if __name__=='__main__':main()
