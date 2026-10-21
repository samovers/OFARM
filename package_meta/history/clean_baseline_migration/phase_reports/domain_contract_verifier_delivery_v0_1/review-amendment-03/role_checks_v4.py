"""Bounded typed-role checks with structured errors; not a complete verifier."""
import re
MISSING=object()

def json_type(value):
    if value is MISSING:return 'missing'
    if value is None:return 'null'
    if type(value) is bool:return 'boolean'
    if type(value) in (int,float):return 'number'
    if isinstance(value,str):return 'string'
    if isinstance(value,list):return 'array'
    if isinstance(value,dict):return 'object'
    return type(value).__name__

def pointer(value,path):
    if not valid_pointer(path):raise ValueError('invalid absolute JSON pointer')
    for token in path.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        if isinstance(value,list):
            if not re.fullmatch(r'0|[1-9][0-9]*',token):raise ValueError('invalid array index')
            value=value[int(token)]
        elif isinstance(value,dict):value=value[token]
        else:raise TypeError('pointer container is not an object or array')
    return value

def valid_pointer(value):
    return isinstance(value,str) and value.startswith('/') and not re.search(r'~(?![01])',value)

def required_role_errors(row,body,required_qualification=False):
    errors=[]
    def err(code,path,**details):errors.append({'code':code,'pointer':path,**details})
    def get(path):
        try:return pointer(body,path)
        except (KeyError,IndexError,TypeError,ValueError):return MISSING
    def require(path,kind):
        value=get(path)
        if value is MISSING:err('MISSING_REQUIRED_ROLE',path);return MISSING
        if json_type(value)!=kind:err('INVALID_TYPE',path,expected=kind,actual=json_type(value));return MISSING
        if value=={} or value==[] or value=='':err('INCOMPLETE_REQUIRED_ROLE',path);return MISSING
        return value
    def obj(path,required,allowed=None):
        value=require(path,'object')
        if value is MISSING:return None
        if allowed is not None:
            unknown=sorted(set(value)-set(allowed))
            if unknown:err('UNKNOWN_MEMBERS',path,members=unknown)
        for k in required:
            if k not in value:err('MISSING_REQUIRED_ROLE',path+'/'+k)
        return value
    def text(path):return require(path,'string')
    def binding(path):
        value=obj(path,[],['fixtureLogicalRef','fixtureRevision','admittedRuntimeBinding'])
        if value is None:return
        for k in ['fixtureLogicalRef','fixtureRevision']:
            v=text(path+'/'+k)
            if v is not MISSING and not v.strip():err('EMPTY_BINDING_COMPONENT',path+'/'+k)
        v=get(path+'/admittedRuntimeBinding')
        if v is MISSING:err('MISSING_REQUIRED_ROLE',path+'/admittedRuntimeBinding')
        elif v is not False:err('INVALID_FIXTURE_ADMISSION_FLAG',path+'/admittedRuntimeBinding',expected=False,actual=json_type(v))
    def ptr(path):
        value=text(path)
        if value is not MISSING and not valid_pointer(value):err('INVALID_JSON_POINTER',path)
    def measured(path):
        keys=['role','measurementBinding','resultPointer','contextBinding','subjectRelationBinding','methodUseBinding','qualificationPointers']
        value=obj(path,[],keys)
        if value is None:return None
        role=text(path+'/role')
        if role is not MISSING and role!='MEASURED_COMPLIANCE_OPERAND':err('SOURCE_ROLE_MISMATCH',path+'/role')
        for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']:binding(path+'/'+k)
        ptr(path+'/resultPointer');qs=require(path+'/qualificationPointers','array')
        if qs is not MISSING:
            for i in range(len(qs)):ptr(path+'/qualificationPointers/'+str(i))
        return value
    def scalar_provenance(path):
        value=obj(path,[],['sourceBinding','valuePointer','lexicalPointer','qualifierPointer'])
        if value is None:return
        binding(path+'/sourceBinding')
        for k in ['valuePointer','lexicalPointer','qualifierPointer']:ptr(path+'/'+k)
    if not isinstance(body,dict):return [{'code':'INVALID_TYPE','pointer':'','expected':'object','actual':json_type(body)}]
    if row=='C03':
        binding('/criterion');binding('/measurement');ptr('/operandPointer');s=measured('/measurementSource')
        if isinstance(s,dict):
            if isinstance(body.get('measurement'),dict) and isinstance(s.get('measurementBinding'),dict) and body['measurement']!=s['measurementBinding']:err('MEASUREMENT_ALIAS_MISMATCH','/measurementSource/measurementBinding')
            if isinstance(body.get('operandPointer'),str) and isinstance(s.get('resultPointer'),str) and body['operandPointer']!=s['resultPointer']:err('POINTER_ALIAS_MISMATCH','/measurementSource/resultPointer')
    elif row=='C04':
        binding('/criterion');op=obj('/operand',[])
        if op is not None:
            measured('/operand/source');text('/operand/resultKind');obj('/operand/admissibleValues',[])
            if op.get('resultKind')=='CENSORED_NUMERIC':
                unknown=sorted(set(op)-{'resultKind','qualifier','limit','nonnegative','admissibleValues','source'})
                if unknown:err('UNKNOWN_MEMBERS','/operand',members=unknown)
                text('/operand/qualifier');obj('/operand/limit',[]);require('/operand/nonnegative','boolean')
            if op.get('resultKind')=='CENSORED_NUMERIC':scalar_provenance('/operand/limit/provenance')
        scalar_provenance('/threshold/provenance')
    elif row=='C06':
        s=obj('/rateSource',[])
        if s is not None:
            kind=text('/rateSource/sourceKind');binding('/rateSource/sourceBinding');ptr('/rateSource/valuePointer')
            allowed={'sourceKind','sourceBinding','valuePointer'}
            if kind=='MEASUREMENT_EVIDENCE':
                allowed.add('measurementSource');ms=measured('/rateSource/measurementSource')
                if isinstance(ms,dict):
                    if isinstance(s.get('sourceBinding'),dict) and isinstance(ms.get('measurementBinding'),dict) and s['sourceBinding']!=ms['measurementBinding']:err('MEASUREMENT_ALIAS_MISMATCH','/rateSource/measurementSource/measurementBinding')
                    if isinstance(s.get('valuePointer'),str) and isinstance(ms.get('resultPointer'),str) and s['valuePointer']!=ms['resultPointer']:err('POINTER_ALIAS_MISMATCH','/rateSource/measurementSource/resultPointer')
            elif kind is not MISSING and kind not in ['HUMAN_REPORT','OPERATION_PARAMETER']:err('UNKNOWN_RATE_SOURCE_KIND','/rateSource/sourceKind')
            unknown=sorted(set(s)-allowed)
            if unknown:err('UNKNOWN_MEMBERS','/rateSource',members=unknown)
    elif row=='C09':
        posture=text('/evidencePosture');binding('/claimBasis')
        if posture=='MEASURED':measured('/measurementSource')
        elif posture is not MISSING and posture not in ['MODELLED','ESTIMATED','DISPUTED']:err('UNKNOWN_METRIC_POSTURE','/evidencePosture')
    if required_qualification:
        q=obj('/measuredQualification',[],['sourceBinding','sourcePointer','methodUseBinding','interpretation'])
        if q is not None:
            binding('/measuredQualification/sourceBinding');binding('/measuredQualification/methodUseBinding');ptr('/measuredQualification/sourcePointer');text('/measuredQualification/interpretation')
    return errors

def error_codes(errors):
    # Compatibility view for inherited finite tests, preserving the structured public result.
    codes=[]
    for e in errors:
        code=e['code'];p=e['pointer']
        codes.append(code+':'+p if code in ['MISSING_REQUIRED_ROLE','INCOMPLETE_REQUIRED_ROLE','INVALID_FIXTURE_BINDING'] else code)
    return codes

def required_role_error_codes(*args,**kwargs):return error_codes(required_role_errors(*args,**kwargs))
