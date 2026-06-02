# OFARM economic intelligence consolidated package smoke check v0.1

## Scope

This note records a minimal post-merge smoke check for the consolidated package built from the v0.6-4 migration seed plus the bounded economics package.

## Checks performed

1. Confirmed presence of the three economics companion artifacts in `01_companion_artifacts/`.
2. Confirmed presence of the economics scenario contract candidate and experimental machine-contract schema bundle in `04_implementation_and_conformance/`.
3. Confirmed presence of Lane A, Lane B, and Lane C execution notes and sample datasets/results where applicable.
4. Confirmed presence of the real-farm pilot validator, runner, CLI wrapper, dataset template, and illustrative dataset.
5. Ran the one-command pilot CLI against the illustrative non-real dataset from inside the consolidated package.

## Outcome

The illustrative pilot smoke run completed successfully and produced:
- lane A READY / EXECUTED
- lane B READY / EXECUTED
- lane C READY / EXECUTED

This smoke check proves package coherence for the bounded economics implementation path.
It does **not** prove real-farm validity, runtime integration, or promotion readiness.
