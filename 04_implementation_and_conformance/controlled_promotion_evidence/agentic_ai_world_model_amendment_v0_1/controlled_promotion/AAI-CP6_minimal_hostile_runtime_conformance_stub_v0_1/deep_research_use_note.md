# Deep Research use note

CP6 uses `source_inputs/deep-research-report-30.md` as supporting context only. The report warns that manifests, handoffs, world-model state, requests, and successful tool calls can create semantic-laundering risk if they are treated as authority, evidence, current state, obligations, or governance success.

CP6 operationalizes that warning by testing hostile cases in which tool success is separated from governance success; handoff context does not transfer authority; world-model state cannot materialize current state; EvidenceNeed and ObservationRequest remain weak request objects; revocation is rechecked before sharing and offline replay; manifest overclaims are blocked; and result qualifications remain visible.

This note does not promote any Deep Research recommendation into active law.
