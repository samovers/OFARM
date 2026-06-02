# OFARM Phase 6 Negative Case Register v0.1

| ID | Negative case | Expected result |
|---|---|---|
| P6-NC-001 | WorldModelState submitted as Compliance current state | Blocked with `WORLD_MODEL_STATE_NOT_CURRENT_STATE` |
| P6-NC-002 | Scenario result used as accepted disease presence | Blocked with `WORLD_MODEL_CONFIDENCE_NOT_EVIDENCE_SUFFICIENCY` |
| P6-NC-003 | Forecast-driven scenario used after forecast divergence | Mark requires recheck or invalidated |
| P6-NC-004 | Scenario output used for filing/submission | Blocked unless independent governed output assembly and approval path exists |
| P6-NC-005 | Model calibration evidence treated as authority | Blocked; calibration is credibility support only |
| P6-NC-006 | Observed-outcome reconciliation mutates canonical history | Blocked; create review/correction candidate if needed |
| P6-NC-007 | Long-context memory cited as truth | Blocked unless persisted as governed artifact and promoted normally |
| P6-NC-008 | Pack/profile change ignored after scenario run | Mark requires recheck or invalidated |
| P6-NC-009 | Third AI/world-model twin created | Blocked as baseline violation |
| P6-NC-010 | World-model scenario hides uncertainty in farmer brief | Result qualification required; unqualified brief blocked |
