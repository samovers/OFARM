# OFARM Phase 8 Scenario — Controlled benchmarking and learning remains advisory and grant-bound

## Scenario family

`controlled_benchmarking_learning`

## Farmer value

Give the farmer useful cohort insight without turning shared data into surveillance or unauthorized training material.

## Actors

- Humans: farm owner
- Agents: Benchmark Advisory Agent, Sharing Sovereignty Agent
- External parties: data cooperative

## Positive workflow

S1. **Sharing Sovereignty Agent** — checks benchmark SharingGrant and learning policy → `BENCHMARK_SCOPE_CONFIRMED`
S2. **Benchmark Advisory Agent** — generates advisory-only cohort comparison with aggregation qualifications → `BENCHMARK_ADVISORY_ONLY`
S3. **Sharing Sovereignty Agent** — records that no training-use grant exists → `NO_TRAINING_RIGHT`

## Expected outputs

- BenchmarkAdvisoryResult
- ResultQualificationEnvelope
- No-training policy trace

## Guardrails

- benchmark stays advisory
- farm data learning requires explicit grant
- cohort thresholds prevent deanonymization

## Must not happen

- benchmark becomes compliance fact
- farm data is retained for training without grant
- small-cohort output reveals neighbor data

## Negative companion

`OFARM-AAI-P8-CONTROLLED-BENCHMARKING-LEARNING-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
