#!/usr/bin/env python3
"""Fetch third_party references as pinned source trees."""

from __future__ import annotations

import argparse
import shutil
import shlex
import subprocess
import sys
import tarfile
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Source:
    path: str
    url: str
    commit: str
    sparse: tuple[str, ...] = ()


@dataclass(frozen=True)
class RunResult:
    output: str
    returncode: int


class FetchError(Exception):
    def __init__(self, source: Source, output: str) -> None:
        super().__init__(source.path)
        self.source = source
        self.output = output


SOURCES = [
    Source(
        "third_party/impl-analysis/angr",
        "https://github.com/angr/angr/archive/refs/tags/v9.2.220.tar.gz",
        "61783949b0ee583e926b0846127a79870972f43f",
    ),
    Source(
        "third_party/impl-analysis/bap",
        "https://github.com/BinaryAnalysisPlatform/bap/archive/refs/tags/v2.5.0.tar.gz",
        "caae08349e43ad744ca0160a17d77428f843829d",
    ),
    Source(
        "third_party/impl-analysis/cle",
        "https://github.com/angr/cle/archive/refs/tags/v9.2.220.tar.gz",
        "dfc03032b8216dcffbf61320c6c0711310eaaeba",
    ),
    Source(
        "third_party/impl-analysis/dyninst",
        "https://github.com/dyninst/dyninst/archive/refs/tags/v13.0.0.tar.gz",
        "268b6300b59d507317b6c342ae9588eb6fedf2ac",
    ),
    Source(
        "third_party/impl-analysis/ghidra",
        "https://github.com/NationalSecurityAgency/ghidra/archive/refs/tags/Ghidra_12.1_build.tar.gz",
        "7e89d94e3478f0b1931c34882a0f606fdb06961f",
    ),
    Source(
        "third_party/impl-analysis/manticore",
        "https://github.com/trailofbits/manticore/archive/refs/tags/0.3.7.tar.gz",
        "9ed66b6970b16d783a387363cadfd4841b547a04",
    ),
    Source(
        "third_party/impl-analysis/radare2",
        "https://github.com/radareorg/radare2/archive/refs/tags/6.1.4.tar.gz",
        "4661541e40947fbc269b0c2686d1cd52ad69c1dc",
    ),
    Source(
        "third_party/impl-analysis/retdec",
        "https://github.com/avast/retdec/archive/refs/tags/v5.0.tar.gz",
        "53e55b4b26e9b843787f0e06d867441e32b1604e",
    ),
    Source(
        "third_party/impl-analysis/rizin",
        "https://github.com/rizinorg/rizin/archive/refs/tags/v0.8.2.tar.gz",
        "5a611eee2999d312317ff90d600e37dde0f58992",
    ),
    Source(
        "third_party/impl-lib/rust-elf",
        "https://github.com/cole14/rust-elf/archive/refs/tags/v0.8.0.tar.gz",
        "c4d5222a34a97e113f863f80399284767d725e28",
    ),
    Source(
        "third_party/impl-loader/android-bionic",
        "https://android.googlesource.com/platform/bionic",
        "731631f300090436d7f5df80d50b6275c8c60a93",
        ("linker", "libdl", "libc"),
    ),
    Source(
        "third_party/impl-linker/binutils-gdb",
        "https://sourceware.org/git/binutils-gdb.git",
        "6b7aea6e0c3a0c9fa4d9392952a5fe53f46120d2",
        ("bfd", "binutils", "gas", "include", "ld"),
    ),
    Source(
        "third_party/impl-kernel/freebsd-src",
        "https://github.com/freebsd/freebsd-src.git",
        "b53eab322946e88fb95ea4e143d1147d3de18d04",
        ("libexec/rtld-elf", "sys/sys"),
    ),
    Source(
        "third_party/impl-loader/glibc",
        "https://sourceware.org/git/glibc.git",
        "79dbb41f159a4defe75f59a8f491d136236d1f7a",
        ("elf", "sysdeps"),
    ),
    Source(
        "third_party/impl-kernel/illumos-gate",
        "https://github.com/illumos/illumos-gate.git",
        "b32229105ff0363d3ca16ede5eeaa6affdba6615",
        ("usr/src/cmd/sgs/rtld", "usr/src/cmd/sgs/libld", "usr/src/uts/common/sys"),
    ),
    Source(
        "third_party/impl-linker/go",
        "https://github.com/golang/go.git",
        "7bd807271cf4ee370b1a2499e863c4fcb6bf7301",
        ("src/debug/elf", "src/cmd/link/internal/ld", "src/cmd/link/internal/loader"),
    ),
    Source(
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
    Source(
        "third_party/impl-kernel/linux",
        "https://github.com/torvalds/linux.git",
        "174914ea551314c52a61713b9c4bde9e42d48073",
        (
            "fs/binfmt_elf.c",
            "fs/binfmt_elf_fdpic.c",
            "include/linux/elfcore.h",
            "include/uapi/linux/elf.h",
            "arch/*/include/asm/elf.h",
            "arch/*/include/uapi/asm/elf.h",
        ),
    ),
    Source(
        "third_party/impl-loader/qemu",
        "https://gitlab.com/qemu-project/qemu.git",
        "81cc5f39aa3042e9c0b2ea772b42a2c8b1488e76",
        ("bsd-user", "hw/core", "include/hw", "linux-user"),
    ),
    Source(
        "third_party/impl-kernel/netbsd-src",
        "https://github.com/NetBSD/src.git",
        "c56a2ae17f7f85c3b1d752220b58d2b54c0ed9a2",
        ("libexec/ld.elf_so", "sys/sys"),
    ),
    Source(
        "third_party/impl-kernel/openbsd-src",
        "https://github.com/openbsd/src.git",
        "b67053e1736e5da02fa744e25e1077cb86bfd81c",
        ("libexec/ld.so", "sys/sys"),
    ),
    Source(
        "third_party/impl-loader/valgrind",
        "https://sourceware.org/git/valgrind.git",
        "a6abdae7a109100b08ba280842f3f9278b7fbebf",
        ("coregrind/m_ume", "coregrind/m_debuginfo", "include"),
    ),
    Source(
        "third_party/impl-linker/zig",
        "https://github.com/ziglang/zig.git",
        "738d2be9d6b6ef3ff3559130c05159ef53336224",
        ("lib/std/elf.zig", "src/arch", "src/link/Elf", "src/link/Elf.zig"),
    ),
]


def positive_int(value: str) -> int:
    result = int(value)
    if result < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return result


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> RunResult:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output = "+ " + shlex.join(cmd) + "\n" + result.stdout
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd, output=output)
    return RunResult(output, result.returncode)


