# Amendment 03 owner fix01

Read [FIX01_DECISION.md](FIX01_DECISION.md). [FIX01_DELIVERY_MANIFEST.json](FIX01_DELIVERY_MANIFEST.json) seals every member of this correction delivery except itself. The boundary is AssertionRecord domain meaning and validation integrity. This is a sealed correction proposal based on `37d680d598af0cd321c6d06e91af6aba60a73c8d`; it is not independent review approval or runtime source admission.

[correction-files-fix01.json](correction-files-fix01.json) names **11 replacements and seven additions** for the current `review-amendment-03/` directory. Copy only those members to their declared current paths. Keep this delivery, its manifest, source/transform ledger and reports together under the separate `review-repair-01/` record. Do not replace the first owner README, delivery manifest, historical reports or checkpoint. The coordinator must explicitly distinguish the original `37d680d` transport from the corrected current transport.

[source-transform-ledger-fix01.json](source-transform-ledger-fix01.json) records exact before/after hashes, reasons and H03 identities. [corrections-fix01.patch](corrections-fix01.patch) contains the complete declared current-file delta. [source-pins-fix01.json](source-pins-fix01.json) pins all 33 reviewed packet files and the completed review evidence.

To validate this owner proposal against a preserved `37d680d` packet, run from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 check_fix01.py \
  --base-packet /absolute/path/to/preserved/review-amendment-03 \
  --repo-root /absolute/path/to/OFARM \
  --dependency-dir /absolute/path/to/rfc8785-parent \
  --frozen-root /absolute/path/to/frozen-03 \
  --output /absolute/path/to/new-full-report.json
```

Omit `--frozen-root` for the portable run. The harness makes a disposable sibling layout inside its own directory, applies only declared corrections, and uses the default `../review-amendment-02` resolution. It removes the disposable files afterward. It verifies the exact reviewed input bytes and refuses a changed base packet. Dependencies are existing Python 3, rfc8785, jsonschema and referencing; these scripts install nothing. The tested environment uses the existing user-site schema packages, so do not add `-I` there.

To repeat the regeneration check:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 rebuild_fix01.py \
  --base-packet /absolute/path/to/preserved/review-amendment-03 \
  --dependency-dir /absolute/path/to/rfc8785-parent \
  --output /absolute/path/to/new-rebuild-report.json
```

After integration, the current packet can run `check_examples_v4.py` directly with `--repo-root`, optional `--dependency-dir`, optional `--frozen-root` and a new `--output`. Its updated `build_v4.py` and `prepare_checks_v4.py` regenerate the corrected fixtures and checker from `--prior-packet ../review-amendment-02`; the data builder also takes `--dependency-dir`. The approved fixture/profile files and typed helper modules are authored sources and must remain present. Reapply no historical builder over the corrected files.

Current evidence: [full report](check-results-fix01.json), **2,170 passes**; [portable report](portable-check-results-fix01.json), **2,118 passes**; [rebuild report](rebuild-check-fix01.json), **12 generated artifacts reproduced**; [review reproductions](review-reproductions-fix01.json); [preservation checks](preservation-check-fix01.json). Use a fresh output path when rerunning; do not overwrite these sealed reports.

Next: transfer the sealed correction, update current custody records explicitly, and obtain review of the exact integrated corrected commit. CI activation and merge remain separate.
