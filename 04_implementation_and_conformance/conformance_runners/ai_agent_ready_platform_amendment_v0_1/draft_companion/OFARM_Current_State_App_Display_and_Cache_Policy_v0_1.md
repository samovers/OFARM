# OFARM Current State App Display and Cache Policy v0.1

Date: 2026-05-13  
Status: draft companion artifact, implementation/conformance support only  
Phase: AI-agent-ready platform amendment Phase 4  
Affected active authority: `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`, `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`, `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`, `01_companion_artifacts/OFARM_Platform_Enforcement_Architecture_Memo_v0_1.md`

## 1. Purpose

This draft policy defines how OFARM client applications, SDKs, dashboards, and AI coding agents may display, cache, and reuse current-state materializations.

It does not create new model law. It makes existing OFARM law app-implementable: current state is a governed materialization, not canonical truth.

## 2. Governing invariant

Applications may display current-state materializations only through public platform surfaces that return a `ResultQualificationEnvelope` or equivalent qualification object.

Applications must not:

- write materialization stores directly
- treat materialization payloads as canonical assertion/history truth
- use stale materializations for high-consequence outputs unless the governing policy explicitly allows it
- hide invalidated, disputed, redacted, permission-limited, or evidence-insufficient status
- persist materialized values as new accepted facts without governed commit and promotion

## 3. Required app-visible states

Every public materialization read must be displayable in one of these states:

| State | Meaning | Default high-consequence use |
|---|---|---|
| `FRESH_USABLE` | Materialization satisfies declared freshness and basis requirements | allowed if authority/evidence also passes |
| `FRESH_ADVISORY_ONLY` | Fresh enough for advisory display but not compliance/action gating | blocked |
| `STALE_INFORMATIONAL` | May be shown as historical or exploratory context | blocked unless low-consequence advisory use is explicit |
| `STALE_BLOCKING` | Recompute or review is required | blocked |
| `INVALIDATED` | Basis changed or identity/context invalidated | blocked |
| `DISPUTED` | Basis contains open dispute or disputed accepted record | blocked or requires annex/review |
| `PERMISSION_LIMITED` | Actor lacks visibility into full basis | blocked unless output class permits redacted basis |
| `EVIDENCE_INSUFFICIENT` | Required evidence is missing, weak, or redacted | blocked for compliance/high-consequence use |
| `IDENTITY_UNRESOLVED` | Field, product, actor, lot, or source identity unresolved | blocked for high-consequence use |

## 4. Cache classes

Applications may cache only according to the qualification envelope:

| Cache class | Allowed app behavior |
|---|---|
| `NOT_CACHEABLE` | use once; must fetch again before display or action |
| `DISPLAY_CACHEABLE` | may cache for UI display; must keep qualification visible |
| `ADVISORY_CACHEABLE` | may support advisory workflow hints; not compliance decisions |
| `COMPLIANCE_RECHECK_REQUIRED` | may store snapshot reference; must preflight before output or action |
| `TRACE_ONLY_CACHEABLE` | may cache trace reference and summary, not materialized value |

Cached materializations must retain `asOf`, `derivedFromPromotionPoint`, `freshnessClass`, `traceRefs`, and all limitations.

## 5. App display obligations

A user-facing display must expose, in plain language:

- whether the value is current, stale, invalidated, disputed, redacted, or permission-limited
- whether it is advisory or compliance-grade
- what canonical basis or trace supports it
- what the user can do next, such as refresh, request permission, attach evidence, or open review

An app must not display `STALE_BLOCKING`, `INVALIDATED`, `DISPUTED`, or `EVIDENCE_INSUFFICIENT` materialization as “current”, “verified”, “complete”, “compliant”, or “accepted”.

## 6. Required platform behavior

The public materialization read surface must return:

- materialization payload or payload reference
- `ResultQualificationEnvelope`
- `RuntimeProblem` entries where limitations exist
- trace references
- permitted next actions

The platform should refuse or downgrade reads for high-consequence use when freshness, authority, evidence, identity, or pack context is insufficient.

## 7. AI coding-agent constraints

Generated application code must branch on qualification fields, not prose messages.

Forbidden generated-code patterns:

```text
if (materialization.value) markCurrent();
if (!records.length) showNoRecords();
cache.write('currentTruth', materialization.payload);
submitComplianceOutput(materialization.payload);
```

Required generated-code pattern:

```text
read = await ofarm.materializations.get(...)
qualification = read.qualification
if (!qualification.highConsequenceUseAllowed) renderBlockedState(qualification)
if (qualification.permissionClass !== 'FULL_DETAIL') renderPermissionLimitedState(qualification)
showTraceLink(qualification.traceRefs)
```

## 8. Promotion route

This policy should remain a draft companion artifact until reviewed against current-state materialization law, query law, output assembly law, and app examples.
