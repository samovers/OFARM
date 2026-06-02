# OFARM High-Consequence Freshness Profiles for Staple-Crop Campaigns v0.1

Date: 2026-04-14  
Status: proposed active supporting implementation artifact  
Scope: bind existing OFARM freshness law to the staple-crop campaign classes most likely to produce stale-state errors in implementation

---

## 1. Purpose

OFARM already has the right law:
- current state is derivative
- freshness is purpose-sensitive
- stale or invalid state must be recomputed, refused, or explicitly reviewed for high-consequence use

What is still needed is a disciplined operational profile for the staple-crop flows where weak implementations most often misuse state.

---

## 2. Core stance

### 2.1 Do not hard-code agronomic constants into core law
This note does **not** freeze universal numbers for moisture windows, safe storage periods, or crop-stage timing. Those remain pack/profile/configuration territory.

### 2.2 Do define trigger classes and use-class obligations
What this note does fix is:
- which trigger classes matter for each high-consequence use class
- when stale may still be tolerated for exploratory use
- when stale must be treated as invalid for governed reliance
- when a retained `MaterializationSnapshot` is mandatory

---

## 3. Required staple-crop freshness profiles

### 3.1 Establishment and replant decision profile
High-consequence uses:
- subsidy or insurance filing
- crop-in-force declarations
- accepted crop-cycle transition affecting later current state

Critical trigger families:
- new emergence/stand observation
- replant intervention
- crop-cycle termination/successor relation
- field revision affecting the applicable planted area
- pack/context change affecting filing logic

Allowed stale posture:
- exploratory advisory review may use stale state if clearly marked

Not allowed stale posture:
- filing or attested claim about crop in force
- accepted current-state update on the wrong cycle identity

Snapshot rule:
- retain a `MaterializationSnapshot` whenever a filing or attested output relies on the crop-in-force answer

### 3.2 Nutrient and PPP compliance profile
High-consequence uses:
- compliance assertion
- inspection dossier
- submission package
- accepted operation consequence that materially affects regulated totals or restrictions

Critical trigger families:
- late machine or invoice evidence
- corrected input identity
- field or zone scope correction
- rule/pack change affecting required evidence or buffers
- human-machine contradiction resolution

Allowed stale posture:
- advisory operational view only

Not allowed stale posture:
- compliance fact
- attested report
- filing package

Snapshot rule:
- retain a `MaterializationSnapshot` for any attested or filed compliance-facing output

### 3.3 Wet-grain and storage-condition profile
High-consequence uses:
- buyer delivery or quality claim
- attested quality report
- storage-risk compliance or insurance dossier
- accepted condition-sensitive decision such as disposal/diversion/claim

Critical trigger families:
- new moisture observation
- new temperature observation or telemetry batch
- drying intervention
- aeration intervention
- lot split/merge/commingle affecting the stored cohort
- storage-location transfer
- contamination or lab-result event
- missed telemetry interval where the profile treats the gap as material

Allowed stale posture:
- exploratory advisory storage monitoring may use stale state with explicit warning

Not allowed stale posture:
- any buyer-facing claim or attested quality output derived from pre-drying or pre-transfer state
- any dossier/submission that relies on an outdated condition basis

Snapshot rule:
- retain a `MaterializationSnapshot` for delivery, attestation, disposal/diversion, or formal claim paths

### 3.4 Buyer delivery and commercial quality profile
High-consequence uses:
- buyer-facing Lot PassportView with claim-bearing quality content
- frozen buyer report or declared package
- regrading or rejection dispute package

Critical trigger families:
- official buyer grade/moisture/protein/dockage result
- lot merge/split or claim-basis reset
- new contamination evidence
- superseding shipment linkage
- new authority/sharing posture affecting what may be shown

Allowed stale posture:
- low-consequence internal coordination view only

Not allowed stale posture:
- externally relied-upon current-state claim
- frozen buyer package or evidentiary report

Snapshot rule:
- retain a `MaterializationSnapshot` whenever a buyer-facing frozen output or claim-bearing delivery package is emitted

### 3.5 Inspection, corrective-action, and submission profile
High-consequence uses:
- dossier attestation
- corrective-action acceptance
- formal submission filing
- superseding submission after late evidence

Critical trigger families:
- new ReviewDecision
- new evidence bundle or provenance gap resolution
- context/pack change affecting the applicable rule or policy posture
- identity/lifecycle change affecting scope interpretation
- authority or revocation change before final filing

Allowed stale posture:
- exploratory internal preparation only

Not allowed stale posture:
- final attestation
- final filing
- final corrective-action closure

Snapshot rule:
- always retain a `MaterializationSnapshot` for final dossier or submission paths

---

## 4. Common implementation rules

- high-consequence freshness is profile-bound, not clock-only
- recompute-before-use must be scenario-visible
- advisory tolerance must not leak into compliance
- missing telemetry can itself be a material trigger

---

## 5. Mandatory fixtures

A conforming implementation should prove at least:
- drying invalidates a prior delivery/quality basis
- new lot merge invalidates a prior buyer-facing claim basis
- new field revision invalidates a subsidy filing basis but not a historical advisory view
- new review decision invalidates a prior dossier/submission basis
- a telemetry gap can force review or refusal when the active profile requires continuity

---

## 6. Non-goals

This note does not create:
- a new freshness-state taxonomy
- a new material-condition ontology
- a new storage-truth layer
- crop-specific legal thresholds inside core law
