---
name: guto-plan
description: Models objectives, decisions, contracts, and work slices as a freely composable node in a Guto orchestration graph.
---

# Guto Plan

## Role

Model or revise the current objective, constraints, assumptions, contracts, acceptance evidence, and executable work slices. Planning artifacts are inputs and outputs, never a permission boundary.

## Composition

This node may invoke any local Guto node in any order, including re-entry:

- [`guto-plan`](../guto-plan/SKILL.md)
- [`guto-build`](../guto-build/SKILL.md)
- [`guto-verify`](../guto-verify/SKILL.md)
- [`guto-review`](../guto-review/SKILL.md)

It may also load any relevant vendored skill. There is no required child set, fixed order, approval checkpoint, terminal status, or phase boundary. Before invoking a local skill, read its complete `SKILL.md`.

## Work

1. Recover the active objective and current artifact state.
2. Load only context that changes a decision or execution step; reuse trustworthy context when it remains relevant.
3. Make constraints, assumptions, unknowns, and acceptance evidence explicit when they matter.
4. Update existing planning artifacts when they help the caller; do not require a particular path or format.
5. Route to the node that adds the most information or makes the next useful mutation. A plan may directly invoke Build, Verify, Review, or another Plan pass.

## Output

Return a compact state snapshot: objective, changed decisions, unresolved risks, evidence needed, and any artifact paths changed. The caller decides whether to continue, branch, join, repeat, or stop.
