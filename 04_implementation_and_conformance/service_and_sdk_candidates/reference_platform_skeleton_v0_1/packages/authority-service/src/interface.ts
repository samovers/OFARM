// authority-service candidate interface boundary.
// Implementation/conformance support only.

export interface AuthorityServicePort {
  readonly moduleId: "authority-service";
  health(): Promise<{ status: "ok" | "degraded"; traceRef?: string }>;
}

// Forbidden in this module boundary:
// - direct writes to canonical assertion store outside governed ingress/promotion
// - direct writes to materialization store from app clients
// - implicit authority decisions without Authority Service trace
// - hidden promotion of advisory output or import candidates
