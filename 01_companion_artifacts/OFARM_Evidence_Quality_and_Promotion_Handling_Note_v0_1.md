# OFARM Evidence Quality and Promotion Handling Note v0.1

Date: 2026-04-14  
Status: active companion artifact  
Scope: make weak-but-real farm evidence, later evidence upgrade, and post-output supersession handling more executable without changing OFARM truth law

---

## 1. Purpose

OFARM already has the correct constitutional stance:
- weak inputs must not auto-promote into stronger in-force truth
- high-consequence paths must pass evidence sufficiency and freshness rules
- late evidence must not rewrite history
- frozen outputs remain distinct from canonical truth

What is still missing is a tighter pattern for the most common real-farm evidentiary problem:

**the evidence exists, but it is degraded, partial, late, ambiguous, or contradictory.**

This note closes that gap without reopening event grammar, commit classes, or truth law.

---

## 2. Core stance

### 2.1 Poor evidence is still evidence
OFARM must not collapse all non-ideal evidence into “missing”.

Examples:
- notebook text with a local product name
- OCR-derived label text without a clean product identifier
- partial machine task export
- scanned ticket with record time but unclear event time
- human report with no machine file yet
- machine record with no human confirmation yet

These are weak, but they are not the same as nothing.

### 2.2 Weak evidence may justify weaker commit classes, not stronger in-force results
Weak or degraded evidence may justify:
- `note`
- `observation assertion`
- `hypothesis assertion`
- `operation claim`
- `evidence record`

It must not silently justify:
- accepted executed intervention consequence
- compliance fact
- attested dossier/document path
- formal submission filing

unless the declared promotion path and policy posture say the additional support is sufficient.

### 2.3 Late evidence strengthens history; it does not erase history
When better evidence arrives later, OFARM should:
- preserve earlier record time and earlier weaker posture
- add the stronger evidence through the normal review/promotion path
- create supersession or a new in-force result where justified
- create a new frozen output version when a frozen output was already assembled

The system must not act as though the earlier weak state never existed.

### 2.4 Human-versus-machine contradiction is a governed state, not a silent tie-breaker
Where human-reported and machine-generated evidence disagree, the platform should preserve that contradiction explicitly and route according to policy.

No silent rule such as “machine always wins” or “farmer always wins” should exist outside governed policy.

---

## 3. Evidence-quality evaluation axes

This note introduces five evaluation axes that may be applied inside `EvidenceSufficiencyCase` reasoning and in implementation-side promotion logic.

These are **evaluation dimensions**, not new constitutional truth layers.

### 3.1 Source specificity
- `EXACT_REFERENCE`
- `AMBIGUOUS_REFERENCE`
- `FREE_TEXT_ONLY`
- `NO_IDENTIFYING_REFERENCE`

### 3.2 Capture integrity
- `ORIGINAL_OR_DURABLE_REF`
- `SCANNED_OR_PHOTO_CAPTURE`
- `OCR_OR_TRANSCRIBED_ONLY`
- `MEMORY_ONLY`

### 3.3 Chronology integrity
- `EVENT_TIME_EXACT`
- `EVENT_TIME_BOUNDED`
- `RECORD_TIME_ONLY`
- `UNDATED_OR_LATE_UNBOUNDED`

### 3.4 Cross-source agreement
- `CONSISTENT_MULTI_SOURCE`
- `HUMAN_ONLY`
- `MACHINE_ONLY`
- `PARTIAL_AGREEMENT`
- `CONFLICTING`

### 3.5 Late-arrival posture
- `ON_TIME`
- `LATE_PRE_DECISION`
- `LATE_POST_DECISION`
- `LATE_POST_OUTPUT`
- `LATE_POST_SUBMISSION`

---

## 4. Promotion-handling rules

### 4.1 Weak evidence default
If evidence posture is degraded on one or more axes and OFARM lacks an explicit stronger promotion path, the default is:
- keep the weaker class
- route to review where policy allows
- refuse the stronger path where policy requires

### 4.2 Ambiguous product/input identity rule
Where a regulated or claim-relevant input cannot be identified precisely enough, OFARM may keep an `operation claim` and supporting `evidence record`, but should not create a compliance fact or compliant submission path from that ambiguity alone.

### 4.3 Partial machine-record rule
Partial machine records may support a claim, but they should not by themselves erase or outrank human-reported remainder data unless a governed rule says so.

### 4.4 Late evidence before decision
If stronger evidence arrives before final review or promotion, OFARM may use it to strengthen the path while preserving earlier record time and earlier evidence posture.

### 4.5 Late evidence after frozen output
If stronger evidence arrives after a frozen output was assembled, OFARM should:
- preserve the prior output and its basis
- create a new review/supersession path
- create a new output version if policy allows
- preserve explicit linkage between old and new output

### 4.6 Late evidence after formal submission
If stronger evidence arrives after a formal submission, OFARM should:
- preserve the original submission package and basis snapshot
- create a correction/supersession pathway
- file or stage a new submission package according to authority and policy

This is the strongest version of the no-edit-in-place rule.

---

## 5. Suggested narrow machine-contract extension

This note does not require a new constitutional artifact family.
It does justify a narrow extension of `OFARM_EvidenceSufficiencyCase` during implementation.

### 5.1 Suggested additions to bundle-level structure
Suggested optional fields for a `v0.2` machine-contract draft:
- `sourceSpecificity`
- `captureIntegrity`
- `chronologyIntegrity`
- `crossSourceAgreement`
- `lateArrivalPosture`

### 5.2 Suggested additions to insufficiency reason codes
Add narrow reason codes for the farm-reality cases that currently disappear into generic notes:
- `AMBIGUOUS_PRODUCT_ID`
- `TIMESTAMP_INCOMPLETE`
- `SOURCE_QUALITY_LOW`
- `MACHINE_RECORD_PARTIAL`
- `HUMAN_MACHINE_CONFLICT`
- `LATE_EVIDENCE_POST_OUTPUT`
- `LATE_EVIDENCE_POST_SUBMISSION`

### 5.3 Why a narrow extension is enough
This gives implementations a common vocabulary for degraded evidence without creating a second evidence ontology.

---

## 6. Mandatory fixture families

A conforming implementation should add at least these scenario fixtures:
1. ambiguous PPP identity upgrade
2. partial machine log plus manual top-up
3. late lab result after intervention
4. late evidence after frozen output
5. late evidence after formal submission

---

## 7. Risks and guardrails

### 7.1 Risks if over-implemented
Do not let these evaluation axes become an ungoverned scoring engine. The point is not to invent a universal confidence number.

### 7.2 Risks if under-implemented
If these axes remain implicit, every deployment will make different decisions about the same weak evidence.

### 7.3 Non-goal
This note does **not** legalize weak evidence for high-consequence paths by default. It makes the weakness explicit so the system can refuse or escalate consistently.
