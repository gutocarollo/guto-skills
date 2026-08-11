# Contrato do ciclo de entrega

O fluxo operacional tem quatro skills invocáveis e três domínios conceituais:

```text
PLANEJAMENTO                 EXECUÇÃO                  GARANTIA
┌───────────┐              ┌───────────┐       ┌────────────┐  ┌────────────┐
│ guto-plan │ ── humano ─▶ │guto-build │ ───▶  │guto-verify │─▶│guto-review │
└───────────┘              └───────────┘       └────────────┘  └────────────┘
```

`guto-verify` e `guto-review` pertencem ao domínio de garantia, mas permanecem separados:

- Verify pergunta: **funciona e satisfaz os critérios de aceite?**
- Review pergunta: **está correto, simples, seguro, sustentável e pronto para merge?**

## Regra de transição humana

Nenhuma skill inicia automaticamente a seguinte:

- `PLAN_READY` não inicia `guto-build`;
- `BUILD_READY_FOR_VERIFY` não inicia `guto-verify`;
- `VERIFIED` não inicia `guto-review`;
- `MERGE_READY` não faz commit, push ou merge.

Cada skill para, apresenta o artefato e permite auditoria humana.

## Estados canônicos

| Estado | Dono | Significado |
|---|---|---|
| `PLAN_DRAFT` | guto-plan | plano em construção |
| `DECISION_REQUIRED` | guto-plan | existe decisão material genuinamente humana |
| `PLAN_READY` | guto-plan | plano decision-complete aguardando aprovação |
| `PLAN_APPROVED` | humano | versão autorizada para execução |
| `BUILD_IN_PROGRESS` | guto-build | tarefas aprovadas em execução |
| `REPLAN_REQUIRED` | qualquer fase | descoberta material invalidou parte do plano |
| `BUILD_READY_FOR_VERIFY` | guto-build | implementação concluída e checks locais verdes |
| `VERIFY_FAILED` | guto-verify | uma claim não foi provada ou falhou |
| `VERIFIED` | guto-verify | critérios de aceite mapeados a evidências atuais |
| `REVIEW_FIX_REQUIRED` | guto-review | achado material deve voltar ao Build |
| `MERGE_READY` | guto-review | zero achado bloqueante/alto aberto e evidência vigente |
| `BLOCKED` | qualquer fase | dependência externa nominal impede progresso |

## Limite entre ajuste local e replanejamento

Retorne a `guto-plan` somente quando uma descoberta mudar materialmente pelo menos um destes itens:

- objetivo ou usuário beneficiado;
- sucesso observável;
- escopo ou não escopo;
- arquitetura ou estratégia principal;
- contrato público, schema ou boundary;
- critério de aceite;
- ordem de dependências crítica;
- premissa de alto impacto.

Não retorne ao planejamento por nome de função, arquivo adicional, ajuste pequeno de teste,
detalhe de implementação ou escolha reversível que não altere o contrato aprovado.

## Fronteiras de mutação

| Skill | Regra padrão |
|---|---|
| `guto-plan` | read-only no produto; pode criar/atualizar artefatos de planejamento |
| `guto-build` | pode alterar o produto dentro do plano aprovado |
| `guto-verify` | read-only; falhas geram pedido de correção para Build |
| `guto-review` | read-only; achados geram pedido de correção para Build |

Uma verificação ou review não deve “aproveitar e corrigir” silenciosamente. Isso mistura autor e
julgador, esconde o diff real e invalida evidências anteriores.

## Checks locais versus Verify formal

`guto-build` executa checks focados depois de cada incremento que possa quebrar o sistema. Isso
impede acumular erros.

`guto-verify` executa a prova consolidada contra os critérios de aceite. Não são duplicatas:

```text
BUILD:  mudar → check focado → continuar
VERIFY: claim → método de prova → evidência atual → veredito
```

## Loops limitados por informação

- Planning repete apenas enquanto houver contexto ou decisão material aberta.
- Build repete por tarefa/incremento aprovado.
- Verify repete depois de código alterado ou de uma prova nova.
- Review admite uma rechecagem direcionada após correções. Se essa rechecagem revelar um novo
  conjunto material não causado pelas correções, pare e exponha o problema em vez de entrar em
  revisão infinita.
