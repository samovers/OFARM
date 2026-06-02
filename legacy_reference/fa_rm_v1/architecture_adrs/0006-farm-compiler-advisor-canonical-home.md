# ADR 0006: Farm Compiler remains a narrative alias while advisor stays the canonical runtime and spec family

## Status

Accepted

## Context

An external five-phase handover package introduces a strong product metaphor, `Farm Compiler`, alongside:

- a proposed `/v1/planning/*` endpoint root
- `Planning*` runtime nouns such as `PlanningScenario` and `PlanningOption`
- crop-pack, normalization, and demo assets authored outside the repo's current advisor source/generated discipline

The repository already has a current advisor line with:

- canonical runtime routes under `/v1/advisor/*`
- current runtime models in `specs/api/v1/server/fastapi/app/advisor_models.py`
- current runtime routing in `specs/api/v1/server/fastapi/app/main.py`
- contract and behavior tests in `specs/api/v1/server/fastapi/tests/test_advisor_api.py`
- authored advisor knowledge-pack source and generated assets under `docs/advisor/v1/knowledge-packs/`
- a repo-local sync/check tool for advisor content hashes and generated JSON under `docs/advisor/v1/tools/sync_advisor_artifacts.py`

Without an explicit decision, the handover could create a second contract family beside the advisor line and violate the repo rule against parallel concepts and transport models.

## Decision

Adopt the following rules for Farm Compiler material in this repository:

1. `Farm Compiler` is a narrative or product alias only.
2. The canonical runtime and spec home remains the existing advisor family:
   - `/v1/advisor/*`
   - `Advisor*` runtime models
   - `docs/advisor/v1/*`
3. `Planning*` nouns from the handover may be used only as source-alias language inside adaptation docs until a later gap audit proves a real missing advisor contract.
4. Raw handover YAML, manifests, and demo assets are migration input, not canonical advisor assets.
5. Future horticulture or open-field crop content must be translated into the current advisor source/generated discipline rather than imported as a second pack format.
6. Any future promotion of `Farm Compiler` from alias to canonical contract family requires a new ADR and supporting runtime evidence.

## Consequences

Positive:

- the repo avoids a second endpoint root and a second top-level recommendation model family
- current advisor tests, capability semantics, and content-hash tooling remain authoritative
- later crop-content adaptation can proceed in narrow passes without reopening endpoint naming every time
- mixed-equipment, buyer-pressure, and projection work can be evaluated as explicit deltas instead of implicit handover defaults

Costs:

- external handover pack IDs, YAML schemas, and demo file names cannot be copied into canonical advisor roots unchanged
- future crop-writing passes must do explicit translation work rather than a bulk import
- some handover fields remain backlog until they are proven to need real advisor request or response changes
