"""Account for all99 definitions,42 requirements,25 meanings and49 duties."""
import hashlib,json
from common import *
from record_comparisons import BRANCHES

def main():
    old=json.loads((HERE.parent/'execution-map.json').read_text());rows=[]
    canonical={r['id']:r for r in reviewed('reviewed-input/canonical/inventory.json')['rows']}
    atoms={r['id']:r for r in reviewed('reviewed-input/domain/inventory.json')['rows']}
    for previous in old['definitions']:
        rid=previous['id'];is_atom=rid in atoms
        checks=['domain_api.evaluate:intrinsics','domain_api.evaluate:selectedMeaning'] if is_atom else ['domain_api.evaluate:canonical']
        if rid.startswith('O') and is_atom:checks.append('domain_api.evaluate:operationSource')
        if rid in BRANCHES:checks.append('domain_api.evaluate:recordSource')
        if rid=='C04':checks.append('domain_api.evaluate:criterionComparison')
        rows.append({'id':rid,'kind':'CLAIM_ATOM' if is_atom else 'CANONICAL_INTERPRETATION','inputSchema':SCHEMA_ID+'#/$defs/'+rid if is_atom else 'https://ofarm.dev/schema/drafts/non-default/assertion-domain/canonical-inputs/v0.1#/$defs/'+rid,
            'callableComparisons':checks,'completeSemanticImplementation':False,
            'sourceDefinition':previous['source'],'sourcePredicates':previous['retainedSourcePredicates'],
            'requirementIds':previous['requirements'],'implementedIntrinsicSubchecks':(['recursive schema, calendar/time interval checks, unique atom IDs, qualification and sequence scope, exact independent typed meaning equality']+(['work activity/target/extent aliases, quantity role/material/basis/time and selected source fidelity'] if rid.startswith('O') else [])) if is_atom else ['fixed actual source-schema projections and explicit row carrier comparisons'],
            'remainingOwnedWork':(['Concrete row-specific source selection and missing carrier roles beyond exact independently selected domain meaning.'] if is_atom and not rid.startswith('O') and rid not in BRANCHES else [])+['Establish every returned row/source role from actual pinned owner contracts; do not replace it with a Boolean.','Integrate and independently test through the complete public verifier entry point.'],
            'scopeStatement':'Schema completeness and callable comparison coverage do not imply full source semantic or owner admission completeness.'})
    reports={name:json.loads((HERE/name).read_text())['counts'] for name in ['field-contract-results.json','semantic-results.json','operation-source-results.json','meaning-comparison-results.json','row-source-results.json','time-range-results.json','intended-source-results.json','review-repair-results.json']}
    obligations=json.loads((HERE.parent/'obligation-retention-map.json').read_text())
    examples=reviewed('review-amendment-03/candidate-examples-v4.json')['examples']
    assert len(rows)==99 and len(old['requirements'])==42 and len(examples)==25 and len(obligations['duties'])==49
    result={'status':'CONTINUING_CONSTRUCTION_WITH_STABLE_CALLABLE_COMPONENTS','sourceHead':HEAD,'primaryTrustBoundary':'AssertionRecord domain meaning and validation integrity','scopeStayedInsideBoundary':True,
        'counts':{'definitions':99,'atomFieldContracts':58,'canonicalInputContracts':41,'operationSourceAdapters':27,'structuralComplianceSourceRows':len(BRANCHES),'requirements':42,'wholeMeanings':25,'timeProfiles':9,'eventPresenceProfileCells':17,'AR':29,'PC':20,'completeSemanticRowEvaluators':0},
        'definitions':rows,'requirements':old['requirements'],'retainedObligations':obligations['duties'],'wholeMeaningIds':[e['id'] for e in examples],
        'verificationCountsByScope':reports,'sealedCheckpointUntouched':'../checkpoint-manifest.json',
        'integrationRule':'Conjoin component errors, exact actual source resolution and all returned required roles with every outer AR/PC duty. ANY and NOT never relax those gates. Component dispositions are not domain PASS or admission.',
        'next':'Continue structural/compliance source adapters and precise source-role investigations while coordinator integrates stable callables.'}
    put('coverage-ledger.json',result);print(json.dumps(result['counts']))
if __name__=='__main__':main()
