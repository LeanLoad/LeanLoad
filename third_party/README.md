# third_party

Shared, pinned references for the LeanLoad umbrella checkout.

```text
abi/              ELF ABI standards and psABI references
impl/             concrete ABI / loader / ELF tool implementations
lean-ref/         Lean tooling, books, and reference libraries
related-elf/      related verified-loader / ELF work
related-lean/     related Lean verification work
related-parser/   related parser / binary-format work
```

Implementation repos should prefer a `THIRD_PARTY_DIR` setting or paths through
the umbrella checkout instead of adding duplicate submodules. Keep deliberately
different version pins local to the consuming repo until they are reconciled.
