"""Stable local JSON entry point for coordinator-owned AR/PC orchestration.

One JSON object on stdin, one result on stdout. Exit code 2 denotes malformed
invocation. A valid invocation returns code 0 even when a comparison fails;
inspect errors and all required roles. This is not the public domain verifier.
"""
import json,sys
from intrinsics import Intrinsics
from carrier_adapters import CanonicalAdapters
from operation_adapters import OperationAdapters
from meaning_comparisons import MeaningComparisons
from record_comparisons import RecordComparisons

def evaluate(request):
    if not isinstance(request,dict) or not isinstance(request.get('operation'),str):raise ValueError('Object with operation is required')
    operation=request['operation']
    fields={'intrinsics':{'operation','proposition'},'canonical':{'operation','row','input'},'operationSource':{'operation','row','input'},'recordSource':{'operation','row','input'},
            'selectedMeaning':{'operation','claim','selected'},'quantityComparison':{'operation','claim','selected','operator','selectedOperator','threshold','selectedThreshold'},
            'criterionComparison':{'operation','claim','selected'}}
    allowed=fields.get(operation)
    if allowed is None:raise ValueError('Unknown operation')
    optional={'selectedMappingContext'} if operation=='criterionComparison' else set()
    if not allowed<=set(request) or set(request)-allowed-optional:raise ValueError('Incorrect request fields for '+operation)
    if operation=='intrinsics':return Intrinsics().check(request['proposition'])
    if operation=='canonical':return CanonicalAdapters().check(request['row'],request['input'])
    if operation=='operationSource':return OperationAdapters().check(request['row'],request['input'])
    if operation=='recordSource':return RecordComparisons().check(request['row'],request['input'])
    m=MeaningComparisons()
    if operation=='selectedMeaning':return m.row(request['claim'],request['selected'])
    if operation=='quantityComparison':return m.quantity(request['claim'],request['selected'],request['operator'],request['selectedOperator'],request['threshold'],request['selectedThreshold'])
    return m.criterion(request['claim'],request['selected'],request.get('selectedMappingContext'))

def main():
    try:
        def reject_nonfinite(value):raise ValueError('Non-finite JSON number '+value)
        def unique_keys(pairs):
            result={}
            for key,value in pairs:
                if key in result:raise ValueError('Duplicate JSON key '+key)
                result[key]=value
            return result
        request=json.load(sys.stdin,parse_constant=reject_nonfinite,object_pairs_hook=unique_keys)
        response=evaluate(request);print(json.dumps(response,ensure_ascii=False,allow_nan=False))
    except (ValueError,KeyError,TypeError,IndexError) as exc:
        print(json.dumps({'disposition':'INVOCATION_FAILED','errors':[{'code':'INVALID_DOMAIN_COMPONENT_INVOCATION','reason':str(exc)}]}));raise SystemExit(2)
if __name__=='__main__':main()
