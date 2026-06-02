# Phase 8 Conformance Runner Notes

This folder contains candidate runner notes only. The Phase 8 package defines tests and schemas but does not claim runtime execution.

A future runner should:

1. load `OFARM_Agent_Readiness_Conformance_TestPlan_v0_1.json`;
2. load each suite file;
3. validate case shape against `OFARM_AgentReadinessConformanceCase_schema_v0_1.json`;
4. execute static checks where possible;
5. call runtime public operations only through the SDK/public contract pack;
6. write an `OFARM_AgentReadinessConformanceExecutionReport`;
7. fail readiness on any BLOCKER failure.

The runner must never use internal platform APIs to make tests pass.
