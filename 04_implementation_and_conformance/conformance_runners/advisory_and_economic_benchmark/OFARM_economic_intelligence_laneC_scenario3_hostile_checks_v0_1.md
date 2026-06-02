# OFARM economic intelligence Lane C — hostile checks v0.1

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: explicit hostile checks for Scenario-3 capex pre-gate screening

## Immediate fail conditions

- any NPV / IRR / payback / DSCR wording appears in positive lane-c result sets,
- any positive lane-c result uses approval or lender-ready wording,
- the scenario requests a SubmissionAssembly instead of a DossierAssembly,
- the bridge skips human approval,
- the bridge does not require external appraisal,
- stale result sets are treated as export-ready for the pre-gate dossier,
- crop margin positivity is used as a capex approval shortcut.

## Additional caution checks

- working-capital numbers stay explicitly assumption-shaped,
- financing-term extracts stay preliminary and extract-shaped,
- energy and settlement extracts stay evidence-linked and non-ledger,
- result notes continue to say screening only / not financing truth.
