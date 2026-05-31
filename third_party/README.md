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

`impl-loader/android-bionic` is Android's userspace runtime linker. Start with
`linker/`, then `libdl/` and `libc/` for the surrounding dynamic-loading ABI.

`impl-loader/glibc` is the main GNU/Linux runtime loader reference. The most
useful files are `elf/dl-load.c`, `elf/rtld.c`, `elf/dl-reloc.c`,
`elf/dl-lookup.c`, and `elf/dynamic-link.h`.

`impl-loader/musl` is a compact libc/runtime-loader implementation. The loader
is centered in `ldso/dynlink.c`, with startup and architecture details in
`crt/*` and `arch/*/reloc.h`.

`impl-loader/qemu` has concrete emulated ELF loaders. Look at
`linux-user/elfload.c`, `bsd-user/elfload.c`, `hw/core/loader.c`, and
`include/hw/elf_ops.h`.

`impl-loader/valgrind` is useful for userspace executable and object loading in
an instrumentation runtime. Start with `coregrind/m_ume/` and
`coregrind/m_debuginfo/`.

### Kernel exec loaders (`impl-kernel/`)

`impl-kernel/freebsd-src` covers FreeBSD's kernel ELF exec contract. Use
`sys/sys/elf*.h` for kernel constants and `libexec/rtld-elf/` when comparing
the userspace runtime linker paired with it.

`impl-kernel/illumos-gate` covers illumos ELF exec and runtime-linker sources.
Use `usr/src/uts/common/sys/elf*.h` for kernel ELF definitions and
`usr/src/cmd/sgs/rtld/` for userspace `ld.so.1`.

`impl-kernel/linux` is the canonical Linux exec loader reference. Start with
`fs/binfmt_elf.c`, `fs/binfmt_elf_fdpic.c`, `include/uapi/linux/elf.h`, and
`arch/*/include/asm/elf.h`.

`impl-kernel/netbsd-src` covers NetBSD's kernel ELF exec path. Use
`sys/sys/exec_elf.h` for kernel support and `libexec/ld.elf_so/` for its
userspace runtime linker.

`impl-kernel/openbsd-src` covers OpenBSD's kernel ELF exec path. Use
`sys/sys/exec_elf.h` for kernel support and `libexec/ld.so/` for its userspace
runtime linker.

### Linkers and ELF producers (`impl-linker/`)

`impl-linker/binutils-gdb` is the GNU linker/toolchain reference. The important
paths are `ld/`, `gas/`, `bfd/elf*.c`, `binutils/readelf.c`, and
`binutils/objdump.c`.

`impl-linker/go` is useful because the Go toolchain has its own ELF linker.
Start with `src/cmd/link/internal/ld/`, `src/cmd/link/internal/loader/`, and
`src/debug/elf/`.

`impl-linker/llvm-project` covers LLVM's object model and `lld`. Use
`lld/ELF/`, `llvm/include/llvm/Object/ELF*.h`, `llvm/lib/Object/ELF*.cpp`,
`llvm/tools/llvm-readobj/`, and `llvm/tools/llvm-objdump/`.

`impl-linker/mold` is a modern ELF linker with a comparatively direct codebase.
Most of the interesting implementation is under `elf/`.

`impl-linker/zig` is useful for Zig's self-hosted ELF linker and emitter. Look
at `src/link/Elf.zig`, `src/link/Elf/`, `src/arch/*/CodeGen.zig`, and
`lib/std/elf.zig`.

### ELF tools and libraries (`impl-tool/`, `impl-lib/`)

`impl-tool/elfutils` is the main external ELF analysis/checking tool reference.
Use `src/elflint.c`, `src/readelf.c`, `src/objdump.c`, `libelf/`, and
`libdwelf/`.

`impl-tool/patchelf` is a practical ELF rewriting reference. Its behavior is
mostly concentrated in `src/patchelf.cc`.

`impl-tool/pax-utils` provides binary-inspection utilities. The most relevant
entry points are `scanelf.c` and `lddtree.py`.

`impl-tool/pyelftools` is a parser/tooling oracle for ELF and DWARF. The useful
modules are under `elftools/elf/`, especially `elffile.py`, `sections.py`,
`segments.py`, `dynamic.py`, and `relocation.py`.

`impl-lib/elfio` is a C++ header-library reference. Start with
`elfio/elfio.hpp` and `examples/`.

`impl-lib/gimli-object` is the Rust `object` crate. The relevant ELF paths are
`src/read/elf/`, `src/write/elf/`, and `src/elf.rs`.

`impl-lib/lief` is a library/API-first ELF reference. Use `include/LIEF/ELF/`,
`src/ELF/`, and `api/python/src/ELF/`.

### Specs and related work

`abi/gabi` and `abi/x86-64-abi` are the primary specification references. Use
`abi/gabi/docsrc/elf/*.rst` for generic ELF and dynamic-linking rules, and
`abi/x86-64-abi` for x86-64 psABI relocation and processor-specific details.

`related-elf/elfsage`, `related-elf/linksem`, `related-elf/minimal-elf`, and
`related-elf/veriload` are adjacent ELF analysis, semantics, and verified
loading references.

`related-parser/daedalus`, `related-parser/everparse`, and `related-parser/vest`
are parser DSL / verified parser framework references.

`related-parser/kaitai-struct-formats` contains `executable/elf.ksy`, a
practical declarative ELF format spec.
