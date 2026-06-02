# OFARM RC2.1 consistency report v0.1

Date: 2026-04-08  
Status: completed  
Scope: cross-check key concepts and boundaries between Constitution RC2.1 and Platform RC2.1 after RFC harmonization

---

## 1. Summary judgment

The RC2.1 pair is materially consistent enough to act as the new harmonized baseline.

No blocking contradiction was found in the main cross-document seams.

The remaining non-blocking asymmetries are intentional:
- Capability Manifest stays runtime-only
- Alignment Register stays unchanged for RFC-5
- several trace objects remain conceptually required before they are fully schematized

---

## 2. Checked seams

### 2.1 Truth model seam
Checked:
- assertion/history-first authority
- CurrentStateMaterialization
- MaterializationBasis / MaterializationSnapshot
- freshness states
- high-consequence recomputation/refusal rule

Result:
- Constitution and Platform are aligned.
- Platform realizes the stricter current-state rules without redefining them.

### 2.2 Query seam
Checked:
- QuerySpecification
- QueryPlanIR
- SemanticPathAlias
- graph-pattern-first / path-aware stance
- no public expert syntax in v2

Result:
- Constitution and Platform are aligned.
- QueryPlanIR stays runtime-only, QuerySpecification stays constitutional.

### 2.3 Pack seam
Checked:
- PackActivationSet
- PackSurfaceFamily
- PackSurfaceMergeMode
- PackMergeResolutionTrace
- same-precedence and cross-precedence rules

Result:
- Constitution defines the law.
- Platform defines runtime evaluation/trace.
- No blocking mismatch found.

### 2.4 Authority seam
Checked:
- AuthorityActionClass
- ScopeInheritanceMode
- AuthorityGrant / DelegationGrant / SharingGrant
- default deny
- human-only defaults for sensitive actions
- AuthorizationDecisionTrace

Result:
- Constitution and Platform are aligned.
- Platform enforcement matches the authority-law direction.

### 2.5 Output seam
Checked:
- PassportView
- DocumentAssembly
- ReportAssembly / DossierAssembly / SubmissionAssembly
- compiled-output separation

Result:
- Constitution and Platform are aligned.
- Platform uses the same taxonomy without reinterpreting it.

### 2.6 Capability seam
Checked:
- Capability Manifest must-ness
- runtime-only nature
- registry relation grounding
- manifest support in testability section

Result:
- Constitution intentionally does not own Capability Manifest semantics.
- Platform owns them explicitly.
- This asymmetry is intentional and acceptable.

---

## 3. Non-blocking follow-on gaps still visible

These are not new contradictions.
They are known remaining follow-ons for later work:

- PackMergeResolutionTrace does not yet have its own formal schema
- AuthorizationDecisionTrace does not yet have its own formal schema
- Materialization freshness policy still relies on baseline categories rather than a richer policy language
- manifest comparison logic is still a tooling concern more than a formal cross-deployment algorithm

These do not block RC2.1 harmonization.

---

## 4. Recommendation

Treat RC2.1 as the cross-RFC harmonized baseline pair.

Use it as the basis for:
- the reference implementation spike
- the final hostile review after gap closure
