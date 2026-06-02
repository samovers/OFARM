from ofarm_client_shape import OFARMClient


def golden_path(client: OFARMClient):
    capabilities = client.capabilities_get()

    dry_run = client.commits_dry_run({
        "commitClass": "INTERVENTION_INTENT",
        "payloadRef": "example:payload:prescription"
    })

    submitted = client.commits_submit(
        {
            "commitClass": "INTERVENTION_INTENT",
            "payloadRef": "example:payload:prescription"
        },
        idempotency_key="example-prescription-001",
        human_approval_ref="approval:example:001",
    )

    query = client.queries_execute({
        "querySpecRef": "example:query:field-treatment-history",
        "requireEvidence": True
    })

    preview = client.assemblies_dry_run({
        "outputType": "PassportView",
        "basisRefs": ["field:7"],
        "requireFreshness": True
    })

    return {
        "capabilities": capabilities,
        "dry_run": dry_run,
        "submitted": submitted,
        "query": query,
        "preview": preview,
    }
