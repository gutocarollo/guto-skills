---
name: guto-build
description: Executa uma versão aprovada do plano em incrementos proporcionais, com preflight de tarefa, documentação oficial quando relevante, checks locais e atualização contínua dos checkboxes. Use quando existe plano executável aprovado e o usuário quer implementar; interrompe em drift material e para ao final com BUILD_READY_FOR_VERIFY.
---

# Guto Build

## Objetivo

Executar somente o plano aprovado, tarefa por tarefa, preservando foco no objetivo diretor e evitando
implementação em lote. Esta skill modifica o produto, mas não executa a verificação consolidada, o
review final, push ou merge automaticamente.

## Contrato operacional embutido

- Classifique cada skill-filha como `USE`, `REUSE`, `SKIP` ou `BLOCKED`; leia integralmente apenas
  as marcadas `USE`.
- `USE` significa trigger presente e trabalho ainda não feito; `REUSE`, resultado vigente;
  `SKIP`, trigger ausente; `BLOCKED`, capacidade necessária sem acesso ou dado indispensável.
- Use os artefatos canônicos do projeto. Sem outra convenção, consuma e atualize `tasks/plan.md`,
  `tasks/todo.md` e `tasks/state.md`.
- A skill é autocontida: arquivos em `references/` na raiz são documentação complementar, não
  pré-condição de execução.
- Nenhuma transição de fase é automática. `BUILD_READY_FOR_VERIFY` devolve o controle ao usuário.

## Pré-condição

Precisa existir uma fonte de plano com:

- versão aprovada;
- tarefas ou próximo entregável identificável;
- critérios de aceite;
- estratégia de verificação.

Fontes aceitas:

- `tasks/plan.md` + `tasks/todo.md` + `tasks/state.md`;
- path explícito equivalente;
- plano inline aprovado pelo usuário.

Sem plano executável, retorne `REPLAN_REQUIRED`; não invente um plano silencioso dentro do Build.

## Skills permitidas

Esta skill pode rotear apenas:

- `planning-and-task-breakdown`
- `source-driven-development`
- `incremental-implementation`
- `test-driven-development`
- `frontend-ui-engineering`
- `api-and-interface-design`
- `security-and-hardening`
- `observability-and-instrumentation`
- `deprecation-and-migration`
- `documentation-and-adrs`
- `git-workflow-and-versioning`

## Preflight obrigatório, workflow proporcional

Antes de cada tarefa, avalie obrigatoriamente estas três skills, sem necessariamente executá-las:

| Skill | Regra |
|---|---|
| `planning-and-task-breakdown` | `REUSE` quando a tarefa aprovada já é pequena, ordenada e verificável; `USE` apenas para decompor o item atual sem mudar o contrato; `REPLAN_REQUIRED` se a decomposição exigir mudança material |
| `source-driven-development` | `USE` quando a tarefa depende de framework, biblioteca, API ou versão; `REUSE` quando a fonte já foi verificada para a mesma versão e decisão; `SKIP` para lógica/versionamento irrelevante |
| `incremental-implementation` | `USE` para mudança não trivial ou multi-arquivo; `SKIP` apenas quando a alteração é mínima e indivisível, mantendo as mesmas regras de escopo e check local |

Isso satisfaz a sequência:

```text
TASK PLAN VALIDATION
        +
SOURCE VALIDATION QUANDO APLICÁVEL
        ↓
INCREMENTAL IMPLEMENTATION QUANDO APLICÁVEL
```

Não execute integralmente `planning-and-task-breakdown` e `source-driven-development` antes de todo
item quando os resultados continuam válidos.

## Triggers das demais skills

| Skill | `USE` quando |
|---|---|
| `test-driven-development` | bug, regra de negócio ou comportamento observável está sendo criado/alterado |
| `frontend-ui-engineering` | UI, acessibilidade, responsividade, design system ou estado visual será alterado |
| `api-and-interface-design` | a tarefa implementa contrato já planejado; se precisar redesenhar o contrato, retorne a Planning |
| `security-and-hardening` | input externo, auth, autorização, secret, dado sensível, storage ou integração cruza trust boundary |
| `observability-and-instrumentation` | o caminho novo precisa ser diagnosticável em produção ou o plano exige telemetria |
| `deprecation-and-migration` | há transição de schema, contrato, consumidor ou caminho legado |
| `documentation-and-adrs` | o plano exige documentação operacional ou registro da decisão já aprovada |
| `git-workflow-and-versioning` | o usuário pediu commit/branch ou a política canônica do projeto exige checkpoints Git |

## Grafo de execução

```text
PLANO APROVADO
      ↓
SELECIONAR PRÓXIMA TAREFA ABERTA
      ↓
ANTI-DRIFT + PREFLIGHT
      ↓
ROTEAR SKILLS APLICÁVEIS
      ↓
MENOR INCREMENTO ÚTIL
      ↓
CHECK LOCAL FOCADO
   ┌──┴─────────────┐
 falha             passa
   │                 │
diagnosticar     atualizar todo/state
   │                 │
corrigir mesmo       ├── próximo incremento
escopo ou parar      ├── checkpoint humano
                     ├── REPLAN_REQUIRED
                     └── BUILD_READY_FOR_VERIFY
```

