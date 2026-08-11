---
name: guto-verify
description: Prova que a implementação satisfaz os critérios de aceite por meio de testes, builds, queries e evidência runtime selecionados conforme cada claim. Use depois do Build ou para verificar uma correção existente; usa browser-testing somente para superfícies de navegador, debugging somente quando algo falha e não altera o produto por padrão.
---

# Guto Verify

## Objetivo

Converter afirmações de conclusão em evidências atuais e reproduzíveis. Esta skill responde
**“funciona conforme o plano?”**, não **“o código está bom para merge?”**.

Opera em modo read-only por padrão. Quando encontra falha, produz um pedido de correção para
`guto-build`; não corrige silenciosamente e não inicia `guto-review` automaticamente.

## Contrato operacional embutido

- Classifique cada skill-filha como `USE`, `REUSE`, `SKIP` ou `BLOCKED`; leia integralmente apenas
  as marcadas `USE`.
- `USE` significa trigger presente e trabalho ainda não feito; `REUSE`, resultado vigente;
  `SKIP`, trigger ausente; `BLOCKED`, capacidade necessária sem acesso ou dado indispensável.
- Use os artefatos canônicos do projeto. Sem outra convenção, leia e atualize `tasks/plan.md`,
  `tasks/todo.md` e `tasks/state.md`.
- A skill é autocontida: arquivos em `references/` na raiz são documentação complementar, não
  pré-condição de execução.
- Nenhuma transição de fase é automática. `VERIFIED` devolve o controle ao usuário.

## Pré-condição

Aceite uma destas entradas:

- `STATUS=BUILD_READY_FOR_VERIFY` para a versão aprovada;
- implementação já existente com critérios de aceite explícitos;
- correção retornando de Review, com claims afetadas identificadas.

Sem critérios verificáveis, retorne `REPLAN_REQUIRED` ou `BLOCKED`; não invente sucesso depois da
implementação.

## Skills permitidas

Esta skill pode rotear apenas:

- `browser-testing-with-devtools`
- `debugging-and-error-recovery`

Testes de unidade, integração, typecheck, lint, build, queries e scripts são métodos de prova do
repositório, não exigem uma skill adicional para serem executados.

## Triggers

| Skill | `USE` quando | `SKIP` quando |
|---|---|---|
| `browser-testing-with-devtools` | uma claim depende de DOM, interação, console, network, armazenamento do browser, acessibilidade renderizada ou performance frontend | backend, banco, CLI, docs ou código sem comportamento em navegador |
| `debugging-and-error-recovery` | teste, build, query, browser ou comportamento observado falhou de forma inesperada e precisa de causa-raiz | baseline verde ou falha já localizada com pedido de correção objetivo |

## Grafo de verificação

```text
IMPLEMENTAÇÃO + PLANO
        ↓
EXTRAIR CLAIMS / CRITÉRIOS DE ACEITE
        ↓
MAPEAR MÉTODO DE PROVA POR CLAIM
        ↓
ROTEAR BROWSER QUANDO APLICÁVEL
        ↓
EXECUTAR PROVAS REAIS
    ┌───┴────────┐
  falha         passa
    │             │
debugging      registrar evidência
quando útil       │
    │             ├── próxima claim
FIX_REQUEST       └── VERIFIED
    │                    ↓
parar                 PARAR
```

## Processo

### 1. Fixe a versão e a superfície

Leia o plano, checklist, estado e diff atual. Registre:

```text
PLAN_VERSION: <n>
CODE_REVISION: <SHA ou worktree fingerprint disponível>
CLAIMS_TO_VERIFY: <AC-ids ou lista explícita>
```

Evidência de outra versão ou de código alterado não prova o estado atual.

### 2. Monte a matriz de prova antes de executar

Para cada claim, escolha o método mais direto capaz de refutá-la:

| Tipo de claim | Prova preferida |
|---|---|
| função/regra de negócio | teste unitário ou de propriedade |
| integração entre componentes | teste de integração com dependências reais ou fixture representativa |
| API/contrato | teste de contrato, request real controlada ou validação de schema |
| persistência/dado | query, transação de teste ou inspeção de schema |
| build/tipos | comando oficial do pacote/repositório |
| UI/interação | browser runtime com DOM, console e network quando relevantes |
| regressão de bug | caso que falhava antes e agora passa, mais proteção contra recorrência |
| performance | medição comparável com baseline e ambiente declarados |
| documentação/configuração | parser, link checker, dry-run ou inspeção determinística |

