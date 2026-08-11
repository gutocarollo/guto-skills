---
name: guto-plan
description: Orquestra definição e planejamento com contexto proporcional, refinamento de ideia, entrevista e clarificação material até produzir um plano executável e auditável. Use quando uma feature, correção ampla, arquitetura, migração ou tarefa multietapa precisa ser consolidada antes de qualquer implementação; para explicitamente antes do Build e aguarda aprovação humana.
---

# Guto Plan

## Objetivo

Produzir um plano **decision-complete para o escopo atual**: nenhuma decisão material conhecida fica
aberta e nenhuma tarefa depende de premissa crítica não verificada. Não promete contexto literalmente
completo nem um plano imune a toda descoberta futura.

Esta skill não edita o produto e não inicia `guto-build` automaticamente.

Leia antes de começar:

- `../../references/routing-contract.md`
- `../../references/lifecycle-contract.md`
- `../../references/artifact-contract.md`

## Entrada

Aceite qualquer combinação de:

- pedido atual;
- issue, PRD, documento, diff ou plano preliminar;
- `tasks/plan.md`, `tasks/todo.md` e `tasks/state.md` existentes;
- `DEPTH=AUTO | LIGHT | STANDARD | DEEP` opcional.

Quando já houver plano, atualize-o; não recomece do zero sem causa material.

## Skills permitidas

Esta skill pode rotear apenas:

- `context-engineering`
- `interview-me`
- `idea-refine`
- `clarification-plan`
- `spec-driven-development`
- `source-driven-development`
- `api-and-interface-design`
- `documentation-and-adrs`
- `planning-and-task-breakdown`

Não use todas por padrão.

## Triggers

| Skill | `USE` quando | `SKIP`/`REUSE` quando |
|---|---|---|
| `context-engineering` | falta contexto material sobre estado atual, padrões, dependências ou blast radius | contexto vigente já sustenta as decisões; faça apenas leitura direcionada |
| `interview-me` | faltam usuário, objetivo, porquê, sucesso, restrição ou não escopo | pedido é concreto, mecânico ou já confirmado |
| `idea-refine` | existe intenção, mas ainda há famílias de solução relevantes | abordagem e escopo já estão definidos |
| `clarification-plan` | após investigação resta decisão material dependente do usuário | fato é pesquisável, decisão já está canonizada ou detalhe é local/reversível |
| `spec-driven-development` | feature nova, mudança significativa ou critérios de aceite ausentes | correção pequena com comportamento inequívoco e spec suficiente |
| `source-driven-development` | arquitetura/contrato depende de framework, biblioteca, versão ou recomendação oficial | decisão é independente de versão ou fonte já foi verificada e continua vigente |
| `api-and-interface-design` | haverá API, schema, evento, módulo público ou boundary | implementação é interna e não muda contrato |
| `documentation-and-adrs` | decisão é cara de reverter ou precisa sobreviver ao plano | decisão local, óbvia e reversível |
| `planning-and-task-breakdown` | trabalho possui múltiplas unidades, dependências ou checkpoints | tarefa já é mínima, ordenada e verificável |

## Grafo do planejamento

```text
PEDIDO / PLANO EXISTENTE
          ↓
ANCORAR OBJETIVO E NÃO ESCOPO
          ↓
OBTER CONTEXTO PROPORCIONAL
          ↓
ROTEAR SKILLS DE DEFINE/PLAN
          ↓
REFINAR INTENÇÃO E SOLUÇÃO
          ↓
DECISÃO MATERIAL ABERTA?
     ┌────┴────┐
    sim       não
     │         │
clarification  ↓
     │      SPEC / CONTRATOS
     └──────▶  ↓
          TASK BREAKDOWN
               ↓
       GATE DE SUFICIÊNCIA
          ┌────┴────┐
         falha     passa
          │          │
      voltar ao      ↓
      ponto certo  PLAN_READY
                     ↓
                  PARAR
```

## Processo

### 1. Recupere o estado vigente

Leia primeiro o artefato canônico do projeto. Quando a convenção `tasks/` estiver em uso, leia nesta
ordem:

1. `tasks/state.md`;
2. `tasks/plan.md`;
3. `tasks/todo.md`;
4. pedido atual e fontes citadas.

Identifique a versão do plano e não trate resumo antigo como verdade sem conferir a fonte atual.

### 2. Ancore a intenção

Registre em linguagem direta:

