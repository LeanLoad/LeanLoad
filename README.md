# LeanLoad

Umbrella checkout for the LeanLoad repositories. This repo owns the shared
setup scripts and pinned `third_party` dependencies; implementation repos live
as top-level submodules.

## Layout

```text
ElfLoader/      # verified ELF loader Lean package
ELFine/         # Lean ELF format modeling, including ELFine.WhatTheElf
ElfSpec/        # Lean ELF specification experiments
ElfZoo/         # related ELF corpus/tools repo
LeanOnWasm/     # Lean-on-WebAssembly demo repo
WhatTheElf/     # Python malformed-ELF generator/checker
third_party/    # shared specs, references, and fixture build deps
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

## Third-party references

Shared, pinned references for the LeanLoad umbrella checkout live under
`third_party/`.

Implementation repos should prefer a `THIRD_PARTY_DIR` setting or paths through
the umbrella checkout instead of adding duplicate submodules. Keep deliberately
different version pins local to the consuming repo until they are reconciled.

Managed references are not submodules. `third_party/fetch.sh` uses pinned source
archives for full source trees:

```sh
cd third_party
./fetch.sh
```

The script creates ignored source trees at the paths listed below.

### Directory map

```text
abi/              ELF ABI standards and psABI references
impl-debug/       crash, profiling, symbolization, debugger, and instrumentation references
impl-kernel/      kernel ELF exec loaders and OS exec ABI support
impl-lang/        language runtimes and toolchains with ELF readers/producers
impl-lib/         ELF/object libraries
impl-linker/      linker implementations
impl-loader/      concrete runtime loader implementations
impl-re/          reverse engineering, decompilation, and symbolic execution tools
impl-tool/        binary inspection, parsing, rewriting, and packaging tools
lean-ref/         Lean tooling, books, and reference libraries
related-elf/      related verified-loader / ELF work
related-lean/     related Lean verification work
related-parser/   related parser / binary-format work
```

### Where to look

This map is intentionally implementation-heavy: these are the references most
useful for checking concrete loader, linker, parser, and object-tool behavior.

#### Runtime loaders (`third_party/impl-loader/`)

`third_party/impl-loader/android-bionic` is Android's userspace runtime linker.
Start with `linker/`, then `libdl/` and `libc/` for the surrounding
dynamic-loading ABI.

`third_party/impl-loader/fex` is a production user-mode emulator with custom ELF
handling for Linux guest tooling. Start with
`Source/Tools/CommonTools/Linux/Utils/ELFParser.*`.

`third_party/impl-loader/glibc` is the main GNU/Linux runtime loader reference.
The most useful files are `elf/dl-load.c`, `elf/rtld.c`, `elf/dl-reloc.c`,
`elf/dl-lookup.c`, and `elf/dynamic-link.h`.

`third_party/impl-loader/musl` is a compact libc/runtime-loader implementation.
The loader is centered in `ldso/dynlink.c`, with startup and architecture
details in `crt/*` and `arch/*/reloc.h`.

`third_party/impl-loader/qemu` has concrete emulated ELF loaders. Look at
`linux-user/elfload.c`, `bsd-user/elfload.c`, `hw/core/loader.c`, and
`include/hw/elf_ops.h`.

`third_party/impl-loader/valgrind` is useful for userspace executable and object
loading in an instrumentation runtime. Start with `coregrind/m_ume/` and
`coregrind/m_debuginfo/`.

#### Kernel exec loaders (`third_party/impl-kernel/`)

`third_party/impl-kernel/freebsd-src` covers FreeBSD's kernel ELF exec contract.
Use `sys/sys/elf*.h` for kernel constants and `libexec/rtld-elf/` when comparing
the userspace runtime linker paired with it.

`third_party/impl-kernel/illumos-gate` covers illumos ELF exec and
runtime-linker sources. Use `usr/src/uts/common/sys/elf*.h` for kernel ELF
definitions and `usr/src/cmd/sgs/rtld/` for userspace `ld.so.1`.

`third_party/impl-kernel/linux` is the canonical Linux exec loader reference.
Start with `fs/binfmt_elf.c`, `fs/binfmt_elf_fdpic.c`,
`include/uapi/linux/elf.h`, and `arch/*/include/asm/elf.h`.

`third_party/impl-kernel/netbsd-src` covers NetBSD's kernel ELF exec path. Use
`sys/sys/exec_elf.h` for kernel support and `libexec/ld.elf_so/` for its
userspace runtime linker.

`third_party/impl-kernel/openbsd-src` covers OpenBSD's kernel ELF exec path. Use
`sys/sys/exec_elf.h` for kernel support and `libexec/ld.so/` for its userspace
runtime linker.

#### Language runtimes and toolchains (`third_party/impl-lang/`)

`third_party/impl-lang/dart-sdk` includes Dart VM ELF writer/reader support for
AOT snapshots. Start with `runtime/platform/elf.h` and `runtime/vm/elf.cc`.

`third_party/impl-lang/go` is useful because the Go toolchain has its own ELF
linker and parser package. Start with `src/cmd/link/internal/ld/`,
`src/cmd/link/internal/loader/`, and `src/debug/elf/`.

`third_party/impl-lang/openjdk-jdk` has HotSpot ELF readers for JVM
symbolization and diagnostics. Start with
`src/hotspot/share/utilities/elfFile.*`, `elfStringTable.*`,
`elfSymbolTable.*`, and `dwarfFile.*`.

`third_party/impl-lang/swift` includes custom Linux ELF readers used by Swift
inspection and backtrace tooling. Start with
`tools/swift-inspect/Sources/SwiftInspectLinux/ElfFile.swift` and
`stdlib/public/Backtrace/`.

`third_party/impl-lang/zig` is useful for Zig's self-hosted ELF linker and
emitter. Look at `src/link/Elf.zig`, `src/link/Elf/`,
`src/arch/*/CodeGen.zig`, and `lib/std/elf.zig`.

#### Linkers (`third_party/impl-linker/`)

`third_party/impl-linker/binutils-gdb` is the GNU linker/toolchain reference.
The important paths are `ld/`, `gas/`, `bfd/elf*.c`, `binutils/readelf.c`, and
`binutils/objdump.c`.

`third_party/impl-linker/llvm-project` covers LLVM's object model and `lld`. Use
`lld/ELF/`, `llvm/include/llvm/Object/ELF*.h`, `llvm/lib/Object/ELF*.cpp`,
`llvm/tools/llvm-readobj/`, and `llvm/tools/llvm-objdump/`.

`third_party/impl-linker/mold` is a modern ELF linker with a comparatively
direct codebase. Most of the interesting implementation is under `elf/`.

#### ELF tools and libraries (`third_party/impl-tool/`, `third_party/impl-lib/`)

`third_party/impl-tool/elfutils` is the main external ELF analysis/checking tool
reference. Use `src/elflint.c`, `src/readelf.c`, `src/objdump.c`, `libelf/`,
and `libdwelf/`.

`third_party/impl-tool/patchelf` is a practical ELF rewriting reference. Its
behavior is mostly concentrated in `src/patchelf.cc`.

`third_party/impl-tool/pax-utils` provides binary-inspection utilities. The most
relevant entry points are `scanelf.c` and `lddtree.py`.

`third_party/impl-tool/pyelftools` is a parser/tooling oracle for ELF and DWARF.
The useful modules are under `elftools/elf/`, especially `elffile.py`,
`sections.py`, `segments.py`, `dynamic.py`, and `relocation.py`. Downstream
consumers that use pyelftools as their low-level ELF parser include the `cle`
loader (which is in turn used by the `angr` analysis framework) and the
`manticore` symbolic-execution framework.

`third_party/impl-tool/sandboxed-api` has a small custom ELF parser used by
Sandbox2 utilities. Start with `sandboxed_api/sandbox2/util/elf_parser.*`.

`third_party/impl-tool/upx` is a mature executable packer with custom ELF
read/modify/write logic. Start with `src/p_elf.h`, `src/p_elf_enum.h`, and
`src/p_lx_elf.*`.

`third_party/impl-lib/elfio` is a C++ header-library reference. Start with
`elfio/elfio.hpp` and `examples/`.

`third_party/impl-lib/gimli-object` is the Rust `object` crate. The relevant ELF
paths are `src/read/elf/`, `src/write/elf/`, and `src/elf.rs`.

`third_party/impl-lib/goblin` is a popular Rust binary parser with ELF support.
Start with `src/elf/`, plus `src/lib.rs` for top-level format dispatch and
`src/archive/` for UNIX archive handling.

`third_party/impl-lib/lief` is a library/API-first ELF reference. Use
`include/LIEF/ELF/`, `src/ELF/`, and `api/python/src/ELF/`.

`third_party/impl-lib/rust-elf` is the Rust `elf` crate, a pure Rust parser used
by tools such as Binsider. Start with `src/elf_bytes.rs`, `src/elf_stream.rs`,
`src/parse.rs`, `src/file.rs`, `src/section.rs`, `src/segment.rs`,
`src/symbol.rs`, and `src/relocation.rs`.

#### Debugging, profiling, and instrumentation (`third_party/impl-debug/`)

These references are observability-first: crash reporting, symbolization,
profiling, debugging, unwinding, and dynamic instrumentation runtimes.

`third_party/impl-debug/async-profiler` has a focused custom Linux ELF parser
for symbolization in a production JVM profiler. Start with
`src/symbols_linux.cpp`.

`third_party/impl-debug/breakpad` has custom Linux ELF utilities for
crash-reporting symbol extraction and file IDs. Start with
`src/common/linux/elfutils.*`, `src/common/linux/file_id.*`, and
`src/common/linux/dump_symbols.cc`.

`third_party/impl-debug/crashpad` has custom ELF readers for inspecting mapped
images in crashed processes. Start with `snapshot/elf/`, especially
`elf_image_reader.*`, `elf_dynamic_array_reader.*`, and
`elf_symbol_table_reader.*`.

`third_party/impl-debug/dynamorio` has a custom core ELF loader in its dynamic
instrumentation runtime. Start with `core/unix/loader.c`,
`core/unix/elf_defines.h`, `core/unix/module.c`, and
`core/unix/loader_linux.c`.

`third_party/impl-debug/libbacktrace` is a compact C library with its own ELF
and DWARF reader for stack traces and symbolization. Start with `elf.c`,
`dwarf.c`, `fileline.c`, and `internal.h`.

`third_party/impl-debug/rr` has an in-tree ELF reader used by its record/replay
debugger for build IDs, symbols, dynamic sections, debug links, and interpreter
data. Start with `src/ElfReader.*`, `src/Dwarf.*`, and `src/Monkeypatcher.*`.

#### Reverse engineering and binary analysis (`third_party/impl-re/`)

These references are program-understanding-first: reverse engineering,
decompilation, binary analysis, and symbolic execution.

`third_party/impl-re/radare2` has an in-tree ELF parser and binary plugin. Start
with `libr/bin/format/elf/` and `libr/bin/p/bin_elf*`.

`third_party/impl-re/rizin` has an in-tree ELF parser and binary plugin. Start
with `librz/bin/format/elf/` and `librz/bin/p/bin_elf*`.

`third_party/impl-re/frida-gum` has a fully custom ELF module parser for dynamic
instrumentation used heavily in reverse-engineering workflows. Start with
`gum/gumelfmodule-priv.h`, `gum/gumelfmodule.c`, and `gum/backend-elf/`.

`third_party/impl-re/ghidra` has an in-tree Java ELF parser and loader. Start
with `Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/elf/`,
`ElfLoader.java`, and `ElfProgramBuilder.java`.

`third_party/impl-re/bap` has an in-tree OCaml ELF parser plus an ELF loader
plugin. Start with `lib/bap_elf/` and `plugins/elf_loader/`.

`third_party/impl-re/retdec` has in-tree ELF file-format support for its
decompiler pipeline. Start with `src/fileformat/`,
`include/retdec/fileformat/`, `elf_wrapper.*`, `elf_detector.*`, and
`elf_heuristics.*`.

`third_party/impl-re/dyninst` has ELF object-file support in SymtabAPI. Start
with `symtabAPI/src/Object-elf.C`, `symtabAPI/src/Object-elf.h`, and
`symtabAPI/src/Elf_X.*`.

`third_party/impl-re/cle` is the ELF loader used by the `angr` analysis
framework. Loader/backend logic lives under `cle/backends/elf/`; it adds
loader-level semantics (relocations, TLS, GOT/PLT, eh_frame/LSDA, DWARF
variable types, `metaelf` flags) on top of `third_party/impl-tool/pyelftools`,
which it uses for all low-level ELF parsing.

#### Specs and related work

`third_party/abi/gabi` and `third_party/abi/x86-64-abi` are the primary
specification references. Use `abi/gabi/docsrc/elf/*.rst` for generic ELF and
dynamic-linking rules, and `abi/x86-64-abi` for x86-64 psABI relocation and
processor-specific details.

`third_party/related-elf/elfsage`, `third_party/related-elf/linksem`,
`third_party/related-elf/minimal-elf`, and `third_party/related-elf/veriload`
are adjacent ELF analysis, semantics, and verified loading references.

`third_party/related-parser/daedalus`, `third_party/related-parser/everparse`,
and `third_party/related-parser/vest` are parser DSL / verified parser framework
references.

`third_party/related-parser/formatfuzzer` is a binary-format fuzzing and parsing
framework that can generate high-coverage inputs from format specifications.

`third_party/related-parser/kaitai-struct-formats` contains
`executable/elf.ksy`, a practical declarative ELF format spec.
