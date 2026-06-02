# OFARM external evidence redaction and sovereignty note v0.1

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: redaction and sovereignty rules for the first real deployment evidence packets sent into the OFARM external evidence intake lane

---

## Primary rule

Redact identities and secrets without destroying semantic or audit meaning.
The packet must stay attributable enough to prove release identity, surface identity, binding posture, capture window, and trace-back lineage.

## Keep

Keep the smallest set that preserves evidence meaning:
- release bundle ref
- release label
- manifest / active-artifact / claim-set refs when present
- deployment scope ref
- surface contract ref when governed
- surface identity ref or implementation-local adapter surface ref
- controlled service-description refs
- observation or telemetry window
- collector identity as a stable controlled principal ref
- trace-back refs
- gate outcomes and timestamps
- deployment evidence refs or controlled audit-record refs

## Redact or control carefully

Redact or replace with stable controlled aliases when needed:
- internal hostnames that reveal sensitive infrastructure
- operator email addresses or phone numbers
- raw account names if a principal ref is enough
- tenant names when a stable tenant alias is enough
- free-form comments that reveal private operational details not needed for the evidence claim

## Never include

Do not include:
- raw bearer tokens
- passwords or API secrets
- session cookies
- private keys
- raw internal access-control tables when a governed grant or principal ref is enough
- unrelated payload rows that widen farm visibility beyond the evidence claim

## Runtime binding rule

Do **not** delete the runtime binding just because it is sensitive.
Either:
- keep the full binding when policy permits, or
- replace it with a stable controlled alias plus an internal sealed mapping outside the package, or
- preserve a binding hash/digest plus enough binding-shape context to prove which governed surface was observed

## Sovereignty reminder

An external evidence packet supports OFARM implementation proof.
It does **not** transfer authorship, governance authority, or unrestricted farm visibility to the package maintainer.
The farm or deployment operator remains the authority over the live operational system unless explicit governance artifacts say otherwise.
