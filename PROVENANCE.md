# Provenance

Este arquivo registra as fontes usadas para desenhar o pacote. Os SHAs fixam o estado consultado;
não significam que o conteúdo upstream foi copiado para este repositório.

## Agent Skills

- Repositório: `addyosmani/agent-skills`
- Commit consultado: `7676817c12a1317454ae3898a0c5c1eacf5dd3d5`
- Data do commit: 2026-08-08
- Uso: dependência externa das skills-folha; convenção de `SKILL.md`, triggers, progressive
  disclosure e workflows especializados.
- Conteúdo vendorizado: nenhum.

## Superpowers

- Repositório: `obra/superpowers`
- Commit consultado: `44c9b2d6e889982ac18c27d05a19fefe335194e1`
- Data do commit: 2026-07-27/28
- Uso: referência arquitetural para separar brainstorming/plano, execução com checklist,
  verificação e review com checkpoints humanos.
- Conteúdo vendorizado: nenhum.

## Orion's Belt

- Repositório: `gutocarollo/orions-belt`
- Commit consultado: `f8a3a169e1644abdaedbf2353a6311c8d19b7798`
- Data do commit: 2026-08-11
- Uso: requisitos do usuário para persistência do objetivo, checkboxes, anti-drift e o conceito de
  `clarification-plan`.
- Port realizado: reescrita independente e reduzida; não foram trazidos Council, hooks, scoring,
  ledger, execution graph, commits obrigatórios ou contratos determinísticos.

## Decisão de arquitetura

`guto-skills` começa deliberadamente pequeno. Novos componentes do Orion's Belt só devem ser
portados quando houver um problema observado neste pacote e evidência de que o componente resolve o
problema com custo proporcional.
