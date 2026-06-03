# Release Profile Validation

Current package: `OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized`.

Release profiles are packaging views only. They do not change OFARM law or repository authority.

## Source Policy Check

Run:

```sh
python3 package_meta/tools/check_release_profile_policy.py
```

This verifies profile files, current package identity, clean-baseline completion, source artifact policy, and root ZIP hygiene.

## Build External Packages

Build both profiles outside the repository:

```sh
OUT="/tmp/ofarm_dev_audit_release_profiles_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
python3 package_meta/tools/build_ofarm_release_profiles.py --all --output-dir "$OUT"
```

The build writes DEV and AUDIT ZIPs, SHA-256 files, contents manifests, and build reports to the external output directory.

## Validate After Extraction

After extracting a package, run:

```sh
python3 package_meta/tools/check_release_profile_policy.py
python3 package_meta/tools/run_repository_validation_suite.py
```

The DEV package is expected to exclude `clean_baseline_phase_reports/`. The AUDIT package is expected to include audit and provenance material.

## Expected External Artifacts

DEV:

- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_DEV.zip`
- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_DEV.zip.sha256`
- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_DEV_contents.txt`
- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_DEV_build_report.json`
- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_DEV_build_report.md`

AUDIT:

- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_AUDIT.zip`
- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_AUDIT.zip.sha256`
- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_AUDIT_contents.txt`
- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_AUDIT_build_report.json`
- `OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2_AUDIT_build_report.md`

Generated ZIPs and staging directories are external release assets and must not be committed.
