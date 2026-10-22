# Registration and review boundary

Register only the separately approved `AuthorizationDecisionEvidence v0.2 / canonical_success_path` draft profile. The target directory and all exact file mappings are in `integration-map.json`. Register the owned schema set as DRAFT/NON_DEFAULT; the fixture source schemas remain fictional conformance inputs, never active authority contracts. Link the opt-in runner, source pins, README, source-interface specification and implementation evidence.

The runner belongs in `04_implementation_and_conformance/conformance_runners/canonical_success_path/`. Package schemas and contract metadata belong in `03_machine_contracts/drafts_non_default/authorization_decision_evidence/canonical_success_path/`. The verbatim pinned PR11 Markdown belongs only in `04_implementation_and_conformance/examples_and_fixtures/fixtures/canonical_success_path/sources/`. The code takes that fixture root through the explicit `source_root` API argument or `--source-root` CLI option and verifies its actual adjacent implementation bytes separately from package-root schemas and fixture-root semantic source bytes, so the layout does not require copying code into the schema directory or falling back to a checkout path.

Do not add this runner to the default repository suite or activate CI. A delivery issue/draft PR may point to #47 as its consumer dependency but remains a separate primary trust boundary. No policy eligibility rule, principal resolver, AuthoritySourceBundle, CP3 envelope, runtime transaction, receipt, signing service or production grant is changed by this packet.

The existing PR11 source law is copied verbatim from its pinned owner revision. The source-record and policy examples are deliberately fictional exact-byte inputs. They exercise the interface without asserting that a live producer or a v0.1-to-v0.2 migration has been admitted. No fixture marker, mirrored Party, ALLOW flag or successful checker report is permission for an effect.

Next: independently review the sealed candidate and install using the exact map; root owns publication of the separate Delivery issue and draft PR.
