# ELF handling conformance matrix

Cross-implementation review of ELF format handling across the loader-path
references in `third_party/`, compared against each other and against the ABI
documents in `third_party/abi/{gabi,gnu-gabi,linux-abi,x86-64-abi}`.

Scope (chosen for relevance to a verified loader):

- **rtld** (dynamic loaders): glibc, musl, Android bionic, uClibc-ng
- **kernel-exec** (program loaders): Linux `binfmt_elf`, FreeBSD `imgact_elf`,
  NetBSD/OpenBSD `exec_elf`, illumos `uts` exec, gVisor
- **lib** (ELF parsers): ELFIO, LIEF, goblin, rust-elf, gimli-object

Focus areas: header/structural validation, segment loading, dynamic/reloc/
symbols, notes & alignment.

## Background

### Section extended numbering (gABI)

`e_shnum` and `e_shstrndx` are 16-bit, and indices `>= SHN_LORESERVE (0xff00)`
are reserved, so real values can never legally fill those fields. The gABI
escape stores the real values in the otherwise-unused initial section header
(index 0, the `SHN_UNDEF` entry):

- real section count `>= SHN_LORESERVE` -> `e_shnum = 0`, actual count in
  `section[0].sh_size`
- real shstrtab index `>= SHN_LORESERVE` -> `e_shstrndx = SHN_XINDEX (0xffff)`,
  actual index in `section[0].sh_link`
- symbol section index `>= SHN_LORESERVE` -> `st_shndx = SHN_XINDEX`, real index
  in a parallel `SHT_SYMTAB_SHNDX` table

Only components that read the section header table can implement this (excludes
the rtlds, which never read section headers, and the program loaders, which
work from program headers).

### PN_XNUM (program-header analogue)

The analogous program-header escape `PN_XNUM` (`e_phnum = 0xffff`, real count in
`section[0].sh_info`) is **not** in the core gABI text in this repo — it is a
GNU convention. This is why support for it differs from the section escapes.

### Other items absent from the core gABI text here

- partial-last-page zeroing of `PT_LOAD` (only the abstract "extra bytes hold 0"
  guarantee is stated)
- `DT_RELR` / `SHT_RELR` packed relocations (absent from all four doc trees)
- GNU hash and symbol versioning (GNU extensions, in `gnu-gabi` only)
- note alignment: the core gABI mandates 8-byte note alignment for ELFCLASS64;
  `linux-abi`/`gnu-gabi` override this, directing parsers to use `p_align` and
  forcing `.note.ABI-tag` / `.note.gnu.build-id` to 4-byte even on 64-bit.

## Matrix

**Legend:** `Y` supports/enforces/conforms; `N` does not (or non-conforming);
`~` partial, config-gated, lenient, or implicit; `-` not applicable to this
component type.

Reference = practical GNU/Linux ABI (`linux-abi` + `gnu-gabi`); gABI-literal
deviations are in the footnotes.

### Header / structural validation

| Rule | glibc | musl | bionic | uClibc | Linux | FreeBSD | NetBSD | OpenBSD | illumos | gVisor | ELFIO | LIEF | goblin | rust-elf | gimli |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Magic checked | Y | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| EI_CLASS validated | Y | N | Y | ~¹ | ~² | Y | Y | Y | Y | Y | Y | ~³ | Y | Y | Y |
| EI_DATA (endianness) validated | Y | N | Y | N | N² | Y | N | Y | Y | Y | Y | ~³ | Y | Y | Y |
| EI_VERSION validated | Y | N | Y | ~¹ | N | Y | N | Y | N | Y | N | N | N | Y | Y |
| `e_phentsize == sizeof(Phdr)` enforced | Y | N | N | N | Y | Y | N | N | ~⁴ | Y | ~⁵ | N | N | Y | Y |
| **PN_XNUM** (`e_phnum==0xffff`) supported | N | N | N | N | N | N | N | N | Y | N | N | N | N | Y | Y |
| **Ext. section count** (`e_shnum==0`->`sh_size`) | - | - | N⁶ | - | - | - | - | - | Y | - | N | N | Y | Y | Y |
| **Ext. shstrndx** (`SHN_XINDEX`->`sh_link`) | - | - | N | - | - | - | - | - | Y | - | N | N | Y | Y | Y |
| `ET_EXEC` loadable/accepted | Y | Y | N⁷ | ~⁸ | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |

