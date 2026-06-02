# OFARM Staple Crop Campaign Fixture Library v0.1

Date: 2026-04-14  
Status: proposed active supporting implementation artifact  
Scope: define the minimum campaign-scale staple-crop fixtures needed to make OFARM strong under ordinary farm reality before implementation expands

---

## 1. Purpose

The current package is strong on many individual seams. What it still lacks is enough **campaign realism**.

This library defines the fixture families that turn staple-crop stress scenarios into executable implementation obligations.

This is not a new semantic layer. It is a conformance and hardening library built on top of existing OFARM law.

---

## 2. Fixture design rules

Every campaign fixture in this library must include:
- at least two event families
- at least two commit classes
- at least one current-state transition
- at least one negative or review-routed path
- at least one query/retrieval assertion
- at least one output-family assertion
- all relevant authority actors for the scenario
- all active packs/profiles needed for the scenario

Every fixture must prove not only the “happy path” but also the refusal/review path that a weak implementation would mishandle.

---

## 3. Required campaign fixtures

### Fixture 1 — Partial replant campaign
Mandatory proof:
- no silent overwrite of the original cycle
- query can distinguish full-field view from child-cycle view
- filing path uses correct cycle in force at evaluation time

### Fixture 2 — Crop switch after failure campaign
Mandatory proof:
- new CropCycle identity created only at the right boundary
- event time, effective time, and record time remain distinct
- frozen submission path retains old and new bases clearly

### Fixture 3 — Variable-rate fertiliser reconciliation campaign
Mandatory proof:
- projection does not become truth
- human and machine evidence can coexist in contradiction or partial agreement
- compliance-facing state is blocked or reviewed when evidence is insufficient

### Fixture 4 — Ambiguous PPP record upgrade campaign
Mandatory proof:
- weak support stays weak until upgraded
- later evidence can strengthen without rewriting history
- dossier/submission output versions supersede rather than mutate in place

### Fixture 5 — Wet grain hold, dry, store, deliver campaign
Mandatory proof:
- materialization freshness is use-class sensitive
- new drying or transfer events invalidate prior high-consequence quality state
- “what was in this storage location when” is reconstructable

### Fixture 6 — Storage sanitation and condition-drift campaign
Mandatory proof:
- sanitation evidence does not disappear from later case reconstruction
- the same lot can continue across condition changes without false new-lot creation
- contamination or spoilage incidents remain query-visible in history and outputs

### Fixture 7 — Lot split, sublot test, partial merge, buyer rejection campaign
Mandatory proof:
- test lineage never disappears through merge
- claim basis before and after merge remains explicit
- new lot identity is created when the cohort changes

### Fixture 8 — Organic/conventional segregation campaign
Mandatory proof:
- pack interaction is deterministic
- access for buyer/certifier remains read/review only as granted
- outputs are dossier/submission where appropriate, not generic passports

### Fixture 9 — Spray-drift dispute campaign
Mandatory proof:
- contested truth remains explicit
- cross-farm sharing remains governed
- no silent conversion of allegation into compliance fact

### Fixture 10 — Contractor late-record and revocation campaign
Mandatory proof:
- report creation may succeed while later high-consequence promotion fails
- authority is re-evaluated at promotion time
- trace shows delegator, delegate, scope, and revocation posture

### Fixture 11 — Post-filing late-evidence supersession campaign
Mandatory proof:
- old package is preserved
- new package has new basis and new output identity/version
- query can retrieve the full supersession chain

### Fixture 12 — Recipient-profile retrieval campaign
Mandatory proof:
- same underlying truth, different governed visibility
- buyer receives a profiled PassportView or report only
- certifier gets dossier or review-facing output only when granted

---

## 4. Cross-cutting mandatory query families

Each campaign must exercise at least one of these query families:
- `as_of_incident_scope_state`
- `current_storage_contents`
- `evidence_supporting_accepted_consequence`
- `lot_claim_basis_before_after_reset`
- `same_field_across_revision`
- `late_evidence_supersession_chain`

---

## 5. Cross-cutting mandatory output families

The library must prove correct use of:
- `PassportView`
- `ReportAssembly`
- `DossierAssembly`
- `SubmissionAssembly`

At least four of the campaigns must prove that the correct answer is **not** a passport.

---

## 6. Packaging guidance

Recommended fixture packaging:
- `04_implementation_and_conformance/ofarm_staple_crop_campaign_fixtures_v0_1/<fixture-id>/inputs/`
- `04_implementation_and_conformance/ofarm_staple_crop_campaign_fixtures_v0_1/<fixture-id>/expected/`
- `04_implementation_and_conformance/ofarm_staple_crop_campaign_fixtures_v0_1/<fixture-id>/results/`

Each fixture should also name:
- governing pack set
- relevant machine contracts reused
- required negative cases
- target conformance rows affected

---

## 7. Coverage-matrix additions

The conformance coverage matrix should add rows for at least:
- staple-crop campaign fixture library
- degraded-evidence upgrade fixtures
- wet-grain/storage freshness fixtures
- lot sublot and merge campaign fixtures
- post-filing supersession fixtures
- recipient-profile retrieval fixtures

Initial status may be `PARTIAL` at design level, but each row must become `COVERED` only when executable fixture results exist.

---

## 8. Priority order

Implement in this order:
1. ambiguous PPP record upgrade
2. wet grain hold/dry/store/deliver
3. lot split/sublot/merge/buyer rejection
4. contractor late-record and revocation
5. post-filing supersession
6. remaining fixtures
