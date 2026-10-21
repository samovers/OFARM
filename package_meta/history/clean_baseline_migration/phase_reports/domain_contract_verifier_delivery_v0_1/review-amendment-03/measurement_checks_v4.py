"""V4 W05 checks with type-safe roles and independently resolved scalar sources."""
from decimal import Decimal,InvalidOperation
import hashlib
import rfc8785
from role_checks_v4 import pointer,required_role_errors,required_role_error_codes,error_codes
from provenance_checks_v4 import owner_error_codes,scalar_without_provenance,source_roles
def digest(x):return 'sha256:'+hashlib.sha256(rfc8785.dumps(x)).hexdigest()
def _semantic_error_codes(content,records,expect):
    """Only the pinned W05 hypothetical owner expectations are evaluated here."""
    b=content['proposition']['body'];errors=required_role_error_codes('C04',b)
    if errors:return errors
    s=b['operand']['source'];op=b['operand']
    def bad(code,condition):
        if not condition and code not in errors:errors.append(code)
    def resolve(k):
        binding=s[k]
        hits=[x for x in records if x['binding']==binding]
        if len(hits)!=1:raise ValueError('RESOLUTION_NOT_EXACT:'+k)
        rec=hits[0];bad('RESOLVED_DIGEST_MISMATCH',digest(rec['record'])==rec['contentDigest'])
        bad('MISSING_ASSERTION_EVIDENCE:'+k,binding in content['evidenceBindings'])
        return rec['record']
    try:
        m=resolve('measurementBinding');c=resolve('contextBinding');rel=resolve('subjectRelationBinding');method=resolve('methodUseBinding')
    except (KeyError,ValueError,TypeError) as ex:return errors+[str(ex)]
    bad('CRITERION_BINDING_MISMATCH',b['criterion']==expect['criterionBinding'] and expect['ruleBinding'] in content['ruleRevisionBindings'] and expect['evidencePolicyBinding'] in content['evidencePolicyRevisionBindings'])
    bad('CLAIM_SCOPE_MISMATCH',content['subject']==expect['subject'] and content['subjectTime']==expect['subjectTime'] and content['proposition']['scope']=={'subject':expect['subject'],'subjectTime':expect['subjectTime'],'extent':expect['extent']})
    bad('SOURCE_POINTER_MISMATCH',s['resultPointer']==expect['resultPointer'])
    try:r=pointer(m,s['resultPointer'])
    except (KeyError,IndexError,TypeError,ValueError):return errors+['SOURCE_POINTER_UNRESOLVED']
    if not isinstance(r,dict):return errors+['SOURCE_VALUE_SHAPE_MISMATCH']
    bad('MEASUREMENT_IDENTITY_MISMATCH',m.get('measurementEvidenceId')==s['measurementBinding']['fixtureLogicalRef'])
    bad('PROPERTY_MISMATCH',m.get('observedPropertyRef')==expect['observedPropertyRef'] and c.get('observedPropertyRef')==expect['observedPropertyRef'] and method.get('propertyRef')==expect['observedPropertyRef'])
    bad('SAMPLE_MISMATCH',m.get('sampleRef')==expect['sampleRef'] and c.get('subject')=={'subjectType':'SAMPLE','subjectRef':expect['sampleRef']} and rel.get('sampleRef')==expect['sampleRef'])
    bad('CONTEXT_LINK_MISMATCH',m.get('agronomicObservationContextRef')==c.get('agronomicObservationContextId')==s['contextBinding']['fixtureLogicalRef'] and rel.get('contextBinding')==s['contextBinding'] and m['measurementEvidenceId'] in c.get('measurementEvidenceRefs',[]))
    target={'scopeType':expect['subject']['kind'],'scopeRef':expect['subject']['binding']['fixtureLogicalRef']}
    spatial=c.get('spatialContext',{})
    bad('TARGET_SUPPORT_MISMATCH',c.get('targetScope')==target and spatial.get('scope')==target and spatial.get('spatialBasis')==expect['spatialBasis'] and spatial.get('partialExtentRef')==expect['supportExtentRef'] and spatial.get('geometryBasisRef')==expect['geometryBasisRef'] and rel.get('subject')==expect['subject'] and rel.get('subjectTime')==expect['subjectTime'] and rel.get('claimExtent')==expect['extent'] and rel.get('supportExtentRef')==expect['supportExtentRef'] and rel.get('geometryBasisRef')==expect['geometryBasisRef'] and rel.get('criterionBinding')==expect['criterionBinding'] and rel.get('declaredUse')==expect['declaredUse'])
    bad('PHENOMENON_TIME_MISMATCH',m.get('phenomenonTime')==expect['phenomenonTime'] and c.get('phenomenonTime')==expect['phenomenonTime'] and expect['phenomenonTime']['instant']<=expect['subjectTime']['at'])
    cp=c.get('procedure',{});lab=m.get('labContext',{})
    bad('METHOD_MISMATCH',m.get('measurementMethod')==expect['measurementMethod'] and m.get('samplingProtocol')==expect['samplingProtocol'] and cp.get('measurementMethodRef')==expect['measurementMethod']['procedureRef'] and cp.get('samplingProtocolRef')==expect['samplingProtocol']['procedureRef'] and lab.get('labMethodRef')==expect['measurementMethod']['procedureRef'] and method.get('method')==expect['measurementMethod'])
    bad('MATRIX_ANALYTE_MISMATCH',lab.get('matrixRef')==expect['matrixRef'] and lab.get('analyteRefs')==expect['analyteRefs'] and method.get('matrixRef')==expect['matrixRef'] and method.get('analyteRefs')==expect['analyteRefs'])
    bad('RESULT_KIND_QUALIFIER_MISMATCH',r.get('resultKind')==op.get('resultKind')==expect['resultKind'] and r.get('censoringQualifier')==op.get('qualifier')==expect['censoringQualifier'])
    lim=op['limit'];dl=r.get('detectionLimit',{})
    owner_errors,quantity_record,criterion_record=owner_error_codes(b,content,m,records,expect,digest)
    errors.extend(owner_errors)
    if criterion_record is None:return errors
    try:
        loq_ok=dl==expect['limit'] and method.get('limit')==expect['limit'] and Decimal(lim['decimal'])==Decimal(str(dl['value'])) and lim['quantityKind']==r.get('quantityKindRef')==dl['quantityKindRef'] and lim['unit']==r.get('unitRef')==dl['unitRef']
    except (KeyError,TypeError,ValueError,InvalidOperation):loq_ok=False
    bad('LOQ_VALUE_UNIT_MISMATCH',loq_ok)
    bad('LEXICAL_RESULT_MISMATCH',r.get('originalLexicalValue')==expect['originalResultLexicalValue'] and r.get('originalUnitText')==expect['originalUnitText'])
    bad('QUALIFICATION_SOURCE_MISMATCH',s['qualificationPointers']==expect['qualificationPointers'] and m.get('uncertainty')==expect['uncertainty'] and c.get('uncertainty')==expect['uncertainty'])
    for p in s['qualificationPointers']:
        try:pointer(m,p)
        except (KeyError,IndexError,TypeError,ValueError):bad('QUALIFICATION_POINTER_UNRESOLVED',False)
    bad('METHOD_DOMAIN_BOUNDS_MISMATCH',method.get('domainLowerBound')==expect['admissibleValues']['lower'] and method.get('censoringUpperBound')=='EXCLUSIVE_LOQ' and method.get('statisticalConfidenceIsHardBound') is False and method.get('criterionBinding')==expect['criterionBinding'] and method.get('declaredUse')==expect['declaredUse'] and op.get('nonnegative') is True and op['admissibleValues']==expect['admissibleValues'])
    bad('THRESHOLD_RULE_MISMATCH',b['operator']==criterion_record['operator'] and scalar_without_provenance(b['threshold'])==criterion_record['threshold'])
    # [0,2) against <=1 contains both satisfying and failing values; confidence is not a hard bound.
    bad('OUTCOME_MISMATCH',b['allegedOutcome']=='INDETERMINATE'==expect['allegedOutcome'])
    bad('SOURCE_POSTURE_MISMATCH',m.get('evidenceStatus')==expect['evidenceStatus'] and m.get('chainOfCustodyStatus')==expect['chainOfCustodyStatus'] and not m.get('degradationReasons'))
    return errors

def w05_errors(content,records,expect):
    try:
        body=content['proposition']['body']
    except (KeyError,TypeError):return [{'code':'INVALID_CLAIM_SHAPE','pointer':'/proposition/body'}]
    structural=required_role_errors('C04',body)
    if structural:return structural
    # Guard the scalar containers before the finite semantic comparisons.
    for key,path in [('limit','/operand/limit'),('threshold','/threshold')]:
        try:value=pointer(body,path)
        except (KeyError,TypeError,ValueError,IndexError):return [{'code':'MISSING_REQUIRED_ROLE','pointer':path}]
        if not isinstance(value,dict):return [{'code':'INVALID_TYPE','pointer':path,'expected':'object'}]
    result=[]
    for code in _semantic_error_codes(content,records,expect):
        if ':' in code and code.split(':',1)[1].startswith('/'):
            name,ptr=code.split(':',1);result.append({'code':name,'pointer':ptr})
        else:result.append({'code':code,'pointer':None})
    return result

def w05_error_codes(content,records,expect):return error_codes(w05_errors(content,records,expect))
