# OFARM Phase 4 Query / Current-State / Output Conformance Gates v0.1

Date: 2026-05-13  
Status: draft implementation/conformance support  
Phase: AI-agent-ready platform amendment Phase 4

## Scope

These gates test whether an implementation preserves OFARM app-facing display honesty for query, materialization, and output assembly surfaces.

## Blocker gates

| Gate ID | Name | Blocker condition |
|---|---|---|
| P4-QRY-001 | Query result qualification required | every public query result has a `ResultQualificationEnvelope` or mapped equivalent |
| P4-QRY-002 | Permission-limited is not no-data | permission-limited evidence does not render as “no records found” |
| P4-QRY-003 | Claim is not accepted execution | submitted operation claims remain distinct from accepted consequences |
| P4-MAT-001 | Materialization is not truth | materialization read cannot be written back as canonical assertion |
| P4-MAT-002 | Stale high-consequence block | stale/invalidated materialization blocks compliance/high-consequence output by default |
| P4-MAT-003 | Cache limitation preserved | cached current-state reads preserve `asOf`, freshness, trace, and limitation fields |
| P4-OUT-001 | PassportView is not attestable document | PassportView cannot be attested or filed as DocumentAssembly |
| P4-OUT-002 | Output preview is not publication | preview/dry-run never creates frozen output, filing, or accepted truth |
| P4-OUT-003 | Dispute/correction visible | disputed or corrected basis is disclosed or annexed according to output policy |
| P4-OUT-004 | Advisory/compliance separation | advisory-only basis cannot satisfy compliance output without governed bridge/promotion |

## Test input families

Use fixtures from:

```text
04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_QueryExecutionResult_example_agronomic_stale_materialization_pre_output_gate_refused_v0_1.json
04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/current_state/OFARM_MaterializationResult_example_field_advisory_stale_v0_1.json
04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_PublicationAssemblyResult_example_lot_passport_attestation_denied_v0_1.json
04_implementation_and_conformance/implementation_notes/query_cookbook_v0_1/
04_implementation_and_conformance/examples_and_fixtures/output_assembly_examples_v0_1/
```

## Pass condition

The platform is not app-agent-ready until the public API, SDK, and any generated UI examples preserve the qualification envelope and refuse unsafe high-consequence use.
