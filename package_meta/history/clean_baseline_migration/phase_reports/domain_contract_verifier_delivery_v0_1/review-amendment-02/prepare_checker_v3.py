"""Copy and narrowly adapt the preserved v2 finite checker; no source edits."""
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('--previous-amendment',type=Path,required=True);a=p.parse_args();O=Path(__file__).resolve().parent
s=(a.previous_amendment/'check_examples.py').read_text()
s=s.replace("parser.add_argument('--source-examples', type=Path)","parser.add_argument('--source-examples', type=Path)\nparser.add_argument('--previous-amendment', type=Path, help='Preserved v2 sibling; defaults to ../review-amendment')")
s=s.replace("bundle = read('candidate-examples-v2.json')","bundle = read('candidate-examples-v3.json')")
s=s.replace("projection = read('projection-contract-v2.json')","projection = read('projection-contract-v3.json')")
s=s.replace("selector_table = read('evidence-selectors.json')","selector_table = read('evidence-selectors-v3.json')")
s=s.replace("before = copy.deepcopy(source); before.pop('assertionAct'); before['candidateGrammar'] = bundle['bundleVersion']", "before = copy.deepcopy(source); before.pop('assertionAct'); before.pop('association', None); before['candidateGrammar'] = bundle['bundleVersion']")
s=s.replace("after = copy.deepcopy(c); after['evidenceBindings'] = source['evidenceBindings']", "after = copy.deepcopy(c); after['evidenceBindings'] = source['evidenceBindings']\n    if e['id'] == 'W05_CENSORED_CRITERION':\n        after['proposition']['definition'] = source['proposition']['definition']\n        after['proposition']['body'].pop('criterion')\n        after['proposition']['body']['operand'].pop('source')\n        after['proposition']['body']['operand'].pop('admissibleValues')")
s=s.replace("c['association']['envelope'] not in c['evidenceBindings'] and\n              c['association']['ingressEvidence'] not in c['evidenceBindings']", "e['associationVerificationInputs']['envelope'] not in c['evidenceBindings'] and\n              e['associationVerificationInputs']['ingressEvidence'] not in c['evidenceBindings'] and 'association' not in c")
s=s.replace("result = {'status':",(O/'checker_additions_v3.txt').read_text()+"\nresult = {'status':")
s=s.replace("'No complete domain verifier was implemented or executed.'", "'No complete domain verifier was implemented or executed; W05 and event checks are finite fictional models.'")
(O/'check_examples_v3.py').write_text(s)
