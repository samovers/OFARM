import type { OFARMClient } from "../src/ofarm-client-shape";

// Candidate example only. Shows safe sequencing, not production code.
export async function goldenPath(client: OFARMClient) {
  const capabilities = await client.capabilities.get();

  const dryRun = await client.commits.dryRun({
    commitClass: "INTERVENTION_INTENT",
    payloadRef: "example:payload:prescription"
  });

  const submitted = await client.commits.submit(
    {
      commitClass: "INTERVENTION_INTENT",
      payloadRef: "example:payload:prescription"
    },
    {
      idempotencyKey: "example-prescription-001",
      humanApprovalRef: "approval:example:001"
    }
  );

  const query = await client.queries.execute({
    querySpecRef: "example:query:field-treatment-history",
    requireEvidence: true
  });

  const preview = await client.assemblies.dryRun({
    outputType: "PassportView",
    basisRefs: ["field:7"],
    requireFreshness: true
  });

  return { capabilities, dryRun, submitted, query, preview };
}
