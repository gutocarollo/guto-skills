# MakersHub Branch Profile

This branch extends the generic `main` exploration model for the repository family:

- `makershub`
- `airflow`
- `salesforce`

For those repositories, `context-engineering` always attempts three discovery lanes before declaring context sufficient:

1. lexical search (`rg` / `grep` / runtime equivalent);
2. CodeGraph;
3. FazGraph.

FazGraph is used for project/domain relationships that a single repository's code graph cannot safely express, including Airflow-to-database-to-MakersHub flows, Salesforce object/field mappings, cross-repository consumers and producers, and data-lineage blast radius.

The branch keeps the same non-Council design as `main`:

- no context state machine;
- no lifecycle receipts;
- no evidence ledger;
- no fixed number of exploration rounds;
- no automatic subagent swarm;
- no automatic transition between Guto phases.

The exploration loop repeats only when evidence exposes a new material relationship or unresolved question. PostgreSQL and other live-state tools remain conditional: they are used to settle concrete facts that code and graph evidence cannot prove.

When this branch is used in an unrelated repository, the generic profile remains active and FazGraph is not invoked.
