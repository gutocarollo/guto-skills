---
name: guto-verify
description: Refreshes evidence and diagnoses discrepancies as a freely composable node in a Guto orchestration graph.
---

# Guto Verify

## Role

Collect current evidence for claims about the active artifact and diagnose differences between observed and expected behavior. Verification may be entered at any point and may immediately route to mutation or planning.

## Composition

This node may invoke any local Guto node in any order, including re-entry:

- [`guto-plan`](../guto-plan/SKILL.md)
- [`guto-build`](../guto-build/SKILL.md)
- [`guto-verify`](../guto-verify/SKILL.md)
- [`guto-review`](../guto-review/SKILL.md)

It may also load any relevant vendored skill. There is no prerequisite Build status, read-only gate around the graph, required child set, fixed order, or mandatory stop before Review. Before invoking a local skill, read its complete `SKILL.md`.

## Work

1. Identify the claims, expected results, and current artifact state.
2. Choose the least expensive evidence that can prove or refute each claim.
3. Execute relevant tests, builds, typechecks, queries, service calls, browser checks, or artifact inspection.
4. Record commands, environment, revision or worktree state, and observed results.
5. Route discrepancies directly to Build, Plan, Review, or another Verify pass; a caller may use any loop shape.

## Output

Return a claim-to-evidence snapshot, unproved claims, diagnosed discrepancies, and suggested graph edges. The caller decides whether evidence is sufficient and whether to continue.
