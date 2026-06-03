# CP14 Phase 6.1 — Remediation and Schema Hardening Plan

Status: CP14 Phase 6.1 remediation candidate  
Schema posture: draft/non-default  
Current/default promotion: none  
CP15 contracts: not created  
OFARM Social / OFARM Exchange / public benchmark product / generic reputation contracts: not created

## Purpose

This remediation pass implements the Phase 6 hostile-review findings as a narrow hardening patch. It does not expand CP14 scope. It makes the farm-to-farm intelligence boundary executable enough to proceed toward a final amendment package.

## P0/P1 remediation mapping

| Defect | RFC text change | Baseline patch change | Schema change | Conformance fixture change | Blocking |
|---|---|---|---|---|---|
| No executable conformance runner | Add CP14 runner requirement and cross-record semantics | No baseline change beyond conformance note | Add schema-aware runner | Added positive/negative fixtures and runner | Yes |
| Share grant temporal/currentness | State grants must be temporally coherent and active to support sharing | No baseline change | Added approval/revocation fields; runner checks validFrom/validUntil/active state | Added invalid/expired/revoked/denied fixtures | Yes |
| Allowed/prohibited overlap | State use-class arrays must be disjoint | No baseline change | Added uniqueItems broadly; runner checks no-overlap | Added overlap fixtures | Yes |
| Strong prohibited output uses | RFC must define forbidden strong uses | No baseline change | Output schema supports qualification fields; runner blocks truth/current/compliance/mission/model use | Added forbidden-use fixtures | Yes |
| Published regional alerts | Published alerts require qualification and applicability boundary | No baseline change | RegionalAlert supports publicationAuthorityTraceRef/correction policy | Added missing qualification/applicability fixtures | Yes |
| Benchmarks | Published benchmarks require aggregation floor and risk/qualification | No baseline change | BenchmarkDelta supports reidentificationRiskAssessmentRef and disclosure flags | Added weak floor/high risk/compliance fixtures | Yes |
| Anonymisation/deidentification | Approval/review requires risk basis and low risk for anonymisation | No baseline change | Added review/output qualification fields | Added high risk/no approval/no risk fixtures | Yes |
| Reidentification disclosure | High/unknown risk blocks public disclosure and requires partner review | No baseline change | ReidentificationRiskAssessment supports partner disclosure review flag | Added public/partner high-risk fixtures | Yes |
| Revocation propagation | Revocation state controls grants/packages/training use | No baseline change | RevocationTrace supports affected outputs/contributions/receipts/failure reasons | Added revoked grant/training/revocation state fixtures | Yes |
| CP13 farm memory boundary | Farm-memory derivatives require explicit CP14 permission and recipient-memory block | No baseline change | LearningArtifactSharePackage supports explicit farm-memory sharing fields | Added farm-memory boundary fixtures | Yes |
| CP11 sustainability disclosure | Sustainability signals require CP11 qualification and cannot become certification/compliance | No baseline change | FarmIntelligenceContribution supports CP11 qualification refs | Added sustainability signal fixtures | Yes |
| CP12 mission/incident disclosure | Mission/incident signals require CP12 qualification and redaction posture | No baseline change | FarmIntelligenceContribution supports CP12 qualification refs | Added mission/incident fixtures | Yes |
| Federated/training use | Federated contribution/training receipt require policy and privacy compliance | No baseline change | Federated/Training schemas support policy fields | Added noncompliant and valid fixtures | Yes |
| Poisoning/anomaly downstream use | Blocking review disposition blocks downstream use | No baseline change | Existing review disposition used by runner | Added poisoning downstream fixtures | Yes |
| Cross-farm applicability | Local high-consequence use requires applicability assessment | No baseline change | Output and applicability schemas support local applicability flags | Added local-use fixtures | P1 |
| TrainingUsePolicyBinding | Training allowed requires purposes, recipients, model families, receipt, retention/revocation policy | No baseline change | Added/checked fields | Added training policy fixtures | P1 |
| ModelImprovementSignal | High-confidence signal requires aggregation/quality/anomaly basis and never authorizes deployment | No baseline change | Added basis fields | Added model-signal fixtures | P1 |
| Schema version hygiene | Harmonize remediated schema version | No baseline change | `cp14-v0.1-draft-phase6-1-remediated` used for all remediated schemas | Validation report checks schema count | P1 |

## Affected revised schema-style definitions

The package contains remediated draft/non-default definitions for all CP14 Phase 5 schemas, including the hostile-review affected set. This is intentionally broad at machine-contract package level so examples and the executable runner have a consistent schema surface, but current/default promotion remains explicitly blocked.

## Minimum P0 runner specification

The runner must be:

- schema-aware;
- cross-record aware;
- able to resolve share grants, output qualification, risk assessment, training policy, contribution quality, poisoning/anomaly review, and applicability records;
- able to reject overlapping use classes;
- able to reject strong prohibited output uses;
- able to enforce CP11/CP12/CP13 boundary references for sustainability, mission/incident, and farm-memory derivative sharing;
- able to keep federated-learning contribution separate from CP15 deployment authority.

## Positive and negative fixture list

The executable suite includes 69 fixtures: 17 positive and 52 negative.

## Non-claims

This remediation does not create production farm-to-farm intelligence readiness, production federated-learning readiness, OFARM Social law, OFARM Exchange law, public benchmark product law, legal/privacy/certification advice, generic reputation law, CP15 model/software deployment law, or current/default machine-contract promotion.
