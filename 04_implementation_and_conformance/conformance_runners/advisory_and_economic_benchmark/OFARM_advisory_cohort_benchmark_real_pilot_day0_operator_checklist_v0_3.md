# OFARM advisory cohort benchmark real-pilot day-0 operator checklist v0.3

Use this checklist before running the real pilot.

- [ ] Dataset uses stable redacted refs only
- [ ] Dataset honesty marker is correct (`REAL_REDACTED_PILOT` + `actualTenantData = true`)
- [ ] Every contribution has an explicit share-grant ref
- [ ] Every contribution has a reviewed extract ref
- [ ] Every contribution has an evidence ref, not raw evidence payload
- [ ] Product-class / exact-product normalization basis is explicit
- [ ] Forbidden metrics remain forbidden
- [ ] One request-history broaden or block case is present
- [ ] One revocation / recompute case is present
- [ ] Validator passes
- [ ] Runner output remains Advisory-only
- [ ] No raw peer rows are shown
- [ ] No exact contributor count is shown
- [ ] No peer total spend is shown
- [ ] No spend-per-hectare is shown
- [ ] Output is treated as benchmark guidance only, not compliance truth