Não use screenshot para provar lógica, lint para provar comportamento nem teste unitário para provar
integração real.

### 3. Avalie o roteamento

Classifique as duas skills permitidas como `USE`, `REUSE`, `SKIP` ou `BLOCKED`. Não abra navegador
por padrão e não inicie debugging preventivo.

### 4. Execute do focado ao amplo

Ordem padrão:

1. prova específica de cada claim;
2. testes do pacote/superfície afetada;
3. typecheck/lint/build aplicáveis;
4. suite mais ampla somente quando o blast radius ou política do projeto justificar;
5. runtime/browser/query para claims que não podem ser provadas estaticamente.

Capture comando, saída relevante, exit code e ambiente necessário para reproduzir.

### 5. Trate falhas sem editar o produto

Quando uma prova falhar:

1. confirme que o comando e o ambiente estão corretos;
2. reproduza a falha;
3. use `debugging-and-error-recovery` se a causa não for óbvia;
4. localize a causa suficientemente para delimitar a correção;
5. produza `FIX_REQUEST` com claim, evidência, causa conhecida/hipótese e escopo recomendado;
6. atualize `STATUS=VERIFY_FAILED`;
7. pare e devolva para `guto-build`.

Não masque falha alterando o teste, reduzindo a expectativa ou usando um comando diferente sem
justificativa.

### 6. Registre PASS por claim

Formato recomendado:

```md
| Claim | Método | Evidência atual | Resultado |
|---|---|---|---|
| AC-1 | `pytest tests/x.py::test_y -q` | `1 passed` | PASS |
| AC-2 | Chrome DevTools: rota `/x`, console/network | sem erro; request 200 | PASS |
```

`PASS` exige evidência observada nesta execução ou evidência anterior ainda válida e ligada ao mesmo
código. “Revisei o diff” não é prova runtime.

### 7. Feche a verificação

Somente quando todas as claims obrigatórias estiverem `PASS`:

```text
STATUS: VERIFIED
CURRENT_PHASE: REVIEW
LATEST_EVIDENCE: <matriz resumida>
```

Se uma claim for impossível de provar por falta externa, use `BLOCKED`, não `PASS` presumido.

Não execute `guto-review` automaticamente.

## Saída

### Sucesso

```text
STATUS: VERIFIED
PLAN_VERSION: <n>
CODE_REVISION: <sha/fingerprint>
CLAIMS: <pass/total>
EVIDENCE: <comandos, queries e runtime checks>
SKILLS_USED: <browser quando aplicável>
NEXT: auditoria humana; depois invocar guto-review
```

### Falha

```text
STATUS: VERIFY_FAILED
FAILED_CLAIM: <id>
OBSERVED: <saída real>
EXPECTED: <resultado esperado>
ROOT_CAUSE: <provada | hipótese ainda aberta>
FIX_SCOPE: <arquivos/superfície provável>
RETURN_TO: guto-build
```

## Red flags

- afirmar sucesso sem critérios de aceite;
- usar evidência de código anterior;
- rodar browser para tarefa sem browser;
- chamar debugging quando nada falhou;
- editar código ou teste para “fazer passar” dentro do Verify;
- substituir integração por mock sem declarar a limitação;
- repetir a mesma prova sem mudança ou informação nova;
- marcar `VERIFIED` com claim obrigatória não testada;
- iniciar Review automaticamente.

## Verificação da própria fase

- [ ] Claims vieram do plano/aceite, não foram inventadas depois.
- [ ] Cada claim possui método de prova adequado.
- [ ] Browser foi usado apenas quando necessário.
- [ ] Falhas inesperadas foram reproduzidas/localizadas.
- [ ] Nenhuma correção foi aplicada silenciosamente.
- [ ] Evidências estão ligadas à versão atual do código.
- [ ] O resultado final é `VERIFIED`, `VERIFY_FAILED`, `REPLAN_REQUIRED` ou `BLOCKED`.
