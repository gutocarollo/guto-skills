# Contrato dos artefatos de trabalho

Os artefatos persistem objetivo, decisões e progresso entre skills, sessões e compactações de
contexto. Eles substituem memória implícita; não substituem o código nem evidência runtime.

## Convenção de localização

1. Se o projeto já possui um sistema canônico de plano/tarefas, use-o e mapeie os campos abaixo.
2. Caso contrário, use:

```text
tasks/
├── plan.md
├── todo.md
└── state.md
```

Não crie um segundo sistema paralelo só para satisfazer esta convenção.

## `tasks/plan.md`

É o contrato diretor aprovado. Deve conter somente decisões vigentes.

```md
# Implementation Plan: <título>

PLAN_VERSION: 1
STATUS: PLAN_DRAFT | PLAN_READY | PLAN_APPROVED | REPLAN_REQUIRED

## Original request
<resumo fiel; preserve links, IDs e restrições literais importantes>

## Objective
<resultado final em uma frase>

## User and outcome
- User: ...
- Success: ...

## Scope
### In
- ...

### Out
- ...

## Context and current state
- ...

## Decisions
- D1 — ... — rationale/evidence

## Assumptions
- A1 — ... — validation status

## Acceptance criteria
- AC-1 — input, comportamento e saída observável

## Implementation tasks
- T1 — ... — dependencies: ... — acceptance: AC-...

## Verification strategy
- AC-1 → comando/ferramenta/evidência esperada

## Risks and rollback
- ...
```

### Versionamento

Incremente `PLAN_VERSION` apenas quando objetivo, escopo, arquitetura, contrato, aceite ou ordem
crítica mudar. Correção de texto e detalhe local não criam nova versão.

## `tasks/todo.md`

É a visão operacional em checkbox. Checkbox só fecha com evidência ou saída observável, nunca por
“parece concluído”.

```md
# Delivery checklist

PLAN_VERSION: 1

## Phase 1 — <nome>
- [x] T1 — <entregável> — evidence: `<comando/arquivo/resultado>`
- [ ] T2 — <entregável>

### Human checkpoint
- [ ] Revisar resultado da fase antes de continuar

## Deferred, non-blocking
- [ ] DFR-1 — <melhoria fora do escopo atual>
```

Não marque como concluída uma tarefa parcialmente implementada. Divida-a ou mantenha-a aberta.

## `tasks/state.md`

É um resumo pequeno para retomada. Deve permanecer curto e atualizado.

```md
# Current delivery state

PLAN_VERSION: 1
STATUS: PLAN_DRAFT
CURRENT_PHASE: PLAN | BUILD | VERIFY | REVIEW
CURRENT_TASK: T1 | none
LAST_COMPLETED: none
NEXT_HUMAN_CHECKPOINT: <descrição>

OBJECTIVE: <uma frase>
SUCCESS: <uma frase observável>
DO_NOT_DRIFT:
- <restrição ou não escopo crítico>

OPEN_MATERIAL_DECISIONS:
- none

LATEST_EVIDENCE:
- none

DEFERRED:
- none
```

## Atualização por skill

### `guto-plan`

- cria ou atualiza os três artefatos;
- mantém `STATUS=PLAN_DRAFT`, `DECISION_REQUIRED` ou `PLAN_READY`;
- nunca escreve `PLAN_APPROVED` em nome do usuário.

### Aprovação humana

Após aprovação explícita, registre `STATUS=PLAN_APPROVED` e a versão autorizada. Aprovação vaga de
uma ideia não equivale a aprovação do plano final.

### `guto-build`

- consome somente a versão aprovada;
- marca `CURRENT_TASK` antes de alterar o produto;
- fecha checkboxes depois dos checks locais;
- registra trabalho notado fora de escopo em `Deferred`, sem executá-lo;
- em drift material, escreve `REPLAN_REQUIRED` e para.

### `guto-verify`

- registra evidência atual por critério de aceite;
- não reaproveita PASS anterior se o código relevante mudou;
- escreve `VERIFY_FAILED` ou `VERIFIED`.

### `guto-review`

- registra findings materiais e disposição;
- escreve `REVIEW_FIX_REQUIRED` ou `MERGE_READY`;
- não executa merge.

## Anti-drift mínimo

Antes de qualquer tarefa ou finding, confira:

1. A ação contribui diretamente para `OBJECTIVE`?
2. Está em `Scope/In` e não viola `Scope/Out`?
3. Usa a mesma `PLAN_VERSION` aprovada?
4. Satisfaz uma tarefa ou critério identificável?

Se a resposta 1–3 for não, pare. Se apenas a 4 for não, registre como trabalho fora de escopo e
continue sem implementá-lo.
