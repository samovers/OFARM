# Event Ingress construction reviews

The primary trust boundary is Event Ingress classification and evidence admission. The scope stayed inside it. This is conditional offline conformance, not runtime admission or production evidence.

## Historical construction reviews

The coordinator independently exercised the public checker with exact source and context bindings. Review found two timestamp normalization bugs: invalid offset minutes and hour 24 were accepted by the host parser. Explicit ASCII component ranges now reject both, and calendar validation rejects impossible dates. The independent 96-case report is retained in the implementation evidence lane. The owner suite passes 468 checks, including all seven event families, all nine commit classes and 63 conditional family/class combinations. Those combinations test interface neutrality; they do not invent promotion law or authorize every pairing.

The coordinator then made a mechanical source-layout repair so verbatim baseline excerpts reside in implementation evidence rather than the machine-contract lane. Original source bytes and their pins remain unchanged. The portable layout still works by default; repository integration explicitly supplies the source root. The complete installed 468-case suite and independent 96-case suite both pass. The canonical interface owner independently reviewed the mechanical diff: all 18 checks passed, with no findings. The exact review conclusion and case reports are retained in the implementation evidence lane. That review covers the source-root change and unchanged R2 semantics; it is not a new full original-owner conformance review.

All ten existing repository validation commands pass, including the transaction regression, hygiene, currentness, cross-reference and authority-order guardrails. The default validation suite, workflow files, active/default selections and source contracts remain unchanged. The new checker is opt-in. CI activation, runtime construction and merge remain separate.

The diff whitespace check reports only inherited Markdown hard-break whitespace in the byte-identical constitution, platform and event-grammar source copies. Those bytes are retained to preserve their source hashes; authored files have no whitespace errors.

## Corrections to the 19 November 2026 review

The [submitted review](https://github.com/samovers/OFARM/pull/49#pullrequestreview-5982712179) covered `2cf45bef00bcdd5e865973535646a9db8b47267d`. Its 468 passing local checks, exact baseline reproduction, nine source-copy comparisons, schema/code pin checks and passing repository suite remain credited to that head. It found two blockers: disagreement between the pinned JSON and frozen report schemas was unchecked at runtime, and the documentation misstated the committed evidence and source layout.

B1 is corrected by rejecting an incompatible pinned report schema with `DEPENDENCY_UNAVAILABLE` / `REPORT_SCHEMA_MISMATCH` before input evaluation. The frozen schema still validates early diagnostics when optional dependencies cannot load. The helper now explains this supported format and the required equality instead of referring to an absent generator. Contract code hashes, its self-digest and all five dependent fictional fixture selections are refreshed. Source schemas, original event/request bytes, semantic sources and historical review evidence are unchanged.

Two additional regression cases select coherently re-pinned contracts and input bindings: one report schema adds a required field; the other broadens the status enum. Both now fail closed. The updated local suite passes 470 checks, and the earlier 468 outcome rows remain identical. The committed compact catalogue and baseline report record the corrected suite; they are not used as its oracle.

B2 is corrected in `PROPOSAL.md` and `PORTABLE_USAGE.md`: committed inputs and compact reports are distinguished from generated output, the repository command supplies the fixture lane as `--source-root`, portable assembly uses only committed files, and obsolete publication steps and unavailable-file instructions are removed. Historical review records keep their original scope and pins; their wider local snapshot seal is not claimed as a complete committed archive.

The baseline-copy size question remains a nonblocking follow-up. Redundant predicates, identifier patterns, summary-count derivation and the dead fallback remain preferences outside this correction. The reviewer requested hosted validation and a fresh exact-head review; local checks do not satisfy hosted validation. Existing workflow files, default runner registration and current/default selections remain unchanged. No CI activation, source adoption or merge is authorized by this correction.

Next: independently recheck B1/B2 at the corrected head, then obtain the separate hosted-validation and canonical-acceptance decisions. Any consumer re-pin belongs in its own boundary. #47's existing offline-use scope is unchanged; #456 remains held until accepted canonical main bytes are available.
