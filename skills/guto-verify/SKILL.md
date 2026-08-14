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

Common verification capabilities include:

- [`context-engineering`](../context-engineering/SKILL.md)
- [`browser-testing-with-devtools`](../browser-testing-with-devtools/SKILL.md)
- [`debugging-and-error-recovery`](../debugging-and-error-recovery/SKILL.md)

## Work

1. Identify the claims, expected results, and current artifact state.
2. Choose the least expensive evidence that can prove or refute each claim.
3. Execute relevant tests, builds, typechecks, queries, service calls, browser checks, or artifact inspection.
4. Record commands, environment, revision or worktree state, and observed results.
5. Route discrepancies directly to Build, Plan, Review, or another Verify pass; a caller may use any loop shape.

## Output

Return a compact `GRAPH_HANDOFF`: claim-to-evidence snapshot, unproved claims, diagnosed discrepancies, selected next node, and exit condition. When automatic orchestration is active and the exit condition is not met, do not stop after suggesting the edge: read and invoke the selected skill now. The caller decides the evidence threshold and loop budget.
