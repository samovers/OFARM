
# OFARM ONT-SEMINT Baseline Harmonisation Fixtures v0.1

Date: 2026-05-14  
Status: active supporting implementation/conformance  
Phase: ONT-SEMINT Phase 6

## Purpose

These fixtures verify that ONT-SEMINT Phases 0 through 5 were reflected into the active baseline without reopening the architecture.

## Required baseline reflection

The active baseline must now mention, at minimum:

- schema validation versus semantic conformance;
- package-local reference resolution;
- externally anchored references and currentness verification;
- ReferenceResolutionManifest, ReferenceResolutionFinding, and ReferenceResolutionReport;
- TemporalFieldConformanceMatrix;
- ExternalRegistryVerificationTrace;
- canonical agronomic carrier fields `agronomicIdentityBindingRefs` and `agronomicCodeBindingProfileRef`;
- compatibility-field conflict behavior for `identityBindingRefs` and `codeBindingProfileRef`;
- distinct time meanings for observation, occurrence, capture, assertion, sync, review, correction, materialization, and output;
- high-consequence alias version pinning with `aliasVersionRef`;
- PassportView review/refusal behavior;
- DocumentAssembly annex behavior;
- Belgium/Phytoweb profile as a narrow package-local profile/conformance closure;
- non-claims for live registry integration, production runtime readiness, external-standard readiness, legal advice, livestock scope expansion, and wire-level interoperability.

## Expected outcome

`PASS` when all baseline reflection checks pass.
