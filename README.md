# Guto Skills

Quatro skills de orquestração para desenvolvimento assistido por IA, com seleção condicional das
skills do [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) e checkpoints
humanos entre as etapas.

O objetivo é preservar contexto, plano diretor e evidências sem transformar toda tarefa em um
Council, máquina de estados pesada ou sequência obrigatória de todas as skills disponíveis.

## Arquitetura

```text
PLANEJAMENTO                 EXECUÇÃO                  GARANTIA
┌───────────┐              ┌───────────┐       ┌────────────┐  ┌────────────┐
│ guto-plan │ ── humano ─▶ │guto-build │ ───▶  │guto-verify │─▶│guto-review │
└───────────┘              └───────────┘       └────────────┘  └────────────┘
```

| Skill | Responsabilidade | Para onde pode retornar |
|---|---|---|
| `guto-plan` | contexto, intenção, refinamento, decisões, spec e task breakdown | permanece no Planning até `PLAN_READY` |
| `guto-build` | executar a versão aprovada em incrementos com checks locais | `guto-plan` em drift material |
| `guto-verify` | provar critérios de aceite com testes e runtime | `guto-build` quando uma prova falha |
| `guto-review` | gate final de qualidade, simplificação, segurança e performance | `guto-build` ou `guto-plan` conforme o finding |

As transições não são automáticas. Cada skill para, entrega o artefato e aguarda auditoria humana.
`MERGE_READY` também não autoriza merge.

## Princípios

- **Skill aplicável, não skill disponível.** Cada skill-filha recebe `USE`, `REUSE`, `SKIP` ou
  `BLOCKED`.
- **Contexto pertence ao Planning.** Build faz apenas recuperação local e retorna ao Planning se a
  descoberta mudar objetivo, escopo, arquitetura, contrato ou aceite.
- **Checks locais não substituem Verify.** Build evita acumular erros; Verify prova o conjunto.
- **Verify não é Review.** Funcionamento e qualidade para merge são julgamentos separados.
- **Sem gates herdados do Orion's Belt.** Não há `edge_id`, scoring, ledger, hooks obrigatórios,
  commit por slice ou review adversarial universal.
- **Sem execução automática de todas as skills.** Frontend, browser, security e performance só
  entram quando a tarefa possui seus triggers.
- **Sem transição automática entre domínios.** O usuário controla quando avançar.

## Skills incluídas

```text
skills/
├── guto-plan/
├── guto-build/
├── guto-verify/
├── guto-review/
└── clarification-plan/
```

`clarification-plan` é uma versão portátil e reduzida da ideia usada no Orion's Belt. Ela mantém:

- investigação antes da pergunta;
- decisão material, não detalhe irrelevante;
- opções com comportamento e exemplos reais;
- recomendação explícita;
- terceira via quando A/B forem insuficientes.

Foram removidos contratos específicos do Council, percentuais, scores, hooks, ledgers e grafo de
execução obrigatório.

## Dependência

Este repositório **não copia** as 24 skills-folha do Agent Skills. Instale os dois pacotes no mesmo
runtime:

```bash
npx skills add addyosmani/agent-skills
npx skills add gutocarollo/guto-skills
```

Instale o pacote completo, não apenas uma skill isolada: as quatro orchestrators compartilham os
contratos em `references/`.

### Claude Code

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills

/plugin marketplace add gutocarollo/guto-skills
/plugin install guto-skills@guto-skills
```

### Codex CLI

```bash
codex plugin marketplace add addyosmani/agent-skills
codex plugin add agent-skills@agent-skills

codex plugin marketplace add gutocarollo/guto-skills
codex plugin add guto-skills@guto-skills
```

## Uso

### 1. Planejar

```text
@guto-plan
Planeje a feature X. Use o contexto real do repositório, refine comigo as decisões materiais e
pare quando a versão do plano estiver pronta para minha aprovação.
```

Saída esperada:

```text
STATUS: PLAN_READY
PLAN_VERSION: 1
OPEN_MATERIAL_DECISIONS: 0
```

### 2. Executar

Depois de aprovar explicitamente a versão:

```text
@guto-build
Execute a PLAN_VERSION 1. Atualize os checkboxes e pare em BUILD_READY_FOR_VERIFY.
```

### 3. Verificar

```text
@guto-verify
Prove todos os critérios de aceite da versão atual. Use browser somente se houver claim de browser.
```

### 4. Revisar

```text
@guto-review
Revise a mudança verificada para merge. Rode simplificação, segurança e performance somente se os
triggers existirem.
```

## Artefatos persistentes

Quando o projeto não possui convenção própria, as skills usam:

```text
tasks/
├── plan.md   # contrato diretor versionado
├── todo.md   # checklist e checkpoints
└── state.md  # resumo curto para retomada/anti-drift
```

A especificação está em [`references/artifact-contract.md`](references/artifact-contract.md).

## O que este pacote não faz

- não instala nem duplica Agent Skills;
- não executa Council ou subagentes por padrão;
- não exige grafo de código, MCP, hooks ou banco;
- não faz commit, push, merge ou deploy sem autorização/política explícita;
- não promete contexto literalmente completo;
- não considera toda recomendação de review bloqueante;
- não substitui as convenções canônicas já existentes no projeto-alvo.

## Desenvolvimento

Valide manifests, frontmatter, referências relativas, nomes e ausência de contratos herdados:

```bash
python3 scripts/validate_skills.py
```

O repositório não ativa CI hospedado por padrão. Conecte esse comando ao runner local ou ao CI já
usado pelo projeto quando fizer sentido.

## Fontes e procedência

Veja [`PROVENANCE.md`](PROVENANCE.md). O desenho usa Agent Skills como dependência, adota a separação
de checkpoints vista no Superpowers e reescreve de forma limpa apenas os conceitos úteis do
Orion's Belt.
