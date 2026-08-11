# Notices and Provenance

## Guto Skills orchestration

The following files are original work in this repository and are released under the root MIT license:

- `skills/guto-plan/SKILL.md`
- `skills/guto-build/SKILL.md`
- `skills/guto-verify/SKILL.md`
- `skills/guto-review/SKILL.md`
- `skills/clarification-plan/SKILL.md`
- repository documentation, manifests, lock metadata, and validation tooling

## Vendored Agent Skills

Selected files under `skills/` and `references/` originate from:

- Project: `addyosmani/agent-skills`
- Upstream commit: `7676817c12a1317454ae3898a0c5c1eacf5dd3d5`
- License: MIT
- Copyright: retained under the upstream license

Most selected files remain vendored byte-for-byte. `skills/context-engineering/SKILL.md` is an intentional local adaptation of the upstream skill: it preserves the context-curation purpose while adding a repository exploration and convergence workflow based on lexical search, CodeGraph, focused source reads, and conditional live-state evidence.

`UPSTREAM_LOCK.json` distinguishes byte-for-byte files from locally adapted upstream files and records both the reviewed upstream blob identity and the local blob identity. The complete upstream MIT notice is preserved in `THIRD_PARTY_LICENSES.md`.

The vendored material is included so the four orchestrators can resolve and read their child skills locally. Guto Skills does not claim authorship of the upstream workflows.

## Orion's Belt

The phase separation, `clarification-plan` intent, and exploration ordering were informed by operational lessons from `gutocarollo/orions-belt`, including its distinction between lexical enumeration, known-symbol impact, dynamic state flow, docs/config work, and live-state investigation.

This repository deliberately does not copy the Orion's Belt Council engine, deterministic context state machine, lifecycle receipts, evidence ledger, scoring system, or graph-state gates. The exploration behavior is implemented as a lightweight reasoning workflow inside `context-engineering`.
