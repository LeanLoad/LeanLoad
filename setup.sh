#!/usr/bin/env bash
# One-shot setup for the shared C toolchain, elan, and fixture dependencies.
# Each Lean submodule pins its own toolchain; elan installs it on first `lake` run.
#
# Large reference/spec submodules are skipped by default. Run
# `git submodule update --init --recursive` if you need them.
set -euxo pipefail
cd "$(dirname "$0")"

sudo apt-get update
sudo apt-get install -y build-essential curl

# Lean
if ! command -v elan >/dev/null 2>&1; then
  curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
    | sh -s -- -y --default-toolchain none
fi

if command -v fish >/dev/null 2>&1; then
  fish -c 'fish_add_path -m ~/.elan/bin/'
else
  export PATH="$HOME/.elan/bin:$PATH"
fi

# Rust
if ! command -v cargo >/dev/null 2>&1; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
fi
if command -v fish >/dev/null 2>&1; then
  fish -c 'fish_add_path -m ~/.cargo/bin/'
else
  export PATH="$HOME/.cargo/bin:$PATH"
fi

# Top-level project repos plus musl libc for ElfLoader example fixtures.
git submodule update --init ElfLoader ELFine ElfZoo LeanOnWasm WhatTheElf
