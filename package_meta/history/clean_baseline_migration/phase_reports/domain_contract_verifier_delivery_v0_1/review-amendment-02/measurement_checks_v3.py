"""Finite fictional checks for the declared W05 fixture and required role examples.
This is not a public domain verifier, evidence resolver or admission mechanism.
"""
from decimal import Decimal
import hashlib
import rfc8785

def digest(x): return 'sha256:'+hashlib.sha256(rfc8785.dumps(x)).hexdigest()
def pointer(x,p):
    if not isinstance(p,str) or not p.startswith('/'):raise ValueError('absolute pointer required')
    for k in p.split('/')[1:]:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x

def required_role_errors(row,body,required_qualification=False):
    """Independent branch obligations, not a scan of the selector/citation table."""
    errors=[]
    def need(p):
        try:v=pointer(body,p)
        except (KeyError,IndexError,TypeError,ValueError):errors.append('MISSING_REQUIRED_ROLE:'+p);return None
        if v is None or v=='' or v==[] or v=={}:errors.append('INCOMPLETE_REQUIRED_ROLE:'+p)
        return v
    def measured(base):
        s=need(base)
        if not isinstance(s,dict):return
        for k in ['role','measurementBinding','resultPointer','contextBinding','subjectRelationBinding','methodUseBinding','qualificationPointers']:need(base+'/'+k)
        if s.get('role')!='MEASURED_COMPLIANCE_OPERAND':errors.append('SOURCE_ROLE_MISMATCH')
        for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']:
            if k in s:
                b=s[k]
                if not isinstance(b,dict) or set(b)!={'fixtureLogicalRef','fixtureRevision','admittedRuntimeBinding'} or not isinstance(b.get('fixtureLogicalRef'),str) or not b.get('fixtureLogicalRef') or not isinstance(b.get('fixtureRevision'),str) or not b.get('fixtureRevision') or b.get('admittedRuntimeBinding') is not False:errors.append('INVALID_FIXTURE_BINDING:'+base+'/'+k)
        if 'resultPointer' in s and (not isinstance(s['resultPointer'],str) or not s['resultPointer'].startswith('/')):errors.append('INVALID_RESULT_POINTER')
        if 'qualificationPointers' in s and (not isinstance(s['qualificationPointers'],list) or any(not isinstance(p,str) or not p.startswith('/') for p in s['qualificationPointers'])):errors.append('INVALID_QUALIFICATION_POINTERS')
    if row=='C03':
        for p in ['/criterion','/measurement','/operandPointer']:need(p)
        measured('/measurementSource')
        s=body.get('measurementSource',{})
        if 'measurement' in body and 'measurementBinding' in s and body['measurement']!=s['measurementBinding']:errors.append('MEASUREMENT_ALIAS_MISMATCH')
        if 'operandPointer' in body and 'resultPointer' in s and body['operandPointer']!=s['resultPointer']:errors.append('POINTER_ALIAS_MISMATCH')
    elif row=='C04':
        need('/criterion');measured('/operand/source')
        need('/operand/resultKind');need('/operand/admissibleValues')
        op=body.get('operand',{})
        if op.get('resultKind')=='CENSORED_NUMERIC':
            for p in ['/operand/qualifier','/operand/limit','/operand/nonnegative']:need(p)
    elif row=='C06':
        s=need('/rateSource')
        if isinstance(s,dict):
            for p in ['/rateSource/sourceKind','/rateSource/sourceBinding','/rateSource/valuePointer']:need(p)
            if s.get('sourceKind')=='MEASUREMENT_EVIDENCE':
                measured('/rateSource/measurementSource');ms=s.get('measurementSource',{})
                if s.get('sourceBinding')!=ms.get('measurementBinding'):errors.append('MEASUREMENT_ALIAS_MISMATCH')
                if s.get('valuePointer')!=ms.get('resultPointer'):errors.append('POINTER_ALIAS_MISMATCH')
            elif s.get('sourceKind') not in ['HUMAN_REPORT','OPERATION_PARAMETER']:errors.append('UNKNOWN_RATE_SOURCE_KIND')
    elif row=='C09':
        need('/evidencePosture');need('/claimBasis')
        if body.get('evidencePosture')=='MEASURED':measured('/measurementSource')
        elif body.get('evidencePosture') not in ['MODELLED','ESTIMATED','DISPUTED']:errors.append('UNKNOWN_METRIC_POSTURE')
    if required_qualification:
        # Selected criterion/profile, not the claimant's optional field presence, requires this.
        q=need('/measuredQualification')
        if isinstance(q,dict):
            for p in ['/measuredQualification/sourceBinding','/measuredQualification/sourcePointer','/measuredQualification/methodUseBinding','/measuredQualification/interpretation']:need(p)
    return errors

def w05_errors(content,records,expect):
    """Only the pinned W05 hypothetical owner expectations are evaluated here."""
    b=content['proposition']['body'];errors=required_role_errors('C04',b)
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
    try:
        loq_ok=dl==expect['limit'] and method.get('limit')==expect['limit'] and Decimal(lim['decimal'])==Decimal(str(dl['value'])) and lim['quantityKind']==r.get('quantityKindRef')==dl['quantityKindRef'] and lim['unit']==r.get('unitRef')==dl['unitRef'] and lim['originalLexicalValue']=='2'
    except (KeyError,TypeError,ValueError):loq_ok=False
    bad('LOQ_VALUE_UNIT_MISMATCH',loq_ok)
    bad('LEXICAL_RESULT_MISMATCH',r.get('originalLexicalValue')==expect['originalResultLexicalValue'] and r.get('originalUnitText')==expect['originalUnitText'])
    bad('QUALIFICATION_SOURCE_MISMATCH',s['qualificationPointers']==expect['qualificationPointers'] and m.get('uncertainty')==expect['uncertainty'] and c.get('uncertainty')==expect['uncertainty'])
    for p in s['qualificationPointers']:
        try:pointer(m,p)
        except (KeyError,IndexError,TypeError,ValueError):bad('QUALIFICATION_POINTER_UNRESOLVED',False)
    bad('METHOD_DOMAIN_BOUNDS_MISMATCH',method.get('domainLowerBound')==expect['admissibleValues']['lower'] and method.get('censoringUpperBound')=='EXCLUSIVE_LOQ' and method.get('statisticalConfidenceIsHardBound') is False and method.get('criterionBinding')==expect['criterionBinding'] and method.get('declaredUse')==expect['declaredUse'] and op.get('nonnegative') is True and op['admissibleValues']==expect['admissibleValues'])
    bad('THRESHOLD_RULE_MISMATCH',b['operator']==expect['operator'] and b['threshold']==expect['threshold'])
    # [0,2) against <=1 contains both satisfying and failing values; confidence is not a hard bound.
    bad('OUTCOME_MISMATCH',b['allegedOutcome']=='INDETERMINATE'==expect['allegedOutcome'])
    bad('SOURCE_POSTURE_MISMATCH',m.get('evidenceStatus')==expect['evidenceStatus'] and m.get('chainOfCustodyStatus')==expect['chainOfCustodyStatus'] and not m.get('degradationReasons'))
    return errors
