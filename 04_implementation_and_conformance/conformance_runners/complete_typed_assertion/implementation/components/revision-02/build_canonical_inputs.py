"""Author consumer input contracts for all 41 canonical interpretation rows.

Record fields reference actual pinned schemas. Projection fields are a fixed
per-row list from the reviewed source selectors, never a caller-defined rule.
These inputs do not implement an evidence producer or authenticate its facts.
"""
from common import *
from runtime_support import Schemas
CANONICAL_ID='https://ofarm.dev/schema/drafts/non-default/assertion-domain/canonical-inputs/v0.1'
S=lambda name,version='v0.1':'https://ofarm.dev/schema/'+name+'/'+version
IDS={'event':S('semanticeventenvelope'),'measurement':S('measurementevidence'),'context':S('agronomicobservationcontext'),
     'execution':S('executionrecordpayload'),'intent':S('interventionintentpayload'),'extent':S('partialextent'),
     'lineage':S('identitylifecyclechange'),'party':S('partyrelationship'),'responsibility':S('scoperesponsibilityrelationship'),
     'commitment':S('externalcommitmentlink'),'decision':S('reviewdecision'),'field':S('fieldidentitypayload'),
     'cycle':S('cropcycleidentitypayload'),'equipment':S('equipmentidentitypayload'),'code':S('agronomicidentitybinding'),
     'codeProfile':S('agronomiccodebindingprofile'),'sufficiency':S('evidencesufficiencycase','v0.2')}
ID_FIELDS={'event':'semanticEventId','measurement':'measurementEvidenceId','context':'agronomicObservationContextId','execution':'executionRecordPayloadId','intent':'interventionIntentPayloadId','extent':'partialExtentId','lineage':'identityLifecycleChangeId','party':'partyRelationshipId','responsibility':'scopeResponsibilityRelationshipId','commitment':'externalCommitmentLinkId','decision':'reviewDecisionId','field':'fieldidentitypayloadId','cycle':'cropcycleidentitypayloadId','equipment':'equipmentidentitypayloadId','code':'agronomicIdentityBindingId','codeProfile':'agronomicCodeBindingProfileId','sufficiency':'sufficiencyCaseId'}
# Lists are authored from the reviewed row predicates and actual carrier fields.
PROJECTIONS={
 'measurementMeaning':('measurement',['observedPropertyRef','phenomenonTime','sampleRef','agronomicObservationContextRef','source','samplingProtocol','measurementMethod','instrument','calibration','labContext','result','uncertainty','chainOfCustodyStatus','originalPayloadRef','originalPayloadHash','provenanceRefs','referenceSnapshotRefs','evidenceStatus','degradationReasons','upgradeOfMeasurementEvidenceRef','supersedesMeasurementEvidenceRef','agronomicIdentityBindingRefs','agronomicCodeBindingProfileRef'],['observedPropertyRef','source','result','provenanceRefs','evidenceStatus']),
 'contextMeaning':('context',['subject','targetScope','observedPropertyRef','phenomenonTime','observationAgent','spatialContext','procedure','cropCycleRef','cropBindings','phenologyStateBinding','targetOrganismBindings','partEvaluated','severityOrPressure','measurementEvidenceRefs','confidence','uncertainty','referenceSnapshotRefs','contextCompleteness','promotionUse'],['subject','observedPropertyRef','phenomenonTime','observationAgent','spatialContext','procedure','contextCompleteness','promotionUse']),
 'operationTarget':('execution',['subject','executionExtent','effectiveTimeInterval'],['subject','executionExtent','effectiveTimeInterval']),
 'extentMeaning':('extent',['extentRole','parentScope','anchorScope','temporalApplicability','geometryBasis','qualityStatement','durableIdentityPolicy'],['extentRole','parentScope','anchorScope','temporalApplicability','geometryBasis','qualityStatement','durableIdentityPolicy']),
 'decisionMeaning':('decision',['reviewedArtifactFamily','reviewedArtifactRef','anchorScopes','decidedAt','reviewAction','decisionOutcomeState','resultingAcceptedConsequenceRefs'],['reviewedArtifactFamily','reviewedArtifactRef','anchorScopes','decidedAt','reviewAction','decisionOutcomeState']),
 'lineageMeaning':('lineage',['subjectFamily','subjectClass','changeKind','continuityOutcome','identityContinuityClass','oldIdentityRefs','newIdentityRefs','revisionRefs','lineageRelations','effectiveFrom'],['subjectFamily','changeKind','continuityOutcome','identityContinuityClass','oldIdentityRefs','newIdentityRefs','lineageRelations']),
 'equipmentUse':('execution',['subject','equipment','actor','sourceEventRef','sourcePayload','effectiveTimeInterval'],['subject','equipment','actor','sourcePayload','effectiveTimeInterval']),
 'equipmentIdentity':('equipment',['identityRecordRef','equipmentClass','inspectionEvidenceRefs'],['identityRecordRef']),
 'partyMeaning':('party',['partyARef','partyBRef','relationshipKind','relationshipDirectionality','validFrom','validUntil','relationshipState'],['partyARef','partyBRef','relationshipKind','relationshipDirectionality','validFrom','relationshipState']),
 'responsibilityMeaning':('responsibility',['partyRef','targetScope','relationshipKind','validFrom','validUntil','relationshipState','counterpartyRef','responsibilityClasses'],['partyRef','targetScope','relationshipKind','validFrom','relationshipState']),
 'commitmentMeaning':('commitment',['linkKind','externalSystemRef','externalObjectType','externalObjectIdentifier','linkedPartyRefs','linkedScopes','validFrom','validUntil','referencePosture'],['linkKind','externalSystemRef','externalObjectType','externalObjectIdentifier','referencePosture']),
 'fieldParent':('field',['identityRecordRef','parentFarmIdentityRef'],['identityRecordRef','parentFarmIdentityRef']),
 'cycleParent':('cycle',['identityRecordRef','parentScopeRefs','startedAt','endedAt','overlapRelationRefs'],['identityRecordRef','parentScopeRefs']),
 'codeMeaning':('code',['bindingRole','localSubject','externalScheme','bindingValue','profileRefs','referenceSnapshotRefs','lineage','promotionBoundary'],['bindingRole','localSubject','externalScheme','bindingValue','promotionBoundary']),
}

