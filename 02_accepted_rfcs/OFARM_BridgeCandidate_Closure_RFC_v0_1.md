
# OFARM BridgeCandidate Closure RFC v0.1

Date: 2026-04-19
Status: accepted post-charter RFC
Scope: promote the narrow Advisory-to-governed-action bridge handoff seam into the active machine-contract set without promoting the full scenario-workspace object family

---

## 1. Problem statement

The active baseline, the Advisory scenario workspace companion note, the current-state materialization RFC, and the compiled-output taxonomy already require all of the following to be true:
- Advisory-origin outputs may inform governed next steps
- Advisory-origin outputs may not directly mutate Compliance truth or accepted executed consequences
- bridge progression is human-gated by default
- high-consequence downstream use must re-enter normal enforcement and freshness law
- live PassportViews may not be silently treated as frozen attestable document outputs

That direction is already correct.
What remains open is the smallest executable handoff object that carries an Advisory-origin recommendation into a governed next-step path without silently becoming truth.

Today:
- `01_companion_artifacts/OFARM_Advisory_Scenario_Workspace_and_Bridge_Note_v0_2.md` defines `BridgeCandidate` as the right narrow object
- `04_implementation_and_conformance/conformance_runners/advisory_and_economic_benchmark/OFARM_Advisory_Scenario_Contracts_Candidate_v0_1.md` preserves the experimental scenario-workspace contract family
- an experimental BridgeCandidate schema already exists in the economic-intelligence spike
- the active machine-contract set still lacks a governed bridge-handoff contract

This RFC closes only that narrow seam.

---

## 2. Core stance

### 2.1 Narrow promotion only
This RFC promotes only the `BridgeCandidate` handoff seam.
It does **not** promote:
- `ScenarioSpec`
- `ScenarioResultSet`
- `ImportedFactExtract`
- `AllocationBasisDeclaration`
- or a new constitutional artifact family for the whole scenario workspace

### 2.2 BridgeCandidate remains proposal-shaped
A BridgeCandidate is never:
- a compliance fact
- an accepted executed intervention consequence
- a review decision
- an attested document
- a filed submission
- or a hidden auto-execution instruction

It remains a proposal-shaped Advisory object that points toward a governed next step.

### 2.3 Human gate is mandatory in the active contract
The active contract must make the human-gated posture machine-visible.
A valid BridgeCandidate may not represent a soft autopilot path.

### 2.4 Compliance-targeted handoff must declare recheck posture
If a BridgeCandidate points toward a Compliance-targeted next step, it must explicitly declare that Compliance freshness must be rechecked before downstream progress.
This preserves the baseline rule that Advisory staleness may be acceptable for exploration but not for governed bridge actions.

### 2.5 The next step still enters the normal enforcement chain
Promotion of `BridgeCandidate` does not create a special bridge shortcut.
The downstream path still resolves through normal OFARM enforcement, authority, evidence, materialization, review, and publication law.

---

## 3. New contract family created by this RFC

This RFC creates one active machine-contract family in `03_machine_contracts/`:
- `OFARM_BridgeCandidate_schema_v0_1.json`

---

## 4. Contract minimums

A valid active `BridgeCandidate` contract must be able to carry at least:
- stable bridge candidate identifier
- creation time
- source twin, fixed to Advisory
- proposal-only posture
- source scenario-result reference
- optional source scenario-spec reference
- proposed next-step class
- intended next twin for the governed next step
- target scope set
- mandatory human-approval requirement
- explicit recheck requirements for the downstream path
- optional source materialization/context references where the scenario relied on current state or context
- optional proposed draft artifact reference
- rationale and optional prerequisite references

---

## 5. Compatibility rule

The broader Advisory scenario-workspace note remains active companion guidance.
The implementation candidate contract packet in `04_implementation_and_conformance/` also remains valid as support material for the still-unpromoted scenario-workspace objects.

After this RFC:
- the narrow BridgeCandidate handoff contract is active substance
- the remaining scenario-workspace objects stay implementation/conformance candidates until separately promoted

---

## 6. Out of scope

This RFC does not:
- standardize the full scenario-workspace schema family
- promote imported economic or accounting extracts
- create a second query language
- allow automatic promotion from scenario output to accepted consequence
- redefine PassportView or DocumentAssembly taxonomy
- change baseline twin law

---

## 7. Outcome

After this RFC:
- BridgeCandidate becomes a governed active machine contract
- the package can prove a hostile Advisory-to-execution-to-passport path without relying on prose alone
- the remaining scenario-workspace object family stays bounded and experimental rather than being promoted in a single jump
