---
name: guto-review
description: Executa o gate final de qualidade contra plano, diff e evidências verificadas, selecionando code review, simplificação, segurança e performance somente quando seus triggers existem. Use depois de VERIFIED ou antes de merge; opera em read-only, bloqueia apenas achados materiais ancorados em evidência e devolve correções ao Build.
---

# Guto Review

## Objetivo

Responder **“esta mudança verificada está pronta para merge?”**. Review não repete toda a verificação
funcional e não modifica o produto. Ele avalia correção, clareza, arquitetura, segurança, performance
e aderência ao plano, com profundidade proporcional.

Leia antes de começar:

- `../../references/routing-contract.md`
- `../../references/lifecycle-contract.md`
- `../../references/artifact-contract.md`

## Pré-condição

Preferencialmente:

```text
STATUS: VERIFIED
PLAN_VERSION: <n>
CODE_REVISION: <sha/fingerprint>
```

Pode revisar antes de Verify quando o usuário pedir explicitamente um review intermediário, mas deve
marcar qualquer claim runtime ainda não provada como pendente; não converta ausência de evidência em
aprovação.

## Skills permitidas

Esta skill pode rotear apenas:

- `code-review-and-quality`
- `code-simplification`
- `security-and-hardening`
- `performance-optimization`

## Triggers

| Skill | `USE` quando | `SKIP` quando |
|---|---|---|
| `code-review-and-quality` | existe alteração de código, schema, configuração executável ou contrato | mudança puramente textual sem comportamento; faça revisão direta do artefato |
| `code-simplification` | código funciona, mas há complexidade material, abstração prematura, duplicação relevante ou fluxo difícil de manter | solução já é direta; preferência estética isolada não basta |
| `security-and-hardening` | mudança toca input externo, auth, autorização, secrets, dados sensíveis, storage, upload, integração ou trust boundary | nenhuma superfície de segurança relevante mudou |
| `performance-optimization` | há requisito, regressão suspeita, caminho quente ou medição que indique problema | preocupação genérica sem baseline, profile ou impacto plausível |

Não execute todas as quatro por padrão.

## Grafo de review

```text
PLANO + DIFF + EVIDÊNCIA VERIFIED
              ↓
DELIMITAR SUPERFÍCIE E RISCO
              ↓
ROTEAR SKILLS APLICÁVEIS
              ↓
REVIEW PRIMÁRIO
              ↓
ACHADO MATERIAL?
       ┌──────┴──────┐
      sim            não
       │              │
FIX_REQUEST        MERGE_READY
       │              ↓
 guto-build           PARAR
       ↓
 guto-verify
       ↓
RECHECK DIRECIONADO (uma rodada normal)
```

## Processo

### 1. Reancore no objetivo, não na narrativa do implementador

Leia:

1. pedido/objetivo e plano aprovados;
2. critérios de aceite;
3. diff e arquivos completos relevantes;
4. evidências de Verify;
5. padrões canônicos do projeto.

Analise o código real. Resumo de implementação é índice, não prova.

### 2. Delimite a superfície

Registre:

- arquivos e contratos alterados;
- consumidores e integrações afetados;
- dados, permissões e estados tocados;
- riscos declarados no plano;
- mudanças locais não relacionadas que devem ser preservadas.

Não transforme todo o repositório em escopo do review.

### 3. Rode o roteamento

Classifique as quatro skills como `USE`, `REUSE`, `SKIP` ou `BLOCKED`. Use profundidade:

- `LIGHT` para alteração local e reversível;
- `STANDARD` para feature/correção normal;
- `DEEP` para autorização, dados, migração, produção, contrato público ou grande blast radius.

### 4. Faça o review primário

Quando `code-review-and-quality=USE`, avalie:

- **correctness:** lógica, estados de borda, falhas parciais, concorrência e contratos;
- **readability/simplicity:** fluxo compreensível, nomes e abstrações justificadas;
- **architecture:** aderência aos boundaries e padrões existentes;
- **tests/evidence:** cobertura dos riscos e correspondência com o plano;
- **operability:** erros, rollback, observabilidade e manutenção quando aplicáveis.

Considere comportamento novo e removido. Não limite o review às linhas verdes/vermelhas quando o
contexto da função ou consumidor for necessário.

### 5. Aplique passes condicionais

#### Simplificação

