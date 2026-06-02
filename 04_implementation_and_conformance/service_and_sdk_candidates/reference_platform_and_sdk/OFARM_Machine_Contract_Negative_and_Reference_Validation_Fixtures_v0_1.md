# OFARM machine-contract negative and reference validation fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact

---

## Scope

These fixtures extend the existing positive schema/example validation suite with bounded negative and cross-file checks.

They are package-local validation fixtures for `03_machine_contracts/`.
They do not alter machine-contract law.

---

## Fixture classes

### 1. Positive schema/example validation
The runner re-checks the full shipped schema/example set using inferred schema matching by file family.

### 2. Negative mutation validation
For each shipped schema family with at least one matching example, the runner creates one bounded in-memory invalid case by one of these strategies:
- remove a required top-level field
- break a top-level `const`
- break a top-level `enum`
- inject an illegal additional property when `additionalProperties: false` is in force

The expected outcome is validation failure.

### 3. Package-local reference consistency
The runner builds a package-local primary-id index from example artifacts and then scans example payloads for refs that currently resolve to that index.

For those resolvable refs, it records:
- source file
- ref path
- ref value
- matched target file(s)
- whether the target is unique or a controlled variant family

### 4. Broken-reference negatives
The runner mutates a bounded sample of unique package-local refs to missing values and confirms that they no longer resolve.

The expected outcome is failure to resolve.

---

## Boundaries

These fixtures intentionally ignore refs that are:
- external-system anchors
- deployment-time only
- not represented by package-local example ids

That boundary keeps the suite honest: it validates what the package can actually prove locally.
