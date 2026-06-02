# OFARM Sister Platform Boundary Policy v0.1

Date: 2026-04-21  
Status: active companion artifact  
Scope: define OFARM-side boundary rules for linked sister platforms so commerce, community, and adjacent domain systems can coexist with OFARM without hidden truth-store drift or silent authority expansion

---

## 1. Purpose

The active baseline, the interoperability policy, the compiled-output taxonomy, the durable relationship RFC, and the starter exchange-boundary RFC already make OFARM strong on truth, authority, sharing, and boundary traceability.

What remained missing was one explicit OFARM-side statement about **sister platforms as a family**.

This policy closes only that seam.
It answers:
- when a linked system should be treated as a sister platform rather than as a pack, profile, or local runtime adapter
- what OFARM must always retain
- what a sister platform may own
- what must cross the boundary explicitly
- what future sister-platform tenets must contain

This policy does **not** create:
- new OFARM twins
- new top-level commerce families inside OFARM
- new top-level social-network truth families inside OFARM
- silent promotion of sister-platform state into OFARM truth

---

## 2. Core stance

### 2.1 Sister platforms are adjacent domain peers
A sister platform is a linked domain system that has its own bounded truth and governance posture while remaining intentionally compatible with OFARM.

A sister platform is **not**:
- an OFARM pack
- an OFARM profile
- an OFARM runtime-surface adapter by itself
- an OFARM Advisory-Twin workspace
- a hidden cache that becomes the real source of OFARM truth

### 2.2 OFARM retains governed farm truth
OFARM remains the governing home for at least:
- farm-scoped identity, scope, and lifecycle meaning
- source truth records, accepted consequences, and governed current-state materialization
- authority, delegation, sharing, and prospective revocation
- evidence posture, review lineage, and promotion law
- PassportView, DocumentAssembly, SubmissionAssembly, and publication basis
- conformance, traceability, and audit lineage for OFARM-governed outputs

Sister platforms may reference these things through explicit boundary artifacts.
They must not silently replace them.

### 2.3 Sister platforms may own adjacent domain truth
A sister platform may own truth that is causally related to farming but not identical to OFARM’s governed farm truth.

Typical examples include:
- conversation, group, moderation, and reputation state
- offer, counteroffer, order, and contract process state
- delivery appointment, commercial dispute, and settlement-summary state
- payment-rail references or payout references where applicable

Owning that truth outside OFARM is allowed.
Letting that truth silently mutate OFARM meaning is not.

### 2.4 No silent boundary effects
The following are prohibited by default:
- contract existence silently granting OFARM access
- group membership silently granting OFARM access
- social popularity or repeated rumours silently becoming OFARM evidence or compliance truth
- order acceptance silently mutating lot identity, operational truth, or accepted execution truth
- payment completion silently confirming delivery truth, claim truth, or compliance truth
- external dispute state silently superseding OFARM review lineage

### 2.5 Explicit boundary artifacts only
Sister-platform interaction with OFARM must resolve through explicit governed artifacts such as:
- `SharingGrant`
- `DelegationGrant` where actual on-behalf-of action is allowed
- `ExternalCommitmentLink`
- `ContractReference`
- `CrossPlatformGrantReceipt`
- publication request/result traces
- recipient-shaped `PassportView` or `DocumentAssembly` outputs
- review/governance artifacts when external challenge or correction requires OFARM action

The boundary may later gain more artifacts, but the default posture remains explicit, typed, and auditable.

### 2.6 Sister platforms do not collapse sharing, authority, and relationship
Sister-platform presence does not remove OFARM’s core separation among:
- relationship context
- authority to act
- delegation to act on behalf of another party
- sharing or read access

This separation remains non-negotiable.

---

## 3. Recognized initial sister-platform lanes

### 3.1 OFARM Exchange
OFARM Exchange is the first higher-risk sister-platform lane.
It is the natural home for:
- offers
- buyer/seller inquiries
- orders
- negotiated contracts
- delivery scheduling
- dispute case handling on the commercial side
- settlement summaries and payment references

OFARM Exchange is intentionally **not** the home for farm-scoped operational truth, accepted execution truth, or OFARM authority law.

### 3.2 OFARM Social
OFARM Social is the first community/advisory-network sister-platform lane.
It is the natural home for:
- social discussion
- groups and communities
- peer alerts and local warnings
- moderation state
- social reputation and conversational activity

OFARM Social is intentionally **not** the home for OFARM compliance truth, accepted evidence, or final authority decisions.

### 3.3 Regulated payment rails remain outside OFARM core
Payment execution, regulated money movement, and similar financial-service functions should remain outside OFARM core.
A sister platform such as OFARM Exchange may integrate with such services, but OFARM should receive only the references it actually needs.

---

## 4. Boundary rules

### 4.1 Outbound OFARM → sister platform
When OFARM supplies data or outputs to a sister platform, the outbound act must preserve:
- recipient identity or counterpart identity
- purpose or contract basis where relevant
- scope and twin posture
- freshness/materialization basis where high consequence is possible
- expiry or revocation posture where access is time-bounded
- output/publication lineage

### 4.2 Inbound sister platform → OFARM
Inbound sister-platform material may:
- request access
- request publication
- carry references to external contracts, discussions, or disputes
- carry candidate evidence or source references
- trigger review or follow-up work

Inbound sister-platform material may **not** by itself:
- become accepted OFARM truth
- create authority
- bypass OFARM review/promotion law
- override OFARM current-state materialization

### 4.3 Identity, purpose, and currentness must stay visible
Cross-platform use must not rely on vague “the partner has access” posture.
The system must be able to explain:
- which party or platform identity is involved
- which purpose or relationship justifies the linkage
- whether the data is live, frozen, or stale-sensitive
- whether the source grant is still valid

### 4.4 Review remains the correction path
If a sister platform challenges, contests, or updates something that matters to OFARM truth, the path forward is an explicit OFARM review/governance path.
The sister platform may raise the issue.
OFARM decides whether truth changes.

### 4.5 No bypass through cross-platform caching
A sister platform may retain its own domain history and references.
It may not become a hidden authoritative mirror of OFARM by convenience, UI habit, or local caching.

---

## 5. Minimum contents of sister-platform tenets

Before a deeper sister-platform constitution is written, the platform should at least publish a tenets document that states:
- what truth that platform owns
- what truth remains in OFARM
- which boundary artifacts are expected
- which cross-boundary effects are prohibited by default
- what identity and consent/currentness posture applies
- how disputes or corrections return to OFARM
- what implementation trigger would justify a deeper constitution or runtime-law pass

This is the preferred first step.
It establishes the architectural picture without pretending that the sister platform already has mature implementation law.

---

## 6. Current package posture

In the current package:
- OFARM-side sister-platform boundary law lives in the active OFARM authority set, including this policy and the accepted boundary RFCs
- linked-domain family framing and sister-platform constitutional tenets live in `07_linked_domain_architectures/` as **active supporting context**
- those linked-domain documents help readers and future agents understand the high-level picture, but they do **not** override OFARM baseline or RFC law
- OFARM Exchange is the first sister-platform lane that should receive deeper treatment if an implementation trigger appears
- OFARM Social is intentionally established now at the tenets level rather than being left implicit

---

## 7. What this policy does not do

This policy does **not**:
- standardize offers, orders, or social objects as native OFARM artifact families
- create OFARM-native payment execution
- force a full constitution for every imagined sister platform
- promote social-signal starter contracts into active law before a real trigger exists
- demote the existing OFARM authority, evidence, review, or publication model
