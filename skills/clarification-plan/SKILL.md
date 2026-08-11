---
name: clarification-plan
description: Estrutura decisões técnicas ou de produto que permanecem materialmente abertas após investigação. Use quando duas ou mais opções reais mudam o plano, o contrato, o risco ou o critério de aceite e a escolha depende do usuário; não use para fatos pesquisáveis, detalhes locais reversíveis ou preferências sem impacto material.
---

# Clarification Plan

## Objetivo

Transformar ambiguidade material em uma decisão informada. Esta skill não transfere pesquisa para o
usuário e não cria perguntas por precaução. Primeiro investiga; depois apresenta consequências
concretas; por fim recomenda uma opção.

## Quando usar

Use quando todas as condições forem verdadeiras:

1. há pelo menos duas opções tecnicamente plausíveis;
2. código, documentação, dados e padrões existentes não determinam sozinhos a resposta;
3. a escolha muda materialmente escopo, arquitetura, contrato, aceite, custo, risco ou experiência;
4. escolher errado agora causaria retrabalho relevante ou uma decisão difícil de reverter;
5. o usuário tem autoridade ou preferência legítima para decidir.

## Quando não usar

Não use para:

- informação que pode ser encontrada no repositório, documentação oficial, banco ou runtime;
- bug cuja causa-raiz ainda não foi investigada;
- nome de função, organização de arquivo ou detalhe local reversível;
- melhoria opcional fora do escopo atual;
- pergunta que o usuário não consegue resolver por falta de acesso ou autoridade;
- confirmar uma decisão já registrada em plano, ADR, schema ou instrução canônica.

## Fluxo

```text
LACUNA
  ↓
INVESTIGAR FONTES REAIS
  ↓
DECISÃO JÁ ESTÁ TOMADA?
  ├── sim → registrar a fonte e remover a pergunta
  └── não
       ↓
MATERIAL E HUMANA?
  ├── não → decidir tecnicamente ou registrar como deferred
  └── sim
       ↓
OPÇÕES + CONSEQUÊNCIAS + RECOMENDAÇÃO
       ↓
RESPOSTA DO USUÁRIO
       ↓
ATUALIZAR SOMENTE O PLANO AFETADO
```

## 1. Investigue antes de perguntar

Consulte, conforme o caso:

- pedido original e plano vigente;
- código e testes relevantes;
- documentação canônica e ADRs;
- versões reais das dependências;
- dados ou comportamento runtime;
- padrões já adotados no projeto.

Para bugs, reproduza e localize a causa antes de oferecer soluções. Se a causa ainda estiver aberta,
entregue um plano de investigação, não um menu de correções.

## 2. Faça inventário das decisões materiais

Liste internamente todas as decisões conhecidas, mas apresente **uma por vez por padrão**. Pode
agrupar até três decisões independentes quando o usuário pedir explicitamente um lote.

Ordene por dependência: uma decisão que elimina outras vem primeiro.

## 3. Formato obrigatório

```md
### D[n] — <pergunta concreta>

**Por que precisa de decisão humana:** <critério que não pode ser deduzido>
**Evidência:** <arquivo:linha, query, comando, documentação ou runtime>
**Destrava:** <parte do plano que depende da resposta>

#### Opção A — <nome>
- **Comportamento:** <efeito concreto>
- **Exemplo aplicado bom:** <resultado no caso real do projeto>
- **Exemplo aplicado ruim:** <custo ou falha no caso real>
- **Escolha quando:** <prioridade que favorece A>

#### Opção B — <nome>
- **Comportamento:** ...
- **Exemplo aplicado bom:** ...
- **Exemplo aplicado ruim:** ...
- **Escolha quando:** ...

#### Opção C — <terceira via, quando A e B isoladas forem insuficientes>
- **Comportamento:** ...
- **Exemplo aplicado bom:** ...
- **Exemplo aplicado ruim:** ...
- **Escolha quando:** ...

**Recomendo: Opção X** — <critério objetivo e evidência que sustentam a recomendação>.
```

A Opção C pode ser combinação, spike, fallback, rollout gradual ou preservação temporária do caminho
atual. Não invente C quando A ou B já domina claramente.

## 4. Regras de qualidade

- Opções devem produzir comportamentos diferentes, não apenas redações diferentes.
- Exemplos devem citar entidade, rota, tabela, arquivo, job, tela, comando ou fluxo real.
- Toda opção deve ter pelo menos um benefício e um custo honesto.
- A recomendação é obrigatória; recomendar não significa decidir pelo usuário.
- Não use jargão como substituto de consequência operacional.
- Não apresente opção inviável apenas para fabricar contraste.
- Não use percentuais de confiança ou progresso sem denominador medido.

## 5. Depois da resposta

1. registre a decisão e sua razão em `tasks/plan.md` ou no artefato canônico do projeto;
2. atualize apenas as tarefas, critérios e riscos afetados;
3. incremente a versão do plano somente se a mudança for material;
4. retire a decisão da lista aberta em `tasks/state.md`;
5. continue o planejamento até não restar decisão material conhecida.

## Saídas válidas

- `DECIDED`: usuário escolheu e o plano foi atualizado;
- `ALREADY_DECIDED`: fonte canônica já resolvia a questão;
- `INVESTIGATION_REQUIRED`: falta causa ou evidência para formular opções honestas;
- `BLOCKED`: dependência externa nominal impede investigar ou decidir.

## Red flags

- perguntar “A ou B?” sem explicar comportamento e trade-off;
- perguntar antes de ler código, docs ou dados disponíveis;
- oferecer correções para bug não reproduzido;
- pedir decisão já registrada no plano ou ADR;
- transformar toda incerteza em pergunta ao usuário;
- listar opções sem recomendar uma;
- continuar planejando como se uma decisão material ainda aberta estivesse resolvida.

## Verificação

- [ ] A lacuna foi investigada antes da pergunta.
- [ ] A decisão é material e genuinamente humana.
- [ ] Nenhuma fonte canônica já decide a questão.
- [ ] As opções têm comportamentos e consequências concretas.
- [ ] Exemplos são aplicados ao projeto real.
- [ ] Há recomendação explícita sustentada por evidência.
- [ ] O plano e o estado foram atualizados depois da resposta.
