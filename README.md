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

## Context Engineering and Codebase Exploration

Project context is larger than the useful attention budget. Every phase therefore starts by loading and executing the local `context-engineering` skill.

The repository is treated as a search space and the model context window as a delivery surface. The exploration model is:

```text
anchor search question
        ↓
canonical docs / rules
        ↓
lexical search + CodeGraph
        ↓
join candidates
        ↓
focused code / tests / contracts
        ↓
live state or data when materially required
        ↓
material gap left?
   yes ↺        no → cohesive context pack
```

Two codebase discovery lanes are always attempted:

- **Lexical search** — `rg`, `grep`, or the runtime equivalent for symbols, strings, config, SQL, docs, tests, and other text.
- **CodeGraph** — semantic and transitive relationships such as definitions, callers, consumers, imports, and blast radius.

Task shape changes the ordering, not whether those two lanes are attempted. For example, lexical enumeration starts with text search, known-symbol impact can run lexical and graph discovery independently before joining, and dynamic state flow proves a local event/state path before expanding outward through the graph.

Search outputs are candidate discovery, not proof. The skill reconciles lexical-only and graph-only findings through focused reads, then repeats only when new evidence exposes a material relationship or unresolved question.

The goal is **broad enough discovery, narrow context delivery**. A previous context pack is a search seed, never a substitute for a fresh phase-specific pass.

## Vendored and Adapted Skills

The selected Agent Skills are stored directly under `skills/`. The orchestrators resolve local sibling files such as:

```text
skills/guto-build/SKILL.md
skills/context-engineering/SKILL.md
skills/planning-and-task-breakdown/SKILL.md
skills/source-driven-development/SKILL.md
skills/incremental-implementation/SKILL.md
```

An orchestrator must read the complete local child `SKILL.md` before invoking it. If the file is absent, the phase returns `BLOCKED`; there is no silent external or remembered fallback.

Most vendored files remain byte-for-byte pinned to the reviewed Agent Skills commit. `context-engineering` is intentionally adapted in this repository to add the lightweight exploration loop while preserving the upstream context-curation purpose. Exact upstream and local blob identities are recorded in [`UPSTREAM_LOCK.json`](UPSTREAM_LOCK.json). See [`NOTICE.md`](NOTICE.md) for attribution and licensing.

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

## Branch Profiles

`main` is the repository-agnostic profile and must remain usable in arbitrary codebases.

Project-specific exploration policies may live on dedicated branches derived from `main`, so specialized repositories can add domain sources without contaminating the generic profile.

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
- English custom/adapted files;
- frontmatter and manifest consistency;
- byte-for-byte pinned upstream files plus tracked local adaptations;
- absence of inherited Orion's Belt Council contracts.

Hosted CI is not enabled by default. Run the validator locally or from the target project's existing CI runner.

## Design Boundary

This repository intentionally does not include:

- a Delivery Council;
- automatic subagent swarms;
- graph evidence ledgers, lifecycle receipts, scoring systems, graph-edge identifiers, or a context state machine;
- automatic transition between phases;
- automatic merge, push, or deployment;
- unrelated Agent Skills outside the exact composition above.

The exploration loop is a reasoning workflow, not a gate machine. Capabilities from Orion's Belt are ported only when they improve context quality without recreating high-assurance orchestration overhead.
