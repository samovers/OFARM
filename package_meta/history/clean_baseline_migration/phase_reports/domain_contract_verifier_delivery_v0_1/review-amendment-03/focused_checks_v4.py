"""Finite malformed-role and provenance regression probes; not a broad verifier."""
import copy,hashlib,json
from decimal import Decimal
import rfc8785
from role_checks_v4 import required_role_errors,valid_pointer
from measurement_checks_v4 import w05_errors

def digest(x):return 'sha256:'+hashlib.sha256(rfc8785.dumps(x)).hexdigest()
def replace(root,path,value,remove=False):
    keys=path.strip('/').split('/');target=root
    for k in keys[:-1]:target=target[int(k)] if isinstance(target,list) else target[k]
    k=keys[-1]
    if remove:
        if isinstance(target,list):target.pop(int(k))
        else:target.pop(k,None)
    elif isinstance(target,list):target[int(k)]=copy.deepcopy(value)
    else:target[k]=copy.deepcopy(value)
def codes(errors):return [e['code'] for e in errors]

def run_focused(out,prior,repo):
    checks=[]
    def check(name,passed,**details):checks.append({'check':name,'passed':bool(passed),**details})
    rd=lambda name:json.loads((out/name).read_text());old=lambda name:json.loads((prior/name).read_text())
    bundle=rd('candidate-examples-v4.json');before=old('candidate-examples-v3.json');c=bundle['examples'][4]['claimContent'];b=c['proposition']['body'];records=rd('measurement-fixtures-v4.json')['records'];expect=rd('criterion-expectations-v4.json');owners=rd('owner-records-v4.json')
    oldroles={x['id']:x for x in old('compliance-role-cases-v3.json')['cases']}
    c03=copy.deepcopy(oldroles['C03_ROLE_COMPLETE']['body']);c06=copy.deepcopy(oldroles['C06_ROLE_COMPLETE']['body']);c09=copy.deepcopy(oldroles['C09_ROLE_COMPLETE']['body']);qual=copy.deepcopy(oldroles['C03_REQUIRED_QUALIFICATION_COMPLETE']['body']);ms=copy.deepcopy(c03['measurementSource']);c06m=copy.deepcopy(c06);c06m['rateSource']={'sourceKind':'MEASUREMENT_EVIDENCE','sourceBinding':ms['measurementBinding'],'valuePointer':ms['resultPointer'],'measurementSource':ms}
    bases={'C03':('C03',c03,False),'C04':('C04',b,False),'C06_report':('C06',c06,False),'C06_measured':('C06',c06m,False),'C09':('C09',c09,False),'qualification':('C03',qual,True)}
    bad_values=[('string','source'),('list',[{}]),('number',7),('zero',0),('boolean_true',True),('boolean_false',False),('null',None),('empty_object',{}),('empty_list',[]),('empty_string',''),('missing',None)]
    containers=[('C03','/measurementSource'),('C04','/operand/source'),('C04','/operand'),('C06_report','/rateSource'),('C06_measured','/rateSource/measurementSource'),('C09','/measurementSource'),('qualification','/measuredQualification')]
    def assert_bad(label,row,body,required):
        try:
            errors=required_role_errors(row,body,required)
            structured=bool(errors) and all(isinstance(e,dict) and isinstance(e.get('code'),str) and isinstance(e.get('pointer'),str) for e in errors)
            check(label,structured,errors=errors)
        except Exception as e:check(label,False,exception=type(e).__name__+': '+str(e))
    for key,path in containers:
        row,body,req=bases[key]
        for tag,value in bad_values:
            x=copy.deepcopy(body);replace(x,path,value,tag=='missing');assert_bad(key+path+': reject '+tag,row,x,req)
        x=copy.deepcopy(body);parent=x
        for k in path.strip('/').split('/'):parent=parent[k]
        parent['unexpected']=True;assert_bad(key+path+': reject unknown member',row,x,req)
    for key,(row,body,req) in bases.items():
        for tag,value in bad_values[:-1]:assert_bad(key+': reject malformed body '+tag,row,value,req)
    binding_paths={
      'C03':['/criterion','/measurement']+['/measurementSource/'+k for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']],
      'C04':['/criterion']+['/operand/source/'+k for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']]+['/operand/limit/provenance/sourceBinding','/threshold/provenance/sourceBinding'],
      'C06_report':['/rateSource/sourceBinding'],
      'C06_measured':['/rateSource/sourceBinding']+['/rateSource/measurementSource/'+k for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']],
      'C09':['/claimBasis']+['/measurementSource/'+k for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']],
      'qualification':['/measuredQualification/sourceBinding','/measuredQualification/methodUseBinding']}
    goodbinding={'fixtureLogicalRef':'source:fictional','fixtureRevision':'r1','admittedRuntimeBinding':False}
    binding_mutations=[('extra_member',{**goodbinding,'extra':1}),('missing_revision',{k:v for k,v in goodbinding.items() if k!='fixtureRevision'}),('boolean_ref',{**goodbinding,'fixtureLogicalRef':True}),('number_revision',{**goodbinding,'fixtureRevision':1}),('empty_ref',{**goodbinding,'fixtureLogicalRef':''}),('blank_revision',{**goodbinding,'fixtureRevision':' '}),('true_admission',{**goodbinding,'admittedRuntimeBinding':True}),('numeric_false_admission',{**goodbinding,'admittedRuntimeBinding':0})]
    for key,paths in binding_paths.items():
        row,body,req=bases[key]
        for path in paths:
            for tag,value in bad_values+binding_mutations:
                x=copy.deepcopy(body);replace(x,path,value,tag=='missing');assert_bad(key+path+': binding '+tag,row,x,req)
    pointer_paths={
      'C03':['/operandPointer','/measurementSource/resultPointer','/measurementSource/qualificationPointers/0'],
      'C04':['/operand/source/resultPointer','/operand/source/qualificationPointers/0']+['/operand/limit/provenance/'+k for k in ['valuePointer','lexicalPointer','qualifierPointer']]+['/threshold/provenance/'+k for k in ['valuePointer','lexicalPointer','qualifierPointer']],
      'C06_report':['/rateSource/valuePointer'],
      'C06_measured':['/rateSource/valuePointer','/rateSource/measurementSource/resultPointer','/rateSource/measurementSource/qualificationPointers/0'],
      'C09':['/measurementSource/resultPointer','/measurementSource/qualificationPointers/0'],
      'qualification':['/measuredQualification/sourcePointer']}
    for key,paths in pointer_paths.items():
        row,body,req=bases[key]
        for path in paths:
            for tag,value in [('relative','result/value'),('invalid_escape','/x~2'),('bare_tilde','/x~'),('empty',''),('number',1),('boolean',False),('null',None),('array',[]),('object',{})]:
                x=copy.deepcopy(body);replace(x,path,value);assert_bad(key+path+': pointer '+tag,row,x,req)
    for key,path in [('C03','/measurementSource/qualificationPointers'),('C04','/operand/source/qualificationPointers'),('C06_measured','/rateSource/measurementSource/qualificationPointers'),('C09','/measurementSource/qualificationPointers')]:
        row,body,req=bases[key]
        for tag,value in bad_values:
            x=copy.deepcopy(body);replace(x,path,value,tag=='missing');assert_bad(key+path+': pointer list '+tag,row,x,req)
    check('RFC6901 escape syntax remains supported',valid_pointer('/a~0b/c~1d') and valid_pointer('/'))
    for key,(row,body,req) in bases.items():check(key+': complete source shape still accepted',required_role_errors(row,body,req)==[])
    # W05 public semantic entry rejects malformed source values without exceptions.
    for path in ['/operand/source','/operand/limit/provenance','/threshold/provenance']:
        for tag,value in bad_values:
            x=copy.deepcopy(c);replace(x['proposition']['body'],path,value,tag=='missing')
            try:errors=w05_errors(x,records,expect);check('W05 '+path+' '+tag,bool(errors) and all(isinstance(e,dict) for e in errors),errors=errors)
            except Exception as e:check('W05 '+path+' '+tag,False,exception=type(e).__name__+': '+str(e))
    check('W05 exact source-semantic positive',w05_errors(c,records,expect)==[])
    check('all 25 IDs and order preserved',[e['id'] for e in bundle['examples']]==[e['id'] for e in before['examples']])
    check('24 examples remain entirely byte-value identical',all(e==before['examples'][i] for i,e in enumerate(bundle['examples']) if i!=4))
    check('numeric limit threshold and conclusion retained',b['operand']['limit']['decimal']=='2' and b['threshold']['decimal']=='1' and b['operator']=='LE' and b['allegedOutcome']=='INDETERMINATE')
    for field in ['operand/limit','threshold']:
        for q in ['MACHINE_REPORTED','EXACT','LABEL_LIMIT','UNKNOWN','invented']:
            x=copy.deepcopy(c);replace(x['proposition']['body'],'/'+field+'/qualifier',q);errs=w05_errors(x,records,expect);check('wrong provenance rejected '+field+' '+q,bool(errs),errors=errs)
    # Select the separately authored and independently pinned r2 owner fixture.
    approved=rd('owner-approved-lexical-r2-fix01.json')['quantityProvenance']
    varied=copy.deepcopy(c);vr=copy.deepcopy(records);ve=copy.deepcopy(expect);q=next(r for r in vr if r['role']=='QUANTITY_PROVENANCE');oldbinding=copy.deepcopy(q['binding']);q.update(copy.deepcopy(approved));varied['proposition']['body']['operand']['limit']['provenance']['sourceBinding']=copy.deepcopy(q['binding']);varied['proposition']['body']['operand']['limit']['originalLexicalValue']=q['record']['loq']['originalLexicalValue'];varied['evidenceBindings']=[q['binding'] if v==oldbinding else v for v in varied['evidenceBindings']];ve['quantityProvenanceBinding']=copy.deepcopy(q['binding']);ve['quantityProvenanceDigest']=q['contentDigest']
    errs=w05_errors(varied,vr,ve);check('selected scalar lexical 2.00 positive under separate r2 owner source',errs==[],errors=errs)
    check('lexical variation preserves censored full result',next(r for r in vr if r['role']=='MEASUREMENT')['record']['result']['originalLexicalValue']=='< 2 mg/kg' and Decimal(varied['proposition']['body']['operand']['limit']['originalLexicalValue'])==Decimal('2'))
    normalized=copy.deepcopy(varied);normalized['proposition']['body']['operand']['limit']['originalLexicalValue']='2';errs=w05_errors(normalized,vr,ve);check('normalizing the selected 2.00 lexical to 2 fails','LOQ_SOURCE_LEXICAL_MISMATCH' in codes(errs),errors=errs)
    full=copy.deepcopy(c);full['proposition']['body']['operand']['limit']['originalLexicalValue']='< 2 mg/kg';errs=w05_errors(full,records,expect);check('full censored result lexical cannot substitute for scalar lexical','LOQ_SOURCE_LEXICAL_MISMATCH' in codes(errs),errors=errs)
    missing=copy.deepcopy(c);missing['evidenceBindings'].remove(expect['quantityProvenanceBinding']);errs=w05_errors(missing,records,expect);check('new quantity provenance must be exact ordinary evidence','MISSING_QUANTITY_PROVENANCE_EVIDENCE' in codes(errs),errors=errs)
    changed=copy.deepcopy(c);ce=copy.deepcopy(expect);changed['proposition']['body']['threshold']['decimal']='3';ce['threshold']['decimal']='3';errs=w05_errors(changed,records,ce);check('claim and expectation mirror cannot redefine independent threshold','THRESHOLD_RULE_MISMATCH' in codes(errs),errors=errs)
    cr=copy.deepcopy(records);crit=next(r for r in cr if r['role']=='CRITERION_OWNER');crit['record']['threshold']['decimal']='3';crit['contentDigest']=digest(crit['record']);errs=w05_errors(changed,cr,ce);check('rewriting criterion record under its old pin fails','CRITERION_OWNER_PIN_MISMATCH' in codes(errs),errors=errs)
    source=next(r for r in records if r['role']=='QUANTITY_PROVENANCE');criterion=next(r for r in records if r['role']=='CRITERION_OWNER')
    check('owner source records have exact digest closure',source['contentDigest']==digest(owners['quantityProvenance']['record']) and criterion['contentDigest']==digest(owners['criterionOwner']['record'])==expect['criterionOwnerDigest'])
    check('threshold authored independently in owner record',owners['criterionOwner']['record']['threshold']=={k:v for k,v in b['threshold'].items() if k!='provenance'} and owners['criterionOwner']['record']['authoringMethod']=='HUMAN_AUTHORED_FICTIONAL_CRITERION')
    for method in ['MACHINE_IMPORT_WITHOUT_OWNER_RULE','UNKNOWN',None]:
        rr=copy.deepcopy(records);qrecord=next(r for r in rr if r['role']=='QUANTITY_PROVENANCE');qrecord['record']['reportingMethod']=method;qrecord['contentDigest']=digest(qrecord['record']);errs=w05_errors(c,rr,expect)
        check('LAB_RESULT cannot replace missing or different scalar reporting role '+str(method),'QUANTITY_REPORTING_ROLE_MISMATCH' in codes(errs),errors=errs)
    from provenance_checks_v4 import QUANTITY_QUALIFIERS
    carrier=json.loads((repo/'03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json').read_text())
    canonical_enum=carrier['properties']['actualQuantityParameters']['items']['properties']['qualifier']['enum']
    check('quantity qualifier enum matches exact pinned source',QUANTITY_QUALIFIERS==set(canonical_enum))
    trace=rd('source-resolution-trace-v4.json')
    check('new ordinary quantity source has exact trace binding/digest/selector closure',trace['ordinaryEvidence'][0]['binding']==source['binding'] and trace['ordinaryEvidence'][0]['recordDigest']==source['contentDigest'] and trace['ordinaryEvidence'][0]['selectors']==b['operand']['limit']['provenance'])
    check('independent criterion has exact definition-source trace closure',trace['definitionSources'][0]['binding']==criterion['binding'] and trace['definitionSources'][0]['recordDigest']==criterion['contentDigest'] and trace['definitionSources'][0]['selectors']==b['threshold']['provenance'])
    return checks
