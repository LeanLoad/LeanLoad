# third_party

Shared, pinned references for the LeanLoad umbrella checkout.

## Table of contents

```text
abi/              ELF ABI standards and psABI references
impl-loader/      concrete runtime loader implementations
impl-kernel/      kernel ELF exec loaders and OS exec ABI support
impl-linker/      linker implementations and linker-capable toolchains
impl-tool/        binary inspection, parsing, and rewriting tools
impl-lib/         ELF/object libraries
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

This map is intentionally implementation-heavy: these are the references most
useful for checking concrete loader, linker, parser, and object-tool behavior.

### Runtime loaders (`impl-loader/`)

| Repo | Useful paths |
| --- | --- |
| `impl-loader/android-bionic` | `linker/`, `libdl/`, `libc/` for Android runtime linking behavior. |
| `impl-loader/glibc` | `elf/dl-load.c`, `elf/rtld.c`, `elf/dl-reloc.c`, `elf/dl-lookup.c`, `elf/dynamic-link.h`. |
| `impl-loader/musl` | `ldso/dynlink.c`, `crt/*`, `arch/*/reloc.h`. |
| `impl-loader/qemu` | `linux-user/elfload.c`, `bsd-user/elfload.c`, `hw/core/loader.c`, `include/hw/elf_ops.h`. |
| `impl-loader/valgrind` | `coregrind/m_ume/`, `coregrind/m_debuginfo/` for userspace executable/object loading. |

### Kernel exec loaders (`impl-kernel/`)

| Repo | Useful paths |
| --- | --- |
| `impl-kernel/freebsd-src` | `sys/sys/elf*.h` for kernel ELF exec support and constants; `libexec/rtld-elf/` for userspace rtld. |
| `impl-kernel/illumos-gate` | `usr/src/uts/common/sys/elf*.h` for kernel ELF definitions; `usr/src/cmd/sgs/rtld/` for userspace rtld. |
| `impl-kernel/linux` | `fs/binfmt_elf.c`, `fs/binfmt_elf_fdpic.c`, `include/uapi/linux/elf.h`, `arch/*/include/asm/elf.h`. |
| `impl-kernel/netbsd-src` | `sys/sys/exec_elf.h` for kernel ELF exec support and constants; `libexec/ld.elf_so/` for userspace rtld. |
| `impl-kernel/openbsd-src` | `sys/sys/exec_elf.h` for kernel ELF exec support and constants; `libexec/ld.so/` for userspace rtld. |

### Linkers and ELF producers (`impl-linker/`)

| Repo | Useful paths |
| --- | --- |
| `impl-linker/binutils-gdb` | `ld/`, `gas/`, `bfd/elf*.c`, `binutils/readelf.c`, `binutils/objdump.c`. |
| `impl-linker/go` | `src/cmd/link/internal/ld/`, `src/cmd/link/internal/loader/`, `src/debug/elf/`. |
| `impl-linker/llvm-project` | `lld/ELF/`, `llvm/include/llvm/Object/ELF*.h`, `llvm/lib/Object/ELF*.cpp`, `llvm/tools/llvm-readobj/`, `llvm/tools/llvm-objdump/`. |
| `impl-linker/mold` | `elf/` for the modern ELF linker implementation. |
| `impl-linker/zig` | `src/link/Elf.zig`, `src/link/Elf/`, `src/arch/*/CodeGen.zig`, `lib/std/elf.zig`. |

### ELF tools and libraries (`impl-tool/`, `impl-lib/`)

| Repo | Useful paths |
| --- | --- |
| `impl-tool/elfutils` | `src/elflint.c`, `src/readelf.c`, `src/objdump.c`, `libelf/`, `libdwelf/`. |
| `impl-tool/patchelf` | `src/patchelf.cc` for practical ELF rewriting. |
| `impl-tool/pax-utils` | `scanelf.c`, `lddtree.py`, and related binary-inspection utilities. |
| `impl-tool/pyelftools` | `elftools/elf/`, especially `elffile.py`, `sections.py`, `segments.py`, `dynamic.py`, `relocation.py`. |
| `impl-lib/elfio` | `elfio/elfio.hpp`, `examples/`. |
| `impl-lib/gimli-object` | `src/read/elf/`, `src/write/elf/`, `src/elf.rs`. |
| `impl-lib/lief` | `include/LIEF/ELF/`, `src/ELF/`, `api/python/src/ELF/`. |

### Specs and related work

| Repo | Useful paths |
| --- | --- |
| `abi/gabi` | `docsrc/elf/*.rst` for generic ELF and dynamic-linking rules. |
| `abi/x86-64-abi` | x86-64 psABI processor-specific ELF details and relocation semantics. |
| `related-elf/elfsage` | Related ELF analysis/spec work. |
| `related-elf/linksem` | Related executable/linker semantics. |
| `related-elf/minimal-elf` | Minimal ELF examples and explanations. |
| `related-elf/veriload` | Related verified loading work and bundled ABI references. |
| `related-parser/daedalus` | Parser DSL examples and binary parsing infrastructure. |
| `related-parser/everparse` | Verified parser/serializer framework references. |
| `related-parser/kaitai-struct-formats` | `executable/elf.ksy` for a practical declarative ELF format spec. |
| `related-parser/vest` | Verified parser/serializer framework references. |
