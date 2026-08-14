---
name: guto-review
description: Independently evaluates the current artifact and routes findings as a freely composable node in a Guto orchestration graph.
---

# Guto Review

## Role

Independently inspect the current objective, artifact, evidence, and surrounding context for correctness, omitted consumers, maintainability, security, performance, and evidence gaps. Review is a graph node, not a final merge gate.

## Composition

This node may invoke any local Guto node in any order, including re-entry:

- [`guto-plan`](../guto-plan/SKILL.md)
- [`guto-build`](../guto-build/SKILL.md)
- [`guto-verify`](../guto-verify/SKILL.md)
- [`guto-review`](../guto-review/SKILL.md)

It may also load any relevant vendored skill. There is no prerequisite verification status, read-only return path, required child set, fixed order, approval checkpoint, or terminal merge status. Before invoking a local skill, read its complete `SKILL.md`.

Common review capabilities include:

- [`context-engineering`](../context-engineering/SKILL.md)
- [`code-review-and-quality`](../code-review-and-quality/SKILL.md)
- [`code-simplification`](../code-simplification/SKILL.md)
- [`security-and-hardening`](../security-and-hardening/SKILL.md)
- [`performance-optimization`](../performance-optimization/SKILL.md)

## Work

1. Reconstruct enough context to challenge the current artifact rather than trusting prior summaries.
2. Inspect changed code, affected callers and consumers, contracts, tests, evidence, and relevant runtime surfaces.
3. Record findings with concrete location, impact, and the evidence that supports them.
4. Load specialised review capabilities when they add information.
5. Route each finding directly to the node that can resolve it, including Plan, Build, Verify, or another Review pass.

## Output

Return a compact `GRAPH_HANDOFF`: context gaps, findings with severity, evidence quality, unresolved risk, selected next node, and exit condition. When automatic orchestration is active and the exit condition is not met, do not stop after suggesting the edge: read and invoke the selected skill now. The caller decides disposition, looping, and release actions.
