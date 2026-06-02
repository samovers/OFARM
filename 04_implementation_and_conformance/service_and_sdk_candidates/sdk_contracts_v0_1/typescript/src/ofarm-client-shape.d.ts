// OFARM TypeScript SDK candidate shape v0.1.
// Implementation/conformance support only.

export type OperationId =
  | "capabilities.get"
  | "authority.preflight"
  | "commits.dryRun"
  | "commits.submit"
  | "evidence.register"
  | "queries.plan"
  | "queries.execute"
  | "materializations.get"
  | "assemblies.dryRun"
  | "assemblies.create"
  | "corrections.submit"
  | "disputes.submit"
  | "identity.resolve"
  | "imports.submitCandidate"
  | "imports.lossMap.get"
  | "sync.replay"
  | "calculations.preview"
  | "contracts.openapi.get"
  | "contracts.asyncapi.get"
  | "contracts.schema.get"
  | "contracts.problems.get"
  | "sdk.codegenManifest.get";

export type RuntimeProblemCode =
  | "AUTHORITY_DENIED"
  | "HUMAN_APPROVAL_REQUIRED"
  | "EVIDENCE_INSUFFICIENT"
  | "IDENTITY_UNRESOLVED"
  | "UNIT_UNRESOLVED"
  | "PRODUCT_BINDING_UNRESOLVED"
  | "MATERIALIZATION_STALE"
  | "MATERIALIZATION_INVALID"
  | "DISPUTE_OPEN"
  | "CORRECTION_REQUIRED"
  | "PACK_CONFLICT"
  | "IMPORT_CANDIDATE_ONLY"
  | "SOURCE_FIDELITY_LOSS"
  | "LOSS_MAP_REQUIRED"
  | "HIGH_CONSEQUENCE_BLOCKED"
  | "PERMISSION_REDACTED"
  | "RETRY_CONFLICT"
  | "IDEMPOTENCY_REPLAY_CONFLICT";

export interface RuntimeProblem {
  reasonCode: RuntimeProblemCode;
  severity: "INFO" | "WARNING" | "ERROR" | "BLOCKER";
  title: string;
  detail?: string;
  traceRef?: string;
  suggestedRemediation?: string[];
}

export interface QualifiedResult<T> {
  data: T;
  qualification: {
    asOf?: string;
    stalenessClass?: string;
    disputeStatus?: string;
    evidenceSufficiency?: string;
    permissionClass?: string;
    candidateStatus?: string;
    traceRef?: string;
  };
  problems?: RuntimeProblem[];
}

export interface OFARMClient {
  capabilities: {
    get(): Promise<QualifiedResult<unknown>>;
  };
  authority: {
    preflight(request: unknown): Promise<QualifiedResult<unknown>>;
  };
  commits: {
    dryRun(request: unknown): Promise<QualifiedResult<unknown>>;
    submit(request: unknown, options: { idempotencyKey: string; humanApprovalRef?: string }): Promise<QualifiedResult<unknown>>;
  };
  evidence: {
    register(request: unknown, options?: { idempotencyKey?: string }): Promise<QualifiedResult<unknown>>;
  };
  queries: {
    plan(request: unknown): Promise<QualifiedResult<unknown>>;
    execute(request: unknown): Promise<QualifiedResult<unknown>>;
  };
  materializations: {
    get(scope: string, options?: { requireFreshness?: boolean }): Promise<QualifiedResult<unknown>>;
  };
  assemblies: {
    dryRun(request: unknown): Promise<QualifiedResult<unknown>>;
    create(request: unknown, options: { idempotencyKey: string; humanApprovalRef?: string }): Promise<QualifiedResult<unknown>>;
  };
  identity: {
    resolve(request: unknown): Promise<QualifiedResult<unknown>>;
  };
  imports: {
    submitCandidate(request: unknown, options: { idempotencyKey: string }): Promise<QualifiedResult<unknown>>;
    lossMap(importReceiptRef: string): Promise<QualifiedResult<unknown>>;
  };
  sync: {
    replay(request: unknown, options: { idempotencyKey: string }): Promise<QualifiedResult<unknown>>;
  };
  calculations: {
    preview(request: unknown): Promise<QualifiedResult<unknown>>;
  };
  traces: {
    get(traceType: string, traceId: string): Promise<QualifiedResult<unknown>>;
  };
}

// Intentionally absent:
// - saveCanonicalAssertion
// - updateMaterializationStore
// - markAcceptedExecution
// - promoteAdvisoryOutputToComplianceFact
// - genericCrudClientForTruthObjects
