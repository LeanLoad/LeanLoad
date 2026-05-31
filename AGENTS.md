# AGENTS.md

Research project. No backward compatibility required.

## Umbrella workspace

This repository coordinates the LeanLoad project family. Keep implementation
rules in each submodule's own `AGENTS.md`; this file is only for workspace-wide
organization.

- Prefer direct refactors over compatibility shims.
- Keep project repos as top-level submodules.
- Keep shared references in `third_party/`; consuming repos should use umbrella
  paths or a `THIRD_PARTY_DIR` setting instead of adding duplicate submodules.
- Do not add a top-level `lean-toolchain`. Each Lean submodule owns its own
  toolchain pin.
- Keep `.gitmodules` paths and `third_party/README.md` in sync.

## Reference map

Use `third_party/README.md` as the table of contents for vendored references,
including where to look inside large repositories for ELF, ABI, linker, loader,
and parser behavior.

## Lean 4 workflows

Before Lean proof work, build debugging, mathlib search, or larger Lean
refactors, read:

```text
third_party/lean-ref/lean4-skills/plugins/lean4/skills/lean4/SKILL.md
```

Environment, from the umbrella repository root:

```sh
LEAN4_PLUGIN_ROOT=$PWD/third_party/lean-ref/lean4-skills/plugins/lean4
LEAN4_SCRIPTS=$LEAN4_PLUGIN_ROOT/lib/scripts
LEAN4_REFS=$LEAN4_PLUGIN_ROOT/skills/lean4/references
```
