# OFARM Farm-Owner Draft Contract Promotion Map v0.1

Generated: 2026-05-13T17:53:02+00:00

| Contract / pattern | Current status | Purpose | Promotion blocker |
|---|---|---|---|
| minimum_capture_profile | draft/non-default | routine operations, contractor work, storage/lot capture floor | do not promote before live/user-burden evidence |
| temporal_qualifier | draft/non-default | exact, bounded, estimated, record-only, unknown/conflicting source timing | promote only if pilots confirm reusable semantics |
| offline_capture_and_late_sync | draft/non-default | local sequence, duplicate retry, effective/recorded/received time, late evidence append | requires runtime pilot before hardening |
| storage_lot_genealogy | draft/non-default | intake, drying, storage, split, merge, dispatch, buyer dispute lineage | needs source-owner storage/lot evidence |
| high_consequence_freshness_gate | draft/non-default | blocks stale/incomplete current state for consequential outputs | requires operational gate implementation proof |
| share_export_exit_bundle | draft/non-default | share grants, export bundle, integrity manifest, loss map | needs source-owner export evidence |
| nutrient_value_recalculation | draft/non-default | estimated versus measured values, late lab recalculation, successor position | needs jurisdictional/regulatory profile review before promotion |
| fmis_shadow_adapter_output | draft/non-default | candidate records, review gaps, loss map from existing FMIS data | keep import-only until owner evidence improves |
| unresolved_actor_identity | draft/non-default | hidden or inferred contractor/carrier/performer signal from weak FMIS records | promote if repeated imports require common pattern |
| live_pilot_evidence_packet | draft/non-default | external packet, metrics, provenance, redaction, disposition | activate only when real packet submitted |

## Promotion rule

No farm-owner draft contract should be promoted to default conformance merely because internal rehearsal passed. Promotion requires accepted owner evidence, live runtime evidence, or an explicit accepted RFC process.
