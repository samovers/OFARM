# Final Clean Baseline Recipient README

Start with `README.md`, then read `PROJECT_AUTHORITY.md`, `CURRENT_ACTIVE_ENTRYPOINT.md`, and `CURRENT_ACTIVE_ENTRYPOINT.json`.

Use current reader views as navigation aids only. Canonical active authority remains in the active folders, especially `00_active_baseline/`.

CP11 through CP15 package-meta evidence is under `package_meta/history/controlled_amendments/`.

`legacy_reference/` is contextual only and never overrides active OFARM 2 law.

Generated files are derived views and should not be cited as independent authority.

After extraction, run:

```bash
python3 package_meta/tools/run_repository_validation_suite.py
```

The CP12 through CP15 JSON-schema conformance runners require the `jsonschema` Python package to be available to the interpreter used as `python3`.