def source_marker(source: Source) -> str:
    mode = "git-sparse" if source.sparse else "archive"
    return f"mode={mode}\nurl={source.url}\ncommit={source.commit}\n"


def safe_extract(archive: tarfile.TarFile, dest: Path) -> None:
    dest = dest.resolve()
    for member in archive.getmembers():
        target = (dest / member.name).resolve()
        if dest != target and dest not in target.parents:
            raise RuntimeError(f"unsafe archive member path: {member.name}")
        if member.issym() or member.islnk():
            link_target = (target.parent / member.linkname).resolve()
            if dest != link_target and dest not in link_target.parents:
                raise RuntimeError(f"unsafe archive link target: {member.name}")
    archive.extractall(dest)


def replace_tree(source: Source, extracted: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.move(str(extracted), dest)
    (dest / ".leanload-source").write_text(source_marker(source), encoding="utf-8")


def fetch_archive(source: Source, dest: Path) -> str:
    output = [f"==> {source.path}\n"]
    marker = dest / ".leanload-source"
    if marker.exists() and marker.read_text(encoding="utf-8") == source_marker(source):
        output.append(f"{source.path}\n")
        return "".join(output)

    with tempfile.TemporaryDirectory(prefix="fetch-", dir=dest.parent) as temp_name:
        temp = Path(temp_name)
        tarball = temp / "source.tar.gz"
        output.append(
            run(
                ["curl", "-L", "--fail", "--silent", "--show-error", "-o", str(tarball), source.url]
            ).output
        )
        extract_dir = temp / "extract"
        extract_dir.mkdir()
        with tarfile.open(tarball, "r:gz") as archive:
            safe_extract(archive, extract_dir)
        roots = [path for path in extract_dir.iterdir() if path.is_dir()]
        if len(roots) != 1:
            raise RuntimeError(f"{source.path} archive should contain exactly one root directory")
        replace_tree(source, roots[0], dest)

    output.append(f"{source.path}\n")
    return "".join(output)


def fetch_git_sparse(source: Source, dest: Path) -> str:
    output = [f"==> {source.path}\n"]
    if dest.exists() and not ((dest / ".git").exists()):
        if any(dest.iterdir()):
            raise RuntimeError(f"{source.path} exists but is not a git checkout")
        dest.rmdir()

    if not dest.exists():
        output.append(run(["git", "clone", "--filter=blob:none", "--no-checkout", source.url, str(dest)]).output)

    output.append(run(["git", "sparse-checkout", "init", "--no-cone"], cwd=dest).output)
    output.append(run(["git", "sparse-checkout", "set", *source.sparse], cwd=dest).output)
    shallow = run(
        ["git", "fetch", "--filter=blob:none", "--depth", "1", "origin", source.commit],
        cwd=dest,
        check=False,
    )
    output.append(shallow.output)
    if shallow.returncode != 0:
        output.append(run(["git", "fetch", "--filter=blob:none", "origin", source.commit], cwd=dest).output)
    output.append(run(["git", "checkout", "--detach", source.commit], cwd=dest).output)
    output.append(f"{source.path}\n")
    return "".join(output)


def fetch(source: Source) -> str:
    dest = ROOT / source.path
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if source.sparse:
            return fetch_git_sparse(source, dest)
        return fetch_archive(source, dest)
    except subprocess.CalledProcessError as error:
        output = [f"==> {source.path}\n"]
        if error.output:
            output.append(str(error.output))
        raise FetchError(source, "".join(output)) from None
    except RuntimeError as error:
        output = [f"==> {source.path}\n"]
        output.append(f"{error}\n")
        raise FetchError(source, "".join(output)) from None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-j",
        "--jobs",
        type=positive_int,
        default=4,
        help="number of repositories to fetch in parallel (default: 4)",
    )
    parser.add_argument(
        "sources",
        nargs="*",
        help="optional source paths or path suffixes to fetch",
    )
    return parser.parse_args(argv)


def selected_sources(patterns: list[str]) -> list[Source]:
    if not patterns:
        return SOURCES

    selected = [
        source
        for source in SOURCES
        if any(source.path == pattern or source.path.endswith(pattern) for pattern in patterns)
    ]
    matched_patterns = {
        pattern
        for pattern in patterns
        if any(source.path == pattern or source.path.endswith(pattern) for source in SOURCES)
    }
    missing = sorted(set(patterns) - matched_patterns)
    if missing:
        raise SystemExit("unknown source pattern(s): " + ", ".join(missing))
    return selected


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    sources = selected_sources(args.sources)
    if args.jobs == 1:
        for source in sources:
            try:
                print(fetch(source), end="")
            except FetchError as error:
                print(error.output, end="", file=sys.stderr)
                return 1
        return 0

    failures: list[FetchError] = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(fetch, source): source for source in sources}
        for future in as_completed(futures):
            try:
                print(future.result(), end="")
            except FetchError as error:
                print(error.output, end="", file=sys.stderr)
                failures.append(error)

    if failures:
        print("failed sources:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure.source.path}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