## Processo

### 1. Fixe a versão executável

Leia o estado e confirme:

```text
PLAN_VERSION: <n>
STATUS: PLAN_APPROVED
CURRENT_TASK: <id ou próxima aberta>
OBJECTIVE: <uma frase>
DO_NOT_DRIFT: <restrições principais>
```

Se o plano mudou depois da aprovação e não foi reaprovado, pare.

### 2. Selecione apenas a próxima tarefa elegível

Respeite dependências e checkpoints. Não execute tarefas futuras “já que o arquivo está aberto”.

Marque `CURRENT_TASK` antes de editar o produto. Não marque o checkbox como concluído ainda.

### 3. Faça o anti-drift

Confirme que a tarefa:

- contribui diretamente para o objetivo;
- está dentro do escopo;
- pertence à versão aprovada;
- satisfaz critério de aceite ou dependência explícita.

Trabalho útil, mas não planejado, vai para `Deferred`; não é implementado nesta execução.

### 4. Execute o preflight

Classifique as skills permitidas em `USE`, `REUSE`, `SKIP` ou `BLOCKED`. Antes de codar, resolva:

- arquivos e padrões locais relevantes;
- versões reais de dependências;
- documentação oficial necessária;
- contrato já aprovado;
- comando de check local adequado.

Se surgir uma decisão material de arquitetura, escopo, contrato ou aceite, escreva
`STATUS=REPLAN_REQUIRED`, descreva a descoberta e pare. Não use uma escolha local para reescrever o
plano.

### 5. Implemente o menor incremento útil

Quando `incremental-implementation=USE`:

1. escolha um slice que produza comportamento ou fundação verificável;
2. altere somente os arquivos necessários;
3. preserve mudanças locais não relacionadas;
4. evite abstração para necessidade hipotética;
5. não misture feature, refactor e cleanup ortogonal;
6. mantenha rollback simples quando o risco justificar.

Quando `test-driven-development=USE`, siga RED → GREEN → REFACTOR. Não escreva implementação ampla
para depois tentar encaixar testes.

### 6. Execute check local após mudança relevante

Use o comando mais focado que pode refutar o incremento:

- teste unitário ou de integração afetado;
- typecheck do pacote;
- lint do escopo;
- build parcial;
- query/fixture;
- checagem manual concreta quando não houver automação.

Não repita comando verde se nenhum código relevante mudou desde a execução anterior.

Falha esperada durante TDD não é bloqueio. Falha inesperada deve ser localizada antes de expandir o
slice. Não acumule tarefas sobre baseline quebrada.

### 7. Atualize os artefatos

Depois de um incremento realmente concluído:

- registre a evidência local;
- marque o checkbox correspondente ou subdivida a tarefa;
- atualize `LAST_COMPLETED` e `CURRENT_TASK`;
- mantenha findings fora de escopo em `Deferred`;
- preserve a versão do plano.

Checkbox significa entregável completo para aquele item, não apenas código escrito.

### 8. Use Git somente quando autorizado ou exigido

- não faça commit por padrão apenas porque um slice terminou;
- quando o usuário pedir commit ou o projeto exigir, use `git-workflow-and-versioning` para commits
  atômicos;
- nunca faça push, force-push, merge ou deploy sem autorização explícita separada.

### 9. Feche o Build

Quando todas as tarefas aprovadas estiverem implementadas e os checks locais aplicáveis estiverem
verdes, atualize:

```text
STATUS: BUILD_READY_FOR_VERIFY
CURRENT_PHASE: VERIFY
CURRENT_TASK: none
```

Não execute `guto-verify` automaticamente.

## Saída

```text
STATUS: BUILD_READY_FOR_VERIFY | REPLAN_REQUIRED | BLOCKED
PLAN_VERSION: <n>
TASKS_COMPLETED: <ids>
FILES_CHANGED: <paths>
LOCAL_CHECKS: <comando e resultado>
SKILLS_USED: <lista>
DEFERRED: <itens fora do escopo>
NEXT: auditoria humana; depois invocar guto-verify
```

## Red flags

- começar sem versão aprovada do plano;
- replanejar arquitetura dentro do Build;
- executar toda a allowlist em cada tarefa;
- escrever centenas de linhas antes do primeiro check;
- usar frontend skill em backend, browser skill em CLI ou security review sem trust boundary;
- corrigir item fora de escopo “aproveitando” o contexto;
- marcar checkbox sem evidência;
- repetir builds/testes verdes sem mudança interveniente;
- fazer commit, push ou merge sem pedido/política explícita;
- iniciar Verify automaticamente ao terminar.

## Verificação do Build

- [ ] A versão executada estava aprovada.
- [ ] Cada tarefa respeitou dependências e escopo.
- [ ] O preflight avaliou plan breakdown, fontes e incrementalidade.
- [ ] Apenas skills com trigger foram carregadas.
- [ ] Cada mudança relevante recebeu check local.
- [ ] Checkboxes e estado refletem o que realmente foi concluído.
- [ ] Drift material retornou a Planning em vez de ser decidido silenciosamente.
- [ ] O Build parou em `BUILD_READY_FOR_VERIFY`.
