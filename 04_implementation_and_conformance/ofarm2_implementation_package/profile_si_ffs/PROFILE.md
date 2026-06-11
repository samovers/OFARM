# Slovenia FFS pilot profile (`profile:si.ffs.recordkeeping.v0_1`)

Status: profile definition — candidate material, not OFARM law. National registers and identifiers are **anchors and bindings under this profile**, never universal OFARM core law (Constitution RC2.1 §3.4).

## Claim scope

Record-keeping completeness only. No current-compliance claim, no certification claim, no legal advice. See `../PILOT_SI.md`.

## Scheme role map (feeds the `AgronomicCodeBindingProfile` instance)

| Scheme | Role under this profile | Currentness posture |
|---|---|---|
| **SI:UVHVVR-FFS-REG** — UVHVVR "Seznam registriranih FFS" (`spletni2.furs.gov.si/FFS/REGSR/`) | Mandatory binding source for plant-protection product authorisation identity; registration/authorisation number is the primary external key; trade name is captured evidence, never sole identity. *(M0 correction: FITO-INFO has been shut down and redirected to GOV.SI registers — see `M0_DESK_RESEARCH.md` §3.)* | Snapshot-based. Cadence declared at M0 (target: weekly scripted; floor: monthly manual). Every snapshot is a dated `ReferenceSnapshot` with source artifact refs. **Weaker than the Belgium reference pattern and declared so.** Export mechanics TO-VERIFY (M0 checklist item 4). |
| **IS Evidenca FFS** — UVHVVR central FFS-use registry (live by 1 Dec 2026) | Future **submission target**, not a binding scheme: the pilot's frozen register export is positioned to become the farmer's annual submission (first due 31 Jan 2027 for 2026). Interface TO-VERIFY (M0 outreach Q2). | Not applicable until the state publishes its interface; tracked in `M0_DESK_RESEARCH.md` §2. |
| **GERK** | Parcel identifier scheme for Field identities (`parcelIdentifiers.scheme = "SI:GERK"`) | **National GERK layer is open data** (OPSI shapefile + WMS, MKGP viewer): the app carries the layer; farmer supplies KMG-MID and confirms their GERK list (eRKG / subsidy paperwork). Layer snapshot-stamped per sync; farmer-provided export remains fallback only. |
| **KMG-MID** | Holding identifier scheme for Farm identities (`holdingIdentifiers.scheme = "SI:KMG-MID"`) | Captured at onboarding as registered identifier + evidence |
| **EPPO** | Crop and target-organism codes | Pinned code-list version per package release |
| **BBCH** | Growth stage codes (where label/rules cite stages) | Pinned version |
| **UCUM / QUDT** | Unit codes / quantity kinds for dose, area, volume | Pinned version |
| **EU Pesticides Database** | EU active-substance **context only** — informational, no legal value, never product authorisation identity | Optional context snapshots |

Reference pattern: `../reference/rfcs/OFARM_External_Code_Binding_Currentness_and_Verification_RFC_v0_1.md` (Belgium/Phytoweb). The SI profile mirrors its structure with an honestly weaker declared currentness class; converging to Phytoweb-grade mechanics is the precondition for any future current-compliance claim.

## Evidence and review policy (`policy:si.ffs.evidence-review.v0_1`)

**Evidence floor for promoting an operation claim to accepted execution:**
resolved product binding (against a dated snapshot) · dose with valid UCUM unit · valid parcel ref (GERK-bound field or explicit `PartialExtent`) · crop binding (EPPO, may come from auto-created cycle) · operator party (with `DelegationGrant` if not the holder) · event time within plausibility window. Photo evidence: encouraged, never required for the floor.

**Sufficiency cases** are auto-generated from this policy template at exactly two points: operation-claim promotion and DocumentAssembly freeze. Drafts and notes never generate cases.

**Review:** farmer self-review for routine claims meeting the floor (the deliberate "confirm & accept" step). Exceptions — unresolved binding, implausible dose, dispute, post-sync discrepancy, late evidence — route to the advisor queue. Self-review is sufficient for record-keeping use, insufficient for certification-grade claims. Software-agent review: Phase-2 candidate, not in this profile version.

**Advisory rule:** authorisation-mismatch and dose-range warnings are `advisory output` commit-class records (Advisory twin). They never block, never auto-create compliance facts, and are never silently dropped from farmer view.

## Shipped instances (validated by `../conformance/ofarm_pkg_contract_check.py`)

- `OFARM_PackActivationSet_example_si_ffs_pilot_v0_1.json` — static single-profile activation (no overlap → no merge trace needed)
- `OFARM_ActiveArtifactSet_example_si_ffs_pilot_v0_1.json` — pilot artifact state; **regenerate at M1** when the deferred instances below exist
- `OFARM_ContextSnapshot_example_si_ffs_pilot_compliance_v0_1.json` — demo-tenant Compliance-twin context spine; runtime generates per-farm snapshots referencing the same activation/artifact sets

## Deferred instances (deliberate — do not fabricate before verification)

| Instance | Why deferred | Due |
|---|---|---|
| SI `AgronomicCodeBindingProfile` JSON (`codebindingprofile:si.ffs.v0_1`) | Requires M0-verified registry facts (lookup surface, export format, cadence, identifier stability) — fabricating them would violate the profile's own discipline | M0/M1 |
| Capability Manifest (`manifest:si.ffs.pilot.v0_1`) | Declares the deployment's actual runtime surfaces + unsupported-surface posture (`../PLATFORM.md`); premature before the API exists | M1 |

## Reserved identifiers

`pack:si.ffs.pilot.v0_1` · `profile:si.ffs.recordkeeping.v0_1` · `policy:si.ffs.evidence-review.v0_1` · `codebindingprofile:si.ffs.v0_1` · `manifest:si.ffs.pilot.v0_1` · `view:si.ffs.spray-register.passportview.v0_1` · `view:si.ffs.inspection-register.documentassembly.v0_1` · `registry:ofarm2-implementation-package.v0_1` · `tenant:si.ffs.pilot.demo`
