"""Account for all definitions and requirements without inflating completion."""
import hashlib,json
from pathlib import Path
from build_value_types import VALUE_ID
HERE=Path(__file__).resolve().parent
def read(name):return json.loads((HERE/name).read_text())
def put(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')

def main():
    source_map=read('definition-construction-map.json');requirements=read('requirement-construction-map.json')
    rows=[]
    named={
        'S03':['recurring zone declaration must be true'],
        'S12':['asset-kind alias equals scoped subject kind'],
        'O22':['profile/posture/facet/output-role matrix','work target/extent/activity and method aliases','output-specification equality'],
        'O25':['distinct reclassification classes','same-cohort basis equality and absent successor'],
        'O27':['no creation effect','proposed identity status','predecessors required except initial/harvest basis'],
        'C03':['measurement binding and selected-result pointer aliases'],
        'C04':['censored result-kind preservation'],
        'C06':['allowed source kind and measured-source aliases'],
        'C16':['qualified organic parcel INDETERMINATE/PENDING representation','independently selected profile/year/route/parcel/history/evidence selector agreement','refusal of unsupported satisfied/exemption outcome'],
        'C17':['recordkeeping allegation does not claim lawful use'],
    }
    for r in source_map['definitions']:
        atom=r['kind']=='CLAIM_ATOM';operation=r['id'].startswith('O') and atom
        intrinsic=['canonical calendar time and positive interval'] if atom else []
        if operation:intrinsic+=['profile/posture agreement','work activity/target/extent aliases','nonempty unique condition IDs','same-atom quantity IDs/role/material references','quantity time/scope/activity agreement','explicit quantity types and role-driven material/basis disclosure rules']
        intrinsic+=named.get(r['id'],[])
        helpers=[]
        if r['group']=='V04':helpers=['event_literal_errors','OwnedComponent.event_time_errors']
        elif r['group']=='V05':helpers=['OwnedComponent.measurement_result_errors','OwnedComponent.measured_instant_errors','interval_outcome (pure math only)']
        rows.append({
            'id':r['id'],'source':r['source'],'definition':r['definition'],'requirements':r.get('requirements',[]),
            'completeSemanticImplementation':False,
            'explicitFieldContract':VALUE_ID+'#/$defs/O22' if r['id']=='O22' else None,
            'explicitQualifiedVariant':VALUE_ID+'#/$defs/nlQualifiedOrganicParcelBody' if r['id']=='C16' else None,
            'finiteReviewedForm':r.get('scaffoldSchemaPointer'),
            'implementedIntrinsicSubchecks':intrinsic,
            'availableSharedHelpersNotCompleteRowEvaluators':helpers,
            'remainingOwnedWork':[
                *([] if r['id']=='O22' else ['Complete explicit row field/branch contract beyond finite reviewed forms or the named qualified variant.'] if atom else ['Complete row-specific interpretation, selected source mapping and semantic evaluator.']),
                'Complete independently selected source comparisons for every source predicate; a matching selector or schema is not evidence admission.',
                'Independent semantic positive/hostile coverage through the complete public verifier entry point.',
            ],
            'retainedSourcePredicates':r['domainPredicates'],
            'interfaceInvestigations':r.get('exactOwnerPrerequisites',[]),
            'investigationCaution':'An investigation ID is not a blanket blocker. Reuse existing carriers; identify the exact missing row/source role before declaring a foreign prerequisite.',
        })
    requirement_map=[{'id':r['id'],'definitionIds':r['constructionDefinitionIds'],'completeImplementation':False,
                      'sourceSpecification':r,'status':'RETAINED_WITH_PARTIAL_SUBCHECKS; owned completion is not inferred from mapping coverage'} for r in requirements['requirements']]
    source=HERE.parent/'owned-contract/source-duties.json';raw=source.read_bytes();duties=json.loads(raw)
    assert len(duties['duties'])==49 and duties['counts']=={'AR':29,'PC':20}
    put('obligation-retention-map.json',{'status':'ALL_49_RETAINED_NO_COMPONENT_COMPLETION_CLAIM',
        'constructionSource':{'path':'../owned-contract/source-duties.json','sha256':hashlib.sha256(raw).hexdigest()},
        'originalSource':duties['source'],'counts':duties['counts'],
        'duties':[{**d,'scope':'Complete public verifier integration obligation; this bounded component does not discharge it.'} for d in duties['duties']],
        'next':'Integrate all AR/PC duties with the coordinator-owned payload and public verifier; do not substitute component test counts.'})
    put('execution-map.json',{'status':'BOUNDED_EXECUTABLE_COMPONENT_PLUS_EXPLICIT_REMAINING_OWNED_WORK',
        'sourceHead':source_map['sourceHead'],'primaryTrustBoundary':'AssertionRecord domain meaning and validation integrity',
        'scopeStayedInsideBoundary':True,
        'counts':{'definitionsAccounted':99,'requirementsAccounted':42,'finiteReviewedFormRows':58,
                  'completeExplicitRowFieldContracts':1,'additionalQualifiedRowVariants':1,'completeSemanticRowEvaluators':0,
                  'preservedWholeMeanings':25,'timeProfiles':9,'retainedEventProfileCells':17,'AR_PC_Obligations':49},
        'definitions':rows,'requirements':requirement_map,
        'numericBoundary':'interval_outcome is only exact set mathematics. It does not select a source, establish a material/basis/role/posture/extent/time, qualify a method or accept a compliance comparison. quantity_context_errors compares the independently selected domain tuples first; actual source interpretation, conversion and admission remain separate required checks.',
        'quantityLimits':'Named role restrictions reject NOT_APPLICABLE for material-dependent and ratio roles. UNREPORTED stays representable but cannot satisfy quantity_context_errors. Arbitrary quantity-kind/unit and process phase semantics, ratio status of newly selected kinds, normalization conversion and proof of subextent remain owned selected-definition/source predicates.',
        'next':'Continue the explicitly retained owned row contracts and source predicates, then close narrowly identified foreign interfaces before complete verifier acceptance.'})
    print(json.dumps({'definitions':len(rows),'requirements':len(requirement_map),'completeRowFieldContracts':1,'completeRowSemanticEvaluators':0,'duties':len(duties['duties'])}))
if __name__=='__main__':main()
