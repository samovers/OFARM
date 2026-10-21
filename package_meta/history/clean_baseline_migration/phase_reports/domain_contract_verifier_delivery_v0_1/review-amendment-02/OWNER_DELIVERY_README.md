# V3 owner artifacts

These are fictional design artifacts for PR47 B2/F4. Start with [domain-owner-recommendation.md](domain-owner-recommendation.md). The primary trust boundary is AssertionRecord domain meaning and validation integrity; scope stayed inside it.

The checker reads the previous amendment without modifying it. When installed as `review-amendment-02/`, its default previous source is the sibling `../review-amendment/`; use `--previous-amendment` for another location. `--packet` selects the packet's preserved `reviewed-input/domain/whole-claim-examples.json`. `--frozen-root` optionally checks the complete original 48-member freeze and source inventory identities. `--repo-root` enables actual schema validation.

Dependencies: Python 3, `rfc8785==0.1.4`, `jsonschema`, and `referencing`. `--dependency-dir` can supply an existing rfc8785 installation. The local run used Python 3.14 with jsonschema/referencing in the existing user site, so it did not use isolated `-I` mode. No dependency was installed. Disable bytecode writes when using preserved source directories.

From the integrated packet directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 review-amendment-02/check_examples_v3.py review-amendment-02 --packet . --repo-root /absolute/path/to/OFARM --dependency-dir /absolute/path/to/rfc8785-parent --output review-amendment-02/check-results-v3.json
```

To reconstruct the authored examples locally, run `build_v3.py` with explicit `--previous-amendment`, `--frozen-root`, `--repo-root` and `--dependency-dir`; then `complete_design_v3.py` with `--frozen-root`, `--canonical-owner` and `--dependency-dir`; then `build_event_cases_v3.py --dependency-dir ...`. These write only beside themselves. The canonical owner note must exist before the completion stage. `prepare_checker_v3.py --previous-amendment ...` constructs the narrowly adapted checker from the exact preserved v2 checker plus `checker_additions_v3.txt`.

`source-record-v3.json` records additional committed-source byte verification performed during this delivery. Its schema-pin appendix in `measurement-role-contract-v3.json` and final check reports are custody outputs, not owner-admission inputs. Regenerate the final file manifest after any reconstruction.

The portable-layout smoke test used temporary symlinks within this owner directory and removed them afterward; no fixture copies or symlinks remain. The default sibling lookup passed 603 checks; the additional frozen-root controls bring the full run to 655.

Next: integrate this versioned packet, preserve all older files and obtain exact-head review.
