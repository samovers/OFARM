"""Construction only: refresh fixed runtime closure before tests; never run after sealing."""
from pathlib import Path
import json,sys,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[2]/'plans/domain-contract-verifier-20261021/local-dependencies'))
from path_common import sha,digest
files={}
for p in [H/'source-pins.json',*(H/'schemas').glob('*.json'),*(H/'sources').glob('*')]:files[str(p.relative_to(H))]=sha(p.read_bytes())
c={'contractId':'ofarm.authorizationDecisionEvidence.canonicalSuccessfulPath.v0.1','packageFamily':'AuthorizationDecisionEvidence.v0.2','status':'DRAFT_NON_DEFAULT','primaryTrustBoundary':'Canonical authorization decision evidence','verificationScope':'SELECTED_OWNER_OUTPUT_INTEGRITY_ONLY','authorizationLawSha256':sha((H/'sources/pr11.md').read_bytes()),'files':dict(sorted(files.items())),'dependencyVersions':{'rfc8785':'0.1.4','jsonschema':'4.26.0'},'sourceTupleOrder':['DIRECT_PARTY_GRANT','ROLE_TARGETED_GRANT','DELEGATED_GRANT','SHARING_GRANT_ACCESS'],'sourceReferencePolicy':'Grant/delegation/sharing source IDs require one-record source digests; other records require a revision or digest and independently pinned original bytes.','notEstablished':['Authorization eligibility','Principal resolution trust','Candidate completeness','Canonical selection correctness','Runtime source origin and admission','Source currentness and migration','CP3 admission','Runtime protection'],'next':'Independent review before use; no default activation or effect permission.'}
c['verificationCode']={n:sha((H/n).read_bytes()) for n in ['verify_success_path.py','path_common.py']}
c['contractDigest']=digest(c);(H/'contract.json').write_text(json.dumps(c,indent=2)+'\n');print(c['contractDigest'])
