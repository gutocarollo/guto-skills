---
name: clarification-plan
description: Resolves material planning decisions after factual investigation. Use when two or more viable choices remain and the correct answer depends on human priorities, policy, risk tolerance, or business intent rather than information discoverable from the project.
---

# Clarification Plan

## Purpose

Help the user make a material decision with concrete consequences. Do not transfer raw ambiguity to the user and do not consume attention on low-impact details.

## Preconditions

Before asking a question:

1. Read the current objective, plan, and context pack.
2. Search canonical project decisions, code, tests, docs, data, and runtime evidence that could answer it.
3. Remove any question already answered by evidence or an existing decision.
4. Confirm that choosing differently would materially change scope, architecture, contract, acceptance criteria, risk, cost, or user-visible behavior.

If the missing answer is factual or testable, investigate it instead of asking the user.

For a bug, establish the best-supported root cause before presenting repair choices. If the root cause is not yet supported, return an investigation plan rather than a menu of fixes.

## Materiality Test

A decision is material when all are true:

- at least two viable paths remain after investigation;
- the paths have materially different consequences;
- the answer depends on a human preference, policy, business rule, irreversible action, or risk tolerance;
- the current plan cannot be finalized honestly without the choice.

Naming, formatting, local file placement, and other reversible implementation details normally do not qualify.

## Interaction Rule

Ask one material decision at a time. Wait for the user's answer before advancing to a dependent decision.

Do not ask a bare question such as "A or B?" Each option must make the resulting behavior visible.

## Required Decision Block

```markdown
### D[n] — [Concrete decision]

**Why this is still open:** [what was investigated and why evidence cannot decide it]
**Evidence:** [paths, commands, queries, documents, or observed facts]
**Unlocks:** [what part of the plan depends on the answer]

**Option A — [name]**
- **Behavior:** [what the system or process will do]
- **Applied good example:** [real project scenario and good result]
- **Applied bad example:** [real project scenario and cost or failure mode]
- **Choose when:** [objective priority]

**Option B — [name]**
- **Behavior:** ...
- **Applied good example:** ...
- **Applied bad example:** ...
- **Choose when:** ...

**Option C — [hybrid, spike, fallback, or staged choice]**
- Include only when A and B alone are both materially deficient.
- Use the same behavior and applied-example structure.

**Recommendation: Option [X]** — [evidence-based reason]
```

An applied example names a real file, interface, route, job, table, workflow, user journey, command, or operational scenario from the current project. Generic analogies do not count.

## Decision Cycle

1. Inventory all known material decisions, but present only the next independent decision.
2. Investigate before writing the decision block.
3. Remove decisions already resolved by canon or evidence.
4. Present options and a recommendation.
5. Record the user's decision and rationale in the planning artifacts.
6. Update only the affected sections of the plan.
7. Re-run the materiality test for remaining decisions.
8. Stop when no material human decision remains.

## Output

For an open decision:

```text
STATUS: DECISION_REQUIRED
DECISION_ID: D[n]
```

When all material decisions are closed:

```text
STATUS: DECISIONS_RESOLVED
OPEN_MATERIAL_DECISIONS: 0
```

## Anti-Patterns

- Asking about a fact that tools or project sources can answer
- Asking about an option already selected in canonical documentation
- Presenting ten low-impact choices while a critical decision remains hidden
- Giving options without a recommendation
- Using generic examples unrelated to the actual project
- Treating an unproven bug hypothesis as a root cause
- Rewriting the entire plan after a local decision
- Adding scores, council states, ledgers, or mandatory graph identifiers

## Verification

- [ ] The question is genuinely material
- [ ] Relevant evidence and canonical decisions were checked first
- [ ] Each option describes behavior and real project consequences
- [ ] A recommendation is explicit
- [ ] Only one independent decision was presented
- [ ] The user's answer was recorded in the plan
- [ ] No low-impact implementation detail consumed a decision slot
