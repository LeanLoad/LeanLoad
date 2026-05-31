# third_party

Shared, pinned references for the LeanLoad umbrella checkout.

## Table of contents

```text
abi/              ELF ABI standards and psABI references
impl-loader/      concrete runtime loader implementations
impl-linker/      linker implementations and linker-capable toolchains
impl-tool/        binary inspection and rewriting tools
impl-lib/         ELF/object libraries
impl-parser/      parser-only implementation references
lean-ref/         Lean tooling, books, and reference libraries
related-elf/      related verified-loader / ELF work
related-lean/     related Lean verification work
related-parser/   related parser / binary-format work
```

Implementation repos should prefer a `THIRD_PARTY_DIR` setting or paths through
the umbrella checkout instead of adding duplicate submodules. Keep deliberately
different version pins local to the consuming repo until they are reconciled.

Large repositories are not submodules. Fetch only the relevant paths with:

```sh
third_party/fetch.py
```

The script creates ignored sparse checkouts at the paths listed below.

## Where to look

| Repo | Useful ELF / loader paths |
| --- | --- |
| `abi/gabi` | `docsrc/elf/*.rst` for generic ELF and dynamic-linking rules. |
| `abi/x86-64-abi` | x86-64 psABI processor-specific ELF details and relocation semantics. |
| `impl-loader/android-bionic` | `linker/`, `libdl/`, `libc/`, and Android-specific runtime linking behavior. |
| `impl-loader/freebsd-src` | `libexec/rtld-elf/`, plus ELF constants in `sys/sys/elf*.h`. |
| `impl-loader/glibc` | `elf/dl-load.c`, `elf/rtld.c`, `elf/dl-reloc.c`, `elf/dl-lookup.c`, `elf/dynamic-link.h`. |
| `impl-loader/illumos-gate` | Userspace loader in `usr/src/cmd/sgs/rtld/`; linker support in `usr/src/cmd/sgs/libld/`; kernel ELF definitions in `usr/src/uts/common/sys/elf*.h`. |
| `impl-loader/musl` | `ldso/dynlink.c`, `crt/*`, `arch/*/reloc.h`. |
| `impl-loader/netbsd-src` | Userspace loader in `libexec/ld.elf_so/`; kernel ELF exec support and constants around `sys/sys/exec_elf.h`. |
| `impl-loader/openbsd-src` | Userspace loader in `libexec/ld.so/`; kernel ELF exec support and constants around `sys/sys/exec_elf.h`. |
| `impl-loader/qemu` | `linux-user/elfload.c`, `bsd-user/elfload.c`, `hw/core/loader.c`, `include/hw/elf_ops.h`. |
| `impl-linker/binutils-gdb` | `bfd/elf*.c`, `binutils/readelf.c`, `binutils/objdump.c`, `ld/`, `gas/`. |
| `impl-linker/go` | `src/debug/elf/`, `src/cmd/link/internal/ld/`, `src/cmd/link/internal/loader/`. |
| `impl-linker/llvm-project` | `llvm/include/llvm/Object/ELF*.h`, `llvm/lib/Object/ELF*.cpp`, `llvm/tools/llvm-readobj/`, `llvm/tools/llvm-objdump/`, `lld/ELF/`. |
| `impl-linker/mold` | `elf/` for the modern ELF linker implementation. |
| `impl-linker/zig` | `src/link/Elf.zig`, `src/link/Elf/`, `src/arch/*/CodeGen.zig`, `lib/std/elf.zig`. |
| `impl-tool/patchelf` | `src/patchelf.cc` for practical ELF rewriting. |
| `impl-tool/pax-utils` | `scanelf.c`, `lddtree.py`, and related binary-inspection utilities. |
| `impl-lib/elfutils` | `libelf/`, `libdwelf/`, `src/readelf.c`, `src/elflint.c`, `src/objdump.c`. |
| `impl-lib/lief` | `include/LIEF/ELF/`, `src/ELF/`, `api/python/src/ELF/`. |
| `impl-lib/elfio` | `elfio/elfio.hpp`, `examples/`. |
| `impl-lib/gimli-object` | `src/read/elf/`, `src/write/elf/`, `src/elf.rs`. |
| `impl-parser/pyelftools` | `elftools/elf/`, especially `elffile.py`, `sections.py`, `segments.py`, `dynamic.py`, `relocation.py`. |
| `related-elf/elfsage` | Related ELF analysis/spec work. |
| `related-elf/linksem` | Related executable/linker semantics. |
| `related-elf/minimal-elf` | Minimal ELF examples and explanations. |
| `related-elf/veriload` | Related verified loading work and bundled ABI references. |
| `related-parser/daedalus` | Parser DSL examples and binary parsing infrastructure. |
| `related-parser/everparse` | Verified parser/serializer framework references. |
| `related-parser/kaitai-struct-formats` | `executable/elf.ksy` for a practical declarative ELF format spec. |
| `related-parser/vest` | Verified parser/serializer framework references. |
