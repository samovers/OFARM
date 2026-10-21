# Portable use

Install Python dependencies `rfc8785==0.1.4` and `jsonschema==4.26.0` in a locally selected environment. No network access occurs during verification.

For the local candidate run:

```sh
python3 -B run_conformance.py --package-root . --fixture-root . --out /tmp/occupancy-conformance.json
python3 -B verify_occupancy.py --request fixtures/mixed-LOT-CONTAINER/request.json --context fixtures/mixed-LOT-CONTAINER/context.json --record-map fixtures/mixed-LOT-CONTAINER/record-map.json --trusted-pins fixtures/mixed-LOT-CONTAINER/trusted-pins.json --package-root . --source-root . --out /tmp/occupancy-report.json
```

The installed layout separates `packageRoot` (contract and schemas), `checkerRoot` (Python), and `fixtureRoot` (fixtures and exact source copies). Pass `--package-root packageRoot --source-root fixtureRoot` to the checker, and `--package-root packageRoot --fixture-root fixtureRoot` to conformance. The exact paths and hashes are in the integration map. Import `verify_occupancy.verify` from checkerRoot and pass those same explicit roots to the API. The API preserves full digest or revision selectors; `selector_key(binding)` constructs only the transport dictionary key.

The CLI record-map is a list of full binding and relative file path pairs. It rejects duplicate selectors and paths escaping that map's directory. Trusted pins are independent caller inputs. Fictional fixture pins illustrate their shape and must not be treated as authentic producer configuration. `MATCHED_SELECTED_OCCUPANCY_EVIDENCE` is conditional comparison, with actual source admission and actual inventory completeness unestablished. There is no standalone runtime verdict or write action.

Next: bind independently selected owner inputs in the consumer and apply all retained source qualifications.
