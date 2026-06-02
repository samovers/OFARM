# CP11 Sustainability Charter Conformance Fixture Set v0.1 — Phase 7.3

Status: schema-aware CP11 conformance fixture set, still draft/non-default.

```text
fixtureCount: 61
positiveFixtureCount: 22
negativeFixtureCount: 39
allFixturesPassed: True
```

## Phase 7.3 additions

Phase 7.3 added final boundary and claim-disposition fixtures for:

- claim-readiness to exact output-disposition binding;
- failed hard constraint results that attempt to allow a plan with `blocking = false`;
- complete `ALLOW_WITH_QUALIFICATION` traces with empty typed results and no basis;
- advisory-only public disclosure blocking;
- positive controls proving valid claim-ready, non-advisory public-disclosure, and qualified no-applicable-rule paths can pass.

The runner validates JSON Schema payloads and applies semantic hardening checks where pure JSON Schema cannot express cross-field/date/set constraints cleanly.
