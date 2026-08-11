---
name: guto-build
description: Executes an explicitly approved plan using refreshed project context, task preflight, authoritative sources, and incremental implementation. Use when a specific approved plan version is ready to be implemented.
---

# Guto Build

## Purpose

Implement one approved plan version without silently changing its objective, scope, contracts, or acceptance criteria. Update task checkboxes and collect local evidence, then stop before formal verification.

## Local Child-Skill Contract

Every child skill is vendored as a sibling under `skills/`.

For each child:

1. Resolve the sibling path relative to this file.
2. Read the complete `SKILL.md` before using it.
3. Execute the child workflow under this phase's scope.
4. If a local child file is missing or unreadable, return `STATUS: BLOCKED`. Do not substitute a remembered or external version.

## Exact Skill Set and Fixed Order

`guto-build` calls exactly these skills, in this order:

1. [`context-engineering`](../context-engineering/SKILL.md)
2. [`planning-and-task-breakdown`](../planning-and-task-breakdown/SKILL.md)
3. [`source-driven-development`](../source-driven-development/SKILL.md)
4. [`incremental-implementation`](../incremental-implementation/SKILL.md)

All four are mandatory on every `guto-build` invocation. No other skill may be loaded or invoked.

## Preconditions

Before editing product code, require:

- an explicit human-approved `PLAN_VERSION`;
- a readable plan and task checklist, using project-native paths or the fallback `tasks/plan.md` and `tasks/todo.md`;
- no unresolved material decision for the next task;
- a clean understanding of unrelated worktree changes that must be preserved.

If the plan is absent, not approved, or ambiguous, return `STATUS: PLAN_REQUIRED` without editing code.

## Step 1 — Mandatory Context Engineering

Always read and execute the local `context-engineering` skill first.

Build a focused execution context pack containing:

- approved plan version and current unchecked task;
- objective, scope, non-goals, decisions, and acceptance criteria;
- actual files and tests affected by the next task;
- existing local implementation patterns and reusable utilities;
- exact dependency, framework, runtime, and tool versions;
- current worktree state and unrelated changes to preserve;
- relevant errors, runtime state, schema, or data;
- any discovery that conflicts with the approved plan.

A context pack from Planning is input, not a substitute. Code and project state may have changed.

## Step 2 — Mandatory Task Preflight

Read and execute `planning-and-task-breakdown` against the approved plan and the next unchecked task.

This is a focused preflight, not permission to redesign the whole plan. Confirm:

- task objective and acceptance criteria;
- dependencies are complete;
- task size is executable;
- likely files and tests are still correct;
- verification commands are concrete;
- the task leaves the repository in a working state.

If the task is too large, split it without changing plan intent. If the preflight exposes a material plan flaw, return `STATUS: REPLAN_REQUIRED`.

## Step 3 — Mandatory Source-Driven Pass

Read and execute `source-driven-development` after task preflight and before implementation.

It must:

- detect the exact stack and versions from the repository;
- identify every implementation decision that depends on a framework, library, protocol, standard, or tool version;
- fetch authoritative documentation for those decisions;
- record the sources and version-specific constraints;
- surface conflicts between current official guidance and project conventions.

For a task with no version-dependent implementation decision, still run the pass and record:

```text
SOURCE_RESULT: NO_VERSION_DEPENDENT_DECISION
```

Do not skip the skill.

A conflict that changes architecture, public contract, scope, or acceptance criteria requires `STATUS: REPLAN_REQUIRED`. A local, reversible implementation detail may be resolved within the task and documented.

## Step 4 — Mandatory Incremental Implementation

Read and execute `incremental-implementation`.

For each smallest useful slice:

1. restate the approved task and slice boundary;
2. modify only the files required for that slice;
3. run the focused local checks defined by the plan and repository;
4. preserve unrelated worktree changes;
5. update `tasks/todo.md` only when evidence supports the checkbox;
6. update `tasks/state.md` with the current task and evidence;
7. continue only while the approved plan remains valid.

Local checks prevent compounded errors. They do not replace `guto-verify`.

Do not perform unrelated cleanup. Do not add a new dependency unless the approved plan permits it or the human explicitly approves the change.

## Material Drift Rule

Return `STATUS: REPLAN_REQUIRED` when a discovery changes any of:

- objective or intended outcome;
- in-scope or out-of-scope boundary;
- architecture or critical dependency direction;
- public API, interface, schema, or data contract;
- acceptance criteria;
- critical task order;
- a high-impact assumption.

Do not replan for a local file choice, naming detail, test adjustment, or other reversible implementation detail that preserves the approved contract.

## Human Boundary

This phase never invokes `guto-verify`, `guto-review`, merge, push, or deployment automatically.

## Output

End with exactly one status:

- `STATUS: BUILD_READY_FOR_VERIFY`
- `STATUS: REPLAN_REQUIRED`
- `STATUS: PLAN_REQUIRED`
- `STATUS: BLOCKED`

For `BUILD_READY_FOR_VERIFY`, include:

```text
PLAN_VERSION: <approved version>
CONTEXT_ENGINEERING: EXECUTED
TASKS_COMPLETED: <ids>
TASKS_REMAINING: <ids or none>
LOCAL_CHECKS: <commands and results>
SOURCE_RESULT: <sources or NO_VERSION_DEPENDENT_DECISION>
FILES_CHANGED: <paths>
NEXT_ACTION: Human audit, then invoke guto-verify explicitly.
```

## Verification

- [ ] The approved plan version was explicit
- [ ] `context-engineering` was read and executed first
- [ ] `planning-and-task-breakdown` was read and executed as task preflight
- [ ] `source-driven-development` was read and executed before code changes
- [ ] `incremental-implementation` governed all edits
- [ ] No unlisted skill was loaded
- [ ] Checkboxes are supported by real local evidence
- [ ] Material drift caused a return to Planning
- [ ] The phase stopped before formal verification
