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

Common planning capabilities include:

- [`context-engineering`](../context-engineering/SKILL.md)
- [`idea-refine`](../idea-refine/SKILL.md)
- [`interview-me`](../interview-me/SKILL.md)
- [`clarification-plan`](../clarification-plan/SKILL.md)
- [`planning-and-task-breakdown`](../planning-and-task-breakdown/SKILL.md)

## Work

1. Recover the active objective and current artifact state.
2. Load only context that changes a decision or execution step; reuse trustworthy context when it remains relevant.
3. Make constraints, assumptions, unknowns, and acceptance evidence explicit when they matter.
4. Update existing planning artifacts when they help the caller; do not require a particular path or format.
5. For MetaPrompt work, `idea-refine ↔ interview-me/clarification-plan` is a useful loop. For executable planning, `clarification-plan ↔ planning-and-task-breakdown` is a useful loop. These are defaults, not allowlists.
6. Route to the node that adds the most information or makes the next useful mutation. A plan may directly invoke Build, Verify, Review, or another Plan pass.

## Gauntlet Pre-Plan Mode

Use this mode when the caller asks for a Gauntlet Loop or wants a meta-prompt that will originate the executable plan.

1. Accept `GOAL` and optional reference artifacts or quality bars. Preserve every relevant reference as an inspectable `REFERENCE_LOCATOR`, even when it is not selected as the primary bar.
2. Choose the strongest concrete bar that an agent can actually inspect and compare against. If none was supplied, propose a useful reference or measurement that plays the same role as real Call of Duty screenshots in Claude of Duty. Explain the bar in one sentence that includes both the inspectable comparator and a deterministic win rule, such as blind preference over the reference or `p95 <= 200 ms`.
3. Emit a short `GAUNTLET_RUN_PROMPT` for Claude Code or Codex. Carry the goal, quality bar, win rule, and all relevant reference locators into the prompt or its referenced artifact. Let the lead agent choose the approach, architecture, exact decomposition, and number of rounds.
4. Tell the lead agent to divide the goal into the smallest pieces that can be improved and judged independently. For each important independent piece, fan out a builder and a separate critic with fresh context.
5. Each critic must inspect the real output, compare it directly with the bar, use blind A/B comparison when possible, identify the biggest remaining gap, and return that gap for another round. Never let a builder grade its own summary.
6. Tell the lead agent to keep looping until the output wins or the caller stops the run, maintain a simple live progress page, and use subagents and ultracode when the host supports them.
7. Do not force parallel fan-out over coupled work. Keep a sequential owner for coupled concerns until they can be evaluated independently.
8. Persist `GOAL`, `REFERENCE_LOCATORS`, `QUALITY_BAR`, its win rule, and `GAUNTLET_RUN_PROMPT` using the target project's planning convention, falling back to `tasks/gauntlet.md`. The generated prompt is not the plan: it is the input to a fresh planning agent that will create the plan.

The handoff for this mode uses `context_policy: fresh`, `selected_next_node: guto-plan`, the pre-plan `artifact_ref`, and an exit condition for executable planning. Pass the artifact by reference instead of duplicating its full payload in `GRAPH_HANDOFF`.

## Output

Return a compact `GRAPH_HANDOFF`: objective, artifact refs, changed decisions, unresolved risks, evidence needed, selected next node, context policy, and exit condition. When automatic orchestration is active and the exit condition is not met, do not stop after suggesting the edge: read and invoke the selected skill now. If `context_policy` is `fresh`, dispatch the selected skill in a new agent context instead of invoking it in the current context; if the runtime cannot do that, report the capability boundary. The caller may still pause, branch, join, repeat, or override the route.
