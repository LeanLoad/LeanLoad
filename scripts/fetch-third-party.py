#!/usr/bin/env python3
"""Fetch large third_party references as sparse, blobless checkouts."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Source:
    path: str
    url: str
    commit: str
    sparse: tuple[str, ...]


SOURCES: dict[str, Source] = {
    "android-bionic": Source(
        "third_party/impl-loader/android-bionic",
        "https://android.googlesource.com/platform/bionic",
        "731631f300090436d7f5df80d50b6275c8c60a93",
        ("linker", "libdl", "libc"),
    ),
    "binutils-gdb": Source(
        "third_party/impl-linker/binutils-gdb",
        "https://sourceware.org/git/binutils-gdb.git",
        "6b7aea6e0c3a0c9fa4d9392952a5fe53f46120d2",
        ("bfd", "binutils", "gas", "include", "ld"),
    ),
    "freebsd-src": Source(
        "third_party/impl-loader/freebsd-src",
        "https://github.com/freebsd/freebsd-src.git",
        "b53eab322946e88fb95ea4e143d1147d3de18d04",
        ("libexec/rtld-elf", "sys/sys"),
    ),
    "glibc": Source(
        "third_party/impl-loader/glibc",
        "https://sourceware.org/git/glibc.git",
        "79dbb41f159a4defe75f59a8f491d136236d1f7a",
        ("elf", "sysdeps"),
    ),
    "go": Source(
        "third_party/impl-linker/go",
        "https://github.com/golang/go.git",
        "7bd807271cf4ee370b1a2499e863c4fcb6bf7301",
        ("src/debug/elf", "src/cmd/link/internal/ld", "src/cmd/link/internal/loader"),
    ),
    "illumos-gate": Source(
        "third_party/impl-loader/illumos-gate",
        "https://github.com/illumos/illumos-gate.git",
        "b32229105ff0363d3ca16ede5eeaa6affdba6615",
        ("usr/src/cmd/sgs/rtld", "usr/src/cmd/sgs/libld", "usr/src/uts/common/sys"),
    ),
    "llvm-project": Source(
        "third_party/impl-linker/llvm-project",
        "https://github.com/llvm/llvm-project.git",
        "80f6b7641ef95d435a9e641970291375e3013cbe",
        (
            "lld/ELF",
            "llvm/include/llvm/Object",
            "llvm/lib/Object",
            "llvm/tools/llvm-objcopy",
            "llvm/tools/llvm-objdump",
            "llvm/tools/llvm-readobj",
        ),
    ),
    "netbsd-src": Source(
        "third_party/impl-loader/netbsd-src",
        "https://github.com/NetBSD/src.git",
        "c56a2ae17f7f85c3b1d752220b58d2b54c0ed9a2",
        ("libexec/ld.elf_so", "sys/sys"),
    ),
    "openbsd-src": Source(
        "third_party/impl-loader/openbsd-src",
        "https://github.com/openbsd/src.git",
        "b67053e1736e5da02fa744e25e1077cb86bfd81c",
        ("libexec/ld.so", "sys/sys"),
    ),
    "qemu": Source(
        "third_party/impl-loader/qemu",
        "https://gitlab.com/qemu-project/qemu.git",
        "81cc5f39aa3042e9c0b2ea772b42a2c8b1488e76",
        ("bsd-user", "hw/core", "include/hw", "linux-user"),
    ),
    "zig": Source(
        "third_party/impl-linker/zig",
        "https://github.com/ziglang/zig.git",
        "738d2be9d6b6ef3ff3559130c05159ef53336224",
        ("lib/std/elf.zig", "src/arch", "src/link/Elf", "src/link/Elf.zig"),
    ),
}


def run(cmd: list[str], cwd: Path | None = None, dry_run: bool = False) -> None:
    print("+ " + " ".join(cmd))
    if not dry_run:
        subprocess.run(cmd, cwd=cwd, check=True)


def fetch(name: str, source: Source, dry_run: bool = False) -> None:
    dest = ROOT / source.path
    if dest.exists() and not ((dest / ".git").exists()):
        if any(dest.iterdir()):
            raise SystemExit(f"{source.path} exists but is not a git checkout")
        if not dry_run:
            dest.rmdir()

    if not dest.exists():
        run(["git", "clone", "--filter=blob:none", "--no-checkout", source.url, str(dest)], dry_run=dry_run)

    run(["git", "sparse-checkout", "init", "--no-cone"], cwd=dest, dry_run=dry_run)
    run(["git", "sparse-checkout", "set", *source.sparse], cwd=dest, dry_run=dry_run)
    try:
        run(["git", "fetch", "--filter=blob:none", "--depth", "1", "origin", source.commit], cwd=dest, dry_run=dry_run)
    except subprocess.CalledProcessError:
        run(["git", "fetch", "--filter=blob:none", "origin", source.commit], cwd=dest, dry_run=dry_run)
    run(["git", "checkout", "--detach", source.commit], cwd=dest, dry_run=dry_run)
    print(f"{name}: {source.path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="*", help="'all' or one or more source names")
    parser.add_argument("--dry-run", action="store_true", help="print commands without running them")
    args = parser.parse_args()

    if args.names == ["list"]:
        for name, source in SOURCES.items():
            print(f"{name:15} {source.path} @ {source.commit}")
        return 0

    names = list(SOURCES) if not args.names or args.names == ["all"] else args.names
    unknown = sorted(set(names) - set(SOURCES))
    if unknown:
        raise SystemExit(f"unknown source(s): {', '.join(unknown)}")

    for name in names:
        fetch(name, SOURCES[name], dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
