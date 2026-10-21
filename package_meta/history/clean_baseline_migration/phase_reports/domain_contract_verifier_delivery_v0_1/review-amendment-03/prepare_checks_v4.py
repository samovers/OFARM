"""Prepare the current full inherited suite with explicit v4 shape amendments."""
import argparse,json,copy,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--prior-packet',type=Path,required=True);a=p.parse_args();O=Path(__file__).resolve().parent
pin=next(x for x in json.loads((O/'source-pins-v4.json').read_text())['priorPacketFiles'] if x['path']=='check_examples_v3.py')
raw=(a.prior_packet/'check_examples_v3.py').read_bytes()
if hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise ValueError('Prior checker source hash mismatch')
s=raw.decode()
replacements=[
("before['candidateGrammar'] = bundle['bundleVersion']","before['candidateGrammar'] = c['candidateGrammar']"),
("after['proposition']['body']['operand'].pop('admissibleValues')","after['proposition']['body']['operand'].pop('admissibleValues')\n        after['proposition']['body']['operand']['limit'].pop('provenance')\n        after['proposition']['body']['threshold'].pop('provenance')"),
("from measurement_checks_v3 import w05_errors, required_role_errors","from measurement_checks_v4 import w05_error_codes as w05_errors, required_role_error_codes as required_role_errors"),
("actual['proposition']['body']['operand'].pop('admissibleValues')","actual['proposition']['body']['operand'].pop('admissibleValues')\n        actual['proposition']['body']['operand']['limit'].pop('provenance');actual['proposition']['body']['threshold'].pop('provenance')"),
("actual['evidenceBindings']=actual['evidenceBindings'][:-2]","actual['evidenceBindings']=actual['evidenceBindings'][:-3]"),
("[expect['contextBinding'],expect['methodUseBinding']]","[expect['contextBinding'],expect['methodUseBinding'],expect['quantityProvenanceBinding']]"),
("W05 original evidence prefix plus exact two new records","W05 original evidence prefix plus exact three new records"),
("selected_by_table(missing,empty_table)==[]", "selected_by_table(missing,empty_table)==[]"),
("w05_errors(case['claimContent'],case['records'],expect)","w05_errors(case['claimContent'],case['records'],{**expect,**case.get('ownerProfileSelection',{})})"),
("': isolated source failure'","': source semantic and independent pin comparisons'"),
]
ledger=[]
for before,after in replacements:
 count=s.count(before)
 if count!=1:raise ValueError((before,count))
 s=s.replace(before,after);ledger.append({'exactSource':before,'replacement':after})
(O/'inherited_checks_v4.py').write_text(s)
(O/'checker-transforms-v4.json').write_text(json.dumps({'source':'../review-amendment-02/check_examples_v3.py','transforms':ledger,'rule':'The full current suite is rerun over the v4 overlay. No historical pass is counted as current.'},indent=2)+'\n')
# Explicitly extend the historical transform chain while preserving its source side.
old=json.loads((a.prior_packet/'source-transform-map-v3.json').read_text());bundle=json.loads((O/'candidate-examples-v4.json').read_text());oldbundle=json.loads((a.prior_packet/'candidate-examples-v3.json').read_text());row=old['examples'][4];e=bundle['examples'][4]
row['intermediateV3']={'head':'1a2583d24aa7d280e257e2d54d1c7c3708b623b6','contentDigest':row['targetContentDigest'],'textDigest':row['targetTextDigest']};row['targetContentDigest']=e['claimContentDigest'];row['targetTextDigest']=e['renderedTextSha256'];row['operations'].append({'op':'versioned-extension','definition':e['claimContent']['proposition']['definition'],'adds':['/claimContent/proposition/body/operand/limit/provenance','/claimContent/proposition/body/threshold/provenance'],'evidenceBinding':e['evidenceClosure']['amendment03AddedBindings'][0]});old['v4Extension']='Only W05 has new provenance fields; all other v3 target bytes remain exact.'
(O/'source-transform-map-v4.json').write_text(json.dumps(old,indent=2)+'\n')
