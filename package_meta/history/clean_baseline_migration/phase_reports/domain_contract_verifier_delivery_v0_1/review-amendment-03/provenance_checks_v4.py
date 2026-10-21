"""Fictional W05 scalar-source comparisons; no admission or provenance inference."""
from decimal import Decimal,InvalidOperation
from role_checks_v4 import pointer,required_role_errors,error_codes

QUANTITY_QUALIFIERS={'EXACT','ESTIMATED','MINIMUM','MAXIMUM','RANGE_MIDPOINT','LABEL_LIMIT','MACHINE_REPORTED','HUMAN_REPORTED','UNKNOWN'}
def scalar_without_provenance(value):return {k:v for k,v in value.items() if k!='provenance'}
def source_roles(body):
    errors=[]
    for path in ['/operand/limit/provenance','/threshold/provenance']:
        try:pv=pointer(body,path)
        except (KeyError,ValueError,TypeError,IndexError):errors.append({'code':'MISSING_REQUIRED_ROLE','pointer':path});continue
        if not isinstance(pv,dict):continue # the common type checker reports this
    return errors

def resolve_exact(binding,records,digest):
    found=[r for r in records if isinstance(r,dict) and r.get('binding')==binding]
    if len(found)!=1:raise ValueError('SOURCE_RESOLUTION_NOT_EXACT')
    r=found[0]
    if r.get('contentDigest')!=digest(r.get('record')):raise ValueError('RESOLVED_DIGEST_MISMATCH')
    if not isinstance(r.get('record'),dict):raise ValueError('SOURCE_RECORD_NOT_OBJECT')
    return r['record']

def owner_error_codes(body,content,measurement,records,expect,digest):
    errors=[]
    def bad(code,ok):
        if not ok and code not in errors:errors.append(code)
    limit=body['operand']['limit'];threshold=body.get('threshold')
    if not isinstance(threshold,dict):return ['THRESHOLD_SOURCE_SHAPE_MISMATCH'],None,None
    lp=limit['provenance'];tp=threshold['provenance']
    try:q=resolve_exact(lp['sourceBinding'],records,digest);criterion=resolve_exact(tp['sourceBinding'],records,digest)
    except (ValueError,TypeError,KeyError) as e:return [str(e)],None,None
    bad('MISSING_QUANTITY_PROVENANCE_EVIDENCE',lp['sourceBinding'] in content['evidenceBindings'])
    bad('QUANTITY_SOURCE_BINDING_MISMATCH',lp['sourceBinding']==expect['quantityProvenanceBinding'])
    bad('CRITERION_SOURCE_BINDING_MISMATCH',tp['sourceBinding']==body['criterion']==expect['criterionOwnerBinding'])
    bad('CRITERION_OWNER_PIN_MISMATCH',digest(criterion)==expect['criterionOwnerDigest'])
    bad('QUANTITY_OWNER_PIN_MISMATCH',digest(q)==expect['quantityProvenanceDigest'])
    bad('QUANTITY_SOURCE_LINK_MISMATCH',q.get('measurementBinding')==body['operand']['source']['measurementBinding'] and q.get('measurementSourceRef')==measurement.get('source',{}).get('sourceRef') and q.get('selectedMeasurementPointer')=='/result/detectionLimit')
    bad('QUANTITY_SOURCE_POINTER_MISMATCH',lp['valuePointer']=='/loq' and lp['lexicalPointer']=='/loq/originalLexicalValue' and lp['qualifierPointer']=='/loq/qualifier')
    bad('CRITERION_SOURCE_POINTER_MISMATCH',tp['valuePointer']=='/threshold' and tp['lexicalPointer']=='/threshold/originalLexicalValue' and tp['qualifierPointer']=='/threshold/qualifier')
    try:
        qs=pointer(q,lp['valuePointer']);ql=pointer(q,lp['lexicalPointer']);qq=pointer(q,lp['qualifierPointer']);ts=pointer(criterion,tp['valuePointer']);tl=pointer(criterion,tp['lexicalPointer']);tq=pointer(criterion,tp['qualifierPointer'])
    except (KeyError,ValueError,TypeError,IndexError):return errors+['SCALAR_SOURCE_POINTER_UNRESOLVED'],q,criterion
    if not isinstance(qs,dict) or not isinstance(ts,dict) or not isinstance(ql,str) or not isinstance(tl,str):return errors+['SCALAR_SOURCE_VALUE_SHAPE_MISMATCH'],q,criterion
    bad('QUANTITY_REPORTING_ROLE_MISMATCH',q.get('fixtureRecordType')=='UNADOPTED_QUANTITY_SOURCE_EXAMPLE' and q.get('reportingMethod')=='HUMAN_TRANSCRIPTION_OF_LAB_REPORT' and isinstance(q.get('reportedByPartyRef'),str) and bool(q['reportedByPartyRef']) and qq=='HUMAN_REPORTED')
    bad('CRITERION_AUTHORING_ROLE_MISMATCH',criterion.get('fixtureRecordType')=='UNADOPTED_CRITERION_OWNER_EXAMPLE' and criterion.get('authoringMethod')=='HUMAN_AUTHORED_FICTIONAL_CRITERION' and isinstance(criterion.get('authoredByPartyRef'),str) and bool(criterion['authoredByPartyRef']) and tq=='HUMAN_REPORTED')
    bad('UNKNOWN_LOQ_QUANTITY_QUALIFIER',isinstance(limit.get('qualifier'),str) and limit['qualifier'] in QUANTITY_QUALIFIERS)
    bad('LOQ_PROVENANCE_QUALIFIER_MISMATCH',limit.get('qualifier')==qq and qq!='UNKNOWN')
    bad('UNKNOWN_THRESHOLD_QUANTITY_QUALIFIER',isinstance(threshold.get('qualifier'),str) and threshold['qualifier'] in QUANTITY_QUALIFIERS)
    bad('THRESHOLD_PROVENANCE_QUALIFIER_MISMATCH',threshold.get('qualifier')==tq and tq!='UNKNOWN')
    bad('LOQ_SOURCE_LEXICAL_MISMATCH',limit.get('originalLexicalValue')==ql)
    bad('THRESHOLD_SOURCE_LEXICAL_MISMATCH',threshold.get('originalLexicalValue')==tl)
    try:
        bad('LOQ_SOURCE_VALUE_MISMATCH',Decimal(str(qs['decimal']))==Decimal(str(measurement['result']['detectionLimit']['value']))==Decimal(str(limit['decimal'])) and qs['quantityKind']==limit['quantityKind'] and qs['unit']==limit['unit'] and qs['unitProfile']==limit['unitProfile'])
        bad('SCALAR_LEXICAL_NUMERIC_MISMATCH',Decimal(ql)==Decimal(str(qs['decimal'])) and Decimal(tl)==Decimal(str(ts['decimal'])))
    except (KeyError,TypeError,ValueError,InvalidOperation):bad('SCALAR_LEXICAL_NUMERIC_MISMATCH',False)
    bad('CRITERION_OWNER_CONTEXT_MISMATCH',criterion.get('ruleBinding')==expect['ruleBinding'] and criterion.get('evidencePolicyBinding')==expect['evidencePolicyBinding'] and criterion.get('observedPropertyRef')==expect['observedPropertyRef'])
    return errors,q,criterion
