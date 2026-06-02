<!--
Promotion review copy only. This file is included inside the Phase 2 supporting review folder.
It is not active OFARM law unless copied to the active target path by a separate controlled promotion.
Phase 2 classification: GREEN_WITH_REVIEW.
-->


# OFARM Application Workflow State Matrix v0.1

Date: 2026-05-13  
Status: draft companion candidate under AI-agent-ready platform amendment  
Authority posture: implementation support only unless promoted

## Purpose

This matrix gives AI coding agents UI-safe language and state boundaries for OFARM client applications. It prevents application screens, assistants, dashboards, and workflow tools from collapsing OFARM states that have different authority, evidence, promotion, and truth posture.

This artifact does not change baseline law. It packages existing OFARM law into app-builder guidance.

## Core rule

A generated app must preserve this chain:

```text
recommendation ≠ prescription ≠ planned intervention ≠ work order ≠ operation claim ≠ as-applied evidence ≠ accepted execution consequence ≠ correction ≠ dispute ≠ outcome
```

It must also preserve:

```text
PassportView ≠ DocumentAssembly
advisory output ≠ compliance output
current-state materialization ≠ canonical history
permission-limited result ≠ no data exists
import candidate ≠ accepted OFARM truth
```

## Safe labels by state

| Canonical OFARM state | Safe app label | Forbidden labels |
|---|---|---|
| advisory output / recommendation | Suggested action | approved treatment; compliant treatment; work order |
| prescription / authorised intent | Prescribed action | work completed; accepted execution |
| planned intervention | Planned work | actual operation; product applied |
| work order | Work order issued | accepted work; completed application |
| operation claim | Submitted work record | accepted execution; verified completed work |
| as-applied evidence | Evidence received | verified execution; compliance fact |
| accepted executed intervention consequence | Accepted execution record | contractor claim; draft work |
| correction assertion | Correction submitted | record deleted; old record overwritten |
| open dispute | Under dispute | completed; verified; compliant |
| current-state materialization | Current status view | canonical truth; source record |
| PassportView preview | Passport preview | final report; submitted document |
| DocumentAssembly preview | Document preview | filed submission; accepted compliance fact |
| permission-limited read result | Restricted details | no records exist; all clear |
| FMIS/import candidate record | Imported candidate | accepted farm record; verified machinery fact |

## Screen implementation requirements

Generated applications must:

1. keep claim/evidence/import states visually distinct from accepted consequences;
2. show freshness, basis, and trace links when displaying current-state views;
3. show advisory-only labels for recommendations and assistant output;
4. show authority scope and expiry for prescriptions and work orders;
5. show correction/dispute lineage without deleting or rewriting earlier history;
6. render permission-limited data as restricted/redacted, not absent;
7. render output previews as previews until publication/freeze/attestation succeeds;
8. keep PassportView and DocumentAssembly naming distinct.

## Negative examples

Unsafe:

```text
Contractor claim synced → app marks task completed → dashboard uses it as compliance evidence.
```

Safe:

```text
Contractor claim synced → app shows submitted work record → platform reviews evidence/authority → accepted execution appears only after governed promotion.
```

Unsafe:

```text
Recommendation generated → app creates approved treatment.
```

Safe:

```text
Recommendation generated → app shows suggested action → authorised actor may create prescription or work order through public APIs.
```

Unsafe:

```text
Query result redacts evidence → app says no evidence exists.
```

Safe:

```text
Query result redacts evidence → app says evidence details are restricted and provides trace/access action where authorised.
```

## Machine-readable matrix

The machine-readable state matrix is:

```text
04_implementation_and_conformance/implementation_notes/application_workflow_cookbook_v0_1/OFARM_ApplicationWorkflowStateMatrix_v0_1.json
```
