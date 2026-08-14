# Guto Skills

Four composable orchestration skills built on a deliberately small, vendored subset of [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills).

## Composition

`guto-plan`, `guto-build`, `guto-verify`, and `guto-review` are graph nodes, not lifecycle gates. Any Guto skill may invoke any other Guto skill, including itself, whenever the active objective benefits from it. Callers may form forward paths, feedback loops, fan-in, fan-out, or targeted re-entry; no human approval, status, prior phase, or fixed order is required to cross an edge.

The caller owns the loop policy: it chooses the objective, exit condition, iteration budget, and evidence to retain. A Guto skill returns a compact `GRAPH_HANDOFF`. When automatic orchestration is active, it invokes the selected next skill immediately instead of stopping at a textual recommendation. The skills may load any vendored skill that is relevant to their current node; listed skills are capabilities, not an allowlist or required sequence.

Each node keeps its natural responsibility:

- `guto-plan` models objectives, decisions, contracts, and work slices.
- `guto-build` mutates the target and records implementation evidence.
- `guto-verify` collects or refreshes evidence and diagnoses discrepancies.
- `guto-review` independently evaluates the current artifact and can route directly to any node.

This preserves useful evidence while allowing flows such as `plan → build → verify → build → verify → review → plan`, direct `review → build`, and concurrent branches that later join at `verify` or `review`.

## Gauntlet Pre-Plan

A Gauntlet Loop starts before executable planning. `guto-plan` receives the goal plus optional references, selects the strongest concrete quality bar that an agent can inspect, and emits a compact pre-plan artifact containing:

- `GOAL` — the original objective without weakening its success condition.
- `REFERENCE_LOCATORS` — every supplied or discovered reference that remains relevant, including those not selected as the primary bar.
- `QUALITY_BAR` — one sentence naming the inspectable reference or measurement and its win rule, such as blind preference over the reference or `p95 <= 200 ms`.
- `GAUNTLET_RUN_PROMPT` — a short prompt for a fresh Claude Code or Codex lead agent that carries the goal, bar, and relevant reference locators.

The generated prompt is not the plan. It is the input that gives rise to the plan in a fresh context. The new lead agent chooses the approach and decomposition, writes the executable plan, maintains a simple live progress page, and orchestrates builder/critic loops against the bar. The pre-plan artifact should use the target project's planning convention; otherwise persist it at `tasks/gauntlet.md` and pass it by reference in `GRAPH_HANDOFF`.

One non-normative arrangement is:

```text
Cycle 1  GOAL + optional references → guto-plan pre-plan → QUALITY_BAR + GAUNTLET_RUN_PROMPT
Cycle 2  fresh agent + generated prompt → clarification-plan ↔ planning-and-task-breakdown → plan
Cycle 3  lead-selected Guto graph → inspect real output against the bar → next best edge
```

The diagram is an example, not a lifecycle contract. The lead or caller may skip, reorder, branch, join, or re-enter any Guto node after planning; there is no required `build → verify → review` sequence.

For each important piece that can be improved and judged independently, the lead agent fans out a builder and a separate critic with fresh context. The critic inspects the real artifact, compares it directly with the bar, uses blind A/B comparison when possible, returns the largest remaining gap, and repeats until the output wins or the caller stops the run. Coupled pieces stay under a sequential owner until they can be judged independently; fan-out is a tool, not a quota.

`context_policy: fresh` is an execution instruction to the external caller or runtime. It is the only exception to inline graph traversal: dispatch the selected node in a new context and pass the artifact reference instead of continuing in the current conversation. If the runtime cannot create a fresh context, it must say so rather than claiming independent review.

## Context Engineering and Codebase Exploration

Project context is larger than the useful attention budget. A graph node may load the local `context-engineering` skill whenever fresh discovery materially improves its next action.

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
├── gauntlet.md # optional pre-plan quality bar and generated runner prompt
├── plan.md   # approved, versioned planning contract
├── todo.md   # checkboxes and evidence-backed progress
└── state.md  # short anti-drift state for session changes or compaction
```

Material discoveries may route to whichever Guto node can resolve them; local reversible implementation details may remain in the current node.

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
$guto-plan
Model this change, then call any Guto node that advances the objective.
```

```text
$guto-build
Implement the current slice, then route to the most useful Guto node.
```

```text
$guto-verify
Refresh the evidence for the current artifact and route failures or gaps directly.
```

```text
$guto-review
Review the current artifact and route findings to any Guto node.
```

## Validate

```bash
python3 scripts/validate_skills.py
```

The validator checks:

- the exact skill inventory;
- local Guto-to-Guto composition references;
- local child paths;
- English custom/adapted files;
- frontmatter and manifest consistency;
- byte-for-byte pinned upstream files plus tracked local adaptations;
- absence of inherited Orion's Belt Council contracts.

Hosted CI is not enabled by default. Run the validator locally or from the target project's existing CI runner.

## Design Boundary

This repository supplies composable skill prompts, not a runtime scheduler. It does not impose a graph shape, status gate, approval gate, transition policy, merge policy, or deployment policy. An external orchestrator may supply those policies when useful.
