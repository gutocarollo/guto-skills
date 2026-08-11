# Guto Skills

Four phase-scoped orchestration skills built on a deliberately small, vendored subset of [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills).

The package keeps a master plan, refreshes context at every phase, selects only the skills explicitly assigned to that phase, and stops for human audit before advancing.

## Lifecycle

```text
guto-plan
    │  PLAN_READY + human approval
    ▼
guto-build
    │  BUILD_READY_FOR_VERIFY + human audit
    ▼
guto-verify
    │  VERIFIED + human audit
    ▼
guto-review
    │
    └── MERGE_READY still requires a human merge decision
```

No phase invokes the next phase automatically.

## Exact Composition

### `guto-plan`

Always:

- `context-engineering`
- `planning-and-task-breakdown` before `PLAN_READY`

Conditionally:

- `interview-me`
- `idea-refine`
- `clarification-plan`
- `spec-driven-development`

### `guto-build`

Always, in this order:

1. `context-engineering`
2. `planning-and-task-breakdown`
3. `source-driven-development`
4. `incremental-implementation`

### `guto-verify`

Always:

- `context-engineering`

Conditionally:

- `browser-testing-with-devtools` for browser claims
- `debugging-and-error-recovery` after a failed or unexpected verification result

Project-native test, build, typecheck, lint, query, and runtime commands are executed as evidence; no generic testing skill is added.

### `guto-review`

Always:

- a fresh independent `context-engineering` pass
- `code-review-and-quality`

Conditionally:

- `code-simplification`
- `security-and-hardening`
- `performance-optimization`

The review context pass explicitly searches for relevant code, contracts, consumers, tests, and architecture that Planning or Build may have omitted.

## Why Context Engineering Is Mandatory

Project context is larger than the useful attention budget. Every phase therefore starts by loading and executing the local `context-engineering` skill.

The goal is not to inject the entire repository. The goal is to route the agent to the smallest cohesive set of current code, documentation, tests, contracts, runtime evidence, and project decisions needed for the phase.

A previous context pack is input, never a substitute:

- Planning needs context to produce the right plan.
- Build needs refreshed context because code and dependencies may have changed.
- Verify needs context to map claims to real proof surfaces.
- Review needs an independent context reconstruction to find omitted impact and stale assumptions.

## Vendored Skills

The selected Agent Skills are stored directly under `skills/`. The orchestrators resolve local sibling files such as:

```text
skills/guto-build/SKILL.md
skills/context-engineering/SKILL.md
skills/planning-and-task-breakdown/SKILL.md
skills/source-driven-development/SKILL.md
skills/incremental-implementation/SKILL.md
```

An orchestrator must read the complete local child `SKILL.md` before invoking it. If the file is absent, the phase returns `BLOCKED`; there is no silent external or remembered fallback.

The vendored snapshot is pinned in [`UPSTREAM_LOCK.json`](UPSTREAM_LOCK.json). See [`NOTICE.md`](NOTICE.md) for attribution and licensing.

## Skills Tree

```text
skills/
├── guto-plan/
├── guto-build/
├── guto-verify/
├── guto-review/
├── clarification-plan/
├── context-engineering/
├── interview-me/
├── idea-refine/
├── spec-driven-development/
├── planning-and-task-breakdown/
├── source-driven-development/
├── incremental-implementation/
├── browser-testing-with-devtools/
├── debugging-and-error-recovery/
├── code-review-and-quality/
├── code-simplification/
├── security-and-hardening/
└── performance-optimization/
```

No other Agent Skills are included in this repository.

## Planning Artifacts

Use the target project's existing planning convention when it has one. Otherwise the fallback is:

```text
tasks/
├── plan.md   # approved, versioned planning contract
├── todo.md   # checkboxes and evidence-backed progress
└── state.md  # short anti-drift state for session changes or compaction
```

Material discoveries return to `guto-plan`. Local reversible implementation details remain in `guto-build`.

## Install

### Open Skills CLI

```bash
npx skills add gutocarollo/guto-skills --skill '*'
```

The selected Agent Skills are already vendored. A separate installation of `addyosmani/agent-skills` is not required.

### Claude Code

```text
/plugin marketplace add gutocarollo/guto-skills
/plugin install guto-skills@guto-skills
```

### Codex

```bash
codex plugin marketplace add gutocarollo/guto-skills
codex plugin add guto-skills@guto-skills
```

## Invoke

```text
@guto-plan
Plan this change from the real repository context. Refine material decisions with me and stop at PLAN_READY.
```

```text
@guto-build
Implement the explicitly approved PLAN_VERSION. Update evidence-backed checkboxes and stop at BUILD_READY_FOR_VERIFY.
```

```text
@guto-verify
Prove the current implementation against every acceptance criterion and stop before Review.
```

```text
@guto-review
Run a fresh context-gap audit and review the verified change for merge readiness.
```

## Validate

```bash
python3 scripts/validate_skills.py
```

The validator checks:

- the exact skill inventory;
- the exact child-skill set for each `guto-*` skill;
- mandatory `context-engineering` in all four phases;
- local child paths;
- English custom files;
- frontmatter and manifest consistency;
- pinned upstream Git blob hashes;
- absence of inherited Orion's Belt Council contracts.

Hosted CI is not enabled by default. Run the validator locally or from the target project's existing CI runner.

## Design Boundary

This repository intentionally does not include:

- a Delivery Council;
- automatic subagent swarms;
- mandatory code graphs, ledgers, hooks, scores, or graph-edge identifiers;
- automatic transition between phases;
- automatic merge, push, or deployment;
- unrelated Agent Skills outside the exact composition above.

Capabilities from Orion's Belt may be ported later only when they solve a measured problem without turning the normal path into a high-assurance Council.