Use `code-simplification` quando houver evidência concreta de complexidade desnecessária. Preserve o
comportamento. Sugira a menor simplificação que reduza custo real; não peça refactor cosmético.

#### Segurança

Use `security-and-hardening` somente nas boundaries afetadas. Verifique autorização no servidor,
validação, exposição de dados, secrets, dependências e failure mode relevantes. Não produza checklist
OWASP genérico desconectado do diff.

#### Performance

Use `performance-optimization` com abordagem measure-first. Compare com requisito ou baseline. Sem
medição e sem mecanismo plausível, registre no máximo hipótese não bloqueante.

### 6. Classifique por materialidade

| Severidade | Critério | Disposição |
|---|---|---|
| `BLOCKING` | pode produzir comportamento incorreto grave, vulnerabilidade, perda/corrupção de dados, quebra de contrato ou impossibilidade de operar/rollback | deve corrigir antes do merge |
| `HIGH` | alta probabilidade de regressão relevante, falha em produção ou dívida que torna a mudança insegura de manter agora | deve corrigir nesta entrega |
| `DEFERRED` | melhoria válida, mas fora do caminho crítico ou sem impacto material nesta entrega | registrar; não bloquear |
| `INVALID` | preferência, hipótese sem evidência, nit ou finding fora de escopo | descartar |

Um finding só pode ser `BLOCKING` ou `HIGH` quando inclui:

- localização concreta;
- comportamento atual;
- mecanismo de falha;
- impacto no objetivo/aceite;
- evidência ou reprodução;
- correção mínima recomendada.

Não infle severidade para garantir atenção.

### 7. Produza o veredito

Formato por finding:

```md
### F[n] — <BLOCKING | HIGH | DEFERRED>: <título>

- **Local:** `path:linha` ou contrato afetado
- **Evidência:** <trecho, comando, teste, query ou comportamento>
- **Mecanismo:** <como a falha acontece>
- **Impacto:** <qual objetivo, usuário ou critério é afetado>
- **Correção mínima:** <escopo recomendado>
- **Reteste:** <claims/comandos que devem rodar novamente>
```

Findings `DEFERRED` ficam separados dos requeridos.

### 8. Retorne correções ao Build

Se existir `BLOCKING` ou `HIGH`:

```text
STATUS: REVIEW_FIX_REQUIRED
RETURN_TO: guto-build
REVERIFY: <claims afetadas>
REREVIEW: <áreas afetadas>
```

Review não aplica a correção. Depois do Build, `guto-verify` repete as provas afetadas e o Review faz
uma rechecagem direcionada.

Uma rechecagem normal é suficiente. Se ela revelar um novo conjunto material não causado pelo fix,
pare e exponha a limitação em vez de entrar em review infinito.

### 9. Feche

Somente com zero `BLOCKING` e zero `HIGH` aberto:

```text
STATUS: MERGE_READY
```

Isso não autoriza commit, push, merge ou deploy. A decisão final é humana.

## Saída

```text
STATUS: MERGE_READY | REVIEW_FIX_REQUIRED | REPLAN_REQUIRED | BLOCKED
PLAN_VERSION: <n>
CODE_REVISION: <sha/fingerprint>
ROUTING: <skills usadas/puladas>
FINDINGS_REQUIRED: <quantidade e IDs>
FINDINGS_DEFERRED: <quantidade e IDs>
VERDICT: <explicação curta>
NEXT: decisão humana ou retorno ao guto-build
```

## Red flags

- executar security/performance/simplification sem trigger;
- revisar apenas o resumo e não o código;
- repetir testes já provados sem motivo;
- classificar nit como bloqueante;
- finding sem localização, mecanismo ou impacto;
- pedir refactor amplo quando uma correção local resolve;
- alterar código dentro do Review;
- aprovar com evidence gap conhecido;
- fazer merge automaticamente;
- iniciar rodadas indefinidas sem informação nova.

## Verificação do Review

- [ ] O review foi ancorado no plano, diff e evidência atual.
- [ ] A superfície foi delimitada.
- [ ] Apenas skills com trigger foram usadas.
- [ ] Findings requeridos possuem evidência e mecanismo concretos.
- [ ] Melhorias opcionais não bloquearam o merge.
- [ ] Correções foram devolvidas ao Build com reteste definido.
- [ ] `MERGE_READY` não foi tratado como autorização de merge.
