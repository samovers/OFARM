# OFARM advisory cohort benchmark real-pilot redaction and sovereignty note v0.3

## Primary rule

The pilot packet is for **redacted benchmark contribution inputs**, not for raw documentary disclosure.

## Keep

Keep only what the bounded benchmark needs:
- stable redacted participant refs
- stable redacted farm refs
- stable redacted viewer refs
- share-grant refs
- reviewed extract refs
- evidence refs
- normalized product-class or exact product refs
- normalized quantity, unit, amount, window, and freshness/revocation posture

## Do not include

Do not include:
- personal names
- tax ids
- bank account numbers
- emails
- phone numbers
- raw invoice or receipt file payloads
- raw OCR text dumps if evidence refs are enough
- free-form comments that reveal a participant identity
- exact contributor counts on any user-facing output

## Product labels

A product label may appear in the pilot packet only when needed to support governed normalization.
That does **not** justify exposing participant identity or raw documents.

## Request-history records

Use request fingerprints or stable request refs rather than raw audit strings if the raw strings reveal tenant identity or other sensitive context.

## Sovereignty reminder

A benchmark contribution share-grant allows bounded benchmarking use.
It does **not** move authorship, governance authority, or unrestricted visibility to the operator or to other tenants.
