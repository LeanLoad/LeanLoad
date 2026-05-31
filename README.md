# LeanLoad

Umbrella checkout for the LeanLoad repositories. This repo owns the shared
setup scripts and pinned `third_party` dependencies; implementation repos live
as top-level submodules.

## Layout

```text
ElfLoader/      # verified ELF loader Lean package
ELFine/         # related ELF/Lean repo
ElfZoo/         # related ELF corpus/tools repo
LeanOnWasm/     # Lean-on-WebAssembly demo repo
WhatTheElf/     # related ELF repo
third_party/    # shared specs, references, and fixture build deps
  abi/             # gABI, GNU ABI extensions, psABI references
  impl-loader/     # concrete runtime loader implementations
  impl-tool/       # compiler/linker/binary utility toolchains
  impl-lib/        # ELF/object libraries
  impl-parser/     # parser-only implementation references
  lean-ref/        # Lean tooling, books, and reference libraries
  related-elf/     # related verified-loader / ELF work
  related-lean/    # related Lean verification work
  related-parser/  # related parser / binary-format work
```

## Quick start

```sh
git clone --recurse-submodules git@github.com:LeanLoad/LeanLoad.git
cd LeanLoad
./setup.sh
make run
```

`setup.sh` installs the system C toolchain and elan, then initializes the
top-level project submodules plus `third_party/impl-loader/musl` for the end-to-end
ElfLoader fixture run. Each Lean submodule owns its own `lean-toolchain`;
the umbrella repo intentionally does not duplicate one. Initialize all
reference/spec submodules with:

```sh
git submodule update --init --recursive
```
