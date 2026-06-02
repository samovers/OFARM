# CP12 final migration notes

Date: 2026-05-28

## Migration posture

CP12 is a controlled amendment candidate. It should be reviewed and accepted before any repository merge.

## Migration sequence

1. Review final CP12 RFC candidate.
2. Review baseline patch text and addenda.
3. Confirm CP12 schemas remain draft/non-default.
4. Run schema validation.
5. Run the CP12 conformance runner.
6. Confirm readiness and hostile-review non-claims.
7. Accept CP12 as a controlled baseline/RFC extension.
8. Only then consider repository merge.

## No automatic currentness promotion

The CP12 schemas remain draft/non-default. Current/default promotion requires a separate currentness-promotion decision.


## Explicit deferrals

CP12 does not create:

- CP13 learning, experimentation, farm-memory, or learning-promotion law;
- CP14 farm-to-farm intelligence, regional mission coordination, or federated-learning law;
- CP15 generated-software delivery, robot-adapter deployment, rollback, or SBOM law;
- livestock-specific mission law;
- vendor protocol conformance;
- legal or safety certification.
