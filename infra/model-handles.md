---
type: Feature
title: Model Handles (info, reproduce)
description: Inspect and bit-for-bit verify saved model handles (.jld2 native, .fmod interim, model:// session) via model info and model reproduce.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/model.md
tags:
  - infra
  - model-handles
  - reproduce
  - jld2
  - fmod
status: draft
stale_after: 2026-12-27T16:56:53Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:56:53Z
sources:
  - id: generated-model
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/docs/src/commands/generated/model.md
    title: Generated model reference (2 leaves)
  - id: src-model
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/model.jl
    title: model info / reproduce handler source
  - id: src-model-handle
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/model_handle.jl
    title: .fmod header, version checks, native/JLD2 dispatch
---

# Summary

The `model` group holds exactly two leaves: `model info` reads a handle header (magic, model type, writing vs runtime CLI/MEMs versions, dimensions) without re-running estimation, and `model reproduce` re-runs the estimator from the recorded seed and diffs fields bit-for-bit. Both accept `.jld2` (native MEMs `save_model`), `.fmod` (interim Serialization with a `FRIEDMAN_FMOD_v1` header), and `model://` serve-session handles.

LEAVES.md open question 2 resolved: `model.md` has exactly `friedman model info` and `friedman model reproduce` — there is no `schema` leaf in this file. `schema` is a separate registry-hidden singleton leaf (`friedman schema [path...]`, `src/commands/schema.jl`) with its own dispatcher and raw-JSON output; see [CLI Engine](../configuration/cli-engine.md).

# Functions

| Leaf | Summary | Output tables |
|---|---|---|
| `friedman model info` | Inspect a handle: type, versions, dimensions | `model_handle_info` |
| `friedman model reproduce` | Verify a handle by re-running its estimator from the recorded seed | `model_reproduce_summary`, `model_reproduce_fields` (only when field diffs exist) |

`model info` arguments:

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | `String` | yes | Path to `.jld2`/`.fmod` handle or `model://` session handle |

`model info` options:

| Option | Short | Type | Default | Choices | Description |
|---|---|---|---|---|---|
| `--output` | `-o` | `String` | `""` | — | Export results to file |
| `--format` | `-f` | `String` | `table` | `table`, `csv`, `json` | table\|csv\|json |

`model reproduce` arguments:

| Argument | Type | Required | Description |
|---|---|---|---|
| `path` | `String` | yes | Handle path (`.jld2`, `.fmod`, or `model://` session handle) |

`model reproduce` options:

| Option | Short | Type | Default | Choices | Description |
|---|---|---|---|---|---|
| `--output` | `-o` | `String` | `""` | — | Export results to file |
| `--format` | `-f` | `String` | `table` | `table`, `csv`, `json` | table\|csv\|json |

Behavior notes (from `src/commands/model.jl`, `src/model_handle.jl`):

- `model info` on `model://` describes the live serve-session object (magic reads `serve-session (model://)`); on `.jld2` it reads the native header; otherwise the `.fmod` header. A native-only `note` row appears when the header carries one.
- `model reproduce` exit is 0 whenever the handle loads: `matched=true` is bit-for-bit equality, `matched=missing` renders `unverifiable (no recorded seed)` (no seed recorded, or a type upstream never implemented `reproduce` for). Only an unloadable handle errors.
- `.fmod` loads enforce exact CLI and MEMs version equality (`env/model-version`, exit 6); a bad magic or corrupt payload is also exit 6. Native `.jld2` uses MEMs' own versioned registry (352 types at v1.0.0).
- The reproduce report records `threads_captured → threads_current`: a thread-count change can break bit-equality honestly.

# Examples

```bash
friedman estimate multivariate var macro.csv --lags 2 --save-model var
friedman model info var
friedman model info var.jld2 --format json
friedman model reproduce var --seed 7
```

# See also

* [Serve & Show](serve-show.md) - `show` renders any handle's payload; `serve --mcp` hosts `model://` handles
* [REPL & Completions](repl-completions.md) - in-memory result cache as the alternative to `--save-model` files
* [Handles & Output](../configuration/output-envelope.md) - stem resolution and the `.jld2`/`.fmod` save rules
