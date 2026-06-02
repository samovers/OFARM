
# OFARM Application Workflow Cookbook v0.1

Date: 2026-05-13  
Status: candidate implementation/conformance guidance  
Authority posture: does not override active OFARM law

## Purpose

This cookbook gives AI coding agents concrete workflow recipes for OFARM applications. It is app-facing: it teaches what screens, SDK calls, and state labels should do without copying platform internals or flattening OFARM into CRUD.

## Included recipes

| File | Workflow |
|---|---|
| `OFARM_ApplicationWorkflowCookbookCase_field_crop_setup_v0_1.json` | Field and crop-cycle setup |
| `OFARM_ApplicationWorkflowCookbookCase_observation_to_advisory_v0_1.json` | Observation to advisory recommendation |
| `OFARM_ApplicationWorkflowCookbookCase_recommendation_prescription_workorder_v0_1.json` | Recommendation to prescription to work order |
| `OFARM_ApplicationWorkflowCookbookCase_execution_claim_to_accepted_v0_1.json` | Operation claim and evidence to accepted execution |
| `OFARM_ApplicationWorkflowCookbookCase_delayed_contractor_sync_v0_1.json` | Offline/delayed contractor sync |
| `OFARM_ApplicationWorkflowCookbookCase_correction_dispute_v0_1.json` | Correction and dispute |
| `OFARM_ApplicationWorkflowCookbookCase_inventory_update_after_execution_v0_1.json` | Inventory update after accepted execution |
| `OFARM_ApplicationWorkflowCookbookCase_audit_query_output_v0_1.json` | Audit query to PassportView/DocumentAssembly preview |

## Non-negotiable implementation lesson

An app may make common farm work easy, but it must not hide OFARM state. The UI can be plain English, but the code must preserve canonical distinctions.

```text
Submitted work record != Accepted execution record
Suggested action != Prescribed action
Evidence received != Verified execution
Current status view != Canonical truth
Passport preview != Frozen document/submission
Restricted details != No data exists
```

## How to use

1. Use the JSON recipes as app-builder fixtures.
2. Generate tests that verify public operation references and safe labels.
3. Use the state matrix as the label source.
4. Treat forbidden behaviours as negative tests.
5. Do not promote these recipes to active law without review.