- objetivo final;
- usuário/beneficiário;
- sucesso observável;
- restrição dominante;
- escopo;
- não escopo.

Se algum desses campos mudar após entrevista, atualize a âncora antes de continuar.

### 3. Construa contexto suficiente

Use `context-engineering` com profundidade proporcional. Procure somente o que pode mudar decisões do
plano:

- docs canônicas e decisões existentes;
- código e testes das superfícies afetadas;
- dependências e versões;
- contratos e integrações;
- dados/runtime quando a tarefa depende do estado vivo;
- implementações locais reutilizáveis.

Contexto suficiente significa: nenhuma decisão material do plano depende de lacuna conhecida. Não
significa ler o repositório inteiro.

### 4. Rode o roteamento

Classifique as skills permitidas como `USE`, `REUSE`, `SKIP` ou `BLOCKED`. Leia integralmente apenas
as marcadas `USE`.

### 5. Refine em ordem causal

Ordem padrão, não obrigatória:

```text
interview-me
   → idea-refine
   → spec-driven-development
   → source-driven-development / api-and-interface-design / ADRs
   → clarification-plan quando decisão humana persistir
   → planning-and-task-breakdown
```

Pule etapas sem trigger. Volte somente ao ponto invalidado por informação nova.

### 6. Resolva decisões materiais

Antes de chamar `clarification-plan`, investigue fatos e consulte decisões canônicas. Apresente uma
decisão por vez por padrão. Após cada resposta:

- registre a escolha e a razão;
- atualize somente a parte afetada;
- remova ramos descartados;
- verifique se a resposta eliminou outras decisões;
- continue até zero decisão material conhecida.

### 7. Produza tarefas verificáveis

Use `planning-and-task-breakdown` quando aplicável. Cada tarefa deve declarar:

- entregável observável;
- dependências;
- critérios de aceite relacionados;
- método de verificação;
- escopo provável;
- checkpoint humano quando necessário.

Prefira slices verticais. Não imponha limite artificial de arquivos; divida quando a tarefa mistura
objetivos ou não pode ser verificada isoladamente.

### 8. Atualize os artefatos

Crie ou atualize o sistema canônico do projeto. Sem outro sistema existente, use:

- `tasks/plan.md`;
- `tasks/todo.md`;
- `tasks/state.md`.

Mantenha checkboxes sem marcar; Planning não conclui trabalho de Build.

## Gate de suficiência

Antes de emitir `PLAN_READY`, confirme:

- [ ] objetivo, usuário e sucesso observável estão confirmados;
- [ ] escopo e não escopo estão explícitos;
- [ ] contexto material e padrões existentes foram consultados;
- [ ] zero decisão material conhecida permanece aberta;
- [ ] contratos e interfaces afetados estão definidos;
- [ ] premissas de alto impacto foram verificadas ou viraram pré-condições explícitas;
- [ ] critérios de aceite são testáveis;
- [ ] tarefas estão ordenadas por dependência;
- [ ] cada tarefa possui método de verificação;
- [ ] riscos, rollout e rollback relevantes estão descritos;
- [ ] plano e checklist usam a mesma versão.

Falha em um item retorna ao passo responsável. Não reinicie todo o processo.

## Aprovação

Ao terminar, apresente:

```text
STATUS: PLAN_READY
PLAN_VERSION: <n>
ARTEFATOS: <paths>
SKILLS_USED: <lista>
SKILLS_SKIPPED: <lista curta com motivo>
OPEN_MATERIAL_DECISIONS: 0
```

Peça aprovação explícita da versão. Não escreva `PLAN_APPROVED` em nome do usuário e não inicie
implementação.

## Saídas válidas

- `PLAN_READY`: plano consolidado aguardando aprovação;
- `DECISION_REQUIRED`: uma decisão material foi apresentada e aguarda resposta;
- `INVESTIGATION_REQUIRED`: falta evidência para planejar honestamente;
- `BLOCKED`: dependência externa nominal impede fechar o plano.

## Red flags

- editar código durante Planning;
- carregar todas as skills disponíveis;
- entrevistar quando o pedido já é inequívoco;
- perguntar sobre fato pesquisável;
- fechar spec antes de obter contexto material;
- criar plano com “descobrir depois”, “conforme necessário” ou critérios subjetivos;
- decompor o mesmo plano repetidamente sem nova evidência;
- iniciar Build depois de `PLAN_READY` sem nova invocação e aprovação humana.
