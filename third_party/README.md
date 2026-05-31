# third_party

Shared, pinned references for the LeanLoad umbrella checkout.

```text
abi/       ELF ABI standards and psABI references
loader/    libc, dynamic loader, and ELF tooling implementations
lean/      Lean tooling, books, and reference libraries
formats/   parser/schema/formal binary-format references
related/   related verified-loader, ELF, and systems work
```

Implementation repos should prefer a `THIRD_PARTY_DIR` setting or paths through
the umbrella checkout instead of adding duplicate submodules. Keep deliberately
different version pins local to the consuming repo until they are reconciled.
