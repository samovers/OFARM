# Supplementary independent review evidence

Primary trust boundary: **transaction and history evidence for protected proposed state**. This is review evidence for the separately sealed 259-file core, with no change to its contract, checker, schemas or fixtures. `core-files.json` publishes the exact relative file list and hashes from that reviewed candidate. The final outcome record and generated indexes are outside that core file list.

`run_independent_late_shapes_02.py` is the independent reviewer's portable copy of the 144 fresh R1 probes. `origin.json` records attribution and exact script/helper hashes. `portable-generator.diff` records path/import adaptation only; expectations and source bytes are unchanged. `portable-parity.json` records 144 passing replays and 1,728 matching input/report files. `late-shape-results.json` records 112 expected rejections and 32 expected conditional passes. These are the same 144 cases already counted once within the 271 independent probes, not additional independent review.

With the declared dependencies installed, run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B run_independent_late_shapes_02.py --repository-root <reviewed-repository> --output-dir <local-output-directory>
```

The script uses only the hash-pinned independent helper and writes every exact original, selection, guard and report for replay. The complete local review archives remain retained separately; this published supplement contains the portable generator, provenance and compact results, not those whole local archives. `public-review-manifest.json` binds this published subset. The generator reproduces all 144 cases from the public reviewed repository.

All observations are fictional and conditional. No real source admission, owner appointment, database protection, authorization, human/domain approval or runtime completion is established. Reports retain runtimeProtection=NOT_ESTABLISHED and laterTransactionGate=NOT_EVALUATED. #392/#396 remain parked; #421, CI activation and merge remain separate.

Next: replay the finite evidence against the exact published files, then consider any consumer binding separately.
