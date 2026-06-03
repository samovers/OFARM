# OFARM Release Profiles

Current package: `OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized`.

Latest controlled amendment: **CP15**.

Release profiles are packaging views. They do not create OFARM semantic law, do not override active authority, and do not move source repository files.

## Profiles

- `DEV` is the lean development-starting-point package for implementation work and Codex development sessions.
- `AUDIT` is the proof/provenance package for reviewers, auditors, stewards, and reconstruction of the clean-baseline migration trail.

The source repository remains the canonical working repository. It stays audit-capable through source-controlled proof files and history lanes, while generated profile ZIPs remain external release assets.

## Artifact Policy

Bulky release ZIPs, report ZIPs, DEV ZIPs, and AUDIT ZIPs must not be committed to the source repo. Build them outside the repository with `package_meta/tools/build_ofarm_release_profiles.py`.

Use `package_meta/tools/check_release_profile_policy.py` to verify that the profile policy files exist, parse, and preserve the current CP15 clean-baseline state.
