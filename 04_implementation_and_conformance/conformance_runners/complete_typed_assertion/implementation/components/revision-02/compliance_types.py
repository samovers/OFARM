"""Explicit compliance claim types and measured-role branches.

These describe assertions. External determinations, statutory calculations and
source roles keep their actual owner contracts; no new foreign record is made.
"""
from common import *

def definitions():
    execution=source('03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json')
    qualifiers=execution['properties']['actualQuantityParameters']['items']['properties']['qualifier']['enum']
    measurement=source('03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json')
    censoring=measurement['properties']['result']['properties']['censoringQualifier']['enum']
    outcomes=enum(['SATISFIED','NOT_SATISFIED','INDETERMINATE'])
    review=enum(['PENDING','WAIVED','FINAL','COURT_CHALLENGED','UNKNOWN'])
    pointer=vref('pointer');decimal=vref('decimal')
    # Preserve the actual reportedValue JSON type. A captured JSON number is
    # not reconstructed source text; its original bytes remain separately pinned.
    scalar_fields={'quantityKind':TEXT,'unit':TEXT,'decimal':decimal,'qualifier':enum(qualifiers),'originalLexicalValue':one({'type':'string'},{'type':'number'}),
        'unitProfile':BINDING,'originalUnitText':{'type':['string','null']},'normalized':vref('normalizedQuantity'),'provenance':ref('scalarProvenance')}
    scalar_required=['quantityKind','unit','decimal','qualifier','originalLexicalValue','unitProfile']
    d={
        'scalarProvenance':obj({'sourceBinding':BINDING,'valuePointer':pointer,'lexicalPointer':pointer,'qualifierPointer':pointer}),
        'complianceQuantity':obj(scalar_fields,scalar_required),
        'provenanceQuantity':obj(scalar_fields,scalar_required+['provenance']),
        'measurementSource':obj({'role':const('MEASURED_COMPLIANCE_OPERAND'),'measurementBinding':BINDING,'resultPointer':pointer,
            'contextBinding':BINDING,'subjectRelationBinding':BINDING,'methodUseBinding':BINDING,'qualificationPointers':arr(pointer,1,True)}),
        'measuredQualification':obj({'sourceBinding':BINDING,'sourcePointer':pointer,'methodUseBinding':BINDING,
            'interpretation':enum(['STATISTICAL_NOT_HARD_BOUND','METHOD_DEFINED_HARD_BOUND','SOURCE_QUALITY_ONLY','EXPLICIT_ESTIMATE','NOT_APPLICABLE_BY_BOUND_METHOD'])}),
        'intervalEndpoint':one(obj({'decimal':decimal,'inclusive':{'type':'boolean'}}),obj({'kind':const('UNBOUNDED')})),
        'admissibleValues':obj({'kind':const('INTERVAL'),'lower':ref('intervalEndpoint'),'upper':ref('intervalEndpoint'),'basis':TEXT}),
        'comparisonRange':obj({'lower':ref('complianceQuantity'),'upper':ref('complianceQuantity'),'lowerInclusive':{'type':'boolean'},'upperInclusive':{'type':'boolean'}}),
        'provenanceComparisonRange':obj({'lower':ref('provenanceQuantity'),'upper':ref('provenanceQuantity'),'lowerInclusive':{'type':'boolean'},'upperInclusive':{'type':'boolean'}}),
        'renewal':one(obj({'state':enum(['NOT_ESTABLISHED','NOT_REQUIRED'])}),obj({'state':const('EVIDENCED'),'binding':BINDING})),
        'holdingIdentifier':obj({'scheme':TEXT,'value':TEXT}),
        'historyEntry':obj({'year':{'type':'integer','minimum':1,'maximum':9999},'crop':BINDING,'cropCodeRevision':BINDING,'source':BINDING,'parcel':BINDING,'lineage':arr(BINDING,1,True)},['year','crop']),
        'profileEvaluationBasis':one(
            obj({'kind':const('PROFILE_OWNER_EVALUATION'),'binding':BINDING}),
            obj({'kind':const('AUTHORITY_DETERMINATION'),'binding':BINDING}),
            obj({'kind':const('CALCULATION_INPUTS'),'profileRevision':BINDING,'numerator':ref('complianceQuantity'),'denominator':ref('complianceQuantity'),'roundingRule':BINDING,'yearCodeCrosswalk':BINDING,'lineageAllocation':BINDING,'precedenceRule':BINDING}),
        ),
    }
    d['rateSource']=one(
        obj({'sourceKind':enum(['HUMAN_REPORT','OPERATION_PARAMETER']),'sourceBinding':BINDING,'valuePointer':pointer}),
        obj({'sourceKind':const('MEASUREMENT_EVIDENCE'),'sourceBinding':BINDING,'valuePointer':pointer,'measurementSource':ref('measurementSource')}),
    )
    # Each source result kind remains distinct. Mapping from coded/qualitative
    # data or quantified uncertainty requires explicit independently selected
    # method-use facts; writing a mapping binding here cannot establish them.
    censored=obj({'resultKind':const('CENSORED_NUMERIC'),'qualifier':enum(censoring),'limit':ref('provenanceQuantity'),
        'nonnegative':{'type':'boolean'},'source':ref('measurementSource'),'admissibleValues':ref('admissibleValues')})
    numeric=obj({'resultKind':const('NUMERIC'),'quantity':ref('complianceQuantity'),'source':ref('measurementSource'),'admissibleValues':ref('admissibleValues')})
    coded=obj({'resultKind':const('CODED'),'codedValue':BINDING,'source':ref('measurementSource'),'mappingBinding':BINDING,'admissibleValues':ref('admissibleValues')})
    qualitative=obj({'resultKind':const('QUALITATIVE'),'originalText':TEXT,'scaleBinding':BINDING,'source':ref('measurementSource'),'mappingBinding':BINDING,'admissibleValues':ref('admissibleValues')})
    pending=obj({'resultKind':const('ABSENT_PENDING'),'source':ref('measurementSource'),'reason':TEXT})
    d['criterionOperand']=one(censored,numeric,coded,qualitative,pending)
    fields={
        'C01':{'form':const('RELEVANCE'),'rule':BINDING,'basis':BINDING,'relevanceRole':TEXT},
        'C02':{'form':const('APPLICABILITY'),'rule':BINDING,'jurisdiction':{'type':'string','pattern':'^[A-Z]{2}$(?![\\s\\S])'},'crop':BINDING,'use':BINDING,'assertedApplicability':enum(['APPLIES','DOES_NOT_APPLY','INDETERMINATE'])},
        'C03':{'form':const('CRITERION_OUTCOME'),'criterion':BINDING,'measurement':BINDING,'operandPointer':pointer,'operator':enum(['LT','LE','EQ','GE','GT','BETWEEN']),
            'threshold':one(ref('complianceQuantity'),ref('comparisonRange')),'allegedOutcome':outcomes,'measurementSource':ref('measurementSource'),'measuredQualification':ref('measuredQualification')},
        'C04':{'form':const('CRITERION_OUTCOME'),'criterion':BINDING,'operand':ref('criterionOperand'),'operator':enum(['LT','LE','GE','GT','BETWEEN']),
            'threshold':one(ref('provenanceQuantity'),ref('provenanceComparisonRange')),'allegedOutcome':outcomes,'measuredQualification':ref('measuredQualification')},
        'C05':{'form':const('PROFILE_CRITERION_OUTCOME'),'profile':BINDING,'jurisdiction':const('BE'),'officialIdentifier':TEXT,'verificationTrace':BINDING,'snapshots':arr(BINDING,1,True),'allegedOutcome':outcomes},
        'C06':{'form':const('CRITERION_OUTCOME'),'condition':BINDING,'product':BINDING,'crop':BINDING,'target':BINDING,'rate':ref('complianceQuantity'),'operator':enum(['LT','LE','EQ','GE','GT','BETWEEN']),
            'boundFrom':BINDING,'allegedOutcome':outcomes,'rateSource':ref('rateSource'),'measuredQualification':ref('measuredQualification')},
        'C07':{'form':const('MODEL_AND_CRITERION'),'basis':BINDING,'model':enum(['IDENTITY_PRESERVED','SEGREGATED','MASS_BALANCE','BOOK_AND_CLAIM','DECLARED_OTHER']),
            'continuityClass':enum(['ONE_TO_ONE_PHYSICAL','SEGREGATED_MULTI_SOURCE','COMMINGLED_ACCOUNTED','NO_PHYSICAL_CONTINUITY_ASSERTED']),'criterion':BINDING,'allegedOutcome':outcomes},
        'C08':{'form':const('DETERMINATION_REPORT'),'decision':BINDING,'rule':BINDING,'finding':TEXT,'subject':BINDING},
        'C09':{'form':const('CHARTER_CRITERION_OUTCOME'),'charter':BINDING,'metric':BINDING,'evidencePosture':enum(['MEASURED','MODELLED','ESTIMATED','DISPUTED']),
            'claimBasis':BINDING,'allegedOutcome':outcomes,'measurementSource':ref('measurementSource'),'measuredQualification':ref('measuredQualification')},
        'C10':{'form':const('EVIDENCE_POLICY_OUTCOME'),'policy':BINDING,'requiredUse':TEXT,'evidenceSet':arr(BINDING,0,True),'missingKinds':arr(TEXT,0,True),'allegedOutcome':enum(['SUFFICIENT','INSUFFICIENT','INDETERMINATE'])},
        'C11':{'form':const('PROFILE_STATUS'),'profile':const('profile:rs.organic-crop.farm-reg-cert.v0_1'),'holding':BINDING,'holdingIdentifier':ref('holdingIdentifier'),
            'statusKind':enum(['REGISTRATION','ACTIVE_PASSIVE','SUBMISSION','RENEWAL']),'allegedStatus':enum(['REGISTERED','NOT_REGISTERED','ACTIVE','PASSIVE','SUBMITTED','NOT_SUBMITTED','RENEWED','NOT_RENEWED','UNKNOWN']),
            'statusDate':DATE,'officialArtefact':BINDING,'renewal':ref('renewal'),'reviewState':review},
        'C12':{'form':const('PROFILE_CERTIFICATE_STATUS'),'profile':const('profile:rs.organic-crop.farm-reg-cert.v0_1'),'certificate':BINDING,'certificateSubject':typed_binding(['PARTY','FARM']),
            'holding':BINDING,'validFrom':TIMESTAMP,'validUntil':TIMESTAMP,'category':BINDING,'issuer':typed_binding(['PARTY']),'adverseStatus':enum(['NONE_REPORTED','SUSPENDED','WITHDRAWN','EXPIRED','UNKNOWN']),
            'ministrySnapshot':BINDING,'accreditationSnapshot':BINDING,'reviewState':review},
        'C13':{'form':const('AUTHORITY_REFERENCE_REPORT'),'profile':const('profile:rs.organic-crop.farm-reg-cert.v0_1'),'certifier':typed_binding(['PARTY']),'ministrySnapshot':BINDING,'accreditationSnapshot':BINDING,
            'scope':BINDING,'at':TIMESTAMP,'reportedStatus':enum(['ACTIVE','NOT_LISTED','SUSPENDED','WITHDRAWN','EXPIRED','UNKNOWN'])},
        'C14':{'form':const('DETERMINATION_REPORT'),'profile':const('profile:rs.organic-crop.farm-reg-cert.v0_1'),'challengedAct':BINDING,'reviewArtefact':BINDING,'serviceProof':BINDING,'authorityAddressed':BINDING,'reviewState':review},
        'C15':{'form':const('PROFILE_HISTORY'),'profile':const('profile:nl.go-glmc7.2026.v0_1'),'claimYear':const(2026),'scopeDate':const('2026-05-15'),'filedGO':BINDING,
            'holding':BINDING,'parcel':BINDING,'parcelSnapshot':BINDING,'cropCodes':BINDING,'history':arr(ref('historyEntry'),1,True),'lineage':arr(BINDING,1,True)},
        'C16':{'form':const('PROFILE_ROUTE_OUTCOME'),'profile':const('profile:nl.go-glmc7.2026.v0_1'),'claimYear':const(2026),'route':TEXT,'routeScope':enum(['PARCEL','HOLDING']),
            'parcel':BINDING,'historyClaim':BINDING,'soilCategory':enum(['SAND_OR_LOESS','OTHER','UNKNOWN']),'soilEvidence':BINDING,'rustgewasEvidence':BINDING,'routeEvidence':BINDING,
            'evaluationBasis':ref('profileEvaluationBasis'),'allegedOutcome':outcomes,'reviewState':review},
        'C17':{'form':const('RECORD_COMPLETENESS'),'profile':const('profile:si.ffs.recordkeeping.v0_1'),'record':BINDING,'useType':enum(['SURFACE_AREA','CLOSED_SPACE','SEED_TREATMENT']),
            'requirementsRevision':BINDING,'allegedOutcome':enum(['COMPLETE_FOR_RECORDKEEPING','INCOMPLETE_FOR_RECORDKEEPING','INDETERMINATE']),'lawfulUseAlleged':const(False)},
    }
    return d,fields
