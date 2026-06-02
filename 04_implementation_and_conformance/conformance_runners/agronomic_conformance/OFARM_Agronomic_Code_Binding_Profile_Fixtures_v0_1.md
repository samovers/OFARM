# OFARM Agronomic Code Binding Profile Fixtures v0.1

Status: Active supporting implementation/conformance artifact. Does not override active baseline law.
Date: 2026-05-13
Phase: AGR-P5

## Purpose

These fixtures validate the Phase AGR-P5 closure for scheme-bound agronomic identity and profile-governed code binding.

The fixtures prove that OFARM can bind crops, varieties, seed lots, crop stages, target organisms, crop-protection products, fertilizer blends, quantity kinds, unit codes, sampling methods, and threshold sources without turning external standards into OFARM truth stores.

## Positive fixture families

| Fixture family | Contract/example | Expected behavior |
|---|---|---|
| Profile declaration | `OFARM_AgronomicCodeBindingProfile_example_si_crop_protection_core_v0_1.json` | Declares external standards as anchors, bindings, runtime surfaces, exchange mappings, or attestation wrappers; packs constrain but do not mutate meaning. |
| Crop species | `OFARM_AgronomicIdentityBinding_example_maize_crop_species_eppo_v0_1.json` | EPPO-bound crop identity may support high-consequence use only through profile and evidence gates. |
| Variety/cultivar | `OFARM_AgronomicIdentityBinding_example_maize_variety_cpvo_v0_1.json` | Variety denomination carries registry context; label alone is not global identity. |
| Seed lot | `OFARM_AgronomicIdentityBinding_example_seed_lot_oecd_gs1_v0_1.json` | Issuer-scoped lot identity and certificate/batch evidence are retained. |
| Crop stage | `OFARM_AgronomicIdentityBinding_example_bbch_crop_stage_v0_1.json` | BBCH stage remains tied to observation evidence. |
| Weed/target organism | `OFARM_AgronomicIdentityBinding_example_velvetleaf_weed_eppo_v0_1.json` | Target-organism binding stays role-specific and evidence-bound. |
| Crop-protection product | `OFARM_AgronomicIdentityBinding_example_crop_protection_product_si_authorisation_v0_1.json` | Jurisdictional authorization and reference snapshot support product identity. |
| Marketing-only product name | `OFARM_AgronomicIdentityBinding_example_crop_protection_product_marketing_name_unresolved_v0_1.json` | Ambiguous marketing name is retained as evidence but blocks high-consequence product identity. |
| Fertilizer local blend | `OFARM_AgronomicIdentityBinding_example_fertilizer_local_blend_v0_1.json` | Local blend identity is separate from PPP product semantics. |
| Quantity kind and unit | `OFARM_AgronomicIdentityBinding_example_application_rate_qudt_ucum_v0_1.json` | Quantity kind and UCUM unit are both required. |
| Sampling method | `OFARM_AgronomicIdentityBinding_example_soil_sampling_method_profile_v0_1.json` | Local method profile can bind where public method coding is not available. |
| Threshold source | `OFARM_AgronomicIdentityBinding_example_advisory_threshold_source_v0_1.json` | Threshold is source-bound and not a free-floating current-state number. |

## Negative fixture expectations

1. Verified identity with no identifier must fail.
2. Ambiguous identity must fail closed or require review.
3. Quantity profile cannot disable the quantity-kind plus unit-code requirement.
4. Binding requirements cannot omit unresolved behavior.
5. Crop-protection product captured only by marketing name cannot support compliance-grade product identity.

## Limitations

This phase closes code-binding/profile carrier semantics. It does not yet close agronomic query/output reconstruction, PassportView disclosure policy, or baseline harmonisation.
