# CP11 Final Migration Notes

## Recommended merge order

1. Add CP11 RFC to `02_accepted_rfcs/`.
2. Apply controlled baseline patch text to the Constitution, Platform Runtime, Alignment Register, readiness memo, and hostile-review memo.
3. Add companion policy note.
4. Stage CP11 schemas under `03_machine_contracts/drafts_non_default/sustainability_charter/`.
5. Add CP11 contract-family currentness addendum.
6. Add pack-contract CP11 surface patch.
7. Add conformance runner and fixtures.
8. Run P0/P1 fixture suite.
9. Only after architect acceptance, update `CONTRACT_FAMILY_CURRENTNESS.md` if CP11 schemas should become current/default.

## Migration posture

Existing sustainability-adjacent text remains advisory/supporting until mapped to CP11 concepts.

Existing sustainability outputs should be treated as advisory/non-claim unless they can produce `SustainabilityClaimBasis`, freshness posture, output qualification, and authority/approval posture.

Existing packs that touch sustainability content should be treated as touching undeclared surfaces until CP11 pack surfaces are declared and merge-tested.

## Backwards compatibility

CP11 adds governance surfaces. It does not rewrite existing truth/current-state/pack/authority laws.

## Rollback posture

If CP11 causes contradiction during review, roll back only CP11 additions. Do not revert existing active baseline law.
