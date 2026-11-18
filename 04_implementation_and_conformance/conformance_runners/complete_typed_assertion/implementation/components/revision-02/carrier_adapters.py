"""Fixed domain comparisons against real source carrier schemas.

A selected record is still subject to the coordinator's exact resolution and
owner-eligibility checks. This module supplies deterministic source comparisons,
not a generic policy interpreter, an evidence producer or an admission verdict.
"""
from common import *
from common import source as pinned_source
def source_file(pin):return pinned_source(pin['originalPath'],pin['commit'],pin['repository'])
from runtime_support import Schemas,Values,exact,instant,error,pointer,sealed
from intrinsics import Intrinsics,time_bounds
from time_validation import foreign_seconds
from build_canonical_inputs import CANONICAL_ID,IDS,ID_FIELDS,PROJECTIONS

ACTIVITIES={'plant':'O03','till':'O05','fertilize':'O02','spray':'O01','irrigate':'O04','prune':'O08','harvest':'O06','cleanout':'O17','sanitize':'O17','maintain':'O18','create-lot':'O27','split-lot':'O11','merge-lots':'O12','move-material':'O15','dispatch':'O15','receive':'O24','reclassify-material':'O25','dispose-material':'O26'}

class CanonicalAdapters:
    def __init__(self):
        self.schemas=Schemas();self.values=Values(self.schemas)
        self.rows={r['id']:r for r in reviewed('reviewed-input/canonical/inventory.json')['rows']}
    def check(self,row,data):
        if row not in self.rows:return {'errors':[error('UNKNOWN_CANONICAL_ROW','/row')],'disposition':'COMPARISON_FAILED'}
        errors=self.schemas.errors(CANONICAL_ID,data,row)
        if errors:return self.result(row,errors,[],[],[])
        comparisons=[];bindings=[];requirements=[]
        def compare(code,actual,expected,path):
            equal=exact(actual,expected);comparisons.append({'pointer':path,'comparison':code,'equal':equal})
            if not equal:errors.append(error(code,path))
        def require(code,path):requirements.append({'role':code,'pointer':path})
        def source(name,key=None):
            key=key or name;entry=data[key];record=entry['record'];binding=entry['binding'];bindings.append({'binding':binding,'schemaId':IDS[name],'pointer':'/'+key})
            compare('SOURCE_ID_BINDING_MISMATCH',record.get(ID_FIELDS[name]),binding['ref'],'/'+key+'/record/'+ID_FIELDS[name])
            require('EXACT_IMMUTABLE_SOURCE_RESOLUTION','/'+key+'/binding')
            return record
        def project(record,name,claimed,path):
            fields=PROJECTIONS[name][1];actual={k:record[k] for k in fields if k in record}
            compare('SOURCE_PROJECTION_CHANGED',actual,claimed,path)
        def endpoint(actual,endpoint,path,style='subject'):
            expected={'subjectType':endpoint['kind'],'subjectRef':endpoint['binding']['ref']} if style=='subject' else {'scopeType':endpoint['kind'],'scopeRef':endpoint['binding']['ref']}
            compare('TYPED_ENDPOINT_MISMATCH',actual,expected,path)
            require('ENDPOINT_IMMUTABLE_VERSION_AND_KIND',path)
        def cover(start,end,t,path):
            try:
                lo=foreign_seconds(t.get('at',t.get('start')));hi=foreign_seconds(t['end']) if 'end' in t else lo if 'at' in t else None;a=foreign_seconds(start);z=foreign_seconds(end) if end is not None else None
                if z is not None and a>=z:errors.append(error('EMPTY_SOURCE_INTERVAL',path))
                if a>lo or (hi is None and z is not None) or (z is not None and (hi or lo)>z):errors.append(error('SOURCE_INTERVAL_DOES_NOT_COVER_CLAIM',path))
            except (ValueError,TypeError):errors.append(error('INVALID_OR_MISSING_SOURCE_TIME',path))
        def temporal(record,t,path):
            kind=record.get('timeType')
            if kind in ['INSTANT','AS_OF']:
                if 'at' not in t:errors.append(error('INSTANT_SOURCE_CANNOT_COVER_INTERVAL',path))
                else:compare('SOURCE_TIME_MISMATCH',record.get('instant'),t['at'],path+'/instant')
            elif kind in ['INTERVAL','OPEN_INTERVAL']:
                if kind=='INTERVAL' and 'intervalEnd' not in record:errors.append(error('MISSING_SOURCE_INTERVAL_END',path))
                cover(record.get('intervalStart'),record.get('intervalEnd'),t,path)
            else:errors.append(error('SOURCE_TIME_TYPE_UNSUPPORTED',path+'/timeType'))
        def measurement_context():
            m=source('measurement');c=source('context');project(m,'measurementMeaning',data['measurementProjection'],'/measurementProjection');project(c,'contextMeaning',data['contextProjection'],'/contextProjection')
            compare('OBSERVED_PROPERTY_MISMATCH',m['observedPropertyRef'],c['observedPropertyRef'],'/context/record/observedPropertyRef')
            if 'agronomicObservationContextRef' in m:compare('MEASUREMENT_CONTEXT_LINK_MISMATCH',m['agronomicObservationContextRef'],c['agronomicObservationContextId'],'/measurement/record/agronomicObservationContextRef')
            elif m['measurementEvidenceId'] not in c.get('measurementEvidenceRefs',[]):errors.append(error('NO_MEASUREMENT_CONTEXT_LINK','/context/record/measurementEvidenceRefs'))
            if c['subject']['subjectType']=='SAMPLE':compare('SAMPLE_CONTEXT_LINK_MISMATCH',m.get('sampleRef'),c['subject']['subjectRef'],'/context/record/subject')
            require('PROPERTY_METHOD_CONTEXT_AND_ELIGIBLE_USE','/measurementProjection')
            return m,c
        if 'subjectTime' in data:errors.extend({**e,'pointer':'/subjectTime'+e['pointer']} for e in self.values.time_errors(data['subjectTime']))
        if row.startswith('V04-') and row not in ['V04-action-families','V04-profiles']:
            e=source('event');selected=data['selectedMeaning'];compare('SELECTED_COMPLETE_MEANING_MISMATCH',data['claimedMeaning'],selected,'/claimedMeaning')
            errors.extend(sealed.event_literal_errors(selected,e,selected['family']))
            errors.extend(self.values.event_time_errors(data['subjectTime'],e,selected['timeSelector']))
            if row!='V04-extension':
                r=self.rows[row];case=r['typedRepresentation']['eventMeaningCase']
                if selected['subtypePresence']=='ABSENT':case=r.get('subtypeAbsentVariant',{})
                for field in ['subtypePresence','eventSubtypeId','dominantSemanticConsequence','concept']:
                    compare('CANONICAL_MEANING_CASE_MISMATCH',selected.get(field),case.get(field),'/selectedMeaning/'+field)
                if 'primaryFamilyFromSource' in case:compare('CANONICAL_FAMILY_MISMATCH',selected['family'],case['primaryFamilyFromSource'],'/selectedMeaning/family')
                elif row in ['V04-prune','V04-spray']:
                    fragment='OFARM_SemanticEventEnvelope_example_pruning_operation' if row=='V04-prune' else 'OFARM_SemanticEventEnvelope_example_field_17_contractor_spot_spray_late_sync'
                    pin=next(p for p in json.loads((HERE/'source-pins.json').read_text())['sources'] if fragment in p['originalPath'])
                    original=source_file(pin)
                    compare('CANONICAL_FAMILY_MISMATCH',selected['family'],original['primaryEventFamily'],'/selectedMeaning/family')
                if 'sourcePackRef' in case:compare('CANONICAL_PACK_MISMATCH',selected['packBinding']['ref'],case['sourcePackRef'],'/selectedMeaning/packBinding/ref')
                perspective=r['typedRepresentation'].get('perspective')
                if perspective:
                    expected=['/timeSemantics/effectiveFrom','/timeSemantics/effectiveUntil'] if perspective=='interval' else '/timeSemantics/'+perspective
                    compare('CASE_TIME_PERSPECTIVE_MISMATCH',selected['timeSelector'],expected,'/selectedMeaning/timeSelector')
            for key,field in [('selectedSubject','subjectRefs'),('selectedAnchor','anchorScopes')]:
                indices=[i for i,v in enumerate(e[field]) if exact(v,data[key])]
                if not indices:
                    if field=='subjectRefs':require('EXACT_EVENT_SUBJECT_RELATION','/'+key)
                    else:errors.append(error('EVENT_ANCHOR_PAIR_NOT_PRESENT','/'+key))
                else:comparisons.append({'pointer':'/event/record/'+field+'/'+str(indices[0]),'comparison':'LOWEST_EXACT_INDEX','index':indices[0]})
            for role in ['PRE_VERDICT_EVENT_CLASSIFICATION','IMMUTABLE_MEANING_PACKAGE_AND_VOCABULARY','COMPLETE_BODY_EVENT_PAYLOAD_COMPARISONS']:require(role,'/selectedMeaning')
        elif row=='V04-action-families':
            atom=data['atom'];expected=ACTIVITIES[data['activityConcept']];actual=atom['definition'].removeprefix(DEFINITION_PREFIX)
            if data['activityConcept']=='spray' and actual=='O19':expected='O19'
            compare('ACTIVITY_ROW_MISMATCH',actual,expected,'/atom/definition')
            if data['activityConcept'] in ['move-material','dispatch']:
                compare('MATERIAL_MOVEMENT_PHASE_MISMATCH',atom['body'].get('parameters',{}).get('movementPhase'),'MOVE' if data['activityConcept']=='move-material' else 'DISPATCH','/atom/body/parameters/movementPhase')
            if data['activityConcept'] in ['cleanout','sanitize']:compare('SANITATION_ACT_MISMATCH',atom['body'].get('parameters',{}).get('sanitationKind'),data['activityConcept'].upper(),'/atom/body/parameters/sanitationKind')
            errors.extend(Intrinsics().check(atom)['errors']);require('EXACT_COMPLETE_EVENT_CASE_FOR_ACTIVITY','/atom')
        elif row=='V04-profiles':
            if data['eventPresence']=='PRESENT':errors.extend(self.values.event_time_errors(data['subjectTime'],source('event'),data['selectedTimeSelector']));require('COMPLETE_EVENT_CASE_AND_INGRESS','/event')
            # Event absence never removes the independent measurement time gate.
            if data['subjectTime']['profile']=='PERFORMED_INSTANT':require('COMPATIBLE_MEASUREMENT_PHENOMENON_INSTANT','/subjectTime')
        elif row.startswith('V05-time-'):
            m=source('measurement');project(m,'measurementMeaning',data['projection'],'/projection');qualifier=self.rows[row]['typedRepresentation']['foreignQualifier']
            errors.extend(self.values.measured_instant_errors(m,data['subjectTime'],qualifier))
            require('EXACT_METHOD_USE_ROLE_AND_QUALIFIER_INTERPRETATION','/methodUseBinding')
        elif row.startswith('V05-result-'):
            m=source('measurement');project(m,'measurementMeaning',data['projection'],'/projection')
            compare('MEASUREMENT_RESULT_BRANCH_MISMATCH',m['result']['resultKind'],self.rows[row]['typedRepresentation']['resultUnionBranch'],'/measurement/record/result/resultKind')
            errors.extend(self.values.measurement_result_errors(m['result'],data['claimedResult']));require('RESULT_PROPERTY_METHOD_AND_ELIGIBLE_USE','/methodUseBinding')
        elif row.startswith('V05-source-'):
            m=source('measurement');project(m,'measurementMeaning',data['projection'],'/projection')
            # These four definitions deliberately reference named historical
            # source records; the exact complete record is retained as a case.
            compare('NAMED_SOURCE_RECORD_CHANGED',m,self.rows[row]['typedRepresentation']['sourceRecord'],'/measurement/record')
            require('SOURCE_SPECIFIC_USE_NOT_OPERATION_EQUIVALENCE','/projection')
        elif row=='V05-context':measurement_context()
        elif row=='V05-code-bindings':
            c=source('code');p=source('codeProfile',key='profile');project(c,'codeMeaning',data['codeProjection'],'/codeProjection');compare('CODE_ROLE_MISMATCH',c['bindingRole'],data['selectedRole'],'/code/record/bindingRole')
            if p['agronomicCodeBindingProfileId'] not in c.get('profileRefs',[]):errors.append(error('CODE_PROFILE_LINK_MISSING','/code/record/profileRefs'))
            require('EXTERNAL_SCHEME_CURRENTNESS_AND_ROLE_USE','/codeProjection')
        elif row=='V06-operation-target':
            e=source('event');x=source('execution');project(x,'operationTarget',data['projection'],'/projection')
            compare('OPERATION_ENDPOINT_KIND',data['from']['kind'],'OPERATION','/from/kind');endpoint(x['subject'],data['from'],'/execution/record/subject');endpoint(x['executionExtent']['targetScope'],data['to'],'/execution/record/executionExtent/targetScope','scope')
            if x['executionRecordPayloadId'] not in e.get('executionRecordPayloadRefs',[]):errors.append(error('EVENT_EXECUTION_LINK_MISSING','/event/record/executionRecordPayloadRefs'))
            if 'sourceEventRef' in x:compare('EXECUTION_EVENT_LINK_MISMATCH',x['sourceEventRef'],e['semanticEventId'],'/execution/record/sourceEventRef')
            cover(x['effectiveTimeInterval']['start'],x['effectiveTimeInterval']['end'],data['subjectTime'],'/execution/record/effectiveTimeInterval');require('EXECUTION_ROLE_AND_EXTENT_ELIGIBILITY','/execution')
        elif row in ['V06-sample-target','V06-report-about']:
            m,c=measurement_context()
            if row=='V06-sample-target':compare('SAMPLE_ENDPOINT_KIND',data['from']['kind'],'SAMPLE','/from/kind');compare('SAMPLE_REF_MISMATCH',m.get('sampleRef'),data['from']['binding']['ref'],'/measurement/record/sampleRef')
            else:
                if data['from']['kind'] not in ['DOCUMENT']:errors.append(error('DOCUMENT_ENDPOINT_KIND','/from/kind'))
                if data['from']['binding']['ref'] not in [m['source'].get('sourceRef'),m.get('originalPayloadRef')]:errors.append(error('REPORT_LINK_MISSING','/measurement/record/source/sourceRef'))
            if 'targetScope' not in c:errors.append(error('CONTEXT_TARGET_SCOPE_MISSING','/context/record/targetScope'))
            else:endpoint(c['targetScope'],data['to'],'/context/record/targetScope','scope')
            temporal(c['phenomenonTime'],data['subjectTime'],'/context/record/phenomenonTime')
            if 'partialExtentRef' in c['spatialContext']:
                if 'extent' not in data or 'extentProjection' not in data:errors.append(error('PARTIAL_EXTENT_SOURCE_REQUIRED','/extent'))
                else:
                    p=source('extent');project(p,'extentMeaning',data['extentProjection'],'/extentProjection');compare('CONTEXT_EXTENT_LINK_MISMATCH',c['spatialContext']['partialExtentRef'],p['partialExtentId'],'/context/record/spatialContext/partialExtentRef');endpoint(p['parentScope'],data['to'],'/extent/record/parentScope','scope');temporal(p['temporalApplicability'],data['subjectTime'],'/extent/record/temporalApplicability')
            elif 'extent' in data:errors.append(error('UNLINKED_EXTENT_SOURCE','/extent'))
        elif row=='V06-extent':
            p=source('extent');project(p,'extentMeaning',data['projection'],'/projection');compare('EXTENT_ENDPOINT_KIND',data['from']['kind'],'PARTIAL_EXTENT','/from/kind');compare('EXTENT_REF_MISMATCH',p['partialExtentId'],data['from']['binding']['ref'],'/from/binding/ref');endpoint(p['parentScope'],data['to'],'/extent/record/parentScope','scope');temporal(p['temporalApplicability'],data['subjectTime'],'/extent/record/temporalApplicability');require('EXTENT_GEOMETRY_AND_DURABLE_POSTURE_USE','/projection')
        elif row=='V06-decision-applies':
            d=source('decision');project(d,'decisionMeaning',data['projection'],'/projection');compare('DECISION_SOURCE_REF_MISMATCH',d['reviewDecisionId'],data['from']['binding']['ref'],'/from/binding/ref');compare('REVIEWED_ARTIFACT_REF_MISMATCH',d['reviewedArtifactRef'],data['reviewedArtifactBinding']['ref'],'/reviewedArtifactBinding/ref');require('REVIEWED_ARTIFACT_TO_EXACT_SUBJECT','/artifactSubjectRelationBindings');require('DECISION_FINDING_AND_IN_FORCE_EFFECT','/projection')
        elif row=='V06-lineage':
            d=source('lineage');project(d,'lineageMeaning',data['projection'],'/projection');relation={'fromRef':data['from']['binding']['ref'],'toRef':data['to']['binding']['ref'],'relationType':data['relationType']}
            if not any(exact(r,relation) for r in d['lineageRelations']):errors.append(error('DIRECTED_LINEAGE_EDGE_MISSING','/lineage/record/lineageRelations'))
            for end in ['from','to']:
                compare('LINEAGE_ENDPOINT_FAMILY_MISMATCH',data[end]['kind'],d['subjectFamily'],'/'+end+'/kind')
                if data[end]['binding']['ref'] not in d['oldIdentityRefs']+d['newIdentityRefs']:errors.append(error('LINEAGE_IDENTITY_NOT_LISTED','/'+end+'/binding/ref'))
            if 'effectiveFrom' not in d:require('LINEAGE_EFFECTIVE_TIME_SOURCE','/lineage/record/effectiveFrom')
            else:cover(d['effectiveFrom'],None,data['subjectTime'],'/lineage/record/effectiveFrom')
            require('LIFECYCLE_CONTINUITY_AND_REVISION_IDENTITY','/projection')
        elif row=='V06-equipment-use':
            x=source('execution');i=source('equipment',key='equipmentIdentity');project(x,'equipmentUse',data['projection'],'/projection');project(i,'equipmentIdentity',data['identityProjection'],'/identityProjection')
            if data['from']['kind'] not in ['EQUIPMENT','TOOL']:errors.append(error('ASSET_ENDPOINT_KIND','/from/kind'))
            compare('EQUIPMENT_ROLE_REF_MISMATCH',x.get('equipment',{}).get(data['equipmentRole']),data['from']['binding']['ref'],'/execution/record/equipment/'+data['equipmentRole']);compare('EQUIPMENT_IDENTITY_MISMATCH',i['identityRecordRef'],data['from']['binding']['ref'],'/equipmentIdentity/record/identityRecordRef');endpoint(x['subject'],data['to'],'/execution/record/subject');cover(x['effectiveTimeInterval']['start'],x['effectiveTimeInterval']['end'],data['subjectTime'],'/execution/record/effectiveTimeInterval');require('ASSET_CONFIGURATION_AND_INSPECTION_RECONCILIATION','/identityProjection')
        elif row=='V06-occupancy':
            d=source('lineage',key='lifecycle');compare('OCCUPANCY_CHANGE_KIND',d['changeKind'],'OCCUPANCY_EPISODE','/lifecycle/record/changeKind')
            if data['from']['kind'] not in ['LOT','INPUT'] or data['to']['kind'] not in ['CONTAINER','STORAGE_LOCATION','FACILITY']:errors.append(error('OCCUPANCY_ENDPOINT_KIND','/from'))
            cover(data['occupancyStart'],data['occupancyEnd'],data['subjectTime'],'/occupancyStart');require('OCCUPANCY_ENDPOINT_INTERVAL_CARRIER','/lifecycle')
        elif row=='V06-party-context':
            kind=data['carrierKind'];d=source(kind);project(d,{'party':'partyMeaning','responsibility':'responsibilityMeaning','commitment':'commitmentMeaning'}[kind],data['projection'],'/projection')
            if kind=='party':
                if data['from']['kind']!='PARTY' or data['to']['kind']!='PARTY':errors.append(error('PARTY_ENDPOINT_KIND','/from'))
                a,b=d['partyARef'],d['partyBRef'];direction=d['relationshipDirectionality'];pair=(data['from']['binding']['ref'],data['to']['binding']['ref'])
                accepted=[(a,b)] if direction=='PARTY_A_TO_PARTY_B' else [(b,a)] if direction=='PARTY_B_TO_PARTY_A' else [(a,b),(b,a)] if direction=='MUTUAL' else []
                if pair not in accepted:errors.append(error('DIRECTED_PARTY_RELATION_MISMATCH','/party/record/relationshipDirectionality'))
            elif kind=='responsibility':
                compare('PARTY_ENDPOINT_KIND',data['from']['kind'],'PARTY','/from/kind');compare('RESPONSIBILITY_PARTY_MISMATCH',d['partyRef'],data['from']['binding']['ref'],'/responsibility/record/partyRef');endpoint(d['targetScope'],data['to'],'/responsibility/record/targetScope','scope')
            else:
                if data['from']['binding']['ref'] not in d.get('linkedPartyRefs',[]):errors.append(error('COMMITMENT_PARTY_LINK_MISSING','/commitment/record/linkedPartyRefs'))
                expected={'scopeType':data['to']['kind'],'scopeRef':data['to']['binding']['ref']}
                if not any(exact(v,expected) for v in d.get('linkedScopes',[])):errors.append(error('COMMITMENT_SCOPE_LINK_MISSING','/commitment/record/linkedScopes'))
            if 'validFrom' in d:cover(d['validFrom'],d.get('validUntil'),data['subjectTime'],'/'+kind+'/record/validFrom')
            else:require('RELATION_APPLICABILITY_TIME_SOURCE','/'+kind+'/record')
            require('RELATION_STATE_AND_SELECTED_USE_ELIGIBILITY','/projection')
        elif row=='V06-parent-scope':
            kind=data['carrierKind'];d=source(kind);project(d,'fieldParent' if kind=='field' else 'cycleParent',data['projection'],'/projection');compare('CHILD_IDENTITY_MISMATCH',d['identityRecordRef'],data['from']['binding']['ref'],'/'+kind+'/record/identityRecordRef');compare('CHILD_KIND_MISMATCH',data['from']['kind'],'FIELD' if kind=='field' else 'CROP_CYCLE','/from/kind')
            if kind=='field':compare('PARENT_KIND_MISMATCH',data['to']['kind'],'FARM','/to/kind');compare('PARENT_REF_MISMATCH',d['parentFarmIdentityRef'],data['to']['binding']['ref'],'/field/record/parentFarmIdentityRef');require('FIELD_PARENT_RELATION_TIME_APPLICABILITY','/field')
            else:
                if data['to']['binding']['ref'] not in d['parentScopeRefs']:errors.append(error('CYCLE_PARENT_REF_MISSING','/cycle/record/parentScopeRefs'))
                if 'startedAt' in d:cover(d['startedAt'],d.get('endedAt'),data['subjectTime'],'/cycle/record/startedAt')
                else:require('CROP_CYCLE_TIME_APPLICABILITY','/cycle/record/startedAt')
            require('PARENT_IMMUTABLE_IDENTITY_KIND_AND_RELATION_USE','/projection')
        elif row=='V06-endpoints':require('SUBJECT_CONTEXT_ENDPOINT_RESOLUTION_WITHOUT_ANCHOR_WIDENING','/subject')
        elif row=='V06-proof-interface':require('EXISTING_OWNER_PROOF_RESOLUTION_AND_SEMANTIC_PROJECTION','/subjectScopeProofBindings')
        return self.result(row,errors,comparisons,bindings,requirements)
    @staticmethod
    def result(row,errors,comparisons,bindings,requirements):
        return {'row':row,'scope':'FIXED_DOMAIN_SOURCE_COMPARISONS_ONLY','disposition':'COMPARISON_FAILED' if errors else 'COMPARISONS_SATISFIED_WITH_OWNER_ROLES_REQUIRED',
            'errors':errors,'comparisons':comparisons,'sourceBindings':bindings,'requiredOwnerRoles':requirements}
