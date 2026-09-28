---
type: Feature
title: Installation, Upgrade, and Removal
description: One-line installers for macOS/Linux/Windows, version pinning, manual release archives, source builds, and uninstall.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/installation.md
tags:
  - installation
  - install-sh
  - juliaup
  - sysimage
  - releases
status: draft
stale_after: 2026-12-27T16:56:53Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:56:53Z
sources:
  - id: docs-installation
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/installation.md
    title: Installation guide
  - id: install-sh
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/install.sh
    title: macOS/Linux installer
  - id: install-ps1
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/install.ps1
    title: Windows installer
  - id: project-toml
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/Project.toml
    title: Version, deps, Julia compat
---

# Summary

One-line installers fetch a platform archive from GitHub Releases into `~/.friedman-cli/` and put `friedman` on PATH. The installer first ensures Julia 1.13 (via juliaup — installing juliaup itself when needed — without changing the default Julia), resolves the version (latest via the GitHub API, or a pinned `--version` / `$env:FRIEDMAN_VERSION`), downloads `friedman-vX.Y.Z-<platform>-<arch>.tar.gz` (`.zip` on Windows), verifies `checksums.sha256` when possible, extracts with safe replacement of the old install, and symlinks `~/.local/bin/friedman` (macOS/Linux) or extends the user PATH (Windows). Re-running upgrades; removal is one `rm`. From source, `Pkg.instantiate()` plus `julia --project bin/friedman` is enough, or `julia build_release.jl` builds a local sysimage.

# Functions

| Step | macOS/Linux (`install.sh`) | Windows (`install.ps1`) |
|---|---|---|
| Quick install | `curl -fsSL .../install.sh \| bash` | `irm .../install.ps1 \| iex` |
| Pin a version | `bash -s -- --version 1.0.0` | `$env:FRIEDMAN_VERSION = "1.0.0"; irm ... \| iex` |
| Archive name | `friedman-vX.Y.Z-darwin-arm64.tar.gz` / `-linux-x86_64.tar.gz` | `friedman-vX.Y.Z-windows-x86_64.zip` |
| Julia bootstrap | juliaup, or existing Julia ≥ 1.13 kept | juliaup via winget, or existing Julia ≥ 1.13 kept |
| Install dir | `~/.friedman-cli/`, shim `~/.local/bin/friedman` | `%USERPROFILE%\.friedman-cli\`, `bin` on user PATH |
| Uninstall | `rm -rf ~/.friedman-cli ~/.local/bin/friedman` | Remove dir + `%USERPROFILE%\.friedman-cli\bin` from PATH |

Requirements and build-from-source (from `docs/src/installation.md`, `Project.toml`):

| Item | Value |
|---|---|
| Julia | `>= 1.13` (compat `julia = "1.13"`; installer adds 1.13 via juliaup) |
| CLI version | `1.0.0` (single source of truth: `Project.toml`, read as `FRIEDMAN_VERSION` at precompile) |
| MacroEconometricModels | `=1.0.0` (exact pin) |
| Source build | `git clone ... && julia --project -e 'using Pkg; Pkg.instantiate()'` |
| Run from source | `julia --project bin/friedman <command> ...` (auto-instantiates when Manifest absent) |
| Local sysimage | `julia build_release.jl`, then `~/.friedman-cli/bin/friedman --version` |

Behavior notes:

- Version fetch failures (e.g. GitHub API rate limits) print a pin-a-version workaround and exit 1; unsupported OS/arch exits 1 with the supported list.
- Checksum verification uses `sha256sum` (Linux) or `shasum -a 256` (macOS); a missing tool or checksums file warns and continues rather than failing.
- Release sysimages use `--strip-metadata` when healthy; x86-64 images target baseline `generic` so the compile fits the Linux runner.
- `bin/friedman-wrapper` prefers `friedman.so` when present, else plain Julia (see [CLI Engine](../configuration/cli-engine.md)).

# Examples

```bash
curl -fsSL https://raw.githubusercontent.com/FriedmanJP/Friedman-cli/master/install.sh | bash
curl -fsSL https://raw.githubusercontent.com/FriedmanJP/Friedman-cli/master/install.sh | bash -s -- --version 1.0.0
friedman --version
rm -rf ~/.friedman-cli ~/.local/bin/friedman
```

```powershell
irm https://raw.githubusercontent.com/FriedmanJP/Friedman-cli/master/install.ps1 | iex
```

```bash
git clone https://github.com/FriedmanJP/Friedman-cli.git
cd Friedman-cli
julia --project -e 'using Pkg; Pkg.instantiate()'
julia --project bin/friedman estimate multivariate var macro.csv --lags 2
```

# See also

* [Architecture](architecture.md) - what the installed launcher executes
* [Testing & Releases](testing.md) - verifying a source checkout and the release record
* [CLI Engine](../configuration/cli-engine.md) - `bin/friedman` vs `bin/friedman-wrapper` dispatch