### Segment loading (parsers don't map -> `-`)

| Rule | glibc | musl | bionic | uClibc | Linux | FreeBSD | NetBSD | OpenBSD | illumos | gVisor | ELFIO | LIEF | goblin | rust-elf | gimli |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `p_align` power-of-2 checked | N | N | ~⁹ | N | N⁹ | Y | N | Y | N | N | - | - | - | - | - |
| `p_align` congruence (`vaddr≡offset mod p_align`) | N¹⁰ | N | N | N | ~¹¹ | N | Y | N | ~¹² | ~¹¹ | - | - | - | - | - |
| `p_memsz >= p_filesz` enforced | N | N | N | N¹³ | Y | Y | N | Y | Y | N | - | - | - | - | - |
| Tolerates unordered `PT_LOAD` | N | Y | Y | N | N | N | N | N | N | N¹⁴ | - | - | - | - | - |
| `PT_GNU_RELRO` honored | Y | Y | Y | ~¹⁵ | N¹⁶ | N¹⁶ | N¹⁶ | Y | N | N | - | - | - | - | - |
| `PT_GNU_STACK` exec bit honored | Y | ~¹⁷ | - | N | Y | Y | ~¹⁸ | N¹⁹ | ~ | N | - | - | - | - | - |
| W^X enforced at map time | N | N | Y | N | N | N | N | Y | N | N | - | - | - | - | - |

### Dynamic / reloc / symbols (kernels don't link -> `-`)

| Rule | glibc | musl | bionic | uClibc | Linux | FreeBSD | NetBSD | OpenBSD | illumos | gVisor | ELFIO | LIEF | goblin | rust-elf | gimli |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DT_HASH | Y | Y | Y | Y | - | - | - | - | - | - | Y | Y | Y | Y | Y |
| DT_GNU_HASH (preferred) | Y | Y | Y | ~²⁰ | - | - | - | - | - | - | Y | Y | Y | Y | Y |
| Symbol versioning (VERNEED/VERDEF) | Y | N²¹ | Y | N | - | - | - | - | - | - | Y | Y | Y | Y | Y |
| REL **and** RELA | Y | Y | Y | ~²² | - | - | - | - | - | - | Y | Y | Y | Y | Y |
| **DT_RELR** packed relocs | Y | Y | Y | ~²⁰ | - | - | - | - | - | - | N | Y | N | N | Y |
| DT_TEXTREL allowed (text relocs) | Y | Y | N²³ | Y | - | - | - | - | - | - | ~²⁴ | ~²⁴ | ~²⁴ | ~²⁴ | ~²⁴ |
| Lazy binding (PLT) | Y | N²⁵ | N²⁵ | Y | - | - | - | - | - | - | - | - | - | - | - |

### Notes & alignment

| Rule | glibc | musl | bionic | uClibc | Linux | FreeBSD | NetBSD | OpenBSD | illumos | gVisor | ELFIO | LIEF | goblin | rust-elf | gimli |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Reads/acts on notes at load | Y | N | Y | N | Y²⁶ | Y | Y | Y | N | N | n/a | n/a | n/a | n/a | n/a |
| Note align from `p_align`/`sh_addralign` (not hardcoded 4) | Y | - | N²⁷ | - | ~²⁸ | N | N | N | - | - | N | N | Y | Y | Y |
| 8-byte note descriptor (ELF64) supported | Y | - | N | - | ~²⁸ | N | N | N | - | - | N | N | Y | Y | Y |
| GNU-property note consumed -> CET/BTI | Y | N | Y | N | Y | N | N | N | N | N | N | Y²⁹ | N | N | Y²⁹ |

## Footnotes

1. uClibc bootstrap self-check validates CLASS+VERSION; the DSO-load path checks
   neither (only magic + `e_machine`).
2. Linux pins class at compile time (32-bit via `compat_binfmt_elf`); no explicit
   in-binary CLASS/DATA reject — wrong endianness is caught only indirectly by
   `elf_check_arch`.
