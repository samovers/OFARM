# OFARM Compiled Output and Passport Taxonomy Note v0.1

Date: 2026-04-08  
Status: phase-10 baseline artifact  
Scope: normative clarification of compiled-output families so “passport” stops acting as a catch-all term

---

## 1. Purpose

OFARM needs cleaner language around compiled outputs.

Before this note, “passport” risked covering too many different things:
- scope summaries
- inspection/case packages
- subsidy/support packages
- buyer-facing compiled outputs

That blur is dangerous because these outputs have different semantics, different governance, and different runtime behavior.

This note defines a cleaner taxonomy.

---

## 2. Core output stack

OFARM now treats output-related concepts in this order:

1. **QuerySpecification** retrieves
2. **ViewModule** shapes
3. **PassportView** provides a portable scope-centric summary view
4. **DocumentAssembly** freezes a governed compiled output for a purpose

This makes retrieval, presentation, and publication distinct.

---

## 3. PassportView

A **PassportView** is a governed, portable, scope-centric compiled view.

Typical characteristics:
- anchored to a stable operational scope object
- concise enough for sharing or coordination
- may be human-readable, machine-readable, or both
- derived from QuerySpecifications plus view logic
- not automatically attested or frozen merely because it exists

Typical scope anchors:
- farm
- site
- field
- crop cycle
- lot
- facility where needed

Typical examples:
- farm passport view
- field passport view
- crop-cycle passport view
- lot passport view

Important rule:
- recipient-specific variants are usually **profiles of a PassportView**, not separate top-level taxonomy families

So:
- a buyer-facing lot passport is still a **Lot PassportView**
- an inspector-oriented field passport is still a **Field PassportView**

unless the output becomes a case package or formal filing, in which case it leaves the passport family.

---

## 4. DocumentAssembly

A **DocumentAssembly** is a frozen, governed compiled output with derivation trace and possible attestation/review state.

DocumentAssembly is the family for outputs that need:
- freezing
- versioning
- durable referencing
- attestation or signature
- later evidentiary reuse

DocumentAssembly is not the same thing as:
- current state
- a live view
- a PassportView

---

## 5. DocumentAssembly subfamilies

### 5.1 ReportAssembly
A **ReportAssembly** is a frozen narrative/tabular/structured report compiled for a purpose.

Typical examples:
- seasonal operations report
- internal compliance report
- buyer report
- advisory summary report

### 5.2 DossierAssembly
A **DossierAssembly** is a frozen evidence-rich package centered on a case, review, inspection, investigation, or claim.

Typical examples:
- inspection dossier
- nonconformity dossier
- insurance dossier
- audit dossier

### 5.3 SubmissionAssembly
A **SubmissionAssembly** is a frozen package intended for formal filing or delivery to another governed process.

Typical examples:
- compliance submission package
- subsidy/support application package
- certifier submission package
- authority filing package

---

## 6. Key boundary rules

### 6.1 Not every compiled output is a passport
Passports are scope summaries, not the universal bucket for every compiled thing.

### 6.2 Inspection output is normally dossier-shaped
An inspection-centered package should normally be a **DossierAssembly**, not an “inspection passport.”

### 6.3 Subsidy/support filing is normally submission-shaped
A subsidy/support package should normally be a **SubmissionAssembly**, not a “passport.”

### 6.4 Buyer-facing output is purpose-dependent
A buyer-facing output may be:
- a profiled PassportView, if it is a concise scope summary
- a ReportAssembly, if it is a frozen report
- a SubmissionAssembly, if it is a formal declared package

### 6.5 DocumentAssembly may later become evidence
A frozen compiled output may later serve as evidence, but publication alone does not make it canonical truth.

---

## 7. Runtime consequences

The platform should therefore keep separate:
- live/recomputable PassportViews
- frozen DocumentAssemblies
- output subtype handling for reports, dossiers, and submissions

This improves:
- naming clarity
- governance clarity
- UI clarity
- compatibility with external processes
- future interoperability

---

## 8. Practical naming consequences

Preferred naming examples:

- **Farm PassportView**
- **Field PassportView**
- **Lot PassportView**
- **Inspection DossierAssembly**
- **Subsidy SubmissionAssembly**
- **Seasonal ReportAssembly**

Avoid using:
- “passport” as a blanket word for every compiled output
- “inspection passport” when what is really meant is a dossier
- “subsidy passport” when what is really meant is a submission package
