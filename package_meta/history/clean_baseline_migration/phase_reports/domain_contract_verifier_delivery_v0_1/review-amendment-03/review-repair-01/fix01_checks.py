"""Deterministic regressions for immutable source pins and owner-selected W05 shape."""
import copy,json,re
from measurement_checks_v4 import w05_errors,digest
from role_checks_v4 import required_role_errors
from w05_profile_checks_fix01 import PROFILE,record_errors

BAD=[('missing',None),('null',None),('empty_object',{}),('string','wrong'),('empty_string',''),('array',[{}]),('empty_array',[]),('number',7),('zero',0),('true',True),('false',False)]
DEFAULT=object()
KINDS=[('numeric','NUMERIC'),('unknown','UNKNOWN_KIND'),('missing',None),('null',None),('number',1),('false',False),('array',[]),('object',{})]

def replace(root,path,value,remove=False):
    tokens=path.strip('/').split('/');current=root
    for token in tokens[:-1]:current=current[token]
    if remove:current.pop(tokens[-1],None)
    else:current[tokens[-1]]=copy.deepcopy(value)

def run_fix01(out):
    rd=lambda n:json.loads((out/n).read_text())
    base=rd('candidate-examples-v4.json')['examples'][4]['claimContent'];records=rd('measurement-fixtures-v4.json')['records'];expect=rd('criterion-expectations-v4.json');checks=[]
    def check(name,ok,**details):checks.append({'check':'fix01: '+name,'passed':bool(ok),**details})
    def probe(name,c=DEFAULT,r=DEFAULT,e=DEFAULT,want=None,positive=False):
        try:
            errors=w05_errors(base if c is DEFAULT else c,records if r is DEFAULT else r,expect if e is DEFAULT else e)
            structured=isinstance(errors,list) and all(isinstance(x,dict) and isinstance(x.get('code'),str) and 'pointer' in x for x in errors)
            codes=[x['code'] for x in errors] if structured else []
            okay=errors==[] if positive else structured and bool(errors) and (want is None or want in codes)
            check(name,okay,errors=errors)
            return errors
        except Exception as exc:
            check(name,False,exception=type(exc).__name__+': '+str(exc));return None
    probe('unchanged r1 positive',positive=True)
    # Every wrong/unknown discriminator is crossed with every required scalar shape.
    for kind_tag,kind in KINDS:
        for path in ['/operand/limit','/threshold','/operand/limit/provenance','/threshold/provenance']:
            for tag,value in BAD:
                c=copy.deepcopy(base);body=c['proposition']['body'];replace(body,'/operand/resultKind',kind,kind_tag=='missing');replace(body,path,value,tag=='missing')
                probe(kind_tag+' with '+path+' '+tag,c=c)
        c=copy.deepcopy(base);replace(c['proposition']['body'],'/operand/resultKind',kind,kind_tag=='missing');probe('discriminator alone '+kind_tag,c=c)
    for path in ['/operand/limit','/threshold']:
        for field in ['quantityKind','unit','decimal','qualifier','originalLexicalValue','unitProfile']:
            c=copy.deepcopy(base);replace(c['proposition']['body'],path+'/'+field,None,True);probe('missing scalar member '+path+'/'+field,c=c)
    for path in ['/operand/limit/provenance','/threshold/provenance']:
        for field in ['sourceBinding','valuePointer','lexicalPointer','qualifierPointer']:
            c=copy.deepcopy(base);replace(c['proposition']['body'],path+'/'+field,None,True);c['proposition']['body']['operand']['resultKind']='NUMERIC';probe('kind cannot hide missing '+path+'/'+field,c=c)
    c=copy.deepcopy(base);b=c['proposition']['body'];b['operand']['resultKind']='NUMERIC';del b['operand']['limit']['provenance'];b['threshold']['provenance']=[];c['evidenceBindings']=[]
    errors=probe('combined discriminator both provenance roles and evidence removal',c=c)
    check('combined shape diagnostics identify both required provenance paths',errors is not None and any(x['pointer']=='/operand/limit/provenance' for x in errors) and any(x['pointer']=='/threshold/provenance' for x in errors))
    e=copy.deepcopy(expect);e['resultKind']='NUMERIC';probe('claim and expected discriminator cannot replace selected owner profile',c=c,e=e,want='OWNER_PROFILE_RESULT_KIND_MISMATCH')
    for field in ['quantityProvenanceDigest','criterionOwnerDigest']:
        e=copy.deepcopy(expect);e[field]='sha256:'+'0'*64;probe('wrong independent expected pin '+field,e=e)
    for mutation in ['lexical','transcriber','measurement_link','reporting_method','qualifier']:
        c=copy.deepcopy(base);r=copy.deepcopy(records);q=next(x for x in r if x['role']=='QUANTITY_PROVENANCE')
        if mutation=='lexical':q['record']['loq']['originalLexicalValue']='2.00';c['proposition']['body']['operand']['limit']['originalLexicalValue']='2.00'
        elif mutation=='transcriber':q['record']['reportedByPartyRef']='party:replacement'
        elif mutation=='measurement_link':q['record']['measurementSourceRef']='lab-report:replacement'
        elif mutation=='reporting_method':q['record']['reportingMethod']='MACHINE_IMPORT'
        elif mutation=='qualifier':q['record']['loq']['qualifier']='MACHINE_REPORTED';c['proposition']['body']['operand']['limit']['qualifier']='MACHINE_REPORTED'
        q['contentDigest']=digest(q['record']);probe('r1 rehash cannot authorize '+mutation,c,r,want='QUANTITY_OWNER_PIN_MISMATCH')
        e=copy.deepcopy(expect);e['quantityProvenanceDigest']=q['contentDigest'];probe('claim plus caller expectation cannot authorize r1 '+mutation,c,r,e,want='OWNER_PROFILE_QUANTITY_PIN_MISMATCH')
    # Exact independently authored r2 remains a valid source, never a rewrite of r1.
    approved=rd('owner-approved-lexical-r2-fix01.json')['quantityProvenance'];c=copy.deepcopy(base);r=copy.deepcopy(records);e=copy.deepcopy(expect);q=next(x for x in r if x['role']=='QUANTITY_PROVENANCE');old=copy.deepcopy(q['binding']);q.update(copy.deepcopy(approved));c['proposition']['body']['operand']['limit']['provenance']['sourceBinding']=copy.deepcopy(q['binding']);c['proposition']['body']['operand']['limit']['originalLexicalValue']='2.00';c['evidenceBindings']=[copy.deepcopy(q['binding']) if v==old else v for v in c['evidenceBindings']];e['quantityProvenanceBinding']=copy.deepcopy(q['binding']);e['quantityProvenanceDigest']=q['contentDigest']
    probe('approved exact r2 positive',c,r,e,positive=True)
    normalized=copy.deepcopy(c);normalized['proposition']['body']['operand']['limit']['originalLexicalValue']='2';probe('r2 normalization rejected',normalized,r,e,want='LOQ_SOURCE_LEXICAL_MISMATCH')
    altered=copy.deepcopy(r);aq=next(x for x in altered if x['role']=='QUANTITY_PROVENANCE');aq['record']['reportedByPartyRef']='party:replacement';aq['contentDigest']=digest(aq['record']);probe('r2 cannot change its approved bytes',c,altered,e,want='QUANTITY_OWNER_PIN_MISMATCH')
    unapproved=copy.deepcopy(e);unapproved['quantityProvenanceBinding']['fixtureRevision']='r3';probe('unapproved r3 has no owner pin',c,r,unapproved,want='UNAPPROVED_QUANTITY_SOURCE_REVISION')
    # Analogous criterion and measurement record rewrites have independent pins.
    for role in ['CRITERION_OWNER','MEASUREMENT','OBSERVATION_CONTEXT','SAMPLE_SUPPORT_RELATION','METHOD_USE_QUALIFICATION']:
        r=copy.deepcopy(records);record=next(x for x in r if x['role']==role);record['record']['fixtureNote']='changed bytes under same binding';record['contentDigest']=digest(record['record']);probe('same-binding record rewrite '+role,r=r,want='CRITERION_OWNER_PIN_MISMATCH' if role=='CRITERION_OWNER' else 'MEASUREMENT_SOURCE_PIN_MISMATCH')
    for role,field in [('QUANTITY_PROVENANCE','loq'),('CRITERION_OWNER','threshold'),('MEASUREMENT','source'),('MEASUREMENT','labContext'),('OBSERVATION_CONTEXT','spatialContext'),('OBSERVATION_CONTEXT','procedure'),('OBSERVATION_CONTEXT','measurementEvidenceRefs')]:
        for tag,value in BAD:
            r=copy.deepcopy(records);rec=next(x for x in r if x['role']==role);replace(rec['record'],'/'+field,value,tag=='missing');rec['contentDigest']=digest(rec['record']);probe('malformed resolved '+role+'/'+field+' '+tag,r=r)
    for role in ['QUANTITY_PROVENANCE','CRITERION_OWNER','MEASUREMENT']:
        for tag,value in BAD:
            r=copy.deepcopy(records);rec=next(x for x in r if x['role']==role)
            if tag=='missing':rec.pop('record')
            else:rec['record']=copy.deepcopy(value)
            probe('malformed record envelope '+role+' '+tag,r=r)
    for tag,value in BAD:
        if tag!='missing':probe('malformed resolver collection '+tag,r=value)
    # The repaired H03 is exactly resolved and pinned; only property meaning fails.
    h=rd('measurement-hostiles-v4.json')['cases'][0];he={**expect,**h['ownerProfileSelection']};hr=h['records'];hc=h['claimContent'];errs=probe('H03 independent valid source retains wrong-property rejection',hc,hr,he,want='PROPERTY_MISMATCH')
    check('H03 has exactly PROPERTY_MISMATCH',errs==[{'code':'PROPERTY_MISMATCH','pointer':None}],errors=errs)
    pin_errors,unsafe=record_errors(hc['proposition']['body'],hr,he,digest);check('H03 exact measurement source pin closure',not pin_errors and not unsafe,errors=pin_errors)
    hq=next(x for x in hr if x['role']=='QUANTITY_PROVENANCE');check('H03 exact approved transcription pin and distinct identity',hq['contentDigest']==he['quantityProvenanceDigest']==digest(hq['record']) and hq['binding']!=expect['quantityProvenanceBinding'])
    check('H03 keeps baseline criterion threshold and outcome',hc['proposition']['body']['threshold']==base['proposition']['body']['threshold'] and hc['proposition']['body']['allegedOutcome']==base['proposition']['body']['allegedOutcome'])
    for role in ['QUANTITY_PROVENANCE','CRITERION_OWNER']:
        rec=next(x for x in records if x['role']==role);field='loq' if role=='QUANTITY_PROVENANCE' else 'threshold';check('original HUMAN_REPORTED preserved '+role,rec['record'][field]['qualifier']=='HUMAN_REPORTED')
    return checks
