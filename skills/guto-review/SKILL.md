---
name: guto-review
description: Reviews a verified change for correctness, omitted context, maintainability, security, and performance before merge. Use only after guto-verify has produced current evidence for the approved plan version.
---

# Guto Review

## Purpose

Decide whether a verified change is ready for merge. Review must independently reconstruct the relevant project context so it can find gaps that Planning, Build, or Verify missed.

## Local Child-Skill Contract

Every child skill is vendored as a sibling under `skills/`.

For each child:

1. Resolve the sibling path relative to this file.
2. Read the complete `SKILL.md` before using it.
3. Apply the workflow within this read-only review boundary.
4. If a required local file is missing, return `STATUS: BLOCKED`. Do not use an external or remembered substitute.

## Exact Skill Set

This skill may call only:

- [`context-engineering`](../context-engineering/SKILL.md) — mandatory, first, fresh on every review
- [`code-review-and-quality`](../code-review-and-quality/SKILL.md) — mandatory
- [`code-simplification`](../code-simplification/SKILL.md) — conditional
- [`security-and-hardening`](../security-and-hardening/SKILL.md) — conditional
- [`performance-optimization`](../performance-optimization/SKILL.md) — conditional

No other skill may be loaded or invoked.

## Preconditions

Require:

- an approved plan version;
- the implementation or diff under review;
- current `guto-verify` evidence for that implementation state;
- access to the surrounding project context.

If verification is absent or stale relative to the code, return `STATUS: VERIFICATION_REQUIRED`.

## Step 1 — Mandatory Independent Context Engineering

Always read and execute `context-engineering` first. It may not be skipped, reused as-is, or replaced by Planning or Build summaries.

The review context pass must independently inspect:

- the original request and approved plan;
- scope, non-goals, decisions, assumptions, and acceptance criteria;
- the complete diff and every changed file;
- surrounding callers, consumers, interfaces, schemas, and tests;
- existing canonical implementations and reusable patterns;
- related configuration, migrations, data flows, or runtime behavior;
- relevant issues, pull requests, and recent conflicting changes when available;
- verification evidence and what it did not cover.

Its explicit purpose is to detect missing context: affected code not included in the plan, an existing abstraction not reused, a consumer overlooked, a contract mismatch, a stale assumption, or a test surface omitted earlier.

Produce a `CONTEXT_GAP_AUDIT` with:

```text
EXPECTED_SURFACE:
ACTUAL_SURFACE:
ADDITIONAL_RELEVANT_CONTEXT:
OMITTED_OR_STALE_CONTEXT:
IMPACT_ON_PLAN_OR_CHANGE:
```

If a context gap invalidates objective, scope, architecture, public contract, or acceptance criteria, return `STATUS: REPLAN_REQUIRED`.

## Step 2 — Mandatory Code Review

Read and execute `code-review-and-quality` against the reconstructed context, verified evidence, and actual change.

Review correctness first, then readability, architecture, security, performance, and verification quality. Findings must identify:

- severity;
- concrete evidence and location;
- affected behavior or contract;
- why it matters;
- required remedy or named structural move;
- whether it requires Build, Verify, or Planning.

Do not block for stylistic preference or unrelated cleanup.

## Step 3 — Conditional Specialist Passes

After the primary review, classify each specialist skill as `USE` or `SKIP`.

### `code-simplification`

Use when the change works but introduces or preserves material avoidable complexity, duplication, deep nesting, unclear boundaries, or an abstraction that does not earn its cost.

Skip when the code is already clear or simplification would be cosmetic churn.

### `security-and-hardening`

Use when the change touches any trust boundary, untrusted input, authentication, authorization, secrets, sensitive data, storage, files, webhooks, external services, permissions, dependency supply chain, or LLM/tool execution.

Skip only when none of those surfaces are present.

### `performance-optimization`

Use when there is a performance requirement, measured or suspected regression, hot path, high-volume query, large dataset, critical latency path, or material frontend runtime impact.

Skip when no performance claim or plausible material regression exists. It is measure-first; do not invent performance findings without evidence.

Record the trigger and decision for all three.

## Read-Only Boundary

Review does not implement fixes, simplify code, harden code, or optimize code directly. A specialist skill is used to identify and specify the required change. Mutation returns to `guto-build`, followed by renewed `guto-verify` and a targeted review of the affected surface.

## Finding Disposition

Use:

- `CRITICAL` — security vulnerability, data loss, broken correctness, or other merge blocker
- `REQUIRED` — material issue that must be fixed before merge
- `OPTIONAL` — useful improvement that does not block merge
- `NIT` — minor style preference
- `FYI` — information only

Only `CRITICAL` and `REQUIRED` block `MERGE_READY`.

A finding that changes the approved planning contract returns to `guto-plan`. A code-level remedy returns to `guto-build`.

## Output

End with exactly one status:

- `STATUS: MERGE_READY`
- `STATUS: FIX_REQUIRED`
- `STATUS: REPLAN_REQUIRED`
- `STATUS: VERIFICATION_REQUIRED`
- `STATUS: BLOCKED`

For `MERGE_READY`, include:

```text
PLAN_VERSION: <number>
CONTEXT_ENGINEERING: EXECUTED_FRESH
CONTEXT_GAPS: none material
PRIMARY_REVIEW: PASSED
SIMPLIFICATION: USED | SKIPPED
SECURITY: USED | SKIPPED
PERFORMANCE: USED | SKIPPED
BLOCKING_FINDINGS: 0
NEXT_ACTION: Human merge decision. No merge, push, or deploy was performed.
```

## Verification

- [ ] A fresh independent `context-engineering` pass ran first
- [ ] The context-gap audit compared expected and actual affected surfaces
- [ ] `code-review-and-quality` was read and executed
- [ ] All three specialist skills received an explicit trigger decision
- [ ] Findings are evidence-backed and severity-labelled
- [ ] No product code was modified
- [ ] No unlisted skill was loaded
- [ ] Current verification evidence matches the reviewed implementation
- [ ] Merge remains a human decision
