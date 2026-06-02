# OFARM Governance Object Closure RFC v0.1

Date: 2026-04-18  
Status: accepted post-charter RFC  
Scope: close the machine-contract seam for OFARM-owned governance objects already named by RC2.1 and the harmonized Alignment Register

---

## 1. Problem statement

The active baseline and companion policy already require OFARM to preserve:
- `DataSovereigntyBoundary`
- `PackCompatibilityDeclaration`
- `PackMergePolicy`
- `PackExclusionRule`

That direction is correct.
The active machine layer still lacks first-class contracts for these governance objects.

Today:
- authority and pack-activation envelopes can mention these ideas by identifier or prose
- pack activation already carries `declaredCompatibilityRefs` and `declaredMergePolicyRefs`
- sharing and authorization flows already depend on a sovereignty boundary in policy terms
- the package does not yet define the governed source objects themselves

This RFC closes that seam with the smallest controlled patch.

---

## 2. Core stance

### 2.1 Governance objects remain explicit and separate
Sovereignty boundaries, compatibility declarations, merge policies, and exclusion rules remain governed source objects.
They are not hidden runtime flags.

### 2.2 Sharing does not erase sovereignty
A `DataSovereigntyBoundary` may constrain sharing or downstream use.
It does not silently convert sharing into authorship or write authority.

### 2.3 Compatibility and exclusion stay activation-set explainable
Pack activation outcomes remain explainable by governed declarations, merge policies, exclusion rules, and merge traces.
This RFC strengthens explainability without changing the pack law already adopted by the baseline and pack-merge RFC.

### 2.4 Minimum fields only
The contracts created here must carry only the minimum machine-verifiable fields needed for:
- identity
- governing party and scope
- time semantics
- compatibility/exclusion class
- merge-mode or boundary posture
- lifecycle state

This RFC does **not** create a full pack registry or legal-policy engine.

---

## 3. New contract families created by this RFC

This RFC creates these active machine-contract families in `03_machine_contracts/`:
- `OFARM_DataSovereigntyBoundary_schema_v0_1.json`
- `OFARM_PackCompatibilityDeclaration_schema_v0_1.json`
- `OFARM_PackMergePolicy_schema_v0_1.json`
- `OFARM_PackExclusionRule_schema_v0_1.json`

---

## 4. Contract minimums

### 4.1 DataSovereigntyBoundary minimums
A `DataSovereigntyBoundary` contract must be able to carry at least:
- stable boundary identifier
- governed scope
- owning or responsible party
- effective time
- default farm-side truth-control posture
- default cross-farm sharing posture
- default twin posture for regional intelligence
- boundary state

### 4.2 PackCompatibilityDeclaration minimums
A `PackCompatibilityDeclaration` contract must be able to carry at least:
- stable declaration identifier
- declaring party
- declaration time
- evaluated pack set
- target scope
- compatibility class
- linked merge or exclusion rules where relevant
- declaration state

### 4.3 PackMergePolicy minimums
A `PackMergePolicy` contract must be able to carry at least:
- stable merge-policy identifier
- declaring party
- declaration time
- affected pack set
- target scope
- surface family
- merge mode
- policy state

### 4.4 PackExclusionRule minimums
A `PackExclusionRule` contract must be able to carry at least:
- stable exclusion-rule identifier
- declaring party
- declaration time
- excluded pack set
- target scope
- exclusion reason
- exclusion state

---

## 5. Compatibility rule

Existing authority, sharing, pack-activation, and pack-merge trace contracts remain valid.
This RFC only requires that package-local examples may now point to governed package-local governance objects rather than leaving these identifiers unresolved.

The following additive linkages are allowed without breaking older examples:
- `SharingGrant` and `AuthorizationDecisionTrace` may carry optional `dataSovereigntyBoundaryRefs`
- `PackActivationRequest` may carry optional `declaredExclusionRuleRefs`
- `PackActivationResult` may carry optional references to the compatibility declarations, merge policies, or exclusion rules actually applied
- `PackMergeResolutionTrace` may carry optional references to the governing merge policy and compatibility declaration used for explanation

---

## 6. Out of scope

This RFC does not:
- create a full global legal code registry
- make every runtime policy decision depend on a single sovereignty object
- replace PackActivationSet or PackMergeResolutionTrace
- weaken deterministic pack-failure behavior

---

## 7. Outcome

After this RFC:
- pack activation can land on governed compatibility, merge, and exclusion objects
- sharing/authorization traces can point to an explicit sovereignty boundary where relevant
- the last remaining governance-object seams named by the active baseline become machine-closed inside the active contract set