3. LIEF auto-detects and **prefers `e_machine`** over `EI_CLASS`/`EI_DATA` when
   they conflict.
4. illumos requires `e_phentsize >= MINPHENTSZ` (a minimum, not exact).
5. ELFIO requires `>= sizeof(Phdr)` then uses the field as stride.
6. **bionic actively rejects** `e_shnum==0` ("has no section headers") — it
   refuses a legally extended-count object.
7. **bionic accepts only `ET_DYN`**; non-PIE `ET_EXEC` cannot load through it.
8. uClibc accepts `ET_EXEC` only when built `__LDSO_STANDALONE_SUPPORT__`.
9. bionic warns and skips non-pow2 `p_align` (no reject); Linux silently ignores
   non-pow2 when computing max alignment; FreeBSD rejects with `ENOEXEC`.
10. glibc checks congruence only **mod page size**, not mod `p_align`.
11. Enforced indirectly: `mmap` rejects a file offset not page-congruent with the
    vaddr.
12. illumos silently **falls back to copy-in** on a page-congruence mismatch
    instead of erroring.
13. uClibc has an unsigned **underflow bug** (`MIN(..., p_memsz - p_filesz)`)
    when `p_memsz < p_filesz`.
14. **gVisor rejects** out-of-order `PT_LOAD` even though the real Linux kernel
    allows it (documented divergence).
15. uClibc honors RELRO only with an MMU.
16. The Linux/FreeBSD/NetBSD **kernels** leave RELRO to userspace ld.so;
    OpenBSD's kernel handles it via its immutability machinery.
17. musl reads only the GNU_STACK **size**, ignoring the exec bit.
18. NetBSD defers exec-stack policy to PaX.
19. OpenBSD does not even define `PT_GNU_STACK`.
20. uClibc: GNU hash and DT_RELR only when compiled in (and non-FDPIC).
21. **musl reads only the `DT_VERSYM` hidden bit** — no VERNEED/VERDEF name
    matching, so it can bind a different symbol than glibc.
22. uClibc does exactly one of REL/RELA per build (arch-fixed); the other is
    hard-refused.
23. **bionic forbids DT_TEXTREL on LP64**, gates it by target-SDK on 32-bit.
24. Libraries only *parse/expose* the tag (goblin tracks it as a bool); they do
    not relocate, so "allowed" is loader semantics.
25. **musl and bionic are eager-only**; `DT_BIND_NOW`/PLTGOT/TLSDESC lazy entries
    are ignored.
26. Linux's only load-time note consumer is `PT_GNU_PROPERTY` (it does **not**
    read `.note.ABI-tag`).
27. bionic hardcodes 4-byte note alignment even on LP64 (its inner GNU-property
    array does use pointer alignment).
28. Linux uses **8-byte** alignment for the GNU-property note specifically
    (`ELF64_GNU_PROPERTY_ALIGN`) but 4-byte for core-dump notes — internally
    asymmetric.
29. LIEF and gimli give `NT_GNU_PROPERTY_TYPE_0` structured parsing; gimli
    deliberately uses **class-based** (8 for ELF64) alignment for the property
    array rather than the section's `sh_addralign`.

## Key takeaways

- **Extended numbering** (PN_XNUM + the two section escapes) is supported by only
  3 of 15 implementations (illumos, rust-elf, gimli). ELFIO/LIEF/goblin and every
  rtld/kernel-exec path are non-conforming. bionic actively rejects extended
  section counts.
- **Note descriptor alignment has no consensus rule.** glibc/goblin/gimli/rust-elf
  honor `p_align`; bionic/ELFIO/LIEF/FreeBSD/NetBSD/OpenBSD hardcode 4; Linux uses
  8 for GNU-property notes but 4 for core-dump notes.
- **`p_align` validation**: NetBSD checks congruence but not power-of-2; OpenBSD
  checks power-of-2 but not congruence — exact complements. FreeBSD rejects a
  non-power-of-2 `p_align` that Linux silently ignores.
- **`p_memsz >= p_filesz`** (a hard gABI invariant) is unenforced by half the
  loaders; uClibc mishandles it via unsigned underflow.
- **Header validation strictness** ranges from glibc (strict: OSABI, padding) to
  musl (checks nothing — relies on the kernel).
