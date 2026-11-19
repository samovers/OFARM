# PR47 commit-class correction

Correct the event `commitClass` to **OPERATION_CLAIM**. Preserve **OPERATION_CLAIM_ASSERTION** as the AssertionRecord result subtype and **OPERATION_ASSERTION** as the effect-subject kind. This fixes the confirmed source-fidelity defect at reviewed head `228b7f4d2918b8b65774c89487a16026c7226222`.

The primary trust boundary and intended PR boundary remain **AssertionRecord domain meaning and validation integrity**. Scope stayed inside that boundary. This is candidate design/evidence fidelity; it changes no authority, classification producer, source contract or admission rule.

The old finite checker compared the fictional package with its proof. Because both used the same incorrect subtype token, that consistency check passed. The corrected helper reads the exact pinned PR23 §7.2 table and both canonical CommitIngressRequest/Result `/properties/commitClass/enum` arrays independently of the package. It verifies the action, actual operation-intent schema discriminator, effect-subject kind, result subtype and all package/proof/trace commit-class roles. Source files are byte-pinned; the helper verifies their hashes before extracting values. PR23 §1 items 1, 2 and 7 state the same distinction.

Six existing files change:

- `event-compatibility-package-v3.json`: both case commit classes corrected.
- `event-cases-v3.json`: positive and inherited hostile records carry corrected canonical roles, updated package/proof digests, and the selected action. E03 deliberately retains the wrong proof class `STRUCTURE_ASSERTION` and now fails the independent action mapping too.
- `build_event_cases_v3.py`: fixes only the two commit-class assignments, retains result-subtype construction, regenerates dependent digests and avoids duplicate selector entries on repeated event-only builds.
- `event_checks_v3.py`: calls the source-backed token checks.
- `checker_additions_v3.txt` and `check_examples_v3.py`: add the canonical-source, subtype-preservation and negative controls.

Add `commit_class_checks_v3.py`, `commit-class-source-pins.json`, the four exact files under `commit-class-sources/`, `build_commit_class_cases_fix01.py` and `commit-class-cases-fix01.json`. The additional negatives cover (1) package/proof/trace agreeing on the invalid subtype token, (2) all three agreeing on a valid ingress enum token for the wrong action, and (3) incorrectly replacing the result subtype with the commit-class token. Their dependent digests are recomputed. The first two would pass the old package-versus-proof equality test and are now rejected by canonical sources.

Validation: **723/723 full checks** and **671/671 portable checks**, with zero failures. The portable run uses the default sibling prior-amendment layout and actual source schemas; the full run adds the 52 optional frozen-root checks. Both retain the measurement/F4, B2 timing/placement and offline-digest controls. All 25 claim examples remain byte-identical. All 12 existing event-case intent, result and envelope objects and intent/result digests remain exactly unchanged. The deliberately altered subtype exists only in the new CC03 negative.

`fix01-transform-map.json` records exact source/output file hashes and every JSON-value change. `fix01-changes.patch` shows the six modified existing files. `fix01-source-record.json` records source commit and sealed-owner hashes. The standalone directory also contains 18 unchanged v3 input files solely so the full checker can run here; the integration manifest identifies these as unchanged, not required replacements.

Run the corrected event builder, then `build_commit_class_cases_fix01.py`, to regenerate the focused cases. Run `prepare_checker_v3.py` against the preserved v2 sibling to regenerate the checker. All these tools write only beside themselves. Dependencies remain Python 3, rfc8785 0.1.4, jsonschema and referencing; no dependency was installed.

These are finite fictional checks, not a verifier implementation, producer/admission proof or fresh independent PR approval. This task wrote only `owner-domain-fix01/`. The sealed `owner-domain/` output and the shared worktree remain untouched by this task. No other agent/chat, GitHub, commit, CI or merge action was taken.

Next: integrate the six replacements and new source-backed controls after the current full review completes, regenerate the packet custody/report references, and obtain fresh review of the exact corrected head.
