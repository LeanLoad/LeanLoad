# third_party

Shared, pinned references for the LeanLoad umbrella checkout.

## Table of contents

```text
abi/              ELF ABI standards and psABI references
impl-analysis/    binary analysis, decompilation, and symbolic execution tools
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

Managed references are not submodules. `fetch.sh` uses pinned source archives
for full source trees:

```sh
./fetch.sh
```

The script creates ignored source trees at the paths listed below.

## Where to look

This map is intentionally implementation-heavy: these are the references most
useful for checking concrete loader, linker, parser, and object-tool behavior.

### Runtime loaders (`impl-loader/`)

`impl-loader/android-bionic` is Android's userspace runtime linker. Start with
`linker/`, then `libdl/` and `libc/` for the surrounding dynamic-loading ABI.

`impl-loader/fex` is a production user-mode emulator with custom ELF handling
for Linux guest tooling. Start with
`Source/Tools/CommonTools/Linux/Utils/ELFParser.*`.

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

`impl-tool/sandboxed-api` has a small custom ELF parser used by Sandbox2
utilities. Start with `sandboxed_api/sandbox2/util/elf_parser.*`.

`impl-tool/swift` includes custom Linux ELF readers used by Swift inspection and
backtrace tooling. Start with
`tools/swift-inspect/Sources/SwiftInspectLinux/ElfFile.swift` and
`stdlib/public/Backtrace/`.

`impl-lib/elfio` is a C++ header-library reference. Start with
`elfio/elfio.hpp` and `examples/`.

`impl-lib/gimli-object` is the Rust `object` crate. The relevant ELF paths are
`src/read/elf/`, `src/write/elf/`, and `src/elf.rs`.

`impl-lib/goblin` is a popular Rust binary parser with ELF support. Start with
`src/elf/`, plus `src/lib.rs` for top-level format dispatch and `src/archive/`
for UNIX archive handling.

`impl-lib/lief` is a library/API-first ELF reference. Use `include/LIEF/ELF/`,
`src/ELF/`, and `api/python/src/ELF/`.

`impl-lib/libbacktrace` is a compact C library with its own ELF and DWARF
reader for stack traces and symbolization. Start with `elf.c`, `dwarf.c`,
`fileline.c`, and `internal.h`.

`impl-lib/rust-elf` is the Rust `elf` crate, a pure Rust parser used by tools
such as Binsider. Start with `src/elf_bytes.rs`, `src/elf_stream.rs`,
`src/parse.rs`, `src/file.rs`, `src/section.rs`, `src/segment.rs`,
`src/symbol.rs`, and `src/relocation.rs`.

### Binary analysis frameworks (`impl-analysis/`)

These references are analysis-first, not all parser-first. Use them when
checking how static analysis, decompilation, reverse engineering, and symbolic
execution tools model ELF inputs.

`impl-analysis/async-profiler` has a focused custom Linux ELF parser for
symbolization in a production JVM profiler. Start with `src/symbols_linux.cpp`.

`impl-analysis/radare2` has an in-tree ELF parser and binary plugin. Start with
`libr/bin/format/elf/` and `libr/bin/p/bin_elf*`.

`impl-analysis/rizin` has an in-tree ELF parser and binary plugin. Start with
`librz/bin/format/elf/` and `librz/bin/p/bin_elf*`.

`impl-analysis/breakpad` has custom Linux ELF utilities for crash-reporting
symbol extraction and file IDs. Start with `src/common/linux/elfutils.*`,
`src/common/linux/file_id.*`, and `src/common/linux/dump_symbols.cc`.

`impl-analysis/crashpad` has custom ELF readers for inspecting mapped images in
crashed processes. Start with `snapshot/elf/`, especially
`elf_image_reader.*`, `elf_dynamic_array_reader.*`, and
`elf_symbol_table_reader.*`.

`impl-analysis/ghidra` has an in-tree Java ELF parser and loader. Start with
`Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/elf/`,
`ElfLoader.java`, and `ElfProgramBuilder.java`.

`impl-analysis/bap` has an in-tree OCaml ELF parser plus an ELF loader plugin.
Start with `lib/bap_elf/` and `plugins/elf_loader/`.

`impl-analysis/retdec` has in-tree ELF file-format support for its decompiler
pipeline. Start with `src/fileformat/`, `include/retdec/fileformat/`,
`elf_wrapper.*`, `elf_detector.*`, and `elf_heuristics.*`.

`impl-analysis/dyninst` has ELF object-file support in SymtabAPI. Start with
`symtabAPI/src/Object-elf.C`, `symtabAPI/src/Object-elf.h`, and
`symtabAPI/src/Elf_X.*`.

`impl-analysis/rr` has an in-tree ELF reader used by its record/replay debugger
for build IDs, symbols, dynamic sections, debug links, and interpreter data.
Start with `src/ElfReader.*`, `src/Dwarf.*`, and `src/Monkeypatcher.*`.

`impl-analysis/angr` is the analysis framework; its ELF loading path lives in
the companion `impl-analysis/cle` checkout. `cle` has ELF loader/backend logic
under `cle/backends/elf/`, but it delegates low-level ELF parsing to
`impl-tool/pyelftools`.

`impl-analysis/manticore` is a symbolic-execution framework with ELF loading
wrappers under `manticore/binary/` and `manticore/native/`; it also delegates
low-level parsing to `impl-tool/pyelftools`.

### Specs and related work

`abi/gabi` and `abi/x86-64-abi` are the primary specification references. Use
`abi/gabi/docsrc/elf/*.rst` for generic ELF and dynamic-linking rules, and
`abi/x86-64-abi` for x86-64 psABI relocation and processor-specific details.

`related-elf/elfsage`, `related-elf/linksem`, `related-elf/minimal-elf`, and
`related-elf/veriload` are adjacent ELF analysis, semantics, and verified
loading references.

`related-parser/daedalus`, `related-parser/everparse`, and `related-parser/vest`
are parser DSL / verified parser framework references.

`related-parser/formatfuzzer` is a binary-format fuzzing and parsing framework
that can generate high-coverage inputs from format specifications.

`related-parser/kaitai-struct-formats` contains `executable/elf.ksy`, a
practical declarative ELF format spec.
