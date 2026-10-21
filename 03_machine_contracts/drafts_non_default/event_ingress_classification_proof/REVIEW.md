# Event Ingress construction review

The primary trust boundary is Event Ingress classification and evidence admission. The scope stayed inside it. This is conditional offline conformance, not runtime admission or production evidence.

The coordinator independently exercised the public checker with exact source and context bindings. Review found two timestamp normalization bugs: invalid offset minutes and hour 24 were accepted by the host parser. Explicit ASCII component ranges now reject both, and calendar validation rejects impossible dates. The independent 96-case report is retained in the implementation evidence lane. The owner suite passes 468 checks, including all seven event families, all nine commit classes and 63 conditional family/class combinations. Those combinations test interface neutrality; they do not invent promotion law or authorize every pairing.

The coordinator then made a mechanical source-layout repair so verbatim baseline excerpts reside in implementation evidence rather than the machine-contract lane. Original source bytes and their pins remain unchanged. The portable layout still works by default; repository integration explicitly supplies the source root. The complete installed 468-case suite and independent 96-case suite both pass. Independent review of that small mechanical diff has also been requested from the canonical interface owner.

All ten existing repository validation commands pass, including the transaction regression, hygiene, currentness, cross-reference and authority-order guardrails. The default validation suite, workflow files, active/default selections and source contracts remain unchanged. The new checker is opt-in. CI activation, runtime construction and merge remain separate.

Next: review this draft and let #47 bind its exact interfaces under the domain-owned contract; do not infer #47 completion from this prerequisite.
