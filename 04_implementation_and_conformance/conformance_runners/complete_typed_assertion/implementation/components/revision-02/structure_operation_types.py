"""Authored structure and operation field contracts; no sample inference.

Literal labels use exact selected-definition/source comparisons. TEXT does not
authorize interpreting a label as a rule or inferring a relationship from it.
"""
from common import *

def definitions():
    occupancy_raw=(HERE/'occupancy-request-source.schema.json').read_bytes()
    if hashlib.sha256(occupancy_raw).hexdigest()!='69f08563ea4320ddfe03a64d042ce8e80a2fe0c3ee784d4ed05f81b37dfc34be':
        raise ValueError('Occupancy request source differs from reviewed PR57 R3 (unchanged from R2).')
    occupancy_request=json.loads(occupancy_raw)
    occupancy_request={k:v for k,v in occupancy_request.items() if k not in ['$schema','$id']}
    partial=source('03_machine_contracts/schemas/agronomic/OFARM_PartialExtent_schema_v0_1.json')
    quality=partial['$defs']['geometryBasis']['properties']['geometryQualityClass']['enum']
    extent_roles=partial['properties']['extentRole']['enum']
    continuity=['ONE_TO_ONE_PHYSICAL','SEGREGATED_MULTI_SOURCE','COMMINGLED_ACCOUNTED','NO_PHYSICAL_CONTINUITY_ASSERTED']
    d={
        'domainSubject':base_subject(),'contextBinding':base_context(),
        'typedBinding':typed_binding(),'partyBinding':typed_binding(['PARTY']),
        'bindingOrUnreported':binding_or_unreported(),
        'typedBindingOrUnreported':one(typed_binding(),unreported()),
        'bindingOrAbsent':one(BINDING,obj({'presence':const('ABSENT')})),
        'prospectiveCohort':obj({'proposalId':LOGICAL_REF,'materialIdentity':BINDING,'cohortBoundary':BINDING,'claimBasis':BINDING,'identityStatus':const('PROPOSED_NOT_CREATED')}),
        'successorProposal':one(obj({'presence':const('ABSENT')}),obj({'presence':const('PRESENT'),'prospectiveCohort':ref('prospectiveCohort'),'lineage':arr(BINDING,1,True)})),
        'occupancy':obj({'lot':BINDING,'start':TIMESTAMP,'end':TIMESTAMP},['lot','start']),
        'completeOccupancyEvidence':occupancy_request,
        'workSpecification':obj({'binding':BINDING,'activityInstance':BINDING,'procedure':BINDING,'target':typed_binding(),'extent':vref('extent'),
            'startConditionIds':arr(TEXT,1,True),'inProgressConditionIds':arr(TEXT,1,True),'finishConditionIds':arr(TEXT,1,True),'outputSpecification':BINDING},
            ['binding','activityInstance','procedure','target','extent','startConditionIds','inProgressConditionIds','finishConditionIds']),
        'overallWorkCoverage':obj({'posture':enum(['FULL_OVERALL_WORK','PARTIAL_OVERALL_WORK']),'overallWorkSpecification':BINDING}),
        'analyticalResult':one(obj({'kind':const('ABSENT_PENDING')}),obj({'kind':const('BOUND_RESULT'),'binding':BINDING})),
        'stageDisclosure':one(obj({'posture':const('NOT_REQUIRED_BY_BOUND_USE'),'basis':BINDING}),obj({'posture':const('STATED'),'stage':BINDING,'basis':BINDING}),obj({'posture':const('UNREPORTED'),'reason':TEXT,'basis':BINDING})),
        'receivedCondition':one(obj({'state':const('STATED'),'condition':BINDING}),unreported()),
        'residualMaterial':one(obj({'state':const('STATED'),'material':typed_binding(['LOT','INPUT']),'quantityParameterId':TEXT}),unreported()),
        'reportSelection':obj({'role':enum(['INTENDED_REPORT_OR_SELECTION','ACTUAL_REPORT']),'binding':BINDING}),
    }
    # Exact source field lists are checked by the builder. Selected optional
    # fields below are explicit meanings in typedFieldsAndOperators, not guessed
    # because a demonstration happened to contain or omit them.
    structures={
        'S01':{'property':const('scope.geometry'),'operator':const('EQUALS_BINDING'),'value':BINDING,'crs':BINDING,'geometryBasis':TEXT,'precision':enum(quality)},
        'S02':{'property':const('scope.governedParent'),'operator':const('RELATED_TO'),'parent':typed_binding(),'relation':const('GOVERNED_MEMBER_OF')},
        'S03':{'property':const('zone.configuration'),'family':TEXT,'purpose':BINDING,'recurring':const(True),'geometry':BINDING},
        'S04':{'property':const('cropCycle.configuration'),'attempt':BINDING,'crop':BINDING,'variety':BINDING,'scope':BINDING,'establishment':BINDING},
        'S05':{'property':const('facility.configuration'),'layout':BINDING,'storagePlaces':arr(BINDING,0,True),'containers':arr(BINDING,0,True)},
        'S06':{'property':const('lot.cohortBasis'),'cohort':BINDING,'traceabilityClaimBasis':BINDING,'physicalContinuityClass':enum(continuity)},
        'S07':{'property':const('input.identityConfiguration'),'identity':BINDING,'formulation':BINDING,'identifierRole':enum(['PRODUCT_OR_INPUT','ACTIVE_SUBSTANCE','GTIN','COMMERCIAL_REFERENCE','REGULATORY_REFERENCE']),'originalLabel':TEXT},
        'S08':{'property':const('operation.configuration'),'target':BINDING,'activity':TEXT,'method':BINDING,'assignedPerformer':BINDING,'resources':arr(BINDING,0,True)},
        'S09':{'property':const('identity.continuity'),'case':enum(['SAME_IDENTITY','REVISION_ONLY','SUCCESSOR_IDENTITIES']),'predecessors':arr(BINDING,1,True),'prospectiveSuccessors':arr(LOGICAL_REF,0,True),'existingSuccessors':arr(BINDING,1,True),'basis':TEXT,'lineageRelation':enum(['revises','replaces','splitFrom','mergedFrom','overlapsWith','succeeds','derivedFrom'])},
        'S10':{'property':const('identity.namedAttribute'),'attributeDefinition':TEXT,'identifierRole':enum(['COMMERCIAL_REFERENCE','REGULATORY_REFERENCE','GOVERNANCE_IDENTITY','PRODUCT_OR_INPUT','ACTIVE_SUBSTANCE','GTIN']),'scheme':BINDING,'value':TEXT,'originalLexicalValue':TEXT},
        'S11':{'property':const('scope.partialExtent'),'value':BINDING,'extentRole':enum(extent_roles),'parentScope':BINDING,'quality':enum(sorted(set(quality+['OPERATOR_SKETCH']))),'durableIdentityPosture':enum(['EVENT_BOUND','NO_NEW_CONSTITUTIONAL_IDENTITY','REUSES_EXISTING_SCOPE','CREATES_OR_REVISES_DURABLE_SCOPE','REVIEW_REQUIRED'])},
        'S12':{'property':const('asset.configuration'),'assetKind':enum(['EQUIPMENT','TOOL']),'asset':BINDING,'configuration':BINDING,'inspectionEvidence':arr(BINDING,0,True)},
        'S13':{'property':const('container.configuration'),'container':BINDING,'reusable':{'type':'boolean'},'occupancies':arr(ref('occupancy'),0,True),
               'occupancyEvidence':ref('completeOccupancyEvidence'),'occupancyClaimPosture':{**enum(['UNQUALIFIED_OCCUPANCY','UNQUALIFIED_EPISODES_DURING_WINDOW','QUALIFIED_SOURCE_HISTORY']),
                   '$comment':'UNQUALIFIED_OCCUPANCY requires each reported episode to support the full selected window. UNQUALIFIED_EPISODES_DURING_WINDOW asserts clean episode support only over each retained covered intersection; it does not assert occupancy throughout the window, continuity between episodes, or an exhaustive real-world inventory. QUALIFIED_SOURCE_HISTORY retains every original qualification without promoting it to an unqualified occupancy claim.'}},
        'S14':{'property':const('storageLocation.configuration'),'location':BINDING,'facility':BINDING,'layoutPosition':BINDING,'lineage':arr(BINDING,1,True)},
    }
    parameters={
        'O01':{'product':BINDING,'targetOrganism':BINDING,'method':BINDING,'rate':vref('quantityReference'),'applicationVolume':vref('quantityReference'),'overallWorkCoverage':ref('overallWorkCoverage')},
        'O02':{'fertilizer':BINDING,'nutrient':BINDING,'nutrientRate':vref('quantityReference'),'productRate':vref('quantityReference')},
        'O03':{'seedLot':BINDING,'crop':BINDING,'attempt':BINDING,'seedRate':vref('quantityReference'),'replantOf':ref('bindingOrAbsent')},
        'O04':{'waterVolume':vref('quantityReference'),'method':BINDING,'waterSource':BINDING},
        'O05':{'method':BINDING,'depth':vref('quantityReference'),'passes':{'type':'integer','minimum':1}},
        'O06':{'cropCycle':BINDING,'outputLots':arr(one(BINDING,ref('prospectiveCohort')),1,True),'harvestedMass':vref('quantityReference')},
        'O07':{'inputLot':BINDING,'method':BINDING,'targetMoisture':vref('quantityReference')},
        'O08':{'method':BINDING,'plantPart':BINDING,'workExtent':TEXT},
        'O09':{'observedProperty':BINDING,'method':BINDING,'observationContext':BINDING},
        'O10':{'specificActivity':const('SAMPLE_COLLECTION'),'sample':BINDING,'sampledProperty':BINDING,'samplingProcedure':BINDING,'analyticalResult':ref('analyticalResult'),'custodyPosture':enum(['COMPLETE','PARTIAL','UNKNOWN','DISPUTED']),'evidencePosture':enum(['REPORTED','NORMALIZED','DEGRADED_SUPPORT','REVIEW_REQUIRED','ACCEPTED_SUPPORT','SUPERSEDED','DISPUTED'])},
        'O11':{'specificActivity':const('LOT_SPLIT'),'predecessors':arr(BINDING,1,True),'successors':arr(one(BINDING,ref('prospectiveCohort')),2,True),'lineageRelation':const('splitFrom')},
        'O12':{'specificActivity':const('LOT_MERGE'),'predecessors':arr(BINDING,2,True),'successors':arr(one(BINDING,ref('prospectiveCohort')),1,True),'mixingPosture':const('GOVERNED_UNIFICATION')},
        'O13':{'specificActivity':const('LOT_COMMINGLE'),'predecessors':arr(BINDING,2,True),'successors':arr(one(BINDING,ref('prospectiveCohort')),1,True),'mixingPosture':const('PHYSICAL_MIX'),'claimBasisAfter':BINDING},
        'O14':{'specificActivity':const('LOT_TRANSFORM'),'inputLots':arr(BINDING,1,True),'outputLots':arr(one(BINDING,ref('prospectiveCohort')),1,True),'method':BINDING,'lineageRelation':const('derivedFrom')},
        'O15':{'specificActivity':const('LOT_MOVE_DISPATCH'),'lot':BINDING,'from':BINDING,'to':BINDING,'custodyChange':enum(['NO_CHANGE','CHANGE_ALLEGED','UNREPORTED']),'shipmentReference':TEXT,'movementPhase':enum(['MOVE','DISPATCH'])},
        'O16':{'specificActivity':const('REPORT_OPERATION_ALLEGATION'),'reportedClaim':BINDING,'reportedActivity':TEXT,'reportingChannel':BINDING},
        'O17':{'method':BINDING,'material':BINDING,'contactDuration':vref('quantityReference'),'sanitationKind':enum(['CLEANOUT','SANITIZE'])},
        'O18':{'method':BINDING,'asset':BINDING,'replacedPart':ref('bindingOrAbsent')},
        'O19':{'useType':const('SURFACE_AREA'),'profile':const('profile:si.ffs.recordkeeping.v0_1'),'product':BINDING,'capturedProductName':TEXT,'officialIdentity':BINDING,'useDate':DATE,'timeRelevance':enum(['SOURCE_RULE_REQUIRES_START_TIME','NOT_REQUIRED_BY_BOUND_USE','UNREPORTED']),'dose':vref('quantityReference'),'parcel':obj({'scheme':const('SI:GERK'),'binding':BINDING,'snapshot':BINDING}),'treatedArea':vref('quantityReference'),'crop':BINDING,'stage':ref('stageDisclosure'),'professionalUser':BINDING,'trainingEvidence':BINDING,'equipment':obj({'kind':enum(['EQUIPMENT','TOOL']),'binding':BINDING,'inspection':BINDING})},
        'O20':{'useType':const('CLOSED_SPACE'),'product':BINDING,'useDate':DATE,'dose':vref('quantityReference'),'treatedAmount':vref('quantityReference'),'batchIfApplicable':ref('bindingOrAbsent')},
        'O21':{'useType':const('SEED_TREATMENT'),'product':BINDING,'useDate':DATE,'dose':vref('quantityReference'),'treatedAmount':vref('quantityReference'),'batchIfApplicable':ref('bindingOrAbsent')},
        'O22':{'sample':BINDING,'property':BINDING,'method':BINDING,'producedResult':vref('analysisOutput')},
        'O23':{'report':ref('reportSelection'),'destinationContext':BINDING,'sourceSystem':BINDING},
        'O24':{'specificActivity':const('MATERIAL_RECEIPT'),'material':typed_binding(['LOT','INPUT']),'sender':ref('bindingOrUnreported'),'receiver':ref('bindingOrUnreported'),'origin':ref('typedBindingOrUnreported'),'destination':ref('typedBindingOrUnreported'),'deliveryReference':ref('bindingOrUnreported'),'receiptMethod':BINDING,'custodyPosture':enum(['PHYSICAL_RECEIPT_ONLY','CUSTODY_CHANGE_ALLEGED','UNREPORTED']),'titleTransferAlleged':{'type':'boolean'},'handledQuantity':vref('quantityReference'),'receivedCondition':ref('receivedCondition')},
        'O25':{'specificActivity':const('MATERIAL_RECLASSIFICATION'),'material':typed_binding(['LOT','INPUT']),'classificationScheme':BINDING,'fromClass':BINDING,'toClass':BINDING,'classificationBasis':BINDING,'method':BINDING,'identityDisposition':enum(['SAME_COHORT_CLASSIFICATION_ONLY','COHORT_OR_STRONG_BASIS_RESET']),'beforeClaimBasis':BINDING,'afterClaimBasis':BINDING,'successorProposal':ref('successorProposal'),'handledQuantity':vref('quantityReference')},
        'O26':{'specificActivity':const('MATERIAL_DISPOSAL'),'material':typed_binding(['LOT','INPUT']),'disposalMethod':BINDING,'destination':ref('typedBindingOrUnreported'),'disposalRoute':BINDING,'reason':BINDING,'residualDisposition':enum(['NO_USABLE_SUCCESSOR_ALLEGED','USABLE_SUCCESSOR_ALLEGED','UNREPORTED']),'disposalRecord':BINDING,'handledQuantity':vref('quantityReference'),'residualMaterial':ref('residualMaterial')},
        'O27':{'specificActivity':const('LOT_CREATION_ALLEGATION'),'prospectiveLot':ref('prospectiveCohort'),'originActivity':BINDING,'creationBasis':enum(['HARVEST_OUTPUT','SPLIT','MERGE','TRANSFORM','STRONG_BASIS_RESET','INITIAL_COHORT']),'predecessors':arr(BINDING,0,True),'lineageRelation':enum(['producedBy','splitFrom','mergedFrom','derivedFrom','succeeds']),'creationProcedure':BINDING,'creationEffectRequested':const(False),'handledQuantity':vref('quantityReference')},
    }
    return d,structures,parameters
