"""Copy exact read-only Git sources into the private construction revision."""
import argparse,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
HEAD='389a8f6b6bb2f43435c35f32df769e723d736856'
PACKET='package_meta/history/clean_baseline_migration/phase_reports/domain_contract_verifier_delivery_v0_1'

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo-root',type=Path,required=True);p.add_argument('--implementation-root',type=Path,required=True);a=p.parse_args()
    roots={'samovers/OFARM':a.repo_root.resolve(),'samovers/OFARM2':a.implementation_root.resolve()};records=[]
    def capture(repo,commit,path,sha=None,identity=None):
        raw=subprocess.check_output(['git','show',commit+':'+path],cwd=roots[repo]);digest=hashlib.sha256(raw).hexdigest()
        if sha is not None and digest!=sha:raise ValueError('Source hash mismatch: '+path)
        relative='sources/'+repo.rsplit('/',1)[-1]+'/'+commit[:12]+'/'+path;dest=HERE/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        records.append({'id':identity,'repository':repo,'commit':commit,'originalPath':path,'localPath':relative,'sha256':digest,'bytes':len(raw)})
        return json.loads(raw) if path.endswith('.json') else raw
    files=['reviewed-input/domain/inventory.json','reviewed-input/domain/requirements.json','reviewed-input/domain/atom-contract.json','reviewed-input/domain/quantity-contract.json','reviewed-input/domain/operation-profile-contract.json','reviewed-input/domain/work-condition-definitions.json','reviewed-input/domain/occurrence-definitions.json','reviewed-input/domain/sources.json','reviewed-input/canonical/inventory.json','reviewed-input/canonical/source-map.json','review-amendment-03/candidate-examples-v4.json','review-amendment-03/evidence-selectors-v4.json','review-amendment-03/measurement-role-contract-v4.json','review-amendment-02/compliance-role-cases-v3.json']
    content={name:capture('samovers/OFARM',HEAD,PACKET+'/'+name) for name in files}
    original_sources=content['reviewed-input/domain/sources.json']['sources']
    for row in content['reviewed-input/canonical/inventory.json']['rows']:original_sources+=row['sourceBindings']
    seen=set()
    for source in original_sources:
        key=(source['repository'],source['commit'],source['path'])
        if key in seen:continue
        seen.add(key);capture(*key,sha=source['sha256'],identity=source['id'])
    # The current consumer schemas are independently pinned at the source head.
    current=['04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_EvidenceSufficiencyCase_example_qualified_lab_result_support_v0_2.json',
        '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_ExternalRegistryVerificationTrace_example_be_phytoweb_authorisation_pass_v0_1.json',
        '03_machine_contracts/schemas/core/OFARM_TraceabilityClaimBasis_schema_v0_1.json',
        '03_machine_contracts/schemas/core/OFARM_LotLineageChange_schema_v0_1.json',
        '03_machine_contracts/schemas/core/OFARM_LocalArtifact_schema_v0_1.json',
        '03_machine_contracts/schemas/evidence/OFARM_ExternalRegistryVerificationTrace_schema_v0_1.json',
        '03_machine_contracts/drafts_non_default/assertion_record_submission/OFARM_AssertionRecord_schema_v0_2.json',
        '03_machine_contracts/schemas/agronomic/OFARM_PartialExtent_schema_v0_1.json',
        '03_machine_contracts/schemas/authority/OFARM_PartyRelationship_schema_v0_1.json',
        '03_machine_contracts/schemas/identity_lifecycle/OFARM_ScopeResponsibilityRelationship_schema_v0_1.json',
        '03_machine_contracts/schemas/identity_lifecycle/OFARM_IdentityLifecycleChange_schema_v0_1.json',
        '03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json',
        '03_machine_contracts/schemas/evidence/OFARM_EvidenceSufficiencyCase_schema_v0_2.json',
        '03_machine_contracts/schemas/agronomic/OFARM_AgronomicObservationContext_schema_v0_1.json',
        '03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json',
        '03_machine_contracts/schemas/agronomic/OFARM_InterventionIntentPayload_schema_v0_1.json',
        '03_machine_contracts/schemas/agronomic/OFARM_AgronomicIdentityBinding_schema_v0_1.json',
        '03_machine_contracts/schemas/agronomic/OFARM_AgronomicCodeBindingProfile_schema_v0_1.json',
        '03_machine_contracts/schemas/output_assembly/OFARM_ReviewDecision_schema_v0_1.json',
        '03_machine_contracts/schemas/interoperability/OFARM_ExternalCommitmentLink_schema_v0_1.json',
        '03_machine_contracts/schemas/event_ingress/OFARM_SemanticEventEnvelope_schema_v0_1.json']
    for path in current:capture('samovers/OFARM',HEAD,path,identity='CURRENT:'+Path(path).stem)
    capture('samovers/OFARM2','92b3c462058a7d1d483225091a84326702d82c32','contracts/core/OFARM_AppliedResourceIdentityPayload_schema_v0_1.json',identity='APPLIED_RESOURCE_PAYLOAD')
    (HERE/'source-pins.json').write_text(json.dumps({'sourceHead':HEAD,'status':'EXACT_PINNED_CONSTRUCTION_SOURCES','sources':records,'next':'Use source contracts and explicit definitions; examples are not schema inference inputs.'},indent=2)+'\n')
    print(json.dumps({'sources':len(records),'originalDistinctSources':len(seen)}))
if __name__=='__main__':main()
