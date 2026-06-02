# OFARM Phase 5 AgentToolManifest Rules

## Required tool descriptor structure

Every agent-facing tool descriptor must declare:

1. tool identity and version;
2. public operation id or operation binding;
3. target twin;
4. action class;
5. effect classification;
6. input schema reference;
7. output schema reference;
8. required authority basis;
9. approval requirement;
10. semantic preconditions;
11. declared hints;
12. external-call policy;
13. farm-data learning policy;
14. redaction and permission-limited result policy;
15. trace requirement;
16. result qualification requirement;
17. readiness-claim limits.

## Required separation of outcomes

Tool invocation must separately report:

- transport outcome;
- tool outcome;
- policy outcome;
- OFARM semantic outcome;
- output disposition.

No single success flag may stand for all five.

## Prohibited pattern

A tool descriptor must not say, in effect:

> `readOnlyHint=true`, therefore no authority check is needed.

That pattern is explicitly rejected.