def main():
    schemas=Schemas().schemas;defs={};rows=reviewed('reviewed-input/canonical/inventory.json')['rows'];ledger=[]
    for name,sid in IDS.items():defs[name+'Source']=obj({'binding':BINDING,'record':{'$ref':sid}})
    for name,(carrier,fields,required) in PROJECTIONS.items():
        assert set(fields)<=set(schemas[IDS[carrier]]['properties'])
        defs[name]=obj({f:{'$ref':IDS[carrier]+'#/properties/'+f} for f in fields},required)
    time=vref('subjectTime');target=obj({'kind':enum(KINDS+['SAMPLE','PARTIAL_EXTENT','DOCUMENT','REVIEW_DECISION','INSPECTION_RECORD','PARTY']),'binding':BINDING})
    defs['endpoint']=target
    defs['timeSelector']=one(enum(['/timeSemantics/'+p for p in ['eventTime','observationTime','decisionTime','effectiveFrom']]),{'const':['/timeSemantics/effectiveFrom','/timeSemantics/effectiveUntil']})
    defs['eventMeaning']=obj({'subtypePresence':enum(['PRESENT','ABSENT']),'eventSubtypeId':TEXT,'dominantSemanticConsequence':TEXT,
        'concept':TEXT,'family':{'$ref':IDS['event']+'#/properties/primaryEventFamily'},'vocabularyBinding':BINDING,'packBinding':BINDING,'timeSelector':ref('timeSelector')},
        ['subtypePresence','dominantSemanticConsequence','concept','family','vocabularyBinding','packBinding','timeSelector'])
    defs['eventMeaning']['allOf']=[condition('subtypePresence','PRESENT',{'required':['eventSubtypeId']},{'not':{'required':['eventSubtypeId']}})]
    event_fields={'event':ref('eventSource'),'subjectTime':time,'selectedMeaning':ref('eventMeaning'),'claimedMeaning':ref('eventMeaning'),
        'selectedSubject':{'$ref':IDS['event']+'#/properties/subjectRefs/items'},'selectedAnchor':{'$ref':IDS['event']+'#/properties/anchorScopes/items'}}
    source_pair={'measurement':ref('measurementSource'),'context':ref('contextSource'),'measurementProjection':ref('measurementMeaning'),'contextProjection':ref('contextMeaning')}
    endpoint_fields={'from':ref('endpoint'),'to':ref('endpoint'),'subjectTime':time}
    for row in rows:
        rid=row['id'];fields={};alternatives=None;notes=[]
        if rid.startswith('V04-') and rid not in ['V04-action-families','V04-profiles']:fields=event_fields
        elif rid=='V04-action-families':
            fields={'activityConcept':enum(row['typedRepresentation']['candidateActivityConcepts']),'atom':{'$ref':SCHEMA_ID+'#/$defs/atom'}}
        elif rid=='V04-profiles':
            alternatives=[obj({'subjectTime':time,'eventPresence':const('ABSENT')}),obj({'subjectTime':time,'eventPresence':const('PRESENT'),'event':ref('eventSource'),'selectedTimeSelector':ref('timeSelector')})]
        elif rid.startswith('V05-time-'):
            fields={'measurement':ref('measurementSource'),'subjectTime':{'$ref':BASE_ID+'#/$defs/PERFORMED_INSTANT'},'methodUseBinding':BINDING,'meaningConcept':const(row['typedRepresentation']['candidateConcept']),'projection':ref('measurementMeaning')}
        elif rid.startswith('V05-result-'):
            fields={'measurement':ref('measurementSource'),'claimedResult':{'$ref':IDS['measurement']+'#/properties/result'},'methodUseBinding':BINDING,'projection':ref('measurementMeaning')}
        elif rid.startswith('V05-source-'):fields={'measurement':ref('measurementSource'),'projection':ref('measurementMeaning')}
        elif rid=='V05-context':fields=source_pair
        elif rid=='V05-code-bindings':fields={'code':ref('codeSource'),'codeProjection':ref('codeMeaning'),'profile':ref('codeProfileSource'),'selectedRole':enum(row['typedRepresentation']['existingSchemaRoles'])}
        elif rid=='V06-operation-target':fields={**endpoint_fields,'event':ref('eventSource'),'execution':ref('executionSource'),'projection':ref('operationTarget')}
        elif rid in ['V06-sample-target','V06-report-about']:fields={**endpoint_fields,**source_pair,'extent':ref('extentSource'),'extentProjection':ref('extentMeaning')}
        elif rid=='V06-extent':fields={**endpoint_fields,'extent':ref('extentSource'),'projection':ref('extentMeaning')}
        elif rid=='V06-decision-applies':fields={**endpoint_fields,'decision':ref('decisionSource'),'projection':ref('decisionMeaning'),'reviewedArtifactBinding':BINDING,'artifactSubjectRelationBindings':arr(BINDING,1,True)}
        elif rid=='V06-lineage':fields={**endpoint_fields,'lineage':ref('lineageSource'),'projection':ref('lineageMeaning'),'relationType':{'$ref':IDS['lineage']+'#/properties/lineageRelations/items/properties/relationType'}}
        elif rid=='V06-equipment-use':fields={**endpoint_fields,'execution':ref('executionSource'),'equipmentIdentity':ref('equipmentSource'),'projection':ref('equipmentUse'),'identityProjection':ref('equipmentIdentity'),'equipmentRole':enum(['equipmentRef','tractorOrPowerUnitRef','implementRef','controllerRef'])}
        elif rid=='V06-occupancy':
            fields={**endpoint_fields,'occupancyStart':TIMESTAMP,'occupancyEnd':TIMESTAMP,'lifecycle':ref('lineageSource')};notes=['The lifecycle token cannot supply missing typed occupancy endpoints/interval. Exact carrier gap OCCUPANCY_ENDPOINT_INTERVAL_CARRIER remains; no synthetic foreign record is accepted.']
        elif rid=='V06-party-context':
            alternatives=[obj({**endpoint_fields,'carrierKind':const(name),name:ref(name+'Source'),'projection':ref(projection)}) for name,projection in [('party','partyMeaning'),('responsibility','responsibilityMeaning'),('commitment','commitmentMeaning')]]
        elif rid=='V06-parent-scope':alternatives=[obj({**endpoint_fields,'carrierKind':const(name),name:ref(name+'Source'),'projection':ref(projection)}) for name,projection in [('field','fieldParent'),('cycle','cycleParent')]]
        elif rid=='V06-endpoints':fields={'subject':{'$ref':SCHEMA_ID+'#/$defs/domainSubject'},'contexts':arr({'$ref':SCHEMA_ID+'#/$defs/contextBinding'}),'evidenceEndpoints':arr(ref('endpoint'))}
        elif rid=='V06-proof-interface':fields={'subjectScopeProofBindings':arr(BINDING,1,True),'contextBindings':arr({'$ref':SCHEMA_ID+'#/$defs/contextBinding'}),'associatedSemanticEventBinding':BINDING}
        else:raise ValueError(rid)
        if alternatives:defs[rid]=one(*alternatives)
        else:
            defs[rid]=obj(fields)
            if rid in ['V06-sample-target','V06-report-about']:
                defs[rid]['required']=[k for k in fields if k not in ['extent','extentProjection']]
                defs[rid]['dependentRequired']={'extent':['extentProjection'],'extentProjection':['extent']}
        ledger.append({'row':rid,'schema':CANONICAL_ID+'#/$defs/'+rid,'sourceRevision':row['revision'],'sourceBindings':row['sourceBindings'],'contractScope':'Explicit consumer input and fixed source projections; foreign resolution/eligible use/admission remains independently required.','notes':notes})
    assert len(ledger)==41
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':CANONICAL_ID,'title':'Canonical domain interpretation consumer inputs',
        '$comment':'41 explicit consumer contracts. Full records retain their actual existing schemas. Selected inputs must be selected independently by the coordinator; passing a projection comparison is not admission.',
        '$defs':defs}
    put('canonical-inputs.schema.json',schema);put('canonical-input-ledger.json',{'rows':ledger,'counts':{'definitions':41},'projectionContracts':PROJECTIONS,'next':'Validate the explicit carrier comparisons and remaining source eligibility interfaces.'})
    print(json.dumps({'canonicalInputContracts':len(ledger),'schemaId':CANONICAL_ID}))
if __name__=='__main__':main()
