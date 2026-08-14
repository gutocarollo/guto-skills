---
name: guto-build
description: Mutates the target in small evidence-backed slices as a freely composable node in a Guto orchestration graph.
---

# Guto Build

## Role

Implement the current useful slice. A formal plan, approval, status, or prior phase can inform the slice but is never required to enter Build.

## Composition

This node may invoke any local Guto node in any order, including re-entry:

- [`guto-plan`](../guto-plan/SKILL.md)
- [`guto-build`](../guto-build/SKILL.md)
- [`guto-verify`](../guto-verify/SKILL.md)
- [`guto-review`](../guto-review/SKILL.md)

It may also load any relevant vendored skill. There is no allowlist, required ordering, approval checkpoint, or mandatory stop before another Guto node. Before invoking a local skill, read its complete `SKILL.md`.

## Work

1. Identify the active objective, current artifact, and smallest useful mutation.
2. Preserve unrelated work and record the state being changed.
3. Use relevant source, implementation, test, and debugging capabilities as needed.
4. Run focused checks whenever they reduce uncertainty; retain the observed result rather than asserting success.
5. Route directly to Plan, Build, Verify, or Review when that node is the best next operation. Material discoveries may be handled by any node.

## Output

Return the mutation summary, affected paths, current evidence, failures or open risks, and a suggested next graph edge. The caller controls continuation and loop budget.
