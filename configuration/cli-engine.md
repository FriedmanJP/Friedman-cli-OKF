---
type: Feature
title: CLI Engine and Command Registry
description: Custom Comonicon-derived command tree, tokenizer and binder, dispatcher, help printer, CommandSpec adapter, family promotion, and the schema self-description leaf.
resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/cli/dispatch.jl
tags:
  - configuration
  - cli-engine
  - registry
  - dispatch
  - parser
  - schema
status: draft
stale_after: 2026-12-27T16:56:53Z
generated:
  by: friedman-cli-okf/build
  at: 2026-09-28T16:56:53Z
sources:
  - id: src-types
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/cli/types.jl
    title: Entry/Node/Leaf/Argument/Option/Flag structs
  - id: src-parser
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/cli/parser.jl
    title: tokenize, bind_args, convert_value
  - id: src-dispatch
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/cli/dispatch.jl
    title: dispatch node/leaf, envelope accumulation
  - id: src-help
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/cli/help.jl
    title: Colored column-aligned help printer
  - id: src-spec
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/registry/spec.jl
    title: CommandSpec and shared option groups
  - id: src-adapter
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/registry/adapter.jl
    title: wrap_legacy, to_leaf, build_node
  - id: src-families
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/registry/families.jl
    title: Family labels, v1.0.0 promotion, replacement map
  - id: src-schema
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/commands/schema.jl
    title: schema self-description leaf
  - id: src-friedman
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/src/Friedman.jl
    title: build_app, APP, run_cli entry
  - id: bin-friedman
    resource: https://github.com/FriedmanJP/Friedman-cli/blob/66bb97e50df7679fff068b78ed628da8c531e4f4/bin/friedman
    title: bin/friedman launcher
---

# Summary

The CLI framework is custom-built (adapted from Comonicon.jl): `Entry` holds a root `NodeCommand` tree of `NodeCommand`/`LeafCommand` nodes with typed `Argument`/`Option`/`Flag` surfaces. `bin/friedman` activates the project (instantiating when the Manifest is absent, retrying once on load failure) and calls `Friedman.main(ARGS)` → `run_cli`, which intercepts `repl`, strips leading globals, and dispatches: entry-level first-token globals, node tree-walk, then `dispatch_leaf` (`tokenize` → `bind_args` → handler). Every command file declares `CommandSpec`s (path, summary, args/options/flags, tables, handler, data/model/result kinds, family); `register!` finalizes them (family stamping + v1.0.0 path promotion) and `to_leaf`/`build_node` bridge them to the engine. `friedman schema [path...]` exposes the whole tree as raw JSON (not an envelope) with per-leaf draft-07 `input_schema` (`x-cli` argv annotations, `x-handle` roles), declared tables, the contract block (embedded envelope schema + exit taxonomy), and optional `--docs` agent guide.

# Functions

| Item | Kind | Role |
|---|---|---|
| `Entry` / `NodeCommand` / `LeafCommand` | tree | Top-level entry, command group, executable leaf |
| `Argument` / `Option` / `Flag` | surface | Positional, `--opt` with optional choices, boolean `--flag` |
| `tokenize` | parser | Raw tokens → positionals/options/flags; `--opt=val`, `-o val`, bundled `-abc`, `--` stops parsing, repeatable `--set`, negative numbers as values |
| `bind_args` | parser | Bind to declared surface; unknown options error with did-you-mean (Levenshtein ≤ 2); `--model`/--result make `<data>` optional |
| `convert_value` | parser | String → Int/Float64/String/Symbol/Bool with typed errors |
| `dispatch` | dispatch | First-token `--version`/`-V`/`--warranty`/`--conditions`, top-level help, then node walk |
| `dispatch_node` | dispatch | Match group name, recurse; `schema` takes a dedicated varpath dispatcher; unknown names raise `DispatchError` (exit 2) with replacement hint |
| `dispatch_leaf` | dispatch | `-h`/`--help` anywhere prints leaf help; empty invocation with required positionals prints help; JSON mode accumulates one envelope, render-then-rethrow on error |
| `print_help` | help | Colored `Usage:` + family-grouped subcommands / args / options / flags |
| `CommandSpec` / `ArgSpec` / `OptionSpec` / `FlagSpec` / `TableSpec` | registry | Declarative leaf declaration incl. stable envelope table keys |
| `wrap_legacy` | adapter | kwargs handler → `CmdContext`: stem resolution, kind checks, handle load/inject, `--save-*` persist, config merge |
| `to_leaf` / `build_node` | adapter | Spec → engine nodes (depth-2 and depth-3 paths; kebab primary only, no aliases) |
| `_finalize_spec` / `_promote_path` | families | Stamp family; promote `estimate <leaf>` → `estimate <family> <leaf>`, `did test` → `test did`, `dsge ha` → `hadsge`; replacements in `_PATH_REPLACEMENTS` |
| `model_catalog` / `catalog_specs` | families | One row per model token across estimate/predict/residuals/forecast verbs |
| `friedman schema [path...]` | leaf | Raw-JSON self-description; `--docs` embeds the agent guide; `--output` writes to file |
| `bin/friedman` | launcher | `Pkg.activate` + instantiate-once + `Friedman.main(ARGS)` |
| `bin/friedman-wrapper` | launcher | Uses `friedman.so` sysimage when present, else plain Julia |

Shared option groups (from `src/registry/spec.jl`):

| Group | Contents |
|---|---|
| `OUTPUT_OPTIONS` | `--format`/`-f` (table\|csv\|json), `--output`/`-o` |
| `PLOT_OPTIONS` + `PLOT_FLAGS` | `--plot-save`, `--plot` |
| `SAVE_MODEL_OPTION` / `MODEL_OPTION` | `--save-model`, `--model` (handle) |
| `RESULT_OPTION` / `SAVE_RESULT_OPTION` | `--result`, `--save-result` (handles; added only when `result_types` nonempty) |
| `CONFIG_ERGONOMICS_OPTIONS` + `STRICT_FLAG` | `--config-json`, repeatable `--set`, `--strict` (added only when `--config` declared) |
| `REG_OPTIONS`, `PREG_OPTIONS`, `SARIMA_OPTIONS`, `COUNT_*`, `BAYES_OPTIONS` | Family option sets composed by name |

Dispatch flags on the `schema` leaf:

| Option/Flag | Type | Default | Description |
|---|---|---|---|
| `--format` / `-f` | `String` | `json` | Always json (raw schema document); choices: `json` |
| `--output` / `-o` | `String` | `""` | Write schema JSON to file |
| `--docs` | flag | `false` | Embed the agent guide as a `docs` markdown string |

# Examples

```bash
friedman --version
friedman estimate --help
friedman estimate multivariate var --help
friedman schema estimate multivariate var | jq .input_schema
friedman schema --docs | jq -r .docs | head -n 40
julia --project bin/friedman --version
```

# See also

* [Config Files & Schema](config-files.md) - `--config` ergonomics wired through `wrap_legacy`
* [Handles & Output](output-envelope.md) - globals, envelope accumulation in `dispatch_leaf`
* [Installation](../installation-architecture/installation.md) - release launcher and sysimage behind `friedman-wrapper`
