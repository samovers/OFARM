"""Apply independently authored finite fixture choices during v4 regeneration."""
import copy,hashlib,json

def read(root,name):return json.loads((root/name).read_text())
def repair_hostiles(hostiles,root):
    approved=read(root,'owner-approved-h03-fix01.json')
    h=next(x for x in hostiles['cases'] if x['id']=='H03_WRONG_PROPERTY_VALID_SOURCE_AND_MEMBERSHIP')
    replacements=[]
    for role,record in approved['records'].items():
        index=next(i for i,r in enumerate(h['records']) if r['role']==role)
        replacements.append((h['records'][index]['binding'],record['binding']))
        h['records'][index]=copy.deepcopy(record)
    body=h['claimContent']['proposition']['body'];selection=copy.deepcopy(approved['ownerProfileSelection'])
    for key in ['measurementBinding','contextBinding','subjectRelationBinding']:body['operand']['source'][key]=copy.deepcopy(selection[key])
    body['operand']['limit']['provenance']['sourceBinding']=copy.deepcopy(selection['quantityProvenanceBinding'])
    for old,new in replacements:h['claimContent']['evidenceBindings']=[copy.deepcopy(new) if b==old else b for b in h['claimContent']['evidenceBindings']]
    h['ownerProfileSelection']=selection
    assert h['expectedErrors']==['PROPERTY_MISMATCH']
    for correction in read(root,'hostile-diagnostics-fix01.json')['cases']:
        case=next(x for x in hostiles['cases'] if x['id']==correction['id'])
        if case['expectedErrors']!=correction['originalErrors']:raise ValueError('Historical hostile meaning changed: '+case['id'])
        case['expectedErrors']=correction['additionalErrors']+case['expectedErrors']

def extend_role_contract(contract,root):
    profile=read(root,'w05-owner-profile-fix01.json')
    contract['fix01SourceProfile']={
        'id':profile['id'],'status':profile['status'],
        'file':'w05-owner-profile-fix01.json',
        'sha256':hashlib.sha256((root/'w05-owner-profile-fix01.json').read_bytes()).hexdigest(),
        'requiredResultKind':profile['requiredResultKind'],
        'requiredScalarProvenance':profile['requiredScalarProvenance'],
        'rule':'The selected finite owner profile fixes required W05 source roles before dependent access. Claimant discriminator changes cannot remove them. Exact immutable source bytes are checked against independent approved pins, not only self-reported contentDigest.',
        'separateApprovedFixtures':[{'file':n,'sha256':hashlib.sha256((root/n).read_bytes()).hexdigest()} for n in ['owner-approved-lexical-r2-fix01.json','owner-approved-h03-fix01.json']],
        'limits':'Fictional non-adopted design fixtures only; no runtime source authority, producer, or general numeric branch engine.'}
