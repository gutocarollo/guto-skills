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

Selected files under `skills/` and `references/` are vendored byte-for-byte from:

- Project: `addyosmani/agent-skills`
- Upstream commit: `7676817c12a1317454ae3898a0c5c1eacf5dd3d5`
- License: MIT
- Copyright: retained under the upstream license

The exact paths and Git blob hashes are recorded in `UPSTREAM_LOCK.json`. The complete upstream MIT notice is preserved in `THIRD_PARTY_LICENSES.md`.

The vendored material is included so the four orchestrators can resolve and read their child skills locally. Guto Skills does not claim authorship of the upstream workflows.

## Orion's Belt

The phase separation and `clarification-plan` intent were informed by operational lessons from `gutocarollo/orions-belt`. No Council engine, deterministic hook suite, scoring system, evidence ledger, or graph-state contract is copied into this clean package.
