#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
}

archive_path() {
  local path=$1
  local url=$2
  local ext=tar

  case "$url" in
    *.tar.gz) ext=tar.gz ;;
    *.tgz) ext=tgz ;;
    *.tar.xz) ext=tar.xz ;;
    *.tar.bz2) ext=tar.bz2 ;;
    *.crate) ext=crate ;;
  esac
  echo "$ROOT/$path.$ext"
}

fetch() {
  local path=$1
  local url=$2
  local dest=$ROOT/$path
  local archive

  echo "==> $path"
  if [[ -d "$dest" ]]; then
    echo "$path"
    return
  fi

  archive=$(archive_path "$path" "$url")
  mkdir -p "$(dirname "$dest")"
  if [[ ! -f "$archive" ]]; then
    run curl -L --fail --silent --show-error -o "$archive" "$url"
  fi
  mkdir -p "$dest"
  run tar -xf "$archive" -C "$dest" --strip-components=1
  echo "$path"
}

fetch "third_party/impl-analysis/angr" \
  "https://github.com/angr/angr/archive/refs/tags/v9.2.220.tar.gz"
fetch "third_party/impl-analysis/async-profiler" \
  "https://github.com/async-profiler/async-profiler/archive/e421f2da900dbb83be097969c30894cb6cc8ba33.tar.gz"
fetch "third_party/impl-analysis/bap" \
  "https://github.com/BinaryAnalysisPlatform/bap/archive/refs/tags/v2.5.0.tar.gz"
fetch "third_party/impl-analysis/breakpad" \
  "https://github.com/google/breakpad/archive/refs/tags/v2024.02.16.tar.gz"
fetch "third_party/impl-analysis/cle" \
  "https://github.com/angr/cle/archive/refs/tags/v9.2.220.tar.gz"
fetch "third_party/impl-analysis/crashpad" \
  "https://github.com/chromium/crashpad/archive/9b439314d0541d42ae4a3cfbf7cad0506d8e9efb.tar.gz"
fetch "third_party/impl-analysis/dyninst" \
  "https://github.com/dyninst/dyninst/archive/refs/tags/v13.0.0.tar.gz"
fetch "third_party/impl-analysis/ghidra" \
  "https://github.com/NationalSecurityAgency/ghidra/archive/refs/tags/Ghidra_12.1_build.tar.gz"
fetch "third_party/impl-analysis/manticore" \
  "https://files.pythonhosted.org/packages/b0/72/9bb5ac53cf0aad3ca27f3ba1388dc99ffa1a63d110236b26da8ac2bb1a35/manticore-0.3.7.tar.gz"
fetch "third_party/impl-analysis/radare2" \
  "https://github.com/radareorg/radare2/releases/download/6.1.4/radare2-6.1.4.tar.xz"
fetch "third_party/impl-analysis/retdec" \
  "https://github.com/avast/retdec/archive/refs/tags/v5.0.tar.gz"
fetch "third_party/impl-analysis/rizin" \
  "https://github.com/rizinorg/rizin/releases/download/v0.8.2/rizin-src-v0.8.2.tar.xz"
fetch "third_party/impl-analysis/rr" \
  "https://github.com/rr-debugger/rr/archive/refs/tags/5.9.0.tar.gz"
fetch "third_party/impl-lib/goblin" \
  "https://static.crates.io/crates/goblin/goblin-0.10.7.crate"
fetch "third_party/impl-lib/libbacktrace" \
  "https://github.com/ianlancetaylor/libbacktrace/archive/549b81b43b46c0f361680561a626bf0e7b79dcbd.tar.gz"
fetch "third_party/impl-lib/rust-elf" \
  "https://github.com/cole14/rust-elf/archive/refs/tags/v0.8.0.tar.gz"
fetch "third_party/impl-loader/android-bionic" \
  "https://github.com/aosp-mirror/platform_bionic/archive/refs/tags/android-16.0.0_r1.tar.gz"
fetch "third_party/impl-loader/fex" \
  "https://github.com/FEX-Emu/FEX/archive/a5c3fc475145f269f511e9edce9afe28c188651a.tar.gz"
fetch "third_party/impl-linker/binutils-gdb" \
  "https://ftp.gnu.org/gnu/binutils/binutils-2.46.0.tar.xz"
fetch "third_party/impl-kernel/freebsd-src" \
  "https://github.com/freebsd/freebsd-src/archive/refs/heads/releng/15.0.tar.gz"
fetch "third_party/impl-loader/glibc" \
  "https://ftp.gnu.org/gnu/glibc/glibc-2.43.tar.xz"
fetch "third_party/impl-kernel/illumos-gate" \
  "https://github.com/illumos/illumos-gate/archive/b32229105ff0363d3ca16ede5eeaa6affdba6615.tar.gz"
fetch "third_party/impl-linker/go" \
  "https://go.dev/dl/go1.25.5.src.tar.gz"
fetch "third_party/impl-linker/llvm-project" \
  "https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-22.1.7.tar.gz"
fetch "third_party/impl-kernel/linux" \
  "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.19.tar.xz"
fetch "third_party/impl-loader/qemu" \
  "https://download.qemu.org/qemu-11.0.1.tar.xz"
fetch "third_party/impl-kernel/netbsd-src" \
  "https://github.com/NetBSD/src/archive/refs/heads/netbsd-11.tar.gz"
fetch "third_party/impl-kernel/openbsd-src" \
  "https://github.com/openbsd/src/archive/b67053e1736e5da02fa744e25e1077cb86bfd81c.tar.gz"
fetch "third_party/impl-loader/valgrind" \
  "https://sourceware.org/pub/valgrind/valgrind-3.27.1.tar.bz2"
fetch "third_party/impl-tool/sandboxed-api" \
  "https://github.com/google/sandboxed-api/archive/f0498b496b471e1a2800b5bf99d121a78638d0ab.tar.gz"
fetch "third_party/impl-tool/swift" \
  "https://github.com/swiftlang/swift/archive/85e5036c0699e1fcbad4d30ab41281f5be0fae35.tar.gz"
fetch "third_party/impl-linker/zig" \
  "https://ziglang.org/download/0.15.2/zig-0.15.2.tar.xz"
