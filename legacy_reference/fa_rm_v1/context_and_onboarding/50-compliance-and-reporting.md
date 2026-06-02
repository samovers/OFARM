# Compliance And Reporting

Use this doc for regulatory scope, rule and report assets, reporting binders, and the strongest evidence-backed compliance boundaries in the repo. For generic runtime endpoint ownership, use [40-api-and-data-contracts.md](40-api-and-data-contracts.md). For implementation maturity and open questions, use [70-implementation-status.md](70-implementation-status.md) and [80-open-questions-and-risks.md](80-open-questions-and-risks.md).

## Where compliance assumptions live

### Rulepacks

- `implemented`: rulepacks live under `specs/v0.4/regulatory/rulepacks/`.
- `implemented`: EU organic 2026 is `normative` and encodes hard or soft rules such as certificate validity, traceability completeness, non-authorized substance detection, authorized-input-only, and GMO prohibition. `specs/v0.4/regulatory/rulepacks/organic-eu-2026.json:L1-L86`
- `implemented`: Slovenia organic 2026 is also `normative`, inherits the EU pack, and adds SI-specific certificate, control-registration, logo, and conversion rules. `specs/v0.4/regulatory/rulepacks/organic-si-2026.json:L1-L78`
- `implemented`: Serbia organic 2026 exists but is explicitly `draft`, not a proven normative baseline. `specs/v0.4/regulatory/rulepacks/organic-rs-2026-draft.json`

### Claim validator

- `implemented`: runtime claim validation delegates to `specs/v0.1/validation/bin/validate-claim.sh`. `specs/api/v1/server/fastapi/app/main.py:L148-L152`, `specs/api/v1/server/fastapi/app/main.py:L11955-L11957`
- `implemented`: the shell validator resolves rulepacks by jurisdiction and profile, merges inherited rules, auto-evaluates facts, enforces minimum evidence count, warns on draft rulepacks, and distinguishes hard errors from soft warnings. `specs/v0.1/validation/bin/validate-claim.sh:L20-L75`, `specs/v0.1/validation/bin/validate-claim.sh:L135-L256`
- `implemented`: tests assert accepted SI claims, draft-warning behavior for RS, and missing-fact warnings. `specs/api/v1/server/fastapi/tests/test_api.py:L226-L260`

## Reporting pack assets

- `implemented`: the SI organic control pack is defined as a report-pack asset with authority, template, layout, official source PDF reference, required fields, and export bundle profile. `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L1-L81`
- `implemented`: the report pack states that the current implementation is crops-only and excludes livestock and beekeeping sections. `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L29-L35`
- `implemented`: the layout map contains explicit section and column PDF placement metadata. `specs/v0.4/regulatory/report-layouts/si-2026-pdf-01.layout-map.v1.json:L1-L260`

## Runtime control-pack binding

- `implemented`: `build_si_org_control_pack_payload()` creates canonical scaffolding for A plant-production, D processing or marketing, and E complaints sections, plus inspector-facing notes. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L649-L803`
- `implemented`: the binder uses persisted certification scopes, operations, inventory receipts, cleanouts, delivery tickets, complaints, harvest rows, rotation plans, residue panels, contamination risks, parallel production data, and task state. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L845-L1015`
- `implemented`: the binder populates concrete rows for A2 fertilization, A3 harvest, D4 purchases, D2 suppliers, D3 customers, D7 sales, D8 inventory, D9 processing cleaning, and E complaints. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1067-L1112`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L2116-L2410`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L2490-L2543`
- `partial`: when persistence is disabled, the binder returns an incomplete payload with explicit warnings rather than pretending data exists. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L647-L648`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L810-L837`

## Reporting bridge to logging and attestation

- `implemented`: the control-pack binder already reads executed operations, conversion timelines, parallel-production controls, and seed-sourcing exceptions together. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1326-L1715`
- `implemented`: inspector-note buckets for `conversionTimeline`, `parallelProduction`, and `seedSourcingExceptions` are already part of the reporting payload. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1456-L1490`
- `implemented`: reporting fetch for executed operations includes operation-type derivation and linked evidence URIs, with `extension_inference` and `unknown` behavior covered by tests. `specs/api/v1/server/fastapi/app/persistence.py:L17173-L17280`, `specs/api/v1/server/fastapi/tests/test_persistence.py:L8282-L8373`
- `implemented`: the additive operation-assessment layer now has a first-class `reportReady` field and `report_ready` lifecycle state for the covered generic families. `specs/api/v1/server/fastapi/app/main.py:L3443-L3545`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L740-L915`
- `partial`: binder-backed official-report readiness can still be stricter than assessment readiness, because Control Center review detail uses live or cached `reportBindings[]` completeness and tests prove a mismatch case where `assessment.reportReady` is `true` while `reportBindings[0].reportReady` is `false`. `specs/api/v1/server/fastapi/app/main.py:L18849-L18902`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L1475-L1485`, `docs/implementation/logging-attestation-master-spec.md:L253-L338`

## A.5 source-plan overlap

- `implemented`: the nearest repo-backed planning overlay for saveable logging work is the A.5 canonical source-plan contract. It preserves `known`, `intentional_blank`, `fallow`, `unsupported`, and `unknown` semantics. `docs/implementation/si-rb-a5-1-rotation-plan-structure-spec.md:L83-L145`, `specs/v0.8/archetypes/CLUSTER.rotation_plan_entry.v1.md:L1-L53`
- `implemented`: the SI binder keeps those A.5 source-plan semantics visible through `sourcePlan` rows and reviewer-facing warning codes. `specs/api/v1/server/fastapi/tests/test_reporting_control_pack.py:L1267-L1338`

## Official PDF rendering

- `implemented`: tests verify that the layout map includes all A, D, and E sections, that official PDF rendering writes a multi-page output, that overflow rules work, and that Slovenian characters survive rendering. `specs/api/v1/server/fastapi/tests/test_si_control_pack_official_form_pdf.py:L70-L99`, `specs/api/v1/server/fastapi/tests/test_si_control_pack_official_form_pdf.py:L102-L159`, `specs/api/v1/server/fastapi/tests/test_si_control_pack_official_form_pdf.py:L206-L243`

## Contract tests around reporting

- `implemented`: `test_si_recordbook_contract_v1.py` checks contract versioning, timezone, crops-only flags, excluded sections, row audit metadata, local date or time formatting, and canonical section keys. `specs/api/v1/server/fastapi/tests/test_si_recordbook_contract_v1.py:L218-L260`
- `implemented`: `test_reporting_control_pack.py` uses stub persistence to verify that jurisdiction facts and recordbook scaffolding are derived from persistence inputs. `specs/api/v1/server/fastapi/tests/test_reporting_control_pack.py:L10-L18`, `specs/api/v1/server/fastapi/tests/test_reporting_control_pack.py:L275-L305`

## What you can safely assume

- `implemented`: EU and SI organic are first-class and test-backed.
- `partial`: RS organic exists as draft rules, not a normative runtime-backed reporting baseline.
- `partial`: reporting implementation is strongest for SI crops-only control-pack workflows.

## What you still need to verify before making broader claims

- `unknown`: no equivalent inspected pack in this pass proved full US regulatory workflows. `specs/v1.0.0/version-map.md:L20-L37`
- `unknown`: broader non-crops or non-SI reporting support should not be assumed without rulepacks, report packs, layouts, runtime binders, and tests that prove it.
