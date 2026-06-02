# OFARM Farm-Owner Consolidated Evidence Posture v0.1

Generated: 2026-05-13T17:53:02+00:00

## Evidence classes

| Evidence class | Meaning | Current status |
|---|---|---|
| Repository-authored rehearsal | Internal fixtures, runners, examples, dry runs | Present; useful for pilot readiness only |
| Real external record reconstruction context | Redacted FMIS/Codex evidence based on existing non-OFARM records | Present; import/gap evidence only |
| Source-owner closure evidence | Operational source-owner proof for documents, reports, performer relation, audit trail, export | Missing |
| Live OFARM runtime evidence | OFARM-compatible runtime used during real farm work | Missing |

## No-overclaim rule

Repository-authored rehearsals cannot become live evidence. Existing FMIS records cannot become live OFARM runtime evidence. Report marts cannot become frozen `DocumentAssembly` outputs unless the issued-report/share/submission system proves basis, recipient, immutability, and supersession state. Document references cannot become `EvidenceBundle` objects without custody-grade binary/hash/version/uploader/export proof.

## Current evidence classification

```text
REAL_EXTERNAL_RECORD_RECONSTRUCTION_CONTEXT
```

## Current blocked upgrade

No readiness upgrade is allowed until owner evidence or live runtime evidence arrives.
