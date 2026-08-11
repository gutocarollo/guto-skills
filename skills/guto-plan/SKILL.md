---
name: guto-plan
description: Builds and refines an implementation plan from real project context. Use when a task needs discovery, requirements clarification, idea refinement, specification, material decisions, or an executable task breakdown before code changes.
---

# Guto Plan

## Purpose

Turn the user's request into an approved, decision-complete implementation plan. This skill is read-only with respect to product code. It may create or update planning artifacts, but it must not implement the change or start `guto-build`.

## Local Child-Skill Contract

Every child skill is vendored as a sibling under `skills/`.

When this skill calls a child skill:

1. Resolve the sibling path relative to this file.
2. Read the complete `SKILL.md` before using it. Do not rely on memory or a summary.
3. Follow the child workflow while preserving this skill's phase boundary and stop condition.
4. If the required local file is missing or unreadable, return `STATUS: BLOCKED`. Do not silently substitute an external or remembered version.

## Exact Skill Set

This skill may call only:

- [`context-engineering`](../context-engineering/SKILL.md) — mandatory, first, on every invocation
- [`interview-me`](../interview-me/SKILL.md) — conditional
- [`idea-refine`](../idea-refine/SKILL.md) — conditional
- [`clarification-plan`](../clarification-plan/SKILL.md) — conditional
- [`spec-driven-development`](../spec-driven-development/SKILL.md) — conditional
- [`planning-and-task-breakdown`](../planning-and-task-breakdown/SKILL.md) — mandatory before `PLAN_READY`

No other skill may be loaded or invoked by `guto-plan`.

## Mandatory Context Pass

`context-engineering` is not optional and is not part of `USE | REUSE | SKIP | BLOCKED` routing. It is always `USE`.

Run it before asking questions, proposing architecture, writing a specification, or decomposing tasks. A previous summary or context pack may be input, but never replaces a fresh context pass.

The context pass must produce a focused planning context pack containing:

- the user's original request and later amendments;
- existing canonical plans, specifications, ADRs, rules, and task files;
- relevant source files, tests, interfaces, schemas, and local patterns;
- current stack and versions when they affect the plan;
- related issues, pull requests, runtime evidence, or data when available and material;
- known constraints, conflicts, assumptions, and unresolved gaps;
- a list of sources intentionally excluded as irrelevant.

Context sufficiency means that no known material planning decision depends on an uninvestigated source. It does not mean loading the whole repository into the context window.

## Conditional Routing

After the mandatory context pass, classify each conditional child as `USE`, `REUSE`, `SKIP`, or `BLOCKED`.

| Skill | `USE` trigger | `SKIP` trigger |
|---|---|---|
| `interview-me` | Intended user, outcome, success, binding constraint, or out-of-scope boundary is still unclear | Intent is already explicit and confirmed |
| `idea-refine` | Multiple materially different solution directions remain worth exploring | The desired direction is already concrete |
| `clarification-plan` | A material human decision remains after facts were investigated | The answer is discoverable from code, docs, data, or an existing canonical decision |
| `spec-driven-development` | New feature, significant change, or acceptance criteria are not yet explicit | A sufficient approved specification already exists |
| `planning-and-task-breakdown` | Always before `PLAN_READY` | Never skipped; use the existing plan as input when it already contains tasks |

Do not invoke a conditional skill merely because it exists.

## Planning Cycle

1. **Anchor the request.** Preserve the original objective and accepted amendments. Separate requested scope from agent-proposed scope.
2. **Run mandatory context engineering.**
3. **Route conditional skills.** Show the routing table and concise reasons.
4. **Clarify intent when needed.** Use `interview-me` before solution design.
5. **Refine the solution space when needed.** Use `idea-refine`; do not force divergent exploration after the direction is settled.
6. **Resolve material decisions.** Investigate first, then use `clarification-plan` only for genuine human choices.
7. **Specify when needed.** Use the specification portions of `spec-driven-development`. Do not enter its implementation phase.
8. **Decompose the approved direction.** Always load and apply `planning-and-task-breakdown`.
9. **Audit plan sufficiency.** Return to the affected step only when a material gap remains.
10. **Stop for human approval.** Never start implementation automatically.

A repeated pass is justified only when it closes a material decision, adds relevant evidence, invalidates an assumption, or changes the plan. If a pass adds no material information, stop.

## Decision-Complete Exit Condition

The plan is ready when:

- the objective, intended user, and observable success are explicit;
- in-scope and out-of-scope boundaries are explicit;
- no known critical or high-impact human decision remains open;
- architecture and contracts needed by the task are specified;
- assumptions and risks are visible;
- acceptance criteria are testable;
- tasks are ordered by dependency and have verification steps;
- the plan identifies where implementation evidence must come from;
- the user has reviewed the current plan version.

Do not claim that context is literally complete or that future discoveries are impossible.

## Persistent Artifacts

Use an existing project convention when one exists. Otherwise maintain:

- `tasks/plan.md` — versioned planning contract
- `tasks/todo.md` — checkbox task list and human checkpoints
- `tasks/state.md` — short anti-drift summary for session changes or compaction

Minimum `tasks/state.md` fields:

```markdown
PLAN_VERSION:
CURRENT_PHASE: PLAN
OBJECTIVE:
SUCCESS:
IN_SCOPE:
OUT_OF_SCOPE:
OPEN_MATERIAL_DECISIONS:
NEXT_HUMAN_CHECKPOINT:
```

Increment `PLAN_VERSION` only when objective, scope, architecture, public contract, acceptance criteria, or critical ordering changes materially.

## Output

End with exactly one status:

- `STATUS: PLAN_READY`
- `STATUS: DECISION_REQUIRED`
- `STATUS: BLOCKED`

For `PLAN_READY`, include:

```text
PLAN_VERSION: <number>
OPEN_MATERIAL_DECISIONS: 0
CONTEXT_ENGINEERING: EXECUTED
CHILD_SKILLS_USED: <names>
CHILD_SKILLS_SKIPPED: <names with reasons>
ARTIFACTS_UPDATED: <paths>
NEXT_ACTION: Human review and explicit approval. Do not start guto-build.
```

## Verification

- [ ] The local `context-engineering` skill was read and executed first
- [ ] Only the exact child-skill set in this file was considered
- [ ] Every conditional skill has a recorded routing decision
- [ ] Questions were limited to material human decisions after investigation
- [ ] Product code was not modified
- [ ] `tasks/plan.md`, `tasks/todo.md`, and `tasks/state.md` are coherent
- [ ] `planning-and-task-breakdown` was applied before `PLAN_READY`
- [ ] The phase stopped for human approval
