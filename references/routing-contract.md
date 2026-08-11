# Contrato de roteamento condicional

Este contrato é compartilhado por `guto-plan`, `guto-build`, `guto-verify` e `guto-review`.
Ele existe para impedir dois extremos: ignorar uma skill útil ou executar todo o catálogo em toda
tarefa.

## Decisões de roteamento

Antes de carregar uma skill-filha, classifique-a em exatamente um estado:

| Estado | Significado | Ação |
|---|---|---|
| `USE` | O trigger da skill está presente e o trabalho ainda não foi feito | Leia a skill inteira e aplique o workflow relevante |
| `REUSE` | Um resultado anterior continua válido para a versão atual do plano/código | Consuma o artefato; não repita o workflow |
| `SKIP` | O trigger não está presente | Registre uma justificativa curta; não carregue a skill |
| `BLOCKED` | A skill é necessária, mas falta acesso, dado ou ferramenta indispensável | Pare somente o ramo afetado e declare o bloqueio concreto |

A existência da skill no catálogo nunca é justificativa para `USE`.

## Formato mínimo

```md
## Skill routing

| Skill | Estado | Trigger observado | Justificativa |
|---|---|---|---|
| context-engineering | USE | contexto insuficiente para decidir arquitetura | ... |
| frontend-ui-engineering | SKIP | nenhuma superfície visual será alterada | ... |
```

Não produza essa tabela para trabalho trivial quando uma frase resolver. O objetivo é tornar a
seleção auditável, não criar burocracia.

## Profundidade proporcional

Use `DEPTH=AUTO` por padrão e infira a profundidade pelo risco real:

- `LIGHT`: alteração mecânica, local, reversível e com critério de sucesso óbvio;
- `STANDARD`: feature ou correção normal, com mais de uma decisão ou superfície;
- `DEEP`: mudança difícil de reverter, alto blast radius, segurança, produção, migração ou fatos
  importantes ainda incertos.

Número de linhas ou arquivos é sinal auxiliar, não critério suficiente. Uma linha em autorização
pode exigir `DEEP`; dez arquivos de rename podem continuar `LIGHT`.

## Regras anti-rigidez

1. Não execute todas as skills “por segurança”.
2. Não use subagentes, councils ou paralelismo sem ganho concreto de independência, cobertura ou
   redução de tempo.
3. Não repita leitura, pesquisa, build ou teste quando o artefato continua válido e o código não
   mudou.
4. Não transforme um detalhe local e reversível em decisão humana.
5. Não faça pergunta sobre fato pesquisável; investigue primeiro.
6. Não bloqueie a fase por melhoria opcional, preferência estilística ou risco sem impacto material.
7. Uma nova rodada só é justificável quando acrescenta evidência material, fecha uma decisão,
   corrige uma falha ou invalida uma premissa.
8. Se uma rodada não produzir informação material nova, encerre-a e exponha o estado atual.

## Carregamento progressivo

No início, use apenas nomes, descrições e triggers. Leia o `SKILL.md` completo somente para skills
classificadas como `USE`. Leia referências suplementares apenas quando o workflow alcançar o ponto
que precisa delas.

## Dependência upstream

As quatro skills `guto-*` compõem workflows, mas não duplicam as skills-folha do
`addyosmani/agent-skills`. O pacote upstream deve estar instalado no mesmo runtime. Quando uma
skill-filha não estiver disponível:

- marque `BLOCKED` se ela for indispensável;
- aplique diretamente apenas princípios simples já descritos na skill `guto-*`;
- não finja que executou uma skill ausente.
