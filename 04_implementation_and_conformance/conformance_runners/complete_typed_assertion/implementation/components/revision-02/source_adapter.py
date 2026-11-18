"""Reversible reviewed-form transformation; never infers source admission."""
import copy,hashlib,json
from common import *

def escape(value):return value.replace('~','~0').replace('/','~1')
def wire_subject(reviewed_subject):
    if not isinstance(reviewed_subject,dict) or set(reviewed_subject)!={'kind','binding'}:raise ValueError('Expected exact reviewed kind/binding subject')
    b=reviewed_subject['binding']
    if not isinstance(b,dict) or set(b) not in [{'ref','revisionRef'},{'ref','digest'}]:raise ValueError('Reviewed subject must carry one immutable selector')
    return {'subjectPosture':'EXISTING_SUBJECT','subjectType':reviewed_subject['kind'],'subjectRef':b['ref'],**{k:v for k,v in b.items() if k!='ref'}}

def adapt_proposition(original):
    operations=[]
    def record(path,before,after,reason):operations.append({'pointer':path,'before':copy.deepcopy(before),'after':copy.deepcopy(after),'reason':reason})
    def visit(value,path):
        if isinstance(value,list):return [visit(v,path+'/'+str(i)) for i,v in enumerate(value)]
        if not isinstance(value,dict):return value
        if set(value)=={'fixtureLogicalRef','fixtureRevision','admittedRuntimeBinding'}:
            if value['admittedRuntimeBinding'] is not False:raise ValueError('Unexpected fixture admission marker')
            out={'ref':value['fixtureLogicalRef'],'revisionRef':value['fixtureRevision']};record(path,value,out,'Fixture spelling to existing immutable selector syntax; no admission inferred.');return out
        out={k:visit(v,path+'/'+escape(k)) for k,v in value.items()}
        if out.get('form')=='ATOM':
            old=out['definition'];row=old.rsplit('#',1)[-1]
            if row not in {r['id'] for r in reviewed('reviewed-input/domain/inventory.json')['rows']}:raise ValueError('Unknown source row: '+row)
            out['definition']=DEFINITION_PREFIX+row;record(path+'/definition',old,out['definition'],'New explicit draft row identity.')
            old=out['scope']['subject'];out['scope']['subject']=wire_subject(old);record(path+'/scope/subject',old,out['scope']['subject'],'Explicit existing-subject adapter. Prospective subjects are a separate direct wire branch.')
        return out
    return visit(copy.deepcopy(original),''),operations

def restore_proposition(adapted,operations):
    restored=copy.deepcopy(adapted)
    for op in reversed(operations):
        path=[s.replace('~1','/').replace('~0','~') for s in op['pointer'].split('/')[1:]]
        if not path:restored=copy.deepcopy(op['before']);continue
        parent=restored
        for part in path[:-1]:parent=parent[int(part)] if isinstance(parent,list) else parent[part]
        key=int(path[-1]) if isinstance(parent,list) else path[-1]
        if parent[key]!=op['after']:raise ValueError('Inverse ledger conflict at '+op['pointer'])
        parent[key]=copy.deepcopy(op['before'])
    return restored

def main():
    examples=reviewed('review-amendment-03/candidate-examples-v4.json')['examples'];converted=[];ledgers=[]
    for example in examples:
        original=example['claimContent']['proposition'];adapted,operations=adapt_proposition(original)
        if restore_proposition(adapted,operations)!=original:raise ValueError('Round trip mismatch: '+example['id'])
        converted.append({'id':example['id'],'proposition':adapted,'sourceClaimContentDigest':example['claimContentDigest'],'sourceRenderedTextDigest':example['renderedTextSha256'],'foreignAdmission':'NOT_ESTABLISHED'})
        ledgers.append({'id':example['id'],'operations':operations,'roundTripVerified':True})
    put('adapted-propositions.json',{'sourceHead':HEAD,'count':len(converted),'examples':converted,'next':'Root-owned projection transforms the outer carrier and rerenders; this file owns only the proposition transformation.'})
    put('source-transformation-ledger.json',{'sourceHead':HEAD,'schemaId':SCHEMA_ID,'definitionPrefix':DEFINITION_PREFIX,'count':len(ledgers),'ledgers':ledgers,'next':'Retain source bytes and use this reversible ledger when integrating the new wire projection.'})
    print(json.dumps({'adaptedPropositions':len(converted),'reversible':len(ledgers)}))
if __name__=='__main__':main()
